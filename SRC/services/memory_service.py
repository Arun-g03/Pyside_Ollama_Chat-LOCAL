"""
Memory Service - Handles LLM memory management across conversations
"""

import os
import json
import hashlib
import re
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from PySide6.QtCore import QObject, Signal
from SRC.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

@dataclass
class MemoryEntry:
    """Represents a single memory entry"""
    id: str
    content: str
    conversation_id: str
    timestamp: str
    importance: float  # 0.0 to 1.0
    tags: List[str]
    memory_type: str  # 'conversation', 'summary', 'fact', 'preference'
    metadata: Dict

@dataclass
class MemorySummary:
    """Represents a conversation summary"""
    id: str
    conversation_id: str
    summary: str
    key_points: List[str]
    timestamp: str
    message_count: int

@dataclass
class LongTermMemoryEntry:
    """Represents a long-term memory entry"""
    type: str  # 'fact', 'preference', 'summary', 'event', 'relationship', 'skill'
    key: Optional[str] = None
    value: Optional[str] = None
    summary: Optional[str] = None
    timestamp: str = ''
    importance: float = 0.5
    tags: List[str] = None
    access_count: int = 0
    last_accessed: str = ''
    context_keywords: List[str] = None  # Keywords for retrieval
    
    def __post_init__(self):
        # Ensure tags is always a list
        if self.tags is None:
            self.tags = []
        if self.context_keywords is None:
            self.context_keywords = []

class MemoryClassifier:
    """Intelligent classifier for determining memory type and importance"""
    
    # Keywords that indicate high importance
    HIGH_IMPORTANCE_KEYWORDS = {
        'name', 'birthday', 'birth', 'born', 'family', 'spouse', 'partner', 'children',
        'job', 'work', 'career', 'profession', 'company', 'employer',
        'home', 'house', 'address', 'city', 'country', 'location',
        'phone', 'email', 'contact', 'emergency',
        'allergy', 'medical', 'health', 'condition', 'medication',
        'password', 'security', 'account', 'bank', 'financial'
    }
    
    # Keywords that indicate preferences
    PREFERENCE_KEYWORDS = {
        'like', 'love', 'hate', 'dislike', 'prefer', 'favorite', 'best', 'worst',
        'enjoy', 'enjoyed', 'enjoying', 'fun', 'boring', 'interesting',
        'music', 'movie', 'book', 'food', 'color', 'hobby', 'sport',
        'style', 'fashion', 'taste', 'opinion', 'think', 'feel'
    }
    
    # Keywords that indicate skills/abilities
    SKILL_KEYWORDS = {
        'can', 'able', 'skill', 'expert', 'proficient', 'know', 'learned',
        'speak', 'language', 'program', 'code', 'write', 'read',
        'play', 'instrument', 'sport', 'game', 'cook', 'drive',
        'degree', 'certification', 'education', 'training'
    }
    
    # Keywords that indicate relationships
    RELATIONSHIP_KEYWORDS = {
        'friend', 'family', 'mother', 'father', 'sister', 'brother',
        'wife', 'husband', 'partner', 'girlfriend', 'boyfriend',
        'colleague', 'boss', 'teacher', 'student', 'neighbor',
        'pet', 'dog', 'cat', 'animal'
    }
    
    @staticmethod
    def classify_message(message: str, role: str = "user") -> Dict:
        """Classify a message and determine its memory characteristics"""
        content = message.lower()
        words = set(re.findall(r'\b\w+\b', content))
        
        # Calculate importance score
        importance = 0.3  # Base importance
        
        # Boost importance for high-value keywords
        high_importance_matches = words.intersection(MemoryClassifier.HIGH_IMPORTANCE_KEYWORDS)
        importance += len(high_importance_matches) * 0.2
        
        # Boost for preference keywords
        preference_matches = words.intersection(MemoryClassifier.PREFERENCE_KEYWORDS)
        importance += len(preference_matches) * 0.15
        
        # Boost for skill keywords
        skill_matches = words.intersection(MemoryClassifier.SKILL_KEYWORDS)
        importance += len(skill_matches) * 0.1
        
        # Boost for relationship keywords
        relationship_matches = words.intersection(MemoryClassifier.RELATIONSHIP_KEYWORDS)
        importance += len(relationship_matches) * 0.15
        
        # Boost for longer, more detailed messages
        if len(message) > 100:
            importance += 0.1
        if len(message) > 200:
            importance += 0.1
            
        # Cap importance at 1.0
        importance = min(importance, 1.0)
        
        # Determine memory type
        memory_type = "conversation"
        if high_importance_matches:
            memory_type = "fact"
        elif preference_matches:
            memory_type = "preference"
        elif skill_matches:
            memory_type = "skill"
        elif relationship_matches:
            memory_type = "relationship"
            
        # Extract context keywords for retrieval
        context_keywords = list(words.intersection(
            MemoryClassifier.HIGH_IMPORTANCE_KEYWORDS |
            MemoryClassifier.PREFERENCE_KEYWORDS |
            MemoryClassifier.SKILL_KEYWORDS |
            MemoryClassifier.RELATIONSHIP_KEYWORDS
        ))
        
        return {
            "importance": importance,
            "memory_type": memory_type,
            "context_keywords": context_keywords,
            "should_store_ltm": importance > 0.5 or memory_type != "conversation"
        }

class MemoryRetriever:
    """Intelligent retriever for finding relevant memories"""
    
    @staticmethod
    def calculate_relevance(query: str, memory_entry: LongTermMemoryEntry) -> float:
        """Calculate relevance score between query and memory entry"""
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        
        # Check direct keyword matches
        if memory_entry.context_keywords:
            keyword_matches = query_words.intersection(set(memory_entry.context_keywords))
            if keyword_matches:
                return len(keyword_matches) / len(memory_entry.context_keywords)
        
        # Check content matches
        content = ""
        if memory_entry.type == "summary":
            content = memory_entry.summary or ""
        else:
            content = memory_entry.value or ""
            
        if content:
            content_words = set(re.findall(r'\b\w+\b', content.lower()))
            word_overlap = len(query_words.intersection(content_words))
            if word_overlap > 0:
                return word_overlap / len(query_words)
        
        return 0.0
    
    @staticmethod
    def get_relevant_memories(query: str, memories: List[LongTermMemoryEntry], 
                            max_results: int = 5, min_relevance: float = 0.1) -> List[Tuple[LongTermMemoryEntry, float]]:
        """Get memories relevant to the query, sorted by relevance"""
        scored_memories = []
        
        for memory in memories:
            relevance = MemoryRetriever.calculate_relevance(query, memory)
            if relevance >= min_relevance:
                scored_memories.append((memory, relevance))
        
        # Sort by relevance (descending) and then by importance (descending)
        scored_memories.sort(key=lambda x: (x[1], x[0].importance), reverse=True)
        
        return scored_memories[:max_results]

class ShortTermMemoryService:
    def __init__(self, max_messages: int = 16, stm_file: str = "memory/short_term_memory.json"):
        self.max_messages = max_messages
        self.stm_file = stm_file
        self.messages: List[Dict] = []
        self._load()
    def _load(self):
        if os.path.exists(self.stm_file):
            try:
                with open(self.stm_file, 'r', encoding='utf-8') as f:
                    self.messages = json.load(f)
            except Exception as e:
                logger.error(f"Error loading STM file: {e}", print_to_terminal=True)
                self.messages = []
    def add_message(self, message: Dict):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        self._save()
    def get_messages(self) -> List[Dict]:
        return self.messages.copy()
    def clear(self):
        self.messages = []
        self._save()
    def _save(self):
        try:
            with open(self.stm_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving STM file: {e}", print_to_terminal=True)

class LongTermMemoryService:
    def __init__(self, ltm_file: str = "memory/long_term_memory.json"):
        self.ltm_file = ltm_file
        self.entries: List[LongTermMemoryEntry] = []
        self._load()
    def _load(self):
        if os.path.exists(self.ltm_file):
            try:
                with open(self.ltm_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = []
                    for entry_data in data:
                        try:
                            # Ensure tags field exists
                            if 'tags' not in entry_data or entry_data['tags'] is None:
                                entry_data['tags'] = []
                            if 'context_keywords' not in entry_data or entry_data['context_keywords'] is None:
                                entry_data['context_keywords'] = []
                            if 'access_count' not in entry_data:
                                entry_data['access_count'] = 0
                            if 'last_accessed' not in entry_data:
                                entry_data['last_accessed'] = ''
                            entry = LongTermMemoryEntry(**entry_data)
                            self.entries.append(entry)
                        except Exception as e:
                            logger.error(f"Error loading LTM entry {entry_data}: {e}", print_to_terminal=True)
                            continue
            except Exception as e:
                logger.error(f"Error loading LTM file: {e}", print_to_terminal=True)
                self.entries = []
    def add_entry(self, entry: LongTermMemoryEntry):
        logger.debug(f"=== LTM ADD ENTRY START ===", print_to_terminal=True)
        logger.debug(f"Adding entry: type='{entry.type}', key='{entry.key}', value='{entry.value}'", print_to_terminal=True)
        logger.debug(f"Current entries count: {len(self.entries)}", print_to_terminal=True)
        
        self.entries.append(entry)
        logger.debug(f"Entry added to memory, new count: {len(self.entries)}", print_to_terminal=True)
        
        logger.debug("Saving to disk...", print_to_terminal=True)
        self._save()
        logger.debug("Save completed", print_to_terminal=True)
        logger.debug(f"=== LTM ADD ENTRY END ===", print_to_terminal=True)
    def get_entries(self, type_filter: Optional[str] = None) -> List[LongTermMemoryEntry]:
        if type_filter:
            return [e for e in self.entries if e.type == type_filter]
        return self.entries.copy()
    def _save(self):
        try:
            logger.debug(f"Saving {len(self.entries)} entries to {self.ltm_file}", print_to_terminal=True)
            with open(self.ltm_file, 'w', encoding='utf-8') as f:
                data_to_save = [asdict(e) for e in self.entries]
                logger.debug(f"Data to save: {data_to_save}", print_to_terminal=True)
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            logger.debug("LTM file saved successfully", print_to_terminal=True)
        except Exception as e:
            logger.error(f"Error saving LTM file: {e}", print_to_terminal=True)
            logger.error(f"Exception type: {type(e)}", print_to_terminal=True)
    def update_access_stats(self, entry: LongTermMemoryEntry):
        """Update access statistics for a memory entry"""
        entry.access_count += 1
        entry.last_accessed = datetime.now().isoformat()
        self._save()

class MemoryService(QObject):
    """Service for managing LLM memory across conversations"""
    
    memory_updated = Signal(list)  # Emits updated memory entries
    summary_updated = Signal(list)  # Emits updated summaries
    
    def __init__(self, max_context_messages: int = 16):
        super().__init__()
        self.stm = ShortTermMemoryService(max_messages=max_context_messages)
        self.ltm = LongTermMemoryService()
        self.memories: List[MemoryEntry] = []
        self.summaries: List[MemorySummary] = []
        self.memory_file = os.path.join("memory", "memories.json")
        self.summaries_file = os.path.join("memory", "summaries.json")
        
        # Initialize classifiers
        self.classifier = MemoryClassifier()
        self.retriever = MemoryRetriever()
        
        os.makedirs("memory", exist_ok=True)
        self._load_memory()
    
    def _load_memory(self):
        """Load memory from disk"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memories = [MemoryEntry(**entry) for entry in data]
            
            if os.path.exists(self.summaries_file):
                with open(self.summaries_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.summaries = [MemorySummary(**summary) for summary in data]
        except Exception as e:
            logger.error(f"Error loading memory: {e}", print_to_terminal=True)
    
    def _save_memory(self):
        """Save memory to disk"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(memory) for memory in self.memories], f, indent=2, ensure_ascii=False)
            
            with open(self.summaries_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(summary) for summary in self.summaries], f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving memory: {e}", print_to_terminal=True)
    
    def add_memory(self, content: str, conversation_id: str, importance: float = 0.5, 
                   tags: List[str] = None, memory_type: str = "conversation", metadata: Dict = None) -> str:
        """Add a new memory entry"""
        memory_id = hashlib.md5(f"{content}{conversation_id}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        memory = MemoryEntry(
            id=memory_id,
            content=content,
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat(),
            importance=importance,
            tags=tags or [],
            memory_type=memory_type,
            metadata=metadata or {}
        )
        
        self.memories.append(memory)
        self._save_memory()
        self.memory_updated.emit(self.memories)
        logger.debug(f"Added memory: {memory_id}")
        return memory_id
    
    def add_summary(self, summary: str, importance: float = 0.5, tags: List[str] = None):
        """Add a conversation summary"""
        summary_id = hashlib.md5(f"{summary}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        memory_summary = MemorySummary(
            id=summary_id,
            conversation_id=summary,
            summary=summary,
            key_points=tags or [],
            timestamp=datetime.now().isoformat(),
            message_count=0
        )
        
        self.summaries.append(memory_summary)
        self._save_memory()
        self.summary_updated.emit(self.summaries)
        logger.debug(f"Added summary: {summary_id}")
        return summary_id
    
    def get_relevant_memories(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Get memories relevant to the current query (simple keyword matching for now)"""
        query_words = set(query.lower().split())
        scored_memories = []
        
        for memory in self.memories:
            score = 0
            content_words = set(memory.content.lower().split())
            
            # Simple relevance scoring
            word_overlap = len(query_words.intersection(content_words))
            score += word_overlap * 0.3
            score += memory.importance * 0.7
            
            # Recency bonus
            memory_time = datetime.fromisoformat(memory.timestamp)
            days_old = (datetime.now() - memory_time).days
            recency_bonus = max(0, 1 - (days_old / 30))  # Decay over 30 days
            score += recency_bonus * 0.2
            
            scored_memories.append((memory, score))
        
        # Sort by score and return top results
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return [memory for memory, score in scored_memories[:limit]]
    
    def intelligent_add_message(self, message: Dict) -> Dict:
        """Intelligently add a message and determine if it should go to LTM"""
        logger.debug(f"=== INTELLIGENT MESSAGE ADDITION START ===", print_to_terminal=True)
        logger.debug(f"Processing message: {message}", print_to_terminal=True)
        
        # Always add to STM
        self.stm.add_message(message)
        logger.debug("Message added to STM", print_to_terminal=True)
        
        # Classify the message
        content = message.get("content", "")
        role = message.get("role", "user")
        
        if role == "user" and content.strip():
            classification = self.classifier.classify_message(content, role)
            logger.debug(f"Message classification: {classification}", print_to_terminal=True)
            
            # If message should be stored in LTM, extract and store facts
            if classification["should_store_ltm"]:
                logger.debug("Message qualifies for LTM storage", print_to_terminal=True)
                
                # Extract facts from the message
                facts = self.extract_facts_from_message(content)
                logger.debug(f"Extracted facts: {facts}", print_to_terminal=True)
                
                # Store each fact in LTM
                for key, value in facts.items():
                    if key and value:
                        self.add_fact(
                            key=key,
                            value=value,
                            importance=classification["importance"],
                            tags=classification["context_keywords"]
                        )
            else:
                logger.debug("Message does not qualify for LTM storage", print_to_terminal=True)
        
        logger.debug(f"=== INTELLIGENT MESSAGE ADDITION END ===", print_to_terminal=True)
        return {"stm_added": True, "ltm_qualified": classification.get("should_store_ltm", False) if role == "user" else False}
    
    def extract_facts_from_message(self, message: str) -> Dict[str, str]:
        """Extract facts from a message using pattern matching"""
        facts = {}
        
        # Extract name patterns - more comprehensive and precise
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"call me (\w+)",
            r"(\w+) is my name",
            r"my name's (\w+)",
            r"i'm called (\w+)",
            r"people call me (\w+)",
            r"you can call me (\w+)",
            r"remember my name is (\w+)",
            r"my name is (\w+), remember that"
        ]
        
        # Common words that should NOT be extracted as names
        invalid_names = {
            'currently', 'recently', 'actually', 'really', 'probably', 'maybe', 'perhaps',
            'sometimes', 'usually', 'always', 'never', 'often', 'rarely', 'occasionally',
            'definitely', 'certainly', 'obviously', 'clearly', 'apparently', 'supposedly',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'down', 'out', 'off', 'over', 'under', 'through', 'during',
            'before', 'after', 'since', 'until', 'while', 'when', 'where', 'why', 'how',
            'what', 'which', 'who', 'whom', 'whose', 'this', 'that', 'these', 'those',
            'i', 'me', 'my', 'myself', 'we', 'us', 'our', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
            'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves'
        }
        
        for pattern in name_patterns:
            match = re.search(pattern, message.lower())
            if match:
                potential_name = match.group(1).title()
                # Validate that it's not a common word
                if potential_name.lower() not in invalid_names and len(potential_name) > 1:
                    facts["name"] = potential_name
                    facts["user_name"] = potential_name  # Also store as user_name for personality system
                    logger.debug(f"Extracted valid name: {potential_name}", print_to_terminal=True)
                    break
                else:
                    logger.debug(f"Rejected invalid name: {potential_name}", print_to_terminal=True)
        
        # Extract location patterns - more precise
        location_patterns = [
            r"i live in ([^.!?]+)",
            r"i'm from ([^.!?]+)",
            r"my home is ([^.!?]+)",
            r"i'm located in ([^.!?]+)",
            r"i live at ([^.!?]+)"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, message.lower())
            if match:
                location = match.group(1).strip()
                # Validate location is meaningful
                if len(location) > 3 and not location.lower() in ['here', 'there', 'somewhere', 'anywhere']:
                    facts["location"] = location
                    facts["home"] = location
                    logger.debug(f"Extracted location: {location}", print_to_terminal=True)
                    break
        
        # Extract preferences - more precise
        preference_patterns = [
            r"i (like|love|enjoy) ([^.!?]+)",
            r"my favorite ([^.!?]+) is ([^.!?]+)",
            r"i prefer ([^.!?]+)",
            r"i (hate|dislike) ([^.!?]+)"
        ]
        
        for pattern in preference_patterns:
            match = re.search(pattern, message.lower())
            if match:
                if "favorite" in pattern:
                    category = match.group(1)
                    item = match.group(2).strip()
                    # Validate preference is meaningful
                    if len(item) > 2 and not item.lower() in ['it', 'this', 'that', 'things', 'stuff']:
                        facts[f"favorite_{category}"] = item
                        logger.debug(f"Extracted favorite {category}: {item}", print_to_terminal=True)
                else:
                    action = match.group(1)
                    item = match.group(2).strip()
                    # Validate preference is meaningful
                    if len(item) > 2 and not item.lower() in ['it', 'this', 'that', 'things', 'stuff']:
                        facts[f"preference_{action}"] = item
                        logger.debug(f"Extracted preference {action}: {item}", print_to_terminal=True)
        
        return facts
    
    def get_user_info(self) -> Dict[str, str]:
        """Get user information for personality pronouns system"""
        user_info = {}
        
        # Get facts from LTM
        facts = self.ltm.get_entries('fact')
        for fact in facts:
            if fact.key == "name" or fact.key == "user_name":
                user_info["name"] = fact.value
            elif fact.key == "location" or fact.key == "home":
                user_info["location"] = fact.value
            elif fact.key.startswith("favorite_"):
                category = fact.key.replace("favorite_", "")
                user_info[f"favorite_{category}"] = fact.value
            elif fact.key.startswith("preference_"):
                category = fact.key.replace("preference_", "")
                user_info[f"preference_{category}"] = fact.value
        
        logger.debug(f"Retrieved user info: {user_info}", print_to_terminal=True)
        return user_info
    
    def get_context_messages(self, current_query: str = "") -> List[Dict]:
        """Get messages for context window, including relevant memories"""
        logger.debug(f"=== CONTEXT RETRIEVAL START ===", print_to_terminal=True)
        logger.debug(f"Current query: '{current_query}'", print_to_terminal=True)
        
        # Get STM messages
        stm_msgs = self.stm.get_messages()
        logger.debug(f"STM messages: {len(stm_msgs)}", print_to_terminal=True)
        
        # Get relevant LTM entries if we have a query
        relevant_ltm = []
        if current_query.strip():
            logger.debug("Retrieving relevant LTM entries...", print_to_terminal=True)
            relevant_ltm = self.retriever.get_relevant_memories(
                current_query, 
                self.ltm.entries, 
                max_results=5, 
                min_relevance=0.2
            )
            logger.debug(f"Found {len(relevant_ltm)} relevant LTM entries", print_to_terminal=True)
            
            # Update access stats for retrieved memories
            for memory, relevance in relevant_ltm:
                self.ltm.update_access_stats(memory)
                logger.debug(f"Retrieved memory: {memory.key} = {memory.value} (relevance: {relevance:.2f})", print_to_terminal=True)
        
        # Build context - only include conversation messages, not system messages
        context = []
        
        # Add LTM summaries as conversation context (not system messages)
        ltm_summaries = [asdict(e) for e in self.ltm.get_entries('summary')]
        for summary in ltm_summaries:
            context.append({'role': 'user', 'content': f"Context: {summary['summary']}"})
        
        # Filter out assistant messages that could confuse identity
        filtered_stm = []
        for msg in stm_msgs:
            content = msg.get('content', '').lower()
            role = msg.get('role', '')
            
            # Skip empty assistant messages
            if role == 'assistant' and not content.strip():
                continue
                
            # Skip assistant messages with confusing identity statements
            if role == 'assistant' and any(phrase in content for phrase in [
                'my name is',
                "i'm bob",
                "i am bob",
                "i'm an ai assistant, and i don't have a personal name",
                "i don't have a personal name"
            ]):
                continue
                
            filtered_stm.append(msg)
        
        context.extend(filtered_stm)
        logger.debug(f"Context messages: {context}", print_to_terminal=True)
        logger.debug(f"=== CONTEXT RETRIEVAL END ===", print_to_terminal=True)
        return context
    
    def summarize_conversation(self, conversation_messages: List[Dict], conversation_id: str) -> str:
        """Create a summary of the conversation (placeholder for now)"""
        if len(conversation_messages) < 10:
            return None  # Don't summarize short conversations
        
        # Simple summarization: extract key points from user messages
        user_messages = [msg for msg in conversation_messages if msg.get("role") == "user"]
        key_points = []
        
        for msg in user_messages[-5:]:  # Last 5 user messages
            content = msg.get("content", "")
            if len(content) > 20:  # Only consider substantial messages
                key_points.append(content[:100] + "..." if len(content) > 100 else content)
        
        summary = f"Conversation summary: {len(conversation_messages)} messages, {len(user_messages)} user inputs. Key topics: {', '.join(key_points[:3])}"
        
        summary_text = f"{summary}\nKey points: {', '.join(key_points)}"
        self.add_summary(summary_text, importance=0.5, tags=["conversation_summary"])
        return summary
    
    def clear_memory(self, memory_type: str = None):
        """Clear memory entries and files"""
        if memory_type:
            self.memories = [m for m in self.memories if m.memory_type != memory_type]
        else:
            # Clear all memory data structures
            self.memories = []
            self.summaries = []
            self.stm.clear()
            self.ltm.entries = []
            
            # Clear all memory files
            try:
                # Clear short-term memory file
                if os.path.exists(self.stm.stm_file):
                    with open(self.stm.stm_file, 'w', encoding='utf-8') as f:
                        json.dump([], f, indent=2, ensure_ascii=False)
                    logger.debug(f"Cleared short-term memory file: {self.stm.stm_file}", print_to_terminal=True)
                
                # Clear long-term memory file
                if os.path.exists(self.ltm.ltm_file):
                    with open(self.ltm.ltm_file, 'w', encoding='utf-8') as f:
                        json.dump([], f, indent=2, ensure_ascii=False)
                    logger.debug(f"Cleared long-term memory file: {self.ltm.ltm_file}", print_to_terminal=True)
                
                # Clear summaries file
                if os.path.exists(self.summaries_file):
                    with open(self.summaries_file, 'w', encoding='utf-8') as f:
                        json.dump([], f, indent=2, ensure_ascii=False)
                    logger.debug(f"Cleared summaries file: {self.summaries_file}", print_to_terminal=True)
                
                # Clear memories file
                if os.path.exists(self.memory_file):
                    with open(self.memory_file, 'w', encoding='utf-8') as f:
                        json.dump([], f, indent=2, ensure_ascii=False)
                    logger.debug(f"Cleared memories file: {self.memory_file}", print_to_terminal=True)
                
                logger.debug("All memory files cleared successfully", print_to_terminal=True)
                
                # Verify files are empty
                self._verify_memory_files_cleared()
                
            except Exception as e:
                logger.error(f"Error clearing memory files: {e}", print_to_terminal=True)
        
        self._save_memory()
        self.memory_updated.emit(self.memories)
        logger.debug(f"Memory cleared: type={memory_type if memory_type else 'all'}", print_to_terminal=True)
    
    def _verify_memory_files_cleared(self):
        """Verify that all memory files are properly cleared"""
        try:
            # Check short-term memory file
            if os.path.exists(self.stm.stm_file):
                with open(self.stm.stm_file, 'r', encoding='utf-8') as f:
                    stm_data = json.load(f)
                    if stm_data:
                        logger.warning(f"Short-term memory file not empty after clearing: {len(stm_data)} entries", print_to_terminal=True)
                    else:
                        logger.debug("Short-term memory file verified as empty", print_to_terminal=True)
            
            # Check long-term memory file
            if os.path.exists(self.ltm.ltm_file):
                with open(self.ltm.ltm_file, 'r', encoding='utf-8') as f:
                    ltm_data = json.load(f)
                    if ltm_data:
                        logger.warning(f"Long-term memory file not empty after clearing: {len(ltm_data)} entries", print_to_terminal=True)
                    else:
                        logger.debug("Long-term memory file verified as empty", print_to_terminal=True)
            
            # Check summaries file
            if os.path.exists(self.summaries_file):
                with open(self.summaries_file, 'r', encoding='utf-8') as f:
                    summaries_data = json.load(f)
                    if summaries_data:
                        logger.warning(f"Summaries file not empty after clearing: {len(summaries_data)} entries", print_to_terminal=True)
                    else:
                        logger.debug("Summaries file verified as empty", print_to_terminal=True)
            
            # Check memories file
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    memories_data = json.load(f)
                    if memories_data:
                        logger.warning(f"Memories file not empty after clearing: {len(memories_data)} entries", print_to_terminal=True)
                    else:
                        logger.debug("Memories file verified as empty", print_to_terminal=True)
                        
        except Exception as e:
            logger.error(f"Error verifying memory files: {e}", print_to_terminal=True)
    
    def delete_memory(self, memory_id: str):
        """Delete a specific memory entry"""
        self.memories = [m for m in self.memories if m.id != memory_id]
        self._save_memory()
        self.memory_updated.emit(self.memories)
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        total_memories = len(self.memories)
        total_summaries = len(self.summaries)
        
        memory_types = {}
        for memory in self.memories:
            memory_types[memory.memory_type] = memory_types.get(memory.memory_type, 0) + 1
        
        avg_importance = sum(m.importance for m in self.memories) / total_memories if total_memories > 0 else 0
        
        return {
            "total_memories": total_memories,
            "total_summaries": total_summaries,
            "memory_types": memory_types,
            "average_importance": avg_importance,
            "max_context_messages": self.stm.max_messages
        }
    
    def add_message(self, message: Dict):
        """Legacy method - use intelligent_add_message instead"""
        return self.intelligent_add_message(message)
    
    def add_fact(self, key: str, value: str, importance: float = 0.7, tags: List[str] = None):
        """Add a fact to long-term memory with validation"""
        logger.debug(f"=== MEMORY SERVICE ADD FACT START ===", print_to_terminal=True)
        logger.debug(f"Adding fact: key='{key}', value='{value}', importance={importance}", print_to_terminal=True)
        
        try:
            # Validate inputs
            if not key or not value:
                logger.debug(f"Invalid fact data: key='{key}', value='{value}'", print_to_terminal=True)
                return
                
            if not isinstance(key, str) or not isinstance(value, str):
                logger.debug(f"Fact key and value must be strings: key={type(key)}, value={type(value)}", print_to_terminal=True)
                return
            
            # Clean the inputs
            clean_key = key.strip()
            clean_value = value.strip()
            logger.debug(f"Cleaned inputs: key='{clean_key}', value='{clean_value}'", print_to_terminal=True)
            
            if not clean_key or not clean_value:
                logger.debug("Fact key or value is empty after cleaning", print_to_terminal=True)
                return
            
            # Check if this fact already exists to avoid duplicates
            logger.debug("Checking for existing facts to avoid duplicates...", print_to_terminal=True)
            existing_facts = self.ltm.get_entries('fact')
            logger.debug(f"Found {len(existing_facts)} existing facts", print_to_terminal=True)
            
            for existing in existing_facts:
                if existing.key == clean_key and existing.value == clean_value:
                    logger.debug(f"Fact already exists: {clean_key} = {clean_value}", print_to_terminal=True)
                    return
            
            logger.debug("No duplicate found, creating new fact entry", print_to_terminal=True)
            entry = LongTermMemoryEntry(
                type='fact', 
                key=clean_key, 
                value=clean_value, 
                timestamp=datetime.now().isoformat(), 
                importance=importance, 
                tags=tags or [],
                context_keywords=tags or []
            )
            logger.debug(f"Created entry: {entry}", print_to_terminal=True)
            
            self.ltm.add_entry(entry)
            logger.debug(f"Added fact to LTM: {clean_key} = {clean_value}", print_to_terminal=True)
            logger.debug(f"Total LTM entries: {len(self.ltm.entries)}", print_to_terminal=True)
            
            # Clean up memory entries to resolve conflicts
            self.cleanup_memory_entries()
            
        except Exception as e:
            logger.error(f"Error adding fact: {e}", print_to_terminal=True)
            logger.error(f"Exception type: {type(e)}", print_to_terminal=True)
        finally:
            logger.debug(f"=== MEMORY SERVICE ADD FACT END ===", print_to_terminal=True)
    
    def add_summary(self, summary: str, importance: float = 0.5, tags: List[str] = None):
        entry = LongTermMemoryEntry(type='summary', summary=summary, timestamp=datetime.now().isoformat(), importance=importance, tags=tags or [])
        self.ltm.add_entry(entry)
    
    def set_max_context_messages(self, max_messages: int):
        """Set the maximum number of context messages"""
        self.stm.max_messages = max_messages
        # Trim existing messages if needed
        if len(self.stm.messages) > max_messages:
            self.stm.messages = self.stm.messages[-max_messages:]
        self.stm._save()
        logger.debug(f"Set max context messages to {max_messages}", print_to_terminal=True)
    
    def search_memories(self, query: str, memory_type: str = None) -> List[MemoryEntry]:
        """Search memories by content"""
        results = []
        query_lower = query.lower()
        
        for memory in self.memories:
            if memory_type and memory.memory_type != memory_type:
                continue
            
            if (query_lower in memory.content.lower() or 
                any(tag.lower() in query_lower for tag in memory.tags)):
                results.append(memory)
        
        return results

    def clear(self):
        """Clear all memory (alias for clear_memory())"""
        self.clear_memory()

    def cleanup_memory_entries(self):
        """Clean up duplicate and conflicting memory entries"""
        logger.debug("=== MEMORY CLEANUP START ===", print_to_terminal=True)
        
        # Group entries by key
        entries_by_key = {}
        for entry in self.ltm.entries:
            if entry.key not in entries_by_key:
                entries_by_key[entry.key] = []
            entries_by_key[entry.key].append(entry)
        
        # Clean up duplicates and conflicts
        cleaned_entries = []
        for key, entries in entries_by_key.items():
            if len(entries) == 1:
                # Single entry, keep it
                cleaned_entries.append(entries[0])
            else:
                # Multiple entries for same key, resolve conflicts
                logger.debug(f"Found {len(entries)} entries for key '{key}': {[e.value for e in entries]}", print_to_terminal=True)
                
                if key in ['name', 'user_name']:
                    # For names, prefer the most recent valid name
                    valid_names = [e for e in entries if e.value.lower() not in ['currently', 'recently', 'actually']]
                    if valid_names:
                        # Sort by timestamp, most recent first
                        valid_names.sort(key=lambda x: x.timestamp, reverse=True)
                        best_name = valid_names[0]
                        logger.debug(f"Selected best name: {best_name.value} (timestamp: {best_name.timestamp})", print_to_terminal=True)
                        cleaned_entries.append(best_name)
                    else:
                        # No valid names found, keep the most recent
                        entries.sort(key=lambda x: x.timestamp, reverse=True)
                        cleaned_entries.append(entries[0])
                        logger.debug(f"No valid names found, keeping most recent: {entries[0].value}", print_to_terminal=True)
                else:
                    # For other keys, keep the most recent entry
                    entries.sort(key=lambda x: x.timestamp, reverse=True)
                    cleaned_entries.append(entries[0])
                    logger.debug(f"Keeping most recent entry for '{key}': {entries[0].value}", print_to_terminal=True)
        
        # Update the entries list
        old_count = len(self.ltm.entries)
        self.ltm.entries = cleaned_entries
        new_count = len(self.ltm.entries)
        
        logger.debug(f"Memory cleanup complete: {old_count} -> {new_count} entries", print_to_terminal=True)
        logger.debug("=== MEMORY CLEANUP END ===", print_to_terminal=True)
        
        # Save the cleaned entries
        self.ltm._save() 
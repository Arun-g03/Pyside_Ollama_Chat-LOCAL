# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *


"""
Memory Service - Handles LLM memory management across conversations
"""



# Import semantic search services
try:
    import sentence_transformers
    from pyside_chat.features.memory.semantic_search import SemanticSearchService
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    from pyside_chat.features.memory.semantic_search_fallback import SemanticSearchFallback as SemanticSearchService
    SENTENCE_TRANSFORMERS_AVAILABLE = False

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
        try:
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
        except Exception as e:
            LoggingHelpers.log_exception_with_context("classify_message", e, {"message": message, "role": role})
            # Return safe defaults
            return {
                "importance": 0.3,
                "memory_type": "conversation",
                "context_keywords": [],
                "should_store_ltm": False
            }

class PronounNormalizer:
    """Normalizes pronouns in user messages to avoid AI confusion"""
    
    # First-person pronouns that should be converted to third-person
    FIRST_PERSON_PRONOUNS = {
        'i': 'the user',
        'me': 'the user',
        'my': 'the user\'s',
        'myself': 'the user',
        'mine': 'the user\'s',
        'we': 'the users',
        'us': 'the users',
        'our': 'the users\'',
        'ours': 'the users\'',
        'ourselves': 'the users'
    }
    
    # Contractions that need special handling
    FIRST_PERSON_CONTRACTIONS = {
        "i'm": "the user is",
        "i'll": "the user will",
        "i've": "the user has",
        "i'd": "the user would",
        "i'm not": "the user is not",
        "i'll not": "the user will not",
        "i've not": "the user has not",
        "i'd not": "the user would not"
    }
    
    @staticmethod
    def normalize_pronouns(text: str, user_name: str = None) -> str:
        """
        Convert first-person pronouns to third-person references to avoid AI confusion
        
        Args:
            text: The text to normalize
            user_name: Optional user name to use instead of generic "the user"
        
        Returns:
            Normalized text with pronouns converted
        """
        try:
            if not text or not isinstance(text, str):
                return text
            
            # Use user name if provided, otherwise use "the user"
            reference = user_name if user_name else "the user"
            reference_possessive = f"{user_name}'s" if user_name else "the user's"
            
            normalized_text = text
            
            # Handle contractions first (before individual words)
            for contraction, replacement in PronounNormalizer.FIRST_PERSON_CONTRACTIONS.items():
                normalized_text = re.sub(r'\b' + re.escape(contraction) + r'\b', replacement, normalized_text, flags=re.IGNORECASE)
            
            # Handle individual pronouns
            for pronoun, replacement in PronounNormalizer.FIRST_PERSON_PRONOUNS.items():
                normalized_text = re.sub(r'\b' + re.escape(pronoun) + r'\b', replacement, normalized_text, flags=re.IGNORECASE)
            
            return normalized_text
        except Exception as e:
            LoggingHelpers.log_exception_with_context("normalize_pronouns", e, {"text": text, "user_name": user_name})
            return text
    
    @staticmethod
    def should_normalize(text: str) -> bool:
        """Check if text contains first-person pronouns that should be normalized"""
        try:
            if not text or not isinstance(text, str):
                return False
            
            text_lower = text.lower()
            words = set(re.findall(r'\b\w+\b', text_lower))
            
            # Check for first-person pronouns
            first_person_words = {'i', 'me', 'my', 'myself', 'mine', 'we', 'us', 'our', 'ours', 'ourselves'}
            if words.intersection(first_person_words):
                return True
            
            # Check for contractions
            for contraction in PronounNormalizer.FIRST_PERSON_CONTRACTIONS:
                if contraction in text_lower:
                    return True
            
            return False
        except Exception as e:
            LoggingHelpers.log_exception_with_context("should_normalize", e, {"text": text})
            return False

class MemoryRetriever:
    """Retrieves relevant memories based on query similarity"""
    
    @staticmethod
    def calculate_relevance(query: str, memory_entry: LongTermMemoryEntry) -> float:
        """Calculate relevance score between query and memory entry"""
        try:
            query_lower = query.lower()
            query_words = set(re.findall(r'\b\w+\b', query_lower))
            
            # Calculate keyword overlap
            entry_keywords = set()
            if memory_entry.context_keywords:
                entry_keywords.update(memory_entry.context_keywords)
            if memory_entry.key:
                entry_keywords.update(re.findall(r'\b\w+\b', memory_entry.key.lower()))
            if memory_entry.value:
                entry_keywords.update(re.findall(r'\b\w+\b', memory_entry.value.lower()))
            if memory_entry.summary:
                entry_keywords.update(re.findall(r'\b\w+\b', memory_entry.summary.lower()))
            
            if not entry_keywords:
                return 0.0
            
            # Calculate overlap
            overlap = len(query_words.intersection(entry_keywords))
            total_unique = len(query_words.union(entry_keywords))
            
            if total_unique == 0:
                return 0.0
            
            relevance = overlap / total_unique
            
            # Boost for importance
            relevance += memory_entry.importance * 0.2
            
            # Boost for recent access
            if memory_entry.last_accessed:
                try:
                    last_accessed = datetime.fromisoformat(memory_entry.last_accessed)
                    days_since = (datetime.now() - last_accessed).days
                    if days_since < 7:
                        relevance += 0.1
                    elif days_since < 30:
                        relevance += 0.05
                except:
                    pass
            
            return min(relevance, 1.0)
        except Exception as e:
            LoggingHelpers.log_exception_with_context("calculate_relevance", e, {"query": query, "memory_entry": str(memory_entry)})
            return 0.0
    
    @staticmethod
    def get_relevant_memories(query: str, memories: List[LongTermMemoryEntry], 
                            max_results: int = 5, min_relevance: float = 0.1) -> List[Tuple[LongTermMemoryEntry, float]]:
        """Get most relevant memories for a query"""
        try:
            relevant_memories = []
            
            for memory in memories:
                relevance = MemoryRetriever.calculate_relevance(query, memory)
                if relevance >= min_relevance:
                    relevant_memories.append((memory, relevance))
            
            # Sort by relevance (highest first)
            relevant_memories.sort(key=lambda x: x[1], reverse=True)
            
            return relevant_memories[:max_results]
        except Exception as e:
            LoggingHelpers.log_exception_with_context("get_relevant_memories", e, {"query": query, "memories_count": len(memories)})
            return []

class ShortTermMemoryService:
    """Manages short-term memory (recent conversation context)"""
    
    def __init__(self, max_messages: int = 16, stm_file: str = "User_history/memory/short_term_memory.json"):
        self.max_messages = max_messages
        self.stm_file = stm_file
        self.messages = []
        self._load()
    
    def _load(self):
        """Load short-term memory from file"""
        try:
            if os.path.exists(self.stm_file):
                with open(self.stm_file, 'r', encoding='utf-8') as f:
                    self.messages = json.load(f)
                LoggingHelpers.log_file_operation("load", self.stm_file, True)
            else:
                LoggingHelpers.log_file_operation("load", self.stm_file, False, FileNotFoundError("File not found"))
        except Exception as e:
            LoggingHelpers.log_file_operation("load", self.stm_file, False, e)
            self.messages = []
    
    def add_message(self, message: Dict):
        """Add a message to short-term memory"""
        try:
            self.messages.append(message)
            if len(self.messages) > self.max_messages:
                self.messages = self.messages[-self.max_messages:]
            self._save()
        except Exception as e:
            LoggingHelpers.log_exception_with_context("add_message", e, {"message": message})
    
    def get_messages(self) -> List[Dict]:
        """Get all messages in short-term memory"""
        return self.messages.copy()
    
    def clear(self):
        """Clear short-term memory"""
        try:
            self.messages = []
            self._save()
        except Exception as e:
            LoggingHelpers.log_exception_with_context("clear", e, {})
    
    def _save(self):
        """Save short-term memory to file"""
        try:
            os.makedirs(os.path.dirname(self.stm_file), exist_ok=True)
            with open(self.stm_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
            LoggingHelpers.log_file_operation("save", self.stm_file, True)
        except Exception as e:
            LoggingHelpers.log_file_operation("save", self.stm_file, False, e)

class LongTermMemoryService:
    """Manages long-term memory storage and retrieval"""
    
    def __init__(self, ltm_file: str = "User_history/memory/long_term_memory.json"):
        self.ltm_file = ltm_file
        self.entries = []
        self._load()
    
    def _load(self):
        """Load long-term memory from file"""
        try:
            if os.path.exists(self.ltm_file):
                with open(self.ltm_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = [LongTermMemoryEntry(**entry) for entry in data]
                LoggingHelpers.log_file_operation("load", self.ltm_file, True)
                LoggingHelpers.log_info_with_context("Loaded LTM entries", {"count": len(self.entries)})
            else:
                LoggingHelpers.log_file_operation("load", self.ltm_file, False, FileNotFoundError("File not found"))
        except Exception as e:
            LoggingHelpers.log_file_operation("load", self.ltm_file, False, e)
            self.entries = []
    
    def add_entry(self, entry: LongTermMemoryEntry):
        """Add an entry to long-term memory"""
        try:
            entry.timestamp = datetime.now().isoformat()
            self.entries.append(entry)
            self._save()
            LoggingHelpers.log_memory_operation("add_entry", entry.type, True)
        except Exception as e:
            LoggingHelpers.log_memory_operation("add_entry", entry.type, False, e)
    
    def get_entries(self, type_filter: Optional[str] = None) -> List[LongTermMemoryEntry]:
        """Get entries from long-term memory, optionally filtered by type"""
        try:
            if type_filter:
                return [entry for entry in self.entries if entry.type == type_filter]
            return self.entries.copy()
        except Exception as e:
            LoggingHelpers.log_exception_with_context("get_entries", e, {"type_filter": type_filter})
            return []
    
    def _save(self):
        """Save long-term memory to file"""
        try:
            os.makedirs(os.path.dirname(self.ltm_file), exist_ok=True)
            with open(self.ltm_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(entry) for entry in self.entries], f, indent=2, ensure_ascii=False)
            LoggingHelpers.log_file_operation("save", self.ltm_file, True)
        except Exception as e:
            LoggingHelpers.log_file_operation("save", self.ltm_file, False, e)
    
    def update_access_stats(self, entry: LongTermMemoryEntry):
        """Update access statistics for a memory entry"""
        try:
            entry.access_count += 1
            entry.last_accessed = datetime.now().isoformat()
            self._save()
        except Exception as e:
            LoggingHelpers.log_exception_with_context("update_access_stats", e, {"entry_type": entry.type})

class MemoryService(QObject):
    """Service for managing LLM memory across conversations"""
    
    memory_updated = Signal(list)  # Emits updated memory entries
    summary_updated = Signal(list)  # Emits updated summaries
    
    def __init__(self, max_context_messages: int = 16):
        super().__init__()
        try:
            self.max_context_messages = max_context_messages
            
            # Initialize memory services
            self.stm_service = ShortTermMemoryService(max_context_messages)
            self.ltm_service = LongTermMemoryService()
            
            # Initialize semantic search service
            try:
                if SENTENCE_TRANSFORMERS_AVAILABLE:
                    self.semantic_search = SemanticSearchService()
                    LoggingHelpers.log_service_initialization("SemanticSearchService (with embeddings)", True)
                else:
                    self.semantic_search = SemanticSearchService()  # This is the fallback service
                    LoggingHelpers.log_service_initialization("SemanticSearchService (fallback mode)", True)
            except Exception as e:
                LoggingHelpers.log_service_initialization("SemanticSearchService", False, e)
                self.semantic_search = None
            
            # Load existing memory
            self._load_memory()
            
            LoggingHelpers.log_service_initialization("MemoryService", True)
        except Exception as e:
            LoggingHelpers.log_service_initialization("MemoryService", False, e)
            raise
    
    def _load_memory(self):
        """Load memory from storage"""
        try:
            # Memory is loaded in the service constructors
            pass
        except Exception as e:
            LoggingHelpers.log_exception_with_context("_load_memory", e, {})
    
    def _save_memory(self):
        """Save memory to storage"""
        try:
            # Memory is saved automatically by the services
            pass
        except Exception as e:
            LoggingHelpers.log_exception_with_context("_save_memory", e, {})
    
    def _on_embeddings_updated(self):
        """Handle embeddings update"""
        try:
            if self.semantic_search:
                self.semantic_search.update_embeddings()
        except Exception as e:
            LoggingHelpers.log_exception_with_context("_on_embeddings_updated", e, {})
    
    def add_memory(self, content: str, conversation_id: str, importance: float = 0.5, 
                   tags: List[str] = None, memory_type: str = "conversation", metadata: Dict = None) -> str:
        """Add a memory entry"""
        try:
            memory_id = hashlib.md5(f"{content}{conversation_id}{datetime.now().isoformat()}".encode()).hexdigest()
            
            entry = MemoryEntry(
                id=memory_id,
                content=content,
                conversation_id=conversation_id,
                timestamp=datetime.now().isoformat(),
                importance=importance,
                tags=tags or [],
                memory_type=memory_type,
                metadata=metadata or {}
            )
            
            # Add to short-term memory
            self.stm_service.add_message({
                "role": "memory",
                "content": content,
                "memory_id": memory_id,
                "timestamp": entry.timestamp
            })
            
            # Add to semantic search service if available
            if self.semantic_search:
                try:
                    self.semantic_search.add_memory(
                        memory_id=memory_id,
                        content=content,
                        memory_type=memory_type,
                        importance=importance,
                        tags=tags,
                        metadata=metadata
                    )
                except Exception as e:
                    logger.warning(f"Failed to add memory to semantic search: {e}")
            
            LoggingHelpers.log_memory_operation("add_memory", memory_type, True)
            return memory_id
        except Exception as e:
            LoggingHelpers.log_memory_operation("add_memory", memory_type, False, e)
            return ""
    
    def add_summary(self, summary: str, importance: float = 0.5, tags: List[str] = None):
        """Add a conversation summary to memory"""
        try:
            entry = LongTermMemoryEntry(
                type="summary",
                summary=summary,
                importance=importance,
                tags=tags or [],
                timestamp=datetime.now().isoformat()
            )
            
            self.ltm_service.add_entry(entry)
            self.summary_updated.emit([entry])
            
            LoggingHelpers.log_memory_operation("add_summary", "summary", True)
        except Exception as e:
            LoggingHelpers.log_memory_operation("add_summary", "summary", False, e)
    
    def get_relevant_memories(self, query: str, limit: int = 10, use_semantic: bool = True) -> List[MemoryEntry]:
        """Get relevant memories for a query"""
        try:
            relevant_memories = []
            
            # Get from long-term memory
            ltm_entries = self.ltm_service.get_entries()
            relevant_ltm = MemoryRetriever.get_relevant_memories(query, ltm_entries, limit)
            
            for entry, relevance in relevant_ltm:
                memory_entry = MemoryEntry(
                    id=hashlib.md5(f"{entry.type}{entry.key}{entry.value}".encode()).hexdigest(),
                    content=entry.summary or f"{entry.key}: {entry.value}" if entry.key and entry.value else str(entry),
                    conversation_id="ltm",
                    timestamp=entry.timestamp,
                    importance=entry.importance,
                    tags=entry.tags,
                    memory_type=entry.type,
                    metadata={"relevance": relevance, "access_count": entry.access_count}
                )
                relevant_memories.append(memory_entry)
                
                # Update access stats
                self.ltm_service.update_access_stats(entry)
            
            # Use semantic search if available
            if use_semantic and self.semantic_search:
                try:
                    semantic_results = self.semantic_search.search_semantic(query, max_results=limit//2)
                    for memory_id, relevance, metadata in semantic_results:
                        # Find the corresponding memory entry
                        memory_entry = MemoryEntry(
                            id=memory_id,
                            content=metadata.get("content", ""),
                            conversation_id="semantic",
                            timestamp=metadata.get("timestamp", ""),
                            importance=metadata.get("importance", 0.5),
                            tags=metadata.get("tags", []),
                            memory_type=metadata.get("memory_type", "semantic"),
                            metadata={"relevance": relevance}
                        )
                        relevant_memories.append(memory_entry)
                except Exception as e:
                    LoggingHelpers.log_exception_with_context("semantic_search", e, {"query": query})
                    logger.warning(f"Semantic search failed, using fallback: {e}")
            
            # Sort by relevance and limit
            relevant_memories.sort(key=lambda x: x.metadata.get("relevance", 0.0), reverse=True)
            return relevant_memories[:limit]
        except Exception as e:
            LoggingHelpers.log_exception_with_context("get_relevant_memories", e, {"query": query, "limit": limit})
            return []
    
    def intelligent_add_message(self, message: Dict) -> Dict:
        """Intelligently add a message to memory with classification"""
        try:
            content = message.get("content", "")
            role = message.get("role", "user")
            
            # Classify the message
            classification = MemoryClassifier.classify_message(content, role)
            
            # Normalize pronouns if needed
            if role == "user" and PronounNormalizer.should_normalize(content):
                normalized_content = PronounNormalizer.normalize_pronouns(content)
                message["content"] = normalized_content
                content = normalized_content
            
            # Add to short-term memory
            self.stm_service.add_message(message)
            
            # Add to semantic search service if available
            if self.semantic_search:
                try:
                    memory_id = hashlib.md5(f"{content}{datetime.now().isoformat()}".encode()).hexdigest()
                    self.semantic_search.add_memory(
                        memory_id=memory_id,
                        content=content,
                        memory_type=classification["memory_type"],
                        importance=classification["importance"],
                        tags=classification["context_keywords"],
                        metadata={"role": role}
                    )
                except Exception as e:
                    logger.warning(f"Failed to add message to semantic search: {e}")
            
            # Check if it should be stored in long-term memory
            if classification["should_store_ltm"]:
                entry = LongTermMemoryEntry(
                    type=classification["memory_type"],
                    value=content,
                    importance=classification["importance"],
                    tags=classification["context_keywords"],
                    timestamp=datetime.now().isoformat()
                )
                self.ltm_service.add_entry(entry)
            
            return {
                "classified": True,
                "memory_type": classification["memory_type"],
                "importance": classification["importance"],
                "ltm_qualified": classification["should_store_ltm"],
                "context_keywords": classification["context_keywords"]
            }
        except Exception as e:
            LoggingHelpers.log_exception_with_context("intelligent_add_message", e, {"message": message})
            return {
                "classified": False,
                "memory_type": "conversation",
                "importance": 0.3,
                "ltm_qualified": False,
                "context_keywords": []
            }
    
    def extract_facts_from_message(self, message: str) -> Dict[str, str]:
        """Extract facts from a message using LLM"""
        try:
            # This would typically use an LLM to extract structured facts
            # For now, return a simple extraction
            facts = {}
            
            # Simple pattern matching for common fact patterns
            patterns = [
                r"my name is (\w+)",
                r"i am (\d+) years old",
                r"i live in ([^.!?]+)",
                r"i work at ([^.!?]+)",
                r"my favorite ([^.!?]+) is ([^.!?]+)"
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, message.lower())
                for match in matches:
                    if isinstance(match, tuple):
                        facts[match[0]] = match[1]
                    else:
                        facts[pattern] = match
            
            return facts
        except Exception as e:
            LoggingHelpers.log_exception_with_context("extract_facts_from_message", e, {"message": message})
            return {}
    
    def get_user_info(self) -> Dict[str, str]:
        """Get user information from memory"""
        try:
            user_info = {}
            ltm_entries = self.ltm_service.get_entries("fact")
            
            for entry in ltm_entries:
                if entry.key and entry.value:
                    user_info[entry.key] = entry.value
            
            return user_info
        except Exception as e:
            LoggingHelpers.log_exception_with_context("get_user_info", e, {})
            return {}
    
    def get_user_name(self) -> Optional[str]:
        """Get the user's name from memory"""
        try:
            user_info = self.get_user_info()
            return user_info.get("name")
        except Exception as e:
            LoggingHelpers.log_exception_with_context("get_user_name", e, {})
            return None
    
    def get_context_messages(self, current_query: str = "") -> List[Dict]:
        """Get context messages for AI conversation"""
        try:
            context_messages = []
            
            # Get recent conversation from short-term memory
            stm_messages = self.stm_service.get_messages()
            context_messages.extend(stm_messages)
            
            # Get relevant long-term memories
            if current_query:
                relevant_memories = self.get_relevant_memories(current_query, limit=5)
                for memory in relevant_memories:
                    context_messages.append({
                        "role": "system",
                        "content": f"Memory: {memory.content}"
                    })
            
            # Limit context size
            if len(context_messages) > self.max_context_messages:
                context_messages = context_messages[-self.max_context_messages:]
            
            return context_messages
        except Exception as e:
            LoggingHelpers.log_exception_with_context("get_context_messages", e, {"current_query": current_query})
            return []
    
    def summarize_conversation(self, conversation_messages: List[Dict], conversation_id: str) -> str:
        """Summarize a conversation"""
        try:
            # Simple summarization - in practice, this would use an LLM
            user_messages = [msg["content"] for msg in conversation_messages if msg.get("role") == "user"]
            assistant_messages = [msg["content"] for msg in conversation_messages if msg.get("role") == "assistant"]
            
            summary = f"Conversation {conversation_id}: {len(user_messages)} user messages, {len(assistant_messages)} assistant responses"
            
            # Add to long-term memory
            self.add_summary(summary, importance=0.6, tags=["conversation", "summary"])
            
            return summary
        except Exception as e:
            LoggingHelpers.log_exception_with_context("summarize_conversation", e, {"conversation_id": conversation_id})
            return ""
    
    def clear_memory(self, memory_type: str = None):
        """Clear memory entries"""
        try:
            if memory_type is None:
                # Clear all memory
                self.stm_service.clear()
                self.ltm_service.entries = []
                self.ltm_service._save()
                LoggingHelpers.log_memory_operation("clear_memory", "all", True)
            else:
                # Clear specific memory type
                if memory_type == "short_term":
                    self.stm_service.clear()
                elif memory_type == "long_term":
                    self.ltm_service.entries = []
                    self.ltm_service._save()
                else:
                    # Clear specific type from long-term memory
                    self.ltm_service.entries = [entry for entry in self.ltm_service.entries if entry.type != memory_type]
                    self.ltm_service._save()
                
                LoggingHelpers.log_memory_operation("clear_memory", memory_type, True)
        except Exception as e:
            LoggingHelpers.log_memory_operation("clear_memory", memory_type or "all", False, e)
    
    def _verify_memory_files_cleared(self):
        """Verify that memory files have been cleared"""
        try:
            # Check short-term memory file
            if os.path.exists(self.stm_service.stm_file):
                with open(self.stm_service.stm_file, 'r', encoding='utf-8') as f:
                    stm_data = json.load(f)
                    if stm_data:
                        LoggingHelpers.log_warning_with_context("STM file not empty after clear", {"file": self.stm_service.stm_file, "data_length": len(stm_data)})
            
            # Check long-term memory file
            if os.path.exists(self.ltm_service.ltm_file):
                with open(self.ltm_service.ltm_file, 'r', encoding='utf-8') as f:
                    ltm_data = json.load(f)
                    if ltm_data:
                        LoggingHelpers.log_warning_with_context("LTM file not empty after clear", {"file": self.ltm_service.ltm_file, "data_length": len(ltm_data)})
        except Exception as e:
            LoggingHelpers.log_exception_with_context("_verify_memory_files_cleared", e, {})
    
    def delete_memory(self, memory_id: str):
        """Delete a specific memory entry"""
        try:
            # Remove from long-term memory
            self.ltm_service.entries = [entry for entry in self.ltm_service.entries 
                                      if hashlib.md5(f"{entry.type}{entry.key}{entry.value}".encode()).hexdigest() != memory_id]
            self.ltm_service._save()
            LoggingHelpers.log_memory_operation("delete_memory", "specific", True)
        except Exception as e:
            LoggingHelpers.log_memory_operation("delete_memory", "specific", False, e)
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        try:
            stm_count = len(self.stm_service.get_messages())
            ltm_count = len(self.ltm_service.get_entries())
            summaries_count = len(self.ltm_service.get_entries("summary"))
            
            # Count by type
            type_counts = {}
            total_importance = 0.0
            importance_count = 0
            
            for entry in self.ltm_service.get_entries():
                type_counts[entry.type] = type_counts.get(entry.type, 0) + 1
                total_importance += entry.importance
                importance_count += 1
            
            # Calculate average importance
            average_importance = total_importance / importance_count if importance_count > 0 else 0.0
            
            # Get semantic search info
            semantic_search = {}
            if hasattr(self, 'semantic_search_service') and self.semantic_search_service:
                semantic_search = {
                    "model_loaded": self.semantic_search_service.model is not None,
                    "model_name": getattr(self.semantic_search_service.model, 'name', 'Unknown') if self.semantic_search_service.model else 'Unknown',
                    "total_memories": len(self.semantic_search_service.embeddings) if hasattr(self.semantic_search_service, 'embeddings') else 0
                }

            return {
                "short_term_count": stm_count,
                "long_term_count": ltm_count,
                "type_counts": type_counts,
                "memory_types": type_counts,  # Alias for compatibility
                "total_memories": stm_count + ltm_count,
                "total_summaries": summaries_count,
                "average_importance": average_importance,
                "max_context_messages": self.max_context_messages,
                "semantic_search": semantic_search,
            }
        except Exception as e:
            LoggingHelpers.log_exception_with_context("get_memory_stats", e, {})
            return {
                "short_term_count": 0,
                "long_term_count": 0,
                "type_counts": {},
                "memory_types": {},
                "total_memories": 0,
                "total_summaries": 0,
                "average_importance": 0.0,
                "max_context_messages": self.max_context_messages,
                "semantic_search": {},
            }
    
    def add_message(self, message: Dict):
        """Add a message to memory (legacy method)"""
        try:
            self.intelligent_add_message(message)
        except Exception as e:
            LoggingHelpers.log_exception_with_context("add_message", e, {"message": message})
    
    def add_fact(self, key: str, value: str, importance: float = 0.7, tags: List[str] = None):
        """Add a fact to long-term memory"""
        try:
            entry = LongTermMemoryEntry(
                type="fact",
                key=key,
                value=value,
                importance=importance,
                tags=tags or [],
                timestamp=datetime.now().isoformat()
            )
            
            self.ltm_service.add_entry(entry)
            LoggingHelpers.log_memory_operation("add_fact", "fact", True)
        except Exception as e:
            LoggingHelpers.log_memory_operation("add_fact", "fact", False, e)
    
    def set_max_context_messages(self, max_messages: int):
        """Set the maximum number of context messages"""
        try:
            self.max_context_messages = max_messages
            self.stm_service.max_messages = max_messages
            LoggingHelpers.log_configuration_change("max_context_messages", "previous", max_messages)
        except Exception as e:
            LoggingHelpers.log_exception_with_context("set_max_context_messages", e, {"max_messages": max_messages})
    
    def search_memories(self, query: str, memory_type: str = None) -> List[MemoryEntry]:
        """Search memories with optional type filter"""
        try:
            if memory_type:
                ltm_entries = self.ltm_service.get_entries(memory_type)
            else:
                ltm_entries = self.ltm_service.get_entries()
            
            relevant_entries = MemoryRetriever.get_relevant_memories(query, ltm_entries)
            
            memory_entries = []
            for entry, relevance in relevant_entries:
                memory_entry = MemoryEntry(
                    id=hashlib.md5(f"{entry.type}{entry.key}{entry.value}".encode()).hexdigest(),
                    content=entry.summary or f"{entry.key}: {entry.value}" if entry.key and entry.value else str(entry),
                    conversation_id="search",
                    timestamp=entry.timestamp,
                    importance=entry.importance,
                    tags=entry.tags,
                    memory_type=entry.type,
                    metadata={"relevance": relevance}
                )
                memory_entries.append(memory_entry)
            
            return memory_entries
        except Exception as e:
            LoggingHelpers.log_exception_with_context("search_memories", e, {"query": query, "memory_type": memory_type})
            return []
    
    def clear(self):
        """Clear all memory"""
        try:
            self.clear_memory()
        except Exception as e:
            LoggingHelpers.log_exception_with_context("clear", e, {})
    
    def cleanup_memory_entries(self):
        """Clean up old or low-importance memory entries"""
        try:
            # Remove entries older than 30 days with low importance
            cutoff_date = datetime.now() - timedelta(days=30)
            original_count = len(self.ltm_service.entries)
            
            self.ltm_service.entries = [
                entry for entry in self.ltm_service.entries
                if (entry.importance > 0.3 or 
                    datetime.fromisoformat(entry.timestamp) > cutoff_date)
            ]
            
            removed_count = original_count - len(self.ltm_service.entries)
            if removed_count > 0:
                self.ltm_service._save()
                LoggingHelpers.log_info_with_context("Cleaned up memory entries", {"removed_count": removed_count})
        except Exception as e:
            LoggingHelpers.log_exception_with_context("cleanup_memory_entries", e, {}) 
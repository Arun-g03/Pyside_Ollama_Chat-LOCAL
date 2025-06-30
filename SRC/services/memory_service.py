"""
Memory Service - Handles LLM memory management across conversations
"""

import os
import json
import hashlib
from typing import List, Dict, Optional, Tuple
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

class MemoryService(QObject):
    """Service for managing LLM memory across conversations"""
    
    memory_updated = Signal(list)  # Emits updated memory entries
    summary_updated = Signal(list)  # Emits updated summaries
    
    def __init__(self, memory_dir: str = "memory", max_context_messages: int = 20):
        super().__init__()
        self.memory_dir = memory_dir
        self.max_context_messages = max_context_messages
        self.memories: List[MemoryEntry] = []
        self.summaries: List[MemorySummary] = []
        self.memory_file = os.path.join(memory_dir, "memories.json")
        self.summaries_file = os.path.join(memory_dir, "summaries.json")
        
        os.makedirs(memory_dir, exist_ok=True)
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
    
    def add_summary(self, conversation_id: str, summary: str, key_points: List[str], message_count: int) -> str:
        """Add a conversation summary"""
        summary_id = hashlib.md5(f"{conversation_id}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        memory_summary = MemorySummary(
            id=summary_id,
            conversation_id=conversation_id,
            summary=summary,
            key_points=key_points,
            timestamp=datetime.now().isoformat(),
            message_count=message_count
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
    
    def get_context_messages(self, conversation_messages: List[Dict], include_memories: bool = True) -> List[Dict]:
        """Get messages for context window, including relevant memories"""
        # Start with recent conversation messages (respecting max_context_messages)
        context_messages = conversation_messages[-self.max_context_messages:]
        
        if include_memories and conversation_messages:
            # Get relevant memories based on recent conversation
            recent_content = " ".join([msg.get("content", "") for msg in conversation_messages[-5:]])
            relevant_memories = self.get_relevant_memories(recent_content, limit=3)
            
            # Add memory context as system messages
            for memory in relevant_memories:
                context_messages.insert(0, {
                    "role": "system",
                    "content": f"Memory: {memory.content}",
                    "metadata": {"memory_id": memory.id, "importance": memory.importance}
                })
        
        return context_messages
    
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
        
        self.add_summary(conversation_id, summary, key_points, len(conversation_messages))
        return summary
    
    def clear_memory(self, memory_type: str = None):
        """Clear memory entries"""
        if memory_type:
            self.memories = [m for m in self.memories if m.memory_type != memory_type]
        else:
            self.memories = []
        
        self._save_memory()
        self.memory_updated.emit(self.memories)
    
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
            "max_context_messages": self.max_context_messages
        }
    
    def set_max_context_messages(self, max_messages: int):
        """Update the maximum number of context messages"""
        self.max_context_messages = max_messages
        logger.debug(f"Updated max context messages to: {max_messages}", print_to_terminal=True)
    
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
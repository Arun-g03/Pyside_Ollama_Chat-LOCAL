"""
Fallback Semantic Search Service - Simple keyword-based memory retrieval
Used when sentence_transformers is not available
"""

import os
import json
import re
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal, QMutex
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

@dataclass
class SimpleMemory:
    """Represents a memory entry with simple keyword matching"""
    memory_id: str
    content: str
    memory_type: str
    importance: float
    timestamp: str
    tags: List[str]
    metadata: Dict

class SemanticSearchFallback(QObject):
    """Fallback service for memory retrieval using keyword matching"""
    
    embeddings_updated = Signal()  # Emitted when memories are updated
    search_completed = Signal(list)  # Emitted when search completes
    
    def __init__(self, cache_dir: str = "User_history/memory/embeddings"):
        super().__init__()
        self.cache_dir = cache_dir
        self.metadata_file = os.path.join(cache_dir, "metadata.json")
        
        # Initialize simple memory storage
        self.memories: List[SimpleMemory] = []
        self.mutex = QMutex()
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load existing memories
        self._load_memories()
    
    def _load_memories(self):
        """Load existing memories from cache"""
        try:
            if os.path.exists(self.metadata_file):
                logger.info("[ID:0335] Loading existing memories from cache", print_to_terminal=True)
                
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                self.memories = []
                for memory_id, meta in metadata.items():
                    memory = SimpleMemory(
                        memory_id=memory_id,
                        content=meta.get('content', ''),
                        memory_type=meta.get('memory_type', 'conversation'),
                        importance=meta.get('importance', 0.5),
                        timestamp=meta.get('timestamp', ''),
                        tags=meta.get('tags', []),
                        metadata=meta.get('metadata', {})
                    )
                    self.memories.append(memory)
                
                logger.info(f"[ID:0334] Loaded {len(self.memories)} memories", print_to_terminal=True)
                
        except Exception as e:
            logger.error(f"[ID:0333] Error loading memories: {e}", print_to_terminal=True)
            self.memories = []
    
    def _save_memories(self):
        """Save memories to cache"""
        try:
            if not self.memories:
                return
            
            # Prepare data for saving
            metadata = {}
            
            for memory in self.memories:
                metadata[memory.memory_id] = {
                    'content': memory.content,
                    'memory_type': memory.memory_type,
                    'importance': memory.importance,
                    'timestamp': memory.timestamp,
                    'tags': memory.tags,
                    'metadata': memory.metadata
                }
            
            # Save metadata
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"[ID:0332] Saved {len(self.memories)} memories to cache", print_to_terminal=True)
            
        except Exception as e:
            logger.error(f"[ID:0331] Error saving memories: {e}", print_to_terminal=True)
    
    def add_memory(self, memory_id: str, content: str, memory_type: str = "conversation", 
                   importance: float = 0.5, tags: List[str] = None, metadata: Dict = None) -> bool:
        """Add a new memory with simple storage"""
        try:
            logger.debug(f"[ID:0329] Adding memory with mutex lock - ID: {memory_id}")
            self.mutex.lock()
            
            try:
                # Check if memory already exists
                existing_memory = next((m for m in self.memories if m.memory_id == memory_id), None)
                if existing_memory:
                    logger.debug(f"[ID:0328] Memory {memory_id} already exists, updating", print_to_terminal=True)
                    self.memories.remove(existing_memory)
                
                # Create simple memory
                memory = SimpleMemory(
                    memory_id=memory_id,
                    content=content,
                    memory_type=memory_type,
                    importance=importance,
                    timestamp=datetime.now().isoformat(),
                    tags=tags or [],
                    metadata=metadata or {}
                )
                
                self.memories.append(memory)
                
                # Save to cache
                logger.debug(f"[ID:0326] Saving memories to cache for memory: {memory_id}")
                self._save_memories()
                
                logger.debug(f"[ID:0325] Added memory {memory_id}", print_to_terminal=True)
                self.embeddings_updated.emit()
                
                return True
                
            finally:
                logger.debug(f"[ID:0324] Releasing mutex lock for memory: {memory_id}")
                self.mutex.unlock()
            
        except Exception as e:
            logger.error(f"[ID:0323] Error adding memory: {e}", print_to_terminal=True)
            return False
    
    def remove_memory(self, memory_id: str) -> bool:
        """Remove a memory"""
        try:
            logger.debug(f"[ID:0321] Removing memory with mutex lock - ID: {memory_id}")
            self.mutex.lock()
            
            try:
                # Find and remove the memory
                memory_to_remove = next((m for m in self.memories if m.memory_id == memory_id), None)
                if memory_to_remove:
                    self.memories.remove(memory_to_remove)
                    logger.debug(f"[ID:0320] Saving memories after removal for memory: {memory_id}")
                    self._save_memories()
                    logger.debug(f"[ID:0319] Removed memory {memory_id}", print_to_terminal=True)
                    self.embeddings_updated.emit()
                    return True
                else:
                    logger.debug(f"[ID:0318] Memory {memory_id} not found", print_to_terminal=True)
                    return False
                    
            finally:
                logger.debug(f"[ID:0317] Releasing mutex lock for memory removal: {memory_id}")
                self.mutex.unlock()
                
        except Exception as e:
            logger.error(f"[ID:0316] Error removing memory {memory_id}: {e}", print_to_terminal=True)
            return False
    
    def _calculate_keyword_similarity(self, query: str, content: str) -> float:
        """Calculate similarity based on keyword matching"""
        try:
            # Convert to lowercase for case-insensitive matching
            query_lower = query.lower()
            content_lower = content.lower()
            
            # Split into words
            query_words = set(re.findall(r'\w+', query_lower))
            content_words = set(re.findall(r'\w+', content_lower))
            
            if not query_words:
                return 0.0
            
            # Calculate Jaccard similarity
            intersection = len(query_words.intersection(content_words))
            union = len(query_words.union(content_words))
            
            if union == 0:
                return 0.0
            
            jaccard_similarity = intersection / union
            
            # Boost score for exact phrase matches
            if query_lower in content_lower:
                jaccard_similarity += 0.3
            
            # Boost score for tag matches
            for word in query_words:
                if word in content_lower:
                    jaccard_similarity += 0.1
            
            return min(1.0, jaccard_similarity)
            
        except Exception as e:
            logger.error(f"Error calculating keyword similarity: {e}")
            return 0.0
    
    def search_semantic(self, query: str, max_results: int = 10, min_similarity: float = 0.3, 
                       memory_types: List[str] = None) -> List[Tuple[str, float, Dict]]:
        """Search memories using keyword similarity"""
        try:
            logger.debug(f"[ID:0313] Starting keyword search - Query: {query[:50]}...")
            logger.debug(f"[ID:0312] Search parameters - Max results: {max_results}, Min similarity: {min_similarity}")
            
            # Filter memories by type if specified
            memories_to_search = self.memories
            if memory_types:
                memories_to_search = [m for m in self.memories if m.memory_type in memory_types]
                logger.debug(f"[ID:0311] Filtered to {len(memories_to_search)} memories of types: {memory_types}")
            
            if not memories_to_search:
                logger.debug("[ID:0310] No memories to search")
                return []
            
            # Calculate similarities
            similarities = []
            for memory in memories_to_search:
                similarity = self._calculate_keyword_similarity(query, memory.content)
                # Boost by importance
                similarity *= (0.7 + 0.3 * memory.importance)
                
                similarities.append((memory.memory_id, similarity, {
                    'content': memory.content,
                    'memory_type': memory.memory_type,
                    'importance': memory.importance,
                    'timestamp': memory.timestamp,
                    'tags': memory.tags,
                    'metadata': memory.metadata
                }))
            
            # Sort by similarity and filter by minimum threshold
            similarities.sort(key=lambda x: x[1], reverse=True)
            results = [(memory_id, similarity, metadata) for memory_id, similarity, metadata in similarities 
                      if similarity >= min_similarity][:max_results]
            
            logger.debug(f"[ID:0309] Keyword search completed - Found {len(results)} results")
            for memory_id, similarity, metadata in results:
                logger.debug(f"[ID:0308] - {memory_id}: {similarity:.3f}")
            
            return results
            
        except Exception as e:
            logger.error(f"[ID:0307] Error in keyword search: {e}", print_to_terminal=True)
            return []
    
    def search_hybrid(self, query: str, max_results: int = 10, min_similarity: float = 0.3,
                     memory_types: List[str] = None, keyword_weight: float = 1.0, 
                     semantic_weight: float = 0.0) -> List[Tuple[str, float, Dict]]:
        """Search memories using keyword matching (semantic weight ignored in fallback)"""
        return self.search_semantic(query, max_results, min_similarity, memory_types)
    
    def update_memory_importance(self, memory_id: str, new_importance: float) -> bool:
        """Update the importance of a memory"""
        try:
            logger.debug(f"[ID:0298] Updating memory importance with mutex lock - ID: {memory_id}, Importance: {new_importance}")
            self.mutex.lock()
            
            try:
                memory = next((m for m in self.memories if m.memory_id == memory_id), None)
                if memory:
                    memory.importance = new_importance
                    logger.debug(f"[ID:0297] Saving memories after importance update for memory: {memory_id}")
                    self._save_memories()
                    logger.debug(f"[ID:0296] Updated importance for memory {memory_id}", print_to_terminal=True)
                    return True
                else:
                    logger.debug(f"[ID:0295] Memory {memory_id} not found for importance update", print_to_terminal=True)
                    return False
                    
            finally:
                logger.debug(f"[ID:0294] Releasing mutex lock for importance update: {memory_id}")
                self.mutex.unlock()
                
        except Exception as e:
            logger.error(f"[ID:0293] Error updating memory importance: {e}", print_to_terminal=True)
            return False
    
    def get_memory_stats(self) -> Dict:
        """Get statistics about the memory service"""
        try:
            logger.debug("[ID:0291] Getting memory stats with mutex lock")
            self.mutex.lock()
            
            try:
                stats = {
                    'total_memories': len(self.memories),
                    'model_loaded': True,  # Always true for fallback
                    'cache_dir': self.cache_dir,
                    'memory_types': {},
                    'average_importance': 0.0,
                    'max_importance': 0.0,
                    'min_importance': 1.0,
                    'fallback_mode': True
                }
                
                if self.memories:
                    # Calculate importance statistics
                    importances = [m.importance for m in self.memories]
                    stats['average_importance'] = sum(importances) / len(importances)
                    stats['max_importance'] = max(importances)
                    stats['min_importance'] = min(importances)
                    
                    # Count by memory type
                    for memory in self.memories:
                        memory_type = memory.memory_type
                        if memory_type not in stats['memory_types']:
                            stats['memory_types'][memory_type] = 0
                        stats['memory_types'][memory_type] += 1
                
                logger.debug(f"[ID:0290] Memory stats: {stats}")
                return stats
                
            finally:
                logger.debug("[ID:0289] Releasing mutex lock for memory stats")
                self.mutex.unlock()
                
        except Exception as e:
            logger.error(f"[ID:0288] Error getting memory stats: {e}", print_to_terminal=True)
            return {
                'total_memories': 0,
                'model_loaded': True,
                'error': str(e),
                'fallback_mode': True
            }
    
    def clear_all(self):
        """Clear all memories"""
        try:
            logger.debug("[ID:0286] Clearing all memories with mutex lock")
            self.mutex.lock()
            
            try:
                memory_count = len(self.memories)
                self.memories.clear()
                
                # Clear cache file
                if os.path.exists(self.metadata_file):
                    os.remove(self.metadata_file)
                
                logger.debug(f"[ID:0285] Cleared {memory_count} memories and cache files")
                self.embeddings_updated.emit()
                
            finally:
                logger.debug("[ID:0284] Releasing mutex lock for clear all")
                self.mutex.unlock()
                
        except Exception as e:
            logger.error(f"[ID:0283] Error clearing all memories: {e}", print_to_terminal=True)
    
    def is_ready(self) -> bool:
        """Check if the memory service is ready"""
        is_ready = True  # Always ready for fallback
        logger.debug(f"[ID:0281] Memory service ready check: {is_ready}")
        return is_ready 
"""
Semantic Search Service - Advanced memory retrieval using vector embeddings
"""

import os
import json
import pickle
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from PySide6.QtCore import QObject, Signal, QThread, QMutex
from pyside_chat.core.logging.logger import CustomLogger
import traceback

logger = CustomLogger.get_logger(__name__)

@dataclass
class VectorizedMemory:
    """Represents a memory entry with its vector embedding"""
    memory_id: str
    content: str
    embedding: np.ndarray
    memory_type: str
    importance: float
    timestamp: str
    tags: List[str]
    metadata: Dict

class SemanticSearchService(QObject):
    """Service for semantic memory retrieval using vector embeddings"""
    
    embeddings_updated = Signal()  # Emitted when embeddings are updated
    search_completed = Signal(list)  # Emitted when search completes
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_dir: str = "User_history/memory/embeddings"):
        super().__init__()
        self.model_name = model_name
        self.cache_dir = cache_dir
        self.embeddings_file = os.path.join(cache_dir, "embeddings.pkl")
        self.metadata_file = os.path.join(cache_dir, "metadata.json")
        
        # Initialize the sentence transformer model
        self.model = None
        self.vectorized_memories: List[VectorizedMemory] = []
        self.mutex = QMutex()
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize the model in a separate thread to avoid blocking UI
        self._init_model()
    
    def _init_model(self):
        """Initialize the sentence transformer model"""
        try:
            logger.info(f"[ID:0339] Loading sentence transformer model: {self.model_name}", print_to_terminal=True)
            self.model = SentenceTransformer(self.model_name)
            logger.info("[ID:0338] Sentence transformer model loaded successfully", print_to_terminal=True)
            
            # Load existing embeddings if available
            self._load_embeddings()
            
        except Exception as e:
            logger.error(f"[ID:0337] Error loading sentence transformer model: {e}", print_to_terminal=True)
            logger.error("[ID:0336] Falling back to keyword-based search", print_to_terminal=True)
    
    def _load_embeddings(self):
        """Load existing embeddings from cache"""
        try:
            if os.path.exists(self.embeddings_file) and os.path.exists(self.metadata_file):
                logger.info("[ID:0335] Loading existing embeddings from cache", print_to_terminal=True)
                
                with open(self.embeddings_file, 'rb') as f:
                    embeddings_data = pickle.load(f)
                
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                self.vectorized_memories = []
                for i, (memory_id, embedding) in enumerate(embeddings_data.items()):
                    if memory_id in metadata:
                        meta = metadata[memory_id]
                        vectorized_memory = VectorizedMemory(
                            memory_id=memory_id,
                            content=meta.get('content', ''),
                            embedding=embedding,
                            memory_type=meta.get('memory_type', 'conversation'),
                            importance=meta.get('importance', 0.5),
                            timestamp=meta.get('timestamp', ''),
                            tags=meta.get('tags', []),
                            metadata=meta.get('metadata', {})
                        )
                        self.vectorized_memories.append(vectorized_memory)
                
                logger.info(f"[ID:0334] Loaded {len(self.vectorized_memories)} vectorized memories", print_to_terminal=True)
                
        except Exception as e:
            logger.error(f"[ID:0333] Error loading embeddings: {e}", print_to_terminal=True)
            self.vectorized_memories = []
    
    def _save_embeddings(self):
        """Save embeddings to cache"""
        try:
            if not self.vectorized_memories:
                return
            
            # Prepare data for saving
            embeddings_data = {}
            metadata = {}
            
            for vm in self.vectorized_memories:
                embeddings_data[vm.memory_id] = vm.embedding
                metadata[vm.memory_id] = {
                    'content': vm.content,
                    'memory_type': vm.memory_type,
                    'importance': vm.importance,
                    'timestamp': vm.timestamp,
                    'tags': vm.tags,
                    'metadata': vm.metadata
                }
            
            # Save embeddings
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(embeddings_data, f)
            
            # Save metadata
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"[ID:0332] Saved {len(self.vectorized_memories)} embeddings to cache", print_to_terminal=True)
            
        except Exception as e:
            logger.error(f"[ID:0331] Error saving embeddings: {e}", print_to_terminal=True)
    
    def add_memory(self, memory_id: str, content: str, memory_type: str = "conversation", 
                   importance: float = 0.5, tags: List[str] = None, metadata: Dict = None) -> bool:
        """Add a new memory with vector embedding"""
        if not self.model:
            logger.warning("[ID:0330] Model not initialized, cannot add memory with embedding", print_to_terminal=True)
            return False
        
        try:
            logger.debug(f"[ID:0329] Adding memory with mutex lock - ID: {memory_id}")
            self.mutex.lock()
            
            try:
                # Check if memory already exists
                existing_memory = next((vm for vm in self.vectorized_memories if vm.memory_id == memory_id), None)
                if existing_memory:
                    logger.debug(f"[ID:0328] Memory {memory_id} already exists, updating", print_to_terminal=True)
                    self.vectorized_memories.remove(existing_memory)
                
                # Create embedding
                logger.debug(f"[ID:0327] Creating embedding for memory: {memory_id}")
                embedding = self.model.encode(content, convert_to_numpy=True)
                
                # Create vectorized memory
                vectorized_memory = VectorizedMemory(
                    memory_id=memory_id,
                    content=content,
                    embedding=embedding,
                    memory_type=memory_type,
                    importance=importance,
                    timestamp=datetime.now().isoformat(),
                    tags=tags or [],
                    metadata=metadata or {}
                )
                
                self.vectorized_memories.append(vectorized_memory)
                
                # Save to cache
                logger.debug(f"[ID:0326] Saving embeddings to cache for memory: {memory_id}")
                self._save_embeddings()
                
                logger.debug(f"[ID:0325] Added memory {memory_id} with embedding", print_to_terminal=True)
                self.embeddings_updated.emit()
                
                return True
                
            finally:
                logger.debug(f"[ID:0324] Releasing mutex lock for memory: {memory_id}")
                self.mutex.unlock()
            
        except Exception as e:
            logger.error(f"[ID:0323] Error adding memory with embedding: {e}", print_to_terminal=True)
            logger.error(f"[ID:0322] Add memory error traceback: {traceback.format_exc()}")
            return False
    
    def remove_memory(self, memory_id: str) -> bool:
        """Remove a memory and its embedding"""
        try:
            logger.debug(f"[ID:0321] Removing memory with mutex lock - ID: {memory_id}")
            self.mutex.lock()
            
            try:
                # Find and remove the memory
                memory_to_remove = next((vm for vm in self.vectorized_memories if vm.memory_id == memory_id), None)
                if memory_to_remove:
                    self.vectorized_memories.remove(memory_to_remove)
                    logger.debug(f"[ID:0320] Saving embeddings after removal for memory: {memory_id}")
                    self._save_embeddings()
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
            logger.error(f"[ID:0315] Remove memory error traceback: {traceback.format_exc()}")
            return False
    
    def search_semantic(self, query: str, max_results: int = 10, min_similarity: float = 0.3, 
                       memory_types: List[str] = None) -> List[Tuple[str, float, Dict]]:
        """Search memories using semantic similarity"""
        if not self.model:
            logger.warning("[ID:0314] Model not initialized, cannot perform semantic search", print_to_terminal=True)
            return []
        
        try:
            logger.debug(f"[ID:0313] Starting semantic search - Query: {query[:50]}...")
            logger.debug(f"[ID:0312] Search parameters - Max results: {max_results}, Min similarity: {min_similarity}")
            
            # Create query embedding
            query_embedding = self.model.encode(query, convert_to_numpy=True)
            
            # Filter memories by type if specified
            memories_to_search = self.vectorized_memories
            if memory_types:
                memories_to_search = [vm for vm in self.vectorized_memories if vm.memory_type in memory_types]
                logger.debug(f"[ID:0311] Filtered to {len(memories_to_search)} memories of types: {memory_types}")
            
            if not memories_to_search:
                logger.debug("[ID:0310] No memories to search")
                return []
            
            # Calculate similarities
            similarities = []
            for vm in memories_to_search:
                similarity = cosine_similarity([query_embedding], [vm.embedding])[0][0]
                similarities.append((vm.memory_id, similarity, {
                    'content': vm.content,
                    'memory_type': vm.memory_type,
                    'importance': vm.importance,
                    'timestamp': vm.timestamp,
                    'tags': vm.tags,
                    'metadata': vm.metadata
                }))
            
            # Sort by similarity and filter by minimum threshold
            similarities.sort(key=lambda x: x[1], reverse=True)
            results = [(memory_id, similarity, metadata) for memory_id, similarity, metadata in similarities 
                      if similarity >= min_similarity][:max_results]
            
            logger.debug(f"[ID:0309] Semantic search completed - Found {len(results)} results")
            for memory_id, similarity, metadata in results:
                logger.debug(f"[ID:0308] - {memory_id}: {similarity:.3f}")
            
            return results
            
        except Exception as e:
            logger.error(f"[ID:0307] Error in semantic search: {e}", print_to_terminal=True)
            logger.error(f"[ID:0306] Semantic search error traceback: {traceback.format_exc()}")
            return []
    
    def search_hybrid(self, query: str, max_results: int = 10, min_similarity: float = 0.3,
                     memory_types: List[str] = None, keyword_weight: float = 0.3, 
                     semantic_weight: float = 0.7) -> List[Tuple[str, float, Dict]]:
        """Search memories using both semantic and keyword matching"""
        if not self.model:
            logger.warning("[ID:0305] Model not initialized, cannot perform hybrid search", print_to_terminal=True)
            return []
        
        try:
            logger.debug(f"[ID:0304] Starting hybrid search - Query: {query[:50]}...")
            logger.debug(f"[ID:0303] Hybrid search parameters - Keyword weight: {keyword_weight}, Semantic weight: {semantic_weight}")
            
            # Get semantic results
            semantic_results = self.search_semantic(query, max_results * 2, min_similarity, memory_types)
            
            # Simple keyword matching
            query_lower = query.lower()
            keyword_results = []
            
            memories_to_search = self.vectorized_memories
            if memory_types:
                memories_to_search = [vm for vm in self.vectorized_memories if vm.memory_type in memory_types]
            
            for vm in memories_to_search:
                content_lower = vm.content.lower()
                # Simple keyword matching
                keyword_score = sum(1 for word in query_lower.split() if word in content_lower) / len(query_lower.split())
                if keyword_score > 0:
                    keyword_results.append((vm.memory_id, keyword_score, {
                        'content': vm.content,
                        'memory_type': vm.memory_type,
                        'importance': vm.importance,
                        'timestamp': vm.timestamp,
                        'tags': vm.tags,
                        'metadata': vm.metadata
                    }))
            
            # Combine results
            combined_scores = {}
            for memory_id, semantic_score, metadata in semantic_results:
                combined_scores[memory_id] = {
                    'semantic_score': semantic_score,
                    'keyword_score': 0,
                    'combined_score': semantic_score * semantic_weight,
                    'metadata': metadata
                }
            
            for memory_id, keyword_score, metadata in keyword_results:
                if memory_id in combined_scores:
                    combined_scores[memory_id]['keyword_score'] = keyword_score
                    combined_scores[memory_id]['combined_score'] += keyword_score * keyword_weight
                else:
                    combined_scores[memory_id] = {
                        'semantic_score': 0,
                        'keyword_score': keyword_score,
                        'combined_score': keyword_score * keyword_weight,
                        'metadata': metadata
                    }
            
            # Sort by combined score
            results = [(memory_id, data['combined_score'], data['metadata']) 
                      for memory_id, data in combined_scores.items() 
                      if data['combined_score'] >= min_similarity]
            results.sort(key=lambda x: x[1], reverse=True)
            results = results[:max_results]
            
            logger.debug(f"[ID:0302] Hybrid search completed - Found {len(results)} results")
            for memory_id, combined_score, metadata in results:
                semantic_score = combined_scores[memory_id]['semantic_score']
                keyword_score = combined_scores[memory_id]['keyword_score']
                logger.debug(f"[ID:0301] - {memory_id}: combined={combined_score:.3f}, semantic={semantic_score:.3f}, keyword={keyword_score:.3f}")
            
            return results
            
        except Exception as e:
            logger.error(f"[ID:0300] Error in hybrid search: {e}", print_to_terminal=True)
            logger.error(f"[ID:0299] Hybrid search error traceback: {traceback.format_exc()}")
            return []
    
    def update_memory_importance(self, memory_id: str, new_importance: float) -> bool:
        """Update the importance of a memory"""
        try:
            logger.debug(f"[ID:0298] Updating memory importance with mutex lock - ID: {memory_id}, Importance: {new_importance}")
            self.mutex.lock()
            
            try:
                memory = next((vm for vm in self.vectorized_memories if vm.memory_id == memory_id), None)
                if memory:
                    memory.importance = new_importance
                    logger.debug(f"[ID:0297] Saving embeddings after importance update for memory: {memory_id}")
                    self._save_embeddings()
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
            logger.error(f"[ID:0292] Update importance error traceback: {traceback.format_exc()}")
            return False
    
    def get_memory_stats(self) -> Dict:
        """Get statistics about the semantic search service"""
        try:
            logger.debug("[ID:0291] Getting memory stats with mutex lock")
            self.mutex.lock()
            
            try:
                stats = {
                    'total_memories': len(self.vectorized_memories),
                    'model_loaded': self.model is not None,
                    'cache_dir': self.cache_dir,
                    'memory_types': {},
                    'average_importance': 0.0,
                    'max_importance': 0.0,
                    'min_importance': 1.0
                }
                
                if self.vectorized_memories:
                    # Calculate importance statistics
                    importances = [vm.importance for vm in self.vectorized_memories]
                    stats['average_importance'] = sum(importances) / len(importances)
                    stats['max_importance'] = max(importances)
                    stats['min_importance'] = min(importances)
                    
                    # Count by memory type
                    for vm in self.vectorized_memories:
                        memory_type = vm.memory_type
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
            logger.error(f"[ID:0287] Memory stats error traceback: {traceback.format_exc()}")
            return {
                'total_memories': 0,
                'model_loaded': False,
                'error': str(e)
            }
    
    def clear_all(self):
        """Clear all memories and embeddings"""
        try:
            logger.debug("[ID:0286] Clearing all memories with mutex lock")
            self.mutex.lock()
            
            try:
                memory_count = len(self.vectorized_memories)
                self.vectorized_memories.clear()
                
                # Clear cache files
                if os.path.exists(self.embeddings_file):
                    os.remove(self.embeddings_file)
                if os.path.exists(self.metadata_file):
                    os.remove(self.metadata_file)
                
                logger.debug(f"[ID:0285] Cleared {memory_count} memories and cache files")
                self.embeddings_updated.emit()
                
            finally:
                logger.debug("[ID:0284] Releasing mutex lock for clear all")
                self.mutex.unlock()
                
        except Exception as e:
            logger.error(f"[ID:0283] Error clearing all memories: {e}", print_to_terminal=True)
            logger.error(f"[ID:0282] Clear all error traceback: {traceback.format_exc()}")
    
    def is_ready(self) -> bool:
        """Check if the semantic search service is ready"""
        is_ready = self.model is not None
        logger.debug(f"[ID:0281] Semantic search service ready check: {is_ready}")
        return is_ready 
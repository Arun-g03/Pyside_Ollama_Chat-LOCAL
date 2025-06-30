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
from SRC.utils.Logging.Custom_Logger import CustomLogger

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
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_dir: str = "memory/embeddings"):
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
            logger.info(f"Loading sentence transformer model: {self.model_name}", print_to_terminal=True)
            self.model = SentenceTransformer(self.model_name)
            logger.info("Sentence transformer model loaded successfully", print_to_terminal=True)
            
            # Load existing embeddings if available
            self._load_embeddings()
            
        except Exception as e:
            logger.error(f"Error loading sentence transformer model: {e}", print_to_terminal=True)
            logger.error("Falling back to keyword-based search", print_to_terminal=True)
    
    def _load_embeddings(self):
        """Load existing embeddings from cache"""
        try:
            if os.path.exists(self.embeddings_file) and os.path.exists(self.metadata_file):
                logger.info("Loading existing embeddings from cache", print_to_terminal=True)
                
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
                
                logger.info(f"Loaded {len(self.vectorized_memories)} vectorized memories", print_to_terminal=True)
                
        except Exception as e:
            logger.error(f"Error loading embeddings: {e}", print_to_terminal=True)
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
            
            logger.debug(f"Saved {len(self.vectorized_memories)} embeddings to cache", print_to_terminal=True)
            
        except Exception as e:
            logger.error(f"Error saving embeddings: {e}", print_to_terminal=True)
    
    def add_memory(self, memory_id: str, content: str, memory_type: str = "conversation", 
                   importance: float = 0.5, tags: List[str] = None, metadata: Dict = None) -> bool:
        """Add a new memory with vector embedding"""
        if not self.model:
            logger.warning("Model not initialized, cannot add memory with embedding", print_to_terminal=True)
            return False
        
        try:
            self.mutex.lock()
            
            # Check if memory already exists
            existing_memory = next((vm for vm in self.vectorized_memories if vm.memory_id == memory_id), None)
            if existing_memory:
                logger.debug(f"Memory {memory_id} already exists, updating", print_to_terminal=True)
                self.vectorized_memories.remove(existing_memory)
            
            # Create embedding
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
            self._save_embeddings()
            
            logger.debug(f"Added memory {memory_id} with embedding", print_to_terminal=True)
            self.embeddings_updated.emit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding memory with embedding: {e}", print_to_terminal=True)
            return False
        finally:
            self.mutex.unlock()
    
    def remove_memory(self, memory_id: str) -> bool:
        """Remove a memory and its embedding"""
        try:
            self.mutex.lock()
            
            # Find and remove the memory
            memory_to_remove = next((vm for vm in self.vectorized_memories if vm.memory_id == memory_id), None)
            if memory_to_remove:
                self.vectorized_memories.remove(memory_to_remove)
                self._save_embeddings()
                logger.debug(f"Removed memory {memory_id}", print_to_terminal=True)
                self.embeddings_updated.emit()
                return True
            else:
                logger.debug(f"Memory {memory_id} not found", print_to_terminal=True)
                return False
                
        except Exception as e:
            logger.error(f"Error removing memory: {e}", print_to_terminal=True)
            return False
        finally:
            self.mutex.unlock()
    
    def search_semantic(self, query: str, max_results: int = 10, min_similarity: float = 0.3, 
                       memory_types: List[str] = None) -> List[Tuple[str, float, Dict]]:
        """
        Search memories using semantic similarity
        
        Returns:
            List of tuples: (memory_id, similarity_score, memory_data)
        """
        if not self.model or not self.vectorized_memories:
            logger.debug("No model or memories available for semantic search", print_to_terminal=True)
            return []
        
        try:
            self.mutex.lock()
            
            # Create query embedding
            query_embedding = self.model.encode(query, convert_to_numpy=True).reshape(1, -1)
            
            # Filter memories by type if specified
            memories_to_search = self.vectorized_memories
            if memory_types:
                memories_to_search = [vm for vm in self.vectorized_memories if vm.memory_type in memory_types]
            
            if not memories_to_search:
                logger.debug("No memories match the specified types", print_to_terminal=True)
                return []
            
            # Calculate similarities
            similarities = []
            for vm in memories_to_search:
                memory_embedding = vm.embedding.reshape(1, -1)
                similarity = cosine_similarity(query_embedding, memory_embedding)[0][0]
                
                # Apply importance boost
                boosted_similarity = similarity * (0.7 + 0.3 * vm.importance)
                
                if boosted_similarity >= min_similarity:
                    similarities.append((vm.memory_id, boosted_similarity, {
                        'content': vm.content,
                        'memory_type': vm.memory_type,
                        'importance': vm.importance,
                        'timestamp': vm.timestamp,
                        'tags': vm.tags,
                        'metadata': vm.metadata
                    }))
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            results = similarities[:max_results]
            
            logger.debug(f"Semantic search found {len(results)} results for query: '{query}'", print_to_terminal=True)
            for memory_id, similarity, _ in results[:3]:  # Log top 3 results
                logger.debug(f"  - {memory_id}: {similarity:.3f}", print_to_terminal=True)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}", print_to_terminal=True)
            return []
        finally:
            self.mutex.unlock()
    
    def search_hybrid(self, query: str, max_results: int = 10, min_similarity: float = 0.3,
                     memory_types: List[str] = None, keyword_weight: float = 0.3, 
                     semantic_weight: float = 0.7) -> List[Tuple[str, float, Dict]]:
        """
        Hybrid search combining semantic similarity and keyword matching
        
        Args:
            query: Search query
            max_results: Maximum number of results
            min_similarity: Minimum similarity threshold
            memory_types: Filter by memory types
            keyword_weight: Weight for keyword matching (0.0 to 1.0)
            semantic_weight: Weight for semantic similarity (0.0 to 1.0)
        """
        if not self.model or not self.vectorized_memories:
            logger.debug("No model or memories available for hybrid search", print_to_terminal=True)
            return []
        
        try:
            self.mutex.lock()
            
            # Filter memories by type if specified
            memories_to_search = self.vectorized_memories
            if memory_types:
                memories_to_search = [vm for vm in self.vectorized_memories if vm.memory_type in memory_types]
            
            if not memories_to_search:
                logger.debug("No memories match the specified types", print_to_terminal=True)
                return []
            
            # Create query embedding
            query_embedding = self.model.encode(query, convert_to_numpy=True).reshape(1, -1)
            query_words = set(query.lower().split())
            
            # Calculate hybrid scores
            hybrid_scores = []
            for vm in memories_to_search:
                # Semantic similarity
                memory_embedding = vm.embedding.reshape(1, -1)
                semantic_similarity = cosine_similarity(query_embedding, memory_embedding)[0][0]
                
                # Keyword matching
                content_words = set(vm.content.lower().split())
                tag_words = set()
                for tag in vm.tags:
                    tag_words.update(tag.lower().split())
                
                all_memory_words = content_words.union(tag_words)
                keyword_matches = len(query_words.intersection(all_memory_words))
                keyword_score = min(1.0, keyword_matches / max(1, len(query_words)))
                
                # Combine scores
                hybrid_score = (semantic_weight * semantic_similarity + 
                              keyword_weight * keyword_score) * (0.7 + 0.3 * vm.importance)
                
                if hybrid_score >= min_similarity:
                    hybrid_scores.append((vm.memory_id, hybrid_score, {
                        'content': vm.content,
                        'memory_type': vm.memory_type,
                        'importance': vm.importance,
                        'timestamp': vm.timestamp,
                        'tags': vm.tags,
                        'metadata': vm.metadata,
                        'semantic_similarity': semantic_similarity,
                        'keyword_score': keyword_score
                    }))
            
            # Sort by hybrid score (descending)
            hybrid_scores.sort(key=lambda x: x[1], reverse=True)
            
            results = hybrid_scores[:max_results]
            
            logger.debug(f"Hybrid search found {len(results)} results for query: '{query}'", print_to_terminal=True)
            for memory_id, score, data in results[:3]:  # Log top 3 results
                semantic = data.get('semantic_similarity', 0)
                keyword = data.get('keyword_score', 0)
                logger.debug(f"  - {memory_id}: {score:.3f} (semantic: {semantic:.3f}, keyword: {keyword:.3f})", print_to_terminal=True)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in hybrid search: {e}", print_to_terminal=True)
            return []
        finally:
            self.mutex.unlock()
    
    def update_memory_importance(self, memory_id: str, new_importance: float) -> bool:
        """Update the importance of a memory"""
        try:
            self.mutex.lock()
            
            memory = next((vm for vm in self.vectorized_memories if vm.memory_id == memory_id), None)
            if memory:
                memory.importance = new_importance
                self._save_embeddings()
                logger.debug(f"Updated importance for memory {memory_id}: {new_importance}", print_to_terminal=True)
                return True
            else:
                logger.debug(f"Memory {memory_id} not found for importance update", print_to_terminal=True)
                return False
                
        except Exception as e:
            logger.error(f"Error updating memory importance: {e}", print_to_terminal=True)
            return False
        finally:
            self.mutex.unlock()
    
    def get_memory_stats(self) -> Dict:
        """Get statistics about the vectorized memories"""
        try:
            self.mutex.lock()
            
            if not self.vectorized_memories:
                return {
                    'total_memories': 0,
                    'memory_types': {},
                    'average_importance': 0.0,
                    'model_loaded': self.model is not None
                }
            
            # Count by memory type
            memory_types = {}
            total_importance = 0.0
            
            for vm in self.vectorized_memories:
                memory_types[vm.memory_type] = memory_types.get(vm.memory_type, 0) + 1
                total_importance += vm.importance
            
            return {
                'total_memories': len(self.vectorized_memories),
                'memory_types': memory_types,
                'average_importance': total_importance / len(self.vectorized_memories),
                'model_loaded': self.model is not None,
                'model_name': self.model_name if self.model else None
            }
            
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}", print_to_terminal=True)
            return {
                'total_memories': 0,
                'memory_types': {},
                'average_importance': 0.0,
                'model_loaded': False,
                'error': str(e)
            }
        finally:
            self.mutex.unlock()
    
    def clear_all(self):
        """Clear all vectorized memories"""
        try:
            self.mutex.lock()
            
            self.vectorized_memories.clear()
            
            # Remove cache files
            if os.path.exists(self.embeddings_file):
                os.remove(self.embeddings_file)
            if os.path.exists(self.metadata_file):
                os.remove(self.metadata_file)
            
            logger.info("Cleared all vectorized memories", print_to_terminal=True)
            self.embeddings_updated.emit()
            
        except Exception as e:
            logger.error(f"Error clearing vectorized memories: {e}", print_to_terminal=True)
        finally:
            self.mutex.unlock()
    
    def is_ready(self) -> bool:
        """Check if the semantic search service is ready"""
        return self.model is not None and len(self.vectorized_memories) > 0 
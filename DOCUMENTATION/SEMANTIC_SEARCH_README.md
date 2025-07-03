# Semantic Search for Memory Retrieval

## Overview

This implementation enhances the memory retrieval system with semantic search capabilities using vector embeddings. Instead of relying solely on keyword matching, the system now uses sentence transformers to create vector representations of memories and queries, enabling more intelligent and contextually relevant memory retrieval.

## Features

### 🔍 **Semantic Search**
- **Vector Embeddings**: Uses the `all-MiniLM-L6-v2` model to create 384-dimensional embeddings
- **Cosine Similarity**: Calculates semantic similarity between query and memory vectors
- **Importance Boosting**: Factors in memory importance to improve relevance scoring

### 🔄 **Hybrid Search**
- **Combined Approach**: Merges semantic similarity with keyword matching
- **Configurable Weights**: Adjustable balance between semantic (70%) and keyword (30%) components
- **Fallback Support**: Gracefully falls back to keyword search if semantic search is unavailable

### 💾 **Persistent Storage**
- **Embedding Cache**: Stores vector embeddings in `memory/embeddings/embeddings.pkl`
- **Metadata Storage**: Maintains memory metadata in `memory/embeddings/metadata.json`
- **Automatic Loading**: Restores embeddings on application startup

### 🎯 **Smart Retrieval**
- **Type Filtering**: Filter memories by type (fact, preference, summary, etc.)
- **Relevance Thresholds**: Configurable minimum similarity scores
- **Result Ranking**: Sorted by relevance and importance

## Architecture

### Core Components

#### 1. **SemanticSearchService** (`pyside_chat/services/semantic_search_service.py`)
- Main service for semantic search operations
- Manages sentence transformer model
- Handles embedding creation and storage
- Provides search interfaces

#### 2. **VectorizedMemory** (Data Class)
```python
@dataclass
class VectorizedMemory:
    memory_id: str
    content: str
    embedding: np.ndarray
    memory_type: str
    importance: float
    timestamp: str
    tags: List[str]
    metadata: Dict
```

#### 3. **Enhanced MemoryService** (`pyside_chat/services/memory_service.py`)
- Integrates semantic search with existing memory system
- Maintains backward compatibility
- Provides unified memory management interface

### Search Methods

#### Semantic Search
```python
results = semantic_search.search_semantic(
    query="What music do I like?",
    max_results=10,
    min_similarity=0.3,
    memory_types=["preference", "fact"]
)
```

#### Hybrid Search
```python
results = semantic_search.search_hybrid(
    query="music and instruments",
    max_results=10,
    min_similarity=0.2,
    keyword_weight=0.3,
    semantic_weight=0.7
)
```

## Installation

### Dependencies
Add these to your `requirements.txt`:
```
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
```

### Installation Commands
```bash
pip install sentence-transformers scikit-learn
```

## Usage

### Basic Integration

The semantic search is automatically integrated into the existing memory system:

```python
from pyside_chat.services.memory_service import MemoryService

# Initialize memory service (includes semantic search)
memory_service = MemoryService()

# Add memories (automatically creates embeddings)
memory_id = memory_service.add_memory(
    content="I love playing guitar and listening to rock music",
    conversation_id="conv_123",
    importance=0.8,
    tags=["music", "guitar", "rock"],
    memory_type="preference"
)

# Retrieve relevant memories using semantic search
relevant_memories = memory_service.get_relevant_memories(
    query="What music do I enjoy?",
    limit=5,
    use_semantic=True  # Enable semantic search
)
```

### Advanced Usage

#### Direct Semantic Search Service
```python
from pyside_chat.services.semantic_search_service import SemanticSearchService

# Initialize service
semantic_search = SemanticSearchService()

# Add memory with embedding
semantic_search.add_memory(
    memory_id="mem_123",
    content="I work as a software developer",
    memory_type="fact",
    importance=0.9,
    tags=["job", "software", "developer"]
)

# Search with semantic similarity
results = semantic_search.search_semantic(
    query="Tell me about my job",
    max_results=5,
    min_similarity=0.3
)

for memory_id, similarity, data in results:
    print(f"{memory_id}: {similarity:.3f} - {data['content']}")
```

#### Hybrid Search Configuration
```python
# Customize hybrid search weights
results = semantic_search.search_hybrid(
    query="programming and coding",
    max_results=10,
    min_similarity=0.2,
    keyword_weight=0.4,    # 40% keyword matching
    semantic_weight=0.6    # 60% semantic similarity
)
```

## Configuration

### Model Selection
The default model is `all-MiniLM-L6-v2`, which provides a good balance of speed and accuracy. You can change this in the `SemanticSearchService` constructor:

```python
semantic_search = SemanticSearchService(model_name="all-mpnet-base-v2")
```

### Cache Directory
Embeddings are stored in `memory/embeddings/` by default. You can customize this:

```python
semantic_search = SemanticSearchService(cache_dir="custom/path/embeddings")
```

## Performance Considerations

### Model Loading
- **First Run**: Model download (~90MB) and initial loading may take 10-30 seconds
- **Subsequent Runs**: Model loads from cache in 2-5 seconds
- **Memory Usage**: Model requires ~200MB RAM

### Search Performance
- **Small Datasets** (<1000 memories): Near-instant results
- **Large Datasets** (>10000 memories): Consider using approximate nearest neighbor search
- **Embedding Creation**: ~1-5ms per memory entry

### Optimization Tips
1. **Batch Processing**: Add multiple memories at once when possible
2. **Regular Cleanup**: Remove old/unused memories to maintain performance
3. **Type Filtering**: Use memory type filters to reduce search space

## UI Integration

### Memory Tab Enhancements
The memory management UI now shows semantic search information:
- **Model Status**: Shows if the semantic search model is loaded
- **Model Name**: Displays the current model being used
- **Vectorized Memories**: Count of memories with embeddings

### Search Interface
The existing search functionality automatically uses semantic search when available, falling back to keyword search if needed.

## Testing

Run the test script to verify the implementation:

```bash
python test_semantic_search.py
```

This will:
1. Initialize the semantic search service
2. Add test memories
3. Perform various search queries
4. Display results and statistics
5. Clean up test data

## Troubleshooting

### Common Issues

#### Model Loading Fails
```
Error: Model not initialized, cannot add memory with embedding
```
**Solution**: Check internet connection for model download, ensure sufficient disk space

#### Low Search Results
```
No results found for semantic search
```
**Solution**: 
- Lower the `min_similarity` threshold
- Check if memories have been properly vectorized
- Verify the model is loaded (`semantic_search.is_ready()`)

#### Performance Issues
**Solution**:
- Reduce the number of memories
- Use type filtering to narrow search scope
- Consider upgrading hardware for large datasets

### Debug Information
Enable debug logging to see detailed information:
```python
import logging
logging.getLogger('pyside_chat.services.semantic_search_service').setLevel(logging.DEBUG)
```

## Future Enhancements

### Planned Features
1. **Approximate Nearest Neighbor**: For large-scale memory systems
2. **Multi-Modal Embeddings**: Support for images and other media
3. **Dynamic Re-ranking**: Real-time relevance adjustment
4. **Clustering**: Group similar memories for better organization
5. **Federated Search**: Search across multiple memory systems

### Model Improvements
- **Custom Fine-tuning**: Train models on domain-specific data
- **Model Ensembles**: Combine multiple models for better accuracy
- **Quantization**: Reduce model size for faster inference

## Contributing

When contributing to the semantic search system:

1. **Test Thoroughly**: Run the test script and add new test cases
2. **Performance Impact**: Measure the impact of changes on search speed
3. **Backward Compatibility**: Ensure existing memory functionality continues to work
4. **Documentation**: Update this README with new features or changes

## License

This semantic search implementation is part of the PySide Chat system and follows the same licensing terms. 
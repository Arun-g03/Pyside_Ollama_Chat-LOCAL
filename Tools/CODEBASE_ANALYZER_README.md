# Codebase Relationship Analyzer

A comprehensive utility for analyzing relationships between functions and classes in your Python codebase and generating detailed markdown reports.

## 📁 Files

- `codebase_analyzer.py` - Basic analyzer with core functionality
- `advanced_codebase_analyzer.py` - Enhanced analyzer with dependency tracking and graph analysis
- `run_analyzer.py` - Simple runner script that handles dependencies and execution
- `CODEBASE_ANALYZER_README.md` - This documentation file

## 🚀 Quick Start

### Option 1: Use the Runner Script (Recommended)

```bash
python run_analyzer.py
```

The runner script will:
1. Check and install required dependencies
2. Let you choose between basic and advanced analyzers
3. Generate comprehensive reports

### Option 2: Run Analyzers Directly

#### Basic Analyzer
```bash
python codebase_analyzer.py
```

#### Advanced Analyzer
```bash
python advanced_codebase_analyzer.py
```

## 📊 What the Analyzers Do

### Basic Analyzer (`codebase_analyzer.py`)
- Scans all Python files in the `pyside_chat` directory
- Identifies classes, functions, and imports
- Extracts method information, decorators, and docstrings
- Generates a comprehensive markdown report
- Finds inheritance relationships between classes

### Advanced Analyzer (`advanced_codebase_analyzer.py`)
Everything from the basic analyzer, plus:
- **Dependency Graph Analysis**: Uses NetworkX to build and analyze dependency graphs
- **Function Call Tracking**: Identifies which functions call other functions
- **Method Call Analysis**: Tracks method calls between classes
- **Circular Dependency Detection**: Finds potential circular dependencies
- **Influence Analysis**: Identifies most dependent and influential files
- **JSON Export**: Exports dependency graph data for further analysis

## 📄 Generated Reports

### Basic Analysis Report (`basic_codebase_analysis.md`)
- **Summary**: Total classes, functions, and files by directory
- **File Structure**: Overview of each file's contents
- **Classes**: Detailed information about each class including:
  - Base classes (inheritance)
  - Methods and their details
  - Decorators
  - Docstrings
- **Functions**: Detailed information about each function including:
  - Arguments and return types
  - Decorators
  - Docstrings
- **Relationships**: Inheritance and dependency relationships
- **Imports**: All import statements by file
- **Statistics**: Distribution of classes and functions by directory

### Advanced Analysis Report (`advanced_codebase_analysis.md`)
Everything from the basic report, plus:
- **Dependency Analysis**: 
  - Most dependent files (high in-degree)
  - Most influential files (high out-degree)
  - Circular dependency detection
- **Function Call Analysis**: Detailed breakdown of function and method calls
- **Enhanced Statistics**: Call statistics and dependency metrics

### Dependency Graph Data (`dependency_graph.json`)
JSON file containing:
- Nodes (files)
- Edges (dependencies)
- In-degree and out-degree statistics

## 🔧 Dependencies

The analyzers require:
- **Python 3.6+** (for f-strings and type hints)
- **networkx** (for advanced analyzer only) - automatically installed by the runner script

## 🎯 Features

### AST-Based Analysis
- Uses Python's Abstract Syntax Tree (AST) for accurate parsing
- Handles complex Python syntax including decorators, type hints, and nested structures
- Extracts docstrings, method signatures, and inheritance information

### Comprehensive Relationship Detection
- **Inheritance**: Tracks class inheritance hierarchies
- **Function Calls**: Identifies which functions call other functions
- **Method Calls**: Tracks method calls between classes
- **Import Dependencies**: Maps import relationships

### Advanced Graph Analysis
- **Dependency Graphs**: Visual representation of file dependencies
- **Centrality Analysis**: Identifies key files in the codebase
- **Cycle Detection**: Finds circular dependencies that could cause issues
- **Influence Metrics**: Measures how much each file affects others

### Detailed Reporting
- **Markdown Format**: Easy to read and version control friendly
- **Structured Sections**: Organized by type (classes, functions, relationships)
- **Statistics**: Quantitative analysis of codebase structure
- **File Organization**: Clear breakdown by directory structure

## 📈 Example Output

### Summary Section
```
## 📊 Summary

- **Total Classes:** 45
- **Total Functions:** 127
- **Total Files:** 23

### Files by Directory

- `MainApp/`: 5 files
- `services/`: 8 files
- `ui/`: 6 files
- `controllers/`: 2 files
- `config/`: 2 files
```

### Class Analysis
```
### `MainApp/ollama_chat.py.OllamaChatApp`

- **File:** `MainApp/ollama_chat.py`
- **Line:** 15
- **Bases:** QMainWindow
- **Decorators:** 
- **Docstring:** Main application class for the Ollama Chat interface...

**Methods:**
- `__init__` (line 25)
- `setup_ui` (line 45)
- `setup_connections` (line 78)
```

### Dependency Analysis
```
### Most Dependent Files (High In-Degree)

- `MainApp/ollama_chat.py`: 12 dependencies
- `services/ollama_service.py`: 8 dependencies
- `ui/chat_tab.py`: 6 dependencies
```

## 🛠️ Customization

### Changing the Root Path
Modify the `root_path` parameter in the analyzer constructor:

```python
# For basic analyzer
analyzer = CodebaseAnalyzer(root_path="your/custom/path")

# For advanced analyzer  
analyzer = AdvancedCodebaseAnalyzer(root_path="your/custom/path")
```

### Custom Output Files
Specify custom output file names:

```python
# Generate custom report names
analyzer.generate_markdown_report("my_custom_analysis.md")
analyzer.export_dependency_graph("my_dependency_graph.json")
```

### Filtering Files
Add custom filters in the `analyze_codebase` method:

```python
# Skip certain directories or files
if "test" in str(file_path) or "temp" in str(file_path):
    continue
```

## 🔍 Use Cases

### Code Review and Documentation
- Generate comprehensive documentation of your codebase structure
- Identify undocumented classes and functions
- Track inheritance hierarchies for better understanding

### Refactoring Planning
- Identify highly coupled files that need refactoring
- Find circular dependencies that could cause issues
- Locate files with too many responsibilities

### Architecture Analysis
- Understand the overall structure of your codebase
- Identify key components and their relationships
- Plan for better separation of concerns

### Dependency Management
- Track which files depend on which others
- Identify potential breaking changes
- Plan for better modularization

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: The runner script will automatically install missing dependencies
2. **Permission Errors**: Ensure you have write permissions in the current directory
3. **Large Codebases**: The analysis may take some time for very large codebases
4. **Complex Syntax**: Some very complex Python constructs might not be fully parsed

### Debug Mode
Add debug prints to the analyzer:

```python
# In the analyzer class
print(f"Debug: Analyzing {file_path}")
print(f"Debug: Found class {class_name}")
```

## 📝 Contributing

To extend the analyzers:

1. **Add New Relationship Types**: Extend the `_build_relationships` method
2. **Add New Analysis**: Create new methods and integrate them into the report generation
3. **Improve Parsing**: Enhance the AST parsing methods for better accuracy
4. **Add Visualizations**: Use the dependency graph data to create visual representations

## 📄 License

This utility is provided as-is for analyzing your codebase. Feel free to modify and extend it for your specific needs. 
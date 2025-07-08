import ast
import os
import re
import xml.etree.ElementTree as ET

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

HARDCODED_DIRECTORY_PATH = r"C:\Users\arun-\OneDrive\My developer career files\Ollama chat\Pyside_Ollama_Chat-LOCAL"
MAIN_FILE_PATH = r"C:\Users\arun-\OneDrive\My developer career files\Ollama chat\Pyside_Ollama_Chat-LOCAL\main.py"
IGNORE_FOLDERS = [
    "venv", "chat_env", "env", ".venv", "__pycache__", ".git", "node_modules", "build", "dist", ".pytest_cache", ".mypy_cache", ".coverage", "htmlcov", ".tox", ".eggs", "*.egg-info"
]
IGNORE_FILES = [
    "setup.py", "requirements.txt", "Pipfile", "poetry.lock", "package.json", "package-lock.json"
]
IGNORE_EXTENSIONS = [
    ".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe"
]
IGNORE_PATHS = []

ID_PATTERN = re.compile(r'\[ID:\d{4}\]\s*')

def find_logger_and_print_statements(filepath):
    """Find all logger calls and print statements in a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"[ID:0027] Warning: Could not read file {filepath} due to encoding issues. Skipping...")
            return []
    
    try:
        tree = ast.parse(content, filename=filepath)
    except SyntaxError as e:
        print(f"[ID:0026] Warning: Syntax error in {filepath}: {e}. Skipping...")
        return []
    
    statements = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check for logger calls (logger.info, logger.error, etc.)
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == 'logger':
                    # Get the line number and the full call
                    line_num = node.lineno
                    call_text = ast.unparse(node) if hasattr(ast, 'unparse') else str(node)
                    statements.append({
                        'type': 'logger',
                        'line': line_num,
                        'call': call_text,
                        'method': node.func.attr
                    })
            
            # Check for print statements
            elif isinstance(node.func, ast.Name) and node.func.id == 'print':
                line_num = node.lineno
                call_text = ast.unparse(node) if hasattr(ast, 'unparse') else str(node)
                statements.append({
                    'type': 'print',
                    'line': line_num,
                    'call': call_text,
                    'method': 'print'
                })
    
    return statements

def analyze_imports_and_calls(filepath):
    """Analyze imports and function calls to understand execution flow."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()
        except UnicodeDecodeError:
            return {"imports": [], "calls": [], "functions": []}
    
    try:
        tree = ast.parse(content, filename=filepath)
    except SyntaxError as e:
        return {"imports": [], "calls": [], "functions": []}
    
    imports = []
    calls = []
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            # Only use the module part, not the symbol being imported
            if node.module:
                imports.append(node.module)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    calls.append(f"{node.func.value.id}.{node.func.attr}")
    
    return {"imports": imports, "calls": calls, "functions": functions}

def parse_directory_for_logging(directory, ignore_env=None):
    """Parse directory for logger and print statements."""
    all_statements = {}
    all_imports_and_calls = {}
    
    for root, dirs, files in os.walk(directory):
        current_dir = os.path.basename(root)
        if current_dir in IGNORE_FOLDERS:
            dirs[:] = []
            continue
        rel_path = os.path.relpath(root, directory)
        if rel_path in IGNORE_PATHS:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
        if ignore_env:
            dirs[:] = [d for d in dirs if d != ignore_env]
        
        for file in files:
            if file in IGNORE_FILES:
                continue
            if any(file.endswith(ext) for ext in IGNORE_EXTENSIONS):
                continue
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                print(f"[ID:0025] Analyzing Python file: {filepath}")
                statements = find_logger_and_print_statements(filepath)
                imports_and_calls = analyze_imports_and_calls(filepath)
                all_imports_and_calls[filepath] = imports_and_calls  # <-- always add
                if statements:
                    all_statements[filepath] = statements
    
    return all_statements, all_imports_and_calls

def determine_execution_order(statements_dict, imports_and_calls_dict):
    """Determine execution order based on imports and function calls."""
    # Build dependency graph
    dependencies = {}
    file_to_module = {}
    
    # Map files to their module names
    for filepath in statements_dict.keys():
        module_name = os.path.splitext(os.path.basename(filepath))[0]
        file_to_module[filepath] = module_name
    
    # Build dependency relationships
    for filepath, imports_and_calls in imports_and_calls_dict.items():
        dependencies[filepath] = []
        for import_name in imports_and_calls["imports"]:
            # Try to find which file this import refers to
            for other_filepath in statements_dict.keys():
                other_module = file_to_module[other_filepath]
                if import_name == other_module or import_name.endswith(f".{other_module}"):
                    dependencies[filepath].append(other_filepath)
    
    # Find main file
    main_file = None
    if MAIN_FILE_PATH:
        main_file_abs = os.path.abspath(MAIN_FILE_PATH)
        for filepath in statements_dict.keys():
            if os.path.abspath(filepath) == main_file_abs:
                main_file = filepath
                break
    
    if not main_file:
        for filepath in statements_dict.keys():
            if os.path.basename(filepath) == "main.py":
                main_file = filepath
                break
    
    # Use topological sort to determine execution order
    execution_order = []
    visited = set()
    
    def visit(filepath):
        if filepath in visited:
            return
        visited.add(filepath)
        
        # Visit dependencies first
        for dep in dependencies.get(filepath, []):
            if dep in statements_dict:  # Only visit if dependency has statements
                visit(dep)
        
        execution_order.append(filepath)
    
    # Start with main file
    if main_file and main_file in statements_dict:
        visit(main_file)
    
    # Visit remaining files
    for filepath in statements_dict.keys():
        if filepath not in visited:
            visit(filepath)
    
    return execution_order

def add_sequential_ids(statements_dict, imports_and_calls_dict=None):
    """Add sequential IDs to all logger and print statements."""
    global_id_counter = 1
    updated_files = {}
    
    # Determine execution order
    if imports_and_calls_dict:
        sorted_files = determine_execution_order(statements_dict, imports_and_calls_dict)
        print(f"Execution order based on dependencies:")
        for i, filepath in enumerate(sorted_files, 1):
            print(f"  {i}. {filepath}")
    else:
        # Fallback to simple sorting
        sorted_files = []
        main_file_found = False
        
        # First, add the main file if it exists in statements_dict
        if MAIN_FILE_PATH:
            main_file_abs = os.path.abspath(MAIN_FILE_PATH)
            for filepath in statements_dict.keys():
                if os.path.abspath(filepath) == main_file_abs:
                    sorted_files.append(filepath)
                    main_file_found = True
                    break
        
        # If main file not found, look for any main.py
        if not main_file_found:
            for filepath in statements_dict.keys():
                if os.path.basename(filepath) == "main.py":
                    sorted_files.append(filepath)
                    main_file_found = True
                    break
        
        # Add remaining files
        for filepath in statements_dict.keys():
            if filepath not in sorted_files:
                sorted_files.append(filepath)
        
        print(f"Processing files in order:")
        for i, filepath in enumerate(sorted_files, 1):
            print(f"  {i}. {filepath}")
    
    # Process files in sorted order
    print(f"Processing files in order:")
    for i, filepath in enumerate(sorted_files, 1):
        print(f"  {i}. {filepath}")
    
    for filepath in sorted_files:
        print(f"Processing file: {filepath}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(filepath, "r", encoding="latin-1") as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                print(f"[ID:0024] Warning: Could not read file {filepath} for updating. Skipping...")
                continue
        
        # Sort statements by line number (descending) to avoid line number shifts
        sorted_statements = sorted(statements_dict[filepath], key=lambda x: x['line'], reverse=True)
        updated_lines = lines.copy()
        
        for statement in sorted_statements:
            line_num = statement['line'] - 1  # Convert to 0-based index
            original_line = lines[line_num].rstrip()
            
            # Remove any existing [ID:xxxx] tags
            clean_line = ID_PATTERN.sub('', original_line)

            # Create the ID
            id_text = f"[ID:{global_id_counter:04d}] "
            
            # Add ID to the statement
            if clean_line.strip().startswith('logger.'):
                # For logger calls, add ID inside the logger statement
                # Find the opening quote and insert ID after it
                if '"' in clean_line:
                    # Find the first quote after logger.method(
                    start_idx = clean_line.find('(') + 1
                    quote_idx = clean_line.find('"', start_idx)
                    if quote_idx != -1:
                        # Insert ID after the opening quote
                        new_line = clean_line[:quote_idx + 1] + id_text + clean_line[quote_idx + 1:]
                    else:
                        # Fallback: add ID at the beginning of the line
                        new_line = id_text + clean_line
                elif "'" in clean_line:
                    # Find the first single quote after logger.method(
                    start_idx = clean_line.find('(') + 1
                    quote_idx = clean_line.find("'", start_idx)
                    if quote_idx != -1:
                        # Insert ID after the opening quote
                        new_line = clean_line[:quote_idx + 1] + id_text + clean_line[quote_idx + 1:]
                    else:
                        # Fallback: add ID at the beginning of the line
                        new_line = id_text + clean_line
                else:
                    # No quotes found, add ID at the beginning of the line
                    new_line = id_text + clean_line
            elif clean_line.strip().startswith('print('):
                # For print statements, add ID inside the print statement
                # Find the opening quote and insert ID after it
                if '"' in clean_line:
                    # Find the first quote after print(
                    start_idx = clean_line.find('print(') + 5
                    quote_idx = clean_line.find('"', start_idx)
                    if quote_idx != -1:
                        # Insert ID after the opening quote
                        new_line = clean_line[:quote_idx + 1] + id_text + clean_line[quote_idx + 1:]
                    else:
                        # Fallback: add ID at the beginning of the line
                        new_line = id_text + clean_line
                elif "'" in clean_line:
                    # Find the first single quote after print(
                    start_idx = clean_line.find('print(') + 5
                    quote_idx = clean_line.find("'", start_idx)
                    if quote_idx != -1:
                        # Insert ID after the opening quote
                        new_line = clean_line[:quote_idx + 1] + id_text + clean_line[quote_idx + 1:]
                    else:
                        # Fallback: add ID at the beginning of the line
                        new_line = id_text + clean_line
                else:
                    # No quotes found, add ID at the beginning of the line
                    new_line = id_text + clean_line
            else:
                # Fallback: add ID at the beginning of the line
                new_line = id_text + clean_line
            
            updated_lines[line_num] = new_line + '\n'
            global_id_counter += 1
        
        updated_files[filepath] = updated_lines
    
    return updated_files

def write_updated_files(updated_files):
    """Write the updated files back to disk."""
    for filepath, lines in updated_files.items():
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"[ID:0023] Updated file: {filepath}")
        except Exception as e:
            print(f"[ID:0022] Error writing to {filepath}: {e}")

def generate_report(statements_dict, output_file="logging_report.xml"):
    """Generate an XML report of all logger and print statements."""
    root = ET.Element("logging_report")
    
    # Add metadata
    metadata = ET.SubElement(root, "metadata")
    ET.SubElement(metadata, "total_files").text = str(len(statements_dict))
    total_statements = sum(len(statements) for statements in statements_dict.values())
    ET.SubElement(metadata, "total_statements").text = str(total_statements)
    
    # Add file details
    files_elem = ET.SubElement(root, "files")
    
    for filepath, statements in statements_dict.items():
        file_elem = ET.SubElement(files_elem, "file")
        ET.SubElement(file_elem, "path").text = filepath
        ET.SubElement(file_elem, "statement_count").text = str(len(statements))
        
        statements_elem = ET.SubElement(file_elem, "statements")
        for statement in statements:
            stmt_elem = ET.SubElement(statements_elem, "statement")
            ET.SubElement(stmt_elem, "type").text = statement['type']
            ET.SubElement(stmt_elem, "line").text = str(statement['line'])
            ET.SubElement(stmt_elem, "method").text = statement['method']
            ET.SubElement(stmt_elem, "call").text = statement['call']
    
    # Write XML to file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"[ID:0021] Logging report saved to: {output_file}")

def print_summary(statements_dict):
    """Print a summary of found logger and print statements."""
    total_files = len(statements_dict)
    total_statements = sum(len(statements) for statements in statements_dict.values())
    
    logger_count = 0
    print_count = 0
    
    for statements in statements_dict.values():
        for statement in statements:
            if statement['type'] == 'logger':
                logger_count += 1
            elif statement['type'] == 'print':
                print_count += 1
    
    print(f"[ID:0020] \n=== LOGGING STATEMENT SUMMARY ===")
    print(f"[ID:0019] Files analyzed: {total_files}")
    print(f"[ID:0018] Total statements found: {total_statements}")
    print(f"[ID:0017] Logger calls: {logger_count}")
    print(f"[ID:0016] Print statements: {print_count}")
    print(f"[ID:0015] ===================================\n")

def build_module_to_file_map(directory):
    module_to_file = {}
    for root, dirs, files in os.walk(directory):
        # Skip ignored folders
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, directory)
                no_ext = os.path.splitext(rel_path)[0]
                module_name = no_ext.replace(os.sep, '.')
                module_to_file[module_name] = filepath
    return module_to_file

def get_reachable_files(main_file, imports_and_calls_dict, module_to_file):
    """Return set of files reachable from main_file via imports."""
    reachable = set()
    stack = [main_file]
    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        for import_name in imports_and_calls_dict.get(current, {}).get("imports", []):
            if import_name in module_to_file:
                stack.append(module_to_file[import_name])
            # else: skip (external or stdlib)
    return reachable

def module_name_from_path(filepath, base_dir):
    rel_path = os.path.relpath(filepath, base_dir)
    no_ext = os.path.splitext(rel_path)[0]
    return no_ext.replace(os.sep, '.')

if __name__ == "__main__":
    if HARDCODED_DIRECTORY_PATH:
        directory_path = HARDCODED_DIRECTORY_PATH
        print(f"[ID:0014] Using hardcoded directory path: {directory_path}")
    else:
        while True:
            directory_path = input("Enter the directory path to analyze (or 'quit' to exit): ").strip()
            if directory_path.lower() == 'quit':
                print("[ID:0013] Exiting...")
                break
            if not os.path.exists(directory_path):
                print(f"[ID:0012] Error: Directory '{directory_path}' does not exist. Please enter a valid path.")
                continue
            if not os.path.isdir(directory_path):
                print(f"[ID:0011] Error: '{directory_path}' is not a directory. Please enter a valid directory path.")
                continue
            break
    
    print(f"[ID:0010] Analyzing directory: {directory_path}")
    print(f"[ID:0009] Ignoring folders: {IGNORE_FOLDERS}")
    print(f"[ID:0008] Ignoring files: {IGNORE_FILES}")
    print(f"[ID:0007] Ignoring file extensions: {IGNORE_EXTENSIONS}")
    print(f"[ID:0006] Ignoring paths: {IGNORE_PATHS}")
    
    ignore_env = input("Enter additional environment folder name to ignore (or press Enter to skip): ").strip()
    if not ignore_env:
        ignore_env = None
    
    try:
        # Find all logger and print statements
        statements_dict, imports_and_calls_dict = parse_directory_for_logging(directory_path, ignore_env)
        
        # Build a mapping from module path to file path for ALL files
        module_to_file = build_module_to_file_map(directory_path)
        print("[DEBUG] module_to_file mapping:")
        for k, v in module_to_file.items():
            print(f"  {k}: {v}")
        
        # Restrict to only files reachable from MAIN_FILE_PATH
        main_file_abs = os.path.abspath(MAIN_FILE_PATH)
        main_file = None
        for f in module_to_file.values():
            if os.path.abspath(f) == main_file_abs:
                main_file = f
                break
        if main_file:
            reachable = get_reachable_files(main_file, imports_and_calls_dict, module_to_file)
            print("[DEBUG] Reachable files:")
            for f in reachable:
                print(f"  {f}")
            statements_dict = {k: v for k, v in statements_dict.items() if k in reachable}
            imports_and_calls_dict = {k: v for k, v in imports_and_calls_dict.items() if k in reachable}
        
        if not statements_dict:
            print("[ID:0005] No logger or print statements found in the specified directory.")
        else:
            # Print summary
            print_summary(statements_dict)
            
            # Generate report
            generate_report(statements_dict)
            
            # Ask user if they want to add IDs
            add_ids = input("Do you want to add sequential IDs to the statements? (y/n): ").strip().lower()
            
            if add_ids == 'y':
                # Add sequential IDs
                updated_files = add_sequential_ids(statements_dict, imports_and_calls_dict)
                
                # Write updated files
                write_updated_files(updated_files)
                
                print(f"[ID:0004] \nOperation complete!")
                print(f"[ID:0003] Added IDs to {len(updated_files)} files")
            else:
                print("[ID:0002] Skipping ID addition. Report generated only.")
                
    except Exception as e:
        print(f"[ID:0001] An error occurred: {e}")

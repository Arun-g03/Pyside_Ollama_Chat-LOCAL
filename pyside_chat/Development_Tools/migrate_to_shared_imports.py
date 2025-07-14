#!/usr/bin/env python3
"""
Migration Script: Convert to Shared Imports

This script helps migrate existing files to use the generated shared import files.
It can automatically replace common import patterns with shared import statements.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
import json

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import mapping for shared imports
SHARED_IMPORT_MAPPINGS = {
    'os_sys': {
        'imports': ['os', 'sys', 'tempfile'],
        'from_imports': [('pathlib', 'Path')],
        'shared_file': 'pyside_chat.core.shared_imports.os_sys_imports',
        'description': 'OS and system utilities'
    },
    'json_time': {
        'imports': ['json', 'time'],
        'from_imports': [('datetime', 'datetime')],
        'shared_file': 'pyside_chat.core.shared_imports.json_time_imports',
        'description': 'JSON and time utilities'
    },
    'audio': {
        'imports': ['pyaudio', 'sounddevice', 'soundfile', 'librosa'],
        'from_imports': [],
        'shared_file': 'pyside_chat.core.shared_imports.audio_imports',
        'description': 'Audio processing libraries'
    }
}

class ImportMigrator:
    """Migrate files to use shared imports"""
    
    def __init__(self, codebase_path: str = "pyside_chat"):
        self.codebase_path = Path(codebase_path)
        self.migration_stats = {
            'files_processed': 0,
            'files_migrated': 0,
            'imports_replaced': 0,
            'errors': []
        }
    
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the codebase"""
        python_files = list(self.codebase_path.rglob("*.py"))
        # Exclude shared import files and the migrator itself
        filtered_files = [
            f for f in python_files 
            if not f.name.startswith('_') and 
               'shared_imports' not in str(f) and
               f.name != 'migrate_to_shared_imports.py' and
               f.name != 'import_analyzer.py' and
               f.name != 'run_import_analyzer.py'
        ]
        return filtered_files
    
    def analyze_file_imports(self, file_path: Path) -> Dict[str, Set[str]]:
        """Analyze imports in a file to determine which shared imports to use"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find regular imports
            import_pattern = r'^import\s+(\w+)'
            imports = set(re.findall(import_pattern, content, re.MULTILINE))
            
            # Find from imports
            from_import_pattern = r'^from\s+(\w+(?:\.\w+)*)\s+import\s+(\w+)'
            from_imports = set()
            for match in re.finditer(from_import_pattern, content, re.MULTILINE):
                module, item = match.groups()
                from_imports.add(f"{module}.{item}")
            
            return {
                'imports': imports,
                'from_imports': from_imports,
                'content': content
            }
        except Exception as e:
            self.migration_stats['errors'].append(f"Error reading {file_path}: {e}")
            return {'imports': set(), 'from_imports': set(), 'content': ''}
    
    def determine_shared_imports_needed(self, file_analysis: Dict) -> Set[str]:
        """Determine which shared import files are needed for this file"""
        needed_shared_imports = set()
        
        for category, mapping in SHARED_IMPORT_MAPPINGS.items():
            # Check if any imports from this category are used
            imports_used = any(imp in file_analysis['imports'] for imp in mapping['imports'])
            from_imports_used = any(imp in file_analysis['from_imports'] for imp in mapping['from_imports'])
            
            if imports_used or from_imports_used:
                needed_shared_imports.add(category)
        
        return needed_shared_imports
    
    def generate_shared_import_statements(self, needed_imports: Set[str]) -> List[str]:
        """Generate the shared import statements for the needed imports"""
        statements = []
        
        for category in sorted(needed_imports):
            if category in SHARED_IMPORT_MAPPINGS:
                shared_file = SHARED_IMPORT_MAPPINGS[category]['shared_file']
                statements.append(f"from {shared_file} import *")
        
        return statements
    
    def remove_individual_imports(self, content: str, needed_imports: Set[str]) -> str:
        """Remove individual import statements that are now covered by shared imports"""
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            
            # Check if this line should be removed
            should_remove = False
            
            for category in needed_imports:
                if category in SHARED_IMPORT_MAPPINGS:
                    mapping = SHARED_IMPORT_MAPPINGS[category]
                    
                    # Check regular imports
                    for imp in mapping['imports']:
                        if re.match(rf'^import\s+{re.escape(imp)}\s*$', line.strip()):
                            should_remove = True
                            break
                    
                    # Check from imports
                    for module, item in mapping['from_imports']:
                        if re.match(rf'^from\s+{re.escape(module)}\s+import\s+{re.escape(item)}\s*$', line.strip()):
                            should_remove = True
                            break
            
            if should_remove:
                continue
            
            # Handle multi-line imports
            if line.strip().endswith('\\'):
                # Check if the next line should also be removed
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    for category in needed_imports:
                        if category in SHARED_IMPORT_MAPPINGS:
                            mapping = SHARED_IMPORT_MAPPINGS[category]
                            for imp in mapping['imports']:
                                if imp in next_line:
                                    skip_next = True
                                    break
            
            new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def migrate_file(self, file_path: Path, dry_run: bool = True) -> bool:
        """Migrate a single file to use shared imports"""
        try:
            # Analyze the file
            analysis = self.analyze_file_imports(file_path)
            if not analysis['content']:
                return False
            
            # Determine which shared imports are needed
            needed_imports = self.determine_shared_imports_needed(analysis)
            
            if not needed_imports:
                return False  # No migration needed
            
            # Generate shared import statements
            shared_import_statements = self.generate_shared_import_statements(needed_imports)
            
            # Remove individual imports
            new_content = self.remove_individual_imports(analysis['content'], needed_imports)
            
            # Add shared import statements at the top (after existing imports)
            lines = new_content.split('\n')
            insert_index = 0
            
            # Find the end of existing imports
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                if line_stripped and not line_stripped.startswith(('#', 'import', 'from')):
                    insert_index = i
                    break
            
            # Insert shared import statements
            if shared_import_statements:
                lines.insert(insert_index, '')
                for statement in shared_import_statements:
                    lines.insert(insert_index, statement)
                lines.insert(insert_index, '# Shared imports')
            
            new_content = '\n'.join(lines)
            
            # Write the file (if not dry run)
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            # Update statistics
            self.migration_stats['files_processed'] += 1
            if needed_imports:
                self.migration_stats['files_migrated'] += 1
                self.migration_stats['imports_replaced'] += len(needed_imports)
            
            return True
            
        except Exception as e:
            self.migration_stats['errors'].append(f"Error migrating {file_path}: {e}")
            return False
    
    def migrate_codebase(self, dry_run: bool = True) -> Dict:
        """Migrate the entire codebase to use shared imports"""
        print(f"{'🔍 DRY RUN' if dry_run else '🚀 MIGRATING'} codebase to shared imports...")
        
        python_files = self.find_python_files()
        print(f"Found {len(python_files)} Python files to process")
        
        for file_path in python_files:
            try:
                self.migrate_file(file_path, dry_run)
                if dry_run:
                    print(f"  📄 Would migrate: {file_path}")
            except Exception as e:
                print(f"  ❌ Error processing {file_path}: {e}")
        
        return self.migration_stats
    
    def print_migration_report(self):
        """Print a summary of the migration"""
        print("\n" + "="*60)
        print("MIGRATION SUMMARY")
        print("="*60)
        
        print(f"📄 Files processed: {self.migration_stats['files_processed']}")
        print(f"🔄 Files migrated: {self.migration_stats['files_migrated']}")
        print(f"📦 Shared import groups added: {self.migration_stats['imports_replaced']}")
        
        if self.migration_stats['errors']:
            print(f"\n❌ Errors encountered: {len(self.migration_stats['errors'])}")
            for error in self.migration_stats['errors'][:5]:  # Show first 5 errors
                print(f"   {error}")
            if len(self.migration_stats['errors']) > 5:
                print(f"   ... and {len(self.migration_stats['errors']) - 5} more")
        
        print("\n📋 Shared import categories available:")
        for category, mapping in SHARED_IMPORT_MAPPINGS.items():
            print(f"   {category}: {mapping['description']}")
            print(f"      Imports: {', '.join(mapping['imports'])}")
            if mapping['from_imports']:
                print(f"      From imports: {', '.join([f'{m}.{i}' for m, i in mapping['from_imports']])}")
        
        print("="*60)

def main():
    """Main function to run the migration"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate codebase to shared imports")
    parser.add_argument(
        "--codebase", 
        default="pyside_chat", 
        help="Path to the codebase to migrate (default: pyside_chat)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        default=True,
        help="Perform a dry run without making changes (default: True)"
    )
    parser.add_argument(
        "--apply", 
        action="store_true", 
        help="Actually apply the changes (overrides --dry-run)"
    )
    parser.add_argument(
        "--file", 
        help="Migrate only a specific file"
    )
    
    args = parser.parse_args()
    
    migrator = ImportMigrator(args.codebase)
    
    if args.file:
        # Migrate a specific file
        file_path = Path(args.file)
        if file_path.exists():
            print(f"Migrating specific file: {file_path}")
            migrator.migrate_file(file_path, dry_run=not args.apply)
        else:
            print(f"File not found: {file_path}")
            return
    else:
        # Migrate the entire codebase
        dry_run = not args.apply
        migrator.migrate_codebase(dry_run=dry_run)
    
    migrator.print_migration_report()
    
    if dry_run:
        print("\n💡 To apply the changes, run with --apply flag")
    else:
        print("\n✅ Migration completed!")

if __name__ == "__main__":
    main() 
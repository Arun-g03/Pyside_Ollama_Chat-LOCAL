#!/usr/bin/env python3
"""
Directory Tree Generator for PySide Ollama Chat Project

This script generates a markdown file with the complete directory tree structure
of the project, excluding specified directories like chat_env and documents.
"""

import os
import sys
from pathlib import Path
from typing import List, Set

class DirectoryTreeGenerator:
    """Generates a markdown file with the project directory tree structure."""
    
    def __init__(self, root_path: str = ".", output_file: str = "Reports/PROJECT_STRUCTURE.md"):
        self.root_path = Path(root_path)
        self.output_file = output_file
        
        # Directories to exclude
        self.exclude_dirs = {
            "chat_env",
            "__pycache__",
            ".git",
            ".vscode",
            "node_modules",
            ".pytest_cache",
            ".coverage",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store",
            "Thumbs.db"
        }
        
        # File extensions to exclude
        self.exclude_extensions = {
            ".pyc", ".pyo", ".pyd", ".so", ".dll", ".dylib",
            ".log", ".tmp", ".temp", ".cache", ".bak", ".swp"
        }
        
        # Files to exclude
        self.exclude_files = {
            ".DS_Store", "Thumbs.db", ".gitignore", ".gitattributes",
            "*.log", "*.tmp", "*.temp", "*.cache", "*.bak", "*.swp"
        }
    
    def should_exclude_path(self, path: Path) -> bool:
        """Check if a path should be excluded from the tree."""
        path_str = str(path)
        
        # Check for excluded directories
        for exclude_dir in self.exclude_dirs:
            if exclude_dir in path_str:
                return True
        
        # Check for excluded file extensions
        if path.is_file():
            if path.suffix.lower() in self.exclude_extensions:
                return True
            
            # Check for excluded files
            for exclude_file in self.exclude_files:
                if path.name == exclude_file or path.name.endswith(exclude_file[1:]):
                    return True
        
        return False
    
    def get_file_size(self, file_path: Path) -> str:
        """Get file size in human-readable format."""
        try:
            size = file_path.stat().st_size
            if size < 1024:
                return f"{size}B"
            elif size < 1024 * 1024:
                return f"{size // 1024}KB"
            else:
                return f"{size // (1024 * 1024)}MB"
        except:
            return "0B"
    
    def generate_tree(self, path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
        """Generate the tree structure recursively."""
        lines = []
        
        if self.should_exclude_path(path):
            return lines
        
        # Get the display name
        if path == self.root_path:
            display_name = path.name or "."
        else:
            display_name = path.name
        
        # Add file size for files
        if path.is_file():
            size = self.get_file_size(path)
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{display_name} ({size})")
        else:
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{display_name}/")
        
        # Process children
        if path.is_dir():
            children = sorted([
                child for child in path.iterdir() 
                if not self.should_exclude_path(child)
            ])
            
            for i, child in enumerate(children):
                is_last_child = i == len(children) - 1
                child_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(self.generate_tree(child, child_prefix, is_last_child))
        
        return lines
    
    def generate_markdown(self) -> str:
        """Generate the complete markdown content."""
        markdown_content = []
        
        # Header
        markdown_content.extend([
            "# 📁 Project Directory Structure",
            "",
            f"**Generated:** {self._get_current_date()}",
            f"**Project:** {self.root_path.name or 'PySide Ollama Chat'}",
            f"**Root Path:** `{self.root_path.absolute()}`",
            "",
            "## 📋 Overview",
            "",
            "This document shows the complete directory structure of the PySide Ollama Chat project.",
            "Excluded directories and files are not shown to keep the structure clean and focused.",
            "",
            "### 🔍 Excluded Items",
            "",
            "The following items are excluded from this tree:",
            "",
            "**Directories:**",
            "- `chat_env/` - Virtual environment",
            "- `documents/` - Documentation files",
            "- `__pycache__/` - Python cache",
            "- `.git/` - Git repository",
            "- `.vscode/` - VS Code settings",
            "",
            "**Files:**",
            "- `*.pyc`, `*.pyo`, `*.pyd` - Python compiled files",
            "- `*.log`, `*.tmp`, `*.cache` - Temporary files",
            "- `.DS_Store`, `Thumbs.db` - System files",
            "",
            "## 🌳 Directory Tree",
            "",
            "```"
        ])
        
        # Generate tree structure
        tree_lines = self.generate_tree(self.root_path)
        markdown_content.extend(tree_lines)
        
        # Close code block
        markdown_content.extend([
            "```",
            "",
            "## 📊 Statistics",
            ""
        ])
        
        # Add statistics
        stats = self._calculate_statistics()
        markdown_content.extend([
            f"- **Total Files:** {stats['files']}",
            f"- **Total Directories:** {stats['directories']}",
            f"- **Total Size:** {stats['total_size']}",
            f"- **Python Files:** {stats['python_files']}",
            f"- **Markdown Files:** {stats['markdown_files']}",
            f"- **JSON Files:** {stats['json_files']}",
            "",
            "## 📝 File Types",
            ""
        ])
        
        # Add file type breakdown
        for ext, count in stats['file_types'].items():
            if count > 0:
                markdown_content.append(f"- **{ext}:** {count} files")
        
        markdown_content.extend([
            "",
            "## 🔧 Usage",
            "",
            "This structure was generated using the `generate_directory_tree.py` script.",
            "To regenerate this file, run:",
            "",
            "```bash",
            "python generate_directory_tree.py",
            "```",
            "",
            "## 📋 Notes",
            "",
            "- Directories are marked with `/`",
            "- File sizes are shown in parentheses",
            "- The tree is sorted alphabetically",
            "- Hidden files and system files are excluded",
            "",
            "---",
            "",
            "*Generated automatically by Directory Tree Generator*"
        ])
        
        return "\n".join(markdown_content)
    
    def _calculate_statistics(self) -> dict:
        """Calculate project statistics."""
        stats = {
            'files': 0,
            'directories': 0,
            'total_size': 0,
            'python_files': 0,
            'markdown_files': 0,
            'json_files': 0,
            'file_types': {}
        }
        
        for root, dirs, files in os.walk(self.root_path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude_path(Path(root) / d)]
            
            # Count directories
            stats['directories'] += len(dirs)
            
            # Process files
            for file in files:
                file_path = Path(root) / file
                if not self.should_exclude_path(file_path):
                    stats['files'] += 1
                    
                    # Get file size
                    try:
                        size = file_path.stat().st_size
                        stats['total_size'] += size
                    except:
                        pass
                    
                    # Count by extension
                    ext = file_path.suffix.lower()
                    if ext not in stats['file_types']:
                        stats['file_types'][ext] = 0
                    stats['file_types'][ext] += 1
                    
                    # Count specific file types
                    if ext == '.py':
                        stats['python_files'] += 1
                    elif ext == '.md':
                        stats['markdown_files'] += 1
                    elif ext == '.json':
                        stats['json_files'] += 1
        
        # Format total size
        total_size = stats['total_size']
        if total_size < 1024:
            stats['total_size'] = f"{total_size}B"
        elif total_size < 1024 * 1024:
            stats['total_size'] = f"{total_size // 1024}KB"
        else:
            stats['total_size'] = f"{total_size // (1024 * 1024)}MB"
        
        return stats
    
    def _get_current_date(self) -> str:
        """Get current date in a readable format."""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    def generate_file(self) -> bool:
        """Generate the markdown file."""
        try:
            print(f"🌳 Generating directory tree for: {self.root_path}")
            print(f"📄 Output file: {self.output_file}")
            print("⏳ Processing...")
            
            # Generate markdown content
            markdown_content = self.generate_markdown()
            
            # Write to file
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✅ Successfully generated: {self.output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating directory tree: {e}")
            return False


def main():
    """Main function to run the directory tree generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate directory tree markdown file")
    parser.add_argument(
        "--root", 
        default=".", 
        help="Root directory to scan (default: current directory)"
    )
    parser.add_argument(
        "--output", 
        default="PROJECT_STRUCTURE.md", 
        help="Output markdown file name (default: PROJECT_STRUCTURE.md)"
    )
    
    args = parser.parse_args()
    
    # Create generator and run
    generator = DirectoryTreeGenerator(args.root, args.output)
    success = generator.generate_file()
    
    if success:
        print("\n🎉 Directory tree generation completed successfully!")
        print(f"📁 Check the generated file: {args.output}")
    else:
        print("\n💥 Directory tree generation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 
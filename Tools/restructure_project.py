#!/usr/bin/env python3
"""
Project Restructuring Script

This script creates a new pyside_chat_refactored directory with the improved
project structure by copying files from the existing pyside_chat structure.
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json

class ProjectRestructurer:
    """Restructures the project into the new organized layout."""
    
    def __init__(self, source_dir: str = "pyside_chat", target_dir: str = "pyside_chat_refactored"):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        

        
        # Define the new structure mapping
        self.structure_mapping = {
            # App-level files
            "app": {
                "main.py": "MainApp/ollama_chat.py",
                "app_lifecycle.py": "MainApp/app_lifecycle.py",
                "event_bus.py": "MainApp/event_handler.py",
                "service_manager.py": "MainApp/service_manager.py"
            },
            
            # Config files
            "config": {
                "__init__.py": "config/__init__.py",
                "config_manager.py": "config/config_manager.py"
            },
            
            # Core models
            "core/models": {
                "base_model.py": "models/__init__.py",  # Will need to be created
                "conversation_metadata.py": "models/conversation_metadata.py"
            },
            
            # Core utils
            "core/utils": {
                "error_handler.py": "utils/error_handler.py",
                "internet_checker.py": "utils/internet_connection.py",
                "prompts.py": "utils/prompts.py",
                "streaming_handler.py": "utils/streaming_handler.py"
            },
            
            # Core logging
            "core/logging": {
                "logger.py": "utils/Logging/Custom_Logger.py",
                "helpers.py": "utils/Logging/logging_helpers.py"
            },
            
            # Chat feature
            "features/chat": {
                "chat_controller.py": "controllers/chat_controller.py"
            },
            
            "features/chat/enhancers": {
                "enhancement_service.py": "services/enhancement_service.py"
            },
            
            "features/chat/summarization": {
                "summarization_service.py": "services/summarization_service.py"
            },
            
            # Memory feature
            "features/memory": {
                "memory_service.py": "services/memory_service.py",
                "semantic_search.py": "services/semantic_search_service.py"
            },
            
            # Voice feature
            "features/voice/tts": {
                "tts_service.py": "services/Voice_STT_TTS_SERVICES/TTS_Service.py",
                "coqui_tts.py": "services/Voice_STT_TTS_SERVICES/coqui_tts_service.py"
            },
            
            "features/voice/stt": {
                "stt_service.py": "services/Voice_STT_TTS_SERVICES/STT_Service.py"
            },
            
            "features/voice/audio": {
                "recording_service.py": "services/Voice_STT_TTS_SERVICES/Recording_Service.py"
            },
            
            "features/voice/orchestrator": {
                "voice_process_manager.py": "services/Voice_STT_TTS_SERVICES/voice_process_manager.py"
            },
            
            # Personality feature
            "features/personality": {
                "loader.py": "Personalities/services/personality_loader.py",
                "formatter.py": "Personalities/utils/personality_formatter.py"
            },
            
            "features/personality/services": {
                "personality_service.py": "Personalities/services/personality_service.py"
            },
            
            "features/personality/models": {
                "personality_types.py": "Personalities/models/personality_types.py",
                "personality_pronouns.py": "Personalities/models/personality_pronouns.py",
                "personality_model.py": "Personalities/personality_model.py"
            },
            
            "features/personality/profiles": {
                # Copy entire personality_Profiles directory
                "": "Personalities/personality_Profiles/"
            },
            
            # Ollama feature
            "features/ollama": {
                "ollama_service.py": "services/ollama_service.py"
            },
            
            # User feature (placeholder)
            "features/user": {
                "user_profile_service.py": "services/conversation_service.py"  # Temporary mapping
            },
            
            # UI main window
            "ui": {
                "main_window.py": "MainApp/ollama_chat.py"  # Will need to be adapted
            },
            
            # UI themes
            "ui/themes": {
                "styles.py": "ui/styles/styles.py"
            },
            
            # UI widgets
            "ui/widgets": {
                "message_editor.py": "ui/Widgets/editable_message_widget.py",
                "spellchecker_widget.py": "ui/Widgets/spellchecker_widget.py",
                "chat_navigation.py": "ui/Widgets/chat_navigation.py"
            },
            
            # UI dialogs
            "ui/dialogs": {
                "settings_dialog.py": "ui/Widgets/settings_dialog.py",
                "coqui_model_dialog.py": "ui/Widgets/coqui_model_dialog.py",
                "voice_settings_dialog.py": "ui/Widgets/voice_settings_dialog.py"
            },
            
            # UI tabs
            "ui/tabs/chat_tab": {
                "chat_tab.py": "ui/tabs/chat_tab/chat_tab.py",
                "input_controls.py": "ui/tabs/chat_tab/input_controls.py",
                "voice_controls.py": "ui/tabs/chat_tab/voice_controls.py",
                "eq_visualizer.py": "ui/tabs/chat_tab/eq_visualizer.py",
                "chat_display.py": "ui/tabs/chat_tab/chat_display.py"
            },
            
            "ui/tabs": {
                "memory_tab.py": "ui/tabs/memory_tab.py",
                "model_tab.py": "ui/tabs/model_tab.py",
                "personality_tab.py": "ui/tabs/personality_tab.py"
            },
            
            # UI visualizers
            "ui/visualizers": {
                "eq_orchestrator.py": "ui/Audio_visualisers/eq_orchestrator.py"
            },
            
            "ui/visualizers/widgets": {
                "bar_eq_widget.py": "ui/Audio_visualisers/eq_widgets/bar_eq_widget.py",
                "circle_eq_widget.py": "ui/Audio_visualisers/eq_widgets/circle_eq_widget.py",
                "circular_gradient_eq_widget.py": "ui/Audio_visualisers/eq_widgets/circular_gradient_eq_widget.py",
                "circular_net_eq_widget.py": "ui/Audio_visualisers/eq_widgets/circular_net_eq_widget.py"
            },
            
            # Workers
            "workers": {
                "worker.py": "services/worker/worker.py"
            },
            
            # Startup
            "startup": {
                "install_dependencies.py": "services/start_up/install_dependencies.py",
                "dependency_checker.py": "services/start_up/dependency_checker.py"
            }
        }
    
    def create_directory_structure(self):
        """Create the new directory structure."""
        print("�� Creating directory structure...")
        
        # Create all directories
        for dir_path in self.structure_mapping.keys():
            full_path = self.target_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {dir_path}")
    
    def copy_files(self):
        """Copy files according to the mapping."""
        print("\n📋 Copying files...")
        
        copied_files = []
        missing_files = []
        
        for target_dir, file_mapping in self.structure_mapping.items():
            target_path = self.target_dir / target_dir
            
            for target_file, source_file in file_mapping.items():
                source_path = self.source_dir / source_file
                target_file_path = target_path / target_file
                
                if source_path.exists():
                    try:
                        # Handle directory copying (for personality profiles)
                        if target_file == "" and source_path.is_dir():
                            # Copy entire directory
                            if target_file_path.exists():
                                shutil.rmtree(target_file_path)
                            shutil.copytree(source_path, target_file_path)
                            print(f"  ✅ Copied directory: {source_file} -> {target_dir}/")
                            copied_files.append(f"{source_file} -> {target_dir}/")
                        else:
                            # Copy single file
                            shutil.copy2(source_path, target_file_path)
                            print(f"  ✅ Copied: {source_file} -> {target_dir}/{target_file}")
                            copied_files.append(f"{source_file} -> {target_dir}/{target_file}")
                    except PermissionError as e:
                        print(f"  ⚠️ Permission error copying {source_file}: {e}")
                        missing_files.append(source_file)
                    except Exception as e:
                        print(f"  ❌ Error copying {source_file}: {e}")
                        missing_files.append(source_file)
                else:
                    print(f"  ❌ Missing: {source_file}")
                    missing_files.append(source_file)
        
        return copied_files, missing_files
    
    def create_init_files(self):
        """Create __init__.py files in all directories."""
        print("\n�� Creating __init__.py files...")
        
        for root, dirs, files in os.walk(self.target_dir):
            root_path = Path(root)
            init_file = root_path / "__init__.py"
            
            if not init_file.exists():
                init_file.touch()
                print(f"  ✅ Created: {init_file.relative_to(self.target_dir)}")
    
    def create_placeholder_files(self):
        """Create placeholder files for missing components."""
        print("\n🔧 Creating placeholder files...")
        
        placeholders = {
            "core/models/base_model.py": '''"""
Base model for all data models in the application.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModel(ABC):
    """Base class for all models in the application."""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create model from dictionary."""
        pass
''',
            
            "features/user/user_profile_service.py": '''"""
User profile service for managing user data and preferences.
"""

from typing import Dict, Any, Optional

class UserProfileService:
    """Service for managing user profiles and preferences."""
    
    def __init__(self):
        self.user_data = {}
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by ID."""
        return self.user_data.get(user_id)
    
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Update user profile."""
        self.user_data[user_id] = profile_data
        return True
''',
            
            "ui/main_window.py": '''"""
Main window component for the application.
This is a placeholder that will be adapted from the current main window.
"""

from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide Ollama Chat - Refactored")
        # TODO: Adapt from current main window implementation
'''
        }
        
        for file_path, content in placeholders.items():
            full_path = self.target_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Created placeholder: {file_path}")
    
    def create_readme(self):
        """Create a README for the refactored structure."""
        readme_content = '''# PySide Chat - Refactored Structure

This directory contains the refactored version of the PySide Chat application with an improved project structure.

## �� Structure Overview

### `app/`
Application-level components including lifecycle management and service coordination.

### `config/`
Configuration management and settings.

### `core/`
Core abstractions, models, and utilities shared across the application.

### `features/`
Domain-oriented feature modules:
- **chat/**: Chat functionality and controllers
- **memory/**: Memory management and semantic search
- **voice/**: Voice processing (TTS, STT, audio)
- **personality/**: AI personality system
- **ollama/**: Ollama AI integration
- **user/**: User profile management

### `ui/`
User interface components:
- **main_window.py**: Main application window
- **themes/**: Styling and theming
- **widgets/**: Reusable UI components
- **dialogs/**: Modal dialogs and settings
- **tabs/**: Tab-based interface components
- **visualizers/**: Audio visualization components

### `workers/`
Background processing and worker threads.

### `startup/`
Application startup, dependency management, and installation utilities.

## �� Migration Status

This is a **work in progress**. Some files may need adaptation to work with the new structure.

### Next Steps:
1. Update import statements to match new structure
2. Adapt main window to new architecture
3. Update service dependencies
4. Test all functionality
5. Remove old structure

## 🚀 Usage

To use the refactored version:

```bash
# Update main.py to import from new structure
python main.py
```

## �� Notes

- All files have been copied from the original structure
- Some files may need manual adaptation
- Import statements will need updating
- The new structure follows domain-driven design principles
'''
        
        readme_path = self.target_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"  ✅ Created README: {readme_path}")
    
    def generate_migration_report(self, copied_files: List[str], missing_files: List[str]):
        """Generate a migration report."""
        report_content = f'''# Migration Report

**Generated:** {self._get_current_date()}
**Source:** {self.source_dir}
**Target:** {self.target_dir}

## �� Summary

- **Total Files Copied:** {len(copied_files)}
- **Missing Files:** {len(missing_files)}
- **Success Rate:** {(len(copied_files) / (len(copied_files) + len(missing_files))) * 100:.1f}%

## ✅ Successfully Copied Files

'''
        
        for file in copied_files:
            report_content += f"- {file}\n"
        
        if missing_files:
            report_content += f"\n## ❌ Missing Files\n\n"
            for file in missing_files:
                report_content += f"- {file}\n"
        
        report_content += f'''

## 🔧 Next Steps

1. **Update Import Statements**
   - All import statements need to be updated to match the new structure
   - Use relative imports where appropriate

2. **Adapt Main Window**
   - The main window needs to be adapted to the new architecture
   - Update service initialization

3. **Test Functionality**
   - Test all features to ensure they work with the new structure
   - Fix any import or dependency issues

4. **Clean Up**
   - Remove the old structure once everything is working
   - Update documentation

## 📝 Notes

- The new structure follows domain-driven design principles
- Each feature is self-contained with its own models, services, and utilities
- The UI layer is separated from business logic
- Core abstractions are shared across features
'''
        
        report_path = self.target_dir / "MIGRATION_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"  ✅ Created migration report: {report_path}")
    
    def _get_current_date(self) -> str:
        """Get current date in a readable format."""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    def restructure(self) -> bool:
        """Perform the complete restructuring."""
        try:
            print("🚀 Starting project restructuring...")
            print(f"📂 Source: {self.source_dir}")
            print(f"📂 Target: {self.target_dir}")
            print()
            
            # Check if source exists
            if not self.source_dir.exists():
                print(f"❌ Error: Source directory '{self.source_dir}' does not exist!")
                return False
            
            # Create target directory
            self.target_dir.mkdir(exist_ok=True)
            
            # Perform restructuring
            self.create_directory_structure()
            copied_files, missing_files = self.copy_files()
            self.create_init_files()
            self.create_placeholder_files()
            self.create_readme()
            self.generate_migration_report(copied_files, missing_files)
            
            print(f"\n🎉 Restructuring completed successfully!")
            print(f"📁 New structure created in: {self.target_dir}")
            print(f"�� Check MIGRATION_REPORT.md for details")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during restructuring: {e}")
            return False


def main():
    """Main function to run the restructuring."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Restructure PySide Chat project")
    parser.add_argument(
        "--source", 
        default="pyside_chat", 
        help="Source directory (default: pyside_chat)"
    )
    parser.add_argument(
        "--target", 
        default="pyside_chat_refactored", 
        help="Target directory (default: pyside_chat_refactored)"
    )
    
    args = parser.parse_args()
    
    # Create restructurer and run
    restructurer = ProjectRestructurer(args.source, args.target)
    success = restructurer.restructure()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
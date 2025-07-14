# Codebase Refactoring Analysis Report

**Generated:** 2025-07-13T22:08:23.571647

## Executive Summary

- **Total Files:** 135
- **Total Lines:** 40,552
- **Total Size:** 1684.3 KB
- **Files Needing Refactoring:** 94
- **Directories Needing Refactoring:** 34

## 🔴 High Priority Files

These files need immediate refactoring attention:

- `Development_Tools\Analyzers\advanced_codebase_analyzer.py`
- `Development_Tools\Analyzers\import_scanner.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py`
- `pyside_chat\app\app_lifecycle.py`
- `pyside_chat\app\event_bus.py`
- `pyside_chat\app\service_manager.py`
- `pyside_chat\config\config_manager.py`
- `pyside_chat\core\logging\helpers.py`
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\core\models\conversation_metadata.py`
- `pyside_chat\core\threading\qrunnable_tasks.py`
- `pyside_chat\core\threading\qthread_workers.py`
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\thread_monitor.py`
- `pyside_chat\core\threading\usage_examples.py`
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\core\utils\threading_utils.py`
- `pyside_chat\features\chat\chat_controller.py`
- `pyside_chat\features\chat\complexity_analyser\complexity_analyzer.py`
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\ollama\ollama_service.py`
- `pyside_chat\features\personality\services\personality_service.py`
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`
- `pyside_chat\ui\dialogs\coqui_model_dialog.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`
- `pyside_chat\ui\tabs\memory_tab.py`
- `pyside_chat\ui\tabs\personality_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\eq_visualizer.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`
- `pyside_chat\ui\visualizers\eq_orchestrator.py`

## 🟡 Medium Priority Files

These files need refactoring but are not urgent:

- `main.py`
- `Development_Tools\Analyzers\advanced_codebase_analyzer.py`
- `Development_Tools\Analyzers\import_scanner.py`
- `Development_Tools\Analyzers\program_flow_tracer.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`
- `Development_Tools\Legacy\LOGGER_ID_Creator.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py`
- `Development_Tools\Utilities\generate_directory_tree.py`
- `PACKAGING_the_app\package_app.py`
- `pyside_chat\app\app_lifecycle.py`
- `pyside_chat\app\main.py`
- `pyside_chat\app\threading_integration.py`
- `pyside_chat\config\config_manager.py`
- `pyside_chat\core\logging\helpers.py`
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\core\models\conversation_metadata.py`
- `pyside_chat\core\threading\persistent_thread_pool.py`
- `pyside_chat\core\threading\qrunnable_tasks.py`
- `pyside_chat\core\threading\qthread_workers.py`
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\thread_calculator.py`
- `pyside_chat\core\threading\thread_monitor.py`
- `pyside_chat\core\threading\thread_pool_manager.py`
- `pyside_chat\core\threading\usage_examples.py`
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\internet_checker.py`
- `pyside_chat\core\utils\prompts.py`
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\core\utils\threading_audit.py`
- `pyside_chat\core\utils\threading_utils.py`
- `pyside_chat\features\chat\chat_controller.py`
- `pyside_chat\features\chat\conversation_service.py`
- `pyside_chat\features\chat\summarization\summarization_service.py`
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`
- `pyside_chat\features\ollama\ollama_chat.py`
- `pyside_chat\features\ollama\ollama_service.py`
- `pyside_chat\features\personality\formatter.py`
- `pyside_chat\features\personality\loader.py`
- `pyside_chat\features\personality\models\personality_model.py`
- `pyside_chat\features\personality\models\personality_pronouns.py`
- `pyside_chat\features\personality\services\personality_service.py`
- `pyside_chat\features\voice\voice_service_manager.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\streaming_audio_player.py`
- `pyside_chat\features\voice\tts\streaming_audio_worker.py`
- `pyside_chat\features\voice\tts\tts_service.py`
- `pyside_chat\startup\dependency_checker.py`
- `pyside_chat\ui\ui_manager.py`
- `pyside_chat\ui\dialogs\coqui_model_dialog.py`
- `pyside_chat\ui\dialogs\error_dialog.py`
- `pyside_chat\ui\dialogs\settings_dialog.py`
- `pyside_chat\ui\tabs\memory_tab.py`
- `pyside_chat\ui\tabs\model_tab.py`
- `pyside_chat\ui\tabs\personality_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`
- `pyside_chat\ui\tabs\chat_tab\eq_visualizer.py`
- `pyside_chat\ui\themes\message_formatter.py`
- `pyside_chat\ui\visualizers\eq_orchestrator.py`
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py`
- `pyside_chat\ui\Widgets\chat_navigation.py`
- `pyside_chat\ui\Widgets\complexity_widget.py`
- `pyside_chat\ui\Widgets\message_editor.py`
- `pyside_chat\ui\Widgets\spellchecker_widget.py`

## 🟢 Low Priority Files

These files could benefit from minor improvements:

- `main.py`
- `test_typewriter_fix.py`
- `Development_Tools\Analyzers\advanced_codebase_analyzer.py`
- `Development_Tools\Analyzers\import_scanner.py`
- `Development_Tools\Analyzers\logs Parser_error_detector.py`
- `Development_Tools\Analyzers\program_flow_graph.py`
- `Development_Tools\Analyzers\program_flow_tracer.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`
- `Development_Tools\Legacy\LOGGER_ID_Creator.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\unified_profiler.py`
- `Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py`
- `Development_Tools\Utilities\generate_directory_tree.py`
- `Development_Tools\Utilities\run_analyzer.py`
- `PACKAGING_the_app\package_app.py`
- `pyside_chat\app\app_lifecycle.py`
- `pyside_chat\app\event_bus.py`
- `pyside_chat\app\main.py`
- `pyside_chat\app\service_manager.py`
- `pyside_chat\app\threading_integration.py`
- `pyside_chat\config\config_manager.py`
- `pyside_chat\core\logging\helpers.py`
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\core\models\conversation_metadata.py`
- `pyside_chat\core\threading\persistent_thread_config.py`
- `pyside_chat\core\threading\persistent_thread_pool.py`
- `pyside_chat\core\threading\qrunnable_tasks.py`
- `pyside_chat\core\threading\qthread_workers.py`
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\thread_calculator.py`
- `pyside_chat\core\threading\thread_calculator_examples.py`
- `pyside_chat\core\threading\thread_monitor.py`
- `pyside_chat\core\threading\thread_pool_manager.py`
- `pyside_chat\core\threading\usage_examples.py`
- `pyside_chat\core\threading\__init__.py`
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\internet_checker.py`
- `pyside_chat\core\utils\prompts.py`
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\core\utils\threading_audit.py`
- `pyside_chat\core\utils\threading_utils.py`
- `pyside_chat\features\chat\chat_controller.py`
- `pyside_chat\features\chat\conversation_service.py`
- `pyside_chat\features\chat\complexity_analyser\complexity_analyzer.py`
- `pyside_chat\features\chat\summarization\summarization_service.py`
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`
- `pyside_chat\features\ollama\ollama_chat.py`
- `pyside_chat\features\ollama\ollama_service.py`
- `pyside_chat\features\personality\formatter.py`
- `pyside_chat\features\personality\loader.py`
- `pyside_chat\features\personality\models\personality_model.py`
- `pyside_chat\features\personality\models\personality_pronouns.py`
- `pyside_chat\features\personality\models\personality_types.py`
- `pyside_chat\features\personality\services\personality_service.py`
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_manager.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\streaming_audio_player.py`
- `pyside_chat\features\voice\tts\streaming_audio_worker.py`
- `pyside_chat\features\voice\tts\tts_service.py`
- `pyside_chat\startup\dependency_checker.py`
- `pyside_chat\startup\system_installer.py`
- `pyside_chat\ui\ui_manager.py`
- `pyside_chat\ui\dialogs\coqui_model_dialog.py`
- `pyside_chat\ui\dialogs\error_dialog.py`
- `pyside_chat\ui\dialogs\settings_dialog.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`
- `pyside_chat\ui\tabs\memory_tab.py`
- `pyside_chat\ui\tabs\model_tab.py`
- `pyside_chat\ui\tabs\personality_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\eq_visualizer.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`
- `pyside_chat\ui\themes\message_formatter.py`
- `pyside_chat\ui\themes\styles.py`
- `pyside_chat\ui\utils\message_utils.py`
- `pyside_chat\ui\visualizers\eq_orchestrator.py`
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py`
- `pyside_chat\ui\Widgets\chat_navigation.py`
- `pyside_chat\ui\Widgets\complexity_widget.py`
- `pyside_chat\ui\Widgets\message_editor.py`
- `pyside_chat\ui\Widgets\spellchecker_widget.py`

## 🔄 Duplicate Functions

These functions appear in multiple files and could be consolidated:

### `def __init__(self)`
**Found in:** 26 files
**Files:**
- `test_typewriter_fix.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py`
- `Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py`
- `PACKAGING_the_app\package_app.py`
- `pyside_chat\app\main.py`
- `pyside_chat\core\logging\helpers.py`
- `pyside_chat\core\threading\thread_calculator.py`
- `pyside_chat\core\threading\usage_examples.py`
- `pyside_chat\core\utils\threading_audit.py`
- `pyside_chat\features\chat\complexity_analyser\complexity_analyzer.py`
- `pyside_chat\features\ollama\ollama_chat.py`
- `pyside_chat\features\user\user_profile_service.py`
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_manager.py`
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`
- `pyside_chat\startup\dependency_checker.py`
- `pyside_chat\ui\visualizers\eq_orchestrator.py`

### `def main()`
**Found in:** 16 files
**Files:**
- `check_critical_issues.py`
- `main.py`
- `test_typewriter_fix.py`
- `Development_Tools\Analyzers\advanced_codebase_analyzer.py`
- `Development_Tools\Analyzers\import_scanner.py`
- `Development_Tools\Analyzers\logs Parser_error_detector.py`
- `Development_Tools\Analyzers\program_flow_graph.py`
- `Development_Tools\Analyzers\program_flow_tracer.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`
- `Development_Tools\Profiler\unified_profiler.py`
- `Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py`
- `Development_Tools\Utilities\generate_directory_tree.py`
- `Development_Tools\Utilities\run_analyzer.py`
- `PACKAGING_the_app\package_app.py`
- `pyside_chat\core\threading\thread_calculator_examples.py`
- `pyside_chat\startup\install_dependencies.py`

### `def cleanup(self)`
**Found in:** 15 files
**Files:**
- `PACKAGING_the_app\package_app.py`
- `pyside_chat\app\service_manager.py`
- `pyside_chat\core\logging\helpers.py`
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\usage_examples.py`
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\features\ollama\ollama_service.py`
- `pyside_chat\features\voice\voice_service_manager.py`
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\streaming_audio_player.py`
- `pyside_chat\features\voice\tts\tts_service.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`
- `pyside_chat\ui\Widgets\spellchecker_widget.py`

### `def __init__(self,parent)`
**Found in:** 12 files
**Files:**
- `pyside_chat\core\threading\persistent_thread_pool.py`
- `pyside_chat\core\threading\qthread_workers.py`
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\thread_monitor.py`
- `pyside_chat\ui\dialogs\coqui_model_dialog.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`
- `pyside_chat\ui\tabs\model_tab.py`
- `pyside_chat\ui\tabs\personality_tab.py`
- `pyside_chat\ui\tabs\chat_tab\eq_visualizer.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`
- `pyside_chat\ui\Widgets\complexity_widget.py`
- `pyside_chat\ui\Widgets\spellchecker_widget.py`

### `def run(self)`
**Found in:** 10 files
**Files:**
- `pyside_chat\core\threading\qrunnable_tasks.py`
- `pyside_chat\core\threading\qrunnable_tasks.py`
- `pyside_chat\core\threading\qrunnable_tasks.py`
- `pyside_chat\core\threading\qrunnable_tasks.py`
- `pyside_chat\core\threading\qrunnable_tasks.py`
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py`
- `pyside_chat\features\voice\tts\streaming_audio_player.py`
- `pyside_chat\features\voice\tts\streaming_audio_worker.py`
- `pyside_chat\ui\dialogs\coqui_model_dialog.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`

### `def setup_ui(self)`
**Found in:** 10 files
**Files:**
- `pyside_chat\ui\dialogs\coqui_model_dialog.py`
- `pyside_chat\ui\dialogs\settings_dialog.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`
- `pyside_chat\ui\tabs\memory_tab.py`
- `pyside_chat\ui\tabs\model_tab.py`
- `pyside_chat\ui\tabs\personality_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\Widgets\chat_navigation.py`
- `pyside_chat\ui\Widgets\complexity_widget.py`
- `pyside_chat\ui\Widgets\message_editor.py`

### `def setup_connections(self)`
**Found in:** 8 files
**Files:**
- `pyside_chat\app\event_bus.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`
- `pyside_chat\ui\tabs\memory_tab.py`
- `pyside_chat\ui\tabs\model_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`
- `pyside_chat\ui\Widgets\chat_navigation.py`

### `def stop(self)`
**Found in:** 7 files
**Files:**
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `pyside_chat\core\threading\qthread_workers.py`
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py`
- `pyside_chat\features\voice\tts\streaming_audio_worker.py`

### `def wrapper()`
**Found in:** 7 files
**Files:**
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\error_handler.py`
- `pyside_chat\core\utils\threading_utils.py`

### `def stop_chat_streaming(self)`
**Found in:** 5 files
**Files:**
- `pyside_chat\app\event_bus.py`
- `pyside_chat\app\threading_integration.py`
- `pyside_chat\app\threading_integration.py`
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\usage_examples.py`

### `def get_threading_status(self) -> Dict[str, Any]`
**Found in:** 5 files
**Files:**
- `pyside_chat\app\event_bus.py`
- `pyside_chat\app\threading_integration.py`
- `pyside_chat\app\threading_integration.py`
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\usage_examples.py`

### `def get_data(self)`
**Found in:** 4 files
**Files:**
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`

### `def __new__(cls)`
**Found in:** 4 files
**Files:**
- `pyside_chat\app\service_manager.py`
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\features\voice\voice_service_manager.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`

### `def start_streaming(self)`
**Found in:** 4 files
**Files:**
- `pyside_chat\core\threading\qthread_workers.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def get_messages(self) -> List[Dict]`
**Found in:** 4 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\features\chat\conversation_service.py`
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def get_ai_name(self) -> str`
**Found in:** 4 files
**Files:**
- `pyside_chat\features\chat\chat_controller.py`
- `pyside_chat\features\personality\services\personality_service.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`

### `def __del__(self)`
**Found in:** 4 files
**Files:**
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\streaming_audio_player.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def is_available(self) -> bool`
**Found in:** 4 files
**Files:**
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def is_initialized(self) -> bool`
**Found in:** 4 files
**Files:**
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def safe_disconnect(signal,slot,logger)`
**Found in:** 4 files
**Files:**
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\ui\tabs\memory_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def _animate(self)`
**Found in:** 4 files
**Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py`

### `def set_idle(self)`
**Found in:** 4 files
**Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py`

### `def start_animation(self)`
**Found in:** 4 files
**Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py`

### `def stop_animation(self)`
**Found in:** 4 files
**Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py`

### `def paintEvent(self,event)`
**Found in:** 4 files
**Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py`

### `def __init__(self,root_path)`
**Found in:** 3 files
**Files:**
- `Development_Tools\Analyzers\advanced_codebase_analyzer.py`
- `Development_Tools\Analyzers\import_scanner.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`

### `def start(self)`
**Found in:** 3 files
**Files:**
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`

### `def _monitor_loop(self)`
**Found in:** 3 files
**Files:**
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`

### `def show_ollama_connection_error(self,context,force_show)`
**Found in:** 3 files
**Files:**
- `pyside_chat\app\app_lifecycle.py`
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def check_ollama_connection(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\app\app_lifecycle.py`
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def _on_tts_finished(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\app\event_bus.py`
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def cleanup_on_exit(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\app\event_bus.py`
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def __post_init__(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\core\models\conversation_metadata.py`
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\personality\models\personality_types.py`

### `def shutdown(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\core\threading\persistent_thread_pool.py`
- `pyside_chat\core\threading\thread_monitor.py`
- `pyside_chat\core\threading\thread_pool_manager.py`

### `def test_connection(self) -> bool`
**Found in:** 3 files
**Files:**
- `pyside_chat\core\utils\internet_checker.py`
- `pyside_chat\features\ollama\ollama_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def get_memory_stats(self) -> Dict`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`

### `def is_ready(self) -> bool`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`
- `pyside_chat\features\voice\voice_service_manager.py`

### `def __init__(self,personalities_dir)`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\personality\loader.py`
- `pyside_chat\features\personality\models\personality_model.py`
- `pyside_chat\features\personality\services\personality_service.py`

### `def get_temperature(self) -> float`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\personality\services\personality_service.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def get_instance()`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def speak_text(self,text)`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def update_settings(self,settings)`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_manager.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def get_current_audio_level(self) -> float`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\audio\recording_service.py`

### `def set_audio_gate_enabled(self,enabled)`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\audio\recording_service.py`

### `def _on_voice_service_ready(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\voice_service_manager.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def _check_availability(self) -> bool`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def stop_playback(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\tts\coqui_tts_service.py`
- `pyside_chat\features\voice\tts\streaming_audio_player.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def __init__(self,parent,config_manager)`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def update_model_list(self,models)`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\tabs\model_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def get_current_personality(self) -> str`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\tabs\personality_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def setup_ui_components(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def stop_streaming(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def clear_chat(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`

### `def get_ui_components(self) -> dict`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_render_completed(self)`
**Found in:** 2 files
**Files:**
- `test_typewriter_fix.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`

### `def generate_report(self) -> str`
**Found in:** 2 files
**Files:**
- `Development_Tools\Analyzers\import_scanner.py`
- `pyside_chat\core\utils\threading_audit.py`

### `def visit_Import(self,node)`
**Found in:** 2 files
**Files:**
- `Development_Tools\Analyzers\import_scanner.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`

### `def visit_ImportFrom(self,node)`
**Found in:** 2 files
**Files:**
- `Development_Tools\Analyzers\import_scanner.py`
- `Development_Tools\Analyzers\refactoring_analyzer.py`

### `def __init__(self,interval)`
**Found in:** 2 files
**Files:**
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`

### `def _collect(self)`
**Found in:** 2 files
**Files:**
- `Development_Tools\Profiler\profiler_helpers.py`
- `Development_Tools\Profiler\profiler_helpers.py`

### `def _stop_streaming_safe(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\event_bus.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`

### `def _setup_ui(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def _setup_connections(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\voice\voice_service.py`

### `def showEvent(self,event)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def closeEvent(self,event)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def get_service_manager(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def get_ui_manager(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def get_event_handler(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def get_lifecycle_manager(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def get_chat_controller(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\main.py`
- `pyside_chat\features\ollama\ollama_chat.py`

### `def _initialize_services(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\service_manager.py`
- `pyside_chat\features\voice\voice_service.py`

### `def get_voice_service(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\service_manager.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def _initialize_voice_service(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\service_manager.py`
- `pyside_chat\features\voice\voice_service_manager.py`

### `def __init__(self,event_handler)`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\threading_integration.py`
- `pyside_chat\app\threading_integration.py`

### `def start_chat_streaming(self,context_messages,chosen_model,temperature,config_manager) -> bool`
**Found in:** 2 files
**Files:**
- `pyside_chat\app\threading_integration.py`
- `pyside_chat\app\threading_integration.py`

### `def unregister_thread(self,thread_name)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\logging\helpers.py`
- `pyside_chat\core\threading\thread_monitor.py`

### `def _on_thread_started(self,thread_name)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\logging\helpers.py`
- `pyside_chat\core\threading\thread_monitor.py`

### `def _on_thread_finished(self,thread_name)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\logging\helpers.py`
- `pyside_chat\core\threading\thread_monitor.py`

### `def info(self,msg)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\core\logging\logger.py`

### `def debug(self,msg)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\core\logging\logger.py`

### `def warning(self,msg)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\core\logging\logger.py`

### `def error(self,msg)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\core\logging\logger.py`

### `def to_dict(self) -> Dict[str, Any]`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\models\base_model.py`
- `pyside_chat\core\models\conversation_metadata.py`

### `def get_pool_status(self) -> Dict[str, Any]`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\threading\persistent_thread_pool.py`
- `pyside_chat\core\threading\thread_pool_manager.py`

### `def shutdown_global_persistent_thread_pool()`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\threading\persistent_thread_pool.py`
- `pyside_chat\core\threading\__init__.py`

### `def _stream_operation(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\threading\qthread_workers.py`
- `pyside_chat\core\threading\qthread_workers.py`

### `def _on_chat_chunk_received(self,chunk)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\usage_examples.py`

### `def _on_chat_progress_updated(self,progress)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\usage_examples.py`

### `def _on_chat_streaming_finished(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\usage_examples.py`

### `def shutdown_global_threading_service()`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\threading\threading_service.py`
- `pyside_chat\core\threading\__init__.py`

### `def _get_next_message_id(self) -> str`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def append_message(self,sender,content,is_code,tag)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def edit_message(self,message_index,new_content) -> bool`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def _process_typewriter_chunk(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def update_streaming_message(self,content,sender,message_id,is_code,tag,append)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def finalize_streaming_message(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def update_last_system_switch(self,message)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def clear_messages(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

### `def safe_disconnect(signal,slot)`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\utils\threading_utils.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`

### `def __init__(self,ollama_service)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\chat\enhancers\enhancement_service.py`
- `pyside_chat\features\chat\summarization\summarization_service.py`

### `def _load(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\memory\memory_service.py`

### `def add_message(self,message)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\memory\memory_service.py`

### `def clear(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\memory\memory_service.py`

### `def _save(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\features\memory\memory_service.py`

### `def cleanup_memory_entries(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\memory_service.py`
- `pyside_chat\ui\tabs\memory_tab.py`

### `def add_memory(self,memory_id,content,memory_type,importance,tags,metadata) -> bool`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`

### `def remove_memory(self,memory_id) -> bool`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`

### `def search_semantic(self,query,max_results,min_similarity,memory_types) -> List[Tuple[str, float, Dict]]`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`

### `def search_hybrid(self,query,max_results,min_similarity,memory_types,keyword_weight,semantic_weight) -> List[Tuple[str, float, Dict]]`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`

### `def update_memory_importance(self,memory_id,new_importance) -> bool`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`

### `def clear_all(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\memory\semantic_search.py`
- `pyside_chat\features\memory\semantic_search_fallback.py`

### `def get_system_prompt(self) -> str`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\personality\services\personality_service.py`
- `pyside_chat\ui\tabs\personality_tab.py`

### `def get_selected_model(self) -> str`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\personality\services\personality_service.py`
- `pyside_chat\ui\tabs\model_tab.py`

### `def _on_recording_started(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def _on_recording_stopped(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def _on_recording_error(self,error)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def is_voice_available(self) -> bool`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def start_voice_input(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def stop_voice_input(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def _on_tts_started(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def _on_tts_error(self,error)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def stop_tts(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def set_continuous_voice_mode(self,enabled)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def is_continuous_voice_mode(self) -> bool`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def get_silence_duration(self) -> float`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def get_silence_threshold(self) -> float`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def get_recording_timeout(self) -> float`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def set_recording_timeout(self,timeout)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def set_silence_duration(self,duration)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def set_silence_threshold(self,threshold)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def get_audio_folder_path(self) -> str`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def list_audio_files(self) -> list`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def cleanup_old_audio_files(self,max_files,max_age_days)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def cleanup_all_audio_files(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\voice_service_wrapper.py`

### `def _reset_error_count(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def speak_text_streaming(self,text)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def speak_text_non_streaming(self,text)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def get_process_info(self) -> Dict[str, Any]`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service_wrapper.py`
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py`

### `def update_api(self,api_name)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def download_selected_model(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\dialogs\coqui_model_dialog.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`

### `def copy_error(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\dialogs\error_dialog.py`
- `pyside_chat\ui\dialogs\error_dialog.py`

### `def reset_copy_button(self,button)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\dialogs\error_dialog.py`
- `pyside_chat\ui\dialogs\error_dialog.py`

### `def setup_styles(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\dialogs\error_dialog.py`
- `pyside_chat\ui\Widgets\message_editor.py`

### `def create_general_tab(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\dialogs\settings_dialog.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`

### `def save_settings(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\dialogs\settings_dialog.py`
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`

### `def on_personality_changed(self,personality_name)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\personality_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`

### `def on_message_edited(self,message_index,new_content)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`

### `def append_to_chat(self,sender,message,is_code)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`

### `def append_response_chunk(self,chunk,model_name)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`

### `def get_streaming_handler(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`

### `def on_model_changed(self,model_name)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def on_user_interrupted(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_request_cancelled(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_voice_input_received(self,text)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_voice_input_error(self,error)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_tts_started(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_tts_finished(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_tts_error(self,error)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_recording_started(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_recording_stopped(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_recording_error(self,error)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_voice_processing_started(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_voice_processing_finished(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_audio_level_changed(self,audio_level)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def on_eq_bars_changed(self,bar_values)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def get_current_model(self) -> str`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def get_current_response(self) -> str`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def force_enable_send_button(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def update_personality_list(self,personalities)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\input_controls.py`

### `def speak_ai_response(self,text)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def _setup_animation_timer(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`

### `def get_current_values(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py`

### `def set_net_radii(self,values)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py`
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py`

### `def show_context_menu(self,position)`
**Found in:** 2 files
**Files:**
- `pyside_chat\ui\Widgets\chat_navigation.py`
- `pyside_chat\ui\Widgets\spellchecker_widget.py`

## 📋 Detailed File Analysis

### check_critical_issues.py

- **Size:** 0.7 KB (25 lines)
- **Classes:** 0
- **Functions:** 1
- **Complexity Score:** 0.17
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### main.py

- **Size:** 11.4 KB (252 lines)
- **Classes:** 0
- **Functions:** 7
- **Complexity Score:** 0.60
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def main()`

**Issues:**
- Deep nesting (8 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### test_typewriter_fix.py

- **Size:** 3.0 KB (95 lines)
- **Classes:** 1
- **Functions:** 6
- **Complexity Score:** 0.57
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def main()`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 3 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Analyzers\advanced_codebase_analyzer.py

- **Size:** 23.6 KB (585 lines)
- **Classes:** 1
- **Functions:** 26
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`

**Issues:**
- File is large (23.6KB) - consider modularization
- Too many functions (26) - consider class-based organization
- Deep nesting (9 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Analyzers\import_scanner.py

- **Size:** 13.4 KB (355 lines)
- **Classes:** 3
- **Functions:** 19
- **Complexity Score:** 0.91
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`
- `def __init__(self,root_path)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Analyzers\logs Parser_error_detector.py

- **Size:** 3.6 KB (95 lines)
- **Classes:** 0
- **Functions:** 4
- **Complexity Score:** 0.52
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`

**Issues:**
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Analyzers\program_flow_graph.py

- **Size:** 4.0 KB (127 lines)
- **Classes:** 0
- **Functions:** 3
- **Complexity Score:** 0.48
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def main()`

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Analyzers\program_flow_tracer.py

- **Size:** 22.9 KB (570 lines)
- **Classes:** 1
- **Functions:** 11
- **Complexity Score:** 0.71
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`

**Issues:**
- File is large (22.9KB) - consider modularization
- Deep nesting (7 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Analyzers\refactoring_analyzer.py

- **Size:** 49.9 KB (1176 lines)
- **Classes:** 8
- **Functions:** 49
- **Complexity Score:** 1.00
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`
- `def __init__(self)`
- `def __init__(self,root_path)`
- `def visit_Import(self,node)`
- `def visit_ImportFrom(self,node)`

**Issues:**
- File is large (49.9KB) - consider modularization
- Long file (839 lines) - consider splitting
- Too many functions (49) - consider class-based organization
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Legacy\LOGGER_ID_Creator.py

- **Size:** 22.1 KB (526 lines)
- **Classes:** 0
- **Functions:** 12
- **Complexity Score:** 0.68
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Issues:**
- File is large (22.1KB) - consider modularization
- Deep nesting (9 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Simplify nested conditions using early returns
- Extract complex logic into separate functions

### Development_Tools\Profiler\profiler_helpers.py

- **Size:** 22.6 KB (601 lines)
- **Classes:** 4
- **Functions:** 23
- **Complexity Score:** 0.96
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def __init__(self)`
- `def __init__(self,interval)`
- `def start(self)`
- `def stop(self)`
- `def _monitor_loop(self)`
- `def _collect(self)`
- `def get_data(self)`

**Issues:**
- File is large (22.6KB) - consider modularization
- Too many functions (23) - consider class-based organization
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 7 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Group related functions into classes
- Create separate utility modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Profiler\unified_profiler.py

- **Size:** 4.4 KB (136 lines)
- **Classes:** 0
- **Functions:** 3
- **Complexity Score:** 0.51
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`

**Issues:**
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py

- **Size:** 27.7 KB (597 lines)
- **Classes:** 2
- **Functions:** 16
- **Complexity Score:** 0.82
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`
- `def __init__(self)`

**Issues:**
- File is large (27.7KB) - consider modularization
- Deep nesting (7 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Utilities\generate_directory_tree.py

- **Size:** 11.2 KB (326 lines)
- **Classes:** 1
- **Functions:** 9
- **Complexity Score:** 0.68
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`

**Issues:**
- Deep nesting (8 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### Development_Tools\Utilities\run_analyzer.py

- **Size:** 4.2 KB (130 lines)
- **Classes:** 0
- **Functions:** 4
- **Complexity Score:** 0.54
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def main()`

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### PACKAGING_the_app\package_app.py

- **Size:** 21.4 KB (666 lines)
- **Classes:** 1
- **Functions:** 14
- **Complexity Score:** 0.75
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def main()`
- `def __init__(self)`

**Issues:**
- File is large (21.4KB) - consider modularization
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 3 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\app\app_lifecycle.py

- **Size:** 21.0 KB (479 lines)
- **Classes:** 1
- **Functions:** 24
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Issues:**
- File is large (21.0KB) - consider modularization
- Too many functions (24) - consider class-based organization
- Deep nesting (7 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\app\event_bus.py

- **Size:** 54.2 KB (1146 lines)
- **Classes:** 1
- **Functions:** 62
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Issues:**
- File is very large (54.2KB) - consider splitting
- Long file (788 lines) - consider splitting
- Too many functions (62) - consider class-based organization
- Deep nesting (7 levels) - consider simplifying logic
- Many imports (30) - consider organizing imports
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 6 duplicate functions that could be consolidated

**Recommendations:**
- Split into multiple smaller files
- Extract classes into separate modules
- Create a dedicated module for this functionality
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\app\main.py

- **Size:** 6.5 KB (168 lines)
- **Classes:** 1
- **Functions:** 12
- **Complexity Score:** 0.70
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`
- `def show_ollama_connection_error(self,context,force_show)`
- `def check_ollama_connection(self)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 12 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\app\service_manager.py

- **Size:** 8.7 KB (206 lines)
- **Classes:** 1
- **Functions:** 18
- **Complexity Score:** 0.81
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def cleanup(self)`

**Issues:**
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\app\threading_integration.py

- **Size:** 9.8 KB (252 lines)
- **Classes:** 2
- **Functions:** 15
- **Complexity Score:** 0.79
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def stop_chat_streaming(self)`
- `def get_threading_status(self) -> Dict[str, Any]`
- `def __init__(self,event_handler)`
- `def start_chat_streaming(self,context_messages,chosen_model,temperature,config_manager) -> bool`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 4 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\config\config_manager.py

- **Size:** 10.5 KB (279 lines)
- **Classes:** 1
- **Functions:** 43
- **Complexity Score:** 0.82
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Issues:**
- Too many functions (43) - consider class-based organization
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True

**Recommendations:**
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Group related functions into classes
- Create separate utility modules

### pyside_chat\core\logging\helpers.py

- **Size:** 18.3 KB (428 lines)
- **Classes:** 3
- **Functions:** 46
- **Complexity Score:** 0.90
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`
- `def cleanup(self)`

**Issues:**
- Too many functions (46) - consider class-based organization
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\logging\logger.py

- **Size:** 7.9 KB (207 lines)
- **Classes:** 5
- **Functions:** 24
- **Complexity Score:** 1.00
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def __new__(cls)`
- `def info(self,msg)`
- `def debug(self,msg)`
- `def warning(self,msg)`
- `def error(self,msg)`

**Issues:**
- Too many functions (24) - consider class-based organization
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\models\base_model.py

- **Size:** 0.5 KB (20 lines)
- **Classes:** 1
- **Functions:** 2
- **Complexity Score:** 0.19
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\models\conversation_metadata.py

- **Size:** 20.3 KB (502 lines)
- **Classes:** 2
- **Functions:** 26
- **Complexity Score:** 0.88
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def to_dict(self) -> Dict[str, Any]`

**Issues:**
- File is large (20.3KB) - consider modularization
- Too many functions (26) - consider class-based organization
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\persistent_thread_pool.py

- **Size:** 16.5 KB (399 lines)
- **Classes:** 1
- **Functions:** 11
- **Complexity Score:** 0.71
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Issues:**
- Deep nesting (8 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 4 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\qrunnable_tasks.py

- **Size:** 27.7 KB (724 lines)
- **Classes:** 5
- **Functions:** 25
- **Complexity Score:** 1.00
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def run(self)`

**Issues:**
- File is large (27.7KB) - consider modularization
- Too many functions (25) - consider class-based organization
- Deep nesting (8 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\qthread_workers.py

- **Size:** 19.9 KB (502 lines)
- **Classes:** 4
- **Functions:** 16
- **Complexity Score:** 0.90
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def stop(self)`
- `def __init__(self,parent)`
- `def _stream_operation(self)`

**Issues:**
- Deep nesting (9 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 4 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\threading_service.py

- **Size:** 24.4 KB (588 lines)
- **Classes:** 1
- **Functions:** 26
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def cleanup(self)`
- `def stop_chat_streaming(self)`
- `def get_threading_status(self) -> Dict[str, Any]`
- `def __init__(self,parent)`

**Issues:**
- File is large (24.4KB) - consider modularization
- Too many functions (26) - consider class-based organization
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 8 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\thread_calculator.py

- **Size:** 16.9 KB (413 lines)
- **Classes:** 2
- **Functions:** 10
- **Complexity Score:** 0.73
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`

**Issues:**
- Deep nesting (7 levels) - consider simplifying logic
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\thread_calculator_examples.py

- **Size:** 5.9 KB (156 lines)
- **Classes:** 1
- **Functions:** 6
- **Complexity Score:** 0.59
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def main()`

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\thread_monitor.py

- **Size:** 20.3 KB (523 lines)
- **Classes:** 1
- **Functions:** 18
- **Complexity Score:** 0.81
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def unregister_thread(self,thread_name)`
- `def _on_thread_started(self,thread_name)`
- `def _on_thread_finished(self,thread_name)`
- `def __init__(self,parent)`
- `def shutdown(self)`

**Issues:**
- File is large (20.3KB) - consider modularization
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\thread_pool_manager.py

- **Size:** 17.0 KB (470 lines)
- **Classes:** 1
- **Functions:** 15
- **Complexity Score:** 0.77
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def get_pool_status(self) -> Dict[str, Any]`
- `def shutdown(self)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\usage_examples.py

- **Size:** 19.7 KB (480 lines)
- **Classes:** 1
- **Functions:** 18
- **Complexity Score:** 0.81
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`
- `def cleanup(self)`
- `def stop_chat_streaming(self)`
- `def get_threading_status(self) -> Dict[str, Any]`
- `def _on_chat_chunk_received(self,chunk)`
- `def _on_chat_progress_updated(self,progress)`
- `def _on_chat_streaming_finished(self)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 7 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\threading\__init__.py

- **Size:** 3.2 KB (101 lines)
- **Classes:** 0
- **Functions:** 2
- **Complexity Score:** 0.49
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def shutdown_global_persistent_thread_pool()`
- `def shutdown_global_threading_service()`

**Issues:**
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\utils\error_handler.py

- **Size:** 14.6 KB (479 lines)
- **Classes:** 1
- **Functions:** 26
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Duplicate Functions:**
- `def wrapper()`

**Issues:**
- Too many functions (26) - consider class-based organization
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\utils\internet_checker.py

- **Size:** 5.8 KB (190 lines)
- **Classes:** 1
- **Functions:** 9
- **Complexity Score:** 0.66
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Issues:**
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\utils\streaming_handler.py

- **Size:** 10.1 KB (257 lines)
- **Classes:** 1
- **Functions:** 19
- **Complexity Score:** 0.83
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def cleanup(self)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 10 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\utils\threading_audit.py

- **Size:** 12.9 KB (330 lines)
- **Classes:** 1
- **Functions:** 11
- **Complexity Score:** 0.71
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def __init__(self)`
- `def generate_report(self) -> str`

**Issues:**
- Deep nesting (7 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\core\utils\threading_utils.py

- **Size:** 15.1 KB (483 lines)
- **Classes:** 1
- **Functions:** 34
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def wrapper()`

**Issues:**
- Too many functions (34) - consider class-based organization
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\chat\chat_controller.py

- **Size:** 23.8 KB (487 lines)
- **Classes:** 1
- **Functions:** 24
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Issues:**
- File is large (23.8KB) - consider modularization
- Too many functions (24) - consider class-based organization
- Many imports (18) - consider organizing imports
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\chat\conversation_service.py

- **Size:** 6.6 KB (156 lines)
- **Classes:** 1
- **Functions:** 10
- **Complexity Score:** 0.67
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def get_messages(self) -> List[Dict]`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\chat\complexity_analyser\complexity_analyzer.py

- **Size:** 18.0 KB (417 lines)
- **Classes:** 3
- **Functions:** 14
- **Complexity Score:** 0.83
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\chat\enhancers\enhancement_service.py

- **Size:** 1.6 KB (43 lines)
- **Classes:** 1
- **Functions:** 4
- **Complexity Score:** 0.35
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\chat\summarization\summarization_service.py

- **Size:** 18.1 KB (415 lines)
- **Classes:** 1
- **Functions:** 10
- **Complexity Score:** 0.69
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self,ollama_service)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\memory\memory_service.py

- **Size:** 42.1 KB (975 lines)
- **Classes:** 8
- **Functions:** 41
- **Complexity Score:** 1.00
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def __post_init__(self)`
- `def get_messages(self) -> List[Dict]`
- `def _load(self)`
- `def add_message(self,message)`
- `def clear(self)`
- `def _save(self)`

**Issues:**
- File is large (42.1KB) - consider modularization
- Long file (731 lines) - consider splitting
- Too many functions (41) - consider class-based organization
- Deep nesting (7 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 8 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\memory\semantic_search.py

- **Size:** 22.0 KB (472 lines)
- **Classes:** 2
- **Functions:** 12
- **Complexity Score:** 0.76
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def get_memory_stats(self) -> Dict`

**Issues:**
- File is large (22.0KB) - consider modularization
- Deep nesting (7 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 8 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\memory\semantic_search_fallback.py

- **Size:** 15.9 KB (371 lines)
- **Classes:** 2
- **Functions:** 12
- **Complexity Score:** 0.76
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def get_memory_stats(self) -> Dict`
- `def add_memory(self,memory_id,content,memory_type,importance,tags,metadata) -> bool`
- `def remove_memory(self,memory_id) -> bool`
- `def search_semantic(self,query,max_results,min_similarity,memory_types) -> List[Tuple[str, float, Dict]]`
- `def search_hybrid(self,query,max_results,min_similarity,memory_types,keyword_weight,semantic_weight) -> List[Tuple[str, float, Dict]]`
- `def update_memory_importance(self,memory_id,new_importance) -> bool`
- `def clear_all(self)`
- `def is_ready(self) -> bool`

**Issues:**
- Deep nesting (7 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 8 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\ollama\ollama_chat.py

- **Size:** 5.4 KB (146 lines)
- **Classes:** 1
- **Functions:** 11
- **Complexity Score:** 0.69
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`
- `def show_ollama_connection_error(self,context,force_show)`
- `def check_ollama_connection(self)`
- `def _setup_ui(self)`
- `def showEvent(self,event)`
- `def closeEvent(self,event)`
- `def get_service_manager(self)`
- `def get_ui_manager(self)`
- `def get_event_handler(self)`
- `def get_lifecycle_manager(self)`
- `def get_chat_controller(self)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 11 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\ollama\ollama_service.py

- **Size:** 36.6 KB (713 lines)
- **Classes:** 1
- **Functions:** 20
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def cleanup(self)`
- `def test_connection(self) -> bool`

**Issues:**
- File is large (36.6KB) - consider modularization
- Long file (515 lines) - consider splitting
- Deep nesting (11 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\personality\loader.py

- **Size:** 11.4 KB (272 lines)
- **Classes:** 1
- **Functions:** 14
- **Complexity Score:** 0.75
- **Responsibilities:** GUI: False, Logic: True, Data: True

**Issues:**
- Mixed responsibilities detected - GUI: False, Logic: True, Data: True
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\personality\models\personality_model.py

- **Size:** 3.7 KB (86 lines)
- **Classes:** 1
- **Functions:** 12
- **Complexity Score:** 0.62
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self,personalities_dir)`

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\personality\models\personality_types.py

- **Size:** 2.0 KB (78 lines)
- **Classes:** 5
- **Functions:** 1
- **Complexity Score:** 0.59
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def __post_init__(self)`

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\personality\services\personality_service.py

- **Size:** 20.5 KB (447 lines)
- **Classes:** 1
- **Functions:** 28
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def get_ai_name(self) -> str`
- `def __init__(self,personalities_dir)`

**Issues:**
- File is large (20.5KB) - consider modularization
- Too many functions (28) - consider class-based organization
- Deep nesting (9 levels) - consider simplifying logic
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\user\user_profile_service.py

- **Size:** 0.6 KB (20 lines)
- **Classes:** 1
- **Functions:** 3
- **Complexity Score:** 0.21
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\voice_service.py

- **Size:** 55.1 KB (1264 lines)
- **Classes:** 1
- **Functions:** 57
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`
- `def _on_tts_finished(self)`
- `def cleanup_on_exit(self)`
- `def _setup_connections(self)`
- `def _initialize_services(self)`

**Issues:**
- File is very large (55.1KB) - consider splitting
- Long file (893 lines) - consider splitting
- Too many functions (57) - consider class-based organization
- Deep nesting (6 levels) - consider simplifying logic
- Many imports (35) - consider organizing imports
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 32 duplicate functions that could be consolidated

**Recommendations:**
- Split into multiple smaller files
- Extract classes into separate modules
- Create a dedicated module for this functionality
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\voice_service_manager.py

- **Size:** 11.6 KB (284 lines)
- **Classes:** 1
- **Functions:** 17
- **Complexity Score:** 0.80
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`
- `def cleanup(self)`
- `def __new__(cls)`
- `def _initialize_voice_service(self)`
- `def is_ready(self) -> bool`
- `def update_settings(self,settings)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 7 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\voice_service_wrapper.py

- **Size:** 18.7 KB (387 lines)
- **Classes:** 1
- **Functions:** 36
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def cleanup_on_exit(self)`
- `def test_connection(self) -> bool`
- `def is_voice_available(self) -> bool`
- `def start_voice_input(self)`
- `def stop_voice_input(self)`
- `def speak_text(self,text)`
- `def stop_tts(self)`
- `def set_continuous_voice_mode(self,enabled)`
- `def is_continuous_voice_mode(self) -> bool`
- `def update_settings(self,settings)`
- `def get_silence_duration(self) -> float`
- `def get_silence_threshold(self) -> float`
- `def get_recording_timeout(self) -> float`
- `def get_current_audio_level(self) -> float`
- `def set_recording_timeout(self,timeout)`
- `def set_silence_duration(self,duration)`
- `def set_silence_threshold(self,threshold)`
- `def set_audio_gate_enabled(self,enabled)`
- `def get_audio_folder_path(self) -> str`
- `def list_audio_files(self) -> list`
- `def cleanup_old_audio_files(self,max_files,max_age_days)`
- `def cleanup_all_audio_files(self)`
- `def _on_voice_service_ready(self)`

**Issues:**
- Too many functions (36) - consider class-based organization
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 26 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\audio\recording_service.py

- **Size:** 14.4 KB (318 lines)
- **Classes:** 1
- **Functions:** 16
- **Complexity Score:** 0.78
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def __init__(self)`
- `def cleanup(self)`
- `def get_current_audio_level(self) -> float`
- `def set_audio_gate_enabled(self,enabled)`

**Issues:**
- Deep nesting (9 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 8 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\orchestrator\voice_process_manager.py

- **Size:** 20.5 KB (474 lines)
- **Classes:** 2
- **Functions:** 15
- **Complexity Score:** 0.81
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`
- `def stop(self)`
- `def run(self)`
- `def get_process_info(self) -> Dict[str, Any]`

**Issues:**
- File is large (20.5KB) - consider modularization
- Deep nesting (16 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 4 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\stt\stt_service.py

- **Size:** 6.6 KB (154 lines)
- **Classes:** 1
- **Functions:** 8
- **Complexity Score:** 0.66
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def __init__(self)`
- `def _check_availability(self) -> bool`
- `def is_available(self) -> bool`
- `def is_initialized(self) -> bool`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\tts\coqui_tts_service.py

- **Size:** 47.8 KB (1063 lines)
- **Classes:** 1
- **Functions:** 47
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def __init__(self)`
- `def cleanup(self)`
- `def __new__(cls)`
- `def get_instance()`
- `def __del__(self)`
- `def is_available(self) -> bool`
- `def is_initialized(self) -> bool`

**Issues:**
- File is large (47.8KB) - consider modularization
- Long file (790 lines) - consider splitting
- Too many functions (47) - consider class-based organization
- Deep nesting (10 levels) - consider simplifying logic
- Many imports (30) - consider organizing imports
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 9 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\tts\streaming_audio_player.py

- **Size:** 17.6 KB (384 lines)
- **Classes:** 1
- **Functions:** 11
- **Complexity Score:** 0.71
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def cleanup(self)`
- `def run(self)`
- `def __del__(self)`
- `def stop_playback(self)`

**Issues:**
- Deep nesting (8 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 4 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\tts\streaming_audio_worker.py

- **Size:** 6.6 KB (147 lines)
- **Classes:** 1
- **Functions:** 6
- **Complexity Score:** 0.63
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def stop(self)`
- `def run(self)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\features\voice\tts\tts_service.py

- **Size:** 9.6 KB (238 lines)
- **Classes:** 1
- **Functions:** 21
- **Complexity Score:** 0.82
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def __init__(self)`
- `def cleanup(self)`
- `def get_instance()`
- `def speak_text(self,text)`
- `def speak_text_streaming(self,text)`
- `def speak_text_non_streaming(self,text)`
- `def _check_availability(self) -> bool`
- `def is_available(self) -> bool`
- `def is_initialized(self) -> bool`
- `def update_api(self,api_name)`
- `def stop_playback(self)`

**Issues:**
- Too many functions (21) - consider class-based organization
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 11 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\startup\dependency_checker.py

- **Size:** 11.5 KB (290 lines)
- **Classes:** 1
- **Functions:** 12
- **Complexity Score:** 0.72
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\startup\install_dependencies.py

- **Size:** 0.9 KB (27 lines)
- **Classes:** 0
- **Functions:** 1
- **Complexity Score:** 0.14
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Duplicate Functions:**
- `def main()`

**Issues:**
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\startup\system_installer.py

- **Size:** 6.0 KB (113 lines)
- **Classes:** 0
- **Functions:** 3
- **Complexity Score:** 0.55
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic

**Recommendations:**
- Simplify nested conditions using early returns
- Extract complex logic into separate functions

### pyside_chat\ui\ui_manager.py

- **Size:** 10.1 KB (244 lines)
- **Classes:** 1
- **Functions:** 14
- **Complexity Score:** 0.75
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules

### pyside_chat\ui\dialogs\coqui_model_dialog.py

- **Size:** 15.4 KB (409 lines)
- **Classes:** 2
- **Functions:** 17
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self,parent)`
- `def run(self)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 4 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\dialogs\error_dialog.py

- **Size:** 10.4 KB (297 lines)
- **Classes:** 2
- **Functions:** 10
- **Complexity Score:** 0.73
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def copy_error(self)`
- `def reset_copy_button(self,button)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 3 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\dialogs\settings_dialog.py

- **Size:** 16.9 KB (385 lines)
- **Classes:** 1
- **Functions:** 10
- **Complexity Score:** 0.67
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def setup_ui(self)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 3 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\dialogs\voice_settings_dialog.py

- **Size:** 63.0 KB (1516 lines)
- **Classes:** 3
- **Functions:** 41
- **Complexity Score:** 0.92
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def setup_connections(self)`
- `def __init__(self,parent)`
- `def run(self)`
- `def safe_disconnect(signal,slot)`
- `def setup_ui(self)`
- `def download_selected_model(self)`
- `def create_general_tab(self)`
- `def save_settings(self)`

**Issues:**
- File is very large (63.0KB) - consider splitting
- Very long file (1063 lines) - needs refactoring
- Too many functions (41) - consider class-based organization
- Deep nesting (9 levels) - consider simplifying logic
- Many imports (22) - consider organizing imports
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 9 duplicate functions that could be consolidated

**Recommendations:**
- Split into multiple smaller files
- Extract classes into separate modules
- Create a dedicated module for this functionality
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\memory_tab.py

- **Size:** 26.0 KB (572 lines)
- **Classes:** 1
- **Functions:** 22
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def setup_connections(self)`
- `def cleanup_memory_entries(self)`
- `def safe_disconnect(signal,slot,logger)`
- `def setup_ui(self)`

**Issues:**
- File is large (26.0KB) - consider modularization
- Too many functions (22) - consider class-based organization
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 4 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\model_tab.py

- **Size:** 17.5 KB (508 lines)
- **Classes:** 1
- **Functions:** 20
- **Complexity Score:** 0.80
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def setup_connections(self)`
- `def __init__(self,parent)`
- `def get_selected_model(self) -> str`
- `def setup_ui(self)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\personality_tab.py

- **Size:** 45.4 KB (1091 lines)
- **Classes:** 1
- **Functions:** 25
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self,parent)`
- `def get_system_prompt(self) -> str`
- `def setup_ui(self)`

**Issues:**
- File is large (45.4KB) - consider modularization
- Long file (580 lines) - consider splitting
- Too many functions (25) - consider class-based organization
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 5 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\chat_tab\chat_display.py

- **Size:** 16.9 KB (420 lines)
- **Classes:** 1
- **Functions:** 22
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def on_render_completed(self)`
- `def start_streaming(self)`
- `def get_ai_name(self) -> str`
- `def __init__(self,parent,config_manager)`

**Issues:**
- Too many functions (22) - consider class-based organization
- Deep nesting (7 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 12 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\chat_tab\chat_renderer.py

- **Size:** 21.9 KB (468 lines)
- **Classes:** 1
- **Functions:** 22
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def cleanup(self)`
- `def _get_next_message_id(self) -> str`
- `def append_message(self,sender,content,is_code,tag)`
- `def edit_message(self,message_index,new_content) -> bool`
- `def get_messages(self) -> List[Dict]`
- `def _process_typewriter_chunk(self)`
- `def update_streaming_message(self,content,sender,message_id,is_code,tag,append)`
- `def finalize_streaming_message(self)`
- `def update_last_system_switch(self,message)`
- `def clear_messages(self)`
- `def clear_chat(self)`

**Issues:**
- File is large (21.9KB) - consider modularization
- Too many functions (22) - consider class-based organization
- Deep nesting (8 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 11 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\chat_tab\chat_tab.py

- **Size:** 66.3 KB (1362 lines)
- **Classes:** 1
- **Functions:** 62
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: True

**Duplicate Functions:**
- `def setup_connections(self)`
- `def _stop_streaming_safe(self)`
- `def start_streaming(self)`
- `def get_ai_name(self) -> str`
- `def get_temperature(self) -> float`
- `def safe_disconnect(signal,slot,logger)`
- `def setup_ui(self)`
- `def update_model_list(self,models)`
- `def on_personality_changed(self,personality_name)`
- `def get_current_personality(self) -> str`
- `def on_message_edited(self,message_index,new_content)`
- `def append_to_chat(self,sender,message,is_code)`
- `def append_response_chunk(self,chunk,model_name)`
- `def stop_streaming(self)`
- `def clear_chat(self)`
- `def get_streaming_handler(self)`

**Issues:**
- File is very large (66.3KB) - consider splitting
- Long file (865 lines) - consider splitting
- Too many functions (62) - consider class-based organization
- Deep nesting (7 levels) - consider simplifying logic
- Many imports (42) - consider organizing imports
- Mixed responsibilities detected - GUI: True, Logic: True, Data: True
- Contains 36 duplicate functions that could be consolidated

**Recommendations:**
- Split into multiple smaller files
- Extract classes into separate modules
- Create a dedicated module for this functionality
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Separate business logic from data access using repository pattern
- Create dedicated service layer
- Separate GUI code from data access
- Use data binding or observer pattern
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\chat_tab\eq_visualizer.py

- **Size:** 22.0 KB (412 lines)
- **Classes:** 1
- **Functions:** 10
- **Complexity Score:** 0.69
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self,parent)`

**Issues:**
- File is large (22.0KB) - consider modularization
- Deep nesting (8 levels) - consider simplifying logic
- Many imports (16) - consider organizing imports
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\chat_tab\input_controls.py

- **Size:** 17.3 KB (430 lines)
- **Classes:** 1
- **Functions:** 20
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def setup_connections(self)`
- `def __init__(self,parent)`
- `def start_streaming(self)`
- `def get_temperature(self) -> float`
- `def update_model_list(self,models)`
- `def get_current_personality(self) -> str`
- `def setup_ui_components(self)`
- `def stop_streaming(self)`
- `def get_ui_components(self) -> dict`
- `def on_model_changed(self,model_name)`
- `def get_current_model(self) -> str`
- `def get_current_response(self) -> str`
- `def force_enable_send_button(self)`
- `def update_personality_list(self,personalities)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 14 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\tabs\chat_tab\voice_controls.py

- **Size:** 80.9 KB (1941 lines)
- **Classes:** 1
- **Functions:** 87
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def cleanup(self)`
- `def setup_connections(self)`
- `def _on_tts_finished(self)`
- `def get_voice_service(self)`
- `def _on_recording_started(self)`
- `def _on_recording_stopped(self)`
- `def _on_recording_error(self,error)`
- `def _on_tts_started(self)`
- `def _on_tts_error(self,error)`
- `def _reset_error_count(self)`
- `def _on_voice_service_ready(self)`
- `def __del__(self)`
- `def safe_disconnect(signal,slot,logger)`
- `def __init__(self,parent,config_manager)`
- `def setup_ui_components(self)`
- `def get_ui_components(self) -> dict`
- `def on_user_interrupted(self)`
- `def on_request_cancelled(self)`
- `def on_voice_input_received(self,text)`
- `def on_voice_input_error(self,error)`
- `def on_tts_started(self)`
- `def on_tts_finished(self)`
- `def on_tts_error(self,error)`
- `def on_recording_started(self)`
- `def on_recording_stopped(self)`
- `def on_recording_error(self,error)`
- `def on_voice_processing_started(self)`
- `def on_voice_processing_finished(self)`
- `def on_audio_level_changed(self,audio_level)`
- `def on_eq_bars_changed(self,bar_values)`
- `def speak_ai_response(self,text)`

**Issues:**
- File is very large (80.9KB) - consider splitting
- Very long file (1273 lines) - needs refactoring
- Too many functions (87) - consider class-based organization
- Deep nesting (7 levels) - consider simplifying logic
- Many imports (39) - consider organizing imports
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 31 duplicate functions that could be consolidated

**Recommendations:**
- Split into multiple smaller files
- Extract classes into separate modules
- Create a dedicated module for this functionality
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\themes\message_formatter.py

- **Size:** 18.8 KB (359 lines)
- **Classes:** 1
- **Functions:** 13
- **Complexity Score:** 0.73
- **Responsibilities:** GUI: False, Logic: True, Data: False

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic

**Recommendations:**
- Simplify nested conditions using early returns
- Extract complex logic into separate functions

### pyside_chat\ui\utils\message_utils.py

- **Size:** 2.7 KB (73 lines)
- **Classes:** 0
- **Functions:** 7
- **Complexity Score:** 0.44
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules

### pyside_chat\ui\visualizers\eq_orchestrator.py

- **Size:** 29.8 KB (676 lines)
- **Classes:** 1
- **Functions:** 22
- **Complexity Score:** 0.84
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self)`

**Issues:**
- File is large (29.8KB) - consider modularization
- Long file (516 lines) - consider splitting
- Too many functions (22) - consider class-based organization
- Deep nesting (9 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 1 duplicate functions that could be consolidated

**Recommendations:**
- Consider extracting large functions into separate modules
- Group related functionality into classes
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Group related functions into classes
- Create separate utility modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\visualizers\widgets\bar_eq_widget.py

- **Size:** 10.5 KB (271 lines)
- **Classes:** 1
- **Functions:** 12
- **Complexity Score:** 0.72
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 7 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\visualizers\widgets\circle_eq_widget.py

- **Size:** 8.1 KB (212 lines)
- **Classes:** 1
- **Functions:** 10
- **Complexity Score:** 0.67
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def _setup_animation_timer(self)`
- `def _animate(self)`
- `def set_idle(self)`
- `def start_animation(self)`
- `def stop_animation(self)`
- `def get_current_values(self)`
- `def paintEvent(self,event)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 7 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py

- **Size:** 5.8 KB (142 lines)
- **Classes:** 1
- **Functions:** 8
- **Complexity Score:** 0.64
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def _animate(self)`
- `def set_idle(self)`
- `def start_animation(self)`
- `def stop_animation(self)`
- `def paintEvent(self,event)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 6 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py

- **Size:** 5.3 KB (129 lines)
- **Classes:** 1
- **Functions:** 7
- **Complexity Score:** 0.65
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def _animate(self)`
- `def set_idle(self)`
- `def start_animation(self)`
- `def stop_animation(self)`
- `def paintEvent(self,event)`
- `def set_net_radii(self,values)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 6 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\Widgets\chat_navigation.py

- **Size:** 18.1 KB (421 lines)
- **Classes:** 1
- **Functions:** 15
- **Complexity Score:** 0.77
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def setup_connections(self)`
- `def setup_ui(self)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 3 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\Widgets\complexity_widget.py

- **Size:** 9.9 KB (241 lines)
- **Classes:** 1
- **Functions:** 11
- **Complexity Score:** 0.71
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def __init__(self,parent)`
- `def setup_ui(self)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\Widgets\message_editor.py

- **Size:** 7.2 KB (210 lines)
- **Classes:** 1
- **Functions:** 9
- **Complexity Score:** 0.64
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def setup_ui(self)`
- `def setup_styles(self)`

**Issues:**
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 2 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

### pyside_chat\ui\Widgets\spellchecker_widget.py

- **Size:** 8.3 KB (213 lines)
- **Classes:** 1
- **Functions:** 13
- **Complexity Score:** 0.73
- **Responsibilities:** GUI: True, Logic: True, Data: False

**Duplicate Functions:**
- `def cleanup(self)`
- `def __init__(self,parent)`
- `def show_context_menu(self,position)`

**Issues:**
- Deep nesting (6 levels) - consider simplifying logic
- Mixed responsibilities detected - GUI: True, Logic: True, Data: False
- Contains 3 duplicate functions that could be consolidated

**Recommendations:**
- Separate GUI code from business logic using MVC pattern
- Create separate UI and controller modules
- Simplify nested conditions using early returns
- Extract complex logic into separate functions
- Extract duplicate functions into a shared utility module
- Consider creating a common library for shared functionality

## 📁 Directory Analysis

### .

- **Files:** 3
- **Total Lines:** 372
- **Total Size:** 15.1 KB

**Largest Files:**
- `main.py` (11.4 KB)
- `test_typewriter_fix.py` (3.0 KB)
- `check_critical_issues.py` (0.7 KB)

**Most Complex Files:**
- `main.py` (complexity: 0.60)
- `test_typewriter_fix.py` (complexity: 0.57)
- `check_critical_issues.py` (complexity: 0.17)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories

### Development_Tools\Analyzers

- **Files:** 6
- **Total Lines:** 2,908
- **Total Size:** 117.4 KB

**Largest Files:**
- `Development_Tools\Analyzers\refactoring_analyzer.py` (49.9 KB)
- `Development_Tools\Analyzers\advanced_codebase_analyzer.py` (23.6 KB)
- `Development_Tools\Analyzers\program_flow_tracer.py` (22.9 KB)
- `Development_Tools\Analyzers\import_scanner.py` (13.4 KB)
- `Development_Tools\Analyzers\program_flow_graph.py` (4.0 KB)

**Most Complex Files:**
- `Development_Tools\Analyzers\refactoring_analyzer.py` (complexity: 1.00)
- `Development_Tools\Analyzers\import_scanner.py` (complexity: 0.91)
- `Development_Tools\Analyzers\advanced_codebase_analyzer.py` (complexity: 0.84)
- `Development_Tools\Analyzers\program_flow_tracer.py` (complexity: 0.71)
- `Development_Tools\Analyzers\logs Parser_error_detector.py` (complexity: 0.52)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### Development_Tools\Legacy

- **Files:** 1
- **Total Lines:** 526
- **Total Size:** 22.1 KB

**Largest Files:**
- `Development_Tools\Legacy\LOGGER_ID_Creator.py` (22.1 KB)

**Most Complex Files:**
- `Development_Tools\Legacy\LOGGER_ID_Creator.py` (complexity: 0.68)

**Issues:**
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization

**Recommendations:**
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules

### Development_Tools\Profiler

- **Files:** 2
- **Total Lines:** 737
- **Total Size:** 27.0 KB

**Largest Files:**
- `Development_Tools\Profiler\profiler_helpers.py` (22.6 KB)
- `Development_Tools\Profiler\unified_profiler.py` (4.4 KB)

**Most Complex Files:**
- `Development_Tools\Profiler\profiler_helpers.py` (complexity: 0.96)
- `Development_Tools\Profiler\unified_profiler.py` (complexity: 0.51)

**Issues:**
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### Development_Tools\ThreadingAnalyser

- **Files:** 1
- **Total Lines:** 597
- **Total Size:** 27.7 KB

**Largest Files:**
- `Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py` (27.7 KB)

**Most Complex Files:**
- `Development_Tools\ThreadingAnalyser\thread_safety_analyzer.py` (complexity: 0.82)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### Development_Tools\Utilities

- **Files:** 4
- **Total Lines:** 472
- **Total Size:** 15.9 KB

**Largest Files:**
- `Development_Tools\Utilities\generate_directory_tree.py` (11.2 KB)
- `Development_Tools\Utilities\run_analyzer.py` (4.2 KB)
- `Development_Tools\Utilities\verify cuda.py` (0.4 KB)
- `Development_Tools\Utilities\how_many_threads.py` (0.1 KB)

**Most Complex Files:**
- `Development_Tools\Utilities\generate_directory_tree.py` (complexity: 0.68)
- `Development_Tools\Utilities\run_analyzer.py` (complexity: 0.54)
- `Development_Tools\Utilities\verify cuda.py` (complexity: 0.07)
- `Development_Tools\Utilities\how_many_threads.py` (complexity: 0.02)

**Issues:**
- Directory contains mixed business logic and data access - consider separation

**Recommendations:**
- Create separate 'services' and 'data' subdirectories

### PACKAGING_the_app

- **Files:** 1
- **Total Lines:** 666
- **Total Size:** 21.4 KB

**Largest Files:**
- `PACKAGING_the_app\package_app.py` (21.4 KB)

**Most Complex Files:**
- `PACKAGING_the_app\package_app.py` (complexity: 0.75)

**Issues:**
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\app

- **Files:** 6
- **Total Lines:** 2,251
- **Total Size:** 100.2 KB

**Largest Files:**
- `pyside_chat\app\event_bus.py` (54.2 KB)
- `pyside_chat\app\app_lifecycle.py` (21.0 KB)
- `pyside_chat\app\threading_integration.py` (9.8 KB)
- `pyside_chat\app\service_manager.py` (8.7 KB)
- `pyside_chat\app\main.py` (6.5 KB)

**Most Complex Files:**
- `pyside_chat\app\app_lifecycle.py` (complexity: 0.84)
- `pyside_chat\app\event_bus.py` (complexity: 0.84)
- `pyside_chat\app\service_manager.py` (complexity: 0.81)
- `pyside_chat\app\threading_integration.py` (complexity: 0.79)
- `pyside_chat\app\main.py` (complexity: 0.70)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\config

- **Files:** 2
- **Total Lines:** 280
- **Total Size:** 10.5 KB

**Largest Files:**
- `pyside_chat\config\config_manager.py` (10.5 KB)
- `pyside_chat\config\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\config\config_manager.py` (complexity: 0.82)
- `pyside_chat\config\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed business logic and data access - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'services' and 'data' subdirectories
- Simplify complex files by extracting helper functions

### pyside_chat\core\logging

- **Files:** 3
- **Total Lines:** 635
- **Total Size:** 26.2 KB

**Largest Files:**
- `pyside_chat\core\logging\helpers.py` (18.3 KB)
- `pyside_chat\core\logging\logger.py` (7.9 KB)
- `pyside_chat\core\logging\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\core\logging\logger.py` (complexity: 1.00)
- `pyside_chat\core\logging\helpers.py` (complexity: 0.90)
- `pyside_chat\core\logging\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Simplify complex files by extracting helper functions

### pyside_chat\core\models

- **Files:** 3
- **Total Lines:** 522
- **Total Size:** 20.8 KB

**Largest Files:**
- `pyside_chat\core\models\conversation_metadata.py` (20.3 KB)
- `pyside_chat\core\models\base_model.py` (0.5 KB)
- `pyside_chat\core\models\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\core\models\conversation_metadata.py` (complexity: 0.88)
- `pyside_chat\core\models\base_model.py` (complexity: 0.19)
- `pyside_chat\core\models\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\core\threading

- **Files:** 11
- **Total Lines:** 4,636
- **Total Size:** 180.4 KB

**Largest Files:**
- `pyside_chat\core\threading\qrunnable_tasks.py` (27.7 KB)
- `pyside_chat\core\threading\threading_service.py` (24.4 KB)
- `pyside_chat\core\threading\thread_monitor.py` (20.3 KB)
- `pyside_chat\core\threading\qthread_workers.py` (19.9 KB)
- `pyside_chat\core\threading\usage_examples.py` (19.7 KB)

**Most Complex Files:**
- `pyside_chat\core\threading\qrunnable_tasks.py` (complexity: 1.00)
- `pyside_chat\core\threading\qthread_workers.py` (complexity: 0.90)
- `pyside_chat\core\threading\threading_service.py` (complexity: 0.84)
- `pyside_chat\core\threading\thread_monitor.py` (complexity: 0.81)
- `pyside_chat\core\threading\usage_examples.py` (complexity: 0.81)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\core\utils

- **Files:** 7
- **Total Lines:** 1,865
- **Total Size:** 63.3 KB

**Largest Files:**
- `pyside_chat\core\utils\threading_utils.py` (15.1 KB)
- `pyside_chat\core\utils\error_handler.py` (14.6 KB)
- `pyside_chat\core\utils\threading_audit.py` (12.9 KB)
- `pyside_chat\core\utils\streaming_handler.py` (10.1 KB)
- `pyside_chat\core\utils\internet_checker.py` (5.8 KB)

**Most Complex Files:**
- `pyside_chat\core\utils\error_handler.py` (complexity: 0.84)
- `pyside_chat\core\utils\threading_utils.py` (complexity: 0.84)
- `pyside_chat\core\utils\streaming_handler.py` (complexity: 0.83)
- `pyside_chat\core\utils\threading_audit.py` (complexity: 0.71)
- `pyside_chat\core\utils\internet_checker.py` (complexity: 0.66)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Simplify complex files by extracting helper functions

### pyside_chat\features\chat

- **Files:** 3
- **Total Lines:** 643
- **Total Size:** 30.4 KB

**Largest Files:**
- `pyside_chat\features\chat\chat_controller.py` (23.8 KB)
- `pyside_chat\features\chat\conversation_service.py` (6.6 KB)
- `pyside_chat\features\chat\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\chat\chat_controller.py` (complexity: 0.84)
- `pyside_chat\features\chat\conversation_service.py` (complexity: 0.67)
- `pyside_chat\features\chat\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\features\chat\complexity_analyser

- **Files:** 1
- **Total Lines:** 417
- **Total Size:** 18.0 KB

**Largest Files:**
- `pyside_chat\features\chat\complexity_analyser\complexity_analyzer.py` (18.0 KB)

**Most Complex Files:**
- `pyside_chat\features\chat\complexity_analyser\complexity_analyzer.py` (complexity: 0.83)

**Issues:**
- Directory contains many complex files - consider simplification

**Recommendations:**
- Simplify complex files by extracting helper functions

### pyside_chat\features\chat\summarization

- **Files:** 2
- **Total Lines:** 415
- **Total Size:** 18.1 KB

**Largest Files:**
- `pyside_chat\features\chat\summarization\summarization_service.py` (18.1 KB)
- `pyside_chat\features\chat\summarization\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\chat\summarization\summarization_service.py` (complexity: 0.69)
- `pyside_chat\features\chat\summarization\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories

### pyside_chat\features\memory

- **Files:** 4
- **Total Lines:** 1,818
- **Total Size:** 80.0 KB

**Largest Files:**
- `pyside_chat\features\memory\memory_service.py` (42.1 KB)
- `pyside_chat\features\memory\semantic_search.py` (22.0 KB)
- `pyside_chat\features\memory\semantic_search_fallback.py` (15.9 KB)
- `pyside_chat\features\memory\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\memory\memory_service.py` (complexity: 1.00)
- `pyside_chat\features\memory\semantic_search.py` (complexity: 0.76)
- `pyside_chat\features\memory\semantic_search_fallback.py` (complexity: 0.76)
- `pyside_chat\features\memory\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\features\ollama

- **Files:** 3
- **Total Lines:** 859
- **Total Size:** 41.9 KB

**Largest Files:**
- `pyside_chat\features\ollama\ollama_service.py` (36.6 KB)
- `pyside_chat\features\ollama\ollama_chat.py` (5.4 KB)
- `pyside_chat\features\ollama\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\ollama\ollama_service.py` (complexity: 0.84)
- `pyside_chat\features\ollama\ollama_chat.py` (complexity: 0.69)
- `pyside_chat\features\ollama\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\features\personality

- **Files:** 3
- **Total Lines:** 555
- **Total Size:** 23.5 KB

**Largest Files:**
- `pyside_chat\features\personality\formatter.py` (12.1 KB)
- `pyside_chat\features\personality\loader.py` (11.4 KB)
- `pyside_chat\features\personality\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\personality\loader.py` (complexity: 0.75)
- `pyside_chat\features\personality\formatter.py` (complexity: 0.65)
- `pyside_chat\features\personality\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed business logic and data access - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'services' and 'data' subdirectories
- Simplify complex files by extracting helper functions

### pyside_chat\features\personality\services

- **Files:** 2
- **Total Lines:** 447
- **Total Size:** 20.5 KB

**Largest Files:**
- `pyside_chat\features\personality\services\personality_service.py` (20.5 KB)
- `pyside_chat\features\personality\services\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\personality\services\personality_service.py` (complexity: 0.84)
- `pyside_chat\features\personality\services\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\features\voice

- **Files:** 4
- **Total Lines:** 1,935
- **Total Size:** 85.4 KB

**Largest Files:**
- `pyside_chat\features\voice\voice_service.py` (55.1 KB)
- `pyside_chat\features\voice\voice_service_wrapper.py` (18.7 KB)
- `pyside_chat\features\voice\voice_service_manager.py` (11.6 KB)
- `pyside_chat\features\voice\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\voice\voice_service.py` (complexity: 0.84)
- `pyside_chat\features\voice\voice_service_wrapper.py` (complexity: 0.84)
- `pyside_chat\features\voice\voice_service_manager.py` (complexity: 0.80)
- `pyside_chat\features\voice\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\features\voice\audio

- **Files:** 2
- **Total Lines:** 318
- **Total Size:** 14.4 KB

**Largest Files:**
- `pyside_chat\features\voice\audio\recording_service.py` (14.4 KB)
- `pyside_chat\features\voice\audio\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\voice\audio\recording_service.py` (complexity: 0.78)
- `pyside_chat\features\voice\audio\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Simplify complex files by extracting helper functions

### pyside_chat\features\voice\orchestrator

- **Files:** 2
- **Total Lines:** 483
- **Total Size:** 20.7 KB

**Largest Files:**
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py` (20.5 KB)
- `pyside_chat\features\voice\orchestrator\__init__.py` (0.2 KB)

**Most Complex Files:**
- `pyside_chat\features\voice\orchestrator\voice_process_manager.py` (complexity: 0.81)
- `pyside_chat\features\voice\orchestrator\__init__.py` (complexity: 0.04)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\features\voice\stt

- **Files:** 2
- **Total Lines:** 154
- **Total Size:** 6.6 KB

**Largest Files:**
- `pyside_chat\features\voice\stt\stt_service.py` (6.6 KB)
- `pyside_chat\features\voice\stt\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\voice\stt\stt_service.py` (complexity: 0.66)
- `pyside_chat\features\voice\stt\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories

### pyside_chat\features\voice\tts

- **Files:** 5
- **Total Lines:** 1,832
- **Total Size:** 81.6 KB

**Largest Files:**
- `pyside_chat\features\voice\tts\coqui_tts_service.py` (47.8 KB)
- `pyside_chat\features\voice\tts\streaming_audio_player.py` (17.6 KB)
- `pyside_chat\features\voice\tts\tts_service.py` (9.6 KB)
- `pyside_chat\features\voice\tts\streaming_audio_worker.py` (6.6 KB)
- `pyside_chat\features\voice\tts\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\features\voice\tts\coqui_tts_service.py` (complexity: 0.84)
- `pyside_chat\features\voice\tts\tts_service.py` (complexity: 0.82)
- `pyside_chat\features\voice\tts\streaming_audio_player.py` (complexity: 0.71)
- `pyside_chat\features\voice\tts\streaming_audio_worker.py` (complexity: 0.63)
- `pyside_chat\features\voice\tts\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\ui

- **Files:** 2
- **Total Lines:** 255
- **Total Size:** 10.2 KB

**Largest Files:**
- `pyside_chat\ui\ui_manager.py` (10.1 KB)
- `pyside_chat\ui\__init__.py` (0.1 KB)

**Most Complex Files:**
- `pyside_chat\ui\ui_manager.py` (complexity: 0.75)
- `pyside_chat\ui\__init__.py` (complexity: 0.04)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Simplify complex files by extracting helper functions

### pyside_chat\ui\dialogs

- **Files:** 5
- **Total Lines:** 2,614
- **Total Size:** 105.8 KB

**Largest Files:**
- `pyside_chat\ui\dialogs\voice_settings_dialog.py` (63.0 KB)
- `pyside_chat\ui\dialogs\settings_dialog.py` (16.9 KB)
- `pyside_chat\ui\dialogs\coqui_model_dialog.py` (15.4 KB)
- `pyside_chat\ui\dialogs\error_dialog.py` (10.4 KB)
- `pyside_chat\ui\dialogs\__init__.py` (0.2 KB)

**Most Complex Files:**
- `pyside_chat\ui\dialogs\voice_settings_dialog.py` (complexity: 0.92)
- `pyside_chat\ui\dialogs\coqui_model_dialog.py` (complexity: 0.84)
- `pyside_chat\ui\dialogs\error_dialog.py` (complexity: 0.73)
- `pyside_chat\ui\dialogs\settings_dialog.py` (complexity: 0.67)
- `pyside_chat\ui\dialogs\__init__.py` (complexity: 0.03)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\ui\tabs

- **Files:** 5
- **Total Lines:** 2,213
- **Total Size:** 90.1 KB

**Largest Files:**
- `pyside_chat\ui\tabs\personality_tab.py` (45.4 KB)
- `pyside_chat\ui\tabs\memory_tab.py` (26.0 KB)
- `pyside_chat\ui\tabs\model_tab.py` (17.5 KB)
- `pyside_chat\ui\tabs\tab_styles.py` (1.1 KB)
- `pyside_chat\ui\tabs\__init__.py` (0.0 KB)

**Most Complex Files:**
- `pyside_chat\ui\tabs\memory_tab.py` (complexity: 0.84)
- `pyside_chat\ui\tabs\personality_tab.py` (complexity: 0.84)
- `pyside_chat\ui\tabs\model_tab.py` (complexity: 0.80)
- `pyside_chat\ui\tabs\tab_styles.py` (complexity: 0.26)
- `pyside_chat\ui\tabs\__init__.py` (complexity: 0.00)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\ui\tabs\chat_tab

- **Files:** 7
- **Total Lines:** 5,033
- **Total Size:** 225.3 KB

**Largest Files:**
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py` (80.9 KB)
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py` (66.3 KB)
- `pyside_chat\ui\tabs\chat_tab\eq_visualizer.py` (22.0 KB)
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py` (21.9 KB)
- `pyside_chat\ui\tabs\chat_tab\input_controls.py` (17.3 KB)

**Most Complex Files:**
- `pyside_chat\ui\tabs\chat_tab\chat_display.py` (complexity: 0.84)
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py` (complexity: 0.84)
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py` (complexity: 0.84)
- `pyside_chat\ui\tabs\chat_tab\input_controls.py` (complexity: 0.84)
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py` (complexity: 0.84)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains mixed business logic and data access - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Create separate 'services' and 'data' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\ui\themes

- **Files:** 3
- **Total Lines:** 622
- **Total Size:** 23.9 KB

**Largest Files:**
- `pyside_chat\ui\themes\message_formatter.py` (18.8 KB)
- `pyside_chat\ui\themes\styles.py` (5.1 KB)
- `pyside_chat\ui\themes\__init__.py` (0.1 KB)

**Most Complex Files:**
- `pyside_chat\ui\themes\message_formatter.py` (complexity: 0.73)
- `pyside_chat\ui\themes\styles.py` (complexity: 0.40)
- `pyside_chat\ui\themes\__init__.py` (complexity: 0.04)

**Issues:**
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Simplify complex files by extracting helper functions

### pyside_chat\ui\utils

- **Files:** 1
- **Total Lines:** 73
- **Total Size:** 2.7 KB

**Largest Files:**
- `pyside_chat\ui\utils\message_utils.py` (2.7 KB)

**Most Complex Files:**
- `pyside_chat\ui\utils\message_utils.py` (complexity: 0.44)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories

### pyside_chat\ui\visualizers

- **Files:** 2
- **Total Lines:** 681
- **Total Size:** 29.9 KB

**Largest Files:**
- `pyside_chat\ui\visualizers\eq_orchestrator.py` (29.8 KB)
- `pyside_chat\ui\visualizers\__init__.py` (0.1 KB)

**Most Complex Files:**
- `pyside_chat\ui\visualizers\eq_orchestrator.py` (complexity: 0.84)
- `pyside_chat\ui\visualizers\__init__.py` (complexity: 0.02)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains many large files - consider modularization
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Split large files into smaller, focused modules
- Simplify complex files by extracting helper functions

### pyside_chat\ui\visualizers\widgets

- **Files:** 5
- **Total Lines:** 759
- **Total Size:** 29.9 KB

**Largest Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py` (10.5 KB)
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py` (8.1 KB)
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py` (5.8 KB)
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py` (5.3 KB)
- `pyside_chat\ui\visualizers\widgets\__init__.py` (0.1 KB)

**Most Complex Files:**
- `pyside_chat\ui\visualizers\widgets\bar_eq_widget.py` (complexity: 0.72)
- `pyside_chat\ui\visualizers\widgets\circle_eq_widget.py` (complexity: 0.67)
- `pyside_chat\ui\visualizers\widgets\circular_net_eq_widget.py` (complexity: 0.65)
- `pyside_chat\ui\visualizers\widgets\circular_gradient_eq_widget.py` (complexity: 0.64)
- `pyside_chat\ui\visualizers\widgets\__init__.py` (complexity: 0.02)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Simplify complex files by extracting helper functions

### pyside_chat\ui\Widgets

- **Files:** 5
- **Total Lines:** 1,096
- **Total Size:** 43.5 KB

**Largest Files:**
- `pyside_chat\ui\Widgets\chat_navigation.py` (18.1 KB)
- `pyside_chat\ui\Widgets\complexity_widget.py` (9.9 KB)
- `pyside_chat\ui\Widgets\spellchecker_widget.py` (8.3 KB)
- `pyside_chat\ui\Widgets\message_editor.py` (7.2 KB)
- `pyside_chat\ui\Widgets\__init__.py` (0.1 KB)

**Most Complex Files:**
- `pyside_chat\ui\Widgets\chat_navigation.py` (complexity: 0.77)
- `pyside_chat\ui\Widgets\spellchecker_widget.py` (complexity: 0.73)
- `pyside_chat\ui\Widgets\complexity_widget.py` (complexity: 0.71)
- `pyside_chat\ui\Widgets\message_editor.py` (complexity: 0.64)
- `pyside_chat\ui\Widgets\__init__.py` (complexity: 0.04)

**Issues:**
- Directory contains mixed GUI and business logic - consider separation
- Directory contains many complex files - consider simplification

**Recommendations:**
- Create separate 'ui' and 'logic' subdirectories
- Simplify complex files by extracting helper functions

## 🏗️ Architectural Issues

- Found 5 very large files - consider breaking into modules
- Found 63 files with mixed GUI and business logic - consider MVC pattern
- Found 40 highly complex files - consider simplifying logic
- Found 174 duplicate functions across the codebase - consider consolidation

## 💡 General Recommendations

- Many large files detected - implement consistent file size limits
- Many complex files detected - implement complexity guidelines
- Consider implementing MVC or MVVM pattern for better separation
- Create consistent naming conventions for files and directories
- Implement dependency injection for better testability
- Consider using design patterns to reduce code duplication
- Create a shared utilities module for common functions
- Implement a common library for frequently used functionality

## 📋 Implementation Plan

### Phase 1: High Priority Files
1. Start with the largest and most complex files
2. Separate GUI code from business logic
3. Extract large functions into smaller, focused functions
4. Create dedicated modules for related functionality

### Phase 2: Medium Priority Files
1. Address files with mixed responsibilities
2. Implement consistent naming conventions
3. Reduce complexity through refactoring

### Phase 3: Low Priority Files
1. Apply minor improvements and optimizations
2. Standardize code style and formatting
3. Add documentation where needed

### Phase 4: Architectural Improvements
1. Implement design patterns (MVC, Repository, etc.)
2. Create proper separation of concerns
3. Improve testability and maintainability

### Phase 5: Duplicate Consolidation
1. Identify and consolidate duplicate functions into shared utilities
2. Create base classes for duplicate class functionality
3. Implement common libraries for frequently used code
4. Update imports to use consolidated modules


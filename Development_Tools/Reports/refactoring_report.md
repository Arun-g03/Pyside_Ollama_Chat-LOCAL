# 🔄 Duplicate Functions

These functions appear in multiple files and could be consolidated:




### `def cleanup(self)`
**Found in:** 14 files
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

### `def __new__(cls)`
**Found in:** 3 files
**Files:**
- `pyside_chat\app\service_manager.py`
- `pyside_chat\core\logging\logger.py`
- `pyside_chat\features\voice\voice_service_manager.py`

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

### `def _get_next_message_id(self) -> str`
**Found in:** 3 files
**Files:**
- `pyside_chat\core\utils\streaming_handler.py`
- `pyside_chat\features\chat\conversation_service.py`
- `pyside_chat\ui\tabs\chat_tab\chat_renderer.py`

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

### `def __del__(self)`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\tts\streaming_audio_player.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def _check_availability(self) -> bool`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def is_available(self) -> bool`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def is_initialized(self) -> bool`
**Found in:** 3 files
**Files:**
- `pyside_chat\features\voice\audio\recording_service.py`
- `pyside_chat\features\voice\stt\stt_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

### `def __init__(self,parent,config_manager)`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\dialogs\voice_settings_dialog.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`
- `pyside_chat\ui\tabs\chat_tab\voice_controls.py`

### `def safe_disconnect(signal,slot,logger)`
**Found in:** 3 files
**Files:**
- `pyside_chat\ui\tabs\memory_tab.py`
- `pyside_chat\ui\tabs\chat_tab\chat_tab.py`
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

### `def split_thoughts_and_answer(message)`
**Found in:** 2 files
**Files:**
- `test_message_saving_timing.py`
- `pyside_chat\ui\themes\message_formatter.py`

### `def test_persistent_thread_pool()`
**Found in:** 2 files
**Files:**
- `test_streaming_message_id_fix.py`
- `Tests\test_threading_fix.py`

### `def on_render_completed(self)`
**Found in:** 2 files
**Files:**
- `test_typewriter_fix.py`
- `pyside_chat\ui\tabs\chat_tab\chat_display.py`

### `def __init__(self,codebase_path)`
**Found in:** 2 files
**Files:**
- `Development_Tools\import_analyzer.py`
- `Development_Tools\migrate_to_shared_imports.py`

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

### `def _on_conversation_updated(self)`
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

### `def is_main_thread() -> bool`
**Found in:** 2 files
**Files:**
- `pyside_chat\core\shared_imports\pyside_imports.py`
- `pyside_chat\core\utils\threading_utils.py`

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

### `def get_instance()`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\voice_service.py`
- `pyside_chat\features\voice\tts\tts_service.py`

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

### `def stop_playback(self)`
**Found in:** 2 files
**Files:**
- `pyside_chat\features\voice\tts\streaming_audio_player.py`
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

### `def append_response_chunk(self,chunk,model_name,msg_id,chunk_index)`
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
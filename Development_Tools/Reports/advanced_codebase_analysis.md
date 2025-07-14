# Advanced Codebase Analysis Report

**Generated on:** 2025-07-14 20:36:32  
**Root Path:** pyside_chat  
**Total Files Analyzed:** 121

---

## 📊 Summary

- **Total Classes:** 113
- **Total Functions:** 1460
- **Total Files:** 121

### Files by Directory

- `Root/`: 1 files
- `app/`: 6 files
- `config/`: 2 files
- `core/`: 1 files
- `core\logging/`: 3 files
- `core\models/`: 3 files
- `core\shared_imports/`: 6 files
- `core\threading/`: 11 files
- `core\utils/`: 7 files
- `features/`: 1 files
- `features\chat/`: 3 files
- `features\chat\complexity_analyser/`: 1 files
- `features\chat\enhancers/`: 2 files
- `features\chat\summarization/`: 2 files
- `features\memory/`: 4 files
- `features\ollama/`: 3 files
- `features\personality/`: 3 files
- `features\personality\models/`: 4 files
- `features\personality\profiles/`: 1 files
- `features\personality\services/`: 2 files
- `features\user/`: 2 files
- `features\voice/`: 4 files
- `features\voice\audio/`: 2 files
- `features\voice\orchestrator/`: 2 files
- `features\voice\stt/`: 2 files
- `features\voice\tts/`: 4 files
- `startup/`: 5 files
- `ui/`: 2 files
- `ui\Widgets/`: 5 files
- `ui\dialogs/`: 5 files
- `ui\tabs/`: 5 files
- `ui\tabs\chat_tab/`: 7 files
- `ui\themes/`: 3 files
- `ui\utils/`: 1 files
- `ui\visualizers/`: 1 files
- `ui\visualizers\widgets/`: 5 files

---

## 🔗 Dependency Analysis

### Most Dependent Files (High In-Degree)

- `core\logging\logger`: 59 dependencies
- `config\config_manager`: 55 dependencies
- `core\threading\qthread_workers`: 52 dependencies
- `core\utils\threading_utils`: 52 dependencies
- `core\logging\helpers`: 51 dependencies
- `ui\tabs\memory_tab`: 51 dependencies
- `ui\dialogs\voice_settings_dialog`: 51 dependencies
- `ui\tabs\chat_tab\chat_tab`: 51 dependencies
- `app\event_bus`: 51 dependencies
- `ui\tabs\chat_tab\voice_controls`: 51 dependencies

### Most Influential Files (High Out-Degree)

- `features\chat\chat_controller.py`: 68 dependents
- `ui\dialogs\voice_settings_dialog.py`: 68 dependents
- `ui\tabs\chat_tab\chat_display.py`: 68 dependents
- `ui\tabs\chat_tab\chat_renderer.py`: 68 dependents
- `ui\tabs\chat_tab\voice_controls.py`: 68 dependents
- `app\main.py`: 67 dependents
- `app\threading_integration.py`: 67 dependents
- `core\logging\helpers.py`: 67 dependents
- `core\models\conversation_metadata.py`: 67 dependents
- `core\threading\persistent_thread_pool.py`: 67 dependents

### ✅ No Circular Dependencies Found


---

## 📁 File Structure

### `__init__.py`

---

### `app\__init__.py`

---

### `app\app_lifecycle.py`

**Classes:**
- `AppLifecycleManager` (line 18)

**Functions:**
- `__init__` (line 21)
- `initialize_application` (line 46)
- `handle_show_event` (line 74)
- `handle_close_event` (line 95)
- `show_initialization_error` (line 133)
- `show_ollama_connection_error` (line 142)
- `show_ollama_startup_dialog` (line 302)
- `check_ollama_connection` (line 309)
- `is_initialization_complete` (line 320)
- `set_ollama_error_shown` (line 324)
- `get_ollama_error_shown` (line 328)
- `reset_ollama_error_shown` (line 332)
- `force_show_ollama_error` (line 337)
- `test_error_dialog` (line 342)
- `get_available_models` (line 348)
- `send_test_message` (line 364)
- `_ensure_ollama_running` (line 406)
- `_is_ollama_installed` (line 442)
- `_find_ollama_executable` (line 468)
- `_start_ollama_background` (line 512)
- `_verify_ollama_installation` (line 635)
- `_stop_ollama_process` (line 679)
- `start_ollama_manually` (line 716)
- `stop_ollama_manually` (line 722)
- `is_ollama_running` (line 726)
- `get_ollama_process_info` (line 730)
- `set_auto_start_ollama` (line 743)
- `get_auto_start_ollama` (line 748)
- `_check_ollama_crash` (line 752)
- `_reset_ollama_restart_attempts` (line 809)
- `set_close_ollama_on_exit` (line 813)
- `get_close_ollama_on_exit` (line 818)
- `force_close_ollama` (line 822)
- `was_ollama_started_by_app` (line 827)
- `get_ollama_status_info` (line 831)
- `_show_custom_path_dialog` (line 849)
- `_validate_ollama_executable` (line 913)
- `set_custom_ollama_path` (line 945)
- `get_custom_ollama_path` (line 956)
- `clear_custom_ollama_path` (line 960)
- `get_ollama_path_info` (line 966)
- `wait_for_ollama` (line 567)

---

### `app\event_bus.py`

**Classes:**
- `EventBus` (line 13)

**Functions:**
- `__init__` (line 16)
- `setup_connections` (line 52)
- `_setup_chat_tab_retry` (line 104)
- `_retry_chat_tab_connection` (line 116)
- `_connect_menu_actions` (line 137)
- `_connect_chat_tab_signals` (line 179)
- `_on_status_updated` (line 229)
- `_on_error_occurred` (line 233)
- `_on_conversation_updated` (line 238)
- `_on_name_generation_requested` (line 244)
- `_on_models_updated` (line 269)
- `_on_message_sent` (line 283)
- `_send_to_ollama` (line 321)
- `_clean_messages_for_ollama` (line 374)
- `_start_worker_after_streaming_message` (line 386)
- `_create_worker_thread` (line 423)
- `_handle_chat_chunk` (line 470)
- `_handle_chat_progress` (line 499)
- `_handle_chat_finished` (line 507)
- `_handle_chat_error` (line 533)
- `_handle_chat_error_safe` (line 547)
- `stop_chat_streaming` (line 564)
- `_on_worker_progress` (line 632)
- `_on_worker_detailed_error` (line 589)
- `_on_worker_thread_finished` (line 604)
- `_on_worker_chunk` (line 609)
- `_update_chat_display_safe` (line 619)
- `_update_progress_safe` (line 644)
- `_on_worker_finished` (line 653)
- `_stop_streaming_safe` (line 675)
- `_on_worker_error` (line 685)
- `_handle_worker_error_safe` (line 698)
- `_on_tts_finished` (line 717)
- `_handle_tts_finished_delayed` (line 724)
- `_cleanup_worker_thread` (line 738)
- `_cleanup_worker_thread_once` (line 750)
- `_final_worker_cleanup` (line 774)
- `_on_message_received` (line 783)
- `_on_message_finished` (line 790)
- `_on_message_cancelled` (line 799)
- `_on_conversation_selected` (line 825)
- `_on_conversation_deleted` (line 833)
- `_on_conversation_renamed` (line 837)
- `_on_personality_changed` (line 859)
- `_on_model_operation_progress` (line 884)
- `_on_model_operation_error` (line 890)
- `_on_conversation_metadata_updated` (line 910)
- `_on_auto_save_completed` (line 922)
- `_on_new_conversation_requested` (line 938)
- `_on_new_conversation` (line 942)
- `_on_clear_chat` (line 959)
- `_on_save_chat` (line 970)
- `_on_load_chat` (line 976)
- `_on_open_settings` (line 982)
- `_create_chat_controller` (line 1009)
- `_setup_ui_with_new_services` (line 1021)
- `_on_refresh_models` (line 1027)
- `_on_refresh_personalities` (line 1059)
- `_on_show_about` (line 1073)
- `_on_delayed_model_update` (line 1077)
- `_check_ollama_connection` (line 1093)
- `_show_ollama_connection_error` (line 1098)
- `get_threading_status` (line 1146)
- `cleanup_on_exit` (line 1157)
- `reconnect_chat_tab_signals` (line 1198)
- `safe_disconnect` (line 187)

---

### `app\main.py`

**Classes:**
- `OllamaChat` (line 20)

**Functions:**
- `__init__` (line 23)
- `_setup_ui` (line 84)
- `_setup_connections` (line 118)
- `showEvent` (line 136)
- `closeEvent` (line 141)
- `show_ollama_connection_error` (line 145)
- `check_ollama_connection` (line 149)
- `get_service_manager` (line 154)
- `get_ui_manager` (line 158)
- `get_event_handler` (line 162)
- `get_lifecycle_manager` (line 166)
- `get_chat_controller` (line 170)

---

### `app\service_manager.py`

**Classes:**
- `ServiceManager` (line 20)

**Functions:**
- `__new__` (line 26)
- `__init__` (line 34)
- `get_instance` (line 62)
- `_initialize_services` (line 68)
- `reinitialize_services` (line 130)
- `get_ollama_service` (line 135)
- `get_conversation_service` (line 139)
- `get_enhancement_service` (line 143)
- `get_memory_service` (line 147)
- `get_summarization_service` (line 151)
- `get_conversation_manager` (line 155)
- `get_personality_service` (line 159)
- `get_voice_service` (line 163)
- `is_voice_service_initialized` (line 169)
- `is_memory_enabled` (line 175)
- `get_session_variables` (line 179)
- `cleanup` (line 183)
- `_initialize_voice_service` (line 207)

---

### `app\threading_integration.py`

**Classes:**
- `ThreadingIntegration` (line 14)
- `EventBusThreadingBridge` (line 141)

**Functions:**
- `__init__` (line 151)
- `start_chat_streaming` (line 211)
- `stop_chat_streaming` (line 232)
- `process_message_spell_check` (line 73)
- `process_message_formatting` (line 92)
- `process_file_operation` (line 111)
- `get_threading_status` (line 241)
- `_on_chunk_received` (line 163)
- `_on_progress_updated` (line 175)
- `_on_finished` (line 187)
- `_on_error` (line 199)

---

### `config\__init__.py`

---

### `config\config_manager.py`

**Classes:**
- `ConfigManager` (line 10)

**Functions:**
- `__init__` (line 13)
- `load_config` (line 17)
- `merge_configs` (line 65)
- `save_config` (line 75)
- `get` (line 88)
- `set` (line 101)
- `get_default_model` (line 118)
- `set_default_model` (line 122)
- `get_default_temperature` (line 126)
- `set_default_temperature` (line 130)
- `get_default_personality` (line 134)
- `set_default_personality` (line 138)
- `get_window_size` (line 142)
- `set_window_size` (line 147)
- `get_chat_settings` (line 151)
- `is_auto_save_enabled` (line 160)
- `set_auto_save_enabled` (line 164)
- `is_spellcheck_enabled` (line 168)
- `set_spellcheck_enabled` (line 172)
- `get_ollama_url` (line 176)
- `set_ollama_url` (line 181)
- `get_history_directory` (line 185)
- `set_history_directory` (line 189)
- `is_enhancement_enabled` (line 193)
- `set_enhancement_enabled` (line 197)
- `is_history_enabled` (line 201)
- `set_history_enabled` (line 205)
- `is_wordwrap_enabled` (line 209)
- `set_wordwrap_enabled` (line 213)
- `is_json_format_enabled` (line 217)
- `set_json_format_enabled` (line 221)
- `is_verbose_enabled` (line 225)
- `set_verbose_enabled` (line 229)
- `is_think_enabled` (line 233)
- `set_think_enabled` (line 237)
- `get_max_tokens` (line 241)
- `get_top_p` (line 244)
- `get_frequency_penalty` (line 247)
- `get_presence_penalty` (line 250)
- `get_max_context_messages` (line 254)
- `set_max_context_messages` (line 258)
- `get_voice_settings` (line 262)
- `set_voice_settings` (line 279)

---

### `core\__init__.py`

---

### `core\logging\__init__.py`

---

### `core\logging\helpers.py`

**Classes:**
- `LoggingHelpers` (line 21)
- `ThreadMonitor` (line 209)
- `ThreadSafeLogger` (line 372)

**Functions:**
- `get_thread_monitor` (line 419)
- `cleanup_thread_monitor` (line 426)
- `log_exception_with_context` (line 25)
- `log_warning_with_context` (line 32)
- `log_info_with_context` (line 38)
- `log_debug` (line 44)
- `log_error` (line 49)
- `log_network_request` (line 54)
- `log_file_operation` (line 64)
- `log_audio_operation` (line 72)
- `log_memory_operation` (line 80)
- `log_ui_operation` (line 88)
- `log_performance_metric` (line 96)
- `log_json_parsing_error` (line 102)
- `log_json_parsing_success` (line 108)
- `log_critical_error` (line 113)
- `log_fact_extraction_start` (line 120)
- `log_fact_extraction_end` (line 125)
- `log_fact_extraction_result` (line 130)
- `log_fact_processing` (line 135)
- `log_fact_storage_start` (line 140)
- `log_fact_storage_end` (line 145)
- `log_fact_storage_summary` (line 150)
- `log_fact_skipped` (line 155)
- `log_memory_result` (line 160)
- `log_memory_ltm_status` (line 165)
- `log_llm_call` (line 170)
- `log_llm_response` (line 175)
- `log_json_extraction` (line 180)
- `log_message_sent` (line 185)
- `log_message_sent_end` (line 190)
- `log_conversation_detection` (line 195)
- `log_service_initialization` (line 200)
- `__init__` (line 216)
- `register_thread` (line 224)
- `unregister_thread` (line 254)
- `_on_thread_started` (line 274)
- `_on_thread_finished` (line 286)
- `get_thread_info` (line 300)
- `get_all_threads` (line 304)
- `get_thread_history` (line 308)
- `get_thread_stats` (line 312)
- `cleanup` (line 352)
- `log_thread_context` (line 376)
- `log_thread_safety_check` (line 394)
- `log_thread_operation` (line 409)

---

### `core\logging\logger.py`

**Classes:**
- `PrintOnLogMixin` (line 39)
- `ThreadInfoFormatter` (line 68)
- `CustomLogger` (line 93)
- `PrintLogger` (line 180)
- `DummyLogger` (line 146)

**Functions:**
- `_sanitize_filename` (line 21)
- `strip_emojis` (line 24)
- `_print` (line 40)
- `info` (line 147)
- `debug` (line 148)
- `warning` (line 149)
- `error` (line 150)
- `critical` (line 151)
- `format` (line 71)
- `_check_config_for_logging` (line 112)
- `__new__` (line 124)
- `set_logging_enabled` (line 131)
- `_clear_log_file` (line 135)
- `get_logger` (line 142)
- `_filter_non_ascii` (line 206)

---

### `core\models\__init__.py`

---

### `core\models\base_model.py`

**Classes:**
- `BaseModel` (line 8)

**Functions:**
- `to_dict` (line 12)
- `from_dict` (line 18)

---

### `core\models\conversation_metadata.py`

**Classes:**
- `ConversationMetadata` (line 18)
- `ConversationManager` (line 129)

**Functions:**
- `__post_init__` (line 30)
- `update_timestamp` (line 37)
- `update_message_count` (line 41)
- `update_model` (line 46)
- `update_personality` (line 51)
- `update_ai_generated_name` (line 56)
- `to_dict` (line 61)
- `from_dict` (line 74)
- `reset` (line 86)
- `get_formatted_created_time` (line 96)
- `get_formatted_modified_time` (line 106)
- `get_display_info` (line 116)
- `get_display_name` (line 124)
- `__init__` (line 135)
- `save_conversation` (line 143)
- `update_conversation_name` (line 180)
- `_create_safe_filename` (line 252)
- `load_conversation` (line 292)
- `auto_save_conversation` (line 324)
- `list_conversations` (line 398)
- `delete_conversation` (line 427)
- `rename_conversation` (line 444)
- `clear_current_conversation` (line 469)
- `get_current_metadata` (line 474)
- `set_auto_save_enabled` (line 478)
- `find_blank_conversation` (line 483)

---

### `core\shared_imports\__init__.py`

---

### `core\shared_imports\audio_imports.py`

---

### `core\shared_imports\json_time_imports.py`

---

### `core\shared_imports\os_sys_imports.py`

---

### `core\shared_imports\pyside_imports.py`

**Functions:**
- `is_main_thread` (line 211)
- `safe_ui_update` (line 217)
- `safe_signal_connect` (line 232)
- `safe_signal_disconnect` (line 249)
- `create_timer` (line 269)
- `create_message_box` (line 276)
- `create_button` (line 290)
- `create_label` (line 296)
- `create_text_edit` (line 302)
- `create_line_edit` (line 309)
- `create_combo_box` (line 316)
- `create_progress_bar` (line 323)
- `create_vertical_layout` (line 334)
- `create_horizontal_layout` (line 341)
- `create_grid_layout` (line 348)
- `create_form_layout` (line 355)

---

### `core\shared_imports\shared_imports.py`

---

### `core\threading\__init__.py`

**Functions:**
- `shutdown_global_threading_service` (line 41)
- `shutdown_global_persistent_thread_pool` (line 53)

---

### `core\threading\persistent_thread_config.py`

**Functions:**
- `get_persistent_thread_config` (line 171)
- `validate_persistent_thread_config` (line 191)
- `get_config_summary` (line 231)

---

### `core\threading\persistent_thread_pool.py`

**Classes:**
- `PersistentThreadPool` (line 19)

**Functions:**
- `get_global_persistent_thread_pool` (line 407)
- `shutdown_global_persistent_thread_pool` (line 418)
- `__init__` (line 34)
- `initialize_pool` (line 95)
- `get_thread` (line 130)
- `return_thread` (line 220)
- `_create_idle_thread` (line 260)
- `_create_active_thread` (line 285)
- `_cleanup_idle_threads` (line 313)
- `get_pool_status` (line 344)
- `shutdown` (line 366)

---

### `core\threading\qrunnable_tasks.py`

**Classes:**
- `StreamingUpdateTask` (line 20)
- `MessageProcessingTask` (line 83)
- `FileProcessingTask` (line 220)
- `DataProcessingTask` (line 332)
- `CalculationTask` (line 578)

**Functions:**
- `__init__` (line 591)
- `run` (line 600)
- `_execute_target` (line 63)
- `_spell_check_message` (line 129)
- `_format_message` (line 173)
- `_analyze_sentiment` (line 194)
- `_read_file` (line 267)
- `_write_file` (line 286)
- `_process_file` (line 301)
- `_handle_model_operation` (line 381)
- `_calculate_data` (line 477)
- `_transform_data` (line 505)
- `_analyze_data` (line 532)
- `_count_nested_levels` (line 564)
- `_calculate_fibonacci` (line 624)
- `_calculate_prime_factors` (line 649)
- `_calculate_statistics` (line 681)

---

### `core\threading\qthread_workers.py`

**Classes:**
- `StreamingWorker` (line 20)
- `ChatStreamingWorker` (line 149)
- `AudioStreamingWorker` (line 306)
- `MonitoringWorker` (line 419)

**Functions:**
- `__init__` (line 38)
- `_log_thread_info` (line 49)
- `configure_streaming` (line 160)
- `reset_state` (line 81)
- `is_running` (line 103)
- `start_streaming` (line 107)
- `stop` (line 130)
- `_stream_operation` (line 473)
- `configure_audio_streaming` (line 317)
- `start_audio_streaming` (line 345)
- `configure_monitoring` (line 433)
- `start_monitoring` (line 458)

---

### `core\threading\thread_calculator.py`

**Classes:**
- `ThreadRecommendations` (line 26)
- `ThreadCalculator` (line 53)

**Functions:**
- `get_thread_recommendations` (line 395)
- `get_pool_thread_count` (line 420)
- `analyze_system` (line 432)
- `__init__` (line 56)
- `get_system_info` (line 59)
- `calculate_thread_recommendations` (line 120)
- `_calculate_recommendations` (line 190)
- `_calculate_memory_safe_threads` (line 301)
- `get_recommendations_for_pool` (line 320)
- `print_system_analysis` (line 345)

---

### `core\threading\thread_calculator_examples.py`

**Classes:**
- `DummyWorker` (line 60)

**Functions:**
- `example_thread_pool_manager` (line 21)
- `example_persistent_thread_pool` (line 42)
- `example_streaming_configuration` (line 67)
- `example_memory_optimization` (line 87)
- `example_dynamic_adjustment` (line 109)
- `main` (line 141)

---

### `core\threading\thread_monitor.py`

**Classes:**
- `ThreadMonitor` (line 19)

**Functions:**
- `get_global_thread_monitor` (line 499)
- `shutdown_global_thread_monitor` (line 515)
- `__init__` (line 37)
- `register_thread` (line 62)
- `unregister_thread` (line 107)
- `record_thread_error` (line 138)
- `get_thread_info` (line 173)
- `get_all_threads_info` (line 202)
- `get_resource_usage` (line 221)
- `cleanup_old_history` (line 257)
- `_on_thread_started` (line 285)
- `_on_thread_finished` (line 298)
- `_update_monitoring` (line 325)
- `generate_report` (line 339)
- `shutdown` (line 384)
- `check_thread_safety` (line 405)
- `force_thread_cleanup` (line 439)
- `get_running_threads` (line 475)

---

### `core\threading\thread_pool_manager.py`

**Classes:**
- `ThreadPoolManager` (line 22)

**Functions:**
- `get_global_thread_pool_manager` (line 443)
- `shutdown_global_thread_pool_manager` (line 462)
- `__init__` (line 39)
- `start_task` (line 74)
- `wait_for_task` (line 138)
- `wait_for_all_tasks` (line 166)
- `cancel_task` (line 193)
- `cancel_all_tasks` (line 229)
- `get_pool_status` (line 250)
- `get_task_info` (line 275)
- `cleanup_old_tasks` (line 309)
- `_update_pool_status` (line 337)
- `on_task_completed` (line 357)
- `on_task_failed` (line 385)
- `shutdown` (line 415)

---

### `core\threading\threading_service.py`

**Classes:**
- `ThreadingService` (line 27)

**Functions:**
- `get_global_threading_service` (line 638)
- `shutdown_global_threading_service` (line 649)
- `__init__` (line 44)
- `_initialize_persistent_pools` (line 102)
- `start_chat_streaming` (line 179)
- `stop_chat_streaming` (line 244)
- `start_audio_streaming` (line 273)
- `stop_audio_streaming` (line 320)
- `start_monitoring` (line 339)
- `stop_monitoring` (line 387)
- `_on_chat_chunk_received` (line 407)
- `_on_chat_progress_updated` (line 416)
- `_on_chat_streaming_finished` (line 423)
- `_on_chat_streaming_error` (line 437)
- `_on_audio_chunk_received` (line 451)
- `_on_audio_streaming_finished` (line 459)
- `_on_audio_streaming_error` (line 472)
- `_on_resource_updated` (line 485)
- `_on_alert_triggered` (line 493)
- `_on_monitoring_finished` (line 500)
- `_on_monitoring_error` (line 513)
- `process_message` (line 527)
- `process_file` (line 542)
- `process_data` (line 557)
- `get_threading_status` (line 572)
- `cleanup` (line 606)

---

### `core\threading\usage_examples.py`

**Classes:**
- `ChatApplicationExample` (line 16)

**Functions:**
- `demonstrate_threading_usage` (line 388)
- `__init__` (line 25)
- `start_chat_streaming` (line 40)
- `_on_chat_streaming_thread_finished` (line 113)
- `stop_chat_streaming` (line 135)
- `process_message_spell_check` (line 158)
- `process_message_formatting` (line 191)
- `process_file_operation` (line 218)
- `_on_chat_chunk_received` (line 249)
- `_on_chat_progress_updated` (line 258)
- `_on_chat_streaming_finished` (line 267)
- `_on_chat_streaming_error` (line 276)
- `on_message_processed` (line 287)
- `on_message_processing_error` (line 309)
- `on_file_processed` (line 318)
- `on_file_processing_error` (line 333)
- `get_threading_status` (line 342)
- `cleanup` (line 367)

---

### `core\utils\__init__.py`

---

### `core\utils\error_handler.py`

**Classes:**
- `ErrorHandler` (line 22)

**Functions:**
- `error_context` (line 231)
- `network_error_context` (line 254)
- `file_operation_context` (line 271)
- `audio_operation_context` (line 288)
- `memory_operation_context` (line 304)
- `ui_operation_context` (line 321)
- `safe_json_parse` (line 337)
- `safe_file_read` (line 358)
- `safe_file_write` (line 378)
- `safe_network_request` (line 402)
- `validate_input` (line 424)
- `cleanup_resources` (line 449)
- `handle_critical_error` (line 468)
- `safe_execute` (line 26)
- `retry_on_failure` (line 51)
- `handle_network_errors` (line 93)
- `handle_file_operations` (line 127)
- `handle_audio_operations` (line 161)
- `handle_memory_operations` (line 184)
- `handle_ui_operations` (line 207)
- `wrapper` (line 218)

---

### `core\utils\internet_checker.py`

**Classes:**
- `InternetConnectionTester` (line 17)

**Functions:**
- `test_internet_connection` (line 127)
- `test_internet_connection_detailed` (line 141)
- `is_online` (line 155)
- `check_internet` (line 166)
- `__init__` (line 24)
- `test_socket_connection` (line 43)
- `test_http_connection` (line 60)
- `test_connection` (line 77)
- `test_connection_with_details` (line 96)

---

### `core\utils\prompts.py`

**Classes:**
- `PromptTemplates` (line 11)
- `PromptFormatter` (line 85)

**Functions:**
- `format_fact_extraction_prompt` (line 89)
- `format_auto_model_selection_info` (line 96)
- `format_conversation_status` (line 101)
- `format_memory_status` (line 107)
- `format_error_message` (line 112)
- `format_status_message` (line 118)
- `get_menu_text` (line 124)

---

### `core\utils\streaming_handler.py`

**Classes:**
- `StreamingHandler` (line 15)

**Functions:**
- `__init__` (line 21)
- `_get_next_message_id` (line 43)
- `set_render_callback` (line 48)
- `sync_messages_to_renderer` (line 52)
- `_request_render` (line 57)
- `_flush_stream_buffer` (line 66)
- `append_message` (line 83)
- `edit_message` (line 104)
- `get_message_by_id` (line 119)
- `get_editable_messages` (line 126)
- `get_messages` (line 139)
- `start_streaming_message` (line 143)
- `_process_typewriter_chunk` (line 158)
- `update_streaming_message` (line 180)
- `finalize_streaming_message` (line 195)
- `update_last_system_switch` (line 212)
- `remove_streaming_placeholder` (line 228)
- `clear_messages` (line 245)
- `cleanup` (line 250)

---

### `core\utils\threading_audit.py`

**Classes:**
- `ThreadSafetyAuditor` (line 18)

**Functions:**
- `run_thread_safety_audit` (line 283)
- `quick_thread_check` (line 295)
- `__init__` (line 26)
- `analyze_current_threads` (line 33)
- `detect_cross_thread_ui_operations` (line 103)
- `check_thread_safety_patterns` (line 126)
- `_get_thread_breakdown` (line 159)
- `generate_recommendations` (line 167)
- `run_full_analysis` (line 202)
- `generate_report` (line 218)
- `save_report` (line 272)

---

### `core\utils\threading_utils.py`

**Classes:**
- `ThreadSafeCallback` (line 262)

**Functions:**
- `is_main_thread` (line 13)
- `safe_ui_update` (line 18)
- `safe_ui_update_with_callback` (line 44)
- `safe_button_update` (line 78)
- `safe_widget_update` (line 117)
- `safe_process_events_alternative` (line 144)
- `safe_force_update` (line 160)
- `safe_connect_signal` (line 186)
- `safe_signal_connect` (line 201)
- `safe_signal_disconnect` (line 213)
- `safe_disconnect_signal` (line 224)
- `create_thread_safe_callback` (line 238)
- `ensure_main_thread` (line 283)
- `log_thread_info` (line 303)
- `safe_log_thread_info` (line 322)
- `safe_disconnect` (line 341)
- `safe_emit_signal` (line 358)
- `safe_set_property` (line 377)
- `safe_call_method` (line 403)
- `safe_show_widget` (line 432)
- `safe_hide_widget` (line 442)
- `safe_enable_widget` (line 452)
- `safe_set_text` (line 463)
- `safe_set_style` (line 474)
- `thread_safe_callback` (line 250)
- `__init__` (line 267)
- `__call__` (line 272)
- `wrapper` (line 293)
- `ui_update_with_callback` (line 64)
- `update_button` (line 100)
- `update_widget` (line 133)
- `force_update` (line 174)
- `set_property` (line 392)
- `call_method` (line 420)

---

### `features\__init__.py`

---

### `features\chat\__init__.py`

---

### `features\chat\chat_controller.py`

**Classes:**
- `ChatController` (line 41)

**Functions:**
- `remove_emojis` (line 25)
- `__init__` (line 52)
- `is_memory_active` (line 74)
- `process_user_message` (line 78)
- `_handle_memory_operations` (line 127)
- `_extract_and_store_facts` (line 140)
- `_extract_facts_with_llm` (line 163)
- `_store_extracted_facts` (line 223)
- `_send_to_ollama` (line 248)
- `_detect_new_conversation` (line 273)
- `_build_context` (line 287)
- `_select_model` (line 293)
- `accumulate_assistant_response` (line 314)
- `clear_pending_assistant_response` (line 323)
- `start_streaming_response` (line 326)
- `finalize_streaming_response` (line 332)
- `handle_ai_response` (line 341)
- `_trigger_tts_for_response` (line 396)
- `set_chat_tab_reference` (line 429)
- `get_ai_name` (line 433)
- `_trigger_name_generation` (line 442)
- `start_new_conversation` (line 449)
- `clear_conversation` (line 496)
- `load_conversation` (line 502)
- `delete_conversation` (line 529)
- `rename_conversation` (line 542)
- `reset_ai_response_guard` (line 556)

---

### `features\chat\complexity_analyser\complexity_analyzer.py`

**Classes:**
- `ComplexityLevel` (line 10)
- `ComplexityMetrics` (line 18)
- `RequestComplexityAnalyzer` (line 32)

**Functions:**
- `__init__` (line 35)
- `analyze_complexity` (line 115)
- `_estimate_tokens` (line 181)
- `_analyze_reasoning_depth` (line 187)
- `_analyze_knowledge_breadth` (line 223)
- `_analyze_ambiguity` (line 248)
- `_count_constraints` (line 267)
- `_analyze_context_dependency` (line 282)
- `_analyze_output_complexity` (line 302)
- `_determine_complexity_level` (line 322)
- `_generate_recommendations` (line 333)
- `get_model_recommendation` (line 375)
- `format_complexity_report` (line 396)
- `extract_size` (line 378)

---

### `features\chat\conversation_service.py`

**Classes:**
- `ConversationService` (line 15)

**Functions:**
- `__init__` (line 21)
- `set_memory_service` (line 34)
- `set_conversation_manager` (line 38)
- `_get_next_message_id` (line 42)
- `add_message` (line 47)
- `start_streaming_message` (line 75)
- `update_streaming_message` (line 93)
- `finalize_streaming_message` (line 135)
- `get_streaming_message_id` (line 193)
- `get_streaming_message_with_content` (line 197)
- `get_message_by_id` (line 204)
- `update_message_by_id` (line 211)
- `_add_to_memory` (line 220)
- `get_messages` (line 255)
- `get_context_messages` (line 266)
- `load_conversation` (line 273)
- `clear_conversation` (line 366)

---

### `features\chat\enhancers\__init__.py`

---

### `features\chat\enhancers\enhancement_service.py`

**Classes:**
- `EnhancementService` (line 8)

**Functions:**
- `__init__` (line 11)
- `should_enhance_response` (line 14)
- `detect_follow_up_question` (line 25)
- `generate_enhanced_response` (line 34)

---

### `features\chat\summarization\__init__.py`

---

### `features\chat\summarization\summarization_service.py`

**Classes:**
- `SummarizationService` (line 18)

**Functions:**
- `__init__` (line 25)
- `generate_chat_name` (line 31)
- `_create_summarization_prompt` (line 120)
- `_clean_generated_name` (line 145)
- `_has_enough_substance` (line 218)
- `_ai_evaluate_conversation_quality` (line 235)
- `_fallback_quality_check` (line 311)
- `_ai_evaluate_name_quality` (line 340)
- `set_summarization_model` (line 412)
- `set_min_messages_threshold` (line 416)

---

### `features\memory\__init__.py`

---

### `features\memory\memory_service.py`

**Classes:**
- `MemoryEntry` (line 24)
- `LongTermMemoryEntry` (line 38)
- `MemoryClassifier` (line 58)
- `PronounNormalizer` (line 165)
- `MemoryRetriever` (line 254)
- `ShortTermMemoryService` (line 327)
- `LongTermMemoryService` (line 381)
- `MemoryService` (line 443)

**Functions:**
- `__post_init__` (line 51)
- `classify_message` (line 96)
- `normalize_pronouns` (line 195)
- `should_normalize` (line 230)
- `calculate_relevance` (line 258)
- `get_relevant_memories` (line 565)
- `__init__` (line 449)
- `_load` (line 389)
- `add_message` (line 885)
- `get_messages` (line 359)
- `clear` (line 947)
- `_save` (line 424)
- `add_entry` (line 404)
- `get_entries` (line 414)
- `update_access_stats` (line 434)
- `_load_memory` (line 478)
- `_save_memory` (line 486)
- `_on_embeddings_updated` (line 494)
- `add_memory` (line 502)
- `add_summary` (line 547)
- `intelligent_add_message` (line 618)
- `extract_facts_from_message` (line 679)
- `get_user_info` (line 708)
- `get_user_name` (line 723)
- `get_context_messages` (line 732)
- `summarize_conversation` (line 759)
- `clear_memory` (line 776)
- `_verify_memory_files_cleared` (line 801)
- `delete_memory` (line 820)
- `get_memory_stats` (line 831)
- `add_fact` (line 892)
- `set_max_context_messages` (line 909)
- `search_memories` (line 918)
- `cleanup_memory_entries` (line 954)

---

### `features\memory\semantic_search.py`

**Classes:**
- `VectorizedMemory` (line 29)
- `SemanticSearchService` (line 40)

**Functions:**
- `__init__` (line 46)
- `_init_model` (line 64)
- `_load_embeddings` (line 82)
- `_save_embeddings` (line 116)
- `add_memory` (line 150)
- `remove_memory` (line 204)
- `search_semantic` (line 233)
- `search_hybrid` (line 286)
- `update_memory_importance` (line 365)
- `get_memory_stats` (line 392)
- `clear_all` (line 439)
- `is_ready` (line 466)

---

### `features\memory\semantic_search_fallback.py`

**Classes:**
- `SimpleMemory` (line 18)
- `SemanticSearchFallback` (line 28)

**Functions:**
- `__init__` (line 34)
- `_load_memories` (line 49)
- `_save_memories` (line 77)
- `add_memory` (line 105)
- `remove_memory` (line 149)
- `_calculate_keyword_similarity` (line 177)
- `search_semantic` (line 215)
- `search_hybrid` (line 263)
- `update_memory_importance` (line 269)
- `get_memory_stats` (line 295)
- `clear_all` (line 343)
- `is_ready` (line 367)

---

### `features\ollama\__init__.py`

---

### `features\ollama\ollama_chat.py`

**Classes:**
- `OllamaChat` (line 20)

**Functions:**
- `__init__` (line 23)
- `_setup_ui` (line 79)
- `showEvent` (line 107)
- `closeEvent` (line 112)
- `show_ollama_connection_error` (line 116)
- `check_ollama_connection` (line 120)
- `get_service_manager` (line 125)
- `get_ui_manager` (line 129)
- `get_event_handler` (line 133)
- `get_lifecycle_manager` (line 137)
- `get_chat_controller` (line 141)

---

### `features\ollama\ollama_service.py`

**Classes:**
- `OllamaService` (line 25)

**Functions:**
- `__init__` (line 35)
- `get_models` (line 66)
- `_get_models_with_library` (line 73)
- `_get_models_with_requests` (line 133)
- `test_connection` (line 182)
- `send_chat_message` (line 211)
- `_send_chat_message_with_library` (line 233)
- `_send_chat_message_with_requests` (line 314)
- `pull_model` (line 412)
- `_pull_model_thread` (line 440)
- `remove_model` (line 489)
- `_remove_model_thread` (line 517)
- `update_model` (line 566)
- `_update_model_thread` (line 594)
- `_extract_system_prompt` (line 643)
- `_build_session_commands` (line 652)
- `cancel_request` (line 668)
- `reset_cancellation` (line 674)
- `is_connected` (line 679)
- `cleanup` (line 683)

---

### `features\personality\__init__.py`

---

### `features\personality\formatter.py`

**Classes:**
- `PersonalityFormatter` (line 13)

**Functions:**
- `format_prompt_with_personality` (line 17)
- `build_comprehensive_system_prompt` (line 53)
- `get_system_prompt` (line 140)
- `get_personality_info` (line 147)
- `validate_personality_data` (line 173)
- `format_personality_summary` (line 204)
- `create_personality_template` (line 244)

---

### `features\personality\loader.py`

**Classes:**
- `PersonalityLoader` (line 21)

**Functions:**
- `__init__` (line 24)
- `find_personality_files` (line 36)
- `extract_personality_name` (line 54)
- `load_personality_from_file` (line 69)
- `load_all_personalities` (line 79)
- `save_personality_to_file` (line 91)
- `find_personality_file_by_name` (line 118)
- `delete_personality_file` (line 133)
- `create_personality_data` (line 145)
- `validate_personality_file` (line 163)
- `backup_personality` (line 182)
- `restore_personality_from_backup` (line 210)
- `get_personality_file_info` (line 241)
- `list_backup_files` (line 261)

---

### `features\personality\models\__init__.py`

---

### `features\personality\models\personality_model.py`

**Classes:**
- `PersonalityModel` (line 15)

**Functions:**
- `__init__` (line 23)
- `service` (line 38)
- `_initialize_default_personalities` (line 42)
- `_find_personality_files` (line 49)
- `_extract_personality_name` (line 53)
- `_load_custom_personalities` (line 57)
- `_find_personality_file_by_name` (line 62)
- `save_custom_personality` (line 66)
- `get_personality_loader` (line 72)
- `get_personality_formatter` (line 76)
- `get_system_personalities` (line 80)
- `get_custom_personalities` (line 84)

---

### `features\personality\models\personality_pronouns.py`

**Classes:**
- `PersonalityPronouns` (line 14)

**Functions:**
- `get_user_titles` (line 37)
- `get_primary_title` (line 53)
- `get_random_title` (line 58)
- `get_formal_title` (line 63)
- `get_pronoun_guide` (line 80)
- `get_user_address` (line 123)
- `format_user_reference` (line 134)

---

### `features\personality\models\personality_types.py`

**Classes:**
- `PersonalityType` (line 13)
- `PersonalityTraits` (line 28)
- `PersonalityConfig` (line 46)
- `PersonalityMetadata` (line 57)
- `PersonalityPrompt` (line 72)

**Functions:**
- `__post_init__` (line 66)

---

### `features\personality\profiles\__init__.py`

---

### `features\personality\services\__init__.py`

---

### `features\personality\services\personality_service.py`

**Classes:**
- `PersonalityService` (line 22)

**Functions:**
- `__init__` (line 25)
- `_initialize_personalities` (line 38)
- `is_system_personality` (line 63)
- `is_custom_personality` (line 72)
- `get_system_personalities` (line 76)
- `get_custom_personalities` (line 84)
- `get_available_personalities` (line 92)
- `get_personality` (line 96)
- `set_current_personality` (line 100)
- `get_current_personality` (line 107)
- `create_custom_personality` (line 113)
- `delete_custom_personality` (line 142)
- `update_custom_personality` (line 173)
- `refresh_personalities` (line 198)
- `format_prompt_with_personality` (line 219)
- `get_system_prompt` (line 238)
- `get_personality_info` (line 255)
- `get_personality_config` (line 260)
- `update_personality_metadata` (line 271)
- `build_comprehensive_system_prompt` (line 295)
- `get_user_context_messages` (line 306)
- `get_personality_categories` (line 374)
- `get_personalities_by_category` (line 385)
- `get_personalities_by_folder` (line 398)
- `search_personalities` (line 408)
- `get_selected_model` (line 437)
- `get_ai_name` (line 441)
- `get_temperature` (line 448)

---

### `features\user\__init__.py`

---

### `features\user\user_profile_service.py`

**Classes:**
- `UserProfileService` (line 7)

**Functions:**
- `__init__` (line 10)
- `get_user_profile` (line 13)
- `update_user_profile` (line 17)

---

### `features\voice\__init__.py`

---

### `features\voice\audio\__init__.py`

---

### `features\voice\audio\recording_service.py`

**Classes:**
- `RecordingService` (line 13)

**Functions:**
- `__init__` (line 23)
- `__del__` (line 52)
- `_check_availability` (line 58)
- `is_available` (line 73)
- `is_initialized` (line 76)
- `start_recording` (line 80)
- `_record_audio` (line 100)
- `_calculate_audio_level` (line 219)
- `audio_level_to_db` (line 233)
- `get_current_audio_level` (line 244)
- `set_audio_gate_enabled` (line 247)
- `set_speech_detection_parameters` (line 254)
- `get_speech_detection_parameters` (line 264)
- `cleanup` (line 273)
- `stop_recording` (line 282)
- `calculate_eq_bars_pcm` (line 125)

---

### `features\voice\orchestrator\__init__.py`

---

### `features\voice\orchestrator\voice_process_manager.py`

**Classes:**
- `VoiceProcessManager` (line 20)
- `VoiceProcessMonitor` (line 273)

**Functions:**
- `_voice_process_worker` (line 350)
- `create_voice_process_manager` (line 450)
- `stop_voice_process_manager` (line 467)
- `__init__` (line 279)
- `start_voice_process` (line 48)
- `stop_voice_process` (line 105)
- `send_command` (line 185)
- `_handle_response` (line 202)
- `_handle_monitor_error` (line 242)
- `is_process_running` (line 250)
- `get_process_info` (line 256)
- `run` (line 290)
- `stop` (line 325)
- `get_stats` (line 340)

---

### `features\voice\stt\__init__.py`

---

### `features\voice\stt\stt_service.py`

**Classes:**
- `STTService` (line 10)

**Functions:**
- `__init__` (line 16)
- `_check_availability` (line 22)
- `is_available` (line 44)
- `is_initialized` (line 47)
- `convert_audio_to_text` (line 51)
- `_convert_with_vosk` (line 58)
- `update_api` (line 91)
- `process_audio_file` (line 95)

---

### `features\voice\tts\__init__.py`

---

### `features\voice\tts\streaming_audio_player.py`

**Classes:**
- `StreamingAudioPlayer` (line 14)

**Functions:**
- `__init__` (line 23)
- `__del__` (line 41)
- `run` (line 47)
- `_process_audio_chunk` (line 155)
- `set_volume` (line 278)
- `add_audio_chunk` (line 282)
- `end_stream` (line 293)
- `stop_playback` (line 301)
- `cleanup` (line 329)
- `calculate_eq_bars` (line 192)
- `terminate_pyaudio` (line 353)

---

### `features\voice\tts\streaming_audio_worker.py`

**Classes:**
- `StreamingAudioWorker` (line 13)

**Functions:**
- `__init__` (line 20)
- `run` (line 27)
- `_split_text_into_sentences` (line 65)
- `_generate_audio_chunk` (line 84)
- `_adjust_audio_speed` (line 127)
- `stop` (line 146)

---

### `features\voice\tts\tts_service.py`

**Classes:**
- `TTSService` (line 17)

**Functions:**
- `get_instance` (line 34)
- `__init__` (line 40)
- `_check_availability` (line 66)
- `is_available` (line 75)
- `is_initialized` (line 78)
- `speak_text` (line 82)
- `speak_text_streaming` (line 97)
- `speak_text_non_streaming` (line 113)
- `_speak_with_espeak` (line 130)
- `_simulate_tts_finished` (line 153)
- `stop_playback` (line 156)
- `update_api` (line 165)
- `update_voice` (line 173)
- `update_speed` (line 181)
- `is_coqui_available` (line 190)
- `get_coqui_models` (line 194)
- `get_coqui_voices` (line 200)
- `get_coqui_model_info` (line 206)
- `load_coqui_model` (line 212)
- `set_coqui_model` (line 218)
- `cleanup` (line 227)

---

### `features\voice\voice_service.py`

**Classes:**
- `VoiceService` (line 23)

**Functions:**
- `get_instance` (line 46)
- `__init__` (line 51)
- `_setup_connections` (line 117)
- `_setup_service_connections` (line 154)
- `_on_recording_started` (line 197)
- `_on_recording_stopped` (line 203)
- `_on_recording_error` (line 209)
- `_on_recording_auto_stopped` (line 215)
- `_on_recording_auto_stopped_for_stt` (line 220)
- `_on_recording_timeout` (line 249)
- `is_voice_available` (line 255)
- `can_handle_new_request` (line 285)
- `queue_request` (line 292)
- `_process_request_queue` (line 312)
- `_handle_voice_input_request` (line 339)
- `_handle_tts_request` (line 366)
- `_complete_request` (line 400)
- `clear_request_queue` (line 409)
- `cancel_current_request` (line 437)
- `handle_user_interruption` (line 462)
- `_on_audio_level_changed` (line 494)
- `start_voice_input` (line 515)
- `stop_voice_input` (line 549)
- `_on_stt_text_received` (line 568)
- `_restart_voice_input_safely` (line 636)
- `_on_stt_error` (line 664)
- `_on_tts_started` (line 699)
- `_on_tts_finished` (line 723)
- `_on_tts_error` (line 759)
- `speak_text` (line 789)
- `_speak_text_impl` (line 821)
- `stop_tts` (line 864)
- `set_continuous_voice_mode` (line 887)
- `is_continuous_voice_mode` (line 892)
- `update_settings` (line 896)
- `get_silence_duration` (line 901)
- `get_silence_threshold` (line 905)
- `get_recording_timeout` (line 909)
- `get_current_audio_level` (line 913)
- `set_recording_timeout` (line 919)
- `set_silence_duration` (line 923)
- `set_silence_threshold` (line 927)
- `set_audio_gate_enabled` (line 931)
- `cleanup_on_exit` (line 937)
- `get_audio_folder_path` (line 1000)
- `list_audio_files` (line 1004)
- `cleanup_old_audio_files` (line 1026)
- `cleanup_all_audio_files` (line 1059)
- `_forward_recording_started` (line 1078)
- `_forward_recording_stopped` (line 1086)
- `_forward_recording_error` (line 1094)
- `_forward_voice_processing_started` (line 1102)
- `_cleanup_resources` (line 1110)
- `_reset_error_count` (line 1144)
- `_connect_signals` (line 1149)
- `_initialize_services` (line 1155)
- `_check_and_emit_ready` (line 1229)

---

### `features\voice\voice_service_manager.py`

**Classes:**
- `VoiceServiceManager` (line 17)

**Functions:**
- `get_voice_service_manager` (line 278)
- `__new__` (line 28)
- `__init__` (line 36)
- `get_voice_service` (line 58)
- `_initialize_voice_service` (line 76)
- `_on_voice_service_ready` (line 139)
- `_try_get_from_service_manager` (line 144)
- `_try_direct_initialization` (line 162)
- `_reset_voice_service` (line 175)
- `update_settings` (line 192)
- `get_settings` (line 210)
- `is_ready` (line 220)
- `is_initializing` (line 226)
- `get_last_error` (line 230)
- `register_ready_callback` (line 234)
- `force_reinitialize` (line 251)
- `cleanup` (line 257)

---

### `features\voice\voice_service_wrapper.py`

**Classes:**
- `VoiceServiceWrapper` (line 14)

**Functions:**
- `__init__` (line 33)
- `_init_process_manager` (line 49)
- `_init_direct_service` (line 70)
- `start_voice_input` (line 98)
- `stop_voice_input` (line 112)
- `speak_text` (line 126)
- `speak_text_streaming` (line 140)
- `speak_text_non_streaming` (line 154)
- `stop_tts` (line 168)
- `is_voice_available` (line 182)
- `update_settings` (line 191)
- `get_recording_timeout` (line 200)
- `set_recording_timeout` (line 206)
- `get_silence_duration` (line 211)
- `set_silence_duration` (line 217)
- `get_silence_threshold` (line 222)
- `set_silence_threshold` (line 228)
- `set_audio_gate_enabled` (line 233)
- `get_current_audio_level` (line 238)
- `set_continuous_voice_mode` (line 244)
- `is_continuous_voice_mode` (line 253)
- `cleanup_on_exit` (line 259)
- `get_audio_folder_path` (line 266)
- `list_audio_files` (line 272)
- `cleanup_old_audio_files` (line 278)
- `cleanup_all_audio_files` (line 283)
- `get_process_info` (line 288)
- `test_connection` (line 294)
- `_update_cached_state` (line 300)
- `_update_cached_state_from_signal` (line 306)
- `is_recording` (line 311)
- `is_processing_voice` (line 318)
- `is_playing_tts` (line 325)
- `recording_service` (line 332)
- `_on_voice_service_ready` (line 338)
- `_check_service_readiness` (line 351)

---

### `startup\__init__.py`

---

### `startup\dependency_checker.py`

**Classes:**
- `DependencyChecker` (line 17)

**Functions:**
- `check_and_install_dependencies` (line 207)
- `__init__` (line 20)
- `test_import` (line 26)
- `check_core_dependencies` (line 42)
- `check_ml_dependencies` (line 83)
- `check_tts_options` (line 102)
- `check_package_versions` (line 118)
- `run_comprehensive_check` (line 155)
- `get_missing_dependencies` (line 166)
- `get_version_conflicts` (line 170)
- `run_install_dependencies` (line 174)
- `get_dependency_summary` (line 199)

---

### `startup\install_dependencies.py`

**Functions:**
- `main` (line 21)

---

### `startup\python_installer.py`

**Functions:**
- `install_python_requirements` (line 6)

---

### `startup\system_installer.py`

**Functions:**
- `is_admin` (line 8)
- `offer_add_espeak_to_path` (line 14)
- `ensure_system_dependencies` (line 38)

---

### `ui\Widgets\__init__.py`

---

### `ui\Widgets\chat_navigation.py`

**Classes:**
- `ChatNavigationWidget` (line 15)

**Functions:**
- `__init__` (line 24)
- `setup_ui` (line 35)
- `setup_connections` (line 149)
- `refresh_conversations` (line 161)
- `create_conversation_item` (line 191)
- `on_conversation_double_clicked` (line 212)
- `show_context_menu` (line 218)
- `rename_conversation` (line 255)
- `delete_conversation` (line 292)
- `set_current_conversation` (line 319)
- `get_selected_conversation` (line 324)
- `clear_all_conversations` (line 331)
- `trigger_name_generation` (line 354)
- `on_summarization_completed` (line 386)
- `on_summarization_failed` (line 412)

---

### `ui\Widgets\complexity_widget.py`

**Classes:**
- `ComplexityWidget` (line 3)

**Functions:**
- `__init__` (line 8)
- `setup_ui` (line 14)
- `analyze_request` (line 107)
- `_update_display` (line 127)
- `_update_model_recommendation` (line 179)
- `_on_switch_model` (line 185)
- `_set_widget_color` (line 190)
- `_set_progress_bar_color` (line 196)
- `_get_color_for_value` (line 212)
- `clear_analysis` (line 226)
- `get_current_metrics` (line 234)

---

### `ui\Widgets\message_editor.py`

**Classes:**
- `EditableMessageWidget` (line 7)

**Functions:**
- `__init__` (line 14)
- `setup_ui` (line 24)
- `setup_styles` (line 86)
- `start_editing` (line 165)
- `save_edit` (line 174)
- `cancel_edit` (line 184)
- `finish_editing` (line 189)
- `get_content` (line 195)
- `set_content` (line 199)

---

### `ui\Widgets\spellchecker_widget.py`

**Classes:**
- `SpellCheckerTextEdit` (line 20)

**Functions:**
- `__init__` (line 23)
- `setup_spellchecker` (line 33)
- `setup_context_menu` (line 50)
- `show_context_menu` (line 55)
- `replace_word` (line 99)
- `add_to_dictionary` (line 109)
- `ignore_word` (line 120)
- `highlight_misspelled_words` (line 124)
- `keyPressEvent` (line 169)
- `on_text_changed` (line 179)
- `enable_spellcheck` (line 186)
- `disable_spellcheck` (line 193)
- `cleanup` (line 205)

---

### `ui\__init__.py`

---

### `ui\dialogs\__init__.py`

---

### `ui\dialogs\coqui_model_dialog.py`

**Classes:**
- `ModelDownloadThread` (line 16)
- `CoquiModelDialog` (line 43)

**Functions:**
- `__init__` (line 49)
- `run` (line 25)
- `setup_ui` (line 65)
- `create_model_panel` (line 194)
- `create_speaker_panel` (line 223)
- `load_models` (line 246)
- `on_model_selected` (line 275)
- `load_speakers_for_model` (line 296)
- `on_speaker_selected` (line 329)
- `download_selected_model` (line 335)
- `start_download` (line 351)
- `on_download_completed` (line 363)
- `update_selection_button` (line 378)
- `accept_selection` (line 385)
- `log_status` (line 393)
- `get_current_time` (line 401)

---

### `ui\dialogs\error_dialog.py`

**Classes:**
- `ErrorDialog` (line 9)
- `DetailedErrorDialog` (line 111)

**Functions:**
- `show_error_dialog` (line 282)
- `__init__` (line 114)
- `copy_error` (line 226)
- `reset_copy_button` (line 258)
- `setup_ui` (line 126)
- `setup_styles` (line 183)
- `accept` (line 278)

---

### `ui\dialogs\settings_dialog.py`

**Classes:**
- `SettingsDialog` (line 7)

**Functions:**
- `__init__` (line 10)
- `setup_ui` (line 21)
- `create_general_tab` (line 65)
- `create_chat_tab` (line 129)
- `create_session_tab` (line 180)
- `create_developer_tab` (line 220)
- `_delayed_load_settings` (line 238)
- `load_current_settings` (line 243)
- `save_settings` (line 303)
- `reset_to_defaults` (line 354)

---

### `ui\dialogs\voice_settings_dialog.py`

**Classes:**
- `InternetCheckThread` (line 26)
- `VoiceSettingsDialog` (line 39)
- `CalibrateSilenceThresholdDialog` (line 1396)

**Functions:**
- `safe_disconnect` (line 1495)
- `run` (line 30)
- `__init__` (line 1397)
- `setup_ui` (line 153)
- `create_stt_tab` (line 292)
- `create_tts_tab` (line 333)
- `create_general_tab` (line 456)
- `setup_connections` (line 629)
- `check_internet_connection` (line 646)
- `on_internet_check_completed` (line 656)
- `update_api_availability` (line 671)
- `on_stt_api_changed` (line 697)
- `refresh_coqui_ui` (line 711)
- `_on_voices_loaded` (line 753)
- `on_tts_api_changed` (line 781)
- `on_voice_changed` (line 815)
- `on_eq_visualizer_changed` (line 819)
- `load_coqui_models` (line 828)
- `on_coqui_model_changed` (line 832)
- `load_coqui_speakers` (line 867)
- `get_speaker_info` (line 873)
- `filter_speakers` (line 936)
- `on_coqui_speaker_changed` (line 986)
- `preview_selected_speaker` (line 1018)
- `download_selected_model` (line 1066)
- `on_silence_threshold_changed` (line 1093)
- `test_settings` (line 1116)
- `save_settings` (line 1172)
- `get_settings` (line 1254)
- `set_settings` (line 1258)
- `on_tts_settings_changed` (line 1379)
- `open_calibration_dialog` (line 1388)
- `_start_step` (line 1423)
- `_start_recording` (line 1437)
- `_on_timer` (line 1443)
- `_finish` (line 1470)
- `get_result` (line 1491)
- `safe_get_text` (line 1188)
- `safe_get_checked` (line 1197)
- `safe_get_value` (line 1207)

---

### `ui\tabs\__init__.py`

---

### `ui\tabs\chat_tab\__init__.py`

---

### `ui\tabs\chat_tab\chat_display.py`

**Classes:**
- `ChatDisplay` (line 14)

**Functions:**
- `__init__` (line 20)
- `setup_ui_components` (line 35)
- `setup_chat_renderer` (line 63)
- `_sync_messages_from_conversation_service` (line 80)
- `sync_messages_from_conversation_service` (line 130)
- `get_ai_name` (line 138)
- `chat_display_mouse_move_event` (line 144)
- `show_edit_button` (line 170)
- `hide_edit_button` (line 204)
- `edit_message_at_index` (line 212)
- `show_message_edit_dialog` (line 223)
- `save_message_edit` (line 312)
- `on_render_completed` (line 331)
- `on_render_error` (line 336)
- `on_message_edited` (line 347)
- `append_to_chat` (line 354)
- `force_update_display` (line 380)
- `_force_render_display` (line 391)
- `append_response_chunk` (line 410)
- `start_streaming` (line 449)
- `stop_streaming` (line 461)
- `clear_chat` (line 477)
- `get_ui_components` (line 488)
- `get_streaming_handler` (line 495)

---

### `ui\tabs\chat_tab\chat_renderer.py`

**Classes:**
- `ChatRenderer` (line 15)

**Functions:**
- `__init__` (line 22)
- `_get_next_message_id` (line 58)
- `add_message` (line 63)
- `append_message` (line 81)
- `edit_message` (line 88)
- `update_last_system_switch` (line 100)
- `_get_current_streaming_message` (line 116)
- `start_streaming_message` (line 123)
- `_process_typewriter_chunk` (line 134)
- `update_streaming_message` (line 156)
- `finalize_streaming_message` (line 193)
- `clear_chat` (line 208)
- `update_message` (line 214)
- `get_messages` (line 223)
- `clear_messages` (line 227)
- `sync_messages_from_handler` (line 232)
- `sync_messages_from_conversation` (line 237)
- `request_render` (line 248)
- `_execute_render` (line 274)
- `_emergency_reset` (line 306)
- `_reset_render_counter` (line 317)
- `_render_chat_display` (line 321)
- `cleanup` (line 478)

---

### `ui\tabs\chat_tab\chat_tab.py`

**Classes:**
- `ChatTab` (line 37)

**Functions:**
- `safe_disconnect` (line 24)
- `__init__` (line 51)
- `setup_components` (line 81)
- `setup_ui` (line 100)
- `setup_connections` (line 260)
- `_on_conversation_updated` (line 301)
- `on_message_sent` (line 309)
- `on_message_cancelled` (line 341)
- `_ensure_voice_controls_initialized` (line 346)
- `on_voice_status_changed` (line 438)
- `on_input_mode_changed` (line 446)
- `on_temperature_changed` (line 518)
- `on_personality_changed` (line 523)
- `on_model_changed` (line 528)
- `on_eq_mode_changed` (line 533)
- `on_user_interrupted` (line 542)
- `on_request_cancelled` (line 559)
- `on_voice_input_received` (line 576)
- `on_voice_input_received_direct` (line 598)
- `process_voice_input` (line 621)
- `on_voice_input_error` (line 654)
- `on_tts_started` (line 664)
- `on_tts_finished` (line 677)
- `on_tts_error` (line 718)
- `on_recording_started` (line 728)
- `on_recording_stopped` (line 735)
- `on_recording_error` (line 742)
- `on_voice_processing_started` (line 752)
- `on_voice_processing_finished` (line 759)
- `on_audio_level_changed` (line 766)
- `on_eq_bars_changed` (line 808)
- `on_message_edited` (line 823)
- `get_ai_name` (line 829)
- `get_current_personality` (line 865)
- `get_current_model` (line 869)
- `get_temperature` (line 873)
- `get_current_response` (line 877)
- `append_to_chat` (line 881)
- `_force_chat_display_update` (line 901)
- `append_response_chunk` (line 926)
- `_append_response_chunk_safe` (line 931)
- `_ensure_chat_display_visible` (line 955)
- `start_streaming` (line 983)
- `_start_streaming_safe` (line 988)
- `stop_streaming` (line 1035)
- `force_enable_send_button` (line 1071)
- `_force_enable_send_button_safe` (line 1076)
- `clear_chat` (line 1098)
- `update_model_list` (line 1102)
- `update_personality_list` (line 1106)
- `speak_ai_response` (line 1110)
- `open_voice_settings` (line 1133)
- `on_eq_visualizer_changed_immediate` (line 1182)
- `on_eq_visualizer_changed_from_voice_controls` (line 1199)
- `on_voice_settings_changed` (line 1216)
- `load_conversation` (line 1227)
- `_load_conversation_fallback` (line 1276)
- `refresh_navigation` (line 1323)
- `set_current_conversation_file` (line 1328)
- `set_chat_controller` (line 1333)
- `get_streaming_handler` (line 1354)
- `streaming_handler` (line 1359)
- `finalize_streaming_and_start_tts` (line 1363)
- `_finalize_and_start` (line 1366)

---

### `ui\tabs\chat_tab\eq_visualizer.py`

**Classes:**
- `EQVisualizer` (line 19)

**Functions:**
- `__init__` (line 25)
- `setup_eq_visualizers` (line 37)
- `switch_to_eq_visualizer` (line 51)
- `switch_to_chat_display` (line 152)
- `update_eq_visualizer` (line 247)
- `_update_eq_widget_safe` (line 378)
- `is_eq_visualizer_active` (line 391)
- `update_eq_visualizer_mode` (line 397)
- `get_eq_mode` (line 405)
- `get_available_eq_modes` (line 409)

---

### `ui\tabs\chat_tab\input_controls.py`

**Classes:**
- `InputControls` (line 12)

**Functions:**
- `__init__` (line 23)
- `setup_ui_components` (line 38)
- `setup_connections` (line 210)
- `set_input_mode` (line 228)
- `on_temperature_changed` (line 247)
- `on_personality_combo_changed` (line 254)
- `on_model_changed` (line 260)
- `send_message` (line 265)
- `cancel_message` (line 286)
- `start_streaming` (line 291)
- `stop_streaming` (line 314)
- `force_enable_send_button` (line 340)
- `update_model_list` (line 360)
- `update_personality_list` (line 372)
- `get_current_model` (line 383)
- `get_temperature` (line 387)
- `get_current_response` (line 391)
- `get_current_personality` (line 395)
- `get_ui_components` (line 399)
- `eventFilter` (line 413)

---

### `ui\tabs\chat_tab\voice_controls.py`

**Classes:**
- `VoiceControls` (line 35)

**Functions:**
- `safe_disconnect` (line 17)
- `__init__` (line 60)
- `setup_ui_components` (line 138)
- `_update_voice_button_state` (line 245)
- `_update_voice_state` (line 312)
- `is_voice_busy` (line 317)
- `_handle_voice_crash` (line 322)
- `_attempt_recovery` (line 335)
- `_stop_all_voice_operations` (line 345)
- `_reset_voice_ui` (line 357)
- `_reinitialize_voice_service` (line 368)
- `_disable_voice_features` (line 379)
- `_reset_error_count` (line 388)
- `_handle_service_error` (line 392)
- `setup_connections` (line 406)
- `_initialize_voice_service_manager` (line 414)
- `force_ui_refresh` (line 492)
- `_on_voice_service_ready` (line 522)
- `_on_direct_voice_service_ready` (line 550)
- `_periodic_ui_refresh` (line 565)
- `_on_voice_service_error` (line 586)
- `_on_voice_service_initializing` (line 596)
- `get_voice_service` (line 606)
- `_setup_voice_connections` (line 630)
- `_disconnect_voice_signals` (line 732)
- `reset_voice_signal_connections` (line 774)
- `_is_voice_service_ready` (line 778)
- `_validate_voice_service_capabilities` (line 803)
- `reset_voice_service` (line 825)
- `toggle_voice_mode` (line 856)
- `_start_continuous_voice_mode` (line 952)
- `_handle_voice_input_safe` (line 1004)
- `_handle_tts_finished_continuous` (line 1075)
- `_restart_voice_input` (line 1086)
- `_reset_voice_button` (line 1101)
- `on_voice_input_received` (line 1123)
- `on_voice_input_error` (line 1136)
- `_handle_voice_input_error_safe` (line 1151)
- `on_tts_started` (line 1181)
- `on_tts_finished` (line 1192)
- `on_tts_error` (line 1209)
- `_handle_tts_error_safe` (line 1225)
- `on_recording_started` (line 1229)
- `_handle_recording_started_safe` (line 1237)
- `on_recording_stopped` (line 1259)
- `_handle_recording_stopped_safe` (line 1267)
- `on_recording_error` (line 1282)
- `_handle_recording_error_safe` (line 1290)
- `on_voice_processing_started` (line 1306)
- `on_voice_processing_finished` (line 1313)
- `on_audio_level_changed` (line 1319)
- `_update_audio_level_ui_safe` (line 1356)
- `speak_ai_response` (line 1417)
- `update_voice_settings` (line 1435)
- `get_voice_settings` (line 1451)
- `is_voice_service_ready` (line 1461)
- `is_voice_service_initializing` (line 1471)
- `get_voice_service_error` (line 1481)
- `force_reinitialize_voice_service` (line 1487)
- `is_voice_mode_active` (line 1497)
- `is_tts_playing` (line 1501)
- `can_handle_interruption` (line 1512)
- `get_interruption_threshold` (line 1523)
- `get_ui_components` (line 1534)
- `on_user_interrupted` (line 1542)
- `on_request_cancelled` (line 1557)
- `on_eq_bars_changed` (line 1573)
- `_update_eq_bars` (line 1577)
- `_restart_voice_input_after_interruption` (line 1602)
- `_restart_voice_input_after_cancellation` (line 1617)
- `_clear_last_voice_input` (line 1632)
- `_is_similar_voice_input` (line 1645)
- `_reset_duplicate_detection_state` (line 1677)
- `cleanup` (line 1690)
- `__del__` (line 1716)
- `_on_voice_input_received` (line 1723)
- `_on_voice_input_error` (line 1744)
- `_on_tts_started` (line 1763)
- `_on_tts_finished` (line 1781)
- `_on_tts_error` (line 1799)
- `_on_recording_started` (line 1820)
- `_on_recording_stopped` (line 1838)
- `_on_recording_error` (line 1856)
- `_on_audio_level_changed` (line 1878)
- `_on_eq_bars_changed` (line 1891)
- `_on_voice_status_changed` (line 1904)
- `update_voice_status` (line 1920)

---

### `ui\tabs\memory_tab.py`

**Classes:**
- `MemoryTab` (line 31)

**Functions:**
- `safe_disconnect` (line 14)
- `__init__` (line 34)
- `setup_ui` (line 41)
- `create_settings_tab` (line 67)
- `create_overview_tab` (line 127)
- `create_memories_tab` (line 187)
- `create_summaries_tab` (line 252)
- `setup_connections` (line 282)
- `update_context_messages` (line 306)
- `refresh_data` (line 311)
- `refresh_overview` (line 317)
- `refresh_memories` (line 373)
- `refresh_summaries` (line 404)
- `search_memories` (line 417)
- `show_memory_details` (line 439)
- `show_summary_details` (line 473)
- `summarize_current_conversation` (line 489)
- `set_conversation_service` (line 495)
- `_summarize_with_service` (line 502)
- `clear_all_memories` (line 523)
- `cleanup_memory_entries` (line 536)
- `delete_selected_memory` (line 552)

---

### `ui\tabs\model_tab.py`

**Classes:**
- `ModelTab` (line 7)

**Functions:**
- `__init__` (line 15)
- `setup_ui` (line 38)
- `setup_model_list` (line 55)
- `setup_operations` (line 131)
- `setup_connections` (line 351)
- `refresh_models` (line 361)
- `update_model_list` (line 369)
- `pull_model` (line 379)
- `remove_selected_model` (line 397)
- `update_selected_model` (line 417)
- `on_model_selection_changed` (line 437)
- `start_operation` (line 444)
- `stop_operation` (line 453)
- `append_status` (line 461)
- `get_current_time` (line 470)
- `on_operation_progress` (line 475)
- `on_operation_finished` (line 479)
- `on_operation_error` (line 487)
- `get_selected_model` (line 493)
- `clear_status` (line 498)

---

### `ui\tabs\personality_tab.py`

**Classes:**
- `PersonalityTab` (line 12)

**Functions:**
- `__init__` (line 18)
- `setup_ui` (line 25)
- `setup_selection_tab` (line 85)
- `setup_creation_tab` (line 192)
- `setup_management_tab` (line 511)
- `load_personalities` (line 684)
- `update_system_personalities_list` (line 724)
- `update_custom_personalities_list` (line 736)
- `on_system_personality_selected` (line 747)
- `update_system_personality_info` (line 753)
- `on_custom_personality_selected` (line 774)
- `on_personality_changed` (line 780)
- `update_personality_info` (line 786)
- `create_personality` (line 809)
- `clear_creation_form` (line 923)
- `delete_custom_personality` (line 965)
- `export_personality` (line 998)
- `refresh_personalities` (line 1019)
- `get_current_personality` (line 1028)
- `get_system_prompt` (line 1032)
- `get_available_personalities` (line 1043)
- `on_conversation_style_changed` (line 1051)
- `on_context_template_changed` (line 1059)
- `get_user_prompt_template` (line 1067)
- `get_context_prompt` (line 1078)

---

### `ui\tabs\tab_styles.py`

**Classes:**
- `TabStyles` (line 9)

**Functions:**
- `get_tab_style` (line 40)

---

### `ui\themes\__init__.py`

---

### `ui\themes\message_formatter.py`

**Classes:**
- `MessageFormatter` (line 15)

**Functions:**
- `detect_code_in_message` (line 19)
- `detect_code_type` (line 48)
- `syntax_highlight_code` (line 60)
- `detect_and_format_code` (line 97)
- `_protect_code_blocks` (line 133)
- `format_markdown` (line 149)
- `handle_html_tags` (line 221)
- `cleanup_message` (line 250)
- `format_chat_message` (line 278)
- `split_thoughts_and_answer` (line 315)
- `to_plain_text` (line 331)
- `format_block_code` (line 107)
- `protect_code_blocks` (line 137)

---

### `ui\themes\styles.py`

---

### `ui\ui_manager.py`

**Classes:**
- `UIManager` (line 24)

**Functions:**
- `__init__` (line 27)
- `setup_ui` (line 41)
- `setup_menu_bar` (line 95)
- `apply_theme` (line 176)
- `update_status` (line 189)
- `get_menu_action` (line 198)
- `get_main_window` (line 202)
- `get_chat_tab` (line 206)
- `get_model_tab` (line 210)
- `get_personality_tab` (line 214)
- `get_memory_tab` (line 218)
- `get_tabs` (line 222)
- `show_about_dialog` (line 226)
- `show_clear_chat_dialog` (line 234)

---

### `ui\utils\message_utils.py`

**Functions:**
- `show_error` (line 11)
- `show_warning` (line 15)
- `show_critical_error` (line 23)
- `show_operation_error` (line 34)
- `show_connection_error` (line 43)
- `show_file_error` (line 52)
- `show_validation_error` (line 63)

---

### `ui\visualizers\__init__.py`

---

### `ui\visualizers\widgets\__init__.py`

---

### `ui\visualizers\widgets\bar_eq_widget.py`

**Classes:**
- `BarEQWidget` (line 3)

**Functions:**
- `__init__` (line 23)
- `_setup_animation_timer` (line 47)
- `_animate` (line 53)
- `set_eq_bars` (line 66)
- `set_idle` (line 102)
- `start_animation` (line 107)
- `stop_animation` (line 111)
- `get_current_values` (line 115)
- `_calculate_bar_geometry` (line 129)
- `_create_bar_gradient` (line 158)
- `_draw_bar` (line 212)
- `paintEvent` (line 241)

---

### `ui\visualizers\widgets\circle_eq_widget.py`

**Classes:**
- `CircleEQWidget` (line 4)

**Functions:**
- `__init__` (line 22)
- `_setup_animation_timer` (line 46)
- `_animate` (line 52)
- `set_eq_sections` (line 66)
- `set_idle` (line 102)
- `start_animation` (line 107)
- `stop_animation` (line 111)
- `get_current_values` (line 115)
- `_create_section_gradient` (line 129)
- `paintEvent` (line 169)

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py`

**Classes:**
- `CircularGradientEQWidget` (line 5)

**Functions:**
- `__init__` (line 15)
- `_smooth_radii` (line 39)
- `_animate` (line 47)
- `set_net_radii` (line 56)
- `set_idle` (line 75)
- `start_animation` (line 81)
- `stop_animation` (line 84)
- `paintEvent` (line 87)

---

### `ui\visualizers\widgets\circular_net_eq_widget.py`

**Classes:**
- `CircularNetEQWidget` (line 5)

**Functions:**
- `__init__` (line 18)
- `_animate` (line 39)
- `set_net_radii` (line 49)
- `set_idle` (line 68)
- `start_animation` (line 72)
- `stop_animation` (line 75)
- `paintEvent` (line 78)

---

## 🏗️ Classes

### `app\app_lifecycle.py.AppLifecycleManager`

- **File:** `app\app_lifecycle.py`
- **Line:** 18
- **Docstring:** Manages application startup, shutdown, and error handling...

**Methods:**
- `__init__` (line 21)
- `initialize_application` (line 46)
- `handle_show_event` (line 74)
- `handle_close_event` (line 95)
- `show_initialization_error` (line 133)
- `show_ollama_connection_error` (line 142)
- `show_ollama_startup_dialog` (line 302)
- `check_ollama_connection` (line 309)
- `is_initialization_complete` (line 320)
- `set_ollama_error_shown` (line 324)
- `get_ollama_error_shown` (line 328)
- `reset_ollama_error_shown` (line 332)
- `force_show_ollama_error` (line 337)
- `test_error_dialog` (line 342)
- `get_available_models` (line 348)
- `send_test_message` (line 364)
- `_ensure_ollama_running` (line 406)
- `_is_ollama_installed` (line 442)
- `_find_ollama_executable` (line 468)
- `_start_ollama_background` (line 512)
- `_verify_ollama_installation` (line 635)
- `_stop_ollama_process` (line 679)
- `start_ollama_manually` (line 716)
- `stop_ollama_manually` (line 722)
- `is_ollama_running` (line 726)
- `get_ollama_process_info` (line 730)
- `set_auto_start_ollama` (line 743)
- `get_auto_start_ollama` (line 748)
- `_check_ollama_crash` (line 752)
- `_reset_ollama_restart_attempts` (line 809)
- `set_close_ollama_on_exit` (line 813)
- `get_close_ollama_on_exit` (line 818)
- `force_close_ollama` (line 822)
- `was_ollama_started_by_app` (line 827)
- `get_ollama_status_info` (line 831)
- `_show_custom_path_dialog` (line 849)
- `_validate_ollama_executable` (line 913)
- `set_custom_ollama_path` (line 945)
- `get_custom_ollama_path` (line 956)
- `clear_custom_ollama_path` (line 960)
- `get_ollama_path_info` (line 966)

---

### `app\event_bus.py.EventBus`

- **File:** `app\event_bus.py`
- **Line:** 13
- **Docstring:** Manages signal connections and event handling...

**Methods:**
- `__init__` (line 16)
- `setup_connections` (line 52)
- `_setup_chat_tab_retry` (line 104)
- `_retry_chat_tab_connection` (line 116)
- `_connect_menu_actions` (line 137)
- `_connect_chat_tab_signals` (line 179)
- `_on_status_updated` (line 229)
- `_on_error_occurred` (line 233)
- `_on_conversation_updated` (line 238)
- `_on_name_generation_requested` (line 244)
- `_on_models_updated` (line 269)
- `_on_message_sent` (line 283)
- `_send_to_ollama` (line 321)
- `_clean_messages_for_ollama` (line 374)
- `_start_worker_after_streaming_message` (line 386)
- `_create_worker_thread` (line 423)
- `_handle_chat_chunk` (line 470)
- `_handle_chat_progress` (line 499)
- `_handle_chat_finished` (line 507)
- `_handle_chat_error` (line 533)
- `_handle_chat_error_safe` (line 547)
- `stop_chat_streaming` (line 564)
- `_on_worker_progress` (line 576)
- `_on_worker_detailed_error` (line 589)
- `_on_worker_thread_finished` (line 604)
- `_on_worker_chunk` (line 609)
- `_update_chat_display_safe` (line 619)
- `_on_worker_progress` (line 632)
- `_update_progress_safe` (line 644)
- `_on_worker_finished` (line 653)
- `_stop_streaming_safe` (line 675)
- `_on_worker_error` (line 685)
- `_handle_worker_error_safe` (line 698)
- `_on_tts_finished` (line 717)
- `_handle_tts_finished_delayed` (line 724)
- `_cleanup_worker_thread` (line 738)
- `_cleanup_worker_thread_once` (line 750)
- `_final_worker_cleanup` (line 774)
- `_on_message_received` (line 783)
- `_on_message_finished` (line 790)
- `_on_message_cancelled` (line 799)
- `_on_conversation_selected` (line 825)
- `_on_conversation_deleted` (line 833)
- `_on_conversation_renamed` (line 837)
- `_on_personality_changed` (line 859)
- `_on_model_operation_progress` (line 884)
- `_on_model_operation_error` (line 890)
- `_on_conversation_metadata_updated` (line 910)
- `_on_auto_save_completed` (line 922)
- `_on_new_conversation_requested` (line 938)
- `_on_new_conversation` (line 942)
- `_on_clear_chat` (line 959)
- `_on_save_chat` (line 970)
- `_on_load_chat` (line 976)
- `_on_open_settings` (line 982)
- `_create_chat_controller` (line 1009)
- `_setup_ui_with_new_services` (line 1021)
- `_on_refresh_models` (line 1027)
- `_on_refresh_personalities` (line 1059)
- `_on_show_about` (line 1073)
- `_on_delayed_model_update` (line 1077)
- `_check_ollama_connection` (line 1093)
- `_show_ollama_connection_error` (line 1098)
- `get_threading_status` (line 1146)
- `cleanup_on_exit` (line 1157)
- `reconnect_chat_tab_signals` (line 1198)

---

### `app\main.py.OllamaChat`

- **File:** `app\main.py`
- **Line:** 20
- **Bases:** QMainWindow
- **Docstring:** Main application window - refactored with modular components...

**Methods:**
- `__init__` (line 23)
- `_setup_ui` (line 84)
- `_setup_connections` (line 118)
- `showEvent` (line 136)
- `closeEvent` (line 141)
- `show_ollama_connection_error` (line 145)
- `check_ollama_connection` (line 149)
- `get_service_manager` (line 154)
- `get_ui_manager` (line 158)
- `get_event_handler` (line 162)
- `get_lifecycle_manager` (line 166)
- `get_chat_controller` (line 170)

---

### `app\service_manager.py.ServiceManager`

- **File:** `app\service_manager.py`
- **Line:** 20
- **Docstring:** Manages all application services and their initialization...

**Methods:**
- `__new__` (line 26)
- `__init__` (line 34)
- `get_instance` (line 62)
- `_initialize_services` (line 68)
- `reinitialize_services` (line 130)
- `get_ollama_service` (line 135)
- `get_conversation_service` (line 139)
- `get_enhancement_service` (line 143)
- `get_memory_service` (line 147)
- `get_summarization_service` (line 151)
- `get_conversation_manager` (line 155)
- `get_personality_service` (line 159)
- `get_voice_service` (line 163)
- `is_voice_service_initialized` (line 169)
- `is_memory_enabled` (line 175)
- `get_session_variables` (line 179)
- `cleanup` (line 183)
- `_initialize_voice_service` (line 207)

---

### `app\threading_integration.py.EventBusThreadingBridge`

- **File:** `app\threading_integration.py`
- **Line:** 141
- **Docstring:** Bridge class that integrates new threading architecture with existing EventBus.

This class provides...

**Methods:**
- `__init__` (line 151)
- `_on_chunk_received` (line 163)
- `_on_progress_updated` (line 175)
- `_on_finished` (line 187)
- `_on_error` (line 199)
- `start_chat_streaming` (line 211)
- `stop_chat_streaming` (line 232)
- `get_threading_status` (line 241)

---

### `app\threading_integration.py.ThreadingIntegration`

- **File:** `app\threading_integration.py`
- **Line:** 14
- **Bases:** QObject
- **Docstring:** Integration layer that bridges the new threading architecture with existing event system.

This clas...

**Methods:**
- `__init__` (line 30)
- `start_chat_streaming` (line 43)
- `stop_chat_streaming` (line 64)
- `process_message_spell_check` (line 73)
- `process_message_formatting` (line 92)
- `process_file_operation` (line 111)
- `get_threading_status` (line 131)

---

### `config\config_manager.py.ConfigManager`

- **File:** `config\config_manager.py`
- **Line:** 10
- **Docstring:** Manages application configuration settings...

**Methods:**
- `__init__` (line 13)
- `load_config` (line 17)
- `merge_configs` (line 65)
- `save_config` (line 75)
- `get` (line 88)
- `set` (line 101)
- `get_default_model` (line 118)
- `set_default_model` (line 122)
- `get_default_temperature` (line 126)
- `set_default_temperature` (line 130)
- `get_default_personality` (line 134)
- `set_default_personality` (line 138)
- `get_window_size` (line 142)
- `set_window_size` (line 147)
- `get_chat_settings` (line 151)
- `is_auto_save_enabled` (line 160)
- `set_auto_save_enabled` (line 164)
- `is_spellcheck_enabled` (line 168)
- `set_spellcheck_enabled` (line 172)
- `get_ollama_url` (line 176)
- `set_ollama_url` (line 181)
- `get_history_directory` (line 185)
- `set_history_directory` (line 189)
- `is_enhancement_enabled` (line 193)
- `set_enhancement_enabled` (line 197)
- `is_history_enabled` (line 201)
- `set_history_enabled` (line 205)
- `is_wordwrap_enabled` (line 209)
- `set_wordwrap_enabled` (line 213)
- `is_json_format_enabled` (line 217)
- `set_json_format_enabled` (line 221)
- `is_verbose_enabled` (line 225)
- `set_verbose_enabled` (line 229)
- `is_think_enabled` (line 233)
- `set_think_enabled` (line 237)
- `get_max_tokens` (line 241)
- `get_top_p` (line 244)
- `get_frequency_penalty` (line 247)
- `get_presence_penalty` (line 250)
- `get_max_context_messages` (line 254)
- `set_max_context_messages` (line 258)
- `get_voice_settings` (line 262)
- `set_voice_settings` (line 279)

---

### `core\logging\helpers.py.LoggingHelpers`

- **File:** `core\logging\helpers.py`
- **Line:** 21
- **Docstring:** Centralized logging helper methods for consistent logging across the application...

**Methods:**
- `log_exception_with_context` (line 25)
- `log_warning_with_context` (line 32)
- `log_info_with_context` (line 38)
- `log_debug` (line 44)
- `log_error` (line 49)
- `log_network_request` (line 54)
- `log_file_operation` (line 64)
- `log_audio_operation` (line 72)
- `log_memory_operation` (line 80)
- `log_ui_operation` (line 88)
- `log_performance_metric` (line 96)
- `log_json_parsing_error` (line 102)
- `log_json_parsing_success` (line 108)
- `log_critical_error` (line 113)
- `log_fact_extraction_start` (line 120)
- `log_fact_extraction_end` (line 125)
- `log_fact_extraction_result` (line 130)
- `log_fact_processing` (line 135)
- `log_fact_storage_start` (line 140)
- `log_fact_storage_end` (line 145)
- `log_fact_storage_summary` (line 150)
- `log_fact_skipped` (line 155)
- `log_memory_result` (line 160)
- `log_memory_ltm_status` (line 165)
- `log_llm_call` (line 170)
- `log_llm_response` (line 175)
- `log_json_extraction` (line 180)
- `log_message_sent` (line 185)
- `log_message_sent_end` (line 190)
- `log_conversation_detection` (line 195)
- `log_service_initialization` (line 200)

---

### `core\logging\helpers.py.ThreadMonitor`

- **File:** `core\logging\helpers.py`
- **Line:** 209
- **Bases:** QObject
- **Docstring:** Monitor for tracking QThread lifecycle and debugging thread issues...

**Methods:**
- `__init__` (line 216)
- `register_thread` (line 224)
- `unregister_thread` (line 254)
- `_on_thread_started` (line 274)
- `_on_thread_finished` (line 286)
- `get_thread_info` (line 300)
- `get_all_threads` (line 304)
- `get_thread_history` (line 308)
- `get_thread_stats` (line 312)
- `cleanup` (line 352)

---

### `core\logging\helpers.py.ThreadSafeLogger`

- **File:** `core\logging\helpers.py`
- **Line:** 372
- **Docstring:** Thread-safe logging utilities...

**Methods:**
- `log_thread_context` (line 376)
- `log_thread_safety_check` (line 394)
- `log_thread_operation` (line 409)

---

### `core\logging\logger.py.CustomLogger`

- **File:** `core\logging\logger.py`
- **Line:** 93
- **Bases:** logging.Logger
- **Docstring:** Custom Logging class for the PyChat project.

This class provides enhanced logging functionality wit...

**Methods:**
- `_check_config_for_logging` (line 112)
- `__new__` (line 124)
- `set_logging_enabled` (line 131)
- `_clear_log_file` (line 135)
- `get_logger` (line 142)
- `info` (line 186)
- `debug` (line 191)
- `warning` (line 196)
- `error` (line 201)
- `_filter_non_ascii` (line 206)

---

### `core\logging\logger.py.DummyLogger`

- **File:** `core\logging\logger.py`
- **Line:** 146

**Methods:**
- `info` (line 147)
- `debug` (line 148)
- `warning` (line 149)
- `error` (line 150)
- `critical` (line 151)

---

### `core\logging\logger.py.PrintLogger`

- **File:** `core\logging\logger.py`
- **Line:** 180
- **Bases:** PrintOnLogMixin

---

### `core\logging\logger.py.PrintOnLogMixin`

- **File:** `core\logging\logger.py`
- **Line:** 39

**Methods:**
- `_print` (line 40)
- `info` (line 42)
- `debug` (line 47)
- `warning` (line 52)
- `error` (line 57)
- `critical` (line 62)

---

### `core\logging\logger.py.ThreadInfoFormatter`

- **File:** `core\logging\logger.py`
- **Line:** 68
- **Bases:** logging.Formatter
- **Docstring:** Custom formatter that includes thread information in log messages...

**Methods:**
- `format` (line 71)

---

### `core\models\base_model.py.BaseModel`

- **File:** `core\models\base_model.py`
- **Line:** 8
- **Bases:** ABC
- **Docstring:** Base class for all models in the application....

**Methods:**
- `to_dict` (line 12)
- `from_dict` (line 18)

---

### `core\models\conversation_metadata.py.ConversationManager`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 129
- **Bases:** QObject
- **Docstring:** Manager for handling conversation persistence and metadata...

**Methods:**
- `__init__` (line 135)
- `save_conversation` (line 143)
- `update_conversation_name` (line 180)
- `_create_safe_filename` (line 252)
- `load_conversation` (line 292)
- `auto_save_conversation` (line 324)
- `list_conversations` (line 398)
- `delete_conversation` (line 427)
- `rename_conversation` (line 444)
- `clear_current_conversation` (line 469)
- `get_current_metadata` (line 474)
- `set_auto_save_enabled` (line 478)
- `find_blank_conversation` (line 483)

---

### `core\models\conversation_metadata.py.ConversationMetadata`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 18
- **Decorators:** dataclass
- **Docstring:** Data class for storing conversation metadata...

**Methods:**
- `__post_init__` (line 30)
- `update_timestamp` (line 37)
- `update_message_count` (line 41)
- `update_model` (line 46)
- `update_personality` (line 51)
- `update_ai_generated_name` (line 56)
- `to_dict` (line 61)
- `from_dict` (line 74)
- `reset` (line 86)
- `get_formatted_created_time` (line 96)
- `get_formatted_modified_time` (line 106)
- `get_display_info` (line 116)
- `get_display_name` (line 124)

---

### `core\threading\persistent_thread_pool.py.PersistentThreadPool`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 19
- **Bases:** QObject
- **Docstring:** Manages persistent threads that stay alive throughout the application lifecycle.

This pool provides...

**Methods:**
- `__init__` (line 34)
- `initialize_pool` (line 95)
- `get_thread` (line 130)
- `return_thread` (line 220)
- `_create_idle_thread` (line 260)
- `_create_active_thread` (line 285)
- `_cleanup_idle_threads` (line 313)
- `get_pool_status` (line 344)
- `shutdown` (line 366)

---

### `core\threading\qrunnable_tasks.py.CalculationTask`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 578
- **Bases:** QRunnable, QObject
- **Docstring:** Task for CPU-intensive calculations.

This is a short-lived task that:
- Performs heavy calculations...

**Methods:**
- `__init__` (line 591)
- `run` (line 600)
- `_calculate_fibonacci` (line 624)
- `_calculate_prime_factors` (line 649)
- `_calculate_statistics` (line 681)

---

### `core\threading\qrunnable_tasks.py.DataProcessingTask`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 332
- **Bases:** QRunnable, QObject
- **Docstring:** Task for data processing operations.

This is a short-lived task that:
- Processes data in the backg...

**Methods:**
- `__init__` (line 345)
- `run` (line 355)
- `_handle_model_operation` (line 381)
- `_calculate_data` (line 477)
- `_transform_data` (line 505)
- `_analyze_data` (line 532)
- `_count_nested_levels` (line 564)

---

### `core\threading\qrunnable_tasks.py.FileProcessingTask`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 220
- **Bases:** QRunnable, QObject
- **Docstring:** Task for file operations (reading, writing, processing).

This is a short-lived task that:
- Process...

**Methods:**
- `__init__` (line 233)
- `run` (line 243)
- `_read_file` (line 267)
- `_write_file` (line 286)
- `_process_file` (line 301)

---

### `core\threading\qrunnable_tasks.py.MessageProcessingTask`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 83
- **Bases:** QRunnable, QObject
- **Docstring:** Task for processing chat messages (spell check, formatting, etc.).

This is a short-lived task that:...

**Methods:**
- `__init__` (line 96)
- `run` (line 105)
- `_spell_check_message` (line 129)
- `_format_message` (line 173)
- `_analyze_sentiment` (line 194)

---

### `core\threading\qrunnable_tasks.py.StreamingUpdateTask`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 20
- **Bases:** QRunnable, QObject
- **Docstring:** Task for handling streaming UI updates.

This task:
- Executes UI update functions in the main threa...

**Methods:**
- `__init__` (line 33)
- `run` (line 43)
- `_execute_target` (line 63)

---

### `core\threading\qthread_workers.py.AudioStreamingWorker`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 306
- **Bases:** StreamingWorker
- **Docstring:** Worker for streaming audio processing.

This is a long-running operation that needs:
- Continuous au...

**Methods:**
- `configure_audio_streaming` (line 317)
- `start_audio_streaming` (line 345)
- `_stream_operation` (line 360)

---

### `core\threading\qthread_workers.py.ChatStreamingWorker`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 149
- **Bases:** StreamingWorker
- **Docstring:** Worker for streaming chat responses from Ollama.

This is a long-running operation that needs:
- Con...

**Methods:**
- `configure_streaming` (line 160)
- `_stream_operation` (line 194)

---

### `core\threading\qthread_workers.py.MonitoringWorker`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 419
- **Bases:** StreamingWorker
- **Docstring:** Worker for continuous monitoring tasks.

This is a long-running operation that needs:
- Continuous m...

**Methods:**
- `configure_monitoring` (line 433)
- `start_monitoring` (line 458)
- `_stream_operation` (line 473)

---

### `core\threading\qthread_workers.py.StreamingWorker`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 20
- **Bases:** QObject
- **Docstring:** Base streaming worker for long-running operations with signal/slot communication.

Use this for:
- R...

**Methods:**
- `__init__` (line 38)
- `_log_thread_info` (line 49)
- `configure_streaming` (line 56)
- `reset_state` (line 81)
- `is_running` (line 103)
- `start_streaming` (line 107)
- `stop` (line 130)
- `_stream_operation` (line 140)

---

### `core\threading\thread_calculator.py.ThreadCalculator`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 53
- **Docstring:** Calculates optimal thread counts based on system capabilities...

**Methods:**
- `__init__` (line 56)
- `get_system_info` (line 59)
- `calculate_thread_recommendations` (line 120)
- `_calculate_recommendations` (line 190)
- `_calculate_memory_safe_threads` (line 301)
- `get_recommendations_for_pool` (line 320)
- `print_system_analysis` (line 345)

---

### `core\threading\thread_calculator.py.ThreadRecommendations`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 26
- **Decorators:** dataclass
- **Docstring:** Thread count recommendations for different use cases...

---

### `core\threading\thread_calculator_examples.py.DummyWorker`

- **File:** `core\threading\thread_calculator_examples.py`
- **Line:** 60

---

### `core\threading\thread_monitor.py.ThreadMonitor`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 19
- **Bases:** QObject
- **Docstring:** Monitor for tracking QThread and QRunnable usage across the application.

This monitor provides:
- T...

**Methods:**
- `__init__` (line 37)
- `register_thread` (line 62)
- `unregister_thread` (line 107)
- `record_thread_error` (line 138)
- `get_thread_info` (line 173)
- `get_all_threads_info` (line 202)
- `get_resource_usage` (line 221)
- `cleanup_old_history` (line 257)
- `_on_thread_started` (line 285)
- `_on_thread_finished` (line 298)
- `_update_monitoring` (line 325)
- `generate_report` (line 339)
- `shutdown` (line 384)
- `check_thread_safety` (line 405)
- `force_thread_cleanup` (line 439)
- `get_running_threads` (line 475)

---

### `core\threading\thread_pool_manager.py.ThreadPoolManager`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 22
- **Bases:** QObject
- **Docstring:** Manager for handling QRunnable tasks with proper resource management.

This manager provides:
- Glob...

**Methods:**
- `__init__` (line 39)
- `start_task` (line 74)
- `wait_for_task` (line 138)
- `wait_for_all_tasks` (line 166)
- `cancel_task` (line 193)
- `cancel_all_tasks` (line 229)
- `get_pool_status` (line 250)
- `get_task_info` (line 275)
- `cleanup_old_tasks` (line 309)
- `_update_pool_status` (line 337)
- `on_task_completed` (line 357)
- `on_task_failed` (line 385)
- `shutdown` (line 415)

---

### `core\threading\threading_service.py.ThreadingService`

- **File:** `core\threading\threading_service.py`
- **Line:** 27
- **Bases:** QObject
- **Docstring:** Service that manages all threading operations in the chat application.

This service provides:
- Uni...

**Methods:**
- `__init__` (line 44)
- `_initialize_persistent_pools` (line 102)
- `start_chat_streaming` (line 179)
- `stop_chat_streaming` (line 244)
- `start_audio_streaming` (line 273)
- `stop_audio_streaming` (line 320)
- `start_monitoring` (line 339)
- `stop_monitoring` (line 387)
- `_on_chat_chunk_received` (line 407)
- `_on_chat_progress_updated` (line 416)
- `_on_chat_streaming_finished` (line 423)
- `_on_chat_streaming_error` (line 437)
- `_on_audio_chunk_received` (line 451)
- `_on_audio_streaming_finished` (line 459)
- `_on_audio_streaming_error` (line 472)
- `_on_resource_updated` (line 485)
- `_on_alert_triggered` (line 493)
- `_on_monitoring_finished` (line 500)
- `_on_monitoring_error` (line 513)
- `process_message` (line 527)
- `process_file` (line 542)
- `process_data` (line 557)
- `get_threading_status` (line 572)
- `cleanup` (line 606)

---

### `core\threading\usage_examples.py.ChatApplicationExample`

- **File:** `core\threading\usage_examples.py`
- **Line:** 16
- **Docstring:** Example class showing how to use QThread and QRunnable in a chat application.

This demonstrates the...

**Methods:**
- `__init__` (line 25)
- `start_chat_streaming` (line 40)
- `_on_chat_streaming_thread_finished` (line 113)
- `stop_chat_streaming` (line 135)
- `process_message_spell_check` (line 158)
- `process_message_formatting` (line 191)
- `process_file_operation` (line 218)
- `_on_chat_chunk_received` (line 249)
- `_on_chat_progress_updated` (line 258)
- `_on_chat_streaming_finished` (line 267)
- `_on_chat_streaming_error` (line 276)
- `on_message_processed` (line 287)
- `on_message_processing_error` (line 309)
- `on_file_processed` (line 318)
- `on_file_processing_error` (line 333)
- `get_threading_status` (line 342)
- `cleanup` (line 367)

---

### `core\utils\error_handler.py.ErrorHandler`

- **File:** `core\utils\error_handler.py`
- **Line:** 22
- **Docstring:** Centralized error handling utilities...

**Methods:**
- `safe_execute` (line 26)
- `retry_on_failure` (line 51)
- `handle_network_errors` (line 93)
- `handle_file_operations` (line 127)
- `handle_audio_operations` (line 161)
- `handle_memory_operations` (line 184)
- `handle_ui_operations` (line 207)

---

### `core\utils\internet_checker.py.InternetConnectionTester`

- **File:** `core\utils\internet_checker.py`
- **Line:** 17
- **Docstring:** A utility class for testing internet connectivity.

Tests multiple reliable endpoints to determine i...

**Methods:**
- `__init__` (line 24)
- `test_socket_connection` (line 43)
- `test_http_connection` (line 60)
- `test_connection` (line 77)
- `test_connection_with_details` (line 96)

---

### `core\utils\prompts.py.PromptFormatter`

- **File:** `core\utils\prompts.py`
- **Line:** 85
- **Docstring:** Utility class for formatting prompts with dynamic content...

**Methods:**
- `format_fact_extraction_prompt` (line 89)
- `format_auto_model_selection_info` (line 96)
- `format_conversation_status` (line 101)
- `format_memory_status` (line 107)
- `format_error_message` (line 112)
- `format_status_message` (line 118)
- `get_menu_text` (line 124)

---

### `core\utils\prompts.py.PromptTemplates`

- **File:** `core\utils\prompts.py`
- **Line:** 11
- **Docstring:** Centralized prompt templates for the application...

---

### `core\utils\streaming_handler.py.StreamingHandler`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 15
- **Bases:** QObject
- **Docstring:** Streaming Handler - Business logic for message management and streaming...

**Methods:**
- `__init__` (line 21)
- `_get_next_message_id` (line 43)
- `set_render_callback` (line 48)
- `sync_messages_to_renderer` (line 52)
- `_request_render` (line 57)
- `_flush_stream_buffer` (line 66)
- `append_message` (line 83)
- `edit_message` (line 104)
- `get_message_by_id` (line 119)
- `get_editable_messages` (line 126)
- `get_messages` (line 139)
- `start_streaming_message` (line 143)
- `_process_typewriter_chunk` (line 158)
- `update_streaming_message` (line 180)
- `finalize_streaming_message` (line 195)
- `update_last_system_switch` (line 212)
- `remove_streaming_placeholder` (line 228)
- `clear_messages` (line 245)
- `cleanup` (line 250)

---

### `core\utils\threading_audit.py.ThreadSafetyAuditor`

- **File:** `core\utils\threading_audit.py`
- **Line:** 18
- **Docstring:** Comprehensive thread safety auditor for PySide6 applications.

This auditor analyzes the current sta...

**Methods:**
- `__init__` (line 26)
- `analyze_current_threads` (line 33)
- `detect_cross_thread_ui_operations` (line 103)
- `check_thread_safety_patterns` (line 126)
- `_get_thread_breakdown` (line 159)
- `generate_recommendations` (line 167)
- `run_full_analysis` (line 202)
- `generate_report` (line 218)
- `save_report` (line 272)

---

### `core\utils\threading_utils.py.ThreadSafeCallback`

- **File:** `core\utils\threading_utils.py`
- **Line:** 262
- **Docstring:** A thread-safe callback wrapper that ensures callbacks are executed in the main thread....

**Methods:**
- `__init__` (line 267)
- `__call__` (line 272)

---

### `features\chat\chat_controller.py.ChatController`

- **File:** `features\chat\chat_controller.py`
- **Line:** 41
- **Bases:** QObject
- **Docstring:** Controller class that mediates between UI components and business logic...

**Methods:**
- `__init__` (line 52)
- `is_memory_active` (line 74)
- `process_user_message` (line 78)
- `_handle_memory_operations` (line 127)
- `_extract_and_store_facts` (line 140)
- `_extract_facts_with_llm` (line 163)
- `_store_extracted_facts` (line 223)
- `_send_to_ollama` (line 248)
- `_detect_new_conversation` (line 273)
- `_build_context` (line 287)
- `_select_model` (line 293)
- `accumulate_assistant_response` (line 314)
- `clear_pending_assistant_response` (line 323)
- `start_streaming_response` (line 326)
- `finalize_streaming_response` (line 332)
- `handle_ai_response` (line 341)
- `_trigger_tts_for_response` (line 396)
- `set_chat_tab_reference` (line 429)
- `get_ai_name` (line 433)
- `_trigger_name_generation` (line 442)
- `start_new_conversation` (line 449)
- `clear_conversation` (line 496)
- `load_conversation` (line 502)
- `delete_conversation` (line 529)
- `rename_conversation` (line 542)
- `reset_ai_response_guard` (line 556)

---

### `features\chat\complexity_analyser\complexity_analyzer.py.ComplexityLevel`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 10
- **Bases:** Enum
- **Docstring:** Enumeration for complexity levels...

---

### `features\chat\complexity_analyser\complexity_analyzer.py.ComplexityMetrics`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 18
- **Decorators:** dataclass
- **Docstring:** Data class to hold complexity analysis results...

---

### `features\chat\complexity_analyser\complexity_analyzer.py.RequestComplexityAnalyzer`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 32
- **Docstring:** Analyzes the complexity of requests to help choose appropriate models...

**Methods:**
- `__init__` (line 35)
- `analyze_complexity` (line 115)
- `_estimate_tokens` (line 181)
- `_analyze_reasoning_depth` (line 187)
- `_analyze_knowledge_breadth` (line 223)
- `_analyze_ambiguity` (line 248)
- `_count_constraints` (line 267)
- `_analyze_context_dependency` (line 282)
- `_analyze_output_complexity` (line 302)
- `_determine_complexity_level` (line 322)
- `_generate_recommendations` (line 333)
- `get_model_recommendation` (line 375)
- `format_complexity_report` (line 396)

---

### `features\chat\conversation_service.py.ConversationService`

- **File:** `features\chat\conversation_service.py`
- **Line:** 15
- **Bases:** QObject
- **Docstring:** Service for managing conversation state and persistence...

**Methods:**
- `__init__` (line 21)
- `set_memory_service` (line 34)
- `set_conversation_manager` (line 38)
- `_get_next_message_id` (line 42)
- `add_message` (line 47)
- `start_streaming_message` (line 75)
- `update_streaming_message` (line 93)
- `finalize_streaming_message` (line 135)
- `get_streaming_message_id` (line 193)
- `get_streaming_message_with_content` (line 197)
- `get_message_by_id` (line 204)
- `update_message_by_id` (line 211)
- `_add_to_memory` (line 220)
- `get_messages` (line 255)
- `get_context_messages` (line 266)
- `load_conversation` (line 273)
- `clear_conversation` (line 366)

---

### `features\chat\enhancers\enhancement_service.py.EnhancementService`

- **File:** `features\chat\enhancers\enhancement_service.py`
- **Line:** 8
- **Docstring:** Service for response enhancement and follow-up detection...

**Methods:**
- `__init__` (line 11)
- `should_enhance_response` (line 14)
- `detect_follow_up_question` (line 25)
- `generate_enhanced_response` (line 34)

---

### `features\chat\summarization\summarization_service.py.SummarizationService`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 18
- **Bases:** QObject
- **Docstring:** Service for generating AI-powered conversation summaries and names...

**Methods:**
- `__init__` (line 25)
- `generate_chat_name` (line 31)
- `_create_summarization_prompt` (line 120)
- `_clean_generated_name` (line 145)
- `_has_enough_substance` (line 218)
- `_ai_evaluate_conversation_quality` (line 235)
- `_fallback_quality_check` (line 311)
- `_ai_evaluate_name_quality` (line 340)
- `set_summarization_model` (line 412)
- `set_min_messages_threshold` (line 416)

---

### `features\memory\memory_service.py.LongTermMemoryEntry`

- **File:** `features\memory\memory_service.py`
- **Line:** 38
- **Decorators:** dataclass
- **Docstring:** Represents a long-term memory entry...

**Methods:**
- `__post_init__` (line 51)

---

### `features\memory\memory_service.py.LongTermMemoryService`

- **File:** `features\memory\memory_service.py`
- **Line:** 381
- **Docstring:** Manages long-term memory storage and retrieval...

**Methods:**
- `__init__` (line 384)
- `_load` (line 389)
- `add_entry` (line 404)
- `get_entries` (line 414)
- `_save` (line 424)
- `update_access_stats` (line 434)

---

### `features\memory\memory_service.py.MemoryClassifier`

- **File:** `features\memory\memory_service.py`
- **Line:** 58
- **Docstring:** Intelligent classifier for determining memory type and importance...

**Methods:**
- `classify_message` (line 96)

---

### `features\memory\memory_service.py.MemoryEntry`

- **File:** `features\memory\memory_service.py`
- **Line:** 24
- **Decorators:** dataclass
- **Docstring:** Represents a single memory entry...

---

### `features\memory\memory_service.py.MemoryRetriever`

- **File:** `features\memory\memory_service.py`
- **Line:** 254
- **Docstring:** Retrieves relevant memories based on query similarity...

**Methods:**
- `calculate_relevance` (line 258)
- `get_relevant_memories` (line 308)

---

### `features\memory\memory_service.py.MemoryService`

- **File:** `features\memory\memory_service.py`
- **Line:** 443
- **Bases:** QObject
- **Docstring:** Service for managing LLM memory across conversations...

**Methods:**
- `__init__` (line 449)
- `_load_memory` (line 478)
- `_save_memory` (line 486)
- `_on_embeddings_updated` (line 494)
- `add_memory` (line 502)
- `add_summary` (line 547)
- `get_relevant_memories` (line 565)
- `intelligent_add_message` (line 618)
- `extract_facts_from_message` (line 679)
- `get_user_info` (line 708)
- `get_user_name` (line 723)
- `get_context_messages` (line 732)
- `summarize_conversation` (line 759)
- `clear_memory` (line 776)
- `_verify_memory_files_cleared` (line 801)
- `delete_memory` (line 820)
- `get_memory_stats` (line 831)
- `add_message` (line 885)
- `add_fact` (line 892)
- `set_max_context_messages` (line 909)
- `search_memories` (line 918)
- `clear` (line 947)
- `cleanup_memory_entries` (line 954)

---

### `features\memory\memory_service.py.PronounNormalizer`

- **File:** `features\memory\memory_service.py`
- **Line:** 165
- **Docstring:** Normalizes pronouns in user messages to avoid AI confusion...

**Methods:**
- `normalize_pronouns` (line 195)
- `should_normalize` (line 230)

---

### `features\memory\memory_service.py.ShortTermMemoryService`

- **File:** `features\memory\memory_service.py`
- **Line:** 327
- **Docstring:** Manages short-term memory (recent conversation context)...

**Methods:**
- `__init__` (line 330)
- `_load` (line 336)
- `add_message` (line 349)
- `get_messages` (line 359)
- `clear` (line 363)
- `_save` (line 371)

---

### `features\memory\semantic_search.py.SemanticSearchService`

- **File:** `features\memory\semantic_search.py`
- **Line:** 40
- **Bases:** QObject
- **Docstring:** Service for semantic memory retrieval using vector embeddings...

**Methods:**
- `__init__` (line 46)
- `_init_model` (line 64)
- `_load_embeddings` (line 82)
- `_save_embeddings` (line 116)
- `add_memory` (line 150)
- `remove_memory` (line 204)
- `search_semantic` (line 233)
- `search_hybrid` (line 286)
- `update_memory_importance` (line 365)
- `get_memory_stats` (line 392)
- `clear_all` (line 439)
- `is_ready` (line 466)

---

### `features\memory\semantic_search.py.VectorizedMemory`

- **File:** `features\memory\semantic_search.py`
- **Line:** 29
- **Decorators:** dataclass
- **Docstring:** Represents a memory entry with its vector embedding...

---

### `features\memory\semantic_search_fallback.py.SemanticSearchFallback`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 28
- **Bases:** QObject
- **Docstring:** Fallback service for memory retrieval using keyword matching...

**Methods:**
- `__init__` (line 34)
- `_load_memories` (line 49)
- `_save_memories` (line 77)
- `add_memory` (line 105)
- `remove_memory` (line 149)
- `_calculate_keyword_similarity` (line 177)
- `search_semantic` (line 215)
- `search_hybrid` (line 263)
- `update_memory_importance` (line 269)
- `get_memory_stats` (line 295)
- `clear_all` (line 343)
- `is_ready` (line 367)

---

### `features\memory\semantic_search_fallback.py.SimpleMemory`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 18
- **Decorators:** dataclass
- **Docstring:** Represents a memory entry with simple keyword matching...

---

### `features\ollama\ollama_chat.py.OllamaChat`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 20
- **Bases:** QMainWindow
- **Docstring:** Main application window - refactored with modular components...

**Methods:**
- `__init__` (line 23)
- `_setup_ui` (line 79)
- `showEvent` (line 107)
- `closeEvent` (line 112)
- `show_ollama_connection_error` (line 116)
- `check_ollama_connection` (line 120)
- `get_service_manager` (line 125)
- `get_ui_manager` (line 129)
- `get_event_handler` (line 133)
- `get_lifecycle_manager` (line 137)
- `get_chat_controller` (line 141)

---

### `features\ollama\ollama_service.py.OllamaService`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 25
- **Bases:** QObject
- **Docstring:** Enhanced service for handling all Ollama API communication with official library support using persi...

**Methods:**
- `__init__` (line 35)
- `get_models` (line 66)
- `_get_models_with_library` (line 73)
- `_get_models_with_requests` (line 133)
- `test_connection` (line 182)
- `send_chat_message` (line 211)
- `_send_chat_message_with_library` (line 233)
- `_send_chat_message_with_requests` (line 314)
- `pull_model` (line 412)
- `_pull_model_thread` (line 440)
- `remove_model` (line 489)
- `_remove_model_thread` (line 517)
- `update_model` (line 566)
- `_update_model_thread` (line 594)
- `_extract_system_prompt` (line 643)
- `_build_session_commands` (line 652)
- `cancel_request` (line 668)
- `reset_cancellation` (line 674)
- `is_connected` (line 679)
- `cleanup` (line 683)

---

### `features\personality\formatter.py.PersonalityFormatter`

- **File:** `features\personality\formatter.py`
- **Line:** 13
- **Docstring:** Handles formatting prompts and building system prompts with personality data...

**Methods:**
- `format_prompt_with_personality` (line 17)
- `build_comprehensive_system_prompt` (line 53)
- `get_system_prompt` (line 140)
- `get_personality_info` (line 147)
- `validate_personality_data` (line 173)
- `format_personality_summary` (line 204)
- `create_personality_template` (line 244)

---

### `features\personality\loader.py.PersonalityLoader`

- **File:** `features\personality\loader.py`
- **Line:** 21
- **Docstring:** Handles loading and saving personality data from/to files...

**Methods:**
- `__init__` (line 24)
- `find_personality_files` (line 36)
- `extract_personality_name` (line 54)
- `load_personality_from_file` (line 69)
- `load_all_personalities` (line 79)
- `save_personality_to_file` (line 91)
- `find_personality_file_by_name` (line 118)
- `delete_personality_file` (line 133)
- `create_personality_data` (line 145)
- `validate_personality_file` (line 163)
- `backup_personality` (line 182)
- `restore_personality_from_backup` (line 210)
- `get_personality_file_info` (line 241)
- `list_backup_files` (line 261)

---

### `features\personality\models\personality_model.py.PersonalityModel`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 15
- **Bases:** PersonalityService
- **Docstring:** Main class for managing AI personalities

This is the refactored version that inherits from Personal...

**Methods:**
- `__init__` (line 23)
- `service` (line 38)
- `_initialize_default_personalities` (line 42)
- `_find_personality_files` (line 49)
- `_extract_personality_name` (line 53)
- `_load_custom_personalities` (line 57)
- `_find_personality_file_by_name` (line 62)
- `save_custom_personality` (line 66)
- `get_personality_loader` (line 72)
- `get_personality_formatter` (line 76)
- `get_system_personalities` (line 80)
- `get_custom_personalities` (line 84)

---

### `features\personality\models\personality_pronouns.py.PersonalityPronouns`

- **File:** `features\personality\models\personality_pronouns.py`
- **Line:** 14
- **Decorators:** dataclass
- **Docstring:** Data class for personality pronoun configuration...

**Methods:**
- `get_user_titles` (line 37)
- `get_primary_title` (line 53)
- `get_random_title` (line 58)
- `get_formal_title` (line 63)
- `get_pronoun_guide` (line 80)
- `get_user_address` (line 123)
- `format_user_reference` (line 134)

---

### `features\personality\models\personality_types.py.PersonalityConfig`

- **File:** `features\personality\models\personality_types.py`
- **Line:** 46
- **Decorators:** dataclass
- **Docstring:** Data class for personality-specific configuration...

---

### `features\personality\models\personality_types.py.PersonalityMetadata`

- **File:** `features\personality\models\personality_types.py`
- **Line:** 57
- **Decorators:** dataclass
- **Docstring:** Data class for personality metadata...

**Methods:**
- `__post_init__` (line 66)

---

### `features\personality\models\personality_types.py.PersonalityPrompt`

- **File:** `features\personality\models\personality_types.py`
- **Line:** 72
- **Decorators:** dataclass
- **Docstring:** Data class for personality prompt templates...

---

### `features\personality\models\personality_types.py.PersonalityTraits`

- **File:** `features\personality\models\personality_types.py`
- **Line:** 28
- **Decorators:** dataclass
- **Docstring:** Data class for personality traits...

---

### `features\personality\models\personality_types.py.PersonalityType`

- **File:** `features\personality\models\personality_types.py`
- **Line:** 13
- **Bases:** Enum
- **Docstring:** Enumeration of available personality types...

---

### `features\personality\services\personality_service.py.PersonalityService`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 22
- **Docstring:** Main service for managing AI personalities...

**Methods:**
- `__init__` (line 25)
- `_initialize_personalities` (line 38)
- `is_system_personality` (line 63)
- `is_custom_personality` (line 72)
- `get_system_personalities` (line 76)
- `get_custom_personalities` (line 84)
- `get_available_personalities` (line 92)
- `get_personality` (line 96)
- `set_current_personality` (line 100)
- `get_current_personality` (line 107)
- `create_custom_personality` (line 113)
- `delete_custom_personality` (line 142)
- `update_custom_personality` (line 173)
- `refresh_personalities` (line 198)
- `format_prompt_with_personality` (line 219)
- `get_system_prompt` (line 238)
- `get_personality_info` (line 255)
- `get_personality_config` (line 260)
- `update_personality_metadata` (line 271)
- `build_comprehensive_system_prompt` (line 295)
- `get_user_context_messages` (line 306)
- `get_personality_categories` (line 374)
- `get_personalities_by_category` (line 385)
- `get_personalities_by_folder` (line 398)
- `search_personalities` (line 408)
- `get_selected_model` (line 437)
- `get_ai_name` (line 441)
- `get_temperature` (line 448)

---

### `features\user\user_profile_service.py.UserProfileService`

- **File:** `features\user\user_profile_service.py`
- **Line:** 7
- **Docstring:** Service for managing user profiles and preferences....

**Methods:**
- `__init__` (line 10)
- `get_user_profile` (line 13)
- `update_user_profile` (line 17)

---

### `features\voice\audio\recording_service.py.RecordingService`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 13
- **Bases:** QObject
- **Docstring:** Audio recording service for capturing voice input...

**Methods:**
- `__init__` (line 23)
- `__del__` (line 52)
- `_check_availability` (line 58)
- `is_available` (line 73)
- `is_initialized` (line 76)
- `start_recording` (line 80)
- `_record_audio` (line 100)
- `_calculate_audio_level` (line 219)
- `audio_level_to_db` (line 233)
- `get_current_audio_level` (line 244)
- `set_audio_gate_enabled` (line 247)
- `set_speech_detection_parameters` (line 254)
- `get_speech_detection_parameters` (line 264)
- `cleanup` (line 273)
- `stop_recording` (line 282)

---

### `features\voice\orchestrator\voice_process_manager.py.VoiceProcessManager`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 20
- **Bases:** QObject
- **Docstring:** Manages voice services in a separate process...

**Methods:**
- `__init__` (line 37)
- `start_voice_process` (line 48)
- `stop_voice_process` (line 105)
- `send_command` (line 185)
- `_handle_response` (line 202)
- `_handle_monitor_error` (line 242)
- `is_process_running` (line 250)
- `get_process_info` (line 256)

---

### `features\voice\orchestrator\voice_process_manager.py.VoiceProcessMonitor`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 273
- **Bases:** QThread
- **Docstring:** Thread to monitor responses from the voice process...

**Methods:**
- `__init__` (line 279)
- `run` (line 290)
- `stop` (line 325)
- `get_stats` (line 340)

---

### `features\voice\stt\stt_service.py.STTService`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 10
- **Bases:** QObject
- **Docstring:** Speech-to-Text service for converting voice to text...

**Methods:**
- `__init__` (line 16)
- `_check_availability` (line 22)
- `is_available` (line 44)
- `is_initialized` (line 47)
- `convert_audio_to_text` (line 51)
- `_convert_with_vosk` (line 58)
- `update_api` (line 91)
- `process_audio_file` (line 95)

---

### `features\voice\tts\streaming_audio_player.py.StreamingAudioPlayer`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 14
- **Bases:** QThread
- **Docstring:** Thread for streaming audio playback...

**Methods:**
- `__init__` (line 23)
- `__del__` (line 41)
- `run` (line 47)
- `_process_audio_chunk` (line 155)
- `set_volume` (line 278)
- `add_audio_chunk` (line 282)
- `end_stream` (line 293)
- `stop_playback` (line 301)
- `cleanup` (line 329)

---

### `features\voice\tts\streaming_audio_worker.py.StreamingAudioWorker`

- **File:** `features\voice\tts\streaming_audio_worker.py`
- **Line:** 13
- **Bases:** QObject
- **Docstring:** Worker for streaming audio generation in a separate thread...

**Methods:**
- `__init__` (line 20)
- `run` (line 27)
- `_split_text_into_sentences` (line 65)
- `_generate_audio_chunk` (line 84)
- `_adjust_audio_speed` (line 127)
- `stop` (line 146)

---

### `features\voice\tts\tts_service.py.TTSService`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 17
- **Bases:** QObject
- **Docstring:** Text-to-Speech service for converting text to speech

Always use TTSService.get_instance() to access...

**Methods:**
- `get_instance` (line 34)
- `__init__` (line 40)
- `_check_availability` (line 66)
- `is_available` (line 75)
- `is_initialized` (line 78)
- `speak_text` (line 82)
- `speak_text_streaming` (line 97)
- `speak_text_non_streaming` (line 113)
- `_speak_with_espeak` (line 130)
- `_simulate_tts_finished` (line 153)
- `stop_playback` (line 156)
- `update_api` (line 165)
- `update_voice` (line 173)
- `update_speed` (line 181)
- `is_coqui_available` (line 190)
- `get_coqui_models` (line 194)
- `get_coqui_voices` (line 200)
- `get_coqui_model_info` (line 206)
- `load_coqui_model` (line 212)
- `set_coqui_model` (line 218)
- `cleanup` (line 227)

---

### `features\voice\voice_service.py.VoiceService`

- **File:** `features\voice\voice_service.py`
- **Line:** 23
- **Bases:** QObject
- **Docstring:** Voice service for handling voice input/output functionality using persistent threading architecture...

**Methods:**
- `get_instance` (line 46)
- `__init__` (line 51)
- `_setup_connections` (line 117)
- `_setup_service_connections` (line 154)
- `_on_recording_started` (line 197)
- `_on_recording_stopped` (line 203)
- `_on_recording_error` (line 209)
- `_on_recording_auto_stopped` (line 215)
- `_on_recording_auto_stopped_for_stt` (line 220)
- `_on_recording_timeout` (line 249)
- `is_voice_available` (line 255)
- `can_handle_new_request` (line 285)
- `queue_request` (line 292)
- `_process_request_queue` (line 312)
- `_handle_voice_input_request` (line 339)
- `_handle_tts_request` (line 366)
- `_complete_request` (line 400)
- `clear_request_queue` (line 409)
- `cancel_current_request` (line 437)
- `handle_user_interruption` (line 462)
- `_on_audio_level_changed` (line 494)
- `start_voice_input` (line 515)
- `stop_voice_input` (line 549)
- `_on_stt_text_received` (line 568)
- `_restart_voice_input_safely` (line 636)
- `_on_stt_error` (line 664)
- `_on_tts_started` (line 699)
- `_on_tts_finished` (line 723)
- `_on_tts_error` (line 759)
- `speak_text` (line 789)
- `_speak_text_impl` (line 821)
- `stop_tts` (line 864)
- `set_continuous_voice_mode` (line 887)
- `is_continuous_voice_mode` (line 892)
- `update_settings` (line 896)
- `get_silence_duration` (line 901)
- `get_silence_threshold` (line 905)
- `get_recording_timeout` (line 909)
- `get_current_audio_level` (line 913)
- `set_recording_timeout` (line 919)
- `set_silence_duration` (line 923)
- `set_silence_threshold` (line 927)
- `set_audio_gate_enabled` (line 931)
- `cleanup_on_exit` (line 937)
- `get_audio_folder_path` (line 1000)
- `list_audio_files` (line 1004)
- `cleanup_old_audio_files` (line 1026)
- `cleanup_all_audio_files` (line 1059)
- `_forward_recording_started` (line 1078)
- `_forward_recording_stopped` (line 1086)
- `_forward_recording_error` (line 1094)
- `_forward_voice_processing_started` (line 1102)
- `_cleanup_resources` (line 1110)
- `_reset_error_count` (line 1144)
- `_connect_signals` (line 1149)
- `_initialize_services` (line 1155)
- `_check_and_emit_ready` (line 1229)

---

### `features\voice\voice_service_manager.py.VoiceServiceManager`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 17
- **Bases:** QObject
- **Docstring:** Singleton manager for voice service initialization and management...

**Methods:**
- `__new__` (line 28)
- `__init__` (line 36)
- `get_voice_service` (line 58)
- `_initialize_voice_service` (line 76)
- `_on_voice_service_ready` (line 139)
- `_try_get_from_service_manager` (line 144)
- `_try_direct_initialization` (line 162)
- `_reset_voice_service` (line 175)
- `update_settings` (line 192)
- `get_settings` (line 210)
- `is_ready` (line 220)
- `is_initializing` (line 226)
- `get_last_error` (line 230)
- `register_ready_callback` (line 234)
- `force_reinitialize` (line 251)
- `cleanup` (line 257)

---

### `features\voice\voice_service_wrapper.py.VoiceServiceWrapper`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 14
- **Bases:** QObject
- **Docstring:** Wrapper for voice services that runs in a separate process...

**Methods:**
- `__init__` (line 33)
- `_init_process_manager` (line 49)
- `_init_direct_service` (line 70)
- `start_voice_input` (line 98)
- `stop_voice_input` (line 112)
- `speak_text` (line 126)
- `speak_text_streaming` (line 140)
- `speak_text_non_streaming` (line 154)
- `stop_tts` (line 168)
- `is_voice_available` (line 182)
- `update_settings` (line 191)
- `get_recording_timeout` (line 200)
- `set_recording_timeout` (line 206)
- `get_silence_duration` (line 211)
- `set_silence_duration` (line 217)
- `get_silence_threshold` (line 222)
- `set_silence_threshold` (line 228)
- `set_audio_gate_enabled` (line 233)
- `get_current_audio_level` (line 238)
- `set_continuous_voice_mode` (line 244)
- `is_continuous_voice_mode` (line 253)
- `cleanup_on_exit` (line 259)
- `get_audio_folder_path` (line 266)
- `list_audio_files` (line 272)
- `cleanup_old_audio_files` (line 278)
- `cleanup_all_audio_files` (line 283)
- `get_process_info` (line 288)
- `test_connection` (line 294)
- `_update_cached_state` (line 300)
- `_update_cached_state_from_signal` (line 306)
- `is_recording` (line 311)
- `is_processing_voice` (line 318)
- `is_playing_tts` (line 325)
- `recording_service` (line 332)
- `_on_voice_service_ready` (line 338)
- `_check_service_readiness` (line 351)

---

### `startup\dependency_checker.py.DependencyChecker`

- **File:** `startup\dependency_checker.py`
- **Line:** 17
- **Docstring:** Handles dependency checking and installation....

**Methods:**
- `__init__` (line 20)
- `test_import` (line 26)
- `check_core_dependencies` (line 42)
- `check_ml_dependencies` (line 83)
- `check_tts_options` (line 102)
- `check_package_versions` (line 118)
- `run_comprehensive_check` (line 155)
- `get_missing_dependencies` (line 166)
- `get_version_conflicts` (line 170)
- `run_install_dependencies` (line 174)
- `get_dependency_summary` (line 199)

---

### `ui\Widgets\chat_navigation.py.ChatNavigationWidget`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 15
- **Bases:** QWidget
- **Docstring:** Widget for navigating between previous conversations...

**Methods:**
- `__init__` (line 24)
- `setup_ui` (line 35)
- `setup_connections` (line 149)
- `refresh_conversations` (line 161)
- `create_conversation_item` (line 191)
- `on_conversation_double_clicked` (line 212)
- `show_context_menu` (line 218)
- `rename_conversation` (line 255)
- `delete_conversation` (line 292)
- `set_current_conversation` (line 319)
- `get_selected_conversation` (line 324)
- `clear_all_conversations` (line 331)
- `trigger_name_generation` (line 354)
- `on_summarization_completed` (line 386)
- `on_summarization_failed` (line 412)

---

### `ui\Widgets\complexity_widget.py.ComplexityWidget`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 3
- **Bases:** QWidget
- **Docstring:** Widget to display request complexity analysis...

**Methods:**
- `__init__` (line 8)
- `setup_ui` (line 14)
- `analyze_request` (line 107)
- `_update_display` (line 127)
- `_update_model_recommendation` (line 179)
- `_on_switch_model` (line 185)
- `_set_widget_color` (line 190)
- `_set_progress_bar_color` (line 196)
- `_get_color_for_value` (line 212)
- `clear_analysis` (line 226)
- `get_current_metrics` (line 234)

---

### `ui\Widgets\message_editor.py.EditableMessageWidget`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 7
- **Bases:** QWidget
- **Docstring:** Widget for displaying and editing user messages...

**Methods:**
- `__init__` (line 14)
- `setup_ui` (line 24)
- `setup_styles` (line 86)
- `start_editing` (line 165)
- `save_edit` (line 174)
- `cancel_edit` (line 184)
- `finish_editing` (line 189)
- `get_content` (line 195)
- `set_content` (line 199)

---

### `ui\Widgets\spellchecker_widget.py.SpellCheckerTextEdit`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 20
- **Bases:** QTextEdit
- **Docstring:** Custom QTextEdit with spell checking functionality...

**Methods:**
- `__init__` (line 23)
- `setup_spellchecker` (line 33)
- `setup_context_menu` (line 50)
- `show_context_menu` (line 55)
- `replace_word` (line 99)
- `add_to_dictionary` (line 109)
- `ignore_word` (line 120)
- `highlight_misspelled_words` (line 124)
- `keyPressEvent` (line 169)
- `on_text_changed` (line 179)
- `enable_spellcheck` (line 186)
- `disable_spellcheck` (line 193)
- `cleanup` (line 205)

---

### `ui\dialogs\coqui_model_dialog.py.CoquiModelDialog`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 43
- **Bases:** QDialog
- **Docstring:** Dialog for selecting Coqui TTS models and speakers...

**Methods:**
- `__init__` (line 49)
- `setup_ui` (line 65)
- `create_model_panel` (line 194)
- `create_speaker_panel` (line 223)
- `load_models` (line 246)
- `on_model_selected` (line 275)
- `load_speakers_for_model` (line 296)
- `on_speaker_selected` (line 329)
- `download_selected_model` (line 335)
- `start_download` (line 351)
- `on_download_completed` (line 363)
- `update_selection_button` (line 378)
- `accept_selection` (line 385)
- `log_status` (line 393)
- `get_current_time` (line 401)

---

### `ui\dialogs\coqui_model_dialog.py.ModelDownloadThread`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 16
- **Bases:** QThread
- **Docstring:** Thread for downloading Coqui TTS models...

**Methods:**
- `__init__` (line 21)
- `run` (line 25)

---

### `ui\dialogs\error_dialog.py.DetailedErrorDialog`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 111
- **Bases:** QDialog
- **Docstring:** Detailed error dialog with expandable details and copy functionality...

**Methods:**
- `__init__` (line 114)
- `setup_ui` (line 126)
- `setup_styles` (line 183)
- `copy_error` (line 226)
- `reset_copy_button` (line 258)
- `accept` (line 278)

---

### `ui\dialogs\error_dialog.py.ErrorDialog`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 9
- **Bases:** QMessageBox
- **Docstring:** Custom error dialog with copy button functionality...

**Methods:**
- `__init__` (line 12)
- `copy_error` (line 60)
- `reset_copy_button` (line 91)

---

### `ui\dialogs\settings_dialog.py.SettingsDialog`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 7
- **Bases:** QDialog
- **Docstring:** Dialog for configuring application settings...

**Methods:**
- `__init__` (line 10)
- `setup_ui` (line 21)
- `create_general_tab` (line 65)
- `create_chat_tab` (line 129)
- `create_session_tab` (line 180)
- `create_developer_tab` (line 220)
- `_delayed_load_settings` (line 238)
- `load_current_settings` (line 243)
- `save_settings` (line 303)
- `reset_to_defaults` (line 354)

---

### `ui\dialogs\voice_settings_dialog.py.CalibrateSilenceThresholdDialog`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1396
- **Bases:** QDialog

**Methods:**
- `__init__` (line 1397)
- `_start_step` (line 1423)
- `_start_recording` (line 1437)
- `_on_timer` (line 1443)
- `_finish` (line 1470)
- `get_result` (line 1491)

---

### `ui\dialogs\voice_settings_dialog.py.InternetCheckThread`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 26
- **Bases:** QThread
- **Docstring:** Thread for checking internet connectivity...

**Methods:**
- `run` (line 30)

---

### `ui\dialogs\voice_settings_dialog.py.VoiceSettingsDialog`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 39
- **Bases:** QDialog
- **Docstring:** Dialog for configuring voice settings...

**Methods:**
- `__init__` (line 46)
- `setup_ui` (line 153)
- `create_stt_tab` (line 292)
- `create_tts_tab` (line 333)
- `create_general_tab` (line 456)
- `setup_connections` (line 629)
- `check_internet_connection` (line 646)
- `on_internet_check_completed` (line 656)
- `update_api_availability` (line 671)
- `on_stt_api_changed` (line 697)
- `refresh_coqui_ui` (line 711)
- `_on_voices_loaded` (line 753)
- `on_tts_api_changed` (line 781)
- `on_voice_changed` (line 815)
- `on_eq_visualizer_changed` (line 819)
- `load_coqui_models` (line 828)
- `on_coqui_model_changed` (line 832)
- `load_coqui_speakers` (line 867)
- `get_speaker_info` (line 873)
- `filter_speakers` (line 936)
- `on_coqui_speaker_changed` (line 986)
- `preview_selected_speaker` (line 1018)
- `download_selected_model` (line 1066)
- `on_silence_threshold_changed` (line 1093)
- `test_settings` (line 1116)
- `save_settings` (line 1172)
- `get_settings` (line 1254)
- `set_settings` (line 1258)
- `on_tts_settings_changed` (line 1379)
- `open_calibration_dialog` (line 1388)

---

### `ui\tabs\chat_tab\chat_display.py.ChatDisplay`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 14
- **Bases:** QObject
- **Docstring:** Chat Display component for message display and editing...

**Methods:**
- `__init__` (line 20)
- `setup_ui_components` (line 35)
- `setup_chat_renderer` (line 63)
- `_sync_messages_from_conversation_service` (line 80)
- `sync_messages_from_conversation_service` (line 130)
- `get_ai_name` (line 138)
- `chat_display_mouse_move_event` (line 144)
- `show_edit_button` (line 170)
- `hide_edit_button` (line 204)
- `edit_message_at_index` (line 212)
- `show_message_edit_dialog` (line 223)
- `save_message_edit` (line 312)
- `on_render_completed` (line 331)
- `on_render_error` (line 336)
- `on_message_edited` (line 347)
- `append_to_chat` (line 354)
- `force_update_display` (line 380)
- `_force_render_display` (line 391)
- `append_response_chunk` (line 410)
- `start_streaming` (line 449)
- `stop_streaming` (line 461)
- `clear_chat` (line 477)
- `get_ui_components` (line 488)
- `get_streaming_handler` (line 495)

---

### `ui\tabs\chat_tab\chat_renderer.py.ChatRenderer`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 15
- **Bases:** QObject
- **Docstring:** Localized chat renderer that handles all UI rendering logic...

**Methods:**
- `__init__` (line 22)
- `_get_next_message_id` (line 58)
- `add_message` (line 63)
- `append_message` (line 81)
- `edit_message` (line 88)
- `update_last_system_switch` (line 100)
- `_get_current_streaming_message` (line 116)
- `start_streaming_message` (line 123)
- `_process_typewriter_chunk` (line 134)
- `update_streaming_message` (line 156)
- `finalize_streaming_message` (line 193)
- `clear_chat` (line 208)
- `update_message` (line 214)
- `get_messages` (line 223)
- `clear_messages` (line 227)
- `sync_messages_from_handler` (line 232)
- `sync_messages_from_conversation` (line 237)
- `request_render` (line 248)
- `_execute_render` (line 274)
- `_emergency_reset` (line 306)
- `_reset_render_counter` (line 317)
- `_render_chat_display` (line 321)
- `cleanup` (line 478)

---

### `ui\tabs\chat_tab\chat_tab.py.ChatTab`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 37
- **Bases:** QWidget
- **Docstring:** Main chat interface tab that orchestrates all components...

**Methods:**
- `__init__` (line 51)
- `setup_components` (line 81)
- `setup_ui` (line 100)
- `setup_connections` (line 260)
- `_on_conversation_updated` (line 301)
- `on_message_sent` (line 309)
- `on_message_cancelled` (line 341)
- `_ensure_voice_controls_initialized` (line 346)
- `on_voice_status_changed` (line 438)
- `on_input_mode_changed` (line 446)
- `on_temperature_changed` (line 518)
- `on_personality_changed` (line 523)
- `on_model_changed` (line 528)
- `on_eq_mode_changed` (line 533)
- `on_user_interrupted` (line 542)
- `on_request_cancelled` (line 559)
- `on_voice_input_received` (line 576)
- `on_voice_input_received_direct` (line 598)
- `process_voice_input` (line 621)
- `on_voice_input_error` (line 654)
- `on_tts_started` (line 664)
- `on_tts_finished` (line 677)
- `on_tts_error` (line 718)
- `on_recording_started` (line 728)
- `on_recording_stopped` (line 735)
- `on_recording_error` (line 742)
- `on_voice_processing_started` (line 752)
- `on_voice_processing_finished` (line 759)
- `on_audio_level_changed` (line 766)
- `on_eq_bars_changed` (line 808)
- `on_message_edited` (line 823)
- `get_ai_name` (line 829)
- `get_current_personality` (line 865)
- `get_current_model` (line 869)
- `get_temperature` (line 873)
- `get_current_response` (line 877)
- `append_to_chat` (line 881)
- `_force_chat_display_update` (line 901)
- `append_response_chunk` (line 926)
- `_append_response_chunk_safe` (line 931)
- `_ensure_chat_display_visible` (line 955)
- `start_streaming` (line 983)
- `_start_streaming_safe` (line 988)
- `stop_streaming` (line 1035)
- `force_enable_send_button` (line 1071)
- `_force_enable_send_button_safe` (line 1076)
- `clear_chat` (line 1098)
- `update_model_list` (line 1102)
- `update_personality_list` (line 1106)
- `speak_ai_response` (line 1110)
- `open_voice_settings` (line 1133)
- `on_eq_visualizer_changed_immediate` (line 1182)
- `on_eq_visualizer_changed_from_voice_controls` (line 1199)
- `on_voice_settings_changed` (line 1216)
- `load_conversation` (line 1227)
- `_load_conversation_fallback` (line 1276)
- `refresh_navigation` (line 1323)
- `set_current_conversation_file` (line 1328)
- `set_chat_controller` (line 1333)
- `get_streaming_handler` (line 1354)
- `streaming_handler` (line 1359)
- `finalize_streaming_and_start_tts` (line 1363)

---

### `ui\tabs\chat_tab\eq_visualizer.py.EQVisualizer`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 19
- **Bases:** QObject
- **Docstring:** EQ Visualizer component for audio visualization...

**Methods:**
- `__init__` (line 25)
- `setup_eq_visualizers` (line 37)
- `switch_to_eq_visualizer` (line 51)
- `switch_to_chat_display` (line 152)
- `update_eq_visualizer` (line 247)
- `_update_eq_widget_safe` (line 378)
- `is_eq_visualizer_active` (line 391)
- `update_eq_visualizer_mode` (line 397)
- `get_eq_mode` (line 405)
- `get_available_eq_modes` (line 409)

---

### `ui\tabs\chat_tab\input_controls.py.InputControls`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 12
- **Bases:** QObject
- **Docstring:** Input Controls component for message input and settings...

**Methods:**
- `__init__` (line 23)
- `setup_ui_components` (line 38)
- `setup_connections` (line 210)
- `set_input_mode` (line 228)
- `on_temperature_changed` (line 247)
- `on_personality_combo_changed` (line 254)
- `on_model_changed` (line 260)
- `send_message` (line 265)
- `cancel_message` (line 286)
- `start_streaming` (line 291)
- `stop_streaming` (line 314)
- `force_enable_send_button` (line 340)
- `update_model_list` (line 360)
- `update_personality_list` (line 372)
- `get_current_model` (line 383)
- `get_temperature` (line 387)
- `get_current_response` (line 391)
- `get_current_personality` (line 395)
- `get_ui_components` (line 399)
- `eventFilter` (line 413)

---

### `ui\tabs\chat_tab\voice_controls.py.VoiceControls`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 35
- **Bases:** QObject
- **Docstring:** Voice Controls component for voice mode, TTS, and audio level handling...

**Methods:**
- `__init__` (line 60)
- `setup_ui_components` (line 138)
- `_update_voice_button_state` (line 245)
- `_update_voice_state` (line 312)
- `is_voice_busy` (line 317)
- `_handle_voice_crash` (line 322)
- `_attempt_recovery` (line 335)
- `_stop_all_voice_operations` (line 345)
- `_reset_voice_ui` (line 357)
- `_reinitialize_voice_service` (line 368)
- `_disable_voice_features` (line 379)
- `_reset_error_count` (line 388)
- `_handle_service_error` (line 392)
- `setup_connections` (line 406)
- `_initialize_voice_service_manager` (line 414)
- `force_ui_refresh` (line 492)
- `_on_voice_service_ready` (line 522)
- `_on_direct_voice_service_ready` (line 550)
- `_periodic_ui_refresh` (line 565)
- `_on_voice_service_error` (line 586)
- `_on_voice_service_initializing` (line 596)
- `get_voice_service` (line 606)
- `_setup_voice_connections` (line 630)
- `_disconnect_voice_signals` (line 732)
- `reset_voice_signal_connections` (line 774)
- `_is_voice_service_ready` (line 778)
- `_validate_voice_service_capabilities` (line 803)
- `reset_voice_service` (line 825)
- `toggle_voice_mode` (line 856)
- `_start_continuous_voice_mode` (line 952)
- `_handle_voice_input_safe` (line 1004)
- `_handle_tts_finished_continuous` (line 1075)
- `_restart_voice_input` (line 1086)
- `_reset_voice_button` (line 1101)
- `on_voice_input_received` (line 1123)
- `on_voice_input_error` (line 1136)
- `_handle_voice_input_error_safe` (line 1151)
- `on_tts_started` (line 1181)
- `on_tts_finished` (line 1192)
- `on_tts_error` (line 1209)
- `_handle_tts_error_safe` (line 1225)
- `on_recording_started` (line 1229)
- `_handle_recording_started_safe` (line 1237)
- `on_recording_stopped` (line 1259)
- `_handle_recording_stopped_safe` (line 1267)
- `on_recording_error` (line 1282)
- `_handle_recording_error_safe` (line 1290)
- `on_voice_processing_started` (line 1306)
- `on_voice_processing_finished` (line 1313)
- `on_audio_level_changed` (line 1319)
- `_update_audio_level_ui_safe` (line 1356)
- `speak_ai_response` (line 1417)
- `update_voice_settings` (line 1435)
- `get_voice_settings` (line 1451)
- `is_voice_service_ready` (line 1461)
- `is_voice_service_initializing` (line 1471)
- `get_voice_service_error` (line 1481)
- `force_reinitialize_voice_service` (line 1487)
- `is_voice_mode_active` (line 1497)
- `is_tts_playing` (line 1501)
- `can_handle_interruption` (line 1512)
- `get_interruption_threshold` (line 1523)
- `get_ui_components` (line 1534)
- `on_user_interrupted` (line 1542)
- `on_request_cancelled` (line 1557)
- `on_eq_bars_changed` (line 1573)
- `_update_eq_bars` (line 1577)
- `_restart_voice_input_after_interruption` (line 1602)
- `_restart_voice_input_after_cancellation` (line 1617)
- `_clear_last_voice_input` (line 1632)
- `_is_similar_voice_input` (line 1645)
- `_reset_duplicate_detection_state` (line 1677)
- `cleanup` (line 1690)
- `__del__` (line 1716)
- `_on_voice_input_received` (line 1723)
- `_on_voice_input_error` (line 1744)
- `_on_tts_started` (line 1763)
- `_on_tts_finished` (line 1781)
- `_on_tts_error` (line 1799)
- `_on_recording_started` (line 1820)
- `_on_recording_stopped` (line 1838)
- `_on_recording_error` (line 1856)
- `_on_audio_level_changed` (line 1878)
- `_on_eq_bars_changed` (line 1891)
- `_on_voice_status_changed` (line 1904)
- `update_voice_status` (line 1920)

---

### `ui\tabs\memory_tab.py.MemoryTab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 31
- **Bases:** QWidget
- **Docstring:** Memory management tab for LLM memory settings and overview...

**Methods:**
- `__init__` (line 34)
- `setup_ui` (line 41)
- `create_settings_tab` (line 67)
- `create_overview_tab` (line 127)
- `create_memories_tab` (line 187)
- `create_summaries_tab` (line 252)
- `setup_connections` (line 282)
- `update_context_messages` (line 306)
- `refresh_data` (line 311)
- `refresh_overview` (line 317)
- `refresh_memories` (line 373)
- `refresh_summaries` (line 404)
- `search_memories` (line 417)
- `show_memory_details` (line 439)
- `show_summary_details` (line 473)
- `summarize_current_conversation` (line 489)
- `set_conversation_service` (line 495)
- `_summarize_with_service` (line 502)
- `clear_all_memories` (line 523)
- `cleanup_memory_entries` (line 536)
- `delete_selected_memory` (line 552)

---

### `ui\tabs\model_tab.py.ModelTab`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 7
- **Bases:** QWidget
- **Docstring:** Model management tab...

**Methods:**
- `__init__` (line 15)
- `setup_ui` (line 38)
- `setup_model_list` (line 55)
- `setup_operations` (line 131)
- `setup_connections` (line 351)
- `refresh_models` (line 361)
- `update_model_list` (line 369)
- `pull_model` (line 379)
- `remove_selected_model` (line 397)
- `update_selected_model` (line 417)
- `on_model_selection_changed` (line 437)
- `start_operation` (line 444)
- `stop_operation` (line 453)
- `append_status` (line 461)
- `get_current_time` (line 470)
- `on_operation_progress` (line 475)
- `on_operation_finished` (line 479)
- `on_operation_error` (line 487)
- `get_selected_model` (line 493)
- `clear_status` (line 498)

---

### `ui\tabs\personality_tab.py.PersonalityTab`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 12
- **Bases:** QWidget
- **Docstring:** Personality management tab...

**Methods:**
- `__init__` (line 18)
- `setup_ui` (line 25)
- `setup_selection_tab` (line 85)
- `setup_creation_tab` (line 192)
- `setup_management_tab` (line 511)
- `load_personalities` (line 684)
- `update_system_personalities_list` (line 724)
- `update_custom_personalities_list` (line 736)
- `on_system_personality_selected` (line 747)
- `update_system_personality_info` (line 753)
- `on_custom_personality_selected` (line 774)
- `on_personality_changed` (line 780)
- `update_personality_info` (line 786)
- `create_personality` (line 809)
- `clear_creation_form` (line 923)
- `delete_custom_personality` (line 965)
- `export_personality` (line 998)
- `refresh_personalities` (line 1019)
- `get_current_personality` (line 1028)
- `get_system_prompt` (line 1032)
- `get_available_personalities` (line 1043)
- `on_conversation_style_changed` (line 1051)
- `on_context_template_changed` (line 1059)
- `get_user_prompt_template` (line 1067)
- `get_context_prompt` (line 1078)

---

### `ui\tabs\tab_styles.py.TabStyles`

- **File:** `ui\tabs\tab_styles.py`
- **Line:** 9
- **Docstring:** Centralized tab styling for the application...

**Methods:**
- `get_tab_style` (line 40)

---

### `ui\themes\message_formatter.py.MessageFormatter`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 15
- **Docstring:** Utility class for formatting messages with code highlighting and HTML processing...

**Methods:**
- `detect_code_in_message` (line 19)
- `detect_code_type` (line 48)
- `syntax_highlight_code` (line 60)
- `detect_and_format_code` (line 97)
- `_protect_code_blocks` (line 133)
- `format_markdown` (line 149)
- `handle_html_tags` (line 221)
- `cleanup_message` (line 250)
- `format_chat_message` (line 278)
- `split_thoughts_and_answer` (line 315)
- `to_plain_text` (line 331)

---

### `ui\ui_manager.py.UIManager`

- **File:** `ui\ui_manager.py`
- **Line:** 24
- **Docstring:** Manages UI setup, menu creation, and styling...

**Methods:**
- `__init__` (line 27)
- `setup_ui` (line 41)
- `setup_menu_bar` (line 95)
- `apply_theme` (line 176)
- `update_status` (line 189)
- `get_menu_action` (line 198)
- `get_main_window` (line 202)
- `get_chat_tab` (line 206)
- `get_model_tab` (line 210)
- `get_personality_tab` (line 214)
- `get_memory_tab` (line 218)
- `get_tabs` (line 222)
- `show_about_dialog` (line 226)
- `show_clear_chat_dialog` (line 234)

---

### `ui\visualizers\widgets\bar_eq_widget.py.BarEQWidget`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 3
- **Bases:** QWidget
- **Docstring:** A bar equalizer widget that displays audio frequency data as animated bars.

This widget renders a s...

**Methods:**
- `__init__` (line 23)
- `_setup_animation_timer` (line 47)
- `_animate` (line 53)
- `set_eq_bars` (line 66)
- `set_idle` (line 102)
- `start_animation` (line 107)
- `stop_animation` (line 111)
- `get_current_values` (line 115)
- `_calculate_bar_geometry` (line 129)
- `_create_bar_gradient` (line 158)
- `_draw_bar` (line 212)
- `paintEvent` (line 241)

---

### `ui\visualizers\widgets\circle_eq_widget.py.CircleEQWidget`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 4
- **Bases:** QWidget
- **Docstring:** A simplified circular equalizer widget that displays audio frequency data in circular sections.

Thi...

**Methods:**
- `__init__` (line 22)
- `_setup_animation_timer` (line 46)
- `_animate` (line 52)
- `set_eq_sections` (line 66)
- `set_idle` (line 102)
- `start_animation` (line 107)
- `stop_animation` (line 111)
- `get_current_values` (line 115)
- `_create_section_gradient` (line 129)
- `paintEvent` (line 169)

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py.CircularGradientEQWidget`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 5
- **Bases:** QWidget
- **Docstring:** Like CircularNetEQWidget, but fills the area defined by the animated points with a soft, faded gradi...

**Methods:**
- `__init__` (line 15)
- `_smooth_radii` (line 39)
- `_animate` (line 47)
- `set_net_radii` (line 56)
- `set_idle` (line 75)
- `start_animation` (line 81)
- `stop_animation` (line 84)
- `paintEvent` (line 87)

---

### `ui\visualizers\widgets\circular_net_eq_widget.py.CircularNetEQWidget`

- **File:** `ui\visualizers\widgets\circular_net_eq_widget.py`
- **Line:** 5
- **Bases:** QWidget
- **Docstring:** A Vanta.js-inspired circular net visualizer: points around a circle, connected by glowing lines, wit...

**Methods:**
- `__init__` (line 18)
- `_animate` (line 39)
- `set_net_radii` (line 49)
- `set_idle` (line 68)
- `start_animation` (line 72)
- `stop_animation` (line 75)
- `paintEvent` (line 78)

---

## ⚙️ Functions

### `app\app_lifecycle.py.__init__`

- **File:** `app\app_lifecycle.py`
- **Line:** 21
- **Arguments:** self, main_window, service_manager, ui_manager, event_handler

---

### `app\app_lifecycle.py._check_ollama_crash`

- **File:** `app\app_lifecycle.py`
- **Line:** 752
- **Arguments:** self
- **Docstring:** Check if Ollama has crashed and restart if needed...

---

### `app\app_lifecycle.py._ensure_ollama_running`

- **File:** `app\app_lifecycle.py`
- **Line:** 406
- **Arguments:** self
- **Docstring:** Ensure Ollama is running, start it if needed...

---

### `app\app_lifecycle.py._find_ollama_executable`

- **File:** `app\app_lifecycle.py`
- **Line:** 468
- **Arguments:** self
- **Returns:** str
- **Docstring:** Find the Ollama app.exe executable path...

---

### `app\app_lifecycle.py._is_ollama_installed`

- **File:** `app\app_lifecycle.py`
- **Line:** 442
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Ollama is installed and accessible...

---

### `app\app_lifecycle.py._reset_ollama_restart_attempts`

- **File:** `app\app_lifecycle.py`
- **Line:** 809
- **Arguments:** self
- **Docstring:** Reset the restart attempts counter (called on successful connection)...

---

### `app\app_lifecycle.py._show_custom_path_dialog`

- **File:** `app\app_lifecycle.py`
- **Line:** 849
- **Arguments:** self, context
- **Docstring:** Show dialog to let user specify custom Ollama path...

---

### `app\app_lifecycle.py._start_ollama_background`

- **File:** `app\app_lifecycle.py`
- **Line:** 512
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Start Ollama in the background with progress dialog...

---

### `app\app_lifecycle.py._stop_ollama_process`

- **File:** `app\app_lifecycle.py`
- **Line:** 679
- **Arguments:** self
- **Docstring:** Stop the Ollama process if running...

---

### `app\app_lifecycle.py._validate_ollama_executable`

- **File:** `app\app_lifecycle.py`
- **Line:** 913
- **Arguments:** self, file_path
- **Returns:** bool
- **Docstring:** Validate that the selected file is a valid Ollama executable...

---

### `app\app_lifecycle.py._verify_ollama_installation`

- **File:** `app\app_lifecycle.py`
- **Line:** 635
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Verify that Ollama is installed, running, and accessible...

---

### `app\app_lifecycle.py.check_ollama_connection`

- **File:** `app\app_lifecycle.py`
- **Line:** 309
- **Arguments:** self
- **Docstring:** Check if Ollama is running and accessible...

---

### `app\app_lifecycle.py.clear_custom_ollama_path`

- **File:** `app\app_lifecycle.py`
- **Line:** 960
- **Arguments:** self
- **Docstring:** Clear the custom Ollama path and revert to auto-detection...

---

### `app\app_lifecycle.py.force_close_ollama`

- **File:** `app\app_lifecycle.py`
- **Line:** 822
- **Arguments:** self
- **Docstring:** Force close Ollama immediately (for manual control)...

---

### `app\app_lifecycle.py.force_show_ollama_error`

- **File:** `app\app_lifecycle.py`
- **Line:** 337
- **Arguments:** self, context
- **Docstring:** Force show the Ollama error dialog regardless of the shown flag...

---

### `app\app_lifecycle.py.get_auto_start_ollama`

- **File:** `app\app_lifecycle.py`
- **Line:** 748
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Get whether auto-start Ollama is enabled (always True)...

---

### `app\app_lifecycle.py.get_available_models`

- **File:** `app\app_lifecycle.py`
- **Line:** 348
- **Arguments:** self
- **Docstring:** Get list of available models from Ollama...

---

### `app\app_lifecycle.py.get_close_ollama_on_exit`

- **File:** `app\app_lifecycle.py`
- **Line:** 818
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Get whether to close Ollama when the application exits...

---

### `app\app_lifecycle.py.get_custom_ollama_path`

- **File:** `app\app_lifecycle.py`
- **Line:** 956
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the custom Ollama path from config...

---

### `app\app_lifecycle.py.get_ollama_error_shown`

- **File:** `app\app_lifecycle.py`
- **Line:** 328
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Get the Ollama error shown flag...

---

### `app\app_lifecycle.py.get_ollama_path_info`

- **File:** `app\app_lifecycle.py`
- **Line:** 966
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get information about Ollama path detection...

---

### `app\app_lifecycle.py.get_ollama_process_info`

- **File:** `app\app_lifecycle.py`
- **Line:** 730
- **Arguments:** self
- **Docstring:** Get information about the Ollama process...

---

### `app\app_lifecycle.py.get_ollama_status_info`

- **File:** `app\app_lifecycle.py`
- **Line:** 831
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get comprehensive information about Ollama status...

---

### `app\app_lifecycle.py.handle_close_event`

- **File:** `app\app_lifecycle.py`
- **Line:** 95
- **Arguments:** self, event
- **Docstring:** Handle application close event...

---

### `app\app_lifecycle.py.handle_show_event`

- **File:** `app\app_lifecycle.py`
- **Line:** 74
- **Arguments:** self
- **Docstring:** Handle application show event...

---

### `app\app_lifecycle.py.initialize_application`

- **File:** `app\app_lifecycle.py`
- **Line:** 46
- **Arguments:** self
- **Docstring:** Initialize the application...

---

### `app\app_lifecycle.py.is_initialization_complete`

- **File:** `app\app_lifecycle.py`
- **Line:** 320
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if initialization is complete...

---

### `app\app_lifecycle.py.is_ollama_running`

- **File:** `app\app_lifecycle.py`
- **Line:** 726
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Ollama is currently running...

---

### `app\app_lifecycle.py.reset_ollama_error_shown`

- **File:** `app\app_lifecycle.py`
- **Line:** 332
- **Arguments:** self
- **Docstring:** Reset the Ollama error shown flag to allow showing error dialogs again...

---

### `app\app_lifecycle.py.send_test_message`

- **File:** `app\app_lifecycle.py`
- **Line:** 364
- **Arguments:** self, model_name, message
- **Docstring:** Send a test message to Ollama and get response...

---

### `app\app_lifecycle.py.set_auto_start_ollama`

- **File:** `app\app_lifecycle.py`
- **Line:** 743
- **Arguments:** self, enabled
- **Docstring:** Set whether to auto-start Ollama (deprecated - always enabled)...

---

### `app\app_lifecycle.py.set_close_ollama_on_exit`

- **File:** `app\app_lifecycle.py`
- **Line:** 813
- **Arguments:** self, enabled
- **Docstring:** Set whether to close Ollama when the application exits...

---

### `app\app_lifecycle.py.set_custom_ollama_path`

- **File:** `app\app_lifecycle.py`
- **Line:** 945
- **Arguments:** self, path
- **Docstring:** Set a custom path for Ollama executable...

---

### `app\app_lifecycle.py.set_ollama_error_shown`

- **File:** `app\app_lifecycle.py`
- **Line:** 324
- **Arguments:** self, shown
- **Docstring:** Set the Ollama error shown flag...

---

### `app\app_lifecycle.py.show_initialization_error`

- **File:** `app\app_lifecycle.py`
- **Line:** 133
- **Arguments:** self, error_message
- **Docstring:** Show initialization error dialog...

---

### `app\app_lifecycle.py.show_ollama_connection_error`

- **File:** `app\app_lifecycle.py`
- **Line:** 142
- **Arguments:** self, context, force_show
- **Docstring:** Show a user-friendly error dialog when Ollama is not running...

---

### `app\app_lifecycle.py.show_ollama_startup_dialog`

- **File:** `app\app_lifecycle.py`
- **Line:** 302
- **Arguments:** self
- **Docstring:** Show a dialog asking if user wants to start Ollama automatically...

---

### `app\app_lifecycle.py.start_ollama_manually`

- **File:** `app\app_lifecycle.py`
- **Line:** 716
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Manually start Ollama (called from UI)...

---

### `app\app_lifecycle.py.stop_ollama_manually`

- **File:** `app\app_lifecycle.py`
- **Line:** 722
- **Arguments:** self
- **Docstring:** Manually stop Ollama (called from UI)...

---

### `app\app_lifecycle.py.test_error_dialog`

- **File:** `app\app_lifecycle.py`
- **Line:** 342
- **Arguments:** self
- **Docstring:** Test method to show the error dialog for testing purposes...

---

### `app\app_lifecycle.py.wait_for_ollama`

- **File:** `app\app_lifecycle.py`
- **Line:** 567
- **Arguments:** 

---

### `app\app_lifecycle.py.was_ollama_started_by_app`

- **File:** `app\app_lifecycle.py`
- **Line:** 827
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Ollama was started by this application...

---

### `app\event_bus.py.__init__`

- **File:** `app\event_bus.py`
- **Line:** 16
- **Arguments:** self, main_window, service_manager, ui_manager, chat_controller, lifecycle_manager

---

### `app\event_bus.py._check_ollama_connection`

- **File:** `app\event_bus.py`
- **Line:** 1093
- **Arguments:** self
- **Docstring:** Check if Ollama is running and accessible...

---

### `app\event_bus.py._clean_messages_for_ollama`

- **File:** `app\event_bus.py`
- **Line:** 374
- **Arguments:** self, messages
- **Docstring:** Clean messages for Ollama API (remove internal fields)...

---

### `app\event_bus.py._cleanup_worker_thread`

- **File:** `app\event_bus.py`
- **Line:** 738
- **Arguments:** self
- **Docstring:** Clean up worker thread safely in the main thread...

---

### `app\event_bus.py._cleanup_worker_thread_once`

- **File:** `app\event_bus.py`
- **Line:** 750
- **Arguments:** self
- **Docstring:** Clean up worker thread once without recursion...

---

### `app\event_bus.py._connect_chat_tab_signals`

- **File:** `app\event_bus.py`
- **Line:** 179
- **Arguments:** self
- **Docstring:** Connect chat tab signals with proper error handling...

---

### `app\event_bus.py._connect_menu_actions`

- **File:** `app\event_bus.py`
- **Line:** 137
- **Arguments:** self
- **Docstring:** Connect menu actions to their handlers...

---

### `app\event_bus.py._create_chat_controller`

- **File:** `app\event_bus.py`
- **Line:** 1009
- **Arguments:** self
- **Docstring:** Create a new chat controller with current services...

---

### `app\event_bus.py._create_worker_thread`

- **File:** `app\event_bus.py`
- **Line:** 423
- **Arguments:** self, context_messages, chosen_model, temperature, streaming_message_id
- **Docstring:** Create and start worker thread for Ollama communication using persistent thread pool...

---

### `app\event_bus.py._final_worker_cleanup`

- **File:** `app\event_bus.py`
- **Line:** 774
- **Arguments:** self
- **Docstring:** Final cleanup to ensure worker thread is properly destroyed...

---

### `app\event_bus.py._handle_chat_chunk`

- **File:** `app\event_bus.py`
- **Line:** 470
- **Arguments:** self, chunk
- **Docstring:** Handle streaming chat chunk...

---

### `app\event_bus.py._handle_chat_error`

- **File:** `app\event_bus.py`
- **Line:** 533
- **Arguments:** self, error_message
- **Docstring:** Handle chat streaming error...

---

### `app\event_bus.py._handle_chat_error_safe`

- **File:** `app\event_bus.py`
- **Line:** 547
- **Arguments:** self, error_message
- **Docstring:** Safely handle chat error in main thread...

---

### `app\event_bus.py._handle_chat_finished`

- **File:** `app\event_bus.py`
- **Line:** 507
- **Arguments:** self
- **Docstring:** Handle chat streaming completion...

---

### `app\event_bus.py._handle_chat_progress`

- **File:** `app\event_bus.py`
- **Line:** 499
- **Arguments:** self, progress
- **Docstring:** Handle chat progress updates...

---

### `app\event_bus.py._handle_tts_finished_delayed`

- **File:** `app\event_bus.py`
- **Line:** 724
- **Arguments:** self
- **Docstring:** Handle TTS finished with a delay to ensure proper coordination...

---

### `app\event_bus.py._handle_worker_error_safe`

- **File:** `app\event_bus.py`
- **Line:** 698
- **Arguments:** self, error_message
- **Docstring:** Safely handle worker error in main thread...

---

### `app\event_bus.py._on_auto_save_completed`

- **File:** `app\event_bus.py`
- **Line:** 922
- **Arguments:** self, filepath
- **Docstring:** Handle auto-save completion...

---

### `app\event_bus.py._on_clear_chat`

- **File:** `app\event_bus.py`
- **Line:** 959
- **Arguments:** self
- **Docstring:** Clear the chat display...

---

### `app\event_bus.py._on_conversation_deleted`

- **File:** `app\event_bus.py`
- **Line:** 833
- **Arguments:** self, filepath
- **Docstring:** Handle conversation deletion from navigation...

---

### `app\event_bus.py._on_conversation_metadata_updated`

- **File:** `app\event_bus.py`
- **Line:** 910
- **Arguments:** self
- **Docstring:** Handle conversation metadata updates...

---

### `app\event_bus.py._on_conversation_renamed`

- **File:** `app\event_bus.py`
- **Line:** 837
- **Arguments:** self, old_filepath, new_filepath
- **Docstring:** Handle conversation rename from AI naming...

---

### `app\event_bus.py._on_conversation_selected`

- **File:** `app\event_bus.py`
- **Line:** 825
- **Arguments:** self, filepath
- **Docstring:** Handle conversation selection from navigation...

---

### `app\event_bus.py._on_conversation_updated`

- **File:** `app\event_bus.py`
- **Line:** 238
- **Arguments:** self
- **Docstring:** Handle conversation updates from controller...

---

### `app\event_bus.py._on_delayed_model_update`

- **File:** `app\event_bus.py`
- **Line:** 1077
- **Arguments:** self
- **Docstring:** Delayed model update to ensure UI is ready...

---

### `app\event_bus.py._on_error_occurred`

- **File:** `app\event_bus.py`
- **Line:** 233
- **Arguments:** self, error_message
- **Docstring:** Handle errors from controller...

---

### `app\event_bus.py._on_load_chat`

- **File:** `app\event_bus.py`
- **Line:** 976
- **Arguments:** self
- **Docstring:** Load a chat from a file...

---

### `app\event_bus.py._on_message_cancelled`

- **File:** `app\event_bus.py`
- **Line:** 799
- **Arguments:** self
- **Docstring:** Handle message cancellation...

---

### `app\event_bus.py._on_message_finished`

- **File:** `app\event_bus.py`
- **Line:** 790
- **Arguments:** self
- **Docstring:** Handle message finished...

---

### `app\event_bus.py._on_message_received`

- **File:** `app\event_bus.py`
- **Line:** 783
- **Arguments:** self, response
- **Docstring:** Handle message received signal from chat controller...

---

### `app\event_bus.py._on_message_sent`

- **File:** `app\event_bus.py`
- **Line:** 283
- **Arguments:** self, message
- **Docstring:** Handle new message sent from chat tab...

---

### `app\event_bus.py._on_model_operation_error`

- **File:** `app\event_bus.py`
- **Line:** 890
- **Arguments:** self, error
- **Docstring:** Handle model operation errors...

---

### `app\event_bus.py._on_model_operation_progress`

- **File:** `app\event_bus.py`
- **Line:** 884
- **Arguments:** self, message
- **Docstring:** Handle model operation progress...

---

### `app\event_bus.py._on_models_updated`

- **File:** `app\event_bus.py`
- **Line:** 269
- **Arguments:** self, models
- **Docstring:** Handle model list updates...

---

### `app\event_bus.py._on_name_generation_requested`

- **File:** `app\event_bus.py`
- **Line:** 244
- **Arguments:** self, filepath
- **Docstring:** Handle name generation request from controller...

---

### `app\event_bus.py._on_new_conversation`

- **File:** `app\event_bus.py`
- **Line:** 942
- **Arguments:** self
- **Docstring:** Start a new conversation...

---

### `app\event_bus.py._on_new_conversation_requested`

- **File:** `app\event_bus.py`
- **Line:** 938
- **Arguments:** self
- **Docstring:** Handle new conversation request...

---

### `app\event_bus.py._on_open_settings`

- **File:** `app\event_bus.py`
- **Line:** 982
- **Arguments:** self
- **Docstring:** Open the settings dialog...

---

### `app\event_bus.py._on_personality_changed`

- **File:** `app\event_bus.py`
- **Line:** 859
- **Arguments:** self, personality_name
- **Docstring:** Handle personality changes...

---

### `app\event_bus.py._on_refresh_models`

- **File:** `app\event_bus.py`
- **Line:** 1027
- **Arguments:** self
- **Docstring:** Refresh the list of available models...

---

### `app\event_bus.py._on_refresh_personalities`

- **File:** `app\event_bus.py`
- **Line:** 1059
- **Arguments:** self
- **Docstring:** Refresh the list of available personalities...

---

### `app\event_bus.py._on_save_chat`

- **File:** `app\event_bus.py`
- **Line:** 970
- **Arguments:** self
- **Docstring:** Save the current chat to a file...

---

### `app\event_bus.py._on_show_about`

- **File:** `app\event_bus.py`
- **Line:** 1073
- **Arguments:** self
- **Docstring:** Show about dialog...

---

### `app\event_bus.py._on_status_updated`

- **File:** `app\event_bus.py`
- **Line:** 229
- **Arguments:** self, message
- **Docstring:** Handle status updates from controller...

---

### `app\event_bus.py._on_tts_finished`

- **File:** `app\event_bus.py`
- **Line:** 717
- **Arguments:** self
- **Docstring:** Handle TTS completion...

---

### `app\event_bus.py._on_worker_chunk`

- **File:** `app\event_bus.py`
- **Line:** 609
- **Arguments:** self, chunk, model_name, msg_id, chunk_index
- **Docstring:** Handle a chunk from the worker thread and update the chat display safely with all required info....

---

### `app\event_bus.py._on_worker_detailed_error`

- **File:** `app\event_bus.py`
- **Line:** 589
- **Arguments:** self, error_message
- **Docstring:** Handle detailed worker error with logging...

---

### `app\event_bus.py._on_worker_error`

- **File:** `app\event_bus.py`
- **Line:** 685
- **Arguments:** self, error_message
- **Docstring:** Handle worker error...

---

### `app\event_bus.py._on_worker_finished`

- **File:** `app\event_bus.py`
- **Line:** 653
- **Arguments:** self
- **Docstring:** Handle worker completion...

---

### `app\event_bus.py._on_worker_progress`

- **File:** `app\event_bus.py`
- **Line:** 632
- **Arguments:** self, progress
- **Docstring:** Handle worker progress signal...

---

### `app\event_bus.py._on_worker_thread_finished`

- **File:** `app\event_bus.py`
- **Line:** 604
- **Arguments:** self
- **Docstring:** Handle worker thread finished signal (legacy method - kept for compatibility)...

---

### `app\event_bus.py._retry_chat_tab_connection`

- **File:** `app\event_bus.py`
- **Line:** 116
- **Arguments:** self
- **Docstring:** Attempt to connect to chat tab after delay....

---

### `app\event_bus.py._send_to_ollama`

- **File:** `app\event_bus.py`
- **Line:** 321
- **Arguments:** self, message, model, temperature
- **Docstring:** Send message to Ollama and handle streaming response...

---

### `app\event_bus.py._setup_chat_tab_retry`

- **File:** `app\event_bus.py`
- **Line:** 104
- **Arguments:** self
- **Docstring:** Set up chat tab signal connections with a retry mechanism....

---

### `app\event_bus.py._setup_ui_with_new_services`

- **File:** `app\event_bus.py`
- **Line:** 1021
- **Arguments:** self
- **Docstring:** Setup UI with new services after configuration change...

---

### `app\event_bus.py._show_ollama_connection_error`

- **File:** `app\event_bus.py`
- **Line:** 1098
- **Arguments:** self, context, force_show
- **Docstring:** Show a user-friendly error dialog when Ollama is not running...

---

### `app\event_bus.py._start_worker_after_streaming_message`

- **File:** `app\event_bus.py`
- **Line:** 386
- **Arguments:** self, context_messages, chosen_model, temperature, streaming_message_id
- **Docstring:** Start worker thread after streaming message is created to prevent race conditions...

---

### `app\event_bus.py._stop_streaming_safe`

- **File:** `app\event_bus.py`
- **Line:** 675
- **Arguments:** self
- **Docstring:** Safely stop streaming in main thread...

---

### `app\event_bus.py._update_chat_display_safe`

- **File:** `app\event_bus.py`
- **Line:** 619
- **Arguments:** self, chunk, model_name, msg_id, chunk_index
- **Docstring:** Safely update chat display in main thread...

---

### `app\event_bus.py._update_progress_safe`

- **File:** `app\event_bus.py`
- **Line:** 644
- **Arguments:** self, progress
- **Docstring:** Safely update progress in main thread...

---

### `app\event_bus.py.cleanup_on_exit`

- **File:** `app\event_bus.py`
- **Line:** 1157
- **Arguments:** self
- **Docstring:** Clean up all resources when application is exiting...

---

### `app\event_bus.py.get_threading_status`

- **File:** `app\event_bus.py`
- **Line:** 1146
- **Arguments:** self
- **Docstring:** Get current threading status and statistics....

---

### `app\event_bus.py.reconnect_chat_tab_signals`

- **File:** `app\event_bus.py`
- **Line:** 1198
- **Arguments:** self
- **Docstring:** Reconnect chat tab signals when chat tab is recreated...

---

### `app\event_bus.py.safe_disconnect`

- **File:** `app\event_bus.py`
- **Line:** 187
- **Arguments:** signal

---

### `app\event_bus.py.setup_connections`

- **File:** `app\event_bus.py`
- **Line:** 52
- **Arguments:** self
- **Docstring:** Setup all signal connections between components...

---

### `app\event_bus.py.stop_chat_streaming`

- **File:** `app\event_bus.py`
- **Line:** 564
- **Arguments:** self
- **Docstring:** Stop chat streaming using persistent thread pool....

---

### `app\main.py.__init__`

- **File:** `app\main.py`
- **Line:** 23
- **Arguments:** self

---

### `app\main.py._setup_connections`

- **File:** `app\main.py`
- **Line:** 118
- **Arguments:** self
- **Docstring:** Setup EventBus connections after UI is fully initialized...

---

### `app\main.py._setup_ui`

- **File:** `app\main.py`
- **Line:** 84
- **Arguments:** self
- **Docstring:** Setup the UI components...

---

### `app\main.py.check_ollama_connection`

- **File:** `app\main.py`
- **Line:** 149
- **Arguments:** self
- **Docstring:** Check if Ollama is running and accessible...

---

### `app\main.py.closeEvent`

- **File:** `app\main.py`
- **Line:** 141
- **Arguments:** self, event
- **Docstring:** Handle application close event...

---

### `app\main.py.get_chat_controller`

- **File:** `app\main.py`
- **Line:** 170
- **Arguments:** self
- **Docstring:** Get the chat controller...

---

### `app\main.py.get_event_handler`

- **File:** `app\main.py`
- **Line:** 162
- **Arguments:** self
- **Docstring:** Get the Event Bus...

---

### `app\main.py.get_lifecycle_manager`

- **File:** `app\main.py`
- **Line:** 166
- **Arguments:** self
- **Docstring:** Get the lifecycle manager...

---

### `app\main.py.get_service_manager`

- **File:** `app\main.py`
- **Line:** 154
- **Arguments:** self
- **Docstring:** Get the service manager...

---

### `app\main.py.get_ui_manager`

- **File:** `app\main.py`
- **Line:** 158
- **Arguments:** self
- **Docstring:** Get the UI manager...

---

### `app\main.py.showEvent`

- **File:** `app\main.py`
- **Line:** 136
- **Arguments:** self, event
- **Docstring:** Handle application show event...

---

### `app\main.py.show_ollama_connection_error`

- **File:** `app\main.py`
- **Line:** 145
- **Arguments:** self, context, force_show
- **Docstring:** Show Ollama connection error dialog...

---

### `app\service_manager.py.__init__`

- **File:** `app\service_manager.py`
- **Line:** 34
- **Arguments:** self, config_manager
- **Docstring:** Initialize the service manager (singleton)...

---

### `app\service_manager.py.__new__`

- **File:** `app\service_manager.py`
- **Line:** 26
- **Arguments:** cls
- **Docstring:** Singleton pattern implementation...

---

### `app\service_manager.py._initialize_services`

- **File:** `app\service_manager.py`
- **Line:** 68
- **Arguments:** self
- **Docstring:** Initialize all application services...

---

### `app\service_manager.py._initialize_voice_service`

- **File:** `app\service_manager.py`
- **Line:** 207
- **Arguments:** self
- **Docstring:** Initialize voice service only when needed (deprecated - use manager)...

---

### `app\service_manager.py.cleanup`

- **File:** `app\service_manager.py`
- **Line:** 183
- **Arguments:** self
- **Docstring:** Clean up services on application shutdown...

---

### `app\service_manager.py.get_conversation_manager`

- **File:** `app\service_manager.py`
- **Line:** 155
- **Arguments:** self
- **Returns:** ConversationManager
- **Docstring:** Get the conversation manager instance...

---

### `app\service_manager.py.get_conversation_service`

- **File:** `app\service_manager.py`
- **Line:** 139
- **Arguments:** self
- **Returns:** ConversationService
- **Docstring:** Get the conversation service instance...

---

### `app\service_manager.py.get_enhancement_service`

- **File:** `app\service_manager.py`
- **Line:** 143
- **Arguments:** self
- **Returns:** EnhancementService
- **Docstring:** Get the enhancement service instance...

---

### `app\service_manager.py.get_instance`

- **File:** `app\service_manager.py`
- **Line:** 62
- **Arguments:** cls
- **Decorators:** classmethod
- **Docstring:** Get the global service manager instance...

---

### `app\service_manager.py.get_memory_service`

- **File:** `app\service_manager.py`
- **Line:** 147
- **Arguments:** self
- **Docstring:** Get the memory service instance (may be None if disabled)...

---

### `app\service_manager.py.get_ollama_service`

- **File:** `app\service_manager.py`
- **Line:** 135
- **Arguments:** self
- **Returns:** OllamaService
- **Docstring:** Get the Ollama service instance...

---

### `app\service_manager.py.get_personality_service`

- **File:** `app\service_manager.py`
- **Line:** 159
- **Arguments:** self
- **Returns:** PersonalityModel
- **Docstring:** Get the personality service instance...

---

### `app\service_manager.py.get_session_variables`

- **File:** `app\service_manager.py`
- **Line:** 179
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get session variables...

---

### `app\service_manager.py.get_summarization_service`

- **File:** `app\service_manager.py`
- **Line:** 151
- **Arguments:** self
- **Returns:** SummarizationService
- **Docstring:** Get the summarization service instance...

---

### `app\service_manager.py.get_voice_service`

- **File:** `app\service_manager.py`
- **Line:** 163
- **Arguments:** self
- **Docstring:** Get the voice service instance from the manager...

---

### `app\service_manager.py.is_memory_enabled`

- **File:** `app\service_manager.py`
- **Line:** 175
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if memory is enabled...

---

### `app\service_manager.py.is_voice_service_initialized`

- **File:** `app\service_manager.py`
- **Line:** 169
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice service has been initialized...

---

### `app\service_manager.py.reinitialize_services`

- **File:** `app\service_manager.py`
- **Line:** 130
- **Arguments:** self
- **Docstring:** Reinitialize services (used when configuration changes)...

---

### `app\threading_integration.py.__init__`

- **File:** `app\threading_integration.py`
- **Line:** 151
- **Arguments:** self, event_handler

---

### `app\threading_integration.py._on_chunk_received`

- **File:** `app\threading_integration.py`
- **Line:** 163
- **Arguments:** self, chunk
- **Docstring:** Handle chunk received from streaming....

---

### `app\threading_integration.py._on_error`

- **File:** `app\threading_integration.py`
- **Line:** 199
- **Arguments:** self, error_message
- **Docstring:** Handle streaming error....

---

### `app\threading_integration.py._on_finished`

- **File:** `app\threading_integration.py`
- **Line:** 187
- **Arguments:** self
- **Docstring:** Handle streaming finished....

---

### `app\threading_integration.py._on_progress_updated`

- **File:** `app\threading_integration.py`
- **Line:** 175
- **Arguments:** self, progress
- **Docstring:** Handle progress update from streaming....

---

### `app\threading_integration.py.get_threading_status`

- **File:** `app\threading_integration.py`
- **Line:** 241
- **Arguments:** self
- **Docstring:** Get current threading status and statistics....

---

### `app\threading_integration.py.process_file_operation`

- **File:** `app\threading_integration.py`
- **Line:** 111
- **Arguments:** self, file_path, operation
- **Returns:** str
- **Docstring:** Process file operation using QRunnable.

Args:
    file_path: Path to the file
    operation: Operat...

---

### `app\threading_integration.py.process_message_formatting`

- **File:** `app\threading_integration.py`
- **Line:** 92
- **Arguments:** self, message, callback
- **Returns:** str
- **Docstring:** Process message formatting using QRunnable.

Args:
    message: Message to format
    callback: Call...

---

### `app\threading_integration.py.process_message_spell_check`

- **File:** `app\threading_integration.py`
- **Line:** 73
- **Arguments:** self, message, callback
- **Returns:** str
- **Docstring:** Process message spell check using QRunnable.

Args:
    message: Message to spell check
    callback...

---

### `app\threading_integration.py.start_chat_streaming`

- **File:** `app\threading_integration.py`
- **Line:** 211
- **Arguments:** self, context_messages, chosen_model, temperature, config_manager
- **Returns:** bool
- **Docstring:** Start chat streaming via bridge.

Args:
    context_messages: List of conversation messages
    chos...

---

### `app\threading_integration.py.stop_chat_streaming`

- **File:** `app\threading_integration.py`
- **Line:** 232
- **Arguments:** self
- **Docstring:** Stop chat streaming safely....

---

### `config\config_manager.py.__init__`

- **File:** `config\config_manager.py`
- **Line:** 13
- **Arguments:** self, config_file

---

### `config\config_manager.py.get`

- **File:** `config\config_manager.py`
- **Line:** 88
- **Arguments:** self, key, default
- **Returns:** Any
- **Docstring:** Get a configuration value...

---

### `config\config_manager.py.get_chat_settings`

- **File:** `config\config_manager.py`
- **Line:** 151
- **Arguments:** self
- **Docstring:** Get chat settings...

---

### `config\config_manager.py.get_default_model`

- **File:** `config\config_manager.py`
- **Line:** 118
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the default model name...

---

### `config\config_manager.py.get_default_personality`

- **File:** `config\config_manager.py`
- **Line:** 134
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the default personality...

---

### `config\config_manager.py.get_default_temperature`

- **File:** `config\config_manager.py`
- **Line:** 126
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get the default temperature...

---

### `config\config_manager.py.get_frequency_penalty`

- **File:** `config\config_manager.py`
- **Line:** 247
- **Arguments:** self

---

### `config\config_manager.py.get_history_directory`

- **File:** `config\config_manager.py`
- **Line:** 185
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the chat history directory...

---

### `config\config_manager.py.get_max_context_messages`

- **File:** `config\config_manager.py`
- **Line:** 254
- **Arguments:** self
- **Returns:** int
- **Docstring:** Get the maximum number of context messages for memory management...

---

### `config\config_manager.py.get_max_tokens`

- **File:** `config\config_manager.py`
- **Line:** 241
- **Arguments:** self

---

### `config\config_manager.py.get_ollama_url`

- **File:** `config\config_manager.py`
- **Line:** 176
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the Ollama API URL...

---

### `config\config_manager.py.get_presence_penalty`

- **File:** `config\config_manager.py`
- **Line:** 250
- **Arguments:** self
- **Docstring:** Get the presence penalty setting...

---

### `config\config_manager.py.get_top_p`

- **File:** `config\config_manager.py`
- **Line:** 244
- **Arguments:** self

---

### `config\config_manager.py.get_voice_settings`

- **File:** `config\config_manager.py`
- **Line:** 262
- **Arguments:** self
- **Docstring:** Get voice settings...

---

### `config\config_manager.py.get_window_size`

- **File:** `config\config_manager.py`
- **Line:** 142
- **Arguments:** self
- **Returns:** tuple
- **Docstring:** Get the default window size...

---

### `config\config_manager.py.is_auto_save_enabled`

- **File:** `config\config_manager.py`
- **Line:** 160
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if auto-save is enabled...

---

### `config\config_manager.py.is_enhancement_enabled`

- **File:** `config\config_manager.py`
- **Line:** 193
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if response enhancement is enabled...

---

### `config\config_manager.py.is_history_enabled`

- **File:** `config\config_manager.py`
- **Line:** 201
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if history is enabled...

---

### `config\config_manager.py.is_json_format_enabled`

- **File:** `config\config_manager.py`
- **Line:** 217
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if JSON format is enabled...

---

### `config\config_manager.py.is_spellcheck_enabled`

- **File:** `config\config_manager.py`
- **Line:** 168
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if spellcheck is enabled...

---

### `config\config_manager.py.is_think_enabled`

- **File:** `config\config_manager.py`
- **Line:** 233
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if think mode is enabled...

---

### `config\config_manager.py.is_verbose_enabled`

- **File:** `config\config_manager.py`
- **Line:** 225
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if verbose is enabled...

---

### `config\config_manager.py.is_wordwrap_enabled`

- **File:** `config\config_manager.py`
- **Line:** 209
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if wordwrap is enabled...

---

### `config\config_manager.py.load_config`

- **File:** `config\config_manager.py`
- **Line:** 17
- **Arguments:** self
- **Docstring:** Load configuration from file or create default if not exists...

---

### `config\config_manager.py.merge_configs`

- **File:** `config\config_manager.py`
- **Line:** 65
- **Arguments:** self, default, loaded
- **Docstring:** Merge loaded config with defaults, ensuring all keys exist...

---

### `config\config_manager.py.save_config`

- **File:** `config\config_manager.py`
- **Line:** 75
- **Arguments:** self, config
- **Returns:** bool
- **Docstring:** Save configuration to file...

---

### `config\config_manager.py.set`

- **File:** `config\config_manager.py`
- **Line:** 101
- **Arguments:** self, key, value
- **Returns:** bool
- **Docstring:** Set a configuration value...

---

### `config\config_manager.py.set_auto_save_enabled`

- **File:** `config\config_manager.py`
- **Line:** 164
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set auto-save enabled/disabled...

---

### `config\config_manager.py.set_default_model`

- **File:** `config\config_manager.py`
- **Line:** 122
- **Arguments:** self, model_name
- **Returns:** bool
- **Docstring:** Set the default model name...

---

### `config\config_manager.py.set_default_personality`

- **File:** `config\config_manager.py`
- **Line:** 138
- **Arguments:** self, personality
- **Returns:** bool
- **Docstring:** Set the default personality...

---

### `config\config_manager.py.set_default_temperature`

- **File:** `config\config_manager.py`
- **Line:** 130
- **Arguments:** self, temperature
- **Returns:** bool
- **Docstring:** Set the default temperature...

---

### `config\config_manager.py.set_enhancement_enabled`

- **File:** `config\config_manager.py`
- **Line:** 197
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set response enhancement enabled/disabled...

---

### `config\config_manager.py.set_history_directory`

- **File:** `config\config_manager.py`
- **Line:** 189
- **Arguments:** self, directory
- **Returns:** bool
- **Docstring:** Set the chat history directory...

---

### `config\config_manager.py.set_history_enabled`

- **File:** `config\config_manager.py`
- **Line:** 205
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set history enabled/disabled...

---

### `config\config_manager.py.set_json_format_enabled`

- **File:** `config\config_manager.py`
- **Line:** 221
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set JSON format enabled/disabled...

---

### `config\config_manager.py.set_max_context_messages`

- **File:** `config\config_manager.py`
- **Line:** 258
- **Arguments:** self, max_messages
- **Returns:** bool
- **Docstring:** Set the maximum number of context messages for memory management...

---

### `config\config_manager.py.set_ollama_url`

- **File:** `config\config_manager.py`
- **Line:** 181
- **Arguments:** self, url
- **Returns:** bool
- **Docstring:** Set the Ollama API URL...

---

### `config\config_manager.py.set_spellcheck_enabled`

- **File:** `config\config_manager.py`
- **Line:** 172
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set spellcheck enabled/disabled...

---

### `config\config_manager.py.set_think_enabled`

- **File:** `config\config_manager.py`
- **Line:** 237
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set think mode enabled/disabled...

---

### `config\config_manager.py.set_verbose_enabled`

- **File:** `config\config_manager.py`
- **Line:** 229
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set verbose enabled/disabled...

---

### `config\config_manager.py.set_voice_settings`

- **File:** `config\config_manager.py`
- **Line:** 279
- **Arguments:** self, settings
- **Returns:** bool
- **Docstring:** Set voice settings...

---

### `config\config_manager.py.set_window_size`

- **File:** `config\config_manager.py`
- **Line:** 147
- **Arguments:** self, width, height
- **Returns:** bool
- **Docstring:** Set the default window size...

---

### `config\config_manager.py.set_wordwrap_enabled`

- **File:** `config\config_manager.py`
- **Line:** 213
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set wordwrap enabled/disabled...

---

### `core\logging\helpers.py.__init__`

- **File:** `core\logging\helpers.py`
- **Line:** 216
- **Arguments:** self

---

### `core\logging\helpers.py._on_thread_finished`

- **File:** `core\logging\helpers.py`
- **Line:** 286
- **Arguments:** self, thread_name
- **Docstring:** Handle thread finished signal...

---

### `core\logging\helpers.py._on_thread_started`

- **File:** `core\logging\helpers.py`
- **Line:** 274
- **Arguments:** self, thread_name
- **Docstring:** Handle thread started signal...

---

### `core\logging\helpers.py.cleanup`

- **File:** `core\logging\helpers.py`
- **Line:** 352
- **Arguments:** self
- **Docstring:** Clean up the thread monitor...

---

### `core\logging\helpers.py.cleanup_thread_monitor`

- **File:** `core\logging\helpers.py`
- **Line:** 426
- **Arguments:** 
- **Docstring:** Clean up the global thread monitor...

---

### `core\logging\helpers.py.get_all_threads`

- **File:** `core\logging\helpers.py`
- **Line:** 304
- **Arguments:** self
- **Docstring:** Get information about all active threads...

---

### `core\logging\helpers.py.get_thread_history`

- **File:** `core\logging\helpers.py`
- **Line:** 308
- **Arguments:** self
- **Docstring:** Get history of completed threads...

---

### `core\logging\helpers.py.get_thread_info`

- **File:** `core\logging\helpers.py`
- **Line:** 300
- **Arguments:** self, thread_name
- **Docstring:** Get information about a specific thread...

---

### `core\logging\helpers.py.get_thread_monitor`

- **File:** `core\logging\helpers.py`
- **Line:** 419
- **Arguments:** 
- **Returns:** ThreadMonitor
- **Docstring:** Get the global thread monitor instance...

---

### `core\logging\helpers.py.get_thread_stats`

- **File:** `core\logging\helpers.py`
- **Line:** 312
- **Arguments:** self
- **Returns:** Dict
- **Docstring:** Get statistics about thread usage...

---

### `core\logging\helpers.py.log_audio_operation`

- **File:** `core\logging\helpers.py`
- **Line:** 72
- **Arguments:** operation, success, error, details
- **Decorators:** staticmethod
- **Docstring:** Log audio operation information...

---

### `core\logging\helpers.py.log_conversation_detection`

- **File:** `core\logging\helpers.py`
- **Line:** 195
- **Arguments:** conversation_type
- **Decorators:** staticmethod
- **Docstring:** Log conversation detection...

---

### `core\logging\helpers.py.log_critical_error`

- **File:** `core\logging\helpers.py`
- **Line:** 113
- **Arguments:** component, error, recovery_action
- **Decorators:** staticmethod
- **Docstring:** Log a critical error with recovery action...

---

### `core\logging\helpers.py.log_debug`

- **File:** `core\logging\helpers.py`
- **Line:** 44
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Log a debug message...

---

### `core\logging\helpers.py.log_error`

- **File:** `core\logging\helpers.py`
- **Line:** 49
- **Arguments:** message, print_to_terminal
- **Decorators:** staticmethod
- **Docstring:** Log an error message...

---

### `core\logging\helpers.py.log_exception_with_context`

- **File:** `core\logging\helpers.py`
- **Line:** 25
- **Arguments:** operation, exception, context
- **Decorators:** staticmethod
- **Docstring:** Log an exception with context information...

---

### `core\logging\helpers.py.log_fact_extraction_end`

- **File:** `core\logging\helpers.py`
- **Line:** 125
- **Arguments:** facts_count
- **Decorators:** staticmethod
- **Docstring:** Log fact extraction end...

---

### `core\logging\helpers.py.log_fact_extraction_result`

- **File:** `core\logging\helpers.py`
- **Line:** 130
- **Arguments:** facts
- **Decorators:** staticmethod
- **Docstring:** Log fact extraction result...

---

### `core\logging\helpers.py.log_fact_extraction_start`

- **File:** `core\logging\helpers.py`
- **Line:** 120
- **Arguments:** query
- **Decorators:** staticmethod
- **Docstring:** Log fact extraction start...

---

### `core\logging\helpers.py.log_fact_processing`

- **File:** `core\logging\helpers.py`
- **Line:** 135
- **Arguments:** fact_type, fact_count
- **Decorators:** staticmethod
- **Docstring:** Log fact processing...

---

### `core\logging\helpers.py.log_fact_skipped`

- **File:** `core\logging\helpers.py`
- **Line:** 155
- **Arguments:** reason, fact_type
- **Decorators:** staticmethod
- **Docstring:** Log skipped fact...

---

### `core\logging\helpers.py.log_fact_storage_end`

- **File:** `core\logging\helpers.py`
- **Line:** 145
- **Arguments:** fact_type, stored_count
- **Decorators:** staticmethod
- **Docstring:** Log fact storage end...

---

### `core\logging\helpers.py.log_fact_storage_start`

- **File:** `core\logging\helpers.py`
- **Line:** 140
- **Arguments:** fact_type, fact_count
- **Decorators:** staticmethod
- **Docstring:** Log fact storage start...

---

### `core\logging\helpers.py.log_fact_storage_summary`

- **File:** `core\logging\helpers.py`
- **Line:** 150
- **Arguments:** total_facts, stored_facts
- **Decorators:** staticmethod
- **Docstring:** Log fact storage summary...

---

### `core\logging\helpers.py.log_file_operation`

- **File:** `core\logging\helpers.py`
- **Line:** 64
- **Arguments:** operation, filepath, success, error
- **Decorators:** staticmethod
- **Docstring:** Log file operation information...

---

### `core\logging\helpers.py.log_info_with_context`

- **File:** `core\logging\helpers.py`
- **Line:** 38
- **Arguments:** message, context
- **Decorators:** staticmethod
- **Docstring:** Log an info message with context information...

---

### `core\logging\helpers.py.log_json_extraction`

- **File:** `core\logging\helpers.py`
- **Line:** 180
- **Arguments:** json_data
- **Decorators:** staticmethod
- **Docstring:** Log JSON extraction...

---

### `core\logging\helpers.py.log_json_parsing_error`

- **File:** `core\logging\helpers.py`
- **Line:** 102
- **Arguments:** error, json_str
- **Decorators:** staticmethod
- **Docstring:** Log JSON parsing error...

---

### `core\logging\helpers.py.log_json_parsing_success`

- **File:** `core\logging\helpers.py`
- **Line:** 108
- **Arguments:** json_str
- **Decorators:** staticmethod
- **Docstring:** Log successful JSON parsing...

---

### `core\logging\helpers.py.log_llm_call`

- **File:** `core\logging\helpers.py`
- **Line:** 170
- **Arguments:** model, prompt_length
- **Decorators:** staticmethod
- **Docstring:** Log LLM call...

---

### `core\logging\helpers.py.log_llm_response`

- **File:** `core\logging\helpers.py`
- **Line:** 175
- **Arguments:** model, response_length
- **Decorators:** staticmethod
- **Docstring:** Log LLM response...

---

### `core\logging\helpers.py.log_memory_ltm_status`

- **File:** `core\logging\helpers.py`
- **Line:** 165
- **Arguments:** ltm_count, stm_count
- **Decorators:** staticmethod
- **Docstring:** Log memory status...

---

### `core\logging\helpers.py.log_memory_operation`

- **File:** `core\logging\helpers.py`
- **Line:** 80
- **Arguments:** operation, memory_type, success, error
- **Decorators:** staticmethod
- **Docstring:** Log memory operation information...

---

### `core\logging\helpers.py.log_memory_result`

- **File:** `core\logging\helpers.py`
- **Line:** 160
- **Arguments:** query, memory_count
- **Decorators:** staticmethod
- **Docstring:** Log memory search result...

---

### `core\logging\helpers.py.log_message_sent`

- **File:** `core\logging\helpers.py`
- **Line:** 185
- **Arguments:** message_length
- **Decorators:** staticmethod
- **Docstring:** Log message sent...

---

### `core\logging\helpers.py.log_message_sent_end`

- **File:** `core\logging\helpers.py`
- **Line:** 190
- **Arguments:** message_length, response_length
- **Decorators:** staticmethod
- **Docstring:** Log message sent end...

---

### `core\logging\helpers.py.log_network_request`

- **File:** `core\logging\helpers.py`
- **Line:** 54
- **Arguments:** url, method, status_code, error
- **Decorators:** staticmethod
- **Docstring:** Log network request information...

---

### `core\logging\helpers.py.log_performance_metric`

- **File:** `core\logging\helpers.py`
- **Line:** 96
- **Arguments:** operation, duration, context
- **Decorators:** staticmethod
- **Docstring:** Log performance metric...

---

### `core\logging\helpers.py.log_service_initialization`

- **File:** `core\logging\helpers.py`
- **Line:** 200
- **Arguments:** service_name, success, error
- **Decorators:** staticmethod
- **Docstring:** Log service initialization...

---

### `core\logging\helpers.py.log_thread_context`

- **File:** `core\logging\helpers.py`
- **Line:** 376
- **Arguments:** message, thread
- **Decorators:** staticmethod
- **Docstring:** Log a message with thread context information...

---

### `core\logging\helpers.py.log_thread_operation`

- **File:** `core\logging\helpers.py`
- **Line:** 409
- **Arguments:** operation, thread_name, details
- **Decorators:** staticmethod
- **Docstring:** Log thread operation...

---

### `core\logging\helpers.py.log_thread_safety_check`

- **File:** `core\logging\helpers.py`
- **Line:** 394
- **Arguments:** operation, current_thread, target_thread
- **Decorators:** staticmethod
- **Docstring:** Log thread safety check...

---

### `core\logging\helpers.py.log_ui_operation`

- **File:** `core\logging\helpers.py`
- **Line:** 88
- **Arguments:** component, operation, success, error
- **Decorators:** staticmethod
- **Docstring:** Log UI operation information...

---

### `core\logging\helpers.py.log_warning_with_context`

- **File:** `core\logging\helpers.py`
- **Line:** 32
- **Arguments:** message, context
- **Decorators:** staticmethod
- **Docstring:** Log a warning with context information...

---

### `core\logging\helpers.py.register_thread`

- **File:** `core\logging\helpers.py`
- **Line:** 224
- **Arguments:** self, thread, thread_type
- **Docstring:** Register a thread for monitoring...

---

### `core\logging\helpers.py.unregister_thread`

- **File:** `core\logging\helpers.py`
- **Line:** 254
- **Arguments:** self, thread_name
- **Docstring:** Unregister a thread from monitoring...

---

### `core\logging\logger.py.__new__`

- **File:** `core\logging\logger.py`
- **Line:** 124
- **Arguments:** cls

---

### `core\logging\logger.py._check_config_for_logging`

- **File:** `core\logging\logger.py`
- **Line:** 112
- **Arguments:** cls
- **Decorators:** classmethod

---

### `core\logging\logger.py._clear_log_file`

- **File:** `core\logging\logger.py`
- **Line:** 135
- **Arguments:** cls, filepath
- **Decorators:** classmethod

---

### `core\logging\logger.py._filter_non_ascii`

- **File:** `core\logging\logger.py`
- **Line:** 206
- **Arguments:** self, s

---

### `core\logging\logger.py._print`

- **File:** `core\logging\logger.py`
- **Line:** 40
- **Arguments:** self, msg

---

### `core\logging\logger.py._sanitize_filename`

- **File:** `core\logging\logger.py`
- **Line:** 21
- **Arguments:** name

---

### `core\logging\logger.py.critical`

- **File:** `core\logging\logger.py`
- **Line:** 151
- **Arguments:** self

---

### `core\logging\logger.py.debug`

- **File:** `core\logging\logger.py`
- **Line:** 148
- **Arguments:** self

---

### `core\logging\logger.py.error`

- **File:** `core\logging\logger.py`
- **Line:** 150
- **Arguments:** self

---

### `core\logging\logger.py.format`

- **File:** `core\logging\logger.py`
- **Line:** 71
- **Arguments:** self, record

---

### `core\logging\logger.py.get_logger`

- **File:** `core\logging\logger.py`
- **Line:** 142
- **Arguments:** cls, name
- **Decorators:** classmethod

---

### `core\logging\logger.py.info`

- **File:** `core\logging\logger.py`
- **Line:** 147
- **Arguments:** self

---

### `core\logging\logger.py.set_logging_enabled`

- **File:** `core\logging\logger.py`
- **Line:** 131
- **Arguments:** cls, enabled
- **Decorators:** classmethod

---

### `core\logging\logger.py.strip_emojis`

- **File:** `core\logging\logger.py`
- **Line:** 24
- **Arguments:** text

---

### `core\logging\logger.py.warning`

- **File:** `core\logging\logger.py`
- **Line:** 149
- **Arguments:** self

---

### `core\models\base_model.py.from_dict`

- **File:** `core\models\base_model.py`
- **Line:** 18
- **Arguments:** cls, data
- **Decorators:** classmethod, abstractmethod
- **Docstring:** Create model from dictionary....

---

### `core\models\base_model.py.to_dict`

- **File:** `core\models\base_model.py`
- **Line:** 12
- **Arguments:** self
- **Decorators:** abstractmethod
- **Docstring:** Convert model to dictionary....

---

### `core\models\conversation_metadata.py.__init__`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 135
- **Arguments:** self, history_dir

---

### `core\models\conversation_metadata.py.__post_init__`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 30
- **Arguments:** self
- **Docstring:** Initialize default values after object creation...

---

### `core\models\conversation_metadata.py._create_safe_filename`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 252
- **Arguments:** self, ai_generated_name
- **Returns:** str
- **Docstring:** Create a safe filename from the AI-generated name

Args:
    ai_generated_name: The AI-generated nam...

---

### `core\models\conversation_metadata.py.auto_save_conversation`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 324
- **Arguments:** self, conversation
- **Docstring:** Auto-save conversation if enabled

Args:
    conversation: List of conversation messages
    
Return...

---

### `core\models\conversation_metadata.py.clear_current_conversation`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 469
- **Arguments:** self
- **Docstring:** Clear current conversation metadata...

---

### `core\models\conversation_metadata.py.delete_conversation`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 427
- **Arguments:** self, filepath
- **Returns:** bool
- **Docstring:** Delete a conversation file

Args:
    filepath: Path to conversation file
    
Returns:
    True if ...

---

### `core\models\conversation_metadata.py.find_blank_conversation`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 483
- **Arguments:** self
- **Docstring:** Find the most recent blank conversation (0 messages)

Returns:
    Filepath of the most recent blank...

---

### `core\models\conversation_metadata.py.from_dict`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 74
- **Arguments:** cls, data
- **Decorators:** classmethod
- **Docstring:** Create metadata from dictionary...

---

### `core\models\conversation_metadata.py.get_current_metadata`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 474
- **Arguments:** self
- **Returns:** ConversationMetadata
- **Docstring:** Get current metadata...

---

### `core\models\conversation_metadata.py.get_display_info`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 116
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get formatted display information...

---

### `core\models\conversation_metadata.py.get_display_name`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 124
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the display name for the conversation...

---

### `core\models\conversation_metadata.py.get_formatted_created_time`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 96
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get formatted creation time for display...

---

### `core\models\conversation_metadata.py.get_formatted_modified_time`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 106
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get formatted last modified time for display...

---

### `core\models\conversation_metadata.py.list_conversations`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 398
- **Arguments:** self
- **Docstring:** List all saved conversations with their metadata

Returns:
    List of tuples (filepath, metadata)...

---

### `core\models\conversation_metadata.py.load_conversation`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 292
- **Arguments:** self, filepath
- **Docstring:** Load conversation and metadata from file

Args:
    filepath: Path to conversation file
    
Returns...

---

### `core\models\conversation_metadata.py.rename_conversation`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 444
- **Arguments:** self, old_filepath, new_filepath
- **Returns:** bool
- **Docstring:** Rename a conversation file and update references

Args:
    old_filepath: Original file path
    new...

---

### `core\models\conversation_metadata.py.reset`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 86
- **Arguments:** self
- **Docstring:** Reset metadata to initial state...

---

### `core\models\conversation_metadata.py.save_conversation`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 143
- **Arguments:** self, conversation, filename
- **Returns:** str
- **Docstring:** Save conversation with metadata to file

Args:
    conversation: List of conversation messages
    f...

---

### `core\models\conversation_metadata.py.set_auto_save_enabled`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 478
- **Arguments:** self, enabled
- **Docstring:** Enable or disable auto-save...

---

### `core\models\conversation_metadata.py.to_dict`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 61
- **Arguments:** self
- **Docstring:** Convert metadata to dictionary for JSON serialization...

---

### `core\models\conversation_metadata.py.update_ai_generated_name`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 56
- **Arguments:** self, name
- **Docstring:** Update the AI-generated name...

---

### `core\models\conversation_metadata.py.update_conversation_name`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 180
- **Arguments:** self, filepath, ai_generated_name
- **Docstring:** Update the AI-generated name for a conversation and rename the file

Args:
    filepath: Path to the...

---

### `core\models\conversation_metadata.py.update_message_count`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 41
- **Arguments:** self, count
- **Docstring:** Update the message count...

---

### `core\models\conversation_metadata.py.update_model`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 46
- **Arguments:** self, model
- **Docstring:** Update the model information...

---

### `core\models\conversation_metadata.py.update_personality`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 51
- **Arguments:** self, personality
- **Docstring:** Update the personality information...

---

### `core\models\conversation_metadata.py.update_timestamp`

- **File:** `core\models\conversation_metadata.py`
- **Line:** 37
- **Arguments:** self
- **Docstring:** Update the last modified timestamp...

---

### `core\shared_imports\pyside_imports.py.create_button`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 290
- **Arguments:** text, parent, enabled
- **Docstring:** Create a configured push button....

---

### `core\shared_imports\pyside_imports.py.create_combo_box`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 316
- **Arguments:** parent, items
- **Docstring:** Create a configured combo box widget....

---

### `core\shared_imports\pyside_imports.py.create_form_layout`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 355
- **Arguments:** parent, spacing, margin
- **Docstring:** Create a configured form layout....

---

### `core\shared_imports\pyside_imports.py.create_grid_layout`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 348
- **Arguments:** parent, spacing, margin
- **Docstring:** Create a configured grid layout....

---

### `core\shared_imports\pyside_imports.py.create_horizontal_layout`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 341
- **Arguments:** parent, spacing, margin
- **Docstring:** Create a configured horizontal layout....

---

### `core\shared_imports\pyside_imports.py.create_label`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 296
- **Arguments:** text, parent, alignment
- **Docstring:** Create a configured label....

---

### `core\shared_imports\pyside_imports.py.create_line_edit`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 309
- **Arguments:** parent, placeholder
- **Docstring:** Create a configured line edit widget....

---

### `core\shared_imports\pyside_imports.py.create_message_box`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 276
- **Arguments:** title, text, icon, buttons
- **Docstring:** Create a configured message box....

---

### `core\shared_imports\pyside_imports.py.create_progress_bar`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 323
- **Arguments:** parent, minimum, maximum
- **Docstring:** Create a configured progress bar....

---

### `core\shared_imports\pyside_imports.py.create_text_edit`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 302
- **Arguments:** parent, placeholder
- **Docstring:** Create a configured text edit widget....

---

### `core\shared_imports\pyside_imports.py.create_timer`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 269
- **Arguments:** interval, single_shot
- **Docstring:** Create and configure a QTimer with common settings....

---

### `core\shared_imports\pyside_imports.py.create_vertical_layout`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 334
- **Arguments:** parent, spacing, margin
- **Docstring:** Create a configured vertical layout....

---

### `core\shared_imports\pyside_imports.py.is_main_thread`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 211
- **Arguments:** 
- **Returns:** bool
- **Docstring:** Check if current thread is the main (GUI) thread....

---

### `core\shared_imports\pyside_imports.py.safe_signal_connect`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 232
- **Arguments:** signal, slot, logger
- **Docstring:** Safely connect a signal to a slot with error handling....

---

### `core\shared_imports\pyside_imports.py.safe_signal_disconnect`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 249
- **Arguments:** signal, slot, logger
- **Docstring:** Safely disconnect a signal from a slot with error handling....

---

### `core\shared_imports\pyside_imports.py.safe_ui_update`

- **File:** `core\shared_imports\pyside_imports.py`
- **Line:** 217
- **Arguments:** func
- **Docstring:** Safely execute UI update function in the main thread....

---

### `core\threading\__init__.py.shutdown_global_persistent_thread_pool`

- **File:** `core\threading\__init__.py`
- **Line:** 53
- **Arguments:** 
- **Docstring:** Shutdown the global persistent thread pool....

---

### `core\threading\__init__.py.shutdown_global_threading_service`

- **File:** `core\threading\__init__.py`
- **Line:** 41
- **Arguments:** 
- **Docstring:** Shutdown the global threading service....

---

### `core\threading\persistent_thread_config.py.get_config_summary`

- **File:** `core\threading\persistent_thread_config.py`
- **Line:** 231
- **Arguments:** config
- **Docstring:** Get a summary of the persistent thread configuration.

Args:
    config: Configuration to summarize
...

---

### `core\threading\persistent_thread_config.py.get_persistent_thread_config`

- **File:** `core\threading\persistent_thread_config.py`
- **Line:** 171
- **Arguments:** config_type
- **Docstring:** Get persistent thread configuration based on type.

Args:
    config_type: Type of configuration ('d...

---

### `core\threading\persistent_thread_config.py.validate_persistent_thread_config`

- **File:** `core\threading\persistent_thread_config.py`
- **Line:** 191
- **Arguments:** config
- **Returns:** bool
- **Docstring:** Validate persistent thread configuration.

Args:
    config: Configuration to validate
    
Returns:...

---

### `core\threading\persistent_thread_pool.py.__init__`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 34
- **Arguments:** self, parent

---

### `core\threading\persistent_thread_pool.py._cleanup_idle_threads`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 313
- **Arguments:** self
- **Docstring:** Clean up idle threads that have exceeded their timeout....

---

### `core\threading\persistent_thread_pool.py._create_active_thread`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 285
- **Arguments:** self, thread_type, worker_class
- **Docstring:** Create an active thread for immediate use....

---

### `core\threading\persistent_thread_pool.py._create_idle_thread`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 260
- **Arguments:** self, thread_type, worker_class
- **Docstring:** Create an idle thread for the pool....

---

### `core\threading\persistent_thread_pool.py.get_global_persistent_thread_pool`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 407
- **Arguments:** 
- **Returns:** PersistentThreadPool
- **Docstring:** Get the global persistent thread pool instance....

---

### `core\threading\persistent_thread_pool.py.get_pool_status`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 344
- **Arguments:** self
- **Docstring:** Get status of all thread pools....

---

### `core\threading\persistent_thread_pool.py.get_thread`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 130
- **Arguments:** self, thread_type, timeout
- **Docstring:** Get an available thread from the pool.

Args:
    thread_type: Type of thread to get
    timeout: Ma...

---

### `core\threading\persistent_thread_pool.py.initialize_pool`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 95
- **Arguments:** self, thread_type, worker_class
- **Docstring:** Initialize a thread pool with the specified worker class.

Args:
    thread_type: Type of thread poo...

---

### `core\threading\persistent_thread_pool.py.return_thread`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 220
- **Arguments:** self, thread
- **Docstring:** Return a thread to the pool for reuse.

Args:
    thread: Thread to return to the pool...

---

### `core\threading\persistent_thread_pool.py.shutdown`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 366
- **Arguments:** self
- **Docstring:** Shutdown all thread pools....

---

### `core\threading\persistent_thread_pool.py.shutdown_global_persistent_thread_pool`

- **File:** `core\threading\persistent_thread_pool.py`
- **Line:** 418
- **Arguments:** 
- **Docstring:** Shutdown the global persistent thread pool....

---

### `core\threading\qrunnable_tasks.py.__init__`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 591
- **Arguments:** self, calculation_type, parameters

---

### `core\threading\qrunnable_tasks.py._analyze_data`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 532
- **Arguments:** self
- **Docstring:** Analyze the data structure and content....

---

### `core\threading\qrunnable_tasks.py._analyze_sentiment`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 194
- **Arguments:** self
- **Docstring:** Analyze sentiment of the message....

---

### `core\threading\qrunnable_tasks.py._calculate_data`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 477
- **Arguments:** self
- **Docstring:** Perform calculations on the data....

---

### `core\threading\qrunnable_tasks.py._calculate_fibonacci`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 624
- **Arguments:** self
- **Docstring:** Calculate Fibonacci numbers....

---

### `core\threading\qrunnable_tasks.py._calculate_prime_factors`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 649
- **Arguments:** self
- **Docstring:** Calculate prime factors of a number....

---

### `core\threading\qrunnable_tasks.py._calculate_statistics`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 681
- **Arguments:** self
- **Docstring:** Calculate statistical measures....

---

### `core\threading\qrunnable_tasks.py._count_nested_levels`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 564
- **Arguments:** self, data, current_level
- **Returns:** int
- **Docstring:** Count the maximum nesting level in a data structure....

---

### `core\threading\qrunnable_tasks.py._execute_target`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 63
- **Arguments:** self
- **Docstring:** Execute the target function and handle completion....

---

### `core\threading\qrunnable_tasks.py._format_message`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 173
- **Arguments:** self
- **Docstring:** Format the message for better readability....

---

### `core\threading\qrunnable_tasks.py._handle_model_operation`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 381
- **Arguments:** self
- **Docstring:** Handle model operations for Ollama service....

---

### `core\threading\qrunnable_tasks.py._process_file`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 301
- **Arguments:** self
- **Docstring:** Process file content (e.g., JSON parsing, text analysis)....

---

### `core\threading\qrunnable_tasks.py._read_file`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 267
- **Arguments:** self
- **Docstring:** Read file content....

---

### `core\threading\qrunnable_tasks.py._spell_check_message`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 129
- **Arguments:** self
- **Docstring:** Perform spell check on the message....

---

### `core\threading\qrunnable_tasks.py._transform_data`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 505
- **Arguments:** self
- **Docstring:** Transform the data....

---

### `core\threading\qrunnable_tasks.py._write_file`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 286
- **Arguments:** self
- **Docstring:** Write content to file....

---

### `core\threading\qrunnable_tasks.py.run`

- **File:** `core\threading\qrunnable_tasks.py`
- **Line:** 600
- **Arguments:** self
- **Docstring:** Execute the calculation task....

---

### `core\threading\qthread_workers.py.__init__`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 38
- **Arguments:** self, parent

---

### `core\threading\qthread_workers.py._log_thread_info`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 49
- **Arguments:** self, action
- **Docstring:** Log thread information for debugging...

---

### `core\threading\qthread_workers.py._stream_operation`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 473
- **Arguments:** self, monitor_interval, alert_threshold
- **Docstring:** Monitor system resources continuously.

Args:
    monitor_interval: Interval between monitoring chec...

---

### `core\threading\qthread_workers.py.configure_audio_streaming`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 317
- **Arguments:** self, audio_source, sample_rate, chunk_size
- **Docstring:** Configure the worker for audio streaming.

Args:
    audio_source: Source of audio data
    sample_r...

---

### `core\threading\qthread_workers.py.configure_monitoring`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 433
- **Arguments:** self, monitor_interval, alert_threshold
- **Docstring:** Configure the worker for monitoring.

Args:
    monitor_interval: Interval between monitoring checks...

---

### `core\threading\qthread_workers.py.configure_streaming`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 160
- **Arguments:** self, context_messages, model, temperature, config_manager, streaming_message_id
- **Docstring:** Configure the worker for chat streaming.

Args:
    context_messages: List of conversation messages
...

---

### `core\threading\qthread_workers.py.is_running`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 103
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if the worker is currently running....

---

### `core\threading\qthread_workers.py.reset_state`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 81
- **Arguments:** self
- **Docstring:** Reset worker state for reuse in persistent thread pool....

---

### `core\threading\qthread_workers.py.start_audio_streaming`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 345
- **Arguments:** self
- **Docstring:** Start audio streaming operation....

---

### `core\threading\qthread_workers.py.start_monitoring`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 458
- **Arguments:** self
- **Docstring:** Start monitoring operation....

---

### `core\threading\qthread_workers.py.start_streaming`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 107
- **Arguments:** self
- **Docstring:** Start the streaming operation....

---

### `core\threading\qthread_workers.py.stop`

- **File:** `core\threading\qthread_workers.py`
- **Line:** 130
- **Arguments:** self
- **Docstring:** Stop the streaming operation....

---

### `core\threading\thread_calculator.py.__init__`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 56
- **Arguments:** self

---

### `core\threading\thread_calculator.py._calculate_memory_safe_threads`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 301
- **Arguments:** self, memory_gb, logical_cores
- **Returns:** int
- **Docstring:** Calculate thread count based on available memory...

---

### `core\threading\thread_calculator.py._calculate_recommendations`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 190
- **Arguments:** self, cpu_count, logical_cores, physical_cores, memory_gb, system_type
- **Returns:** ThreadRecommendations
- **Docstring:** Calculate specific thread recommendations...

---

### `core\threading\thread_calculator.py.analyze_system`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 432
- **Arguments:** 
- **Docstring:** Print system analysis (useful for debugging)...

---

### `core\threading\thread_calculator.py.calculate_thread_recommendations`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 120
- **Arguments:** self
- **Returns:** ThreadRecommendations
- **Docstring:** Calculate optimal thread counts for different use cases...

---

### `core\threading\thread_calculator.py.get_pool_thread_count`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 420
- **Arguments:** pool_type
- **Returns:** int
- **Docstring:** Get recommended thread count for a specific pool type...

---

### `core\threading\thread_calculator.py.get_recommendations_for_pool`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 320
- **Arguments:** self, pool_type
- **Returns:** int
- **Docstring:** Get thread count recommendation for specific pool type...

---

### `core\threading\thread_calculator.py.get_system_info`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 59
- **Arguments:** self
- **Docstring:** Get comprehensive system information...

---

### `core\threading\thread_calculator.py.get_thread_recommendations`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 395
- **Arguments:** 
- **Returns:** ThreadRecommendations
- **Docstring:** Get thread recommendations for the current system...

---

### `core\threading\thread_calculator.py.print_system_analysis`

- **File:** `core\threading\thread_calculator.py`
- **Line:** 345
- **Arguments:** self
- **Docstring:** Print detailed system analysis and recommendations...

---

### `core\threading\thread_calculator_examples.py.example_dynamic_adjustment`

- **File:** `core\threading\thread_calculator_examples.py`
- **Line:** 109
- **Arguments:** 
- **Docstring:** Example: Dynamically adjusting thread counts based on system load...

---

### `core\threading\thread_calculator_examples.py.example_memory_optimization`

- **File:** `core\threading\thread_calculator_examples.py`
- **Line:** 87
- **Arguments:** 
- **Docstring:** Example: Using thread calculator for memory optimization...

---

### `core\threading\thread_calculator_examples.py.example_persistent_thread_pool`

- **File:** `core\threading\thread_calculator_examples.py`
- **Line:** 42
- **Arguments:** 
- **Docstring:** Example: Using thread calculator with PersistentThreadPool...

---

### `core\threading\thread_calculator_examples.py.example_streaming_configuration`

- **File:** `core\threading\thread_calculator_examples.py`
- **Line:** 67
- **Arguments:** 
- **Docstring:** Example: Using thread calculator for streaming configuration...

---

### `core\threading\thread_calculator_examples.py.example_thread_pool_manager`

- **File:** `core\threading\thread_calculator_examples.py`
- **Line:** 21
- **Arguments:** 
- **Docstring:** Example: Using thread calculator with ThreadPoolManager...

---

### `core\threading\thread_calculator_examples.py.main`

- **File:** `core\threading\thread_calculator_examples.py`
- **Line:** 141
- **Arguments:** 
- **Docstring:** Run all examples...

---

### `core\threading\thread_monitor.py.__init__`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 37
- **Arguments:** self, parent

---

### `core\threading\thread_monitor.py._on_thread_finished`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 298
- **Arguments:** self, thread_name
- **Docstring:** Handle thread finished event....

---

### `core\threading\thread_monitor.py._on_thread_started`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 285
- **Arguments:** self, thread_name
- **Docstring:** Handle thread started event....

---

### `core\threading\thread_monitor.py._update_monitoring`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 325
- **Arguments:** self
- **Docstring:** Update monitoring information and emit signals....

---

### `core\threading\thread_monitor.py.check_thread_safety`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 405
- **Arguments:** self, thread_name
- **Returns:** bool
- **Docstring:** Check if a thread is safe to destroy (not running).

Args:
    thread_name: Name of the thread to ch...

---

### `core\threading\thread_monitor.py.cleanup_old_history`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 257
- **Arguments:** self, max_age_hours
- **Docstring:** Clean up old thread history.

Args:
    max_age_hours: Maximum age in hours for history to keep...

---

### `core\threading\thread_monitor.py.force_thread_cleanup`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 439
- **Arguments:** self, thread_name, timeout_seconds
- **Docstring:** Force cleanup of a thread with timeout.

Args:
    thread_name: Name of the thread to cleanup
    ti...

---

### `core\threading\thread_monitor.py.generate_report`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 339
- **Arguments:** self
- **Docstring:** Generate a comprehensive threading report.

Returns:
    dict: Comprehensive threading report...

---

### `core\threading\thread_monitor.py.get_all_threads_info`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 202
- **Arguments:** self
- **Docstring:** Get information about all threads.

Returns:
    dict: Information about all threads...

---

### `core\threading\thread_monitor.py.get_global_thread_monitor`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 499
- **Arguments:** 
- **Returns:** ThreadMonitor
- **Docstring:** Get the global thread monitor instance.

Returns:
    ThreadMonitor: Global thread monitor...

---

### `core\threading\thread_monitor.py.get_resource_usage`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 221
- **Arguments:** self
- **Docstring:** Get current resource usage statistics.

Returns:
    dict: Resource usage information...

---

### `core\threading\thread_monitor.py.get_running_threads`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 475
- **Arguments:** self
- **Docstring:** Get list of currently running threads.

Returns:
    List[str]: List of running thread names...

---

### `core\threading\thread_monitor.py.get_thread_info`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 173
- **Arguments:** self, thread_name
- **Docstring:** Get information about a specific thread.

Args:
    thread_name: Name of the thread
    
Returns:
  ...

---

### `core\threading\thread_monitor.py.record_thread_error`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 138
- **Arguments:** self, thread_name, error_message, error_type
- **Docstring:** Record an error for a specific thread.

Args:
    thread_name: Name of the thread
    error_message:...

---

### `core\threading\thread_monitor.py.register_thread`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 62
- **Arguments:** self, thread, thread_type, metadata
- **Docstring:** Register a thread for monitoring.

Args:
    thread: QThread instance to monitor
    thread_type: Ty...

---

### `core\threading\thread_monitor.py.shutdown`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 384
- **Arguments:** self
- **Docstring:** Shutdown the thread monitor....

---

### `core\threading\thread_monitor.py.shutdown_global_thread_monitor`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 515
- **Arguments:** 
- **Docstring:** Shutdown the global thread monitor....

---

### `core\threading\thread_monitor.py.unregister_thread`

- **File:** `core\threading\thread_monitor.py`
- **Line:** 107
- **Arguments:** self, thread_name
- **Docstring:** Unregister a thread from monitoring.

Args:
    thread_name: Name of the thread to unregister...

---

### `core\threading\thread_pool_manager.py.__init__`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 39
- **Arguments:** self, max_threads, parent

---

### `core\threading\thread_pool_manager.py._update_pool_status`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 337
- **Arguments:** self
- **Docstring:** Update pool status and emit signals....

---

### `core\threading\thread_pool_manager.py.cancel_all_tasks`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 229
- **Arguments:** self
- **Returns:** int
- **Docstring:** Cancel all active tasks.

Returns:
    int: Number of tasks cancelled...

---

### `core\threading\thread_pool_manager.py.cancel_task`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 193
- **Arguments:** self, task_id
- **Returns:** bool
- **Docstring:** Cancel a specific task.

Args:
    task_id: Task identifier
    
Returns:
    bool: True if task was...

---

### `core\threading\thread_pool_manager.py.cleanup_old_tasks`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 309
- **Arguments:** self, max_age_hours
- **Docstring:** Clean up old completed and failed tasks.

Args:
    max_age_hours: Maximum age in hours for tasks to...

---

### `core\threading\thread_pool_manager.py.get_global_thread_pool_manager`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 443
- **Arguments:** 
- **Returns:** ThreadPoolManager
- **Docstring:** Get the global thread pool manager instance.

Returns:
    ThreadPoolManager: Global thread pool man...

---

### `core\threading\thread_pool_manager.py.get_pool_status`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 250
- **Arguments:** self
- **Docstring:** Get current thread pool status.

Returns:
    dict: Pool status information...

---

### `core\threading\thread_pool_manager.py.get_task_info`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 275
- **Arguments:** self, task_id
- **Docstring:** Get information about a specific task.

Args:
    task_id: Task identifier
    
Returns:
    dict: T...

---

### `core\threading\thread_pool_manager.py.on_task_completed`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 357
- **Arguments:** self, task_id
- **Docstring:** Handle task completion.

Args:
    task_id: Task identifier...

---

### `core\threading\thread_pool_manager.py.on_task_failed`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 385
- **Arguments:** self, task_id, error_message
- **Docstring:** Handle task failure.

Args:
    task_id: Task identifier
    error_message: Error message...

---

### `core\threading\thread_pool_manager.py.shutdown`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 415
- **Arguments:** self
- **Docstring:** Shutdown the thread pool manager....

---

### `core\threading\thread_pool_manager.py.shutdown_global_thread_pool_manager`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 462
- **Arguments:** 
- **Docstring:** Shutdown the global thread pool manager....

---

### `core\threading\thread_pool_manager.py.start_task`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 74
- **Arguments:** self, task, task_id
- **Returns:** str
- **Docstring:** Start a QRunnable task.

Args:
    task: QRunnable task to execute
    task_id: Optional task identi...

---

### `core\threading\thread_pool_manager.py.wait_for_all_tasks`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 166
- **Arguments:** self, timeout
- **Returns:** bool
- **Docstring:** Wait for all active tasks to complete.

Args:
    timeout: Maximum time to wait in seconds
    
Retu...

---

### `core\threading\thread_pool_manager.py.wait_for_task`

- **File:** `core\threading\thread_pool_manager.py`
- **Line:** 138
- **Arguments:** self, task_id, timeout
- **Returns:** bool
- **Docstring:** Wait for a specific task to complete.

Args:
    task_id: Task identifier
    timeout: Maximum time ...

---

### `core\threading\threading_service.py.__init__`

- **File:** `core\threading\threading_service.py`
- **Line:** 44
- **Arguments:** self, parent

---

### `core\threading\threading_service.py._initialize_persistent_pools`

- **File:** `core\threading\threading_service.py`
- **Line:** 102
- **Arguments:** self
- **Docstring:** Initialize persistent thread pools for different operations....

---

### `core\threading\threading_service.py._on_alert_triggered`

- **File:** `core\threading\threading_service.py`
- **Line:** 493
- **Arguments:** self, alert_message
- **Docstring:** Handle alert from monitoring thread....

---

### `core\threading\threading_service.py._on_audio_chunk_received`

- **File:** `core\threading\threading_service.py`
- **Line:** 451
- **Arguments:** self, chunk
- **Docstring:** Handle audio chunk received from persistent thread....

---

### `core\threading\threading_service.py._on_audio_streaming_error`

- **File:** `core\threading\threading_service.py`
- **Line:** 472
- **Arguments:** self, error_message
- **Docstring:** Handle audio streaming error from persistent thread....

---

### `core\threading\threading_service.py._on_audio_streaming_finished`

- **File:** `core\threading\threading_service.py`
- **Line:** 459
- **Arguments:** self
- **Docstring:** Handle audio streaming finished from persistent thread....

---

### `core\threading\threading_service.py._on_chat_chunk_received`

- **File:** `core\threading\threading_service.py`
- **Line:** 407
- **Arguments:** self, chunk, model_name, msg_id, chunk_index
- **Docstring:** Handle chat chunk received from persistent thread....

---

### `core\threading\threading_service.py._on_chat_progress_updated`

- **File:** `core\threading\threading_service.py`
- **Line:** 416
- **Arguments:** self, progress
- **Docstring:** Handle chat progress update from persistent thread....

---

### `core\threading\threading_service.py._on_chat_streaming_error`

- **File:** `core\threading\threading_service.py`
- **Line:** 437
- **Arguments:** self, error_message
- **Docstring:** Handle chat streaming error from persistent thread....

---

### `core\threading\threading_service.py._on_chat_streaming_finished`

- **File:** `core\threading\threading_service.py`
- **Line:** 423
- **Arguments:** self
- **Docstring:** Handle chat streaming finished from persistent thread....

---

### `core\threading\threading_service.py._on_monitoring_error`

- **File:** `core\threading\threading_service.py`
- **Line:** 513
- **Arguments:** self, error_message
- **Docstring:** Handle monitoring error from persistent thread....

---

### `core\threading\threading_service.py._on_monitoring_finished`

- **File:** `core\threading\threading_service.py`
- **Line:** 500
- **Arguments:** self
- **Docstring:** Handle monitoring finished from persistent thread....

---

### `core\threading\threading_service.py._on_resource_updated`

- **File:** `core\threading\threading_service.py`
- **Line:** 485
- **Arguments:** self, resource_data
- **Docstring:** Handle resource update from monitoring thread....

---

### `core\threading\threading_service.py.cleanup`

- **File:** `core\threading\threading_service.py`
- **Line:** 606
- **Arguments:** self
- **Docstring:** Clean up all threading resources....

---

### `core\threading\threading_service.py.get_global_threading_service`

- **File:** `core\threading\threading_service.py`
- **Line:** 638
- **Arguments:** 
- **Returns:** ThreadingService
- **Docstring:** Get the global threading service instance....

---

### `core\threading\threading_service.py.get_threading_status`

- **File:** `core\threading\threading_service.py`
- **Line:** 572
- **Arguments:** self
- **Docstring:** Get current threading status and statistics....

---

### `core\threading\threading_service.py.process_data`

- **File:** `core\threading\threading_service.py`
- **Line:** 557
- **Arguments:** self, data, operation, callback
- **Returns:** str
- **Docstring:** Process data using QRunnable....

---

### `core\threading\threading_service.py.process_file`

- **File:** `core\threading\threading_service.py`
- **Line:** 542
- **Arguments:** self, file_path, operation, callback
- **Returns:** str
- **Docstring:** Process file operation using QRunnable....

---

### `core\threading\threading_service.py.process_message`

- **File:** `core\threading\threading_service.py`
- **Line:** 527
- **Arguments:** self, message, operation, callback
- **Returns:** str
- **Docstring:** Process message using QRunnable....

---

### `core\threading\threading_service.py.shutdown_global_threading_service`

- **File:** `core\threading\threading_service.py`
- **Line:** 649
- **Arguments:** 
- **Docstring:** Shutdown the global threading service....

---

### `core\threading\threading_service.py.start_audio_streaming`

- **File:** `core\threading\threading_service.py`
- **Line:** 273
- **Arguments:** self, audio_source, sample_rate, chunk_size
- **Returns:** bool
- **Docstring:** Start audio streaming using persistent thread pool....

---

### `core\threading\threading_service.py.start_chat_streaming`

- **File:** `core\threading\threading_service.py`
- **Line:** 179
- **Arguments:** self, context_messages, model, temperature, config_manager, streaming_message_id
- **Returns:** bool
- **Docstring:** Start chat streaming using persistent thread pool.

This method:
- Gets a thread from the persistent...

---

### `core\threading\threading_service.py.start_monitoring`

- **File:** `core\threading\threading_service.py`
- **Line:** 339
- **Arguments:** self, monitor_interval, alert_threshold
- **Returns:** bool
- **Docstring:** Start system monitoring using persistent thread pool....

---

### `core\threading\threading_service.py.stop_audio_streaming`

- **File:** `core\threading\threading_service.py`
- **Line:** 320
- **Arguments:** self
- **Docstring:** Stop audio streaming and return thread to pool....

---

### `core\threading\threading_service.py.stop_chat_streaming`

- **File:** `core\threading\threading_service.py`
- **Line:** 244
- **Arguments:** self
- **Docstring:** Stop chat streaming and return thread to pool....

---

### `core\threading\threading_service.py.stop_monitoring`

- **File:** `core\threading\threading_service.py`
- **Line:** 387
- **Arguments:** self
- **Docstring:** Stop monitoring and return thread to pool....

---

### `core\threading\usage_examples.py.__init__`

- **File:** `core\threading\usage_examples.py`
- **Line:** 25
- **Arguments:** self

---

### `core\threading\usage_examples.py._on_chat_chunk_received`

- **File:** `core\threading\usage_examples.py`
- **Line:** 249
- **Arguments:** self, chunk
- **Docstring:** Handle chat chunk received from streaming worker....

---

### `core\threading\usage_examples.py._on_chat_progress_updated`

- **File:** `core\threading\usage_examples.py`
- **Line:** 258
- **Arguments:** self, progress
- **Docstring:** Handle chat progress update from streaming worker....

---

### `core\threading\usage_examples.py._on_chat_streaming_error`

- **File:** `core\threading\usage_examples.py`
- **Line:** 276
- **Arguments:** self, error
- **Docstring:** Handle chat streaming error....

---

### `core\threading\usage_examples.py._on_chat_streaming_finished`

- **File:** `core\threading\usage_examples.py`
- **Line:** 267
- **Arguments:** self
- **Docstring:** Handle chat streaming finished....

---

### `core\threading\usage_examples.py._on_chat_streaming_thread_finished`

- **File:** `core\threading\usage_examples.py`
- **Line:** 113
- **Arguments:** self
- **Docstring:** Handle chat streaming thread finished....

---

### `core\threading\usage_examples.py.cleanup`

- **File:** `core\threading\usage_examples.py`
- **Line:** 367
- **Arguments:** self
- **Docstring:** Clean up all threading resources....

---

### `core\threading\usage_examples.py.demonstrate_threading_usage`

- **File:** `core\threading\usage_examples.py`
- **Line:** 388
- **Arguments:** 
- **Docstring:** Demonstrate the usage of QThread vs QRunnable in a chat application.

This function shows:
1. How to...

---

### `core\threading\usage_examples.py.get_threading_status`

- **File:** `core\threading\usage_examples.py`
- **Line:** 342
- **Arguments:** self
- **Docstring:** Get current threading status and statistics....

---

### `core\threading\usage_examples.py.on_file_processed`

- **File:** `core\threading\usage_examples.py`
- **Line:** 318
- **Arguments:** self, operation, file_path, result
- **Docstring:** Handle file processing completion....

---

### `core\threading\usage_examples.py.on_file_processing_error`

- **File:** `core\threading\usage_examples.py`
- **Line:** 333
- **Arguments:** self, operation, file_path, error_message
- **Docstring:** Handle file processing error....

---

### `core\threading\usage_examples.py.on_message_processed`

- **File:** `core\threading\usage_examples.py`
- **Line:** 287
- **Arguments:** self, task_type, result
- **Docstring:** Handle message processing completion....

---

### `core\threading\usage_examples.py.on_message_processing_error`

- **File:** `core\threading\usage_examples.py`
- **Line:** 309
- **Arguments:** self, task_type, error_message
- **Docstring:** Handle message processing error....

---

### `core\threading\usage_examples.py.process_file_operation`

- **File:** `core\threading\usage_examples.py`
- **Line:** 218
- **Arguments:** self, file_path, operation
- **Docstring:** Process file operation using QRunnable....

---

### `core\threading\usage_examples.py.process_message_formatting`

- **File:** `core\threading\usage_examples.py`
- **Line:** 191
- **Arguments:** self, message
- **Docstring:** Process message formatting using QRunnable....

---

### `core\threading\usage_examples.py.process_message_spell_check`

- **File:** `core\threading\usage_examples.py`
- **Line:** 158
- **Arguments:** self, message
- **Docstring:** Process message spell check using QRunnable (short-lived, fire-and-forget task).

This is a QRunnabl...

---

### `core\threading\usage_examples.py.start_chat_streaming`

- **File:** `core\threading\usage_examples.py`
- **Line:** 40
- **Arguments:** self, messages, model, temperature, ollama_url, max_tokens, top_p, frequency_penalty, presence_penalty
- **Docstring:** Start chat streaming using QThread (long-running, persistent task).

This is a QThread use case beca...

---

### `core\threading\usage_examples.py.stop_chat_streaming`

- **File:** `core\threading\usage_examples.py`
- **Line:** 135
- **Arguments:** self
- **Docstring:** Stop chat streaming safely....

---

### `core\utils\error_handler.py.audio_operation_context`

- **File:** `core\utils\error_handler.py`
- **Line:** 288
- **Arguments:** operation
- **Decorators:** contextmanager
- **Docstring:** Context manager for audio operations with error handling

Args:
    operation: Audio operation being...

---

### `core\utils\error_handler.py.cleanup_resources`

- **File:** `core\utils\error_handler.py`
- **Line:** 449
- **Arguments:** resources
- **Docstring:** Safely cleanup a list of resources

Args:
    resources: List of resources to cleanup...

---

### `core\utils\error_handler.py.error_context`

- **File:** `core\utils\error_handler.py`
- **Line:** 231
- **Arguments:** operation, context
- **Decorators:** contextmanager
- **Docstring:** Context manager for error handling with automatic logging

Args:
    operation: Name of the operatio...

---

### `core\utils\error_handler.py.file_operation_context`

- **File:** `core\utils\error_handler.py`
- **Line:** 271
- **Arguments:** operation, filepath
- **Decorators:** contextmanager
- **Docstring:** Context manager for file operations with error handling

Args:
    operation: File operation being p...

---

### `core\utils\error_handler.py.handle_audio_operations`

- **File:** `core\utils\error_handler.py`
- **Line:** 161
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle audio operation errors

Args:
    func: Function to decorate
    
Returns:
    D...

---

### `core\utils\error_handler.py.handle_critical_error`

- **File:** `core\utils\error_handler.py`
- **Line:** 468
- **Arguments:** error, component, recovery_action
- **Docstring:** Handle critical errors that may require application restart

Args:
    error: The critical error
   ...

---

### `core\utils\error_handler.py.handle_file_operations`

- **File:** `core\utils\error_handler.py`
- **Line:** 127
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle file operation errors

Args:
    func: Function to decorate
    
Returns:
    De...

---

### `core\utils\error_handler.py.handle_memory_operations`

- **File:** `core\utils\error_handler.py`
- **Line:** 184
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle memory operation errors

Args:
    func: Function to decorate
    
Returns:
    ...

---

### `core\utils\error_handler.py.handle_network_errors`

- **File:** `core\utils\error_handler.py`
- **Line:** 93
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle network-related errors specifically

Args:
    func: Function to decorate
    
R...

---

### `core\utils\error_handler.py.handle_ui_operations`

- **File:** `core\utils\error_handler.py`
- **Line:** 207
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle UI operation errors

Args:
    func: Function to decorate
    
Returns:
    Deco...

---

### `core\utils\error_handler.py.memory_operation_context`

- **File:** `core\utils\error_handler.py`
- **Line:** 304
- **Arguments:** operation, memory_type
- **Decorators:** contextmanager
- **Docstring:** Context manager for memory operations with error handling

Args:
    operation: Memory operation bei...

---

### `core\utils\error_handler.py.network_error_context`

- **File:** `core\utils\error_handler.py`
- **Line:** 254
- **Arguments:** url, method
- **Decorators:** contextmanager
- **Docstring:** Context manager for network operations with error handling

Args:
    url: URL being accessed
    me...

---

### `core\utils\error_handler.py.retry_on_failure`

- **File:** `core\utils\error_handler.py`
- **Line:** 51
- **Arguments:** func, max_attempts, delay_seconds, exceptions
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to retry a function on failure

Args:
    func: Function to retry
    max_attempts: Maximu...

---

### `core\utils\error_handler.py.safe_execute`

- **File:** `core\utils\error_handler.py`
- **Line:** 26
- **Arguments:** func
- **Returns:** Any
- **Decorators:** staticmethod
- **Docstring:** Safely execute a function with comprehensive error handling

Args:
    func: Function to execute
   ...

---

### `core\utils\error_handler.py.safe_file_read`

- **File:** `core\utils\error_handler.py`
- **Line:** 358
- **Arguments:** filepath, encoding, default
- **Returns:** Any
- **Docstring:** Safely read a file with error handling

Args:
    filepath: Path to the file
    encoding: File enco...

---

### `core\utils\error_handler.py.safe_file_write`

- **File:** `core\utils\error_handler.py`
- **Line:** 378
- **Arguments:** filepath, content, encoding
- **Returns:** bool
- **Docstring:** Safely write to a file with error handling

Args:
    filepath: Path to the file
    content: Conten...

---

### `core\utils\error_handler.py.safe_json_parse`

- **File:** `core\utils\error_handler.py`
- **Line:** 337
- **Arguments:** json_str, default
- **Returns:** Any
- **Docstring:** Safely parse JSON string with error handling

Args:
    json_str: JSON string to parse
    default: ...

---

### `core\utils\error_handler.py.safe_network_request`

- **File:** `core\utils\error_handler.py`
- **Line:** 402
- **Arguments:** url, method
- **Docstring:** Safely make a network request with error handling

Args:
    url: URL to request
    method: HTTP me...

---

### `core\utils\error_handler.py.ui_operation_context`

- **File:** `core\utils\error_handler.py`
- **Line:** 321
- **Arguments:** component, operation
- **Decorators:** contextmanager
- **Docstring:** Context manager for UI operations with error handling

Args:
    component: UI component being opera...

---

### `core\utils\error_handler.py.validate_input`

- **File:** `core\utils\error_handler.py`
- **Line:** 424
- **Arguments:** data, expected_type, field_name
- **Returns:** bool
- **Docstring:** Validate input data with error handling

Args:
    data: Data to validate
    expected_type: Expecte...

---

### `core\utils\error_handler.py.wrapper`

- **File:** `core\utils\error_handler.py`
- **Line:** 218
- **Arguments:** 
- **Decorators:** functools.wraps

---

### `core\utils\internet_checker.py.__init__`

- **File:** `core\utils\internet_checker.py`
- **Line:** 24
- **Arguments:** self, timeout
- **Docstring:** Initialize the internet connection tester.

Args:
    timeout (float): Timeout in seconds for connec...

---

### `core\utils\internet_checker.py.check_internet`

- **File:** `core\utils\internet_checker.py`
- **Line:** 166
- **Arguments:** 
- **Returns:** bool
- **Docstring:** Alias for is_online() for backward compatibility.

Returns:
    bool: True if internet connection is...

---

### `core\utils\internet_checker.py.is_online`

- **File:** `core\utils\internet_checker.py`
- **Line:** 155
- **Arguments:** 
- **Returns:** bool
- **Docstring:** Quick check for internet connectivity using default settings.

Returns:
    bool: True if internet c...

---

### `core\utils\internet_checker.py.test_connection`

- **File:** `core\utils\internet_checker.py`
- **Line:** 77
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Test internet connectivity using multiple methods.

Returns:
    bool: True if internet connection i...

---

### `core\utils\internet_checker.py.test_connection_with_details`

- **File:** `core\utils\internet_checker.py`
- **Line:** 96
- **Arguments:** self
- **Docstring:** Test internet connectivity and return detailed results.

Returns:
    Tuple[bool, List[str]]: (is_co...

---

### `core\utils\internet_checker.py.test_http_connection`

- **File:** `core\utils\internet_checker.py`
- **Line:** 60
- **Arguments:** self, url
- **Returns:** bool
- **Docstring:** Test connection using HTTP request to a specific URL.

Args:
    url (str): URL to test
    
Returns...

---

### `core\utils\internet_checker.py.test_internet_connection`

- **File:** `core\utils\internet_checker.py`
- **Line:** 127
- **Arguments:** timeout
- **Returns:** bool
- **Docstring:** Simple function to test internet connectivity.

Args:
    timeout (float): Timeout in seconds for co...

---

### `core\utils\internet_checker.py.test_internet_connection_detailed`

- **File:** `core\utils\internet_checker.py`
- **Line:** 141
- **Arguments:** timeout
- **Docstring:** Test internet connectivity with detailed failure information.

Args:
    timeout (float): Timeout in...

---

### `core\utils\internet_checker.py.test_socket_connection`

- **File:** `core\utils\internet_checker.py`
- **Line:** 43
- **Arguments:** self, host, port
- **Returns:** bool
- **Docstring:** Test connection using socket to a specific host and port.

Args:
    host (str): Host to connect to
...

---

### `core\utils\prompts.py.format_auto_model_selection_info`

- **File:** `core\utils\prompts.py`
- **Line:** 96
- **Arguments:** model
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format auto model selection info message...

---

### `core\utils\prompts.py.format_conversation_status`

- **File:** `core\utils\prompts.py`
- **Line:** 101
- **Arguments:** status_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format conversation status message...

---

### `core\utils\prompts.py.format_error_message`

- **File:** `core\utils\prompts.py`
- **Line:** 112
- **Arguments:** error_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format error message...

---

### `core\utils\prompts.py.format_fact_extraction_prompt`

- **File:** `core\utils\prompts.py`
- **Line:** 89
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format the fact extraction prompt with the given message...

---

### `core\utils\prompts.py.format_memory_status`

- **File:** `core\utils\prompts.py`
- **Line:** 107
- **Arguments:** status_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format memory status message...

---

### `core\utils\prompts.py.format_status_message`

- **File:** `core\utils\prompts.py`
- **Line:** 118
- **Arguments:** status_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format status message...

---

### `core\utils\prompts.py.get_menu_text`

- **File:** `core\utils\prompts.py`
- **Line:** 124
- **Arguments:** menu_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Get menu text...

---

### `core\utils\streaming_handler.py.__init__`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 21
- **Arguments:** self, render_callback, ai_name

---

### `core\utils\streaming_handler.py._flush_stream_buffer`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 66
- **Arguments:** self
- **Docstring:** Flush the stream buffer...

---

### `core\utils\streaming_handler.py._get_next_message_id`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 43
- **Arguments:** self
- **Returns:** str
- **Docstring:** Generate a unique message ID...

---

### `core\utils\streaming_handler.py._process_typewriter_chunk`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 158
- **Arguments:** self
- **Docstring:** Process a chunk with typewriter effect delay...

---

### `core\utils\streaming_handler.py._request_render`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 57
- **Arguments:** self, immediate
- **Docstring:** Request a render through the callback...

---

### `core\utils\streaming_handler.py.append_message`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 83
- **Arguments:** self, sender, content, is_code, tag
- **Docstring:** Append a new message (user or system)...

---

### `core\utils\streaming_handler.py.cleanup`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 250
- **Arguments:** self
- **Docstring:** Clean up resources...

---

### `core\utils\streaming_handler.py.clear_messages`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 245
- **Arguments:** self
- **Docstring:** Clear all messages...

---

### `core\utils\streaming_handler.py.edit_message`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 104
- **Arguments:** self, message_index, new_content
- **Returns:** bool
- **Docstring:** Edit a specific message by index...

---

### `core\utils\streaming_handler.py.finalize_streaming_message`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 195
- **Arguments:** self
- **Docstring:** Mark the last streaming message as finalized...

---

### `core\utils\streaming_handler.py.get_editable_messages`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 126
- **Arguments:** self
- **Docstring:** Get list of messages that can be edited (non-streaming, non-system)...

---

### `core\utils\streaming_handler.py.get_message_by_id`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 119
- **Arguments:** self, message_id
- **Returns:** int
- **Docstring:** Get message index by message_id...

---

### `core\utils\streaming_handler.py.get_messages`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 139
- **Arguments:** self
- **Docstring:** Get all messages as a list of dictionaries...

---

### `core\utils\streaming_handler.py.remove_streaming_placeholder`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 228
- **Arguments:** self
- **Docstring:** Remove the last streaming placeholder message...

---

### `core\utils\streaming_handler.py.set_render_callback`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 48
- **Arguments:** self, callback
- **Docstring:** Set the render callback for UI updates...

---

### `core\utils\streaming_handler.py.start_streaming_message`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 143
- **Arguments:** self, sender, tag
- **Docstring:** Start a streaming message...

---

### `core\utils\streaming_handler.py.sync_messages_to_renderer`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 52
- **Arguments:** self, renderer
- **Docstring:** Sync messages to the renderer...

---

### `core\utils\streaming_handler.py.update_last_system_switch`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 212
- **Arguments:** self, message
- **Docstring:** Update the last system message with new content...

---

### `core\utils\streaming_handler.py.update_streaming_message`

- **File:** `core\utils\streaming_handler.py`
- **Line:** 180
- **Arguments:** self, content, sender, message_id, is_code, tag, append
- **Docstring:** Update the content of the last streaming message with typewriter effect...

---

### `core\utils\threading_audit.py.__init__`

- **File:** `core\utils\threading_audit.py`
- **Line:** 26
- **Arguments:** self

---

### `core\utils\threading_audit.py._get_thread_breakdown`

- **File:** `core\utils\threading_audit.py`
- **Line:** 159
- **Arguments:** self
- **Docstring:** Get breakdown of threads by type...

---

### `core\utils\threading_audit.py.analyze_current_threads`

- **File:** `core\utils\threading_audit.py`
- **Line:** 33
- **Arguments:** self
- **Docstring:** Analyze all currently active threads...

---

### `core\utils\threading_audit.py.check_thread_safety_patterns`

- **File:** `core\utils\threading_audit.py`
- **Line:** 126
- **Arguments:** self
- **Docstring:** Check for common thread safety patterns and issues...

---

### `core\utils\threading_audit.py.detect_cross_thread_ui_operations`

- **File:** `core\utils\threading_audit.py`
- **Line:** 103
- **Arguments:** self
- **Docstring:** Detect potential cross-thread UI operations...

---

### `core\utils\threading_audit.py.generate_recommendations`

- **File:** `core\utils\threading_audit.py`
- **Line:** 167
- **Arguments:** self
- **Docstring:** Generate recommendations for thread safety improvements...

---

### `core\utils\threading_audit.py.generate_report`

- **File:** `core\utils\threading_audit.py`
- **Line:** 218
- **Arguments:** self
- **Returns:** str
- **Docstring:** Generate a comprehensive thread safety report...

---

### `core\utils\threading_audit.py.quick_thread_check`

- **File:** `core\utils\threading_audit.py`
- **Line:** 295
- **Arguments:** 
- **Docstring:** Perform a quick thread safety check.

Returns:
    Dict containing basic thread safety information...

---

### `core\utils\threading_audit.py.run_full_analysis`

- **File:** `core\utils\threading_audit.py`
- **Line:** 202
- **Arguments:** self
- **Docstring:** Run a complete thread safety analysis...

---

### `core\utils\threading_audit.py.run_thread_safety_audit`

- **File:** `core\utils\threading_audit.py`
- **Line:** 283
- **Arguments:** 
- **Returns:** ThreadSafetyAuditor
- **Docstring:** Run a complete thread safety audit and return the auditor instance.

Returns:
    ThreadSafetyAudito...

---

### `core\utils\threading_audit.py.save_report`

- **File:** `core\utils\threading_audit.py`
- **Line:** 272
- **Arguments:** self, filepath
- **Docstring:** Save the thread safety report to a file...

---

### `core\utils\threading_utils.py.__call__`

- **File:** `core\utils\threading_utils.py`
- **Line:** 272
- **Arguments:** self
- **Docstring:** Execute the callback in a thread-safe manner....

---

### `core\utils\threading_utils.py.__init__`

- **File:** `core\utils\threading_utils.py`
- **Line:** 267
- **Arguments:** self, callback

---

### `core\utils\threading_utils.py.call_method`

- **File:** `core\utils\threading_utils.py`
- **Line:** 420
- **Arguments:** 

---

### `core\utils\threading_utils.py.create_thread_safe_callback`

- **File:** `core\utils\threading_utils.py`
- **Line:** 238
- **Arguments:** callback
- **Docstring:** Create a thread-safe callback that ensures execution in the main thread.

Args:
    callback: The ca...

---

### `core\utils\threading_utils.py.ensure_main_thread`

- **File:** `core\utils\threading_utils.py`
- **Line:** 283
- **Arguments:** func
- **Returns:** Callable
- **Docstring:** Decorator to ensure a function runs in the main thread.

Args:
    func: The function to wrap

Retur...

---

### `core\utils\threading_utils.py.force_update`

- **File:** `core\utils\threading_utils.py`
- **Line:** 174
- **Arguments:** 

---

### `core\utils\threading_utils.py.is_main_thread`

- **File:** `core\utils\threading_utils.py`
- **Line:** 13
- **Arguments:** 
- **Returns:** bool
- **Docstring:** Check if current thread is the main (GUI) thread....

---

### `core\utils\threading_utils.py.log_thread_info`

- **File:** `core\utils\threading_utils.py`
- **Line:** 303
- **Arguments:** operation, logger_instance
- **Docstring:** Log thread information for debugging.

Args:
    operation: Description of the operation being perfo...

---

### `core\utils\threading_utils.py.safe_button_update`

- **File:** `core\utils\threading_utils.py`
- **Line:** 78
- **Arguments:** button, enabled, visible, text
- **Docstring:** Safely update button properties from any thread.

Args:
    button: The button to update
    enabled...

---

### `core\utils\threading_utils.py.safe_call_method`

- **File:** `core\utils\threading_utils.py`
- **Line:** 403
- **Arguments:** widget, method_name
- **Docstring:** Safely call a widget method from any thread.

Args:
    widget: The widget to call the method on
   ...

---

### `core\utils\threading_utils.py.safe_connect_signal`

- **File:** `core\utils\threading_utils.py`
- **Line:** 186
- **Arguments:** signal, slot, connection_type
- **Docstring:** Safely connect a signal to a slot with proper connection type.

Args:
    signal: The signal to conn...

---

### `core\utils\threading_utils.py.safe_disconnect`

- **File:** `core\utils\threading_utils.py`
- **Line:** 341
- **Arguments:** signal, slot
- **Docstring:** Safely disconnect a signal from a slot.

Args:
    signal: The signal to disconnect
    slot: The sl...

---

### `core\utils\threading_utils.py.safe_disconnect_signal`

- **File:** `core\utils\threading_utils.py`
- **Line:** 224
- **Arguments:** signal, slot
- **Docstring:** Safely disconnect a signal from a slot.

Args:
    signal: The signal to disconnect
    slot: The sl...

---

### `core\utils\threading_utils.py.safe_emit_signal`

- **File:** `core\utils\threading_utils.py`
- **Line:** 358
- **Arguments:** signal
- **Docstring:** Safely emit a signal from any thread.

Args:
    signal: The signal to emit
    *args: Arguments to ...

---

### `core\utils\threading_utils.py.safe_enable_widget`

- **File:** `core\utils\threading_utils.py`
- **Line:** 452
- **Arguments:** widget, enabled
- **Docstring:** Safely enable/disable a widget from any thread.

Args:
    widget: The widget to enable/disable
    ...

---

### `core\utils\threading_utils.py.safe_force_update`

- **File:** `core\utils\threading_utils.py`
- **Line:** 160
- **Arguments:** widget
- **Docstring:** Safely force a widget update without using processEvents.

Args:
    widget: The widget to update...

---

### `core\utils\threading_utils.py.safe_hide_widget`

- **File:** `core\utils\threading_utils.py`
- **Line:** 442
- **Arguments:** widget
- **Docstring:** Safely hide a widget from any thread.

Args:
    widget: The widget to hide...

---

### `core\utils\threading_utils.py.safe_log_thread_info`

- **File:** `core\utils\threading_utils.py`
- **Line:** 322
- **Arguments:** operation
- **Docstring:** Safely log thread information for debugging.

Args:
    operation: Description of the operation bein...

---

### `core\utils\threading_utils.py.safe_process_events_alternative`

- **File:** `core\utils\threading_utils.py`
- **Line:** 144
- **Arguments:** 
- **Docstring:** Alternative to processEvents() that's safer for background threads.
This schedules a small delay to ...

---

### `core\utils\threading_utils.py.safe_set_property`

- **File:** `core\utils\threading_utils.py`
- **Line:** 377
- **Arguments:** widget, property_name, value
- **Docstring:** Safely set a widget property from any thread.

Args:
    widget: The widget to update
    property_n...

---

### `core\utils\threading_utils.py.safe_set_style`

- **File:** `core\utils\threading_utils.py`
- **Line:** 474
- **Arguments:** widget, style
- **Docstring:** Safely set style sheet on a widget from any thread.

Args:
    widget: The widget to update
    styl...

---

### `core\utils\threading_utils.py.safe_set_text`

- **File:** `core\utils\threading_utils.py`
- **Line:** 463
- **Arguments:** widget, text
- **Docstring:** Safely set text on a widget from any thread.

Args:
    widget: The widget to update
    text: The t...

---

### `core\utils\threading_utils.py.safe_show_widget`

- **File:** `core\utils\threading_utils.py`
- **Line:** 432
- **Arguments:** widget
- **Docstring:** Safely show a widget from any thread.

Args:
    widget: The widget to show...

---

### `core\utils\threading_utils.py.safe_signal_connect`

- **File:** `core\utils\threading_utils.py`
- **Line:** 201
- **Arguments:** signal, slot, connection_type
- **Docstring:** Alias for safe_connect_signal for backward compatibility.

Args:
    signal: The signal to connect
 ...

---

### `core\utils\threading_utils.py.safe_signal_disconnect`

- **File:** `core\utils\threading_utils.py`
- **Line:** 213
- **Arguments:** signal, slot
- **Docstring:** Alias for safe_disconnect for backward compatibility.

Args:
    signal: The signal to disconnect
  ...

---

### `core\utils\threading_utils.py.safe_ui_update`

- **File:** `core\utils\threading_utils.py`
- **Line:** 18
- **Arguments:** target, method
- **Docstring:** Safely update UI from any thread.

Args:
    target: The QObject to call the method on
    method: T...

---

### `core\utils\threading_utils.py.safe_ui_update_with_callback`

- **File:** `core\utils\threading_utils.py`
- **Line:** 44
- **Arguments:** target, method, callback
- **Docstring:** Safely update UI from any thread with optional callback.

Args:
    target: The QObject to call the ...

---

### `core\utils\threading_utils.py.safe_widget_update`

- **File:** `core\utils\threading_utils.py`
- **Line:** 117
- **Arguments:** widget, method
- **Docstring:** Safely update any widget from any thread.

Args:
    widget: The widget to update
    method: The me...

---

### `core\utils\threading_utils.py.set_property`

- **File:** `core\utils\threading_utils.py`
- **Line:** 392
- **Arguments:** 

---

### `core\utils\threading_utils.py.thread_safe_callback`

- **File:** `core\utils\threading_utils.py`
- **Line:** 250
- **Arguments:** 

---

### `core\utils\threading_utils.py.ui_update_with_callback`

- **File:** `core\utils\threading_utils.py`
- **Line:** 64
- **Arguments:** 

---

### `core\utils\threading_utils.py.update_button`

- **File:** `core\utils\threading_utils.py`
- **Line:** 100
- **Arguments:** 

---

### `core\utils\threading_utils.py.update_widget`

- **File:** `core\utils\threading_utils.py`
- **Line:** 133
- **Arguments:** 

---

### `core\utils\threading_utils.py.wrapper`

- **File:** `core\utils\threading_utils.py`
- **Line:** 293
- **Arguments:** 

---

### `features\chat\chat_controller.py.__init__`

- **File:** `features\chat\chat_controller.py`
- **Line:** 52
- **Arguments:** self, ollama_service, conversation_service, enhancement_service, memory_service, conversation_manager, personality_service

---

### `features\chat\chat_controller.py._build_context`

- **File:** `features\chat\chat_controller.py`
- **Line:** 287
- **Arguments:** self, context_messages, is_new_conversation
- **Docstring:** Build the final context for the AI...

---

### `features\chat\chat_controller.py._detect_new_conversation`

- **File:** `features\chat\chat_controller.py`
- **Line:** 273
- **Arguments:** self, context_messages
- **Returns:** bool
- **Docstring:** Detect if this is a new conversation...

---

### `features\chat\chat_controller.py._extract_and_store_facts`

- **File:** `features\chat\chat_controller.py`
- **Line:** 140
- **Arguments:** self, message
- **Docstring:** Extract facts from the message using LLM and store in long-term memory...

---

### `features\chat\chat_controller.py._extract_facts_with_llm`

- **File:** `features\chat\chat_controller.py`
- **Line:** 163
- **Arguments:** self, message
- **Docstring:** Use qwen3:0.6b to extract facts as key-value pairs from a message...

---

### `features\chat\chat_controller.py._handle_memory_operations`

- **File:** `features\chat\chat_controller.py`
- **Line:** 127
- **Arguments:** self, message
- **Docstring:** Handle memory-related operations for a message...

---

### `features\chat\chat_controller.py._select_model`

- **File:** `features\chat\chat_controller.py`
- **Line:** 293
- **Arguments:** self, requested_model, message, context_messages
- **Returns:** str
- **Docstring:** Select the appropriate model for the request...

---

### `features\chat\chat_controller.py._send_to_ollama`

- **File:** `features\chat\chat_controller.py`
- **Line:** 248
- **Arguments:** self, message, model, temperature
- **Docstring:** Send message to Ollama and handle response...

---

### `features\chat\chat_controller.py._store_extracted_facts`

- **File:** `features\chat\chat_controller.py`
- **Line:** 223
- **Arguments:** self, facts
- **Docstring:** Store extracted facts in memory...

---

### `features\chat\chat_controller.py._trigger_name_generation`

- **File:** `features\chat\chat_controller.py`
- **Line:** 442
- **Arguments:** self, filepath
- **Docstring:** Trigger AI name generation for a conversation...

---

### `features\chat\chat_controller.py._trigger_tts_for_response`

- **File:** `features\chat\chat_controller.py`
- **Line:** 396
- **Arguments:** self, response
- **Docstring:** Trigger TTS for AI response if voice mode is active...

---

### `features\chat\chat_controller.py.accumulate_assistant_response`

- **File:** `features\chat\chat_controller.py`
- **Line:** 314
- **Arguments:** self, chunk
- **Docstring:** Accumulate assistant response chunk....

---

### `features\chat\chat_controller.py.clear_conversation`

- **File:** `features\chat\chat_controller.py`
- **Line:** 496
- **Arguments:** self
- **Docstring:** Clear the current conversation...

---

### `features\chat\chat_controller.py.clear_pending_assistant_response`

- **File:** `features\chat\chat_controller.py`
- **Line:** 323
- **Arguments:** self

---

### `features\chat\chat_controller.py.delete_conversation`

- **File:** `features\chat\chat_controller.py`
- **Line:** 529
- **Arguments:** self, filepath
- **Docstring:** Delete a conversation...

---

### `features\chat\chat_controller.py.finalize_streaming_response`

- **File:** `features\chat\chat_controller.py`
- **Line:** 332
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Finalize the current streaming response...

---

### `features\chat\chat_controller.py.get_ai_name`

- **File:** `features\chat\chat_controller.py`
- **Line:** 433
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the AI name from the current personality...

---

### `features\chat\chat_controller.py.handle_ai_response`

- **File:** `features\chat\chat_controller.py`
- **Line:** 341
- **Arguments:** self
- **Docstring:** Handle AI response completion using accumulated response....

---

### `features\chat\chat_controller.py.is_memory_active`

- **File:** `features\chat\chat_controller.py`
- **Line:** 74
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if memory is enabled and available...

---

### `features\chat\chat_controller.py.load_conversation`

- **File:** `features\chat\chat_controller.py`
- **Line:** 502
- **Arguments:** self, filepath
- **Docstring:** Load a conversation from file...

---

### `features\chat\chat_controller.py.process_user_message`

- **File:** `features\chat\chat_controller.py`
- **Line:** 78
- **Arguments:** self, message, model, temperature
- **Docstring:** Process a user message and send to Ollama...

---

### `features\chat\chat_controller.py.remove_emojis`

- **File:** `features\chat\chat_controller.py`
- **Line:** 25
- **Arguments:** text

---

### `features\chat\chat_controller.py.rename_conversation`

- **File:** `features\chat\chat_controller.py`
- **Line:** 542
- **Arguments:** self, old_filepath, new_filepath
- **Docstring:** Handle conversation rename...

---

### `features\chat\chat_controller.py.reset_ai_response_guard`

- **File:** `features\chat\chat_controller.py`
- **Line:** 556
- **Arguments:** self
- **Docstring:** Reset the AI response guard for a new streaming session....

---

### `features\chat\chat_controller.py.set_chat_tab_reference`

- **File:** `features\chat\chat_controller.py`
- **Line:** 429
- **Arguments:** self, chat_tab
- **Docstring:** Set reference to chat tab for TTS functionality...

---

### `features\chat\chat_controller.py.start_new_conversation`

- **File:** `features\chat\chat_controller.py`
- **Line:** 449
- **Arguments:** self
- **Docstring:** Start a new conversation...

---

### `features\chat\chat_controller.py.start_streaming_response`

- **File:** `features\chat\chat_controller.py`
- **Line:** 326
- **Arguments:** self
- **Returns:** str
- **Docstring:** Start a streaming response and return the message ID...

---

### `features\chat\complexity_analyser\complexity_analyzer.py.__init__`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 35
- **Arguments:** self

---

### `features\chat\complexity_analyser\complexity_analyzer.py._analyze_ambiguity`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 248
- **Arguments:** self, text
- **Returns:** float
- **Docstring:** Analyze the ambiguity level of the request...

---

### `features\chat\complexity_analyser\complexity_analyzer.py._analyze_context_dependency`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 282
- **Arguments:** self, text, conversation_history
- **Returns:** float
- **Docstring:** Analyze how much the request depends on conversation context...

---

### `features\chat\complexity_analyser\complexity_analyzer.py._analyze_knowledge_breadth`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 223
- **Arguments:** self, text
- **Returns:** float
- **Docstring:** Analyze the breadth of knowledge domains required...

---

### `features\chat\complexity_analyser\complexity_analyzer.py._analyze_output_complexity`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 302
- **Arguments:** self, text
- **Returns:** float
- **Docstring:** Analyze the complexity of expected output...

---

### `features\chat\complexity_analyser\complexity_analyzer.py._analyze_reasoning_depth`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 187
- **Arguments:** self, text
- **Returns:** float
- **Docstring:** Analyze the depth of reasoning required...

---

### `features\chat\complexity_analyser\complexity_analyzer.py._count_constraints`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 267
- **Arguments:** self, text
- **Returns:** int
- **Docstring:** Count the number of constraints in the request...

---

### `features\chat\complexity_analyser\complexity_analyzer.py._determine_complexity_level`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 322
- **Arguments:** self, overall_score, factors
- **Returns:** ComplexityLevel
- **Docstring:** Determine the complexity level based on overall score and factors...

---

### `features\chat\complexity_analyser\complexity_analyzer.py._estimate_tokens`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 181
- **Arguments:** self, text
- **Returns:** int
- **Docstring:** Rough token estimation (words + punctuation)...

---

### `features\chat\complexity_analyser\complexity_analyzer.py._generate_recommendations`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 333
- **Arguments:** self, level, factors
- **Docstring:** Generate recommendations based on complexity analysis...

---

### `features\chat\complexity_analyser\complexity_analyzer.py.analyze_complexity`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 115
- **Arguments:** self, request, conversation_history
- **Returns:** ComplexityMetrics
- **Docstring:** Analyze the complexity of a request and return detailed metrics.

Args:
    request: The user's requ...

---

### `features\chat\complexity_analyser\complexity_analyzer.py.extract_size`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 378
- **Arguments:** model_name

---

### `features\chat\complexity_analyser\complexity_analyzer.py.format_complexity_report`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 396
- **Arguments:** self, metrics
- **Returns:** str
- **Docstring:** Format complexity analysis as a readable report...

---

### `features\chat\complexity_analyser\complexity_analyzer.py.get_model_recommendation`

- **File:** `features\chat\complexity_analyser\complexity_analyzer.py`
- **Line:** 375
- **Arguments:** self, complexity_metrics, available_models
- **Returns:** str
- **Docstring:** Get model recommendation based on complexity analysis...

---

### `features\chat\conversation_service.py.__init__`

- **File:** `features\chat\conversation_service.py`
- **Line:** 21
- **Arguments:** self, history_dir, memory_service

---

### `features\chat\conversation_service.py._add_to_memory`

- **File:** `features\chat\conversation_service.py`
- **Line:** 220
- **Arguments:** self, role, content
- **Docstring:** Add message to memory service...

---

### `features\chat\conversation_service.py._get_next_message_id`

- **File:** `features\chat\conversation_service.py`
- **Line:** 42
- **Arguments:** self
- **Returns:** str
- **Docstring:** Generate a unique message ID...

---

### `features\chat\conversation_service.py.add_message`

- **File:** `features\chat\conversation_service.py`
- **Line:** 47
- **Arguments:** self, role, content, message_id
- **Docstring:** Add a message to the conversation...

---

### `features\chat\conversation_service.py.clear_conversation`

- **File:** `features\chat\conversation_service.py`
- **Line:** 366
- **Arguments:** self
- **Docstring:** Clear the current conversation...

---

### `features\chat\conversation_service.py.finalize_streaming_message`

- **File:** `features\chat\conversation_service.py`
- **Line:** 135
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Finalize the current streaming message...

---

### `features\chat\conversation_service.py.get_context_messages`

- **File:** `features\chat\conversation_service.py`
- **Line:** 266
- **Arguments:** self
- **Docstring:** Get messages for context window, including relevant memories...

---

### `features\chat\conversation_service.py.get_message_by_id`

- **File:** `features\chat\conversation_service.py`
- **Line:** 204
- **Arguments:** self, message_id
- **Docstring:** Get a message by its ID...

---

### `features\chat\conversation_service.py.get_messages`

- **File:** `features\chat\conversation_service.py`
- **Line:** 255
- **Arguments:** self
- **Docstring:** Get the current conversation messages...

---

### `features\chat\conversation_service.py.get_streaming_message_id`

- **File:** `features\chat\conversation_service.py`
- **Line:** 193
- **Arguments:** self
- **Docstring:** Get the current streaming message ID...

---

### `features\chat\conversation_service.py.get_streaming_message_with_content`

- **File:** `features\chat\conversation_service.py`
- **Line:** 197
- **Arguments:** self
- **Docstring:** Get the streaming message that has actual content...

---

### `features\chat\conversation_service.py.load_conversation`

- **File:** `features\chat\conversation_service.py`
- **Line:** 273
- **Arguments:** self, filename
- **Docstring:** Load a conversation from a file...

---

### `features\chat\conversation_service.py.set_conversation_manager`

- **File:** `features\chat\conversation_service.py`
- **Line:** 38
- **Arguments:** self, conversation_manager
- **Docstring:** Set the conversation manager for unified saving...

---

### `features\chat\conversation_service.py.set_memory_service`

- **File:** `features\chat\conversation_service.py`
- **Line:** 34
- **Arguments:** self, memory_service
- **Docstring:** Set the memory service for integration...

---

### `features\chat\conversation_service.py.start_streaming_message`

- **File:** `features\chat\conversation_service.py`
- **Line:** 75
- **Arguments:** self, role
- **Returns:** str
- **Docstring:** Start a new streaming message, finalizing any previous one first...

---

### `features\chat\conversation_service.py.update_message_by_id`

- **File:** `features\chat\conversation_service.py`
- **Line:** 211
- **Arguments:** self, message_id, content
- **Returns:** bool
- **Docstring:** Update a message's content by ID...

---

### `features\chat\conversation_service.py.update_streaming_message`

- **File:** `features\chat\conversation_service.py`
- **Line:** 93
- **Arguments:** self, chunk, append, msg_id, chunk_index
- **Returns:** bool
- **Docstring:** Update the streaming message with a new chunk...

---

### `features\chat\enhancers\enhancement_service.py.__init__`

- **File:** `features\chat\enhancers\enhancement_service.py`
- **Line:** 11
- **Arguments:** self, ollama_service

---

### `features\chat\enhancers\enhancement_service.py.detect_follow_up_question`

- **File:** `features\chat\enhancers\enhancement_service.py`
- **Line:** 25
- **Arguments:** self, response
- **Docstring:** Detect a follow-up question in the response (placeholder logic)...

---

### `features\chat\enhancers\enhancement_service.py.generate_enhanced_response`

- **File:** `features\chat\enhancers\enhancement_service.py`
- **Line:** 34
- **Arguments:** self, original_response, context
- **Returns:** str
- **Docstring:** Generate an enhanced response (placeholder logic)...

---

### `features\chat\enhancers\enhancement_service.py.should_enhance_response`

- **File:** `features\chat\enhancers\enhancement_service.py`
- **Line:** 14
- **Arguments:** self, response
- **Returns:** bool
- **Docstring:** Determine if a response should be enhanced (placeholder logic)...

---

### `features\chat\summarization\summarization_service.py.__init__`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 25
- **Arguments:** self, ollama_service

---

### `features\chat\summarization\summarization_service.py._ai_evaluate_conversation_quality`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 235
- **Arguments:** self, user_messages
- **Returns:** bool
- **Docstring:** Use AI to evaluate if a conversation has enough substance for naming

Args:
    user_messages: List ...

---

### `features\chat\summarization\summarization_service.py._ai_evaluate_name_quality`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 340
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Use AI to evaluate if a generated name is suitable

Args:
    name: The generated name to evaluate
 ...

---

### `features\chat\summarization\summarization_service.py._clean_generated_name`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 145
- **Arguments:** self, response
- **Docstring:** Clean and validate the generated name...

---

### `features\chat\summarization\summarization_service.py._create_summarization_prompt`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 120
- **Arguments:** self, user_messages
- **Returns:** str
- **Docstring:** Create a prompt for generating a concise chat name...

---

### `features\chat\summarization\summarization_service.py._fallback_quality_check`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 311
- **Arguments:** self, user_messages
- **Returns:** bool
- **Docstring:** Fallback quality check if AI evaluation fails

Args:
    user_messages: List of user messages
    
R...

---

### `features\chat\summarization\summarization_service.py._has_enough_substance`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 218
- **Arguments:** self, user_messages
- **Returns:** bool
- **Docstring:** Check if the conversation has enough substance for meaningful naming
Uses AI to evaluate conversatio...

---

### `features\chat\summarization\summarization_service.py.generate_chat_name`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 31
- **Arguments:** self, conversation, filepath
- **Docstring:** Generate an AI-powered name for a conversation

Args:
    conversation: List of conversation message...

---

### `features\chat\summarization\summarization_service.py.set_min_messages_threshold`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 416
- **Arguments:** self, threshold
- **Docstring:** Set the minimum number of messages required for summarization...

---

### `features\chat\summarization\summarization_service.py.set_summarization_model`

- **File:** `features\chat\summarization\summarization_service.py`
- **Line:** 412
- **Arguments:** self, model
- **Docstring:** Set the model to use for summarization...

---

### `features\memory\memory_service.py.__init__`

- **File:** `features\memory\memory_service.py`
- **Line:** 449
- **Arguments:** self, max_context_messages

---

### `features\memory\memory_service.py.__post_init__`

- **File:** `features\memory\memory_service.py`
- **Line:** 51
- **Arguments:** self

---

### `features\memory\memory_service.py._load`

- **File:** `features\memory\memory_service.py`
- **Line:** 389
- **Arguments:** self
- **Docstring:** Load long-term memory from file...

---

### `features\memory\memory_service.py._load_memory`

- **File:** `features\memory\memory_service.py`
- **Line:** 478
- **Arguments:** self
- **Docstring:** Load memory from storage...

---

### `features\memory\memory_service.py._on_embeddings_updated`

- **File:** `features\memory\memory_service.py`
- **Line:** 494
- **Arguments:** self
- **Docstring:** Handle embeddings update...

---

### `features\memory\memory_service.py._save`

- **File:** `features\memory\memory_service.py`
- **Line:** 424
- **Arguments:** self
- **Docstring:** Save long-term memory to file...

---

### `features\memory\memory_service.py._save_memory`

- **File:** `features\memory\memory_service.py`
- **Line:** 486
- **Arguments:** self
- **Docstring:** Save memory to storage...

---

### `features\memory\memory_service.py._verify_memory_files_cleared`

- **File:** `features\memory\memory_service.py`
- **Line:** 801
- **Arguments:** self
- **Docstring:** Verify that memory files have been cleared...

---

### `features\memory\memory_service.py.add_entry`

- **File:** `features\memory\memory_service.py`
- **Line:** 404
- **Arguments:** self, entry
- **Docstring:** Add an entry to long-term memory...

---

### `features\memory\memory_service.py.add_fact`

- **File:** `features\memory\memory_service.py`
- **Line:** 892
- **Arguments:** self, key, value, importance, tags
- **Docstring:** Add a fact to long-term memory...

---

### `features\memory\memory_service.py.add_memory`

- **File:** `features\memory\memory_service.py`
- **Line:** 502
- **Arguments:** self, content, conversation_id, importance, tags, memory_type, metadata
- **Returns:** str
- **Docstring:** Add a memory entry...

---

### `features\memory\memory_service.py.add_message`

- **File:** `features\memory\memory_service.py`
- **Line:** 885
- **Arguments:** self, message
- **Docstring:** Add a message to memory (legacy method)...

---

### `features\memory\memory_service.py.add_summary`

- **File:** `features\memory\memory_service.py`
- **Line:** 547
- **Arguments:** self, summary, importance, tags
- **Docstring:** Add a conversation summary to memory...

---

### `features\memory\memory_service.py.calculate_relevance`

- **File:** `features\memory\memory_service.py`
- **Line:** 258
- **Arguments:** query, memory_entry
- **Returns:** float
- **Decorators:** staticmethod
- **Docstring:** Calculate relevance score between query and memory entry...

---

### `features\memory\memory_service.py.classify_message`

- **File:** `features\memory\memory_service.py`
- **Line:** 96
- **Arguments:** message, role
- **Returns:** Dict
- **Decorators:** staticmethod
- **Docstring:** Classify a message and determine its memory characteristics...

---

### `features\memory\memory_service.py.cleanup_memory_entries`

- **File:** `features\memory\memory_service.py`
- **Line:** 954
- **Arguments:** self
- **Docstring:** Clean up old or low-importance memory entries...

---

### `features\memory\memory_service.py.clear`

- **File:** `features\memory\memory_service.py`
- **Line:** 947
- **Arguments:** self
- **Docstring:** Clear all memory...

---

### `features\memory\memory_service.py.clear_memory`

- **File:** `features\memory\memory_service.py`
- **Line:** 776
- **Arguments:** self, memory_type
- **Docstring:** Clear memory entries...

---

### `features\memory\memory_service.py.delete_memory`

- **File:** `features\memory\memory_service.py`
- **Line:** 820
- **Arguments:** self, memory_id
- **Docstring:** Delete a specific memory entry...

---

### `features\memory\memory_service.py.extract_facts_from_message`

- **File:** `features\memory\memory_service.py`
- **Line:** 679
- **Arguments:** self, message
- **Docstring:** Extract facts from a message using LLM...

---

### `features\memory\memory_service.py.get_context_messages`

- **File:** `features\memory\memory_service.py`
- **Line:** 732
- **Arguments:** self, current_query
- **Docstring:** Get context messages for AI conversation...

---

### `features\memory\memory_service.py.get_entries`

- **File:** `features\memory\memory_service.py`
- **Line:** 414
- **Arguments:** self, type_filter
- **Docstring:** Get entries from long-term memory, optionally filtered by type...

---

### `features\memory\memory_service.py.get_memory_stats`

- **File:** `features\memory\memory_service.py`
- **Line:** 831
- **Arguments:** self
- **Returns:** Dict
- **Docstring:** Get memory statistics...

---

### `features\memory\memory_service.py.get_messages`

- **File:** `features\memory\memory_service.py`
- **Line:** 359
- **Arguments:** self
- **Docstring:** Get all messages in short-term memory...

---

### `features\memory\memory_service.py.get_relevant_memories`

- **File:** `features\memory\memory_service.py`
- **Line:** 565
- **Arguments:** self, query, limit, use_semantic
- **Docstring:** Get relevant memories for a query...

---

### `features\memory\memory_service.py.get_user_info`

- **File:** `features\memory\memory_service.py`
- **Line:** 708
- **Arguments:** self
- **Docstring:** Get user information from memory...

---

### `features\memory\memory_service.py.get_user_name`

- **File:** `features\memory\memory_service.py`
- **Line:** 723
- **Arguments:** self
- **Docstring:** Get the user's name from memory...

---

### `features\memory\memory_service.py.intelligent_add_message`

- **File:** `features\memory\memory_service.py`
- **Line:** 618
- **Arguments:** self, message
- **Returns:** Dict
- **Docstring:** Intelligently add a message to memory with classification...

---

### `features\memory\memory_service.py.normalize_pronouns`

- **File:** `features\memory\memory_service.py`
- **Line:** 195
- **Arguments:** text, user_name
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Convert first-person pronouns to third-person references to avoid AI confusion

Args:
    text: The ...

---

### `features\memory\memory_service.py.search_memories`

- **File:** `features\memory\memory_service.py`
- **Line:** 918
- **Arguments:** self, query, memory_type
- **Docstring:** Search memories with optional type filter...

---

### `features\memory\memory_service.py.set_max_context_messages`

- **File:** `features\memory\memory_service.py`
- **Line:** 909
- **Arguments:** self, max_messages
- **Docstring:** Set the maximum number of context messages...

---

### `features\memory\memory_service.py.should_normalize`

- **File:** `features\memory\memory_service.py`
- **Line:** 230
- **Arguments:** text
- **Returns:** bool
- **Decorators:** staticmethod
- **Docstring:** Check if text contains first-person pronouns that should be normalized...

---

### `features\memory\memory_service.py.summarize_conversation`

- **File:** `features\memory\memory_service.py`
- **Line:** 759
- **Arguments:** self, conversation_messages, conversation_id
- **Returns:** str
- **Docstring:** Summarize a conversation...

---

### `features\memory\memory_service.py.update_access_stats`

- **File:** `features\memory\memory_service.py`
- **Line:** 434
- **Arguments:** self, entry
- **Docstring:** Update access statistics for a memory entry...

---

### `features\memory\semantic_search.py.__init__`

- **File:** `features\memory\semantic_search.py`
- **Line:** 46
- **Arguments:** self, model_name, cache_dir

---

### `features\memory\semantic_search.py._init_model`

- **File:** `features\memory\semantic_search.py`
- **Line:** 64
- **Arguments:** self
- **Docstring:** Initialize the sentence transformer model...

---

### `features\memory\semantic_search.py._load_embeddings`

- **File:** `features\memory\semantic_search.py`
- **Line:** 82
- **Arguments:** self
- **Docstring:** Load existing embeddings from cache...

---

### `features\memory\semantic_search.py._save_embeddings`

- **File:** `features\memory\semantic_search.py`
- **Line:** 116
- **Arguments:** self
- **Docstring:** Save embeddings to cache...

---

### `features\memory\semantic_search.py.add_memory`

- **File:** `features\memory\semantic_search.py`
- **Line:** 150
- **Arguments:** self, memory_id, content, memory_type, importance, tags, metadata
- **Returns:** bool
- **Docstring:** Add a new memory with vector embedding...

---

### `features\memory\semantic_search.py.clear_all`

- **File:** `features\memory\semantic_search.py`
- **Line:** 439
- **Arguments:** self
- **Docstring:** Clear all memories and embeddings...

---

### `features\memory\semantic_search.py.get_memory_stats`

- **File:** `features\memory\semantic_search.py`
- **Line:** 392
- **Arguments:** self
- **Returns:** Dict
- **Docstring:** Get statistics about the semantic search service...

---

### `features\memory\semantic_search.py.is_ready`

- **File:** `features\memory\semantic_search.py`
- **Line:** 466
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if the semantic search service is ready...

---

### `features\memory\semantic_search.py.remove_memory`

- **File:** `features\memory\semantic_search.py`
- **Line:** 204
- **Arguments:** self, memory_id
- **Returns:** bool
- **Docstring:** Remove a memory and its embedding...

---

### `features\memory\semantic_search.py.search_hybrid`

- **File:** `features\memory\semantic_search.py`
- **Line:** 286
- **Arguments:** self, query, max_results, min_similarity, memory_types, keyword_weight, semantic_weight
- **Docstring:** Search memories using both semantic and keyword matching...

---

### `features\memory\semantic_search.py.search_semantic`

- **File:** `features\memory\semantic_search.py`
- **Line:** 233
- **Arguments:** self, query, max_results, min_similarity, memory_types
- **Docstring:** Search memories using semantic similarity...

---

### `features\memory\semantic_search.py.update_memory_importance`

- **File:** `features\memory\semantic_search.py`
- **Line:** 365
- **Arguments:** self, memory_id, new_importance
- **Returns:** bool
- **Docstring:** Update the importance of a memory...

---

### `features\memory\semantic_search_fallback.py.__init__`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 34
- **Arguments:** self, cache_dir

---

### `features\memory\semantic_search_fallback.py._calculate_keyword_similarity`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 177
- **Arguments:** self, query, content
- **Returns:** float
- **Docstring:** Calculate similarity based on keyword matching...

---

### `features\memory\semantic_search_fallback.py._load_memories`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 49
- **Arguments:** self
- **Docstring:** Load existing memories from cache...

---

### `features\memory\semantic_search_fallback.py._save_memories`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 77
- **Arguments:** self
- **Docstring:** Save memories to cache...

---

### `features\memory\semantic_search_fallback.py.add_memory`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 105
- **Arguments:** self, memory_id, content, memory_type, importance, tags, metadata
- **Returns:** bool
- **Docstring:** Add a new memory with simple storage...

---

### `features\memory\semantic_search_fallback.py.clear_all`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 343
- **Arguments:** self
- **Docstring:** Clear all memories...

---

### `features\memory\semantic_search_fallback.py.get_memory_stats`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 295
- **Arguments:** self
- **Returns:** Dict
- **Docstring:** Get statistics about the memory service...

---

### `features\memory\semantic_search_fallback.py.is_ready`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 367
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if the memory service is ready...

---

### `features\memory\semantic_search_fallback.py.remove_memory`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 149
- **Arguments:** self, memory_id
- **Returns:** bool
- **Docstring:** Remove a memory...

---

### `features\memory\semantic_search_fallback.py.search_hybrid`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 263
- **Arguments:** self, query, max_results, min_similarity, memory_types, keyword_weight, semantic_weight
- **Docstring:** Search memories using keyword matching (semantic weight ignored in fallback)...

---

### `features\memory\semantic_search_fallback.py.search_semantic`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 215
- **Arguments:** self, query, max_results, min_similarity, memory_types
- **Docstring:** Search memories using keyword similarity...

---

### `features\memory\semantic_search_fallback.py.update_memory_importance`

- **File:** `features\memory\semantic_search_fallback.py`
- **Line:** 269
- **Arguments:** self, memory_id, new_importance
- **Returns:** bool
- **Docstring:** Update the importance of a memory...

---

### `features\ollama\ollama_chat.py.__init__`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 23
- **Arguments:** self

---

### `features\ollama\ollama_chat.py._setup_ui`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 79
- **Arguments:** self
- **Docstring:** Setup the UI components...

---

### `features\ollama\ollama_chat.py.check_ollama_connection`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 120
- **Arguments:** self
- **Docstring:** Check if Ollama is running and accessible...

---

### `features\ollama\ollama_chat.py.closeEvent`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 112
- **Arguments:** self, event
- **Docstring:** Handle application close event...

---

### `features\ollama\ollama_chat.py.get_chat_controller`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 141
- **Arguments:** self
- **Docstring:** Get the chat controller...

---

### `features\ollama\ollama_chat.py.get_event_handler`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 133
- **Arguments:** self
- **Docstring:** Get the Event Bus...

---

### `features\ollama\ollama_chat.py.get_lifecycle_manager`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 137
- **Arguments:** self
- **Docstring:** Get the lifecycle manager...

---

### `features\ollama\ollama_chat.py.get_service_manager`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 125
- **Arguments:** self
- **Docstring:** Get the service manager...

---

### `features\ollama\ollama_chat.py.get_ui_manager`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 129
- **Arguments:** self
- **Docstring:** Get the UI manager...

---

### `features\ollama\ollama_chat.py.showEvent`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 107
- **Arguments:** self, event
- **Docstring:** Handle application show event...

---

### `features\ollama\ollama_chat.py.show_ollama_connection_error`

- **File:** `features\ollama\ollama_chat.py`
- **Line:** 116
- **Arguments:** self, context, force_show
- **Docstring:** Show Ollama connection error dialog...

---

### `features\ollama\ollama_service.py.__init__`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 35
- **Arguments:** self, base_url

---

### `features\ollama\ollama_service.py._build_session_commands`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 652
- **Arguments:** self, session_variables
- **Docstring:** Build session commands from variables...

---

### `features\ollama\ollama_service.py._extract_system_prompt`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 643
- **Arguments:** self, messages
- **Returns:** str
- **Docstring:** Extract system prompt from messages...

---

### `features\ollama\ollama_service.py._get_models_with_library`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 73
- **Arguments:** self
- **Docstring:** Get models using the official Ollama library...

---

### `features\ollama\ollama_service.py._get_models_with_requests`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 133
- **Arguments:** self
- **Docstring:** Get models using requests (fallback method)...

---

### `features\ollama\ollama_service.py._pull_model_thread`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 440
- **Arguments:** self, model_name
- **Docstring:** Background thread for pulling models...

---

### `features\ollama\ollama_service.py._remove_model_thread`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 517
- **Arguments:** self, model_name
- **Docstring:** Background thread for removing models...

---

### `features\ollama\ollama_service.py._send_chat_message_with_library`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 233
- **Arguments:** self, model, messages, temperature, stream, session_variables
- **Docstring:** Send chat message using the official Ollama library...

---

### `features\ollama\ollama_service.py._send_chat_message_with_requests`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 314
- **Arguments:** self, model, messages, temperature, stream, session_variables
- **Docstring:** Send chat message using requests (fallback method)...

---

### `features\ollama\ollama_service.py._update_model_thread`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 594
- **Arguments:** self, model_name
- **Docstring:** Background thread for updating models...

---

### `features\ollama\ollama_service.py.cancel_request`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 668
- **Arguments:** self
- **Docstring:** Cancel any ongoing request...

---

### `features\ollama\ollama_service.py.cleanup`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 683
- **Arguments:** self
- **Docstring:** Clean up resources and stop all active operations...

---

### `features\ollama\ollama_service.py.get_models`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 66
- **Arguments:** self
- **Docstring:** Get list of available models from Ollama using the best available method...

---

### `features\ollama\ollama_service.py.is_connected`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 679
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Ollama is running and accessible...

---

### `features\ollama\ollama_service.py.pull_model`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 412
- **Arguments:** self, model_name
- **Docstring:** Pull a model from Ollama using the best available method...

---

### `features\ollama\ollama_service.py.remove_model`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 489
- **Arguments:** self, model_name
- **Docstring:** Remove a model from Ollama using the best available method...

---

### `features\ollama\ollama_service.py.reset_cancellation`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 674
- **Arguments:** self
- **Docstring:** Reset cancellation flag...

---

### `features\ollama\ollama_service.py.send_chat_message`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 211
- **Arguments:** self, model, messages, temperature, stream, session_variables
- **Docstring:** Send a chat message to Ollama and yield streaming responses.
Uses the official library if available,...

---

### `features\ollama\ollama_service.py.test_connection`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 182
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Test if Ollama is running and accessible without emitting signals...

---

### `features\ollama\ollama_service.py.update_model`

- **File:** `features\ollama\ollama_service.py`
- **Line:** 566
- **Arguments:** self, model_name
- **Docstring:** Update a model from Ollama using the best available method...

---

### `features\personality\formatter.py.build_comprehensive_system_prompt`

- **File:** `features\personality\formatter.py`
- **Line:** 53
- **Arguments:** personality_data
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Build a comprehensive system prompt with pronoun guidance...

---

### `features\personality\formatter.py.create_personality_template`

- **File:** `features\personality\formatter.py`
- **Line:** 244
- **Arguments:** name, description
- **Decorators:** staticmethod
- **Docstring:** Create a template personality data structure...

---

### `features\personality\formatter.py.format_personality_summary`

- **File:** `features\personality\formatter.py`
- **Line:** 204
- **Arguments:** personality_data
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format a brief summary of a personality...

---

### `features\personality\formatter.py.format_prompt_with_personality`

- **File:** `features\personality\formatter.py`
- **Line:** 17
- **Arguments:** personality_data, user_input, context
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format a prompt using the personality's prompt templates...

---

### `features\personality\formatter.py.get_personality_info`

- **File:** `features\personality\formatter.py`
- **Line:** 147
- **Arguments:** personality_data
- **Decorators:** staticmethod
- **Docstring:** Get detailed information about a personality...

---

### `features\personality\formatter.py.get_system_prompt`

- **File:** `features\personality\formatter.py`
- **Line:** 140
- **Arguments:** personality_data
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Get the system prompt for a personality...

---

### `features\personality\formatter.py.validate_personality_data`

- **File:** `features\personality\formatter.py`
- **Line:** 173
- **Arguments:** personality_data
- **Decorators:** staticmethod
- **Docstring:** Validate personality data and return list of errors...

---

### `features\personality\loader.py.__init__`

- **File:** `features\personality\loader.py`
- **Line:** 24
- **Arguments:** self, personalities_dir

---

### `features\personality\loader.py.backup_personality`

- **File:** `features\personality\loader.py`
- **Line:** 182
- **Arguments:** self, name, backup_dir
- **Returns:** bool
- **Docstring:** Create a backup of a personality file...

---

### `features\personality\loader.py.create_personality_data`

- **File:** `features\personality\loader.py`
- **Line:** 145
- **Arguments:** self, traits, prompt, config, metadata
- **Docstring:** Create personality data dictionary from component objects...

---

### `features\personality\loader.py.delete_personality_file`

- **File:** `features\personality\loader.py`
- **Line:** 133
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Delete a personality file...

---

### `features\personality\loader.py.extract_personality_name`

- **File:** `features\personality\loader.py`
- **Line:** 54
- **Arguments:** self, filepath
- **Returns:** str
- **Docstring:** Extract personality name from file path, preserving folder structure for uniqueness...

---

### `features\personality\loader.py.find_personality_file_by_name`

- **File:** `features\personality\loader.py`
- **Line:** 118
- **Arguments:** self, personality_name
- **Docstring:** Find the actual file path for a personality by its name...

---

### `features\personality\loader.py.find_personality_files`

- **File:** `features\personality\loader.py`
- **Line:** 36
- **Arguments:** self, directory
- **Docstring:** Recursively find all personality JSON files in the given directory and subdirectories...

---

### `features\personality\loader.py.get_personality_file_info`

- **File:** `features\personality\loader.py`
- **Line:** 241
- **Arguments:** self, filepath
- **Docstring:** Get information about a personality file...

---

### `features\personality\loader.py.list_backup_files`

- **File:** `features\personality\loader.py`
- **Line:** 261
- **Arguments:** self, backup_dir
- **Docstring:** List all backup files...

---

### `features\personality\loader.py.load_all_personalities`

- **File:** `features\personality\loader.py`
- **Line:** 79
- **Arguments:** self
- **Docstring:** Load all personalities from JSON files recursively...

---

### `features\personality\loader.py.load_personality_from_file`

- **File:** `features\personality\loader.py`
- **Line:** 69
- **Arguments:** self, filepath
- **Docstring:** Load a single personality from a JSON file...

---

### `features\personality\loader.py.restore_personality_from_backup`

- **File:** `features\personality\loader.py`
- **Line:** 210
- **Arguments:** self, backup_filepath
- **Returns:** bool
- **Docstring:** Restore a personality from a backup file...

---

### `features\personality\loader.py.save_personality_to_file`

- **File:** `features\personality\loader.py`
- **Line:** 91
- **Arguments:** self, name, personality_data
- **Returns:** bool
- **Docstring:** Save a personality to a JSON file...

---

### `features\personality\loader.py.validate_personality_file`

- **File:** `features\personality\loader.py`
- **Line:** 163
- **Arguments:** self, filepath
- **Docstring:** Validate a personality file and return list of errors...

---

### `features\personality\models\personality_model.py.__init__`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 23
- **Arguments:** self, personalities_dir

---

### `features\personality\models\personality_model.py._extract_personality_name`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 53
- **Arguments:** self, filepath
- **Returns:** str
- **Docstring:** Extract personality name - now handled by loader...

---

### `features\personality\models\personality_model.py._find_personality_file_by_name`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 62
- **Arguments:** self, personality_name
- **Docstring:** Find personality file by name - now handled by loader...

---

### `features\personality\models\personality_model.py._find_personality_files`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 49
- **Arguments:** self, directory
- **Docstring:** Find personality files - now handled by loader...

---

### `features\personality\models\personality_model.py._initialize_default_personalities`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 42
- **Arguments:** self
- **Docstring:** Initialize the default personality set - now handled by service...

---

### `features\personality\models\personality_model.py._load_custom_personalities`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 57
- **Arguments:** self
- **Docstring:** Load custom personalities - now handled by service...

---

### `features\personality\models\personality_model.py.get_custom_personalities`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 84
- **Arguments:** self
- **Docstring:** Return a list of custom personality names (for UI compatibility)...

---

### `features\personality\models\personality_model.py.get_personality_formatter`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 76
- **Arguments:** self
- **Docstring:** Get access to the personality formatter for advanced operations...

---

### `features\personality\models\personality_model.py.get_personality_loader`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 72
- **Arguments:** self
- **Docstring:** Get access to the personality loader for advanced operations...

---

### `features\personality\models\personality_model.py.get_system_personalities`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 80
- **Arguments:** self
- **Docstring:** Return a list of system personality names (for UI compatibility)...

---

### `features\personality\models\personality_model.py.save_custom_personality`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 66
- **Arguments:** self, name, personality_data
- **Returns:** bool
- **Docstring:** Save a custom personality - for backward compatibility...

---

### `features\personality\models\personality_model.py.service`

- **File:** `features\personality\models\personality_model.py`
- **Line:** 38
- **Arguments:** self
- **Decorators:** property
- **Docstring:** Backward compatibility: return self as the service...

---

### `features\personality\models\personality_pronouns.py.format_user_reference`

- **File:** `features\personality\models\personality_pronouns.py`
- **Line:** 134
- **Arguments:** self, template
- **Returns:** str
- **Docstring:** Format a template with appropriate user references...

---

### `features\personality\models\personality_pronouns.py.get_formal_title`

- **File:** `features\personality\models\personality_pronouns.py`
- **Line:** 63
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the most formal title from the list...

---

### `features\personality\models\personality_pronouns.py.get_primary_title`

- **File:** `features\personality\models\personality_pronouns.py`
- **Line:** 53
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the primary (first) user title...

---

### `features\personality\models\personality_pronouns.py.get_pronoun_guide`

- **File:** `features\personality\models\personality_pronouns.py`
- **Line:** 80
- **Arguments:** self
- **Returns:** str
- **Docstring:** Generate a comprehensive pronoun guide for the AI...

---

### `features\personality\models\personality_pronouns.py.get_random_title`

- **File:** `features\personality\models\personality_pronouns.py`
- **Line:** 58
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get a random user title for variety...

---

### `features\personality\models\personality_pronouns.py.get_user_address`

- **File:** `features\personality\models\personality_pronouns.py`
- **Line:** 123
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the appropriate way to address the user...

---

### `features\personality\models\personality_pronouns.py.get_user_titles`

- **File:** `features\personality\models\personality_pronouns.py`
- **Line:** 37
- **Arguments:** self
- **Docstring:** Get user titles as a list, handling both string and list formats...

---

### `features\personality\models\personality_types.py.__post_init__`

- **File:** `features\personality\models\personality_types.py`
- **Line:** 66
- **Arguments:** self

---

### `features\personality\services\personality_service.py.__init__`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 25
- **Arguments:** self, personalities_dir

---

### `features\personality\services\personality_service.py._initialize_personalities`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 38
- **Arguments:** self
- **Docstring:** Initialize personalities by loading from files...

---

### `features\personality\services\personality_service.py.build_comprehensive_system_prompt`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 295
- **Arguments:** self, memory_service
- **Returns:** str
- **Docstring:** Build a comprehensive system prompt with pronoun guidance...

---

### `features\personality\services\personality_service.py.create_custom_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 113
- **Arguments:** self, name, traits, prompt, config, metadata
- **Returns:** bool
- **Docstring:** Create a new custom personality in the Custom folder...

---

### `features\personality\services\personality_service.py.delete_custom_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 142
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Delete a custom personality (only if it's in the Custom folder)...

---

### `features\personality\services\personality_service.py.format_prompt_with_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 219
- **Arguments:** self, user_input, context
- **Returns:** str
- **Docstring:** Format a prompt using the current personality's prompt templates...

---

### `features\personality\services\personality_service.py.get_ai_name`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 441
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the AI's name from the current personality...

---

### `features\personality\services\personality_service.py.get_available_personalities`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 92
- **Arguments:** self
- **Docstring:** Get list of all available personality names...

---

### `features\personality\services\personality_service.py.get_current_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 107
- **Arguments:** self
- **Docstring:** Get the current active personality...

---

### `features\personality\services\personality_service.py.get_custom_personalities`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 84
- **Arguments:** self
- **Docstring:** Get custom personalities (editable/deletable)...

---

### `features\personality\services\personality_service.py.get_personalities_by_category`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 385
- **Arguments:** self, category
- **Docstring:** Get personalities by category...

---

### `features\personality\services\personality_service.py.get_personalities_by_folder`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 398
- **Arguments:** self, folder_name
- **Docstring:** Get personalities by folder name...

---

### `features\personality\services\personality_service.py.get_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 96
- **Arguments:** self, name
- **Docstring:** Get personality by name...

---

### `features\personality\services\personality_service.py.get_personality_categories`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 374
- **Arguments:** self
- **Docstring:** Get list of all personality categories...

---

### `features\personality\services\personality_service.py.get_personality_config`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 260
- **Arguments:** self, name
- **Docstring:** Get configuration for a personality...

---

### `features\personality\services\personality_service.py.get_personality_info`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 255
- **Arguments:** self, name
- **Docstring:** Get detailed information about a personality...

---

### `features\personality\services\personality_service.py.get_selected_model`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 437
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality name...

---

### `features\personality\services\personality_service.py.get_system_personalities`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 76
- **Arguments:** self
- **Docstring:** Get system personalities (read-only)...

---

### `features\personality\services\personality_service.py.get_system_prompt`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 238
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the system prompt for the current personality...

---

### `features\personality\services\personality_service.py.get_temperature`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 448
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get the temperature for the current personality, or default to 0.7...

---

### `features\personality\services\personality_service.py.get_user_context_messages`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 306
- **Arguments:** self, memory_service, is_new_conversation
- **Docstring:** Get dynamic user context messages that should be added to conversation...

---

### `features\personality\services\personality_service.py.is_custom_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 72
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Check if a personality is a custom personality (editable/deletable)...

---

### `features\personality\services\personality_service.py.is_system_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 63
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Check if a personality is a system personality (read-only)...

---

### `features\personality\services\personality_service.py.refresh_personalities`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 198
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Refresh personalities from disk, reloading all JSON files...

---

### `features\personality\services\personality_service.py.search_personalities`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 408
- **Arguments:** self, query
- **Docstring:** Search personalities by name, description, or tags...

---

### `features\personality\services\personality_service.py.set_current_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 100
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Set the current active personality...

---

### `features\personality\services\personality_service.py.update_custom_personality`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 173
- **Arguments:** self, name, traits, prompt, config, metadata
- **Returns:** bool
- **Docstring:** Update a custom personality (only if it's in the Custom folder)...

---

### `features\personality\services\personality_service.py.update_personality_metadata`

- **File:** `features\personality\services\personality_service.py`
- **Line:** 271
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Update metadata for a personality...

---

### `features\user\user_profile_service.py.__init__`

- **File:** `features\user\user_profile_service.py`
- **Line:** 10
- **Arguments:** self

---

### `features\user\user_profile_service.py.get_user_profile`

- **File:** `features\user\user_profile_service.py`
- **Line:** 13
- **Arguments:** self, user_id
- **Docstring:** Get user profile by ID....

---

### `features\user\user_profile_service.py.update_user_profile`

- **File:** `features\user\user_profile_service.py`
- **Line:** 17
- **Arguments:** self, user_id, profile_data
- **Returns:** bool
- **Docstring:** Update user profile....

---

### `features\voice\audio\recording_service.py.__del__`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 52
- **Arguments:** self

---

### `features\voice\audio\recording_service.py.__init__`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 23
- **Arguments:** self

---

### `features\voice\audio\recording_service.py._calculate_audio_level`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 219
- **Arguments:** self, audio_data
- **Returns:** float

---

### `features\voice\audio\recording_service.py._check_availability`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 58
- **Arguments:** self
- **Returns:** bool

---

### `features\voice\audio\recording_service.py._record_audio`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 100
- **Arguments:** self

---

### `features\voice\audio\recording_service.py.audio_level_to_db`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 233
- **Arguments:** self, audio_level
- **Returns:** float

---

### `features\voice\audio\recording_service.py.calculate_eq_bars_pcm`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 125
- **Arguments:** audio_bytes, num_bars, sample_rate

---

### `features\voice\audio\recording_service.py.cleanup`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 273
- **Arguments:** self

---

### `features\voice\audio\recording_service.py.get_current_audio_level`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 244
- **Arguments:** self
- **Returns:** float

---

### `features\voice\audio\recording_service.py.get_speech_detection_parameters`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 264
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get current speech detection parameters...

---

### `features\voice\audio\recording_service.py.is_available`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 73
- **Arguments:** self
- **Returns:** bool

---

### `features\voice\audio\recording_service.py.is_initialized`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 76
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Recording service is properly initialized...

---

### `features\voice\audio\recording_service.py.set_audio_gate_enabled`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 247
- **Arguments:** self, enabled

---

### `features\voice\audio\recording_service.py.set_speech_detection_parameters`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 254
- **Arguments:** self, silence_duration, silence_threshold, min_speech_duration
- **Docstring:** Configure speech detection parameters for better user experience...

---

### `features\voice\audio\recording_service.py.start_recording`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 80
- **Arguments:** self

---

### `features\voice\audio\recording_service.py.stop_recording`

- **File:** `features\voice\audio\recording_service.py`
- **Line:** 282
- **Arguments:** self

---

### `features\voice\orchestrator\voice_process_manager.py.__init__`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 279
- **Arguments:** self, response_queue, parent

---

### `features\voice\orchestrator\voice_process_manager.py._handle_monitor_error`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 242
- **Arguments:** self, error_message
- **Docstring:** Handle monitor thread error...

---

### `features\voice\orchestrator\voice_process_manager.py._handle_response`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 202
- **Arguments:** self, response
- **Docstring:** Handle response from the voice process...

---

### `features\voice\orchestrator\voice_process_manager.py._voice_process_worker`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 350
- **Arguments:** command_queue, response_queue
- **Docstring:** Worker function that runs in the separate voice process...

---

### `features\voice\orchestrator\voice_process_manager.py.create_voice_process_manager`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 450
- **Arguments:** 
- **Returns:** VoiceProcessManager
- **Docstring:** Create and start a voice process manager...

---

### `features\voice\orchestrator\voice_process_manager.py.get_process_info`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 256
- **Arguments:** self
- **Docstring:** Get information about the voice process...

---

### `features\voice\orchestrator\voice_process_manager.py.get_stats`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 340
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get monitor statistics for debugging...

---

### `features\voice\orchestrator\voice_process_manager.py.is_process_running`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 250
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if the voice process is running...

---

### `features\voice\orchestrator\voice_process_manager.py.run`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 290
- **Arguments:** self
- **Docstring:** Monitor the response queue...

---

### `features\voice\orchestrator\voice_process_manager.py.send_command`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 185
- **Arguments:** self, command, data
- **Docstring:** Send a command to the voice process...

---

### `features\voice\orchestrator\voice_process_manager.py.start_voice_process`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 48
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Start the voice process and monitoring thread...

---

### `features\voice\orchestrator\voice_process_manager.py.stop`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 325
- **Arguments:** self
- **Docstring:** Stop the monitoring thread safely...

---

### `features\voice\orchestrator\voice_process_manager.py.stop_voice_process`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 105
- **Arguments:** self
- **Docstring:** Stop the voice process and monitoring thread safely...

---

### `features\voice\orchestrator\voice_process_manager.py.stop_voice_process_manager`

- **File:** `features\voice\orchestrator\voice_process_manager.py`
- **Line:** 467
- **Arguments:** manager
- **Docstring:** Stop a voice process manager...

---

### `features\voice\stt\stt_service.py.__init__`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 16
- **Arguments:** self

---

### `features\voice\stt\stt_service.py._check_availability`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 22
- **Arguments:** self
- **Returns:** bool

---

### `features\voice\stt\stt_service.py._convert_with_vosk`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 58
- **Arguments:** self, audio_file

---

### `features\voice\stt\stt_service.py.convert_audio_to_text`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 51
- **Arguments:** self, audio_file

---

### `features\voice\stt\stt_service.py.is_available`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 44
- **Arguments:** self
- **Returns:** bool

---

### `features\voice\stt\stt_service.py.is_initialized`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 47
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if STT service is properly initialized...

---

### `features\voice\stt\stt_service.py.process_audio_file`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 95
- **Arguments:** self, audio_file_path

---

### `features\voice\stt\stt_service.py.update_api`

- **File:** `features\voice\stt\stt_service.py`
- **Line:** 91
- **Arguments:** self, api_name

---

### `features\voice\tts\streaming_audio_player.py.__del__`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 41
- **Arguments:** self
- **Docstring:** Destructor to ensure cleanup...

---

### `features\voice\tts\streaming_audio_player.py.__init__`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 23
- **Arguments:** self, sample_rate, channels, chunk_size

---

### `features\voice\tts\streaming_audio_player.py._process_audio_chunk`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 155
- **Arguments:** self, audio_chunk
- **Returns:** np.ndarray
- **Docstring:** Process audio chunk with comprehensive error handling...

---

### `features\voice\tts\streaming_audio_player.py.add_audio_chunk`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 282
- **Arguments:** self, audio_chunk
- **Docstring:** Add audio chunk to queue with error handling...

---

### `features\voice\tts\streaming_audio_player.py.calculate_eq_bars`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 192
- **Arguments:** chunk, num_bars, sample_rate

---

### `features\voice\tts\streaming_audio_player.py.cleanup`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 329
- **Arguments:** self
- **Docstring:** Comprehensive cleanup with error handling...

---

### `features\voice\tts\streaming_audio_player.py.end_stream`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 293
- **Arguments:** self
- **Docstring:** End audio stream with error handling...

---

### `features\voice\tts\streaming_audio_player.py.run`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 47
- **Arguments:** self
- **Docstring:** Main playback loop with comprehensive error handling...

---

### `features\voice\tts\streaming_audio_player.py.set_volume`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 278
- **Arguments:** self, volume

---

### `features\voice\tts\streaming_audio_player.py.stop_playback`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 301
- **Arguments:** self
- **Docstring:** Stop audio playback with comprehensive error handling...

---

### `features\voice\tts\streaming_audio_player.py.terminate_pyaudio`

- **File:** `features\voice\tts\streaming_audio_player.py`
- **Line:** 353
- **Arguments:** 

---

### `features\voice\tts\streaming_audio_worker.py.__init__`

- **File:** `features\voice\tts\streaming_audio_worker.py`
- **Line:** 20
- **Arguments:** self, text, tts_service

---

### `features\voice\tts\streaming_audio_worker.py._adjust_audio_speed`

- **File:** `features\voice\tts\streaming_audio_worker.py`
- **Line:** 127
- **Arguments:** self, audio
- **Returns:** np.ndarray

---

### `features\voice\tts\streaming_audio_worker.py._generate_audio_chunk`

- **File:** `features\voice\tts\streaming_audio_worker.py`
- **Line:** 84
- **Arguments:** self, text

---

### `features\voice\tts\streaming_audio_worker.py._split_text_into_sentences`

- **File:** `features\voice\tts\streaming_audio_worker.py`
- **Line:** 65
- **Arguments:** self, text

---

### `features\voice\tts\streaming_audio_worker.py.run`

- **File:** `features\voice\tts\streaming_audio_worker.py`
- **Line:** 27
- **Arguments:** self

---

### `features\voice\tts\streaming_audio_worker.py.stop`

- **File:** `features\voice\tts\streaming_audio_worker.py`
- **Line:** 146
- **Arguments:** self

---

### `features\voice\tts\tts_service.py.__init__`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 40
- **Arguments:** self

---

### `features\voice\tts\tts_service.py._check_availability`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 66
- **Arguments:** self
- **Returns:** bool

---

### `features\voice\tts\tts_service.py._simulate_tts_finished`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 153
- **Arguments:** self

---

### `features\voice\tts\tts_service.py._speak_with_espeak`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 130
- **Arguments:** self, text

---

### `features\voice\tts\tts_service.py.cleanup`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 227
- **Arguments:** self
- **Docstring:** Cleanup TTS service resources...

---

### `features\voice\tts\tts_service.py.get_coqui_model_info`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 206
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get information about the current Coqui TTS model...

---

### `features\voice\tts\tts_service.py.get_coqui_models`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 194
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get available Coqui TTS models...

---

### `features\voice\tts\tts_service.py.get_coqui_voices`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 200
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get available Coqui TTS voices for current model...

---

### `features\voice\tts\tts_service.py.get_instance`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 34
- **Arguments:** 
- **Decorators:** staticmethod
- **Docstring:** Get the singleton instance of TTSService...

---

### `features\voice\tts\tts_service.py.is_available`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 75
- **Arguments:** self
- **Returns:** bool

---

### `features\voice\tts\tts_service.py.is_coqui_available`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 190
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Coqui TTS is available...

---

### `features\voice\tts\tts_service.py.is_initialized`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 78
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if TTS service is properly initialized...

---

### `features\voice\tts\tts_service.py.load_coqui_model`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 212
- **Arguments:** self, model_name
- **Returns:** bool
- **Docstring:** Load a specific Coqui TTS model...

---

### `features\voice\tts\tts_service.py.set_coqui_model`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 218
- **Arguments:** self, model_name
- **Returns:** bool
- **Docstring:** Set the Coqui TTS model to use...

---

### `features\voice\tts\tts_service.py.speak_text`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 82
- **Arguments:** self, text

---

### `features\voice\tts\tts_service.py.speak_text_non_streaming`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 113
- **Arguments:** self, text
- **Docstring:** Convert text to speech using non-streaming synthesis...

---

### `features\voice\tts\tts_service.py.speak_text_streaming`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 97
- **Arguments:** self, text
- **Docstring:** Convert text to speech using streaming synthesis (Coqui TTS only)...

---

### `features\voice\tts\tts_service.py.stop_playback`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 156
- **Arguments:** self

---

### `features\voice\tts\tts_service.py.update_api`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 165
- **Arguments:** self, api_name

---

### `features\voice\tts\tts_service.py.update_speed`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 181
- **Arguments:** self, speed
- **Docstring:** Update speech speed (1.0 = normal, 1.5 = faster, 0.5 = slower)...

---

### `features\voice\tts\tts_service.py.update_voice`

- **File:** `features\voice\tts\tts_service.py`
- **Line:** 173
- **Arguments:** self, voice_name

---

### `features\voice\voice_service.py.__init__`

- **File:** `features\voice\voice_service.py`
- **Line:** 51
- **Arguments:** self

---

### `features\voice\voice_service.py._check_and_emit_ready`

- **File:** `features\voice\voice_service.py`
- **Line:** 1229
- **Arguments:** self
- **Docstring:** Check if all services are ready and emit signal if they are...

---

### `features\voice\voice_service.py._cleanup_resources`

- **File:** `features\voice\voice_service.py`
- **Line:** 1110
- **Arguments:** self
- **Docstring:** Clean up resources with error handling...

---

### `features\voice\voice_service.py._complete_request`

- **File:** `features\voice\voice_service.py`
- **Line:** 400
- **Arguments:** self
- **Docstring:** Complete current request and process next...

---

### `features\voice\voice_service.py._connect_signals`

- **File:** `features\voice\voice_service.py`
- **Line:** 1149
- **Arguments:** self
- **Docstring:** Connect signals from voice services...

---

### `features\voice\voice_service.py._forward_recording_error`

- **File:** `features\voice\voice_service.py`
- **Line:** 1094
- **Arguments:** self, error
- **Docstring:** Forward recording error signal to response queue...

---

### `features\voice\voice_service.py._forward_recording_started`

- **File:** `features\voice\voice_service.py`
- **Line:** 1078
- **Arguments:** self
- **Docstring:** Forward recording started signal to response queue...

---

### `features\voice\voice_service.py._forward_recording_stopped`

- **File:** `features\voice\voice_service.py`
- **Line:** 1086
- **Arguments:** self
- **Docstring:** Forward recording stopped signal to response queue...

---

### `features\voice\voice_service.py._forward_voice_processing_started`

- **File:** `features\voice\voice_service.py`
- **Line:** 1102
- **Arguments:** self
- **Docstring:** Forward voice processing started signal to response queue...

---

### `features\voice\voice_service.py._handle_tts_request`

- **File:** `features\voice\voice_service.py`
- **Line:** 366
- **Arguments:** self, data
- **Docstring:** Handle TTS request...

---

### `features\voice\voice_service.py._handle_voice_input_request`

- **File:** `features\voice\voice_service.py`
- **Line:** 339
- **Arguments:** self, data
- **Docstring:** Handle voice input request...

---

### `features\voice\voice_service.py._initialize_services`

- **File:** `features\voice\voice_service.py`
- **Line:** 1155
- **Arguments:** self
- **Docstring:** Initialize voice services with error handling...

---

### `features\voice\voice_service.py._on_audio_level_changed`

- **File:** `features\voice\voice_service.py`
- **Line:** 494
- **Arguments:** self, audio_level
- **Docstring:** Handle audio level changes for interruption detection...

---

### `features\voice\voice_service.py._on_recording_auto_stopped`

- **File:** `features\voice\voice_service.py`
- **Line:** 215
- **Arguments:** self
- **Docstring:** Handle automatic recording stop...

---

### `features\voice\voice_service.py._on_recording_auto_stopped_for_stt`

- **File:** `features\voice\voice_service.py`
- **Line:** 220
- **Arguments:** self
- **Docstring:** Handle automatic recording stop for STT processing...

---

### `features\voice\voice_service.py._on_recording_error`

- **File:** `features\voice\voice_service.py`
- **Line:** 209
- **Arguments:** self, error
- **Docstring:** Handle recording error signal...

---

### `features\voice\voice_service.py._on_recording_started`

- **File:** `features\voice\voice_service.py`
- **Line:** 197
- **Arguments:** self
- **Docstring:** Handle recording started signal...

---

### `features\voice\voice_service.py._on_recording_stopped`

- **File:** `features\voice\voice_service.py`
- **Line:** 203
- **Arguments:** self
- **Docstring:** Handle recording stopped signal...

---

### `features\voice\voice_service.py._on_recording_timeout`

- **File:** `features\voice\voice_service.py`
- **Line:** 249
- **Arguments:** self
- **Docstring:** Handle recording timeout...

---

### `features\voice\voice_service.py._on_stt_error`

- **File:** `features\voice\voice_service.py`
- **Line:** 664
- **Arguments:** self, error
- **Docstring:** Handle STT error...

---

### `features\voice\voice_service.py._on_stt_text_received`

- **File:** `features\voice\voice_service.py`
- **Line:** 568
- **Arguments:** self, text

---

### `features\voice\voice_service.py._on_tts_error`

- **File:** `features\voice\voice_service.py`
- **Line:** 759
- **Arguments:** self, error
- **Docstring:** Handle TTS error with comprehensive error handling...

---

### `features\voice\voice_service.py._on_tts_finished`

- **File:** `features\voice\voice_service.py`
- **Line:** 723
- **Arguments:** self
- **Docstring:** Handle TTS finished event with comprehensive error handling...

---

### `features\voice\voice_service.py._on_tts_started`

- **File:** `features\voice\voice_service.py`
- **Line:** 699
- **Arguments:** self
- **Docstring:** Handle TTS started...

---

### `features\voice\voice_service.py._process_request_queue`

- **File:** `features\voice\voice_service.py`
- **Line:** 312
- **Arguments:** self
- **Docstring:** Process queued requests if capacity allows...

---

### `features\voice\voice_service.py._reset_error_count`

- **File:** `features\voice\voice_service.py`
- **Line:** 1144
- **Arguments:** self
- **Docstring:** Reset error count after a delay...

---

### `features\voice\voice_service.py._restart_voice_input_safely`

- **File:** `features\voice\voice_service.py`
- **Line:** 636
- **Arguments:** self
- **Docstring:** Safely restart voice input after ensuring queue is processed...

---

### `features\voice\voice_service.py._setup_connections`

- **File:** `features\voice\voice_service.py`
- **Line:** 117
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `features\voice\voice_service.py._setup_service_connections`

- **File:** `features\voice\voice_service.py`
- **Line:** 154
- **Arguments:** self
- **Docstring:** Setup connections for newly initialized services...

---

### `features\voice\voice_service.py._speak_text_impl`

- **File:** `features\voice\voice_service.py`
- **Line:** 821
- **Arguments:** self, text
- **Docstring:** Implementation of speak_text with thread safety...

---

### `features\voice\voice_service.py.can_handle_new_request`

- **File:** `features\voice\voice_service.py`
- **Line:** 285
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if we can handle a new request without overload...

---

### `features\voice\voice_service.py.cancel_current_request`

- **File:** `features\voice\voice_service.py`
- **Line:** 437
- **Arguments:** self
- **Docstring:** Cancel the current request...

---

### `features\voice\voice_service.py.cleanup_all_audio_files`

- **File:** `features\voice\voice_service.py`
- **Line:** 1059
- **Arguments:** self
- **Docstring:** Clean up all audio files (since they're only for STT processing)...

---

### `features\voice\voice_service.py.cleanup_old_audio_files`

- **File:** `features\voice\voice_service.py`
- **Line:** 1026
- **Arguments:** self, max_files, max_age_days
- **Docstring:** Clean up old audio files to prevent folder from getting too large...

---

### `features\voice\voice_service.py.cleanup_on_exit`

- **File:** `features\voice\voice_service.py`
- **Line:** 937
- **Arguments:** self
- **Docstring:** Comprehensive cleanup with error handling...

---

### `features\voice\voice_service.py.clear_request_queue`

- **File:** `features\voice\voice_service.py`
- **Line:** 409
- **Arguments:** self
- **Docstring:** Clear all requests and reset voice service state...

---

### `features\voice\voice_service.py.get_audio_folder_path`

- **File:** `features\voice\voice_service.py`
- **Line:** 1000
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the path to the audio folder...

---

### `features\voice\voice_service.py.get_current_audio_level`

- **File:** `features\voice\voice_service.py`
- **Line:** 913
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current audio level from recording service...

---

### `features\voice\voice_service.py.get_instance`

- **File:** `features\voice\voice_service.py`
- **Line:** 46
- **Arguments:** 
- **Decorators:** staticmethod

---

### `features\voice\voice_service.py.get_recording_timeout`

- **File:** `features\voice\voice_service.py`
- **Line:** 909
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get recording timeout setting...

---

### `features\voice\voice_service.py.get_silence_duration`

- **File:** `features\voice\voice_service.py`
- **Line:** 901
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get silence duration setting...

---

### `features\voice\voice_service.py.get_silence_threshold`

- **File:** `features\voice\voice_service.py`
- **Line:** 905
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get silence threshold setting...

---

### `features\voice\voice_service.py.handle_user_interruption`

- **File:** `features\voice\voice_service.py`
- **Line:** 462
- **Arguments:** self
- **Docstring:** Handle user interruption during AI response...

---

### `features\voice\voice_service.py.is_continuous_voice_mode`

- **File:** `features\voice\voice_service.py`
- **Line:** 892
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if continuous voice mode is enabled...

---

### `features\voice\voice_service.py.is_voice_available`

- **File:** `features\voice\voice_service.py`
- **Line:** 255
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice functionality is available...

---

### `features\voice\voice_service.py.list_audio_files`

- **File:** `features\voice\voice_service.py`
- **Line:** 1004
- **Arguments:** self
- **Returns:** list
- **Docstring:** List all audio files in the audio folder...

---

### `features\voice\voice_service.py.queue_request`

- **File:** `features\voice\voice_service.py`
- **Line:** 292
- **Arguments:** self, request_type, data
- **Returns:** str
- **Docstring:** Queue a new request and return request ID...

---

### `features\voice\voice_service.py.set_audio_gate_enabled`

- **File:** `features\voice\voice_service.py`
- **Line:** 931
- **Arguments:** self, enabled
- **Docstring:** Set audio gate enabled setting...

---

### `features\voice\voice_service.py.set_continuous_voice_mode`

- **File:** `features\voice\voice_service.py`
- **Line:** 887
- **Arguments:** self, enabled
- **Docstring:** Set continuous voice mode...

---

### `features\voice\voice_service.py.set_recording_timeout`

- **File:** `features\voice\voice_service.py`
- **Line:** 919
- **Arguments:** self, timeout
- **Docstring:** Set recording timeout setting...

---

### `features\voice\voice_service.py.set_silence_duration`

- **File:** `features\voice\voice_service.py`
- **Line:** 923
- **Arguments:** self, duration
- **Docstring:** Set silence duration setting...

---

### `features\voice\voice_service.py.set_silence_threshold`

- **File:** `features\voice\voice_service.py`
- **Line:** 927
- **Arguments:** self, threshold
- **Docstring:** Set silence threshold setting...

---

### `features\voice\voice_service.py.speak_text`

- **File:** `features\voice\voice_service.py`
- **Line:** 789
- **Arguments:** self, text
- **Docstring:** Speak text with comprehensive error handling and thread safety...

---

### `features\voice\voice_service.py.start_voice_input`

- **File:** `features\voice\voice_service.py`
- **Line:** 515
- **Arguments:** self
- **Docstring:** Start voice recording and convert to text...

---

### `features\voice\voice_service.py.stop_tts`

- **File:** `features\voice\voice_service.py`
- **Line:** 864
- **Arguments:** self
- **Docstring:** Stop TTS with comprehensive error handling...

---

### `features\voice\voice_service.py.stop_voice_input`

- **File:** `features\voice\voice_service.py`
- **Line:** 549
- **Arguments:** self
- **Docstring:** Stop voice recording and process the audio...

---

### `features\voice\voice_service.py.update_settings`

- **File:** `features\voice\voice_service.py`
- **Line:** 896
- **Arguments:** self, settings
- **Docstring:** Update voice settings...

---

### `features\voice\voice_service_manager.py.__init__`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 36
- **Arguments:** self
- **Docstring:** Initialize the voice service manager (singleton)...

---

### `features\voice\voice_service_manager.py.__new__`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 28
- **Arguments:** cls
- **Docstring:** Singleton pattern implementation...

---

### `features\voice\voice_service_manager.py._initialize_voice_service`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 76
- **Arguments:** self
- **Docstring:** Initialize the voice service...

---

### `features\voice\voice_service_manager.py._on_voice_service_ready`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 139
- **Arguments:** self
- **Docstring:** Handle voice service ready signal from the actual service...

---

### `features\voice\voice_service_manager.py._reset_voice_service`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 175
- **Arguments:** self
- **Docstring:** Reset the voice service (for reinitialization)...

---

### `features\voice\voice_service_manager.py._try_direct_initialization`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 162
- **Arguments:** self
- **Docstring:** Try direct voice service initialization (always use direct service, skip wrapper)...

---

### `features\voice\voice_service_manager.py._try_get_from_service_manager`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 144
- **Arguments:** self
- **Docstring:** Try to get voice service from service manager...

---

### `features\voice\voice_service_manager.py.cleanup`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 257
- **Arguments:** self
- **Docstring:** Cleanup the voice service manager...

---

### `features\voice\voice_service_manager.py.force_reinitialize`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 251
- **Arguments:** self
- **Docstring:** Force reinitialization of the voice service...

---

### `features\voice\voice_service_manager.py.get_last_error`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 230
- **Arguments:** self
- **Docstring:** Get the last initialization error...

---

### `features\voice\voice_service_manager.py.get_settings`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 210
- **Arguments:** self
- **Docstring:** Get current voice service settings...

---

### `features\voice\voice_service_manager.py.get_voice_service`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 58
- **Arguments:** self, force_reinitialize
- **Docstring:** Get the voice service instance, initializing if necessary

Args:
    force_reinitialize: Force reini...

---

### `features\voice\voice_service_manager.py.get_voice_service_manager`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 278
- **Arguments:** 
- **Returns:** VoiceServiceManager
- **Docstring:** Get the global voice service manager instance...

---

### `features\voice\voice_service_manager.py.is_initializing`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 226
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice service is currently initializing...

---

### `features\voice\voice_service_manager.py.is_ready`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 220
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice service is ready...

---

### `features\voice\voice_service_manager.py.register_ready_callback`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 234
- **Arguments:** self, callback
- **Docstring:** Register a callback to be called when voice service becomes ready

Args:
    callback: Function to c...

---

### `features\voice\voice_service_manager.py.update_settings`

- **File:** `features\voice\voice_service_manager.py`
- **Line:** 192
- **Arguments:** self, settings
- **Docstring:** Update voice service settings

Args:
    settings: Dictionary of settings to apply...

---

### `features\voice\voice_service_wrapper.py.__init__`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 33
- **Arguments:** self, use_separate_process

---

### `features\voice\voice_service_wrapper.py._check_service_readiness`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 351
- **Arguments:** self
- **Docstring:** Check if the voice service is ready and emit signal if it is...

---

### `features\voice\voice_service_wrapper.py._init_direct_service`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 70
- **Arguments:** self
- **Docstring:** Initialize direct voice service (fallback)...

---

### `features\voice\voice_service_wrapper.py._init_process_manager`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 49
- **Arguments:** self
- **Docstring:** Initialize the process manager...

---

### `features\voice\voice_service_wrapper.py._on_voice_service_ready`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 338
- **Arguments:** self
- **Docstring:** Handle voice service ready signal...

---

### `features\voice\voice_service_wrapper.py._update_cached_state`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 300
- **Arguments:** self
- **Docstring:** Update cached state from process manager...

---

### `features\voice\voice_service_wrapper.py._update_cached_state_from_signal`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 306
- **Arguments:** self, state
- **Docstring:** Update cached state from signal...

---

### `features\voice\voice_service_wrapper.py.cleanup_all_audio_files`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 283
- **Arguments:** self
- **Docstring:** Clean up all audio files...

---

### `features\voice\voice_service_wrapper.py.cleanup_old_audio_files`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 278
- **Arguments:** self, max_files, max_age_days
- **Docstring:** Clean up old audio files to prevent folder from getting too large...

---

### `features\voice\voice_service_wrapper.py.cleanup_on_exit`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 259
- **Arguments:** self
- **Docstring:** Clean up resources on application exit...

---

### `features\voice\voice_service_wrapper.py.get_audio_folder_path`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 266
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the path to the audio folder...

---

### `features\voice\voice_service_wrapper.py.get_current_audio_level`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 238
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current audio level for debugging...

---

### `features\voice\voice_service_wrapper.py.get_process_info`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 288
- **Arguments:** self
- **Docstring:** Get information about the voice process...

---

### `features\voice\voice_service_wrapper.py.get_recording_timeout`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 200
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current recording timeout in seconds...

---

### `features\voice\voice_service_wrapper.py.get_silence_duration`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 211
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current silence duration in seconds...

---

### `features\voice\voice_service_wrapper.py.get_silence_threshold`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 222
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current silence threshold (0-1)...

---

### `features\voice\voice_service_wrapper.py.is_continuous_voice_mode`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 253
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if continuous voice mode is enabled...

---

### `features\voice\voice_service_wrapper.py.is_playing_tts`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 325
- **Arguments:** self
- **Returns:** bool
- **Decorators:** property
- **Docstring:** Check if TTS is currently playing...

---

### `features\voice\voice_service_wrapper.py.is_processing_voice`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 318
- **Arguments:** self
- **Returns:** bool
- **Decorators:** property
- **Docstring:** Check if currently processing voice input...

---

### `features\voice\voice_service_wrapper.py.is_recording`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 311
- **Arguments:** self
- **Returns:** bool
- **Decorators:** property
- **Docstring:** Check if currently recording...

---

### `features\voice\voice_service_wrapper.py.is_voice_available`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 182
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice functionality is available...

---

### `features\voice\voice_service_wrapper.py.list_audio_files`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 272
- **Arguments:** self
- **Returns:** list
- **Docstring:** List all audio files in the audio folder...

---

### `features\voice\voice_service_wrapper.py.recording_service`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 332
- **Arguments:** self
- **Decorators:** property
- **Docstring:** Get the recording service (only available in direct mode)...

---

### `features\voice\voice_service_wrapper.py.set_audio_gate_enabled`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 233
- **Arguments:** self, enabled
- **Docstring:** Enable or disable audio gate detection...

---

### `features\voice\voice_service_wrapper.py.set_continuous_voice_mode`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 244
- **Arguments:** self, enabled
- **Docstring:** Enable or disable continuous voice mode...

---

### `features\voice\voice_service_wrapper.py.set_recording_timeout`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 206
- **Arguments:** self, timeout
- **Docstring:** Set recording timeout in seconds...

---

### `features\voice\voice_service_wrapper.py.set_silence_duration`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 217
- **Arguments:** self, duration
- **Docstring:** Set silence duration in seconds...

---

### `features\voice\voice_service_wrapper.py.set_silence_threshold`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 228
- **Arguments:** self, threshold
- **Docstring:** Set silence threshold (0-1)...

---

### `features\voice\voice_service_wrapper.py.speak_text`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 126
- **Arguments:** self, text
- **Docstring:** Convert text to speech and play it...

---

### `features\voice\voice_service_wrapper.py.speak_text_non_streaming`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 154
- **Arguments:** self, text
- **Docstring:** Convert text to speech using non-streaming synthesis...

---

### `features\voice\voice_service_wrapper.py.speak_text_streaming`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 140
- **Arguments:** self, text
- **Docstring:** Convert text to speech using streaming synthesis...

---

### `features\voice\voice_service_wrapper.py.start_voice_input`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 98
- **Arguments:** self
- **Docstring:** Start voice recording and convert to text...

---

### `features\voice\voice_service_wrapper.py.stop_tts`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 168
- **Arguments:** self
- **Docstring:** Stop current TTS playback...

---

### `features\voice\voice_service_wrapper.py.stop_voice_input`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 112
- **Arguments:** self
- **Docstring:** Stop voice recording and process the audio...

---

### `features\voice\voice_service_wrapper.py.test_connection`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 294
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Test connection to voice process...

---

### `features\voice\voice_service_wrapper.py.update_settings`

- **File:** `features\voice\voice_service_wrapper.py`
- **Line:** 191
- **Arguments:** self, settings
- **Docstring:** Update voice service settings...

---

### `startup\dependency_checker.py.__init__`

- **File:** `startup\dependency_checker.py`
- **Line:** 20
- **Arguments:** self

---

### `startup\dependency_checker.py.check_and_install_dependencies`

- **File:** `startup\dependency_checker.py`
- **Line:** 207
- **Arguments:** auto_install, verbose
- **Returns:** bool
- **Docstring:** Check dependencies and optionally install missing ones.

Args:
    auto_install: If True, automatica...

---

### `startup\dependency_checker.py.check_core_dependencies`

- **File:** `startup\dependency_checker.py`
- **Line:** 42
- **Arguments:** self
- **Docstring:** Check core application dependencies....

---

### `startup\dependency_checker.py.check_ml_dependencies`

- **File:** `startup\dependency_checker.py`
- **Line:** 83
- **Arguments:** self
- **Docstring:** Check machine learning dependencies (all optional)....

---

### `startup\dependency_checker.py.check_package_versions`

- **File:** `startup\dependency_checker.py`
- **Line:** 118
- **Arguments:** self
- **Docstring:** Check for version conflicts....

---

### `startup\dependency_checker.py.check_tts_options`

- **File:** `startup\dependency_checker.py`
- **Line:** 102
- **Arguments:** self
- **Docstring:** Check if at least one TTS option is available....

---

### `startup\dependency_checker.py.get_dependency_summary`

- **File:** `startup\dependency_checker.py`
- **Line:** 199
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get a concise summary of dependency status....

---

### `startup\dependency_checker.py.get_missing_dependencies`

- **File:** `startup\dependency_checker.py`
- **Line:** 166
- **Arguments:** self
- **Docstring:** Get list of missing dependencies....

---

### `startup\dependency_checker.py.get_version_conflicts`

- **File:** `startup\dependency_checker.py`
- **Line:** 170
- **Arguments:** self
- **Docstring:** Get list of version conflicts....

---

### `startup\dependency_checker.py.run_comprehensive_check`

- **File:** `startup\dependency_checker.py`
- **Line:** 155
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Run the complete dependency check and return if fixes are needed....

---

### `startup\dependency_checker.py.run_install_dependencies`

- **File:** `startup\dependency_checker.py`
- **Line:** 174
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Run the install_dependencies.py script....

---

### `startup\dependency_checker.py.test_import`

- **File:** `startup\dependency_checker.py`
- **Line:** 26
- **Arguments:** self, module_name, description
- **Docstring:** Test if a module can be imported successfully and return version....

---

### `startup\install_dependencies.py.main`

- **File:** `startup\install_dependencies.py`
- **Line:** 21
- **Arguments:** 

---

### `startup\python_installer.py.install_python_requirements`

- **File:** `startup\python_installer.py`
- **Line:** 6
- **Arguments:** requirements_path

---

### `startup\system_installer.py.ensure_system_dependencies`

- **File:** `startup\system_installer.py`
- **Line:** 38
- **Arguments:** 

---

### `startup\system_installer.py.is_admin`

- **File:** `startup\system_installer.py`
- **Line:** 8
- **Arguments:** 

---

### `startup\system_installer.py.offer_add_espeak_to_path`

- **File:** `startup\system_installer.py`
- **Line:** 14
- **Arguments:** 

---

### `ui\Widgets\chat_navigation.py.__init__`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 24
- **Arguments:** self, conversation_manager, summarization_service, parent

---

### `ui\Widgets\chat_navigation.py.clear_all_conversations`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 331
- **Arguments:** self
- **Docstring:** Delete all conversations after confirmation...

---

### `ui\Widgets\chat_navigation.py.create_conversation_item`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 191
- **Arguments:** self, filepath, metadata
- **Returns:** QListWidgetItem
- **Docstring:** Create a list item for a conversation...

---

### `ui\Widgets\chat_navigation.py.delete_conversation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 292
- **Arguments:** self, filepath
- **Docstring:** Delete a conversation...

---

### `ui\Widgets\chat_navigation.py.get_selected_conversation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 324
- **Arguments:** self
- **Docstring:** Get the currently selected conversation filepath...

---

### `ui\Widgets\chat_navigation.py.on_conversation_double_clicked`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 212
- **Arguments:** self, item
- **Docstring:** Handle double-click on conversation item...

---

### `ui\Widgets\chat_navigation.py.on_summarization_completed`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 386
- **Arguments:** self, filepath, generated_name
- **Docstring:** Handle successful summarization...

---

### `ui\Widgets\chat_navigation.py.on_summarization_failed`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 412
- **Arguments:** self, filepath, error_message
- **Docstring:** Handle summarization failure...

---

### `ui\Widgets\chat_navigation.py.refresh_conversations`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 161
- **Arguments:** self
- **Docstring:** Refresh the list of conversations...

---

### `ui\Widgets\chat_navigation.py.rename_conversation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 255
- **Arguments:** self, filepath
- **Docstring:** Rename a conversation file...

---

### `ui\Widgets\chat_navigation.py.set_current_conversation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 319
- **Arguments:** self, filepath
- **Docstring:** Set the currently active conversation...

---

### `ui\Widgets\chat_navigation.py.setup_connections`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 149
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\Widgets\chat_navigation.py.setup_ui`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 35
- **Arguments:** self
- **Docstring:** Setup the navigation UI...

---

### `ui\Widgets\chat_navigation.py.show_context_menu`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 218
- **Arguments:** self, position
- **Docstring:** Show context menu for conversation items...

---

### `ui\Widgets\chat_navigation.py.trigger_name_generation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 354
- **Arguments:** self, filepath
- **Docstring:** Trigger AI name generation for a conversation...

---

### `ui\Widgets\complexity_widget.py.__init__`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 8
- **Arguments:** self, parent

---

### `ui\Widgets\complexity_widget.py._get_color_for_value`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 212
- **Arguments:** self, value, reverse
- **Returns:** QColor
- **Docstring:** Get color based on value (0-1)...

---

### `ui\Widgets\complexity_widget.py._on_switch_model`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 185
- **Arguments:** self
- **Docstring:** Handle model switch button click...

---

### `ui\Widgets\complexity_widget.py._set_progress_bar_color`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 196
- **Arguments:** self, progress_bar, color
- **Docstring:** Set progress bar color...

---

### `ui\Widgets\complexity_widget.py._set_widget_color`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 190
- **Arguments:** self, widget, color
- **Docstring:** Set widget text color...

---

### `ui\Widgets\complexity_widget.py._update_display`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 127
- **Arguments:** self
- **Docstring:** Update the display with current metrics...

---

### `ui\Widgets\complexity_widget.py._update_model_recommendation`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 179
- **Arguments:** self, recommended_model
- **Docstring:** Update the model recommendation display...

---

### `ui\Widgets\complexity_widget.py.analyze_request`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 107
- **Arguments:** self, request, conversation_history, available_models
- **Docstring:** Analyze a request and update the display...

---

### `ui\Widgets\complexity_widget.py.clear_analysis`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 226
- **Arguments:** self
- **Docstring:** Clear the current analysis...

---

### `ui\Widgets\complexity_widget.py.get_current_metrics`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 234
- **Arguments:** self
- **Docstring:** Get the current complexity metrics...

---

### `ui\Widgets\complexity_widget.py.setup_ui`

- **File:** `ui\Widgets\complexity_widget.py`
- **Line:** 14
- **Arguments:** self
- **Docstring:** Setup the user interface...

---

### `ui\Widgets\message_editor.py.__init__`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 14
- **Arguments:** self, content, message_id, parent

---

### `ui\Widgets\message_editor.py.cancel_edit`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 184
- **Arguments:** self
- **Docstring:** Cancel editing and revert to original content...

---

### `ui\Widgets\message_editor.py.finish_editing`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 189
- **Arguments:** self
- **Docstring:** Finish editing mode...

---

### `ui\Widgets\message_editor.py.get_content`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 195
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the current message content...

---

### `ui\Widgets\message_editor.py.save_edit`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 174
- **Arguments:** self
- **Docstring:** Save the edited message...

---

### `ui\Widgets\message_editor.py.set_content`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 199
- **Arguments:** self, content
- **Docstring:** Set the message content...

---

### `ui\Widgets\message_editor.py.setup_styles`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 86
- **Arguments:** self
- **Docstring:** Setup widget styles...

---

### `ui\Widgets\message_editor.py.setup_ui`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 24
- **Arguments:** self
- **Docstring:** Setup the widget UI...

---

### `ui\Widgets\message_editor.py.start_editing`

- **File:** `ui\Widgets\message_editor.py`
- **Line:** 165
- **Arguments:** self
- **Docstring:** Start editing the message...

---

### `ui\Widgets\spellchecker_widget.py.__init__`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 23
- **Arguments:** self, parent

---

### `ui\Widgets\spellchecker_widget.py.add_to_dictionary`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 109
- **Arguments:** self, word
- **Docstring:** Add word to personal dictionary...

---

### `ui\Widgets\spellchecker_widget.py.cleanup`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 205
- **Arguments:** self
- **Docstring:** Clean up resources...

---

### `ui\Widgets\spellchecker_widget.py.disable_spellcheck`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 193
- **Arguments:** self
- **Docstring:** Disable spell checking by clearing highlights...

---

### `ui\Widgets\spellchecker_widget.py.enable_spellcheck`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 186
- **Arguments:** self
- **Docstring:** Enable spell checking...

---

### `ui\Widgets\spellchecker_widget.py.highlight_misspelled_words`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 124
- **Arguments:** self
- **Docstring:** Highlight misspelled words in the text...

---

### `ui\Widgets\spellchecker_widget.py.ignore_word`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 120
- **Arguments:** self, word
- **Docstring:** Ignore the word (add to personal dictionary)...

---

### `ui\Widgets\spellchecker_widget.py.keyPressEvent`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 169
- **Arguments:** self, event
- **Docstring:** Override key press event to check spelling on space/enter...

---

### `ui\Widgets\spellchecker_widget.py.on_text_changed`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 179
- **Arguments:** self
- **Docstring:** Handle text changes for spell checking...

---

### `ui\Widgets\spellchecker_widget.py.replace_word`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 99
- **Arguments:** self, cursor, new_word
- **Docstring:** Replace the misspelled word with the suggestion...

---

### `ui\Widgets\spellchecker_widget.py.setup_context_menu`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 50
- **Arguments:** self
- **Docstring:** Setup context menu for spell checking...

---

### `ui\Widgets\spellchecker_widget.py.setup_spellchecker`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 33
- **Arguments:** self
- **Docstring:** Initialize the spellchecker...

---

### `ui\Widgets\spellchecker_widget.py.show_context_menu`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 55
- **Arguments:** self, position
- **Docstring:** Show context menu with spell check suggestions...

---

### `ui\dialogs\coqui_model_dialog.py.__init__`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 49
- **Arguments:** self, parent

---

### `ui\dialogs\coqui_model_dialog.py.accept_selection`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 385
- **Arguments:** self
- **Docstring:** Accept the current model and speaker selection...

---

### `ui\dialogs\coqui_model_dialog.py.create_model_panel`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 194
- **Arguments:** self
- **Docstring:** Create the model selection panel...

---

### `ui\dialogs\coqui_model_dialog.py.create_speaker_panel`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 223
- **Arguments:** self
- **Docstring:** Create the speaker selection panel...

---

### `ui\dialogs\coqui_model_dialog.py.download_selected_model`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 335
- **Arguments:** self
- **Docstring:** Download the selected model...

---

### `ui\dialogs\coqui_model_dialog.py.get_current_time`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 401
- **Arguments:** self
- **Docstring:** Get current time string...

---

### `ui\dialogs\coqui_model_dialog.py.load_models`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 246
- **Arguments:** self
- **Docstring:** Load available Coqui TTS models...

---

### `ui\dialogs\coqui_model_dialog.py.load_speakers_for_model`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 296
- **Arguments:** self, model_name
- **Docstring:** Load available speakers for the selected model...

---

### `ui\dialogs\coqui_model_dialog.py.log_status`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 393
- **Arguments:** self, message
- **Docstring:** Log a status message...

---

### `ui\dialogs\coqui_model_dialog.py.on_download_completed`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 363
- **Arguments:** self, success, message
- **Docstring:** Handle download completion...

---

### `ui\dialogs\coqui_model_dialog.py.on_model_selected`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 275
- **Arguments:** self, item
- **Docstring:** Handle model selection...

---

### `ui\dialogs\coqui_model_dialog.py.on_speaker_selected`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 329
- **Arguments:** self, item
- **Docstring:** Handle speaker selection...

---

### `ui\dialogs\coqui_model_dialog.py.run`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 25
- **Arguments:** self

---

### `ui\dialogs\coqui_model_dialog.py.setup_ui`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 65
- **Arguments:** self
- **Docstring:** Setup the dialog UI...

---

### `ui\dialogs\coqui_model_dialog.py.start_download`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 351
- **Arguments:** self, model_name
- **Docstring:** Start downloading a model...

---

### `ui\dialogs\coqui_model_dialog.py.update_selection_button`

- **File:** `ui\dialogs\coqui_model_dialog.py`
- **Line:** 378
- **Arguments:** self
- **Docstring:** Update the selection button state...

---

### `ui\dialogs\error_dialog.py.__init__`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 114
- **Arguments:** self, title, message, details, traceback, parent

---

### `ui\dialogs\error_dialog.py.accept`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 278
- **Arguments:** self
- **Docstring:** Close the dialog...

---

### `ui\dialogs\error_dialog.py.copy_error`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 226
- **Arguments:** self
- **Docstring:** Copy error details to clipboard...

---

### `ui\dialogs\error_dialog.py.reset_copy_button`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 258
- **Arguments:** self, button
- **Docstring:** Reset copy button to original state...

---

### `ui\dialogs\error_dialog.py.setup_styles`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 183
- **Arguments:** self
- **Docstring:** Setup the dialog styles...

---

### `ui\dialogs\error_dialog.py.setup_ui`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 126
- **Arguments:** self, message, details, traceback
- **Docstring:** Setup the UI components...

---

### `ui\dialogs\error_dialog.py.show_error_dialog`

- **File:** `ui\dialogs\error_dialog.py`
- **Line:** 282
- **Arguments:** title, message, details, traceback, parent
- **Docstring:** Show an error dialog with copy functionality...

---

### `ui\dialogs\settings_dialog.py.__init__`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 10
- **Arguments:** self, config_manager, available_models, available_personalities, parent

---

### `ui\dialogs\settings_dialog.py._delayed_load_settings`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 238
- **Arguments:** self
- **Docstring:** Load settings after UI is fully ready...

---

### `ui\dialogs\settings_dialog.py.create_chat_tab`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 129
- **Arguments:** self
- **Docstring:** Create the chat settings tab...

---

### `ui\dialogs\settings_dialog.py.create_developer_tab`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 220
- **Arguments:** self

---

### `ui\dialogs\settings_dialog.py.create_general_tab`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 65
- **Arguments:** self
- **Docstring:** Create the general settings tab...

---

### `ui\dialogs\settings_dialog.py.create_session_tab`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 180
- **Arguments:** self
- **Docstring:** Create the session variables tab...

---

### `ui\dialogs\settings_dialog.py.load_current_settings`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 243
- **Arguments:** self
- **Docstring:** Load current settings into the UI...

---

### `ui\dialogs\settings_dialog.py.reset_to_defaults`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 354
- **Arguments:** self
- **Docstring:** Reset all settings to defaults...

---

### `ui\dialogs\settings_dialog.py.save_settings`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 303
- **Arguments:** self
- **Docstring:** Save the current settings...

---

### `ui\dialogs\settings_dialog.py.setup_ui`

- **File:** `ui\dialogs\settings_dialog.py`
- **Line:** 21
- **Arguments:** self
- **Docstring:** Setup the user interface...

---

### `ui\dialogs\voice_settings_dialog.py.__init__`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1397
- **Arguments:** self, parent

---

### `ui\dialogs\voice_settings_dialog.py._finish`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1470
- **Arguments:** self

---

### `ui\dialogs\voice_settings_dialog.py._on_timer`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1443
- **Arguments:** self

---

### `ui\dialogs\voice_settings_dialog.py._on_voices_loaded`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 753
- **Arguments:** self, speakers
- **Docstring:** Slot to update speaker list when voices_loaded fires....

---

### `ui\dialogs\voice_settings_dialog.py._start_recording`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1437
- **Arguments:** self

---

### `ui\dialogs\voice_settings_dialog.py._start_step`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1423
- **Arguments:** self, step

---

### `ui\dialogs\voice_settings_dialog.py.check_internet_connection`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 646
- **Arguments:** self
- **Docstring:** Check internet connectivity...

---

### `ui\dialogs\voice_settings_dialog.py.create_general_tab`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 456
- **Arguments:** self
- **Docstring:** Create the general settings tab...

---

### `ui\dialogs\voice_settings_dialog.py.create_stt_tab`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 292
- **Arguments:** self
- **Docstring:** Create the STT configuration tab...

---

### `ui\dialogs\voice_settings_dialog.py.create_tts_tab`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 333
- **Arguments:** self
- **Docstring:** Create the TTS configuration tab...

---

### `ui\dialogs\voice_settings_dialog.py.download_selected_model`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1066
- **Arguments:** self
- **Docstring:** Download the selected Coqui TTS model and refresh lists after download...

---

### `ui\dialogs\voice_settings_dialog.py.filter_speakers`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 936
- **Arguments:** self, filter_type
- **Docstring:** Filter speakers based on selected criteria...

---

### `ui\dialogs\voice_settings_dialog.py.get_result`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1491
- **Arguments:** self

---

### `ui\dialogs\voice_settings_dialog.py.get_settings`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1254
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get current settings...

---

### `ui\dialogs\voice_settings_dialog.py.get_speaker_info`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 873
- **Arguments:** self, speaker_name, model_name
- **Returns:** dict
- **Docstring:** Get speaker information for display...

---

### `ui\dialogs\voice_settings_dialog.py.load_coqui_models`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 828
- **Arguments:** self
- **Docstring:** DEPRECATED: Use refresh_coqui_ui instead....

---

### `ui\dialogs\voice_settings_dialog.py.load_coqui_speakers`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 867
- **Arguments:** self, model_name
- **Docstring:** Load available speakers for the selected model with enhanced information (now async via voices_loade...

---

### `ui\dialogs\voice_settings_dialog.py.on_coqui_model_changed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 832
- **Arguments:** self, model_text
- **Docstring:** Handle Coqui TTS model selection...

---

### `ui\dialogs\voice_settings_dialog.py.on_coqui_speaker_changed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 986
- **Arguments:** self, speaker_name
- **Docstring:** Handle Coqui TTS speaker selection...

---

### `ui\dialogs\voice_settings_dialog.py.on_eq_visualizer_changed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 819
- **Arguments:** self, eq_type
- **Docstring:** Handle EQ visualizer selection change...

---

### `ui\dialogs\voice_settings_dialog.py.on_internet_check_completed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 656
- **Arguments:** self, is_connected, status
- **Docstring:** Handle internet check completion...

---

### `ui\dialogs\voice_settings_dialog.py.on_silence_threshold_changed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1093
- **Arguments:** self, value
- **Docstring:** Handle silence threshold value change...

---

### `ui\dialogs\voice_settings_dialog.py.on_stt_api_changed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 697
- **Arguments:** self, api_name
- **Docstring:** Handle STT API selection change...

---

### `ui\dialogs\voice_settings_dialog.py.on_tts_api_changed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 781
- **Arguments:** self, api_name
- **Docstring:** Handle TTS API selection change...

---

### `ui\dialogs\voice_settings_dialog.py.on_tts_settings_changed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1379
- **Arguments:** self, settings

---

### `ui\dialogs\voice_settings_dialog.py.on_voice_changed`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 815
- **Arguments:** self, voice
- **Docstring:** Handle voice selection change...

---

### `ui\dialogs\voice_settings_dialog.py.open_calibration_dialog`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1388
- **Arguments:** self

---

### `ui\dialogs\voice_settings_dialog.py.preview_selected_speaker`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1018
- **Arguments:** self
- **Docstring:** Preview the selected speaker's voice...

---

### `ui\dialogs\voice_settings_dialog.py.refresh_coqui_ui`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 711
- **Arguments:** self, force_refresh_service
- **Docstring:** Refresh Coqui TTS UI, reusing the service if possible and updating models/speakers....

---

### `ui\dialogs\voice_settings_dialog.py.run`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 30
- **Arguments:** self

---

### `ui\dialogs\voice_settings_dialog.py.safe_disconnect`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1495
- **Arguments:** signal, slot

---

### `ui\dialogs\voice_settings_dialog.py.safe_get_checked`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1197
- **Arguments:** widget, default

---

### `ui\dialogs\voice_settings_dialog.py.safe_get_text`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1188
- **Arguments:** widget, default

---

### `ui\dialogs\voice_settings_dialog.py.safe_get_value`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1207
- **Arguments:** widget, default

---

### `ui\dialogs\voice_settings_dialog.py.save_settings`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1172
- **Arguments:** self
- **Docstring:** Save the current settings...

---

### `ui\dialogs\voice_settings_dialog.py.set_settings`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1258
- **Arguments:** self, settings
- **Docstring:** Set current settings...

---

### `ui\dialogs\voice_settings_dialog.py.setup_connections`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 629
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\dialogs\voice_settings_dialog.py.setup_ui`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 153
- **Arguments:** self
- **Docstring:** Setup the dialog UI...

---

### `ui\dialogs\voice_settings_dialog.py.test_settings`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 1116
- **Arguments:** self
- **Docstring:** Test the current voice settings...

---

### `ui\dialogs\voice_settings_dialog.py.update_api_availability`

- **File:** `ui\dialogs\voice_settings_dialog.py`
- **Line:** 671
- **Arguments:** self
- **Docstring:** Update API availability based on internet connection...

---

### `ui\tabs\chat_tab\chat_display.py.__init__`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 20
- **Arguments:** self, parent, config_manager

---

### `ui\tabs\chat_tab\chat_display.py._force_render_display`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 391
- **Arguments:** self
- **Docstring:** Force render the chat display immediately...

---

### `ui\tabs\chat_tab\chat_display.py._sync_messages_from_conversation_service`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 80
- **Arguments:** self
- **Docstring:** Sync messages from conversation service to renderer to prevent duplicates...

---

### `ui\tabs\chat_tab\chat_display.py.append_response_chunk`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 410
- **Arguments:** self, chunk, model_name, msg_id, chunk_index
- **Docstring:** Append a streaming response chunk, now with msg_id and chunk_index support and duplicate guard....

---

### `ui\tabs\chat_tab\chat_display.py.append_to_chat`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 354
- **Arguments:** self, sender, message, is_code

---

### `ui\tabs\chat_tab\chat_display.py.chat_display_mouse_move_event`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 144
- **Arguments:** self, event
- **Docstring:** Handle mouse move events to show/hide edit buttons...

---

### `ui\tabs\chat_tab\chat_display.py.clear_chat`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 477
- **Arguments:** self
- **Docstring:** Clear the chat display...

---

### `ui\tabs\chat_tab\chat_display.py.edit_message_at_index`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 212
- **Arguments:** self, message_index
- **Docstring:** Edit message at specific index...

---

### `ui\tabs\chat_tab\chat_display.py.force_update_display`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 380
- **Arguments:** self
- **Docstring:** Force an immediate update of the chat display...

---

### `ui\tabs\chat_tab\chat_display.py.get_ai_name`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 138
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the AI name - this should be overridden by parent...

---

### `ui\tabs\chat_tab\chat_display.py.get_streaming_handler`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 495
- **Arguments:** self
- **Docstring:** Get the streaming handler (now returns chat renderer for compatibility)...

---

### `ui\tabs\chat_tab\chat_display.py.get_ui_components`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 488
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get UI components for integration with parent...

---

### `ui\tabs\chat_tab\chat_display.py.hide_edit_button`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 204
- **Arguments:** self
- **Docstring:** Hide the edit button...

---

### `ui\tabs\chat_tab\chat_display.py.on_message_edited`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 347
- **Arguments:** self, message_index, new_content
- **Docstring:** Handle message edit from streaming handler...

---

### `ui\tabs\chat_tab\chat_display.py.on_render_completed`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 331
- **Arguments:** self
- **Docstring:** Handle completion of rendering...

---

### `ui\tabs\chat_tab\chat_display.py.on_render_error`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 336
- **Arguments:** self, error_message
- **Docstring:** Handle rendering errors...

---

### `ui\tabs\chat_tab\chat_display.py.save_message_edit`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 312
- **Arguments:** self, dialog, message_index, new_content
- **Docstring:** Save the edited message...

---

### `ui\tabs\chat_tab\chat_display.py.setup_chat_renderer`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 63
- **Arguments:** self
- **Docstring:** Setup the chat renderer for chat display...

---

### `ui\tabs\chat_tab\chat_display.py.setup_ui_components`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 35
- **Arguments:** self
- **Docstring:** Setup UI components for chat display...

---

### `ui\tabs\chat_tab\chat_display.py.show_edit_button`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 170
- **Arguments:** self, pos, message_index
- **Docstring:** Show edit button for a specific message...

---

### `ui\tabs\chat_tab\chat_display.py.show_message_edit_dialog`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 223
- **Arguments:** self, message_index, current_content
- **Docstring:** Show dialog to edit a message...

---

### `ui\tabs\chat_tab\chat_display.py.start_streaming`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 449
- **Arguments:** self
- **Docstring:** Start streaming state...

---

### `ui\tabs\chat_tab\chat_display.py.stop_streaming`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 461
- **Arguments:** self
- **Docstring:** Stop streaming state...

---

### `ui\tabs\chat_tab\chat_display.py.sync_messages_from_conversation_service`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 130
- **Arguments:** self

---

### `ui\tabs\chat_tab\chat_renderer.py.__init__`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 22
- **Arguments:** self, chat_display, ai_name, config_manager

---

### `ui\tabs\chat_tab\chat_renderer.py._emergency_reset`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 306
- **Arguments:** self
- **Docstring:** Emergency reset if render gets stuck...

---

### `ui\tabs\chat_tab\chat_renderer.py._execute_render`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 274
- **Arguments:** self
- **Docstring:** Execute the actual render - simplified and unified...

---

### `ui\tabs\chat_tab\chat_renderer.py._get_current_streaming_message`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 116
- **Arguments:** self
- **Docstring:** Return the current (last) streaming message, or None if not found....

---

### `ui\tabs\chat_tab\chat_renderer.py._get_next_message_id`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 58
- **Arguments:** self
- **Returns:** str
- **Docstring:** Generate a unique message ID...

---

### `ui\tabs\chat_tab\chat_renderer.py._process_typewriter_chunk`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 134
- **Arguments:** self

---

### `ui\tabs\chat_tab\chat_renderer.py._render_chat_display`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 321
- **Arguments:** self
- **Docstring:** Render the chat display with all messages...

---

### `ui\tabs\chat_tab\chat_renderer.py._reset_render_counter`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 317
- **Arguments:** self
- **Docstring:** Reset the render counter periodically...

---

### `ui\tabs\chat_tab\chat_renderer.py.add_message`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 63
- **Arguments:** self, sender, content, is_code, is_streaming, tag
- **Returns:** str
- **Docstring:** Add a message to the renderer's storage...

---

### `ui\tabs\chat_tab\chat_renderer.py.append_message`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 81
- **Arguments:** self, sender, content, is_code, tag
- **Docstring:** Append a new message and request render...

---

### `ui\tabs\chat_tab\chat_renderer.py.cleanup`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 478
- **Arguments:** self
- **Docstring:** Clean up resources...

---

### `ui\tabs\chat_tab\chat_renderer.py.clear_chat`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 208
- **Arguments:** self
- **Docstring:** Clear all messages and render...

---

### `ui\tabs\chat_tab\chat_renderer.py.clear_messages`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 227
- **Arguments:** self
- **Docstring:** Clear all messages...

---

### `ui\tabs\chat_tab\chat_renderer.py.edit_message`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 88
- **Arguments:** self, message_index, new_content
- **Returns:** bool
- **Docstring:** Edit a specific message by index...

---

### `ui\tabs\chat_tab\chat_renderer.py.finalize_streaming_message`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 193
- **Arguments:** self
- **Docstring:** Mark the last streaming message as finalized...

---

### `ui\tabs\chat_tab\chat_renderer.py.get_messages`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 223
- **Arguments:** self
- **Docstring:** Get all messages...

---

### `ui\tabs\chat_tab\chat_renderer.py.request_render`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 248
- **Arguments:** self, immediate
- **Docstring:** Request a render - unified entry point...

---

### `ui\tabs\chat_tab\chat_renderer.py.start_streaming_message`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 123
- **Arguments:** self, sender, tag
- **Returns:** str

---

### `ui\tabs\chat_tab\chat_renderer.py.sync_messages_from_conversation`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 237
- **Arguments:** self, conversation_messages
- **Docstring:** Sync messages from conversation service to renderer (replace, never append)....

---

### `ui\tabs\chat_tab\chat_renderer.py.sync_messages_from_handler`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 232
- **Arguments:** self, handler_messages
- **Docstring:** Sync messages from the streaming handler...

---

### `ui\tabs\chat_tab\chat_renderer.py.update_last_system_switch`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 100
- **Arguments:** self, message
- **Docstring:** Update the last system message with new content...

---

### `ui\tabs\chat_tab\chat_renderer.py.update_message`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 214
- **Arguments:** self, message_id, content, is_code, tag
- **Docstring:** Update an existing message...

---

### `ui\tabs\chat_tab\chat_renderer.py.update_streaming_message`

- **File:** `ui\tabs\chat_tab\chat_renderer.py`
- **Line:** 156
- **Arguments:** self, content, sender, message_id, is_code, tag, append
- **Docstring:** Update the content of the current streaming message with typewriter effect, or instantly if disabled...

---

### `ui\tabs\chat_tab\chat_tab.py.__init__`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 51
- **Arguments:** self, parent, conversation_manager, summarization_service, config_manager

---

### `ui\tabs\chat_tab\chat_tab.py._append_response_chunk_safe`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 931
- **Arguments:** self, chunk, model_name, msg_id, chunk_index
- **Docstring:** Append a streaming response chunk safely in the main thread, now with msg_id and chunk_index support...

---

### `ui\tabs\chat_tab\chat_tab.py._ensure_chat_display_visible`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 955
- **Arguments:** self
- **Docstring:** Ensure the chat display is visible for message display...

---

### `ui\tabs\chat_tab\chat_tab.py._ensure_voice_controls_initialized`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 346
- **Arguments:** self
- **Docstring:** Ensure voice controls are initialized with proper signal management...

---

### `ui\tabs\chat_tab\chat_tab.py._finalize_and_start`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1366
- **Arguments:** 

---

### `ui\tabs\chat_tab\chat_tab.py._force_chat_display_update`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 901
- **Arguments:** self
- **Docstring:** Force immediate update of the chat display...

---

### `ui\tabs\chat_tab\chat_tab.py._force_enable_send_button_safe`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1076
- **Arguments:** self
- **Docstring:** Force enable the send button safely in the main thread...

---

### `ui\tabs\chat_tab\chat_tab.py._load_conversation_fallback`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1276
- **Arguments:** self, filepath
- **Docstring:** Fallback method for loading conversation when conversation service is not available...

---

### `ui\tabs\chat_tab\chat_tab.py._on_conversation_updated`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 301
- **Arguments:** self
- **Docstring:** Handle conversation updates from conversation service...

---

### `ui\tabs\chat_tab\chat_tab.py._start_streaming_safe`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 988
- **Arguments:** self
- **Docstring:** Start streaming state safely in the main thread...

---

### `ui\tabs\chat_tab\chat_tab.py.append_response_chunk`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 926
- **Arguments:** self, chunk, model_name, msg_id, chunk_index
- **Docstring:** Append a streaming response chunk (single call per chunk, all args required)....

---

### `ui\tabs\chat_tab\chat_tab.py.append_to_chat`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 881
- **Arguments:** self, sender, message, is_code
- **Docstring:** Add a message to the chat display...

---

### `ui\tabs\chat_tab\chat_tab.py.clear_chat`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1098
- **Arguments:** self
- **Docstring:** Clear the chat display...

---

### `ui\tabs\chat_tab\chat_tab.py.finalize_streaming_and_start_tts`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1363
- **Arguments:** self, tts_text
- **Docstring:** Finalize chat display after streaming, then start TTS playback...

---

### `ui\tabs\chat_tab\chat_tab.py.force_enable_send_button`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1071
- **Arguments:** self
- **Docstring:** Force enable the send button and ensure UI is updated...

---

### `ui\tabs\chat_tab\chat_tab.py.get_ai_name`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 829
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the AI name based on current personality...

---

### `ui\tabs\chat_tab\chat_tab.py.get_current_model`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 869
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected model...

---

### `ui\tabs\chat_tab\chat_tab.py.get_current_personality`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 865
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality...

---

### `ui\tabs\chat_tab\chat_tab.py.get_current_response`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 877
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the current streaming response...

---

### `ui\tabs\chat_tab\chat_tab.py.get_streaming_handler`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1354
- **Arguments:** self
- **Docstring:** Get the streaming handler for backward compatibility...

---

### `ui\tabs\chat_tab\chat_tab.py.get_temperature`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 873
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get the current temperature setting...

---

### `ui\tabs\chat_tab\chat_tab.py.load_conversation`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1227
- **Arguments:** self, filepath
- **Docstring:** Load a conversation from file...

---

### `ui\tabs\chat_tab\chat_tab.py.on_audio_level_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 766
- **Arguments:** self, audio_level
- **Docstring:** Handle audio level changes with throttling to prevent excessive processing...

---

### `ui\tabs\chat_tab\chat_tab.py.on_eq_bars_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 808
- **Arguments:** self, bar_values
- **Docstring:** Handle EQ bar array changes and update the EQ visualizer directly...

---

### `ui\tabs\chat_tab\chat_tab.py.on_eq_mode_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 533
- **Arguments:** self, mode
- **Docstring:** Handle EQ mode change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_eq_visualizer_changed_from_voice_controls`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1199
- **Arguments:** self, eq_mode
- **Docstring:** Handle EQ visualizer changes from voice controls...

---

### `ui\tabs\chat_tab\chat_tab.py.on_eq_visualizer_changed_immediate`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1182
- **Arguments:** self, eq_mode
- **Docstring:** Handle immediate EQ visualizer changes from the settings dialog...

---

### `ui\tabs\chat_tab\chat_tab.py.on_input_mode_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 446
- **Arguments:** self, mode
- **Docstring:** Handle input mode change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_message_cancelled`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 341
- **Arguments:** self
- **Docstring:** Handle message cancelled from input controls...

---

### `ui\tabs\chat_tab\chat_tab.py.on_message_edited`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 823
- **Arguments:** self, message_index, new_content
- **Docstring:** Handle message edit...

---

### `ui\tabs\chat_tab\chat_tab.py.on_message_sent`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 309
- **Arguments:** self, message
- **Docstring:** Handle message sent (text or voice)...

---

### `ui\tabs\chat_tab\chat_tab.py.on_model_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 528
- **Arguments:** self, model_name
- **Docstring:** Handle model change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_personality_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 523
- **Arguments:** self, personality_name
- **Docstring:** Handle personality change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_recording_error`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 742
- **Arguments:** self, error
- **Docstring:** Handle recording error...

---

### `ui\tabs\chat_tab\chat_tab.py.on_recording_started`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 728
- **Arguments:** self
- **Docstring:** Handle recording started...

---

### `ui\tabs\chat_tab\chat_tab.py.on_recording_stopped`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 735
- **Arguments:** self
- **Docstring:** Handle recording stopped...

---

### `ui\tabs\chat_tab\chat_tab.py.on_request_cancelled`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 559
- **Arguments:** self
- **Docstring:** Handle request cancellation...

---

### `ui\tabs\chat_tab\chat_tab.py.on_temperature_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 518
- **Arguments:** self, temperature
- **Docstring:** Handle temperature change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_tts_error`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 718
- **Arguments:** self, error
- **Docstring:** Handle TTS error...

---

### `ui\tabs\chat_tab\chat_tab.py.on_tts_finished`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 677
- **Arguments:** self
- **Docstring:** Handle TTS finished...

---

### `ui\tabs\chat_tab\chat_tab.py.on_tts_started`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 664
- **Arguments:** self
- **Docstring:** Handle TTS started...

---

### `ui\tabs\chat_tab\chat_tab.py.on_user_interrupted`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 542
- **Arguments:** self
- **Docstring:** Handle user interruption during AI response...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_input_error`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 654
- **Arguments:** self, error
- **Docstring:** Handle voice input error...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_input_received`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 576
- **Arguments:** self, text

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_input_received_direct`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 598
- **Arguments:** self, text
- **Docstring:** Handle voice input received directly from voice service (fallback)...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_processing_finished`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 759
- **Arguments:** self
- **Docstring:** Handle voice processing finished...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_processing_started`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 752
- **Arguments:** self
- **Docstring:** Handle voice processing started...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_settings_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1216
- **Arguments:** self, settings
- **Docstring:** Handle voice settings changes...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_status_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 438
- **Arguments:** self, status
- **Docstring:** Update the audio level label or status indicator with the current voice service status...

---

### `ui\tabs\chat_tab\chat_tab.py.open_voice_settings`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1133
- **Arguments:** self
- **Docstring:** Open voice settings dialog...

---

### `ui\tabs\chat_tab\chat_tab.py.process_voice_input`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 621
- **Arguments:** self, text
- **Docstring:** Process voice input as a user message...

---

### `ui\tabs\chat_tab\chat_tab.py.refresh_navigation`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1323
- **Arguments:** self
- **Docstring:** Refresh the navigation widget...

---

### `ui\tabs\chat_tab\chat_tab.py.safe_disconnect`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 24
- **Arguments:** signal, slot, logger

---

### `ui\tabs\chat_tab\chat_tab.py.set_chat_controller`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1333
- **Arguments:** self, chat_controller
- **Docstring:** Set the chat controller reference...

---

### `ui\tabs\chat_tab\chat_tab.py.set_current_conversation_file`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1328
- **Arguments:** self, filepath
- **Docstring:** Set the current conversation file in the navigation widget...

---

### `ui\tabs\chat_tab\chat_tab.py.setup_components`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 81
- **Arguments:** self
- **Docstring:** Initialize all modular components...

---

### `ui\tabs\chat_tab\chat_tab.py.setup_connections`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 260
- **Arguments:** self
- **Docstring:** Setup signal connections between components...

---

### `ui\tabs\chat_tab\chat_tab.py.setup_ui`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 100
- **Arguments:** self
- **Docstring:** Setup the chat interface UI...

---

### `ui\tabs\chat_tab\chat_tab.py.speak_ai_response`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1110
- **Arguments:** self, text
- **Docstring:** Speak AI response using TTS...

---

### `ui\tabs\chat_tab\chat_tab.py.start_streaming`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 983
- **Arguments:** self
- **Docstring:** Start streaming state...

---

### `ui\tabs\chat_tab\chat_tab.py.stop_streaming`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1035
- **Arguments:** self
- **Docstring:** Stop streaming state...

---

### `ui\tabs\chat_tab\chat_tab.py.streaming_handler`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1359
- **Arguments:** self
- **Decorators:** property
- **Docstring:** Property to access streaming handler for backward compatibility...

---

### `ui\tabs\chat_tab\chat_tab.py.update_model_list`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1102
- **Arguments:** self, models
- **Docstring:** Update the model combo box with available models...

---

### `ui\tabs\chat_tab\chat_tab.py.update_personality_list`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 1106
- **Arguments:** self, personalities
- **Docstring:** Update the personality combo box with available personalities...

---

### `ui\tabs\chat_tab\eq_visualizer.py.__init__`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 25
- **Arguments:** self, parent

---

### `ui\tabs\chat_tab\eq_visualizer.py._update_eq_widget_safe`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 378
- **Arguments:** self, bar_values
- **Docstring:** Update the EQ widget safely in the main thread...

---

### `ui\tabs\chat_tab\eq_visualizer.py.get_available_eq_modes`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 409
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get list of available EQ visualizer modes...

---

### `ui\tabs\chat_tab\eq_visualizer.py.get_eq_mode`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 405
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the current EQ visualizer mode...

---

### `ui\tabs\chat_tab\eq_visualizer.py.is_eq_visualizer_active`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 391
- **Arguments:** self, voice_mode, tts_playing
- **Docstring:** Check if EQ visualizer should be active...

---

### `ui\tabs\chat_tab\eq_visualizer.py.setup_eq_visualizers`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 37
- **Arguments:** self
- **Docstring:** Initialize EQ visualizer widgets...

---

### `ui\tabs\chat_tab\eq_visualizer.py.switch_to_chat_display`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 152
- **Arguments:** self, chat_display
- **Docstring:** Switch back to chat display mode...

---

### `ui\tabs\chat_tab\eq_visualizer.py.switch_to_eq_visualizer`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 51
- **Arguments:** self, chat_display, voice_mode
- **Docstring:** Switch the chat display to EQ visualizer mode...

---

### `ui\tabs\chat_tab\eq_visualizer.py.update_eq_visualizer`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 247
- **Arguments:** self, audio_level, tts_playing
- **Docstring:** Update the EQ visualizer with audio level data....

---

### `ui\tabs\chat_tab\eq_visualizer.py.update_eq_visualizer_mode`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 397
- **Arguments:** self, mode
- **Docstring:** Update the EQ visualizer mode...

---

### `ui\tabs\chat_tab\input_controls.py.__init__`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 23
- **Arguments:** self, parent

---

### `ui\tabs\chat_tab\input_controls.py.cancel_message`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 286
- **Arguments:** self
- **Docstring:** Cancel the current message...

---

### `ui\tabs\chat_tab\input_controls.py.eventFilter`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 413
- **Arguments:** self, obj, event
- **Docstring:** Handle key events in message input...

---

### `ui\tabs\chat_tab\input_controls.py.force_enable_send_button`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 340
- **Arguments:** self
- **Docstring:** Force enable the send button and ensure UI is updated...

---

### `ui\tabs\chat_tab\input_controls.py.get_current_model`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 383
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected model...

---

### `ui\tabs\chat_tab\input_controls.py.get_current_personality`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 395
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality...

---

### `ui\tabs\chat_tab\input_controls.py.get_current_response`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 391
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the current streaming response...

---

### `ui\tabs\chat_tab\input_controls.py.get_temperature`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 387
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get the current temperature setting...

---

### `ui\tabs\chat_tab\input_controls.py.get_ui_components`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 399
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get UI components for integration with parent...

---

### `ui\tabs\chat_tab\input_controls.py.on_model_changed`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 260
- **Arguments:** self, model_name
- **Docstring:** Handle model combo box change...

---

### `ui\tabs\chat_tab\input_controls.py.on_personality_combo_changed`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 254
- **Arguments:** self, personality_name
- **Docstring:** Handle personality combo box change...

---

### `ui\tabs\chat_tab\input_controls.py.on_temperature_changed`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 247
- **Arguments:** self, value
- **Docstring:** Handle temperature slider value change...

---

### `ui\tabs\chat_tab\input_controls.py.send_message`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 265
- **Arguments:** self
- **Docstring:** Send the current message...

---

### `ui\tabs\chat_tab\input_controls.py.set_input_mode`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 228
- **Arguments:** self, mode
- **Docstring:** Set the input mode (Chat or Voice)...

---

### `ui\tabs\chat_tab\input_controls.py.setup_connections`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 210
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\tabs\chat_tab\input_controls.py.setup_ui_components`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 38
- **Arguments:** self
- **Docstring:** Setup UI components for input controls...

---

### `ui\tabs\chat_tab\input_controls.py.start_streaming`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 291
- **Arguments:** self
- **Docstring:** Start streaming state...

---

### `ui\tabs\chat_tab\input_controls.py.stop_streaming`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 314
- **Arguments:** self
- **Docstring:** Stop streaming state...

---

### `ui\tabs\chat_tab\input_controls.py.update_model_list`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 360
- **Arguments:** self, models
- **Docstring:** Update the model combo box with available models, always including 'Auto' as the first option...

---

### `ui\tabs\chat_tab\input_controls.py.update_personality_list`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 372
- **Arguments:** self, personalities
- **Docstring:** Update the personality combo box with available personalities...

---

### `ui\tabs\chat_tab\voice_controls.py.__del__`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1716
- **Arguments:** self
- **Docstring:** Destructor to ensure cleanup...

---

### `ui\tabs\chat_tab\voice_controls.py.__init__`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 60
- **Arguments:** self, parent, config_manager

---

### `ui\tabs\chat_tab\voice_controls.py._attempt_recovery`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 335
- **Arguments:** self
- **Docstring:** Attempt to recover voice service...

---

### `ui\tabs\chat_tab\voice_controls.py._clear_last_voice_input`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1632
- **Arguments:** self
- **Docstring:** Clear the last processed voice input to allow reprocessing...

---

### `ui\tabs\chat_tab\voice_controls.py._disable_voice_features`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 379
- **Arguments:** self
- **Docstring:** Disable voice features after failed recovery...

---

### `ui\tabs\chat_tab\voice_controls.py._disconnect_voice_signals`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 732
- **Arguments:** self
- **Docstring:** Disconnect voice service signals with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_recording_error_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1290
- **Arguments:** self, error
- **Docstring:** Handle recording error safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_recording_started_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1237
- **Arguments:** self
- **Docstring:** Handle recording started safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_recording_stopped_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1267
- **Arguments:** self
- **Docstring:** Handle recording stopped safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_service_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 392
- **Arguments:** self, error
- **Docstring:** Handle service errors with exponential backoff...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_tts_error_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1225
- **Arguments:** self, error
- **Docstring:** Handle TTS error safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_tts_finished_continuous`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1075
- **Arguments:** self
- **Docstring:** Handle TTS finished in continuous voice mode...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_voice_crash`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 322
- **Arguments:** self
- **Docstring:** Handle voice service crashes gracefully...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_voice_input_error_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1151
- **Arguments:** self, error
- **Docstring:** Handle voice input error safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_voice_input_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1004
- **Arguments:** self, text
- **Docstring:** Handle voice input safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._initialize_voice_service_manager`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 414
- **Arguments:** self
- **Docstring:** Initialize the voice service manager...

---

### `ui\tabs\chat_tab\voice_controls.py._is_similar_voice_input`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1645
- **Arguments:** self, text1, text2
- **Returns:** bool
- **Docstring:** Check if two voice inputs are similar enough to be considered duplicates...

---

### `ui\tabs\chat_tab\voice_controls.py._is_voice_service_ready`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 778
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice service is ready to use...

---

### `ui\tabs\chat_tab\voice_controls.py._on_audio_level_changed`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1878
- **Arguments:** self, level
- **Docstring:** Handle audio level changes with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_direct_voice_service_ready`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 550
- **Arguments:** self
- **Docstring:** Handle direct voice service ready signal (from VoiceService)...

---

### `ui\tabs\chat_tab\voice_controls.py._on_eq_bars_changed`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1891
- **Arguments:** self, bars
- **Docstring:** Handle EQ bars changes with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_recording_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1856
- **Arguments:** self, error
- **Docstring:** Handle recording error with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_recording_started`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1820
- **Arguments:** self
- **Docstring:** Handle recording started with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_recording_stopped`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1838
- **Arguments:** self
- **Docstring:** Handle recording stopped with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_tts_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1799
- **Arguments:** self, error
- **Docstring:** Handle TTS error with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_tts_finished`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1781
- **Arguments:** self
- **Docstring:** Handle TTS finished with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_tts_started`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1763
- **Arguments:** self
- **Docstring:** Handle TTS started with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_voice_input_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1744
- **Arguments:** self, error
- **Docstring:** Handle voice input error with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_voice_input_received`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1723
- **Arguments:** self, text
- **Docstring:** Handle voice input received with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._on_voice_service_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 586
- **Arguments:** self, error
- **Docstring:** Handle voice service error signal...

---

### `ui\tabs\chat_tab\voice_controls.py._on_voice_service_initializing`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 596
- **Arguments:** self
- **Docstring:** Handle voice service initializing signal...

---

### `ui\tabs\chat_tab\voice_controls.py._on_voice_service_ready`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 522
- **Arguments:** self
- **Docstring:** Handle voice service ready signal...

---

### `ui\tabs\chat_tab\voice_controls.py._on_voice_status_changed`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1904
- **Arguments:** self, status
- **Docstring:** Handle voice status changes with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._periodic_ui_refresh`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 565
- **Arguments:** self
- **Docstring:** Periodically check and update UI state...

---

### `ui\tabs\chat_tab\voice_controls.py._reinitialize_voice_service`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 368
- **Arguments:** self
- **Docstring:** Reinitialize voice service (for recovery)...

---

### `ui\tabs\chat_tab\voice_controls.py._reset_duplicate_detection_state`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1677
- **Arguments:** self
- **Docstring:** Reset the duplicate detection state for voice input....

---

### `ui\tabs\chat_tab\voice_controls.py._reset_error_count`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 388
- **Arguments:** self
- **Docstring:** Reset error count after timeout...

---

### `ui\tabs\chat_tab\voice_controls.py._reset_voice_button`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1101
- **Arguments:** self
- **Docstring:** Reset voice button to initial state...

---

### `ui\tabs\chat_tab\voice_controls.py._reset_voice_ui`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 357
- **Arguments:** self
- **Docstring:** Reset voice UI to safe state...

---

### `ui\tabs\chat_tab\voice_controls.py._restart_voice_input`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1086
- **Arguments:** self
- **Docstring:** Restart voice input for continuous mode...

---

### `ui\tabs\chat_tab\voice_controls.py._restart_voice_input_after_cancellation`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1617
- **Arguments:** self
- **Docstring:** Restart voice input after request cancellation...

---

### `ui\tabs\chat_tab\voice_controls.py._restart_voice_input_after_interruption`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1602
- **Arguments:** self
- **Docstring:** Restart voice input after user interruption...

---

### `ui\tabs\chat_tab\voice_controls.py._setup_voice_connections`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 630
- **Arguments:** self
- **Docstring:** Setup voice service signal connections with comprehensive error handling...

---

### `ui\tabs\chat_tab\voice_controls.py._start_continuous_voice_mode`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 952
- **Arguments:** self
- **Docstring:** Start continuous voice mode cycle...

---

### `ui\tabs\chat_tab\voice_controls.py._stop_all_voice_operations`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 345
- **Arguments:** self
- **Docstring:** Stop all voice operations safely...

---

### `ui\tabs\chat_tab\voice_controls.py._update_audio_level_ui_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1356
- **Arguments:** self, audio_level
- **Docstring:** Update audio level UI safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._update_eq_bars`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1577
- **Arguments:** self, audio_level
- **Docstring:** Update EQ bars based on audio level...

---

### `ui\tabs\chat_tab\voice_controls.py._update_voice_button_state`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 245
- **Arguments:** self, enabled, status
- **Docstring:** Update the voice button state based on voice service status...

---

### `ui\tabs\chat_tab\voice_controls.py._update_voice_state`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 312
- **Arguments:** self, key, value
- **Docstring:** Thread-safe voice state update...

---

### `ui\tabs\chat_tab\voice_controls.py._validate_voice_service_capabilities`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 803
- **Arguments:** self, voice_service
- **Docstring:** Validate that the voice service has the required methods...

---

### `ui\tabs\chat_tab\voice_controls.py.can_handle_interruption`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1512
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if the system can handle user interruptions...

---

### `ui\tabs\chat_tab\voice_controls.py.cleanup`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1690
- **Arguments:** self
- **Docstring:** Clean up voice controls and disconnect all signals...

---

### `ui\tabs\chat_tab\voice_controls.py.force_reinitialize_voice_service`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1487
- **Arguments:** self
- **Docstring:** Force reinitialization of the voice service...

---

### `ui\tabs\chat_tab\voice_controls.py.force_ui_refresh`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 492
- **Arguments:** self
- **Docstring:** Force UI refresh to update button state based on current voice service status...

---

### `ui\tabs\chat_tab\voice_controls.py.get_interruption_threshold`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1523
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get the audio level threshold for interruption detection...

---

### `ui\tabs\chat_tab\voice_controls.py.get_ui_components`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1534
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get UI components for integration with parent...

---

### `ui\tabs\chat_tab\voice_controls.py.get_voice_service`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 606
- **Arguments:** self
- **Docstring:** Get voice service with lazy loading...

---

### `ui\tabs\chat_tab\voice_controls.py.get_voice_service_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1481
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the last voice service error...

---

### `ui\tabs\chat_tab\voice_controls.py.get_voice_settings`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1451
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get current voice settings...

---

### `ui\tabs\chat_tab\voice_controls.py.is_tts_playing`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1501
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if TTS is currently playing...

---

### `ui\tabs\chat_tab\voice_controls.py.is_voice_busy`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 317
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Thread-safe check if voice is busy...

---

### `ui\tabs\chat_tab\voice_controls.py.is_voice_mode_active`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1497
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice mode is active...

---

### `ui\tabs\chat_tab\voice_controls.py.is_voice_service_initializing`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1471
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice service is initializing...

---

### `ui\tabs\chat_tab\voice_controls.py.is_voice_service_ready`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1461
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice service is ready...

---

### `ui\tabs\chat_tab\voice_controls.py.on_audio_level_changed`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1319
- **Arguments:** self, audio_level
- **Docstring:** Handle audio level changes with throttling to prevent excessive processing...

---

### `ui\tabs\chat_tab\voice_controls.py.on_eq_bars_changed`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1573
- **Arguments:** self, bar_values
- **Docstring:** Handle EQ bar array changes from the voice service and forward to parent (chat tab)...

---

### `ui\tabs\chat_tab\voice_controls.py.on_recording_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1282
- **Arguments:** self, error
- **Docstring:** Handle recording error...

---

### `ui\tabs\chat_tab\voice_controls.py.on_recording_started`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1229
- **Arguments:** self
- **Docstring:** Handle recording started...

---

### `ui\tabs\chat_tab\voice_controls.py.on_recording_stopped`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1259
- **Arguments:** self
- **Docstring:** Handle recording stopped...

---

### `ui\tabs\chat_tab\voice_controls.py.on_request_cancelled`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1557
- **Arguments:** self
- **Docstring:** Handle request cancellation...

---

### `ui\tabs\chat_tab\voice_controls.py.on_tts_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1209
- **Arguments:** self, error
- **Docstring:** Handle TTS error...

---

### `ui\tabs\chat_tab\voice_controls.py.on_tts_finished`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1192
- **Arguments:** self
- **Docstring:** Handle TTS finished...

---

### `ui\tabs\chat_tab\voice_controls.py.on_tts_started`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1181
- **Arguments:** self
- **Docstring:** Handle TTS started...

---

### `ui\tabs\chat_tab\voice_controls.py.on_user_interrupted`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1542
- **Arguments:** self
- **Docstring:** Handle user interruption during AI response...

---

### `ui\tabs\chat_tab\voice_controls.py.on_voice_input_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1136
- **Arguments:** self, error
- **Docstring:** Handle voice input error...

---

### `ui\tabs\chat_tab\voice_controls.py.on_voice_input_received`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1123
- **Arguments:** self, text
- **Docstring:** Handle voice input received...

---

### `ui\tabs\chat_tab\voice_controls.py.on_voice_processing_finished`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1313
- **Arguments:** self
- **Docstring:** Handle voice processing finished...

---

### `ui\tabs\chat_tab\voice_controls.py.on_voice_processing_started`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1306
- **Arguments:** self
- **Docstring:** Handle voice processing started...

---

### `ui\tabs\chat_tab\voice_controls.py.reset_voice_service`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 825
- **Arguments:** self
- **Docstring:** Force reset the voice service to clear stuck states...

---

### `ui\tabs\chat_tab\voice_controls.py.reset_voice_signal_connections`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 774
- **Arguments:** self
- **Docstring:** Reset the internal guard flag to allow reconnection if needed (e.g., after re-init)....

---

### `ui\tabs\chat_tab\voice_controls.py.safe_disconnect`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 17
- **Arguments:** signal, slot, logger

---

### `ui\tabs\chat_tab\voice_controls.py.setup_connections`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 406
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\tabs\chat_tab\voice_controls.py.setup_ui_components`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 138
- **Arguments:** self
- **Docstring:** Setup UI components for voice controls...

---

### `ui\tabs\chat_tab\voice_controls.py.speak_ai_response`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1417
- **Arguments:** self, text
- **Docstring:** Speak AI response using TTS...

---

### `ui\tabs\chat_tab\voice_controls.py.toggle_voice_mode`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 856
- **Arguments:** self
- **Docstring:** Toggle voice mode on/off with proper cleanup...

---

### `ui\tabs\chat_tab\voice_controls.py.update_voice_settings`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1435
- **Arguments:** self, settings
- **Docstring:** Update voice settings...

---

### `ui\tabs\chat_tab\voice_controls.py.update_voice_status`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 1920
- **Arguments:** self, status
- **Docstring:** Update voice status with comprehensive error handling...

---

### `ui\tabs\memory_tab.py.__init__`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 34
- **Arguments:** self, memory_service

---

### `ui\tabs\memory_tab.py._summarize_with_service`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 502
- **Arguments:** self
- **Docstring:** Summarize the current conversation using the conversation service...

---

### `ui\tabs\memory_tab.py.cleanup_memory_entries`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 536
- **Arguments:** self
- **Docstring:** Clean up duplicate and conflicting memory entries...

---

### `ui\tabs\memory_tab.py.clear_all_memories`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 523
- **Arguments:** self
- **Docstring:** Clear all memories...

---

### `ui\tabs\memory_tab.py.create_memories_tab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 187
- **Arguments:** self
- **Docstring:** Create the memories management tab...

---

### `ui\tabs\memory_tab.py.create_overview_tab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 127
- **Arguments:** self
- **Docstring:** Create the memory overview tab...

---

### `ui\tabs\memory_tab.py.create_settings_tab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 67
- **Arguments:** self
- **Docstring:** Create the memory settings tab...

---

### `ui\tabs\memory_tab.py.create_summaries_tab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 252
- **Arguments:** self
- **Docstring:** Create the summaries management tab...

---

### `ui\tabs\memory_tab.py.delete_selected_memory`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 552
- **Arguments:** self
- **Docstring:** Delete the selected memory...

---

### `ui\tabs\memory_tab.py.refresh_data`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 311
- **Arguments:** self
- **Docstring:** Refresh all data displays...

---

### `ui\tabs\memory_tab.py.refresh_memories`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 373
- **Arguments:** self
- **Docstring:** Refresh the memories table based on STM/LTM filter...

---

### `ui\tabs\memory_tab.py.refresh_overview`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 317
- **Arguments:** self
- **Docstring:** Refresh the overview tab data...

---

### `ui\tabs\memory_tab.py.refresh_summaries`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 404
- **Arguments:** self
- **Docstring:** Refresh the summaries list...

---

### `ui\tabs\memory_tab.py.safe_disconnect`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 14
- **Arguments:** signal, slot, logger

---

### `ui\tabs\memory_tab.py.search_memories`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 417
- **Arguments:** self
- **Docstring:** Search memories based on input...

---

### `ui\tabs\memory_tab.py.set_conversation_service`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 495
- **Arguments:** self, conversation_service
- **Docstring:** Set the conversation service for summarization...

---

### `ui\tabs\memory_tab.py.setup_connections`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 282
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\tabs\memory_tab.py.setup_ui`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 41
- **Arguments:** self
- **Docstring:** Setup the memory tab UI...

---

### `ui\tabs\memory_tab.py.show_memory_details`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 439
- **Arguments:** self
- **Docstring:** Show details for selected memory...

---

### `ui\tabs\memory_tab.py.show_summary_details`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 473
- **Arguments:** self
- **Docstring:** Show details for selected summary...

---

### `ui\tabs\memory_tab.py.summarize_current_conversation`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 489
- **Arguments:** self
- **Docstring:** Summarize the current conversation...

---

### `ui\tabs\memory_tab.py.update_context_messages`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 306
- **Arguments:** self, value
- **Docstring:** Update the maximum context messages...

---

### `ui\tabs\model_tab.py.__init__`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 15
- **Arguments:** self, parent

---

### `ui\tabs\model_tab.py.append_status`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 461
- **Arguments:** self, message
- **Docstring:** Append a status message to the status text area...

---

### `ui\tabs\model_tab.py.clear_status`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 498
- **Arguments:** self
- **Docstring:** Clear the status text area...

---

### `ui\tabs\model_tab.py.get_current_time`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 470
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get current time as string...

---

### `ui\tabs\model_tab.py.get_selected_model`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 493
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected model...

---

### `ui\tabs\model_tab.py.on_model_selection_changed`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 437
- **Arguments:** self
- **Docstring:** Handle model selection change...

---

### `ui\tabs\model_tab.py.on_operation_error`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 487
- **Arguments:** self, error
- **Docstring:** Handle operation errors...

---

### `ui\tabs\model_tab.py.on_operation_finished`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 479
- **Arguments:** self, operation
- **Docstring:** Handle operation completion...

---

### `ui\tabs\model_tab.py.on_operation_progress`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 475
- **Arguments:** self, message
- **Docstring:** Handle operation progress updates...

---

### `ui\tabs\model_tab.py.pull_model`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 379
- **Arguments:** self
- **Docstring:** Pull a new model...

---

### `ui\tabs\model_tab.py.refresh_models`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 361
- **Arguments:** self
- **Docstring:** Refresh the list of available models...

---

### `ui\tabs\model_tab.py.remove_selected_model`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 397
- **Arguments:** self
- **Docstring:** Remove the selected model...

---

### `ui\tabs\model_tab.py.setup_connections`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 351
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\tabs\model_tab.py.setup_model_list`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 55
- **Arguments:** self, parent
- **Docstring:** Setup the model list area...

---

### `ui\tabs\model_tab.py.setup_operations`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 131
- **Arguments:** self, parent
- **Docstring:** Setup the operations area...

---

### `ui\tabs\model_tab.py.setup_ui`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 38
- **Arguments:** self
- **Docstring:** Setup the model management UI...

---

### `ui\tabs\model_tab.py.start_operation`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 444
- **Arguments:** self
- **Docstring:** Start an operation (disable UI elements)...

---

### `ui\tabs\model_tab.py.stop_operation`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 453
- **Arguments:** self
- **Docstring:** Stop an operation (enable UI elements)...

---

### `ui\tabs\model_tab.py.update_model_list`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 369
- **Arguments:** self, models
- **Docstring:** Update the model list display...

---

### `ui\tabs\model_tab.py.update_selected_model`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 417
- **Arguments:** self
- **Docstring:** Update the selected model...

---

### `ui\tabs\personality_tab.py.__init__`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 18
- **Arguments:** self, parent

---

### `ui\tabs\personality_tab.py.clear_creation_form`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 923
- **Arguments:** self
- **Docstring:** Clear the personality creation form...

---

### `ui\tabs\personality_tab.py.create_personality`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 809
- **Arguments:** self
- **Docstring:** Create a new personality...

---

### `ui\tabs\personality_tab.py.delete_custom_personality`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 965
- **Arguments:** self
- **Docstring:** Delete the selected custom personality...

---

### `ui\tabs\personality_tab.py.export_personality`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 998
- **Arguments:** self
- **Docstring:** Export the selected personality to a file...

---

### `ui\tabs\personality_tab.py.get_available_personalities`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 1043
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get list of available personality names...

---

### `ui\tabs\personality_tab.py.get_context_prompt`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 1078
- **Arguments:** self
- **Docstring:** Get the context prompt from the form...

---

### `ui\tabs\personality_tab.py.get_current_personality`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 1028
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality name...

---

### `ui\tabs\personality_tab.py.get_system_prompt`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 1032
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the system prompt for the current personality...

---

### `ui\tabs\personality_tab.py.get_user_prompt_template`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 1067
- **Arguments:** self
- **Docstring:** Get the user prompt template from the form...

---

### `ui\tabs\personality_tab.py.load_personalities`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 684
- **Arguments:** self
- **Docstring:** Load available personalities into the combo box and lists...

---

### `ui\tabs\personality_tab.py.on_context_template_changed`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 1059
- **Arguments:** self, text
- **Docstring:** Handle context template selection...

---

### `ui\tabs\personality_tab.py.on_conversation_style_changed`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 1051
- **Arguments:** self, text
- **Docstring:** Handle conversation style template selection...

---

### `ui\tabs\personality_tab.py.on_custom_personality_selected`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 774
- **Arguments:** self, item
- **Docstring:** Handle custom personality selection...

---

### `ui\tabs\personality_tab.py.on_personality_changed`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 780
- **Arguments:** self, personality_name
- **Docstring:** Handle personality selection change...

---

### `ui\tabs\personality_tab.py.on_system_personality_selected`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 747
- **Arguments:** self, item
- **Docstring:** Handle system personality selection...

---

### `ui\tabs\personality_tab.py.refresh_personalities`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 1019
- **Arguments:** self
- **Docstring:** Refresh personalities from disk...

---

### `ui\tabs\personality_tab.py.setup_creation_tab`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 192
- **Arguments:** self
- **Docstring:** Setup the personality creation tab...

---

### `ui\tabs\personality_tab.py.setup_management_tab`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 511
- **Arguments:** self
- **Docstring:** Setup the personality management tab...

---

### `ui\tabs\personality_tab.py.setup_selection_tab`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 85
- **Arguments:** self
- **Docstring:** Setup the personality selection tab...

---

### `ui\tabs\personality_tab.py.setup_ui`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 25
- **Arguments:** self
- **Docstring:** Setup the personality management UI...

---

### `ui\tabs\personality_tab.py.update_custom_personalities_list`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 736
- **Arguments:** self
- **Docstring:** Update the custom personalities list...

---

### `ui\tabs\personality_tab.py.update_personality_info`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 786
- **Arguments:** self, personality_name
- **Docstring:** Update the personality info display...

---

### `ui\tabs\personality_tab.py.update_system_personalities_list`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 724
- **Arguments:** self
- **Docstring:** Update the system personalities list...

---

### `ui\tabs\personality_tab.py.update_system_personality_info`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 753
- **Arguments:** self, personality_name
- **Docstring:** Update the system personality info display...

---

### `ui\tabs\tab_styles.py.get_tab_style`

- **File:** `ui\tabs\tab_styles.py`
- **Line:** 40
- **Arguments:** 
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Get the tab widget style...

---

### `ui\themes\message_formatter.py._protect_code_blocks`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 133
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Helper function to protect code blocks from processing...

---

### `ui\themes\message_formatter.py.cleanup_message`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 250
- **Arguments:** sender, message, is_code
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Prepares a message for display by adding sender and formatting....

---

### `ui\themes\message_formatter.py.detect_and_format_code`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 97
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Detects code and applies formatting. Highlights syntax using Pygments.
It handles inline and block c...

---

### `ui\themes\message_formatter.py.detect_code_in_message`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 19
- **Arguments:** message
- **Returns:** bool
- **Decorators:** staticmethod
- **Docstring:** Detect if a message contains code blocks or inline code.
Returns True if code is detected, False oth...

---

### `ui\themes\message_formatter.py.detect_code_type`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 48
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Detects the programming language of a code block using Pygments....

---

### `ui\themes\message_formatter.py.format_block_code`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 107
- **Arguments:** match

---

### `ui\themes\message_formatter.py.format_chat_message`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 278
- **Arguments:** sender, message, is_code
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format a complete chat message with styling based on sender type....

---

### `ui\themes\message_formatter.py.format_markdown`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 149
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Enhanced markdown formatting for better AI output presentation.
Handles headers, lists, emphasis, an...

---

### `ui\themes\message_formatter.py.handle_html_tags`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 221
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Properly handle HTML tags in messages - escape them for display when they're part of discussions
but...

---

### `ui\themes\message_formatter.py.protect_code_blocks`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 137
- **Arguments:** match

---

### `ui\themes\message_formatter.py.split_thoughts_and_answer`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 315
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Splits a message into (thoughts, main_answer) if <think>...</think> is present.
Returns a tuple (tho...

---

### `ui\themes\message_formatter.py.syntax_highlight_code`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 60
- **Arguments:** message, language
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Highlight the code using Pygments and return formatted HTML....

---

### `ui\themes\message_formatter.py.to_plain_text`

- **File:** `ui\themes\message_formatter.py`
- **Line:** 331
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Convert a message with markdown, code, and HTML to plain text for TTS.
Removes formatting, code bloc...

---

### `ui\ui_manager.py.__init__`

- **File:** `ui\ui_manager.py`
- **Line:** 27
- **Arguments:** self, main_window, config_manager

---

### `ui\ui_manager.py.apply_theme`

- **File:** `ui\ui_manager.py`
- **Line:** 176
- **Arguments:** self, theme
- **Docstring:** Apply the specified theme...

---

### `ui\ui_manager.py.get_chat_tab`

- **File:** `ui\ui_manager.py`
- **Line:** 206
- **Arguments:** self
- **Docstring:** Get the chat tab...

---

### `ui\ui_manager.py.get_main_window`

- **File:** `ui\ui_manager.py`
- **Line:** 202
- **Arguments:** self
- **Docstring:** Get the main window...

---

### `ui\ui_manager.py.get_memory_tab`

- **File:** `ui\ui_manager.py`
- **Line:** 218
- **Arguments:** self
- **Docstring:** Get the memory tab...

---

### `ui\ui_manager.py.get_menu_action`

- **File:** `ui\ui_manager.py`
- **Line:** 198
- **Arguments:** self, action_name
- **Docstring:** Get a menu action by name...

---

### `ui\ui_manager.py.get_model_tab`

- **File:** `ui\ui_manager.py`
- **Line:** 210
- **Arguments:** self
- **Docstring:** Get the model tab...

---

### `ui\ui_manager.py.get_personality_tab`

- **File:** `ui\ui_manager.py`
- **Line:** 214
- **Arguments:** self
- **Docstring:** Get the personality tab...

---

### `ui\ui_manager.py.get_tabs`

- **File:** `ui\ui_manager.py`
- **Line:** 222
- **Arguments:** self
- **Docstring:** Get the tab widget...

---

### `ui\ui_manager.py.setup_menu_bar`

- **File:** `ui\ui_manager.py`
- **Line:** 95
- **Arguments:** self
- **Docstring:** Setup the menu bar with all actions...

---

### `ui\ui_manager.py.setup_ui`

- **File:** `ui\ui_manager.py`
- **Line:** 41
- **Arguments:** self, conversation_manager, summarization_service, memory_enabled, memory_service
- **Docstring:** Setup the main UI components...

---

### `ui\ui_manager.py.show_about_dialog`

- **File:** `ui\ui_manager.py`
- **Line:** 226
- **Arguments:** self
- **Docstring:** Show the about dialog...

---

### `ui\ui_manager.py.show_clear_chat_dialog`

- **File:** `ui\ui_manager.py`
- **Line:** 234
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Show clear chat confirmation dialog...

---

### `ui\ui_manager.py.update_status`

- **File:** `ui\ui_manager.py`
- **Line:** 189
- **Arguments:** self, message
- **Docstring:** Update status bar message...

---

### `ui\utils\message_utils.py.show_connection_error`

- **File:** `ui\utils\message_utils.py`
- **Line:** 43
- **Arguments:** service, error, parent
- **Docstring:** Show a connection error with copy functionality...

---

### `ui\utils\message_utils.py.show_critical_error`

- **File:** `ui\utils\message_utils.py`
- **Line:** 23
- **Arguments:** title, message, exception, parent
- **Docstring:** Show a critical error dialog with copy functionality and exception details...

---

### `ui\utils\message_utils.py.show_error`

- **File:** `ui\utils\message_utils.py`
- **Line:** 11
- **Arguments:** title, message, details, traceback_str, parent
- **Docstring:** Show an error dialog with copy functionality...

---

### `ui\utils\message_utils.py.show_file_error`

- **File:** `ui\utils\message_utils.py`
- **Line:** 52
- **Arguments:** operation, file_path, error, parent
- **Docstring:** Show a file operation error with copy functionality...

---

### `ui\utils\message_utils.py.show_operation_error`

- **File:** `ui\utils\message_utils.py`
- **Line:** 34
- **Arguments:** operation, error, parent
- **Docstring:** Show an operation error with copy functionality...

---

### `ui\utils\message_utils.py.show_validation_error`

- **File:** `ui\utils\message_utils.py`
- **Line:** 63
- **Arguments:** field, message, parent
- **Docstring:** Show a validation error with copy functionality...

---

### `ui\utils\message_utils.py.show_warning`

- **File:** `ui\utils\message_utils.py`
- **Line:** 15
- **Arguments:** title, message, details, parent
- **Docstring:** Show a warning dialog with copy functionality...

---

### `ui\visualizers\widgets\bar_eq_widget.py.__init__`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 23
- **Arguments:** self, parent, num_bars
- **Docstring:** Initialize the bar equalizer widget.

Args:
    parent: Parent widget
    num_bars: Number of freque...

---

### `ui\visualizers\widgets\bar_eq_widget.py._animate`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 53
- **Arguments:** self
- **Docstring:** Animate the bars by smoothly interpolating current values toward target values.
This method is calle...

---

### `ui\visualizers\widgets\bar_eq_widget.py._calculate_bar_geometry`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 129
- **Arguments:** self, widget_width, widget_height
- **Docstring:** Calculate bar dimensions and positioning.

Args:
    widget_width: Width of the widget
    widget_he...

---

### `ui\visualizers\widgets\bar_eq_widget.py._create_bar_gradient`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 158
- **Arguments:** self, x, y, width, height, is_reflection, bar_index
- **Docstring:** Create a gradient for a bar.

Args:
    x: X position of the bar
    y: Y position of the bar
    wi...

---

### `ui\visualizers\widgets\bar_eq_widget.py._draw_bar`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 212
- **Arguments:** self, painter, x, y, width, height, value, max_height, bar_index
- **Docstring:** Draw a single bar with its reflection.

Args:
    painter: QPainter instance
    x: X position of th...

---

### `ui\visualizers\widgets\bar_eq_widget.py._setup_animation_timer`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 47
- **Arguments:** self
- **Docstring:** Initialize and configure the animation timer....

---

### `ui\visualizers\widgets\bar_eq_widget.py.get_current_values`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 115
- **Arguments:** self
- **Docstring:** Get current bar values for debugging/monitoring.

Returns:
    dict: Current state information...

---

### `ui\visualizers\widgets\bar_eq_widget.py.paintEvent`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 241
- **Arguments:** self, event
- **Docstring:** Paint the bar equalizer widget.

Args:
    event: Paint event...

---

### `ui\visualizers\widgets\bar_eq_widget.py.set_eq_bars`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 66
- **Arguments:** self, values
- **Decorators:** Slot
- **Docstring:** Set the target values for the frequency bars.

Args:
    values: List of float values representing t...

---

### `ui\visualizers\widgets\bar_eq_widget.py.set_idle`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 102
- **Arguments:** self
- **Docstring:** Reset all bars to their idle state....

---

### `ui\visualizers\widgets\bar_eq_widget.py.start_animation`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 107
- **Arguments:** self
- **Docstring:** Start the animation timer....

---

### `ui\visualizers\widgets\bar_eq_widget.py.stop_animation`

- **File:** `ui\visualizers\widgets\bar_eq_widget.py`
- **Line:** 111
- **Arguments:** self
- **Docstring:** Stop the animation timer....

---

### `ui\visualizers\widgets\circle_eq_widget.py.__init__`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 22
- **Arguments:** self, parent, num_sections
- **Docstring:** Initialize the circular equalizer widget.

Args:
    parent: Parent widget
    num_sections: Number ...

---

### `ui\visualizers\widgets\circle_eq_widget.py._animate`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 52
- **Arguments:** self
- **Docstring:** Animate the sections by smoothly interpolating current values toward target values.
This method is c...

---

### `ui\visualizers\widgets\circle_eq_widget.py._create_section_gradient`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 129
- **Arguments:** self, center_x, center_y, inner_radius, outer_radius, angle_start, angle_span, value, section_index
- **Docstring:** Create a gradient for a circular section.

Args:
    center_x, center_y: Center of the circle
    in...

---

### `ui\visualizers\widgets\circle_eq_widget.py._setup_animation_timer`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 46
- **Arguments:** self
- **Docstring:** Initialize and configure the animation timer....

---

### `ui\visualizers\widgets\circle_eq_widget.py.get_current_values`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 115
- **Arguments:** self
- **Docstring:** Get current section values for debugging/monitoring.

Returns:
    dict: Current state information...

---

### `ui\visualizers\widgets\circle_eq_widget.py.paintEvent`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 169
- **Arguments:** self, event
- **Docstring:** Paint the circular equalizer widget.

Args:
    event: Paint event...

---

### `ui\visualizers\widgets\circle_eq_widget.py.set_eq_sections`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 66
- **Arguments:** self, values
- **Decorators:** Slot
- **Docstring:** Set the target values for the circular sections.

Args:
    values: List of float values representin...

---

### `ui\visualizers\widgets\circle_eq_widget.py.set_idle`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 102
- **Arguments:** self
- **Docstring:** Reset all sections to their idle state....

---

### `ui\visualizers\widgets\circle_eq_widget.py.start_animation`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 107
- **Arguments:** self
- **Docstring:** Start the animation timer....

---

### `ui\visualizers\widgets\circle_eq_widget.py.stop_animation`

- **File:** `ui\visualizers\widgets\circle_eq_widget.py`
- **Line:** 111
- **Arguments:** self
- **Docstring:** Stop the animation timer....

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 15
- **Arguments:** self, parent, num_points, color, alpha, radius_scale, radius_ratio, energy_mult

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py._animate`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 47
- **Arguments:** self

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py._smooth_radii`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 39
- **Arguments:** self, radii, window

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py.paintEvent`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 87
- **Arguments:** self, event

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py.set_idle`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 75
- **Arguments:** self

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py.set_net_radii`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 56
- **Arguments:** self, values
- **Decorators:** Slot

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py.start_animation`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 81
- **Arguments:** self

---

### `ui\visualizers\widgets\circular_gradient_eq_widget.py.stop_animation`

- **File:** `ui\visualizers\widgets\circular_gradient_eq_widget.py`
- **Line:** 84
- **Arguments:** self

---

### `ui\visualizers\widgets\circular_net_eq_widget.py.__init__`

- **File:** `ui\visualizers\widgets\circular_net_eq_widget.py`
- **Line:** 18
- **Arguments:** self, parent, num_points, color

---

### `ui\visualizers\widgets\circular_net_eq_widget.py._animate`

- **File:** `ui\visualizers\widgets\circular_net_eq_widget.py`
- **Line:** 39
- **Arguments:** self

---

### `ui\visualizers\widgets\circular_net_eq_widget.py.paintEvent`

- **File:** `ui\visualizers\widgets\circular_net_eq_widget.py`
- **Line:** 78
- **Arguments:** self, event

---

### `ui\visualizers\widgets\circular_net_eq_widget.py.set_idle`

- **File:** `ui\visualizers\widgets\circular_net_eq_widget.py`
- **Line:** 68
- **Arguments:** self

---

### `ui\visualizers\widgets\circular_net_eq_widget.py.set_net_radii`

- **File:** `ui\visualizers\widgets\circular_net_eq_widget.py`
- **Line:** 49
- **Arguments:** self, values
- **Decorators:** Slot

---

### `ui\visualizers\widgets\circular_net_eq_widget.py.start_animation`

- **File:** `ui\visualizers\widgets\circular_net_eq_widget.py`
- **Line:** 72
- **Arguments:** self

---

### `ui\visualizers\widgets\circular_net_eq_widget.py.stop_animation`

- **File:** `ui\visualizers\widgets\circular_net_eq_widget.py`
- **Line:** 75
- **Arguments:** self

---

## 🔗 Relationships

### `app\app_lifecycle.py`

- calls_function:core\logging\logger.py.format
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:config\config_manager.py.get

### `app\event_bus.py`

- calls_function:core\models\conversation_metadata.py.update_personality
- calls_method:core\utils\prompts.py.PromptFormatter.format_status_message
- calls_method:core\logging\helpers.py.LoggingHelpers.log_error
- calls_function:ui\tabs\memory_tab.py.safe_disconnect
- calls_function:ui\utils\message_utils.py.show_critical_error
- calls_function:ui\dialogs\voice_settings_dialog.py.safe_disconnect
- calls_function:core\models\conversation_metadata.py.update_model
- calls_method:core\logging\helpers.py.LoggingHelpers.log_debug
- calls_function:ui\tabs\chat_tab\chat_tab.py.safe_disconnect
- calls_function:core\utils\threading_utils.py.safe_disconnect
- calls_function:app\event_bus.py.safe_disconnect
- calls_function:core\shared_imports\pyside_imports.py.safe_ui_update
- calls_function:features\ollama\ollama_service.py.update_model
- calls_function:core\utils\threading_utils.py.safe_ui_update
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\threading_service.py.get_global_threading_service
- calls_function:ui\utils\message_utils.py.show_operation_error
- calls_function:ui\tabs\chat_tab\voice_controls.py.safe_disconnect

### `app\main.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\ollama\ollama_chat.py.showEvent
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:app\main.py.showEvent
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `app\service_manager.py`

- calls_function:features\voice\voice_service_manager.py.__new__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:features\voice\voice_service_manager.py.get_voice_service_manager
- calls_function:core\logging\logger.py.__new__
- calls_function:app\service_manager.py.__new__

### `app\threading_integration.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:core\threading\threading_service.py.get_global_threading_service
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `config\config_manager.py`

- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:config\config_manager.py.get

### `core\logging\helpers.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `core\logging\logger.py`

- calls_function:core\logging\logger.py.error
- calls_function:core\logging\logger.py.critical
- calls_function:core\logging\logger.py.warning
- calls_function:core\logging\logger.py._sanitize_filename
- calls_function:features\voice\voice_service_manager.py.__new__
- calls_function:config\config_manager.py.set
- calls_function:core\logging\logger.py.strip_emojis
- calls_function:core\logging\logger.py.debug
- calls_function:core\logging\logger.py.info
- calls_function:core\logging\logger.py.__new__
- calls_function:core\logging\logger.py.format
- calls_function:app\service_manager.py.__new__

### `core\logging\logger.py.PrintLogger`

- inherits_from:core\logging\logger.py.PrintOnLogMixin

### `core\models\conversation_metadata.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:config\config_manager.py.get
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_method:core\models\conversation_metadata.py.ConversationMetadata.from_dict
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `core\shared_imports\pyside_imports.py`

- calls_function:core\shared_imports\pyside_imports.py.is_main_thread
- calls_function:core\utils\threading_utils.py.is_main_thread

### `core\threading\__init__.py`

- calls_method:core\logging\logger.py.CustomLogger.get_logger

### `core\threading\persistent_thread_config.py`

- calls_function:core\threading\persistent_thread_config.py.validate_persistent_thread_config
- calls_function:core\threading\persistent_thread_config.py.get_persistent_thread_config
- calls_function:core\threading\persistent_thread_config.py.get_config_summary

### `core\threading\persistent_thread_pool.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:core\threading\thread_monitor.py.get_global_thread_monitor
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `core\threading\qrunnable_tasks.py`

- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:config\config_manager.py.set

### `core\threading\qthread_workers.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:config\config_manager.py.get
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:core\threading\qthread_workers.py.configure_streaming
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `core\threading\qthread_workers.py.AudioStreamingWorker`

- inherits_from:core\threading\qthread_workers.py.StreamingWorker

### `core\threading\qthread_workers.py.ChatStreamingWorker`

- inherits_from:core\threading\qthread_workers.py.StreamingWorker

### `core\threading\qthread_workers.py.MonitoringWorker`

- inherits_from:core\threading\qthread_workers.py.StreamingWorker

### `core\threading\thread_calculator.py`

- calls_function:core\threading\thread_calculator.py.analyze_system
- calls_method:core\logging\logger.py.CustomLogger.get_logger

### `core\threading\thread_calculator_examples.py`

- calls_function:startup\install_dependencies.py.main
- calls_function:core\threading\thread_calculator_examples.py.example_thread_pool_manager
- calls_function:core\threading\thread_calculator_examples.py.example_streaming_configuration
- calls_function:core\threading\thread_calculator_examples.py.example_persistent_thread_pool
- calls_function:core\threading\thread_calculator_examples.py.main
- calls_function:core\threading\thread_calculator.py.get_pool_thread_count
- calls_function:core\threading\thread_calculator_examples.py.example_memory_optimization
- calls_function:core\threading\thread_calculator.py.get_thread_recommendations
- calls_function:core\threading\thread_calculator_examples.py.example_dynamic_adjustment

### `core\threading\thread_monitor.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `core\threading\thread_pool_manager.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:core\threading\thread_calculator.py.get_pool_thread_count
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `core\threading\threading_service.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.get_global_persistent_thread_pool
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:core\threading\thread_calculator.py.get_pool_thread_count
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:core\threading\thread_pool_manager.py.get_global_thread_pool_manager
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:core\threading\thread_monitor.py.get_global_thread_monitor
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `core\threading\usage_examples.py`

- calls_function:core\threading\thread_monitor.py.get_global_thread_monitor
- calls_function:core\threading\thread_pool_manager.py.get_global_thread_pool_manager
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\usage_examples.py.demonstrate_threading_usage

### `core\utils\error_handler.py`

- calls_method:core\logging\helpers.py.LoggingHelpers.log_json_parsing_error
- calls_method:core\logging\helpers.py.LoggingHelpers.log_memory_operation
- calls_method:core\logging\helpers.py.LoggingHelpers.log_warning_with_context
- calls_method:core\logging\helpers.py.LoggingHelpers.log_audio_operation
- calls_method:core\logging\helpers.py.LoggingHelpers.log_ui_operation
- calls_method:core\logging\helpers.py.LoggingHelpers.log_file_operation
- calls_method:core\logging\helpers.py.LoggingHelpers.log_exception_with_context
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_method:core\logging\helpers.py.LoggingHelpers.log_performance_metric
- calls_method:core\logging\helpers.py.LoggingHelpers.log_network_request
- calls_method:core\logging\helpers.py.LoggingHelpers.log_critical_error

### `core\utils\internet_checker.py`

- calls_function:core\utils\internet_checker.py.is_online
- calls_function:core\utils\internet_checker.py.test_internet_connection
- calls_function:core\utils\internet_checker.py.test_internet_connection_detailed

### `core\utils\prompts.py`

- calls_function:core\logging\logger.py.format

### `core\utils\streaming_handler.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `core\utils\threading_audit.py`

- calls_function:core\utils\threading_audit.py.run_thread_safety_audit
- calls_method:core\logging\logger.py.CustomLogger.get_logger

### `core\utils\threading_utils.py`

- calls_function:core\utils\threading_utils.py.safe_widget_update
- calls_function:core\logging\logger.py.error
- calls_function:ui\tabs\memory_tab.py.safe_disconnect
- calls_function:core\utils\threading_utils.py.safe_connect_signal
- calls_function:core\shared_imports\pyside_imports.py.is_main_thread
- calls_function:ui\dialogs\voice_settings_dialog.py.safe_disconnect
- calls_function:ui\tabs\chat_tab\chat_tab.py.safe_disconnect
- calls_function:core\utils\threading_utils.py.safe_disconnect
- calls_function:app\event_bus.py.safe_disconnect
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\utils\threading_utils.py.is_main_thread
- calls_function:ui\tabs\chat_tab\voice_controls.py.safe_disconnect

### `features\chat\chat_controller.py`

- calls_function:core\threading\thread_calculator.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_fact_storage_start
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_method:core\utils\prompts.py.PromptFormatter.format_status_message
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_llm_call
- calls_method:core\logging\helpers.py.LoggingHelpers.log_memory_ltm_status
- calls_function:core\threading\thread_monitor.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_debug
- calls_function:app\app_lifecycle.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_message_sent_end
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_method:core\utils\prompts.py.PromptFormatter.format_error_message
- calls_method:core\logging\helpers.py.LoggingHelpers.log_fact_skipped
- calls_method:core\logging\helpers.py.LoggingHelpers.log_fact_processing
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:core\models\conversation_metadata.py.update_model
- calls_function:features\chat\chat_controller.py.remove_emojis
- calls_method:core\logging\helpers.py.LoggingHelpers.log_fact_storage_end
- calls_method:core\utils\prompts.py.PromptFormatter.format_fact_extraction_prompt
- calls_function:app\event_bus.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_fact_extraction_result
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_fact_storage_summary
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\utils\threading_audit.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\ollama\ollama_service.py.update_model
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_method:core\utils\prompts.py.PromptFormatter.format_auto_model_selection_info
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_method:core\logging\helpers.py.LoggingHelpers.log_exception_with_context
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_conversation_detection
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_fact_extraction_start
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_memory_result
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:core\threading\threading_service.py.get_global_threading_service
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__

### `features\chat\conversation_service.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\chat\summarization\summarization_service.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\memory\memory_service.py`

- calls_function:core\threading\thread_calculator.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_warning_with_context
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_method:features\memory\memory_service.py.PronounNormalizer.normalize_pronouns
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_method:features\memory\memory_service.py.PronounNormalizer.should_normalize
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\utils\threading_audit.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_service_initialization
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_memory_operation
- calls_function:core\utils\threading_utils.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_method:core\logging\helpers.py.LoggingHelpers.log_exception_with_context
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:config\config_manager.py.set
- calls_function:ui\ui_manager.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_method:features\memory\memory_service.py.MemoryRetriever.calculate_relevance
- calls_method:core\logging\helpers.py.LoggingHelpers.log_info_with_context
- calls_method:features\memory\memory_service.py.MemoryClassifier.classify_message
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_file_operation
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_method:features\memory\memory_service.py.MemoryRetriever.get_relevant_memories
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__

### `features\memory\semantic_search.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\memory\semantic_search_fallback.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:config\config_manager.py.set
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\ollama\ollama_chat.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\ollama\ollama_chat.py.showEvent
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:app\main.py.showEvent
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\ollama\ollama_service.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_service_initialization
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.get_global_persistent_thread_pool
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:config\config_manager.py.set
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:config\config_manager.py.get
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_info_with_context
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_network_request
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_debug
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:core\threading\threading_service.py.get_global_threading_service
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_exception_with_context
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\personality\formatter.py`

- calls_function:config\config_manager.py.get

### `features\personality\loader.py`

- calls_method:features\personality\formatter.py.PersonalityFormatter.validate_personality_data
- calls_method:core\logging\logger.py.CustomLogger.get_logger

### `features\personality\models\personality_model.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:features\personality\services\personality_service.py.get_custom_personalities
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:features\personality\models\personality_model.py.get_custom_personalities
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:features\personality\models\personality_model.py.get_system_personalities
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:features\personality\services\personality_service.py.get_system_personalities
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\personality\models\personality_model.py.PersonalityModel`

- inherits_from:features\personality\services\personality_service.py.PersonalityService

### `features\personality\services\personality_service.py`

- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:config\config_manager.py.get
- calls_function:config\config_manager.py.set

### `features\voice\audio\recording_service.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:features\voice\audio\recording_service.py.calculate_eq_bars_pcm
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:core\utils\threading_utils.py.log_thread_info
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\voice\orchestrator\voice_process_manager.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_method:features\voice\voice_service.py.VoiceService.get_instance
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\utils\threading_utils.py.safe_process_events_alternative
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\voice\stt\stt_service.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:config\config_manager.py.get
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\voice\tts\streaming_audio_player.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.calculate_eq_bars
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\voice\tts\streaming_audio_worker.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\voice\tts\tts_service.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\voice\voice_service.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_warning_with_context
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.get_global_persistent_thread_pool
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:config\config_manager.py.set
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_method:features\voice\tts\tts_service.py.TTSService.get_instance
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_method:core\logging\helpers.py.LoggingHelpers.log_audio_operation
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:core\threading\threading_service.py.get_global_threading_service
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:core\utils\threading_utils.py.log_thread_info
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\voice\voice_service_manager.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_method:app\service_manager.py.ServiceManager.get_instance
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_method:features\voice\voice_service.py.VoiceService.get_instance
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:app\service_manager.py.__new__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:core\logging\logger.py.__new__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\voice\voice_service_manager.py.__new__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `features\voice\voice_service_wrapper.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_method:features\voice\voice_service.py.VoiceService.get_instance
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.create_voice_process_manager
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `startup\install_dependencies.py`

- calls_function:core\threading\thread_calculator_examples.py.main
- calls_function:startup\install_dependencies.py.main
- calls_function:startup\system_installer.py.ensure_system_dependencies
- calls_function:startup\python_installer.py.install_python_requirements

### `startup\system_installer.py`

- calls_function:startup\system_installer.py.is_admin
- calls_function:startup\system_installer.py.offer_add_espeak_to_path

### `ui\Widgets\chat_navigation.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\Widgets\complexity_widget.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\Widgets\message_editor.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\Widgets\spellchecker_widget.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.keyPressEvent
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\dialogs\coqui_model_dialog.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\dialogs\error_dialog.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:ui\dialogs\error_dialog.py.accept
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\dialogs\settings_dialog.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\dialogs\voice_settings_dialog.py`

- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_method:features\voice\tts\tts_service.py.TTSService.get_instance
- calls_function:ui\dialogs\voice_settings_dialog.py.safe_get_value
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\shared_imports\pyside_imports.py.safe_ui_update
- calls_function:app\event_bus.py.safe_disconnect
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.safe_get_text
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.safe_disconnect
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:core\utils\internet_checker.py.test_internet_connection
- calls_function:core\utils\threading_utils.py.safe_process_events_alternative
- calls_function:app\event_bus.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.safe_get_checked
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:core\utils\threading_utils.py.safe_disconnect
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\utils\threading_audit.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.safe_disconnect
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.safe_disconnect
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\tabs\memory_tab.py.safe_disconnect
- calls_function:config\config_manager.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:core\utils\threading_utils.py.safe_ui_update
- calls_function:features\ollama\ollama_service.py.__init__

### `ui\tabs\chat_tab\chat_display.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\utils\message_utils.py.show_operation_error
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.show_error_dialog
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\utils\message_utils.py.show_validation_error
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\tabs\chat_tab\chat_renderer.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_method:ui\themes\message_formatter.py.MessageFormatter.detect_and_format_code
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_method:ui\themes\message_formatter.py.MessageFormatter.split_thoughts_and_answer
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_method:ui\themes\message_formatter.py.MessageFormatter.syntax_highlight_code
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_method:ui\themes\message_formatter.py.MessageFormatter.format_markdown
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\tabs\chat_tab\chat_tab.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:config\config_manager.py.get
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\utils\threading_utils.py.safe_process_events_alternative
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\tabs\chat_tab\eq_visualizer.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\utils\threading_utils.py.safe_process_events_alternative
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\tabs\chat_tab\input_controls.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\utils\threading_utils.py.safe_process_events_alternative
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.eventFilter
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\tabs\chat_tab\voice_controls.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:core\utils\threading_utils.py.safe_signal_connect
- calls_function:core\shared_imports\pyside_imports.py.safe_signal_disconnect
- calls_function:config\config_manager.py.set
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:features\voice\voice_service_manager.py.get_voice_service_manager
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\utils\threading_utils.py.safe_signal_disconnect
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:core\utils\threading_utils.py.log_thread_info
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:core\shared_imports\pyside_imports.py.safe_signal_connect
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\tabs\memory_tab.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.safe_disconnect
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.safe_disconnect
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:app\event_bus.py.safe_disconnect
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:core\utils\threading_utils.py.safe_disconnect
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.safe_disconnect
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:ui\tabs\memory_tab.py.safe_disconnect
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\tabs\model_tab.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\tabs\personality_tab.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\themes\message_formatter.py`

- calls_method:ui\themes\message_formatter.py.MessageFormatter.handle_html_tags
- calls_method:ui\themes\message_formatter.py.MessageFormatter.detect_code_type
- calls_method:ui\themes\message_formatter.py.MessageFormatter.syntax_highlight_code
- calls_method:ui\themes\message_formatter.py.MessageFormatter._protect_code_blocks
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_method:ui\themes\message_formatter.py.MessageFormatter.format_markdown
- calls_method:ui\themes\message_formatter.py.MessageFormatter.detect_and_format_code
- calls_method:ui\themes\message_formatter.py.MessageFormatter.cleanup_message

### `ui\ui_manager.py`

- calls_method:core\utils\prompts.py.PromptFormatter.get_menu_text
- calls_method:core\utils\prompts.py.PromptFormatter.format_status_message
- calls_method:core\logging\logger.py.CustomLogger.get_logger
- calls_method:ui\tabs\tab_styles.py.TabStyles.get_tab_style

### `ui\utils\message_utils.py`

- calls_function:ui\dialogs\error_dialog.py.show_error_dialog
- calls_function:ui\utils\message_utils.py.show_critical_error
- calls_method:core\logging\logger.py.CustomLogger.get_logger

### `ui\visualizers\widgets\bar_eq_widget.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\visualizers\widgets\circle_eq_widget.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\visualizers\widgets\circular_gradient_eq_widget.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

### `ui\visualizers\widgets\circular_net_eq_widget.py`

- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:features\memory\semantic_search_fallback.py.__init__
- calls_function:core\threading\thread_calculator.py.__init__
- calls_function:ui\dialogs\settings_dialog.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:features\chat\enhancers\enhancement_service.py.__init__
- calls_function:features\voice\tts\streaming_audio_player.py.__init__
- calls_function:ui\ui_manager.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:core\threading\qthread_workers.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\visualizers\widgets\bar_eq_widget.py.__init__
- calls_function:core\logging\helpers.py.__init__
- calls_function:ui\dialogs\voice_settings_dialog.py.__init__
- calls_function:ui\visualizers\widgets\circle_eq_widget.py.__init__
- calls_function:core\utils\streaming_handler.py.__init__
- calls_function:ui\dialogs\coqui_model_dialog.py.__init__
- calls_function:features\personality\loader.py.__init__
- calls_function:features\voice\voice_service.py.__init__
- calls_function:features\user\user_profile_service.py.__init__
- calls_function:features\voice\voice_service_wrapper.py.__init__
- calls_function:features\chat\conversation_service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:app\threading_integration.py.__init__
- calls_function:app\main.py.__init__
- calls_function:core\threading\threading_service.py.__init__
- calls_function:features\voice\orchestrator\voice_process_manager.py.__init__
- calls_function:core\threading\usage_examples.py.__init__
- calls_function:ui\visualizers\widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:app\event_bus.py.__init__
- calls_function:features\voice\audio\recording_service.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\visualizers\widgets\circular_net_eq_widget.py.__init__
- calls_function:features\chat\chat_controller.py.__init__
- calls_function:features\ollama\ollama_chat.py.__init__
- calls_function:features\voice\stt\stt_service.py.__init__
- calls_function:core\threading\thread_monitor.py.__init__
- calls_function:core\utils\internet_checker.py.__init__
- calls_function:features\memory\semantic_search.py.__init__
- calls_function:features\chat\summarization\summarization_service.py.__init__
- calls_function:features\memory\memory_service.py.__init__
- calls_function:app\app_lifecycle.py.__init__
- calls_function:app\service_manager.py.__init__
- calls_function:ui\Widgets\complexity_widget.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:features\voice\voice_service_manager.py.__init__
- calls_function:startup\dependency_checker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_renderer.py.__init__
- calls_function:features\chat\complexity_analyser\complexity_analyzer.py.__init__
- calls_function:core\threading\qrunnable_tasks.py.__init__
- calls_function:features\voice\tts\tts_service.py.__init__
- calls_function:ui\Widgets\message_editor.py.__init__
- calls_function:features\personality\models\personality_model.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\dialogs\error_dialog.py.__init__
- calls_function:core\models\conversation_metadata.py.__init__
- calls_function:features\voice\tts\streaming_audio_worker.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:core\utils\threading_utils.py.__init__
- calls_function:features\personality\services\personality_service.py.__init__
- calls_function:features\ollama\ollama_service.py.__init__
- calls_function:core\threading\persistent_thread_pool.py.__init__
- calls_function:core\threading\thread_pool_manager.py.__init__
- calls_function:core\utils\threading_audit.py.__init__

## 📦 Imports

### `app\app_lifecycle.py`

- `PySide6.QtWidgets.QFileDialog`
- `PySide6.QtWidgets.QInputDialog`
- `json`
- `platform`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `requests`
- `shutil`
- `subprocess`
- `threading`
- `webbrowser`

### `app\event_bus.py`

- `pyside_chat.core.logging.helpers.LoggingHelpers`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.utils.prompts.PromptFormatter`
- `pyside_chat.core.utils.threading_utils.safe_ui_update`
- `pyside_chat.features.chat.chat_controller.ChatController`
- `pyside_chat.ui.dialogs.settings_dialog.SettingsDialog`
- `pyside_chat.ui.utils.message_utils.show_critical_error`
- `pyside_chat.ui.utils.message_utils.show_operation_error`

### `app\main.py`

- `pyside_chat.app.app_lifecycle.AppLifecycleManager`
- `pyside_chat.app.event_bus.EventBus`
- `pyside_chat.app.service_manager.ServiceManager`
- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.features.chat.chat_controller.ChatController`
- `pyside_chat.ui.ui_manager.UIManager`
- `traceback`

### `app\service_manager.py`

- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.models.conversation_metadata.ConversationManager`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.chat.conversation_service.ConversationService`
- `pyside_chat.features.chat.enhancers.enhancement_service.EnhancementService`
- `pyside_chat.features.chat.summarization.summarization_service.SummarizationService`
- `pyside_chat.features.memory.memory_service.MemoryService`
- `pyside_chat.features.ollama.ollama_service.OllamaService`
- `pyside_chat.features.personality.models.personality_model.PersonalityModel`
- `pyside_chat.features.voice.voice_service_manager.get_voice_service_manager`

### `app\threading_integration.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`

### `config\config_manager.py`

- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

### `core\logging\helpers.py`

- `logging`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `threading`
- `traceback`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `core\logging\logger.py`

- `logging`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `re`
- `threading`

### `core\models\base_model.py`

- `abc.ABC`
- `abc.abstractmethod`
- `typing.Any`
- `typing.Dict`

### `core\models\conversation_metadata.py`

- `dataclasses.dataclass`
- `dataclasses.field`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

### `core\shared_imports\audio_imports.py`

- `librosa`
- `pyaudio`
- `sounddevice`
- `soundfile`

### `core\shared_imports\json_time_imports.py`

- `datetime.datetime`
- `datetime.timedelta`
- `json`
- `time`

### `core\shared_imports\os_sys_imports.py`

- `os`
- `pathlib.Path`
- `sys`
- `tempfile`

### `core\shared_imports\pyside_imports.py`

- `PySide6.QtCore.QByteArray`
- `PySide6.QtCore.QCoreApplication`
- `PySide6.QtCore.QDataStream`
- `PySide6.QtCore.QDate`
- `PySide6.QtCore.QDateTime`
- `PySide6.QtCore.QDir`
- `PySide6.QtCore.QEvent`
- `PySide6.QtCore.QFile`
- `PySide6.QtCore.QFileInfo`
- `PySide6.QtCore.QIODevice`
- `PySide6.QtCore.QMetaObject`
- `PySide6.QtCore.QMutex`
- `PySide6.QtCore.QMutexLocker`
- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QPoint`
- `PySide6.QtCore.QPointF`
- `PySide6.QtCore.QProcess`
- `PySide6.QtCore.QRect`
- `PySide6.QtCore.QRectF`
- `PySide6.QtCore.QRunnable`
- `PySide6.QtCore.QSettings`
- `PySide6.QtCore.QSize`
- `PySide6.QtCore.QSizeF`
- `PySide6.QtCore.QThread`
- `PySide6.QtCore.QThreadPool`
- `PySide6.QtCore.QTime`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.QUrl`
- `PySide6.QtCore.QWaitCondition`
- `PySide6.QtCore.Q_ARG`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtCore.Slot`
- `PySide6.QtGui.QAccessible`
- `PySide6.QtGui.QAccessibleInterface`
- `PySide6.QtGui.QAction`
- `PySide6.QtGui.QActionGroup`
- `PySide6.QtGui.QBitmap`
- `PySide6.QtGui.QBrush`
- `PySide6.QtGui.QClipboard`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QConicalGradient`
- `PySide6.QtGui.QContextMenuEvent`
- `PySide6.QtGui.QCursor`
- `PySide6.QtGui.QDrag`
- `PySide6.QtGui.QDragEnterEvent`
- `PySide6.QtGui.QDropEvent`
- `PySide6.QtGui.QFocusEvent`
- `PySide6.QtGui.QFont`
- `PySide6.QtGui.QFontInfo`
- `PySide6.QtGui.QFontMetrics`
- `PySide6.QtGui.QIcon`
- `PySide6.QtGui.QImage`
- `PySide6.QtGui.QKeyEvent`
- `PySide6.QtGui.QLinearGradient`
- `PySide6.QtGui.QMouseEvent`
- `PySide6.QtGui.QMoveEvent`
- `PySide6.QtGui.QPainter`
- `PySide6.QtGui.QPainterPath`
- `PySide6.QtGui.QPalette`
- `PySide6.QtGui.QPen`
- `PySide6.QtGui.QPixmap`
- `PySide6.QtGui.QRadialGradient`
- `PySide6.QtGui.QResizeEvent`
- `PySide6.QtGui.QShortcut`
- `PySide6.QtGui.QTextBlock`
- `PySide6.QtGui.QTextCharFormat`
- `PySide6.QtGui.QTextCursor`
- `PySide6.QtGui.QTextDocument`
- `PySide6.QtGui.QTextFragment`
- `PySide6.QtGui.QTextLayout`
- `PySide6.QtGui.QTransform`
- `PySide6.QtGui.QWheelEvent`
- `PySide6.QtMultimedia.QAudioBuffer`
- `PySide6.QtMultimedia.QAudioDecoder`
- `PySide6.QtMultimedia.QAudioDevice`
- `PySide6.QtMultimedia.QAudioFormat`
- `PySide6.QtMultimedia.QAudioInput`
- `PySide6.QtMultimedia.QAudioOutput`
- `PySide6.QtMultimedia.QCamera`
- `PySide6.QtMultimedia.QCameraDevice`
- `PySide6.QtMultimedia.QImageCapture`
- `PySide6.QtMultimedia.QMediaPlayer`
- `PySide6.QtMultimedia.QMediaRecorder`
- `PySide6.QtMultimedia.QSoundEffect`
- `PySide6.QtNetwork.QDnsLookup`
- `PySide6.QtNetwork.QHostAddress`
- `PySide6.QtNetwork.QHostInfo`
- `PySide6.QtNetwork.QNetworkAccessManager`
- `PySide6.QtNetwork.QNetworkAddressEntry`
- `PySide6.QtNetwork.QNetworkInterface`
- `PySide6.QtNetwork.QNetworkReply`
- `PySide6.QtNetwork.QNetworkRequest`
- `PySide6.QtNetwork.QSslCertificate`
- `PySide6.QtNetwork.QSslConfiguration`
- `PySide6.QtNetwork.QSslSocket`
- `PySide6.QtNetwork.QWebSocket`
- `PySide6.QtNetwork.QWebSocketServer`
- `PySide6.QtSql.QSqlDatabase`
- `PySide6.QtSql.QSqlDriver`
- `PySide6.QtSql.QSqlDriverCreator`
- `PySide6.QtSql.QSqlDriverCreatorBase`
- `PySide6.QtSql.QSqlField`
- `PySide6.QtSql.QSqlQuery`
- `PySide6.QtSql.QSqlQueryModel`
- `PySide6.QtSql.QSqlRecord`
- `PySide6.QtSql.QSqlRelationalTableModel`
- `PySide6.QtSql.QSqlTableModel`
- `PySide6.QtWidgets.QApplication`
- `PySide6.QtWidgets.QCalendarWidget`
- `PySide6.QtWidgets.QCheckBox`
- `PySide6.QtWidgets.QColorDialog`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QDateEdit`
- `PySide6.QtWidgets.QDateTimeEdit`
- `PySide6.QtWidgets.QDial`
- `PySide6.QtWidgets.QDialog`
- `PySide6.QtWidgets.QDialogButtonBox`
- `PySide6.QtWidgets.QDoubleSpinBox`
- `PySide6.QtWidgets.QFileDialog`
- `PySide6.QtWidgets.QFontDialog`
- `PySide6.QtWidgets.QFormLayout`
- `PySide6.QtWidgets.QFrame`
- `PySide6.QtWidgets.QGraphicsItem`
- `PySide6.QtWidgets.QGraphicsPixmapItem`
- `PySide6.QtWidgets.QGraphicsScene`
- `PySide6.QtWidgets.QGraphicsView`
- `PySide6.QtWidgets.QGridLayout`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QHeaderView`
- `PySide6.QtWidgets.QInputDialog`
- `PySide6.QtWidgets.QLCDNumber`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QLineEdit`
- `PySide6.QtWidgets.QListWidget`
- `PySide6.QtWidgets.QListWidgetItem`
- `PySide6.QtWidgets.QMainWindow`
- `PySide6.QtWidgets.QMdiArea`
- `PySide6.QtWidgets.QMdiSubWindow`
- `PySide6.QtWidgets.QMenu`
- `PySide6.QtWidgets.QMenuBar`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QPlainTextEdit`
- `PySide6.QtWidgets.QProgressBar`
- `PySide6.QtWidgets.QProgressDialog`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QRadioButton`
- `PySide6.QtWidgets.QScrollArea`
- `PySide6.QtWidgets.QScrollBar`
- `PySide6.QtWidgets.QSlider`
- `PySide6.QtWidgets.QSpinBox`
- `PySide6.QtWidgets.QSplitter`
- `PySide6.QtWidgets.QStackedWidget`
- `PySide6.QtWidgets.QStatusBar`
- `PySide6.QtWidgets.QSystemTrayIcon`
- `PySide6.QtWidgets.QTabBar`
- `PySide6.QtWidgets.QTabWidget`
- `PySide6.QtWidgets.QTableWidget`
- `PySide6.QtWidgets.QTableWidgetItem`
- `PySide6.QtWidgets.QTextBrowser`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QTimeEdit`
- `PySide6.QtWidgets.QToolBar`
- `PySide6.QtWidgets.QToolButton`
- `PySide6.QtWidgets.QTreeWidget`
- `PySide6.QtWidgets.QTreeWidgetItem`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `PySide6.QtWidgets.QWizard`
- `PySide6.QtWidgets.QWizardPage`
- `PySide6.QtXml.QDomDocument`
- `PySide6.QtXml.QDomElement`
- `PySide6.QtXml.QDomNode`
- `PySide6.QtXml.QDomNodeList`
- `PySide6.QtXml.QXmlStreamReader`
- `PySide6.QtXml.QXmlStreamWriter`

### `core\shared_imports\shared_imports.py`

- `TTS`
- `blis`
- `contextlib`
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime`
- `datetime.datetime`
- `datetime.timedelta`
- `enchant`
- `enum.Enum`
- `functools`
- `hashlib`
- `html.escape`
- `html.unescape`
- `io`
- `json`
- `librosa`
- `logging`
- `math`
- `networkx`
- `numpy`
- `ollama`
- `os`
- `pickle`
- `platform`
- `psutil`
- `pyaudio`
- `pyenchant`
- `pygame`
- `pygments`
- `pygments.formatters.HtmlFormatter`
- `pygments.highlight`
- `pygments.lexers.get_lexer_by_name`
- `pygments.lexers.guess_lexer`
- `pyside_chat.core.logging.helpers.LoggingHelpers`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.threading.persistent_thread_pool.get_global_persistent_thread_pool`
- `pyside_chat.core.threading.qrunnable_tasks.DataProcessingTask`
- `pyside_chat.core.threading.threading_service.get_global_threading_service`
- `pyttsx3`
- `queue`
- `random`
- `re`
- `requests`
- `scipy`
- `sentence_transformers`
- `shutil`
- `sklearn.metrics.pairwise.cosine_similarity`
- `socket`
- `sounddevice`
- `soundfile`
- `struct`
- `subprocess`
- `sys`
- `tempfile`
- `threading`
- `threading.Lock`
- `time`
- `traceback`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generator`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`
- `typing.Type`
- `typing.Union`
- `uuid`
- `vosk`

### `core\threading\__init__.py`

- `persistent_thread_pool.PersistentThreadPool`
- `persistent_thread_pool.get_global_persistent_thread_pool`
- `pyside_chat.core.logging.logger.CustomLogger`
- `qrunnable_tasks.CalculationTask`
- `qrunnable_tasks.DataProcessingTask`
- `qrunnable_tasks.FileProcessingTask`
- `qrunnable_tasks.MessageProcessingTask`
- `qthread_workers.AudioStreamingWorker`
- `qthread_workers.ChatStreamingWorker`
- `qthread_workers.MonitoringWorker`
- `qthread_workers.StreamingWorker`
- `thread_calculator.ThreadCalculator`
- `thread_calculator.ThreadRecommendations`
- `thread_calculator.analyze_system`
- `thread_calculator.get_pool_thread_count`
- `thread_calculator.get_thread_recommendations`
- `thread_calculator.thread_calculator`
- `thread_monitor.ThreadMonitor`
- `thread_monitor.get_global_thread_monitor`
- `thread_pool_manager.ThreadPoolManager`
- `thread_pool_manager.get_global_thread_pool_manager`
- `threading_service.ThreadingService`
- `threading_service.get_global_threading_service`

### `core\threading\persistent_thread_config.py`

- `typing.Any`
- `typing.Dict`

### `core\threading\persistent_thread_pool.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `thread_monitor.get_global_thread_monitor`

### `core\threading\qrunnable_tasks.py`

- `ollama`
- `os`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `subprocess`

### `core\threading\qthread_workers.py`

- `psutil`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`

### `core\threading\thread_calculator.py`

- `dataclasses.dataclass`
- `logging`
- `platform`
- `psutil`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

### `core\threading\thread_calculator_examples.py`

- `psutil`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.threading.PersistentThreadPool`
- `pyside_chat.core.threading.ThreadPoolManager`
- `pyside_chat.core.threading.get_pool_thread_count`
- `pyside_chat.core.threading.get_thread_recommendations`
- `pyside_chat.core.threading.thread_calculator`

### `core\threading\thread_monitor.py`

- `psutil`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`

### `core\threading\thread_pool_manager.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `thread_calculator.get_pool_thread_count`

### `core\threading\threading_service.py`

- `persistent_thread_pool.get_global_persistent_thread_pool`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `qrunnable_tasks.DataProcessingTask`
- `qrunnable_tasks.FileProcessingTask`
- `qrunnable_tasks.MessageProcessingTask`
- `qthread_workers.AudioStreamingWorker`
- `qthread_workers.ChatStreamingWorker`
- `qthread_workers.MonitoringWorker`
- `thread_calculator.get_pool_thread_count`
- `thread_monitor.get_global_thread_monitor`
- `thread_pool_manager.get_global_thread_pool_manager`

### `core\threading\usage_examples.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`

### `core\utils\error_handler.py`

- `contextlib.contextmanager`
- `functools`
- `os`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.Logging.logging_helpers.LoggingHelpers`
- `requests`
- `traceback`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `typing.Type`
- `typing.Union`

### `core\utils\internet_checker.py`

- `socket`
- `typing.List`
- `typing.Tuple`
- `urllib.error`
- `urllib.request`

### `core\utils\prompts.py`

- `typing.Any`
- `typing.Dict`

### `core\utils\streaming_handler.py`

- `logging`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `traceback`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `core\utils\threading_audit.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `threading`
- `traceback`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `core\utils\threading_utils.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Optional`

### `features\chat\chat_controller.py`

- `datetime.datetime`
- `json`
- `os`
- `pyside_chat.core.models.conversation_metadata.ConversationManager`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.threading.threading_service.get_global_threading_service`
- `pyside_chat.core.utils.prompts.PromptFormatter`
- `pyside_chat.features.chat.complexity_analyser.complexity_analyzer.RequestComplexityAnalyzer`
- `pyside_chat.features.chat.conversation_service.ConversationService`
- `pyside_chat.features.chat.enhancers.enhancement_service.EnhancementService`
- `pyside_chat.features.memory.memory_service.MemoryService`
- `pyside_chat.features.ollama.ollama_service.OllamaService`
- `re`
- `traceback`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `features\chat\complexity_analyser\complexity_analyzer.py`

- `dataclasses.dataclass`
- `enum.Enum`
- `re`
- `requests`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `features\chat\conversation_service.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `features\chat\enhancers\enhancement_service.py`

- `typing.Optional`

### `features\chat\summarization\summarization_service.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.chat.complexity_analyser.complexity_analyzer.RequestComplexityAnalyzer`
- `pyside_chat.features.ollama.ollama_service.OllamaService`
- `re`

### `features\memory\memory_service.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.memory.semantic_search.SemanticSearchService`
- `pyside_chat.features.memory.semantic_search_fallback.SemanticSearchFallback`
- `sentence_transformers`

### `features\memory\semantic_search.py`

- `dataclasses.dataclass`
- `numpy`
- `pickle`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `sentence_transformers.SentenceTransformer`
- `sklearn.metrics.pairwise.cosine_similarity`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `features\memory\semantic_search_fallback.py`

- `dataclasses.dataclass`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `features\ollama\ollama_chat.py`

- `pyside_chat.app.app_lifecycle.AppLifecycleManager`
- `pyside_chat.app.event_bus.EventBus`
- `pyside_chat.app.service_manager.ServiceManager`
- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.features.chat.chat_controller.ChatController`
- `pyside_chat.ui.ui_manager.UIManager`
- `traceback`

### `features\ollama\ollama_service.py`

- `ollama`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`

### `features\personality\formatter.py`

- `pyside_chat.features.personality.models.PersonalityConfig`
- `pyside_chat.features.personality.models.PersonalityMetadata`
- `pyside_chat.features.personality.models.PersonalityPrompt`
- `pyside_chat.features.personality.models.PersonalityTraits`
- `pyside_chat.features.personality.models.personality_pronouns.PersonalityPronouns`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `features\personality\loader.py`

- `dataclasses.asdict`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.personality.formatter.PersonalityFormatter`
- `pyside_chat.features.personality.models.personality_types.PersonalityConfig`
- `pyside_chat.features.personality.models.personality_types.PersonalityMetadata`
- `pyside_chat.features.personality.models.personality_types.PersonalityPrompt`
- `pyside_chat.features.personality.models.personality_types.PersonalityTraits`
- `shutil`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `features\personality\models\personality_model.py`

- `pyside_chat.features.personality.services.personality_service.PersonalityService`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `features\personality\models\personality_pronouns.py`

- `dataclasses.dataclass`
- `random`
- `typing.List`

### `features\personality\models\personality_types.py`

- `dataclasses.dataclass`
- `enum.Enum`
- `typing.List`

### `features\personality\services\personality_service.py`

- `datetime.datetime`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.personality.formatter.PersonalityFormatter`
- `pyside_chat.features.personality.loader.PersonalityLoader`
- `pyside_chat.features.personality.models.personality_types.PersonalityConfig`
- `pyside_chat.features.personality.models.personality_types.PersonalityMetadata`
- `pyside_chat.features.personality.models.personality_types.PersonalityPrompt`
- `pyside_chat.features.personality.models.personality_types.PersonalityTraits`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `features\user\user_profile_service.py`

- `typing.Any`
- `typing.Dict`
- `typing.Optional`

### `features\voice\audio\recording_service.py`

- `datetime`
- `math`
- `pyside_chat.core.shared_imports.audio_imports.*`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `struct`
- `threading`
- `typing.Optional`
- `wave`

### `features\voice\orchestrator\__init__.py`

- `voice_process_manager.VoiceProcessManager`
- `voice_process_manager.create_voice_process_manager`

### `features\voice\orchestrator\voice_process_manager.py`

- `multiprocessing`
- `pickle`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.utils.threading_utils.safe_process_events_alternative`
- `pyside_chat.features.voice.voice_service.VoiceService`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`

### `features\voice\stt\stt_service.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `traceback`
- `vosk.KaldiRecognizer`
- `vosk.Model`
- `wave`

### `features\voice\tts\streaming_audio_player.py`

- `numpy`
- `pyside_chat.core.shared_imports.audio_imports.*`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `threading`
- `traceback`

### `features\voice\tts\streaming_audio_worker.py`

- `numpy`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `re`
- `scipy.signal`
- `traceback`
- `typing.List`
- `typing.Optional`

### `features\voice\tts\tts_service.py`

- `coqui_tts_service.CoquiTTSService`
- `platform`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `subprocess`

### `features\voice\voice_service.py`

- `pyside_chat.core.shared_imports.audio_imports.*`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.voice.audio.recording_service.RecordingService`
- `pyside_chat.features.voice.stt.stt_service.STTService`
- `speech_recognition`
- `traceback`
- `typing.Callable`
- `typing.Optional`
- `uuid`
- `wave`

### `features\voice\voice_service_manager.py`

- `pyside_chat.app.service_manager.ServiceManager`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.voice.voice_service.VoiceService`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

### `features\voice\voice_service_wrapper.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.features.voice.orchestrator.create_voice_process_manager`
- `traceback`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `voice_service.VoiceService`

### `startup\dependency_checker.py`

- `importlib`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `subprocess`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `startup\install_dependencies.py`

- `ctypes`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.startup.python_installer.install_python_requirements`
- `pyside_chat.startup.system_installer.ensure_system_dependencies`
- `shutil`
- `subprocess`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `startup\python_installer.py`

- `pyside_chat.core.shared_imports.shared_imports.*`
- `subprocess`

### `startup\system_installer.py`

- `ctypes`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `shutil`
- `subprocess`

### `ui\Widgets\chat_navigation.py`

- `pyside_chat.core.models.conversation_metadata.ConversationManager`
- `pyside_chat.core.models.conversation_metadata.ConversationMetadata`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.chat.summarization.summarization_service.SummarizationService`

### `ui\Widgets\complexity_widget.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`

### `ui\Widgets\message_editor.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`

### `ui\Widgets\spellchecker_widget.py`

- `enchant`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `re`

### `ui\dialogs\__init__.py`

- `error_dialog.DetailedErrorDialog`
- `error_dialog.ErrorDialog`
- `error_dialog.show_error_dialog`

### `ui\dialogs\coqui_model_dialog.py`

- `datetime.datetime`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.voice.tts.coqui_tts_service.CoquiTTSService`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `ui\dialogs\error_dialog.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`

### `ui\dialogs\settings_dialog.py`

- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`

### `ui\dialogs\voice_settings_dialog.py`

- `math`
- `pyaudio`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.utils.internet_checker.test_internet_connection`
- `pyside_chat.core.utils.threading_utils.safe_process_events_alternative`
- `pyside_chat.core.utils.threading_utils.safe_ui_update`
- `pyside_chat.features.voice.tts.coqui_tts_service.CoquiTTSService`
- `pyside_chat.features.voice.tts.tts_service.TTSService`
- `struct`
- `time`
- `traceback`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `ui\tabs\chat_tab\chat_display.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.utils.streaming_handler.StreamingHandler`
- `pyside_chat.ui.dialogs.error_dialog.show_error_dialog`
- `pyside_chat.ui.tabs.chat_tab.chat_renderer.ChatRenderer`
- `pyside_chat.ui.utils.message_utils.show_operation_error`
- `pyside_chat.ui.utils.message_utils.show_validation_error`
- `traceback`

### `ui\tabs\chat_tab\chat_renderer.py`

- `html.escape`
- `logging`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.ui.themes.message_formatter.MessageFormatter`
- `traceback`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `ui\tabs\chat_tab\chat_tab.py`

- `PySide6.QtGui.QTextCursor`
- `chat_display.ChatDisplay`
- `eq_visualizer.EQVisualizer`
- `input_controls.InputControls`
- `os`
- `pyside_chat.core.models.conversation_metadata.ConversationMetadata`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.utils.threading_utils.safe_process_events_alternative`
- `pyside_chat.ui.Widgets.chat_navigation.ChatNavigationWidget`
- `pyside_chat.ui.dialogs.voice_settings_dialog.VoiceSettingsDialog`
- `traceback`
- `voice_controls.VoiceControls`

### `ui\tabs\chat_tab\eq_visualizer.py`

- `logging`
- `pyside_chat.core.logging.logger.CustomLogger`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.utils.threading_utils.safe_process_events_alternative`
- `pyside_chat.ui.visualizers.widgets.bar_eq_widget.BarEQWidget`
- `pyside_chat.ui.visualizers.widgets.circle_eq_widget.CircleEQWidget`
- `pyside_chat.ui.visualizers.widgets.circular_gradient_eq_widget.CircularGradientEQWidget`
- `pyside_chat.ui.visualizers.widgets.circular_net_eq_widget.CircularNetEQWidget`
- `random`
- `traceback`
- `typing.Dict`
- `typing.Optional`

### `ui\tabs\chat_tab\input_controls.py`

- `logging`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.utils.threading_utils.safe_process_events_alternative`
- `typing.Dict`
- `typing.Optional`

### `ui\tabs\chat_tab\voice_controls.py`

- `logging`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.utils.threading_utils.*`
- `pyside_chat.features.voice.voice_service_manager.get_voice_service_manager`
- `traceback`
- `typing.Dict`
- `typing.Optional`

### `ui\tabs\memory_tab.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.memory.memory_service.MemoryService`

### `ui\tabs\model_tab.py`

- `datetime.datetime`
- `pyside_chat.core.shared_imports.pyside_imports.*`

### `ui\tabs\personality_tab.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.features.personality.models.personality_model.PersonalityConfig`
- `pyside_chat.features.personality.models.personality_model.PersonalityMetadata`
- `pyside_chat.features.personality.models.personality_model.PersonalityModel`
- `pyside_chat.features.personality.models.personality_model.PersonalityPrompt`
- `pyside_chat.features.personality.models.personality_model.PersonalityTraits`

### `ui\themes\message_formatter.py`

- `html.escape`
- `html.unescape`
- `pygments.formatters.HtmlFormatter`
- `pygments.highlight`
- `pygments.lexers.get_lexer_by_name`
- `pygments.lexers.guess_lexer`
- `pyside_chat.core.logging.logger.CustomLogger`
- `re`

### `ui\ui_manager.py`

- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `pyside_chat.core.shared_imports.shared_imports.*`
- `pyside_chat.core.utils.prompts.PromptFormatter`
- `pyside_chat.ui.tabs.chat_tab.chat_tab.ChatTab`
- `pyside_chat.ui.tabs.memory_tab.MemoryTab`
- `pyside_chat.ui.tabs.model_tab.ModelTab`
- `pyside_chat.ui.tabs.personality_tab.PersonalityTab`
- `pyside_chat.ui.tabs.tab_styles.TabStyles`
- `pyside_chat.ui.themes.styles.dark_stylesheet`
- `pyside_chat.ui.themes.styles.light_stylesheet`

### `ui\utils\message_utils.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`
- `traceback`
- `typing.Optional`

### `ui\visualizers\widgets\bar_eq_widget.py`

- `pyside_chat.core.shared_imports.pyside_imports.*`

### `ui\visualizers\widgets\circle_eq_widget.py`

- `math`
- `pyside_chat.core.shared_imports.pyside_imports.*`

### `ui\visualizers\widgets\circular_gradient_eq_widget.py`

- `math`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `random`

### `ui\visualizers\widgets\circular_net_eq_widget.py`

- `math`
- `pyside_chat.core.shared_imports.pyside_imports.*`
- `random`

## 📞 Function Call Analysis

### `app\app_lifecycle.py`

**Function Calls:**
- `QMessageBox`
- `QProgressDialog`
- `QTimer`
- `bool`
- `enumerate`
- `format`
- `get`
- `int`
- `len`
- `lower`
- `min`
- `str`
- `type`

### `app\event_bus.py`

**Function Calls:**
- `ChatController`
- `Exception`
- `QMessageBox`
- `QTimer`
- `SettingsDialog`
- `get_global_threading_service`
- `hasattr`
- `len`
- `objectName`
- `safe_disconnect`
- `safe_ui_update`
- `show_critical_error`
- `show_operation_error`
- `str`
- `update_model`
- `update_personality`

### `app\main.py`

**Function Calls:**
- `AppLifecycleManager`
- `ChatController`
- `ConfigManager`
- `EventBus`
- `ServiceManager`
- `UIManager`
- `__init__`
- `showEvent`
- `super`

### `app\service_manager.py`

**Function Calls:**
- `ConversationManager`
- `ConversationService`
- `EnhancementService`
- `MemoryService`
- `OllamaService`
- `PersonalityModel`
- `RuntimeError`
- `SummarizationService`
- `__new__`
- `get_voice_service_manager`
- `hasattr`
- `super`

### `app\threading_integration.py`

**Function Calls:**
- `Signal`
- `ThreadingIntegration`
- `__init__`
- `get_global_threading_service`
- `hasattr`
- `super`

### `config\config_manager.py`

**Function Calls:**
- `get`
- `isinstance`
- `open`

### `core\logging\helpers.py`

**Function Calls:**
- `Signal`
- `ThreadMonitor`
- `__init__`
- `hasattr`
- `id`
- `len`
- `str`
- `sum`
- `super`

### `core\logging\logger.py`

**Function Calls:**
- `DummyLogger`
- `ThreadInfoFormatter`
- `__new__`
- `_sanitize_filename`
- `critical`
- `debug`
- `error`
- `format`
- `info`
- `join`
- `open`
- `print`
- `set`
- `str`
- `strip_emojis`
- `super`
- `type`
- `warning`

### `core\models\conversation_metadata.py`

**Function Calls:**
- `ConversationMetadata`
- `Signal`
- `ValueError`
- `__init__`
- `cls`
- `get`
- `isinstance`
- `isoformat`
- `len`
- `open`
- `str`
- `strftime`
- `super`

### `core\shared_imports\pyside_imports.py`

**Function Calls:**
- `QComboBox`
- `QFormLayout`
- `QGridLayout`
- `QHBoxLayout`
- `QLabel`
- `QLineEdit`
- `QMessageBox`
- `QProgressBar`
- `QPushButton`
- `QTextEdit`
- `QTimer`
- `QVBoxLayout`
- `func`
- `hasattr`
- `is_main_thread`
- `thread`

### `core\threading\persistent_thread_config.py`

**Function Calls:**
- `get_config_summary`
- `get_persistent_thread_config`
- `items`
- `len`
- `print`
- `sum`
- `validate_persistent_thread_config`

### `core\threading\persistent_thread_pool.py`

**Function Calls:**
- `Lock`
- `PersistentThreadPool`
- `QThread`
- `QTimer`
- `Signal`
- `__init__`
- `append`
- `get_global_thread_monitor`
- `hasattr`
- `id`
- `len`
- `list`
- `pop`
- `range`
- `super`
- `update`
- `worker_class`

### `core\threading\qrunnable_tasks.py`

**Function Calls:**
- `RuntimeError`
- `Signal`
- `ValueError`
- `all`
- `any`
- `error_callback`
- `int`
- `isinstance`
- `islower`
- `iter`
- `join`
- `len`
- `list`
- `max`
- `min`
- `open`
- `progress_callback`
- `range`
- `set`
- `sorted`
- `str`
- `success_callback`
- `sum`
- `type`
- `upper`

### `core\threading\qthread_workers.py`

**Function Calls:**
- `NotImplementedError`
- `Signal`
- `ValueError`
- `__init__`
- `configure_streaming`
- `get`
- `id`
- `int`
- `list`
- `str`
- `super`

### `core\threading\thread_calculator.py`

**Function Calls:**
- `ThreadCalculator`
- `ThreadRecommendations`
- `analyze_system`
- `int`
- `max`
- `min`
- `print`

### `core\threading\thread_calculator_examples.py`

**Function Calls:**
- `PersistentThreadPool`
- `ThreadPoolManager`
- `example_dynamic_adjustment`
- `example_memory_optimization`
- `example_persistent_thread_pool`
- `example_streaming_configuration`
- `example_thread_pool_manager`
- `get_pool_thread_count`
- `get_thread_recommendations`
- `main`
- `max`
- `min`
- `print`

### `core\threading\thread_monitor.py`

**Function Calls:**
- `QTimer`
- `Signal`
- `ThreadMonitor`
- `__init__`
- `copy`
- `id`
- `len`
- `list`
- `max`
- `sum`
- `super`

### `core\threading\thread_pool_manager.py`

**Function Calls:**
- `QThreadPool`
- `QTimer`
- `Signal`
- `ThreadPoolManager`
- `__init__`
- `copy`
- `get_pool_thread_count`
- `int`
- `len`
- `list`
- `str`
- `super`
- `type`

### `core\threading\threading_service.py`

**Function Calls:**
- `DataProcessingTask`
- `FileProcessingTask`
- `MessageProcessingTask`
- `Signal`
- `ThreadingService`
- `__init__`
- `get_global_persistent_thread_pool`
- `get_global_thread_monitor`
- `get_global_thread_pool_manager`
- `get_pool_thread_count`
- `hasattr`
- `len`
- `super`

### `core\threading\usage_examples.py`

**Function Calls:**
- `ChatApplicationExample`
- `ChatStreamingWorker`
- `FileProcessingTask`
- `MessageProcessingTask`
- `QThread`
- `demonstrate_threading_usage`
- `get_global_thread_monitor`
- `get_global_thread_pool_manager`
- `id`
- `len`
- `print`

### `core\utils\error_handler.py`

**Function Calls:**
- `func`
- `hasattr`
- `isinstance`
- `open`
- `range`
- `str`
- `type`

### `core\utils\internet_checker.py`

**Function Calls:**
- `InternetConnectionTester`
- `is_online`
- `print`
- `test_internet_connection`
- `test_internet_connection_detailed`

### `core\utils\prompts.py`

**Function Calls:**
- `format`

### `core\utils\streaming_handler.py`

**Function Calls:**
- `QTimer`
- `Signal`
- `__init__`
- `enumerate`
- `hasattr`
- `join`
- `len`
- `range`
- `reversed`
- `super`

### `core\utils\threading_audit.py`

**Function Calls:**
- `ThreadSafetyAuditor`
- `enumerate`
- `join`
- `len`
- `open`
- `print`
- `run_thread_safety_audit`
- `str`
- `thread`
- `upper`

### `core\utils\threading_utils.py`

**Function Calls:**
- `Q_ARG`
- `callback`
- `error`
- `func`
- `getattr`
- `is_main_thread`
- `method`
- `safe_connect_signal`
- `safe_disconnect`
- `safe_widget_update`
- `thread`
- `type`

### `features\chat\chat_controller.py`

**Function Calls:**
- `RequestComplexityAnalyzer`
- `Signal`
- `__init__`
- `get_global_threading_service`
- `getattr`
- `hasattr`
- `isinstance`
- `len`
- `remove_emojis`
- `str`
- `strftime`
- `strip`
- `super`
- `update_model`

### `features\chat\complexity_analyser\complexity_analyzer.py`

**Function Calls:**
- `ComplexityMetrics`
- `float`
- `int`
- `len`
- `max`
- `min`
- `sorted`
- `sum`
- `title`

### `features\chat\conversation_service.py`

**Function Calls:**
- `Signal`
- `__init__`
- `enumerate`
- `hasattr`
- `int`
- `isinstance`
- `len`
- `max`
- `min`
- `open`
- `reversed`
- `split`
- `startswith`
- `strftime`
- `strip`
- `super`

### `features\chat\enhancers\enhancement_service.py`

**Function Calls:**
- `endswith`
- `len`
- `reversed`

### `features\chat\summarization\summarization_service.py`

**Function Calls:**
- `RequestComplexityAnalyzer`
- `Signal`
- `__init__`
- `any`
- `join`
- `len`
- `startswith`
- `str`
- `strip`
- `super`
- `upper`

### `features\memory\memory_service.py`

**Function Calls:**
- `FileNotFoundError`
- `LongTermMemoryEntry`
- `LongTermMemoryService`
- `MemoryEntry`
- `SemanticSearchService`
- `ShortTermMemoryService`
- `Signal`
- `__init__`
- `asdict`
- `encode`
- `getattr`
- `hasattr`
- `hexdigest`
- `isinstance`
- `isoformat`
- `len`
- `list`
- `min`
- `open`
- `set`
- `str`
- `super`
- `timedelta`

### `features\memory\semantic_search.py`

**Function Calls:**
- `QMutex`
- `SentenceTransformer`
- `Signal`
- `VectorizedMemory`
- `__init__`
- `cosine_similarity`
- `enumerate`
- `isoformat`
- `len`
- `max`
- `min`
- `next`
- `open`
- `str`
- `sum`
- `super`

### `features\memory\semantic_search_fallback.py`

**Function Calls:**
- `QMutex`
- `Signal`
- `SimpleMemory`
- `__init__`
- `isoformat`
- `len`
- `max`
- `min`
- `next`
- `open`
- `set`
- `str`
- `sum`
- `super`

### `features\ollama\ollama_chat.py`

**Function Calls:**
- `AppLifecycleManager`
- `ChatController`
- `ConfigManager`
- `EventBus`
- `ServiceManager`
- `UIManager`
- `__init__`
- `showEvent`
- `super`

### `features\ollama\ollama_service.py`

**Function Calls:**
- `DataProcessingTask`
- `Exception`
- `Signal`
- `__init__`
- `get`
- `get_global_persistent_thread_pool`
- `get_global_threading_service`
- `hasattr`
- `insert`
- `isinstance`
- `iter`
- `join`
- `len`
- `map`
- `next`
- `reversed`
- `set`
- `str`
- `super`
- `type`

### `features\personality\formatter.py`

**Function Calls:**
- `PersonalityConfig`
- `PersonalityMetadata`
- `PersonalityPrompt`
- `PersonalityPronouns`
- `PersonalityTraits`
- `enumerate`
- `get`
- `join`

### `features\personality\loader.py`

**Function Calls:**
- `PersonalityConfig`
- `PersonalityMetadata`
- `asdict`
- `isoformat`
- `len`
- `open`
- `sorted`
- `strftime`

### `features\personality\models\personality_model.py`

**Function Calls:**
- `RuntimeError`
- `__init__`
- `get_custom_personalities`
- `get_system_personalities`
- `keys`
- `list`
- `str`
- `super`

### `features\personality\models\personality_pronouns.py`

**Function Calls:**
- `isinstance`
- `join`
- `len`

### `features\personality\services\personality_service.py`

**Function Calls:**
- `PersonalityConfig`
- `PersonalityFormatter`
- `PersonalityLoader`
- `PersonalityMetadata`
- `float`
- `get`
- `hasattr`
- `isoformat`
- `list`
- `lower`
- `set`
- `setattr`
- `sorted`

### `features\voice\audio\recording_service.py`

**Function Calls:**
- `Signal`
- `__init__`
- `calculate_eq_bars_pcm`
- `float`
- `join`
- `len`
- `log_thread_info`
- `max`
- `range`
- `str`
- `strftime`
- `sum`
- `super`

### `features\voice\orchestrator\voice_process_manager.py`

**Function Calls:**
- `QApplication`
- `Signal`
- `VoiceProcessManager`
- `VoiceProcessMonitor`
- `__init__`
- `hasattr`
- `id`
- `objectName`
- `safe_process_events_alternative`
- `str`
- `super`

### `features\voice\stt\stt_service.py`

**Function Calls:**
- `Exception`
- `KaldiRecognizer`
- `Model`
- `Signal`
- `__init__`
- `get`
- `join`
- `len`
- `print`
- `str`
- `strip`
- `super`

### `features\voice\tts\streaming_audio_player.py`

**Function Calls:**
- `Signal`
- `__init__`
- `calculate_eq_bars`
- `float`
- `len`
- `max`
- `min`
- `range`
- `str`
- `sum`
- `super`

### `features\voice\tts\streaming_audio_worker.py`

**Function Calls:**
- `Signal`
- `__init__`
- `enumerate`
- `int`
- `isinstance`
- `len`
- `str`
- `super`

### `features\voice\tts\tts_service.py`

**Function Calls:**
- `Signal`
- `TTSService`
- `__init__`
- `int`
- `len`
- `max`
- `min`
- `str`
- `super`

### `features\voice\voice_service.py`

**Function Calls:**
- `Exception`
- `QTimer`
- `RecordingService`
- `STTService`
- `Signal`
- `VoiceService`
- `__init__`
- `any`
- `get_global_persistent_thread_pool`
- `get_global_threading_service`
- `hasattr`
- `len`
- `log_thread_info`
- `max`
- `print`
- `set`
- `setattr`
- `str`
- `super`

### `features\voice\voice_service_manager.py`

**Function Calls:**
- `Exception`
- `Signal`
- `VoiceServiceManager`
- `__init__`
- `__new__`
- `callback`
- `hasattr`
- `str`
- `super`
- `type`

### `features\voice\voice_service_wrapper.py`

**Function Calls:**
- `QTimer`
- `Signal`
- `__init__`
- `create_voice_process_manager`
- `hasattr`
- `super`

### `startup\dependency_checker.py`

**Function Calls:**
- `DependencyChecker`
- `getattr`
- `hasattr`
- `join`
- `len`
- `lower`
- `print`
- `split`
- `str`

### `startup\install_dependencies.py`

**Function Calls:**
- `ensure_system_dependencies`
- `install_python_requirements`
- `main`
- `print`

### `startup\python_installer.py`

**Function Calls:**
- `print`

### `startup\system_installer.py`

**Function Calls:**
- `input`
- `is_admin`
- `lower`
- `offer_add_espeak_to_path`
- `print`
- `strip`

### `ui\Widgets\chat_navigation.py`

**Function Calls:**
- `QFont`
- `QFrame`
- `QHBoxLayout`
- `QLabel`
- `QListWidget`
- `QListWidgetItem`
- `QMenu`
- `QPushButton`
- `QVBoxLayout`
- `Signal`
- `__init__`
- `hasattr`
- `len`
- `print`
- `str`
- `super`

### `ui\Widgets\complexity_widget.py`

**Function Calls:**
- `QColor`
- `QFont`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QProgressBar`
- `QPushButton`
- `QTextEdit`
- `QVBoxLayout`
- `RequestComplexityAnalyzer`
- `Signal`
- `__init__`
- `getattr`
- `hasattr`
- `int`
- `join`
- `min`
- `str`
- `super`
- `title`

### `ui\Widgets\message_editor.py`

**Function Calls:**
- `QFrame`
- `QHBoxLayout`
- `QLabel`
- `QPushButton`
- `QTextEdit`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `strip`
- `super`

### `ui\Widgets\spellchecker_widget.py`

**Function Calls:**
- `QAction`
- `QColor`
- `QMenu`
- `QTextCharFormat`
- `QTimer`
- `__init__`
- `find`
- `keyPressEvent`
- `strip`
- `super`

### `ui\dialogs\coqui_model_dialog.py`

**Function Calls:**
- `ModelDownloadThread`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QListWidget`
- `QListWidgetItem`
- `QProgressBar`
- `QPushButton`
- `QSplitter`
- `QTextEdit`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `len`
- `maximum`
- `replace`
- `setValue`
- `split`
- `str`
- `strftime`
- `super`

### `ui\dialogs\error_dialog.py`

**Function Calls:**
- `DetailedErrorDialog`
- `ErrorDialog`
- `QClipboard`
- `QFont`
- `QHBoxLayout`
- `QLabel`
- `QPushButton`
- `QTextEdit`
- `QVBoxLayout`
- `__init__`
- `accept`
- `super`

### `ui\dialogs\settings_dialog.py`

**Function Calls:**
- `QCheckBox`
- `QComboBox`
- `QFormLayout`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QPushButton`
- `QSpinBox`
- `QTabWidget`
- `QVBoxLayout`
- `QWidget`
- `__init__`
- `int`
- `str`
- `super`

### `ui\dialogs\voice_settings_dialog.py`

**Function Calls:**
- `CalibrateSilenceThresholdDialog`
- `InternetCheckThread`
- `QCheckBox`
- `QComboBox`
- `QDoubleSpinBox`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QProgressBar`
- `QPushButton`
- `QSpinBox`
- `QTabWidget`
- `QTimer`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `any`
- `bool`
- `currentText`
- `float`
- `getattr`
- `hasattr`
- `int`
- `isChecked`
- `len`
- `max`
- `min`
- `range`
- `replace`
- `safe_disconnect`
- `safe_get_checked`
- `safe_get_text`
- `safe_get_value`
- `safe_process_events_alternative`
- `safe_ui_update`
- `split`
- `str`
- `sum`
- `super`
- `test_internet_connection`
- `value`

### `ui\tabs\chat_tab\chat_display.py`

**Function Calls:**
- `ChatRenderer`
- `Exception`
- `QDialog`
- `QHBoxLayout`
- `QLabel`
- `QPushButton`
- `QScrollArea`
- `QTextEdit`
- `QVBoxLayout`
- `Signal`
- `StreamingHandler`
- `__init__`
- `enumerate`
- `hasattr`
- `join`
- `len`
- `mouseMoveEvent`
- `show_error_dialog`
- `show_operation_error`
- `show_validation_error`
- `startswith`
- `strip`
- `super`

### `ui\tabs\chat_tab\chat_renderer.py`

**Function Calls:**
- `QTimer`
- `Signal`
- `__init__`
- `any`
- `escape`
- `join`
- `len`
- `reversed`
- `str`
- `super`
- `thread`

### `ui\tabs\chat_tab\chat_tab.py`

**Function Calls:**
- `ChatDisplay`
- `ChatNavigationWidget`
- `EQVisualizer`
- `InputControls`
- `QHBoxLayout`
- `QLabel`
- `QPushButton`
- `QSplitter`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `VoiceControls`
- `VoiceSettingsDialog`
- `__init__`
- `deleteLater`
- `get`
- `getattr`
- `hasattr`
- `hide`
- `int`
- `isEnabled`
- `isVisible`
- `isinstance`
- `len`
- `open`
- `print`
- `range`
- `safe_process_events_alternative`
- `setEnabled`
- `setValue`
- `setVisible`
- `setattr`
- `show`
- `str`
- `super`
- `update`
- `upper`

### `ui\tabs\chat_tab\eq_visualizer.py`

**Function Calls:**
- `BarEQWidget`
- `CircleEQWidget`
- `CircularGradientEQWidget`
- `CircularNetEQWidget`
- `Signal`
- `__init__`
- `enumerate`
- `hasattr`
- `isinstance`
- `len`
- `list`
- `max`
- `min`
- `safe_process_events_alternative`
- `super`
- `type`

### `ui\tabs\chat_tab\input_controls.py`

**Function Calls:**
- `QComboBox`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QPushButton`
- `QSlider`
- `QTextEdit`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `eventFilter`
- `safe_process_events_alternative`
- `str`
- `strip`
- `super`

### `ui\tabs\chat_tab\voice_controls.py`

**Function Calls:**
- `QLabel`
- `QMutex`
- `QMutexLocker`
- `QProgressBar`
- `QPushButton`
- `QTimer`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `abs`
- `any`
- `delattr`
- `get_voice_service_manager`
- `hasattr`
- `id`
- `int`
- `len`
- `log_thread_info`
- `max`
- `min`
- `print`
- `range`
- `safe_signal_connect`
- `safe_signal_disconnect`
- `set`
- `str`
- `strip`
- `super`
- `type`

### `ui\tabs\memory_tab.py`

**Function Calls:**
- `QCheckBox`
- `QComboBox`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QLineEdit`
- `QListWidget`
- `QListWidgetItem`
- `QPushButton`
- `QSlider`
- `QSpinBox`
- `QTabWidget`
- `QTableWidget`
- `QTableWidgetItem`
- `QTextEdit`
- `QVBoxLayout`
- `QWidget`
- `__init__`
- `encode`
- `enumerate`
- `hasattr`
- `hexdigest`
- `items`
- `join`
- `len`
- `next`
- `safe_disconnect`
- `setSectionResizeMode`
- `sorted`
- `str`
- `strftime`
- `super`
- `text`

### `ui\tabs\model_tab.py`

**Function Calls:**
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QLineEdit`
- `QListWidget`
- `QProgressBar`
- `QPushButton`
- `QSplitter`
- `QTextEdit`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `hasattr`
- `len`
- `strftime`
- `strip`
- `super`

### `ui\tabs\personality_tab.py`

**Function Calls:**
- `PersonalityConfig`
- `PersonalityMetadata`
- `PersonalityModel`
- `PersonalityPrompt`
- `PersonalityTraits`
- `QCheckBox`
- `QComboBox`
- `QDoubleSpinBox`
- `QFormLayout`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QLineEdit`
- `QListWidget`
- `QPushButton`
- `QScrollArea`
- `QSpinBox`
- `QTabWidget`
- `QTextEdit`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `isoformat`
- `join`
- `sorted`
- `str`
- `strip`
- `super`

### `ui\themes\message_formatter.py`

**Function Calls:**
- `HtmlFormatter`
- `enumerate`
- `escape`
- `get_lexer_by_name`
- `guess_lexer`
- `highlight`
- `join`
- `len`
- `startswith`
- `strip`
- `unescape`

### `ui\ui_manager.py`

**Function Calls:**
- `ChatTab`
- `MemoryTab`
- `ModelTab`
- `PersonalityTab`
- `QAction`
- `QStatusBar`
- `QTabWidget`
- `QVBoxLayout`
- `QWidget`
- `hasattr`

### `ui\utils\message_utils.py`

**Function Calls:**
- `ErrorDialog`
- `show_critical_error`
- `show_error_dialog`
- `str`

### `ui\visualizers\widgets\bar_eq_widget.py`

**Function Calls:**
- `QBrush`
- `QColor`
- `QLinearGradient`
- `QPainter`
- `QTimer`
- `Slot`
- `__init__`
- `enumerate`
- `float`
- `int`
- `isinstance`
- `len`
- `max`
- `min`
- `range`
- `super`

### `ui\visualizers\widgets\circle_eq_widget.py`

**Function Calls:**
- `QBrush`
- `QColor`
- `QPainter`
- `QRadialGradient`
- `QTimer`
- `Slot`
- `__init__`
- `enumerate`
- `float`
- `int`
- `isinstance`
- `len`
- `max`
- `min`
- `range`
- `super`

### `ui\visualizers\widgets\circular_gradient_eq_widget.py`

**Function Calls:**
- `QBrush`
- `QColor`
- `QPainter`
- `QPainterPath`
- `QPen`
- `QRadialGradient`
- `QTimer`
- `Slot`
- `__init__`
- `enumerate`
- `float`
- `isinstance`
- `len`
- `max`
- `min`
- `range`
- `sum`
- `super`

### `ui\visualizers\widgets\circular_net_eq_widget.py`

**Function Calls:**
- `QColor`
- `QPainter`
- `QTimer`
- `Slot`
- `__init__`
- `enumerate`
- `float`
- `int`
- `isinstance`
- `len`
- `max`
- `min`
- `range`
- `super`


### Method Calls

**`app\app_lifecycle.py`:**
- `CustomLogger.get_logger`
- `QApplication.processEvents`
- `QFileDialog.getOpenFileName`
- `data.get`
- `error_msg.exec`
- `error_msg.setIcon`
- `error_msg.setInformativeText`
- `error_msg.setText`
- `error_msg.setWindowTitle`
- `event.accept`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `msg_box.addButton`
- `msg_box.clickedButton`
- `msg_box.exec`
- `msg_box.setIcon`
- `msg_box.setInformativeText`
- `msg_box.setText`
- `msg_box.setTextFormat`
- `msg_box.setTextInteractionFlags`
- `msg_box.setWindowTitle`
- `ollama_service.test_connection`
- `os.access`
- `os.getenv`
- `os.path.basename`
- `os.path.exists`
- `os.path.getsize`
- `os.path.isabs`
- `platform.system`
- `progress.activateWindow`
- `progress.close`
- `progress.raise_`
- `progress.setAutoClose`
- `progress.setLabelText`
- `progress.setMinimumDuration`
- `progress.setModal`
- `progress.setValue`
- `progress.setWindowTitle`
- `progress.show`
- `progress.wasCanceled`
- `requests.get`
- `requests.post`
- `response.json`
- `self._find_ollama_executable`
- `self._is_ollama_installed`
- `self._reset_ollama_restart_attempts`
- `self._show_custom_path_dialog`
- `self._show_initialization_error`
- `self._start_ollama_background`
- `self._stop_ollama_process`
- `self._validate_ollama_executable`
- `self._verify_ollama_installation`
- `self.check_ollama_connection`
- `self.event_handler._on_refresh_models`
- `self.get_available_models`
- `self.get_close_ollama_on_exit`
- `self.get_custom_ollama_path`
- `self.get_ollama_process_info`
- `self.is_ollama_running`
- `self.main_window.close`
- `self.main_window.isVisible`
- `self.main_window.resize`
- `self.main_window.show`
- `self.main_window.size`
- `self.ollama_crash_detection_timer.start`
- `self.ollama_crash_detection_timer.stop`
- `self.ollama_crash_detection_timer.timeout.connect`
- `self.ollama_process.kill`
- `self.ollama_process.poll`
- `self.ollama_process.stdout.read`
- `self.ollama_process.terminate`
- `self.ollama_process.wait`
- `self.reset_ollama_error_shown`
- `self.service_manager.config_manager.get`
- `self.service_manager.config_manager.get_window_size`
- `self.service_manager.config_manager.save_config`
- `self.service_manager.config_manager.set`
- `self.service_manager.config_manager.set_window_size`
- `self.service_manager.get_ollama_service`
- `self.show_ollama_connection_error`
- `self.start_ollama_manually`
- `self.ui_manager.apply_theme`
- `shutil.which`
- `size.height`
- `size.width`
- `subprocess.Popen`
- `subprocess.run`
- `success_msg.exec`
- `success_msg.setIcon`
- `success_msg.setInformativeText`
- `success_msg.setText`
- `success_msg.setWindowTitle`
- `threading.Thread`
- `time.sleep`
- `traceback.format_exc`
- `wait_thread.is_alive`
- `wait_thread.join`
- `wait_thread.start`
- `webbrowser.open`

**`app\event_bus.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_debug`
- `LoggingHelpers.log_error`
- `PromptFormatter.format_status_message`
- `QThread.currentThread`
- `QTimer.singleShot`
- `about_action.triggered.connect`
- `chat_tab.append_response_chunk`
- `chat_tab.append_to_chat`
- `chat_tab.chat_display._sync_messages_from_conversation_service`
- `chat_tab.chat_display.sync_messages_from_conversation_service`
- `chat_tab.clear_chat`
- `chat_tab.conversation_deleted.connect`
- `chat_tab.conversation_renamed.connect`
- `chat_tab.conversation_selected.connect`
- `chat_tab.force_enable_send_button`
- `chat_tab.get_current_model`
- `chat_tab.get_temperature`
- `chat_tab.load_chat`
- `chat_tab.load_conversation`
- `chat_tab.message_cancelled.connect`
- `chat_tab.message_sent.connect`
- `chat_tab.new_conversation_requested.connect`
- `chat_tab.on_personality_changed`
- `chat_tab.personality_combo.setCurrentText`
- `chat_tab.refresh_navigation`
- `chat_tab.save_chat`
- `chat_tab.set_current_conversation_file`
- `chat_tab.start_streaming`
- `chat_tab.stop_streaming`
- `chat_tab.update_model_list`
- `chat_tab.update_personality_list`
- `cleaned_messages.append`
- `clear_chat_action.triggered.connect`
- `conversation_manager.get_current_metadata`
- `conversation_manager.load_conversation`
- `conversation_manager.metadata_updated.connect`
- `conversation_service.auto_save_completed.connect`
- `conversation_service.clear_conversation`
- `dialog.exec`
- `error.lower`
- `exit_action.triggered.connect`
- `load_chat_action.triggered.connect`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `main_window.statusBar`
- `message.get`
- `metadata.get_display_info`
- `model_tab.append_status`
- `model_tab.model_pull_requested.connect`
- `model_tab.model_remove_requested.connect`
- `model_tab.model_update_requested.connect`
- `model_tab.update_model_list`
- `msg_box.exec`
- `msg_box.setIcon`
- `msg_box.setText`
- `msg_box.setTextFormat`
- `msg_box.setTextInteractionFlags`
- `msg_box.setWindowTitle`
- `new_conversation_action.triggered.connect`
- `ollama_service.cancel_request`
- `ollama_service.get_models`
- `ollama_service.model_list_updated.connect`
- `ollama_service.model_operation_error.connect`
- `ollama_service.model_operation_progress.connect`
- `ollama_service.test_connection`
- `os.path.basename`
- `personality_tab.get_available_personalities`
- `personality_tab.personality_changed.connect`
- `personality_tab.personality_model.get_available_personalities`
- `refresh_models_action.triggered.connect`
- `save_chat_action.triggered.connect`
- `self._chat_tab_retry_timer.setSingleShot`
- `self._chat_tab_retry_timer.start`
- `self._chat_tab_retry_timer.timeout.connect`
- `self._check_ollama_connection`
- `self._clean_messages_for_ollama`
- `self._cleanup_worker_thread`
- `self._cleanup_worker_thread_once`
- `self._connect_chat_tab_signals`
- `self._connect_menu_actions`
- `self._create_chat_controller`
- `self._handle_chat_error_safe`
- `self._handle_chat_finished`
- `self._handle_worker_error_safe`
- `self._on_error_occurred`
- `self._on_new_conversation`
- `self._on_refresh_models`
- `self._on_refresh_personalities`
- `self._on_worker_finished`
- `self._send_to_ollama`
- `self._setup_chat_tab_retry`
- `self._setup_connections`
- `self._setup_ui_with_new_services`
- `self._show_ollama_connection_error`
- `self._start_worker_after_streaming_message`
- `self._update_chat_display_safe`
- `self._update_progress_safe`
- `self.chat_controller._select_model`
- `self.chat_controller.accumulate_assistant_response`
- `self.chat_controller.conversation_service.finalize_streaming_message`
- `self.chat_controller.conversation_service.get_context_messages`
- `self.chat_controller.conversation_updated.connect`
- `self.chat_controller.delete_conversation`
- `self.chat_controller.error_occurred.connect`
- `self.chat_controller.error_occurred.emit`
- `self.chat_controller.finalize_streaming_response`
- `self.chat_controller.handle_ai_response`
- `self.chat_controller.load_conversation`
- `self.chat_controller.message_received.connect`
- `self.chat_controller.name_generation_requested.connect`
- `self.chat_controller.process_user_message`
- `self.chat_controller.start_new_conversation`
- `self.chat_controller.start_streaming_response`
- `self.chat_controller.status_updated.connect`
- `self.lifecycle_manager.get_ollama_error_shown`
- `self.lifecycle_manager.set_ollama_error_shown`
- `self.lifecycle_manager.show_ollama_connection_error`
- `self.model_update_timer.setSingleShot`
- `self.model_update_timer.timeout.connect`
- `self.service_manager.config_manager.get`
- `self.service_manager.get_conversation_manager`
- `self.service_manager.get_conversation_service`
- `self.service_manager.get_enhancement_service`
- `self.service_manager.get_memory_service`
- `self.service_manager.get_ollama_service`
- `self.service_manager.get_session_variables`
- `self.service_manager.get_summarization_service`
- `self.service_manager.is_memory_enabled`
- `self.service_manager.reinitialize_services`
- `self.threading_service.chat_streaming_thread.isRunning`
- `self.threading_service.chat_streaming_thread.terminate`
- `self.threading_service.chat_streaming_thread.wait`
- `self.threading_service.chunk_received.connect`
- `self.threading_service.cleanup`
- `self.threading_service.error.connect`
- `self.threading_service.finalize`
- `self.threading_service.finished.connect`
- `self.threading_service.get_threading_status`
- `self.threading_service.progress_updated.connect`
- `self.threading_service.start_chat_streaming`
- `self.threading_service.stop_chat_streaming`
- `self.ui_manager.get_chat_tab`
- `self.ui_manager.get_main_window`
- `self.ui_manager.get_menu_action`
- `self.ui_manager.get_model_tab`
- `self.ui_manager.get_personality_tab`
- `self.ui_manager.show_about_dialog`
- `self.ui_manager.show_clear_chat_dialog`
- `self.ui_manager.update_status`
- `settings_action.triggered.connect`
- `signal.connect`
- `signal.disconnect`
- `summarization_service.generate_chat_name`
- `time.sleep`
- `traceback.format_exc`

**`app\main.py`:**
- `CustomLogger.get_logger`
- `chat_tab.set_chat_controller`
- `logger.error`
- `logger.info`
- `logger.warning`
- `self._setup_connections`
- `self._setup_ui`
- `self.chat_controller.set_chat_tab_reference`
- `self.event_handler.reconnect_chat_tab_signals`
- `self.event_handler.setup_connections`
- `self.lifecycle_manager.check_ollama_connection`
- `self.lifecycle_manager.handle_close_event`
- `self.lifecycle_manager.handle_show_event`
- `self.lifecycle_manager.initialize_application`
- `self.lifecycle_manager.show_ollama_connection_error`
- `self.service_manager.get_conversation_manager`
- `self.service_manager.get_conversation_service`
- `self.service_manager.get_enhancement_service`
- `self.service_manager.get_memory_service`
- `self.service_manager.get_ollama_service`
- `self.service_manager.get_personality_service`
- `self.service_manager.get_summarization_service`
- `self.service_manager.is_memory_enabled`
- `self.ui_manager.get_chat_tab`
- `self.ui_manager.setup_menu_bar`
- `self.ui_manager.setup_ui`
- `traceback.format_exc`
- `traceback.print_exc`

**`app\service_manager.py`:**
- `CustomLogger.get_logger`
- `logger.error`
- `logger.info`
- `logger.warning`
- `self._initialize_services`
- `self.config_manager.get`
- `self.config_manager.get_history_directory`
- `self.config_manager.get_max_context_messages`
- `self.config_manager.get_ollama_url`
- `self.config_manager.is_history_enabled`
- `self.config_manager.is_json_format_enabled`
- `self.config_manager.is_think_enabled`
- `self.config_manager.is_verbose_enabled`
- `self.config_manager.is_wordwrap_enabled`
- `self.conversation_service.set_conversation_manager`
- `self.conversation_service.set_memory_service`
- `self.get_voice_service`
- `self.session_variables.copy`
- `self.voice_service_manager.cleanup`
- `self.voice_service_manager.get_voice_service`
- `self.voice_service_manager.is_ready`
- `threading.Lock`

**`app\threading_integration.py`:**
- `CustomLogger.get_logger`
- `logger.debug`
- `logger.error`
- `self.event_handler._on_worker_chunk`
- `self.event_handler._on_worker_error`
- `self.event_handler._on_worker_finished`
- `self.event_handler._on_worker_progress`
- `self.threading_integration.chunk_received.connect`
- `self.threading_integration.error.connect`
- `self.threading_integration.finished.connect`
- `self.threading_integration.get_threading_status`
- `self.threading_integration.progress_updated.connect`
- `self.threading_integration.start_chat_streaming`
- `self.threading_integration.stop_chat_streaming`
- `self.threading_service.chunk_received.connect`
- `self.threading_service.error.connect`
- `self.threading_service.finished.connect`
- `self.threading_service.get_threading_status`
- `self.threading_service.process_file_operation`
- `self.threading_service.process_message`
- `self.threading_service.progress_updated.connect`
- `self.threading_service.start_chat_streaming`
- `self.threading_service.stop_chat_streaming`

**`config\config_manager.py`:**
- `CustomLogger.get_logger`
- `default.copy`
- `json.dump`
- `json.load`
- `key.split`
- `loaded.items`
- `logger.debug`
- `os.path.exists`
- `self.config.get`
- `self.get`
- `self.load_config`
- `self.merge_configs`
- `self.save_config`
- `self.set`
- `size.get`

**`core\logging\helpers.py`:**
- `CustomLogger.get_logger`
- `QThread.currentThread`
- `current_thread.objectName`
- `get_thread_monitor._instance.cleanup`
- `logger.critical`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `self._on_thread_finished`
- `self._on_thread_started`
- `self.active_threads.clear`
- `self.active_threads.copy`
- `self.active_threads.get`
- `self.active_threads.values`
- `self.get_thread_stats`
- `self.thread_finished.emit`
- `self.thread_history.append`
- `self.thread_history.clear`
- `self.thread_history.copy`
- `self.thread_started.emit`
- `target_thread.objectName`
- `thread.finished.connect`
- `thread.isRunning`
- `thread.objectName`
- `thread.priority`
- `thread.stackSize`
- `thread.started.connect`
- `time.time`
- `traceback.format_exc`
- `type_counts.get`

**`core\logging\logger.py`:**
- `QThread.currentThread`
- `c.isalnum`
- `cls._check_config_for_logging`
- `cls._clear_log_file`
- `cls._cleared_files.add`
- `config.get`
- `emoji_pattern.sub`
- `file_handler.setFormatter`
- `json.load`
- `logger.addHandler`
- `logger.setLevel`
- `logging.FileHandler`
- `logging.getLogger`
- `os.makedirs`
- `os.path.abspath`
- `os.path.dirname`
- `os.path.exists`
- `os.path.join`
- `qt_thread.objectName`
- `re.compile`
- `re.sub`
- `self._filter_non_ascii`
- `self._print`
- `threading.current_thread`

**`core\models\conversation_metadata.py`:**
- `ConversationMetadata.from_dict`
- `CustomLogger.get_logger`
- `conversations.append`
- `conversations.sort`
- `created_dt.strftime`
- `data.get`
- `datetime.fromisoformat`
- `datetime.now`
- `filename.endswith`
- `json.dump`
- `json.load`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `metadata.to_dict`
- `metadata.update_ai_generated_name`
- `modified_dt.strftime`
- `os.listdir`
- `os.makedirs`
- `os.path.exists`
- `os.path.join`
- `os.path.splitext`
- `os.remove`
- `os.rename`
- `re.sub`
- `safe_name.endswith`
- `safe_name.strip`
- `self._create_safe_filename`
- `self.get_formatted_created_time`
- `self.list_conversations`
- `self.load_conversation`
- `self.metadata.reset`
- `self.metadata.to_dict`
- `self.metadata.update_ai_generated_name`
- `self.metadata.update_message_count`
- `self.metadata.update_timestamp`
- `self.metadata_updated.emit`
- `self.update_timestamp`

**`core\shared_imports\pyside_imports.py`:**
- `QApplication.instance`
- `QMetaObject.invokeMethod`
- `QThread.currentThread`
- `button.setEnabled`
- `combo_box.addItems`
- `label.setAlignment`
- `layout.setContentsMargins`
- `layout.setSpacing`
- `line_edit.setPlaceholderText`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `msg_box.setIcon`
- `msg_box.setStandardButtons`
- `msg_box.setText`
- `msg_box.setWindowTitle`
- `progress_bar.setMaximum`
- `progress_bar.setMinimum`
- `signal.connect`
- `signal.disconnect`
- `text_edit.setPlaceholderText`
- `timer.setInterval`
- `timer.setSingleShot`

**`core\threading\__init__.py`:**
- `CustomLogger.get_logger`
- `_global_persistent_thread_pool.shutdown`
- `_global_threading_service.cleanup`
- `logger.error`

**`core\threading\persistent_thread_config.py`:**
- `config.items`
- `config.values`
- `config_type.upper`
- `configs.get`
- `thread_config.get`

**`core\threading\persistent_thread_pool.py`:**
- `CustomLogger.get_logger`
- `_global_persistent_thread_pool.shutdown`
- `idle_threads.clear`
- `idle_threads.pop`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `self._create_active_thread`
- `self._create_idle_thread`
- `self.active_threads.clear`
- `self.active_threads.items`
- `self.active_threads.values`
- `self.cleanup_timer.start`
- `self.cleanup_timer.stop`
- `self.cleanup_timer.timeout.connect`
- `self.idle_threads.items`
- `self.pool_config.keys`
- `self.thread_available.emit`
- `self.thread_busy.emit`
- `thread.deleteLater`
- `thread.isRunning`
- `thread.objectName`
- `thread.quit`
- `thread.setObjectName`
- `thread.start`
- `thread.wait`
- `thread.worker._configuration.get`
- `thread.worker._configuration.keys`
- `thread.worker.reset_state`
- `thread_monitor.register_thread`
- `thread_type.capitalize`
- `time.sleep`
- `time.time`
- `traceback.format_exc`
- `worker.moveToThread`

**`core\threading\qrunnable_tasks.py`:**
- `CustomLogger.get_logger`
- `QApplication.instance`
- `QObject.__init__`
- `QRunnable.__init__`
- `c.isdigit`
- `c.islower`
- `c.isupper`
- `content.split`
- `content.splitlines`
- `corrected_words.append`
- `corrections_made.append`
- `data.keys`
- `data.values`
- `f.read`
- `f.write`
- `factors.append`
- `json.loads`
- `line.strip`
- `logger.debug`
- `logger.error`
- `logger.info`
- `m.group`
- `model_data.get`
- `ollama.delete`
- `ollama.pull`
- `os.path.exists`
- `process.stdout.close`
- `process.terminate`
- `process.wait`
- `re.findall`
- `re.sub`
- `result.append`
- `self._analyze_data`
- `self._analyze_sentiment`
- `self._calculate_data`
- `self._calculate_fibonacci`
- `self._calculate_prime_factors`
- `self._calculate_statistics`
- `self._count_nested_levels`
- `self._format_message`
- `self._handle_model_operation`
- `self._process_file`
- `self._read_file`
- `self._spell_check_message`
- `self._transform_data`
- `self._write_file`
- `self.callback`
- `self.data.keys`
- `self.data.lower`
- `self.data.split`
- `self.data.splitlines`
- `self.data.upper`
- `self.error_occurred.emit`
- `self.kwargs.get`
- `self.message.lower`
- `self.message.split`
- `self.operation.startswith`
- `self.parameters.get`
- `self.result_ready.emit`
- `self.setAutoDelete`
- `self.target`
- `self.update_complete.emit`
- `self.update_error.emit`
- `subprocess.Popen`
- `time.time`
- `traceback.format_exc`
- `word.lower`
- `words.intersection`

**`core\threading\qthread_workers.py`:**
- `CustomLogger.get_logger`
- `QThread.currentThread`
- `config_manager.get_frequency_penalty`
- `config_manager.get_max_tokens`
- `config_manager.get_ollama_url`
- `config_manager.get_presence_penalty`
- `config_manager.get_top_p`
- `current_thread.objectName`
- `data.get`
- `json.loads`
- `kwargs.keys`
- `line.decode`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `psutil.cpu_percent`
- `psutil.disk_usage`
- `psutil.virtual_memory`
- `requests.post`
- `response.iter_lines`
- `self._configuration.get`
- `self._configuration.keys`
- `self._configuration.update`
- `self._log_thread_info`
- `self._stream_operation`
- `self.alert_triggered.emit`
- `self.chunk_received.emit`
- `self.error.emit`
- `self.finished.emit`
- `self.progress_updated.emit`
- `self.resource_updated.emit`
- `time.sleep`
- `time.time`
- `traceback.format_exc`

**`core\threading\thread_calculator.py`:**
- `CustomLogger.get_logger`
- `logger.error`
- `logger.info`
- `logging.basicConfig`
- `logging.getLogger`
- `os.cpu_count`
- `platform.system`
- `pool_recommendations.get`
- `psutil.cpu_count`
- `psutil.virtual_memory`
- `self._calculate_memory_safe_threads`
- `self._calculate_recommendations`
- `self.calculate_thread_recommendations`
- `self.get_recommendations_for_pool`
- `self.get_system_info`
- `thread_calculator.calculate_thread_recommendations`
- `thread_calculator.get_recommendations_for_pool`
- `thread_calculator.print_system_analysis`

**`core\threading\thread_calculator_examples.py`:**
- `os.path.dirname`
- `os.path.join`
- `persistent_pool.initialize_pool`
- `psutil.cpu_percent`
- `psutil.virtual_memory`
- `streaming_config.items`
- `sys.path.insert`

**`core\threading\thread_monitor.py`:**
- `CustomLogger.get_logger`
- `_global_thread_monitor.shutdown`
- `error.get`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `psutil.cpu_percent`
- `psutil.virtual_memory`
- `running_threads.append`
- `self._on_thread_finished`
- `self._on_thread_started`
- `self.active_threads.copy`
- `self.active_threads.items`
- `self.active_threads.keys`
- `self.active_threads.values`
- `self.cleanup_old_history`
- `self.generate_report`
- `self.get_resource_usage`
- `self.monitor_timer.start`
- `self.monitor_timer.stop`
- `self.monitor_timer.timeout.connect`
- `self.resource_usage_updated.emit`
- `self.stats.copy`
- `self.thread_error.emit`
- `self.thread_errors.append`
- `self.thread_errors.copy`
- `self.thread_finished.emit`
- `self.thread_history.append`
- `self.thread_history.copy`
- `self.thread_registered.emit`
- `self.thread_started.emit`
- `thread.copy`
- `thread.finished.connect`
- `thread.get`
- `thread.isRunning`
- `thread.objectName`
- `thread.priority`
- `thread.stackSize`
- `thread.started.connect`
- `thread_info.get`
- `thread_types.get`
- `time.sleep`
- `time.time`
- `traceback.format_exc`

**`core\threading\thread_pool_manager.py`:**
- `CustomLogger.get_logger`
- `_global_thread_pool_manager.shutdown`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `self.active_tasks.keys`
- `self.cancel_all_tasks`
- `self.cancel_task`
- `self.cleanup_old_tasks`
- `self.completed_tasks.append`
- `self.failed_tasks.append`
- `self.get_pool_status`
- `self.monitor_timer.start`
- `self.monitor_timer.stop`
- `self.monitor_timer.timeout.connect`
- `self.pool_status_updated.emit`
- `self.task_completed.emit`
- `self.task_failed.emit`
- `self.task_started.emit`
- `self.thread_pool.activeThreadCount`
- `self.thread_pool.maxThreadCount`
- `self.thread_pool.setMaxThreadCount`
- `self.thread_pool.start`
- `self.wait_for_all_tasks`
- `task.copy`
- `task.get`
- `time.sleep`
- `time.time`
- `traceback.format_exc`

**`core\threading\threading_service.py`:**
- `CustomLogger.get_logger`
- `_global_threading_service.cleanup`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `self._initialize_persistent_pools`
- `self.chunk_received.emit`
- `self.current_audio_thread.objectName`
- `self.current_audio_thread.worker.stop`
- `self.current_chat_thread.objectName`
- `self.current_chat_thread.worker.is_running`
- `self.current_chat_thread.worker.stop`
- `self.current_monitoring_thread.objectName`
- `self.current_monitoring_thread.worker.stop`
- `self.error.emit`
- `self.finished.emit`
- `self.persistent_thread_pool.get_pool_status`
- `self.persistent_thread_pool.get_thread`
- `self.persistent_thread_pool.initialize_pool`
- `self.persistent_thread_pool.return_thread`
- `self.progress_updated.emit`
- `self.stop_audio_streaming`
- `self.stop_chat_streaming`
- `self.stop_monitoring`
- `self.thread_monitor.get_resource_usage`
- `self.thread_pool_manager.get_pool_status`
- `self.thread_pool_manager.start_task`
- `thread.objectName`
- `time.sleep`
- `time.time`
- `traceback.format_exc`
- `worker.alert_triggered.connect`
- `worker.chunk_received.connect`
- `worker.configure_audio_streaming`
- `worker.configure_monitoring`
- `worker.configure_streaming`
- `worker.error.connect`
- `worker.finished.connect`
- `worker.progress_updated.connect`
- `worker.resource_updated.connect`
- `worker.start_audio_streaming`
- `worker.start_monitoring`
- `worker.start_streaming`

**`core\threading\usage_examples.py`:**
- `CustomLogger.get_logger`
- `app.cleanup`
- `app.get_threading_status`
- `app.process_file_operation`
- `app.process_message_formatting`
- `app.process_message_spell_check`
- `app.start_chat_streaming`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `result.get`
- `self.active_tasks.clear`
- `self.chat_streaming_thread.deleteLater`
- `self.chat_streaming_thread.finished.connect`
- `self.chat_streaming_thread.isRunning`
- `self.chat_streaming_thread.objectName`
- `self.chat_streaming_thread.quit`
- `self.chat_streaming_thread.setObjectName`
- `self.chat_streaming_thread.start`
- `self.chat_streaming_thread.started.connect`
- `self.chat_streaming_thread.terminate`
- `self.chat_streaming_thread.wait`
- `self.chat_streaming_worker.chunk_received.connect`
- `self.chat_streaming_worker.error.connect`
- `self.chat_streaming_worker.finished.connect`
- `self.chat_streaming_worker.is_running`
- `self.chat_streaming_worker.moveToThread`
- `self.chat_streaming_worker.progress_updated.connect`
- `self.chat_streaming_worker.start_streaming`
- `self.chat_streaming_worker.stop`
- `self.stop_chat_streaming`
- `self.thread_monitor.get_resource_usage`
- `self.thread_monitor.register_thread`
- `self.thread_monitor.unregister_thread`
- `self.thread_pool_manager.get_pool_status`
- `self.thread_pool_manager.start_task`
- `self.thread_pool_manager.wait_for_all_tasks`
- `time.time`
- `traceback.format_exc`

**`core\utils\error_handler.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_audio_operation`
- `LoggingHelpers.log_critical_error`
- `LoggingHelpers.log_exception_with_context`
- `LoggingHelpers.log_file_operation`
- `LoggingHelpers.log_json_parsing_error`
- `LoggingHelpers.log_memory_operation`
- `LoggingHelpers.log_network_request`
- `LoggingHelpers.log_performance_metric`
- `LoggingHelpers.log_ui_operation`
- `LoggingHelpers.log_warning_with_context`
- `f.read`
- `f.write`
- `functools.wraps`
- `json.loads`
- `os.makedirs`
- `os.path.dirname`
- `requests.request`
- `resource.cleanup`
- `resource.close`
- `time.sleep`
- `time.time`

**`core\utils\internet_checker.py`:**
- `failed_tests.append`
- `self.test_http_connection`
- `self.test_socket_connection`
- `socket.create_connection`
- `tester.test_connection`
- `tester.test_connection_with_details`
- `urllib.request.Request`
- `urllib.request.urlopen`

**`core\utils\prompts.py`:**
- `PromptTemplates.CONVERSATION.get`
- `PromptTemplates.ERRORS.get`
- `PromptTemplates.MEMORY.get`
- `PromptTemplates.MENU.get`
- `PromptTemplates.STATUS.get`
- `template.format`

**`core\utils\streaming_handler.py`:**
- `CustomLogger.get_logger`
- `editable.append`
- `logger.debug`
- `logger.error`
- `msg.get`
- `renderer.sync_messages_from_handler`
- `self._get_next_message_id`
- `self._request_render`
- `self._stream_timer.isActive`
- `self._stream_timer.setInterval`
- `self._stream_timer.stop`
- `self._stream_timer.timeout.connect`
- `self._typewriter_timer.isActive`
- `self._typewriter_timer.setInterval`
- `self._typewriter_timer.setSingleShot`
- `self._typewriter_timer.start`
- `self._typewriter_timer.timeout.connect`
- `self.message_edited.emit`
- `self.messages.append`
- `self.messages.clear`
- `self.messages.copy`
- `self.render_callback`
- `self.update_streaming_message`
- `traceback.format_exc`

**`core\utils\threading_audit.py`:**
- `CustomLogger.get_logger`
- `QApplication.instance`
- `audio_threads.append`
- `auditor.generate_report`
- `auditor.run_full_analysis`
- `breakdown.get`
- `f.write`
- `logger.error`
- `logger.info`
- `other_threads.append`
- `recommendations.append`
- `recommendations.extend`
- `report.append`
- `self._get_thread_breakdown`
- `self.analyze_current_threads`
- `self.check_thread_safety_patterns`
- `self.cross_thread_operations.append`
- `self.detect_cross_thread_ui_operations`
- `self.generate_recommendations`
- `self.generate_report`
- `self.run_full_analysis`
- `self.thread_info.items`
- `self.thread_info.values`
- `self.thread_safety_issues.append`
- `t.name.lower`
- `thread.is_alive`
- `thread.name.lower`
- `thread_breakdown.get`
- `thread_breakdown.items`
- `thread_type.capitalize`
- `threading.enumerate`
- `voice_threads.append`
- `worker_threads.append`

**`core\utils\threading_utils.py`:**
- `CustomLogger.get_logger`
- `QApplication.instance`
- `QMetaObject.invokeMethod`
- `QThread.currentThread`
- `QTimer.singleShot`
- `button.setEnabled`
- `button.setText`
- `button.setVisible`
- `button.update`
- `current_thread.objectName`
- `log_func.debug`
- `logger.debug`
- `logger.error`
- `main_thread.objectName`
- `self.callback`
- `signal.connect`
- `signal.disconnect`
- `signal.emit`
- `widget.repaint`
- `widget.setProperty`
- `widget.update`

**`features\chat\chat_controller.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_conversation_detection`
- `LoggingHelpers.log_debug`
- `LoggingHelpers.log_exception_with_context`
- `LoggingHelpers.log_fact_extraction_result`
- `LoggingHelpers.log_fact_extraction_start`
- `LoggingHelpers.log_fact_processing`
- `LoggingHelpers.log_fact_skipped`
- `LoggingHelpers.log_fact_storage_end`
- `LoggingHelpers.log_fact_storage_start`
- `LoggingHelpers.log_fact_storage_summary`
- `LoggingHelpers.log_llm_call`
- `LoggingHelpers.log_memory_ltm_status`
- `LoggingHelpers.log_memory_result`
- `LoggingHelpers.log_message_sent_end`
- `PromptFormatter.format_auto_model_selection_info`
- `PromptFormatter.format_error_message`
- `PromptFormatter.format_fact_extraction_prompt`
- `PromptFormatter.format_status_message`
- `analyzer.analyze_complexity`
- `analyzer.get_model_recommendation`
- `datetime.now`
- `emoji_pattern.sub`
- `facts.items`
- `json.loads`
- `json_match.group`
- `key.strip`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `message.strip`
- `metadata.get_display_info`
- `msg.get`
- `new_filepath.split`
- `old_filepath.split`
- `os.path.basename`
- `os.path.join`
- `re.compile`
- `re.search`
- `re.sub`
- `response.strip`
- `response_chunks.append`
- `response_content.strip`
- `result.get`
- `self._build_context`
- `self._chat_tab_reference.speak_ai_response`
- `self._detect_new_conversation`
- `self._extract_and_store_facts`
- `self._extract_facts_with_llm`
- `self._handle_memory_operations`
- `self._send_to_ollama`
- `self._store_extracted_facts`
- `self._trigger_name_generation`
- `self._trigger_tts_for_response`
- `self.clear_pending_assistant_response`
- `self.conversation_manager.auto_save_conversation`
- `self.conversation_manager.clear_current_conversation`
- `self.conversation_manager.find_blank_conversation`
- `self.conversation_manager.get_current_metadata`
- `self.conversation_manager.load_conversation`
- `self.conversation_service.add_message`
- `self.conversation_service.clear_conversation`
- `self.conversation_service.finalize_streaming_message`
- `self.conversation_service.get_message_by_id`
- `self.conversation_service.get_messages`
- `self.conversation_service.get_streaming_message_id`
- `self.conversation_service.get_streaming_message_with_content`
- `self.conversation_service.load_conversation`
- `self.conversation_service.start_streaming_message`
- `self.conversation_service.update_streaming_message`
- `self.conversation_updated.emit`
- `self.error_occurred.emit`
- `self.finalize_streaming_response`
- `self.is_memory_active`
- `self.memory_service.add_fact`
- `self.memory_service.get_context_messages`
- `self.memory_service.intelligent_add_message`
- `self.message_received.emit`
- `self.message_sent.emit`
- `self.name_generation_requested.emit`
- `self.ollama_service.get_models`
- `self.ollama_service.send_chat_message`
- `self.personality_service.get_ai_name`
- `self.start_new_conversation`
- `self.status_updated.emit`
- `traceback.format_exc`
- `value.strip`

**`features\chat\complexity_analyser\complexity_analyzer.py`:**
- `domains.values`
- `match.group`
- `metrics.level.value.replace`
- `re.findall`
- `re.search`
- `recommendations.append`
- `recommendations.extend`
- `report.strip`
- `self._analyze_ambiguity`
- `self._analyze_context_dependency`
- `self._analyze_knowledge_breadth`
- `self._analyze_output_complexity`
- `self._analyze_reasoning_depth`
- `self._count_constraints`
- `self._determine_complexity_level`
- `self._estimate_tokens`
- `self._generate_recommendations`
- `text.lower`
- `text.split`

**`features\chat\conversation_service.py`:**
- `CustomLogger.get_logger`
- `content.lower`
- `content.strip`
- `data.get`
- `datetime.now`
- `filename.replace`
- `json.load`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `message.get`
- `metadata.to_dict`
- `msg.get`
- `os.makedirs`
- `os.path.join`
- `self._add_to_memory`
- `self._get_next_message_id`
- `self.auto_save_completed.emit`
- `self.conversation.append`
- `self.conversation.copy`
- `self.conversation_manager.auto_save_conversation`
- `self.conversation_manager.load_conversation`
- `self.conversation_updated.emit`
- `self.finalize_streaming_message`
- `self.get_message_by_id`
- `self.memory_service.add_memory`
- `self.memory_service.get_context_messages`
- `tags.append`

**`features\chat\enhancers\enhancement_service.py`:**
- `response.split`
- `response.strip`
- `self.detect_follow_up_question`
- `sentence.strip`

**`features\chat\summarization\summarization_service.py`:**
- `CustomLogger.get_logger`
- `analyzer.analyze_complexity`
- `analyzer.get_model_recommendation`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `message.lower`
- `msg.get`
- `name.lower`
- `name.strip`
- `name.upper`
- `prefix.lower`
- `re.sub`
- `response.strip`
- `self._ai_evaluate_conversation_quality`
- `self._ai_evaluate_name_quality`
- `self._clean_generated_name`
- `self._create_summarization_prompt`
- `self._fallback_quality_check`
- `self._has_enough_substance`
- `self.ollama_service.get_models`
- `self.ollama_service.send_chat_message`
- `self.summarization_completed.emit`
- `self.summarization_failed.emit`

**`features\memory\memory_service.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_configuration_change`
- `LoggingHelpers.log_exception_with_context`
- `LoggingHelpers.log_file_operation`
- `LoggingHelpers.log_info_with_context`
- `LoggingHelpers.log_memory_operation`
- `LoggingHelpers.log_service_initialization`
- `LoggingHelpers.log_warning_with_context`
- `MemoryClassifier.classify_message`
- `MemoryRetriever.calculate_relevance`
- `MemoryRetriever.get_relevant_memories`
- `PronounNormalizer.FIRST_PERSON_CONTRACTIONS.items`
- `PronounNormalizer.FIRST_PERSON_PRONOUNS.items`
- `PronounNormalizer.normalize_pronouns`
- `PronounNormalizer.should_normalize`
- `context_messages.append`
- `context_messages.extend`
- `datetime.fromisoformat`
- `datetime.now`
- `entry_keywords.update`
- `hashlib.md5`
- `json.dump`
- `json.load`
- `logger.warning`
- `memory_entries.append`
- `memory_entry.key.lower`
- `memory_entry.summary.lower`
- `memory_entry.value.lower`
- `message.get`
- `message.lower`
- `metadata.get`
- `msg.get`
- `os.makedirs`
- `os.path.dirname`
- `os.path.exists`
- `query.lower`
- `query_words.intersection`
- `query_words.union`
- `re.escape`
- `re.findall`
- `re.sub`
- `relevant_memories.append`
- `relevant_memories.sort`
- `self._load`
- `self._load_memory`
- `self._save`
- `self.add_summary`
- `self.clear_memory`
- `self.entries.append`
- `self.entries.copy`
- `self.get_relevant_memories`
- `self.get_user_info`
- `self.intelligent_add_message`
- `self.ltm_service._save`
- `self.ltm_service.add_entry`
- `self.ltm_service.get_entries`
- `self.ltm_service.update_access_stats`
- `self.messages.append`
- `self.messages.copy`
- `self.semantic_search.add_memory`
- `self.semantic_search.search_semantic`
- `self.semantic_search.update_embeddings`
- `self.stm_service.add_message`
- `self.stm_service.clear`
- `self.stm_service.get_messages`
- `self.summary_updated.emit`
- `text.lower`
- `type_counts.get`
- `user_info.get`
- `words.intersection`
- `x.metadata.get`

**`features\memory\semantic_search.py`:**
- `CustomLogger.get_logger`
- `combined_scores.items`
- `datetime.now`
- `embeddings_data.items`
- `json.dump`
- `json.load`
- `keyword_results.append`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `meta.get`
- `os.makedirs`
- `os.path.exists`
- `os.path.join`
- `os.remove`
- `pickle.dump`
- `pickle.load`
- `query.lower`
- `query_lower.split`
- `results.sort`
- `self._init_model`
- `self._load_embeddings`
- `self._save_embeddings`
- `self.embeddings_updated.emit`
- `self.model.encode`
- `self.mutex.lock`
- `self.mutex.unlock`
- `self.search_semantic`
- `self.vectorized_memories.append`
- `self.vectorized_memories.clear`
- `self.vectorized_memories.remove`
- `similarities.append`
- `similarities.sort`
- `traceback.format_exc`
- `vm.content.lower`

**`features\memory\semantic_search_fallback.py`:**
- `CustomLogger.get_logger`
- `content.lower`
- `datetime.now`
- `json.dump`
- `json.load`
- `logger.debug`
- `logger.error`
- `logger.info`
- `meta.get`
- `metadata.items`
- `os.makedirs`
- `os.path.exists`
- `os.path.join`
- `os.remove`
- `query.lower`
- `query_words.intersection`
- `query_words.union`
- `re.findall`
- `self._calculate_keyword_similarity`
- `self._load_memories`
- `self._save_memories`
- `self.embeddings_updated.emit`
- `self.memories.append`
- `self.memories.clear`
- `self.memories.remove`
- `self.mutex.lock`
- `self.mutex.unlock`
- `self.search_semantic`
- `similarities.append`
- `similarities.sort`

**`features\ollama\ollama_chat.py`:**
- `CustomLogger.get_logger`
- `logger.error`
- `logger.info`
- `self._setup_ui`
- `self.chat_controller.set_chat_tab_reference`
- `self.event_handler.setup_connections`
- `self.lifecycle_manager.check_ollama_connection`
- `self.lifecycle_manager.handle_close_event`
- `self.lifecycle_manager.handle_show_event`
- `self.lifecycle_manager.initialize_application`
- `self.lifecycle_manager.show_ollama_connection_error`
- `self.service_manager.get_conversation_manager`
- `self.service_manager.get_conversation_service`
- `self.service_manager.get_enhancement_service`
- `self.service_manager.get_memory_service`
- `self.service_manager.get_ollama_service`
- `self.service_manager.get_summarization_service`
- `self.service_manager.is_memory_enabled`
- `self.ui_manager.get_chat_tab`
- `self.ui_manager.setup_menu_bar`
- `self.ui_manager.setup_ui`
- `traceback.format_exc`
- `traceback.print_exc`

**`features\ollama\ollama_service.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_debug`
- `LoggingHelpers.log_exception_with_context`
- `LoggingHelpers.log_info_with_context`
- `LoggingHelpers.log_network_request`
- `LoggingHelpers.log_service_initialization`
- `LoggingHelpers.log_thread_operation`
- `base_url.rstrip`
- `chunk.get`
- `commands.append`
- `data.get`
- `item.get`
- `json.dumps`
- `json.loads`
- `line.strip`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `m.get`
- `model.dict`
- `model.get`
- `model_dict.get`
- `model_name.strip`
- `model_names.append`
- `models.items`
- `msg.get`
- `ollama.Options`
- `ollama.chat`
- `ollama.delete`
- `ollama.list`
- `ollama.pull`
- `ollama.set_host`
- `process.stdout.close`
- `process.terminate`
- `process.wait`
- `requests.get`
- `requests.post`
- `response.get`
- `response.iter_lines`
- `response.json`
- `response.raise_for_status`
- `self._active_operations.add`
- `self._build_session_commands`
- `self._extract_system_prompt`
- `self._get_models_with_library`
- `self._get_models_with_requests`
- `self._send_chat_message_with_library`
- `self._send_chat_message_with_requests`
- `self.model_list_updated.emit`
- `self.model_operation_error.emit`
- `self.model_operation_finished.emit`
- `self.model_operation_progress.emit`
- `self.model_operation_started.emit`
- `self.test_connection`
- `self.threading_service.process_data`
- `session_variables.items`
- `subprocess.Popen`
- `time.time`
- `traceback.format_exc`

**`features\personality\formatter.py`:**
- `comprehensive_prompt.append`
- `config_data.get`
- `errors.append`
- `features.append`
- `formatted_template.format`
- `metadata.get`
- `name.lower`
- `personality_data.get`
- `prompt_data.get`
- `pronouns.format_user_reference`
- `pronouns.get_pronoun_guide`
- `style_info.append`
- `summary_parts.append`
- `traits.get`

**`features\personality\loader.py`:**
- `CustomLogger.get_logger`
- `PersonalityFormatter.validate_personality_data`
- `backup_files.append`
- `datetime.fromtimestamp`
- `datetime.now`
- `errors.append`
- `file.endswith`
- `filename.endswith`
- `json.dump`
- `json.load`
- `logger.debug`
- `name.split`
- `name_with_timestamp.rsplit`
- `name_without_ext.replace`
- `os.listdir`
- `os.makedirs`
- `os.path.basename`
- `os.path.exists`
- `os.path.getmtime`
- `os.path.getsize`
- `os.path.join`
- `os.path.relpath`
- `os.path.splitext`
- `os.remove`
- `os.walk`
- `personality_files.append`
- `personality_name.split`
- `self.extract_personality_name`
- `self.find_personality_file_by_name`
- `self.find_personality_files`
- `self.load_personality_from_file`
- `self.save_personality_to_file`
- `self.validate_personality_file`
- `shutil.copy2`

**`features\personality\models\personality_model.py`:**
- `self._initialize_personalities`
- `self.loader.extract_personality_name`
- `self.loader.find_personality_file_by_name`
- `self.loader.find_personality_files`
- `self.loader.save_personality_to_file`

**`features\personality\models\personality_pronouns.py`:**
- `formatted.replace`
- `guide.strip`
- `priority_title.lower`
- `random.choice`
- `self.get_primary_title`
- `self.get_user_address`
- `self.get_user_titles`
- `self.user_title.split`
- `title.lower`
- `title.strip`

**`features\personality\services\personality_service.py`:**
- `CustomLogger.get_logger`
- `categories.add`
- `context_messages.append`
- `context_text.strip`
- `datetime.now`
- `k.startswith`
- `key.replace`
- `key.startswith`
- `kwargs.items`
- `logger.debug`
- `matching_personalities.append`
- `memory_service.get_user_info`
- `metadata.get`
- `name.lower`
- `name.startswith`
- `personality.get`
- `personality_data.get`
- `preferences.items`
- `query.lower`
- `self._initialize_personalities`
- `self.formatter.build_comprehensive_system_prompt`
- `self.formatter.format_prompt_with_personality`
- `self.formatter.get_personality_info`
- `self.formatter.get_system_prompt`
- `self.get_current_personality`
- `self.get_personality`
- `self.is_custom_personality`
- `self.is_system_personality`
- `self.loader.create_personality_data`
- `self.loader.delete_personality_file`
- `self.loader.extract_personality_name`
- `self.loader.find_personality_file_by_name`
- `self.loader.find_personality_files`
- `self.loader.load_all_personalities`
- `self.loader.save_personality_to_file`
- `self.personalities.get`
- `self.personalities.items`
- `self.personalities.keys`
- `self.personalities.values`
- `tag.lower`
- `traits.get`
- `user_info.get`
- `user_info.items`

**`features\user\user_profile_service.py`:**
- `self.user_data.get`

**`features\voice\audio\recording_service.py`:**
- `CustomLogger.get_logger`
- `bar_vals.append`
- `datetime.datetime.now`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `math.log10`
- `math.sqrt`
- `np.abs`
- `np.array`
- `np.fft.rfft`
- `np.fft.rfftfreq`
- `np.log10`
- `np.logspace`
- `np.mean`
- `np.sqrt`
- `np.where`
- `os.getcwd`
- `os.makedirs`
- `os.path.join`
- `pyaudio.PyAudio`
- `self._calculate_audio_level`
- `self._check_availability`
- `self.audio.get_sample_size`
- `self.audio.open`
- `self.audio.terminate`
- `self.audio_level_changed.emit`
- `self.cleanup`
- `self.eq_bars_changed.emit`
- `self.frames.append`
- `self.recording_auto_stopped.emit`
- `self.recording_error.emit`
- `self.recording_started.emit`
- `self.recording_stopped.emit`
- `self.recording_thread.is_alive`
- `self.recording_thread.join`
- `self.recording_thread.start`
- `self.stream.close`
- `self.stream.read`
- `self.stream.stop_stream`
- `struct.unpack`
- `test_stream.close`
- `threading.Thread`
- `time.time`
- `wave.open`
- `wf.setframerate`
- `wf.setnchannels`
- `wf.setsampwidth`
- `wf.writeframes`

**`features\voice\orchestrator\voice_process_manager.py`:**
- `CustomLogger.get_logger`
- `QApplication.instance`
- `QThread.currentThread`
- `VoiceService.get_instance`
- `command_queue.get`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `manager.start_voice_process`
- `manager.stop_voice_process`
- `message.get`
- `mp.Process`
- `mp.Queue`
- `mp.set_start_method`
- `response.get`
- `response_queue.put`
- `self.command_queue.empty`
- `self.command_queue.get_nowait`
- `self.command_queue.put`
- `self.is_process_running`
- `self.monitor_error.emit`
- `self.monitor_thread.deleteLater`
- `self.monitor_thread.get_stats`
- `self.monitor_thread.isRunning`
- `self.monitor_thread.monitor_error.connect`
- `self.monitor_thread.response_received.connect`
- `self.monitor_thread.start`
- `self.monitor_thread.stop`
- `self.monitor_thread.wait`
- `self.process_status_changed.emit`
- `self.recording_error.emit`
- `self.recording_started.emit`
- `self.recording_stopped.emit`
- `self.response_queue.empty`
- `self.response_queue.get`
- `self.response_queue.get_nowait`
- `self.response_received.emit`
- `self.send_command`
- `self.setObjectName`
- `self.state_updated.emit`
- `self.stop_voice_process`
- `self.tts_error.emit`
- `self.tts_finished.emit`
- `self.tts_started.emit`
- `self.voice_input_error.emit`
- `self.voice_input_received.emit`
- `self.voice_process.is_alive`
- `self.voice_process.join`
- `self.voice_process.kill`
- `self.voice_process.start`
- `self.voice_process.terminate`
- `self.voice_processing_finished.emit`
- `self.voice_processing_started.emit`
- `time.sleep`
- `traceback.format_exc`
- `voice_service.cleanup_on_exit`
- `voice_service.set_continuous_voice_mode`
- `voice_service.speak_text`
- `voice_service.speak_text_non_streaming`
- `voice_service.speak_text_streaming`
- `voice_service.start_voice_input`
- `voice_service.stop_tts`
- `voice_service.stop_voice_input`
- `voice_service.update_settings`

**`features\voice\stt\stt_service.py`:**
- `CustomLogger.get_logger`
- `final_result.get`
- `json.loads`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `os.getcwd`
- `os.path.exists`
- `os.path.join`
- `rec.AcceptWaveform`
- `rec.FinalResult`
- `rec.Result`
- `rec.SetWords`
- `result.get`
- `results.append`
- `self._check_availability`
- `self._convert_with_vosk`
- `self.error_occurred.emit`
- `self.text_received.emit`
- `text.strip`
- `traceback.format_exc`
- `wave.open`
- `wf.close`
- `wf.getframerate`
- `wf.getnchannels`
- `wf.getsampwidth`
- `wf.readframes`

**`features\voice\tts\streaming_audio_player.py`:**
- `CustomLogger.get_logger`
- `audio_chunk.astype`
- `bar_vals.append`
- `device_info.get`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `np.abs`
- `np.array`
- `np.clip`
- `np.fft.rfft`
- `np.fft.rfftfreq`
- `np.log10`
- `np.logspace`
- `np.max`
- `np.mean`
- `np.min`
- `np.sqrt`
- `np.where`
- `processed_audio.tobytes`
- `pyaudio.PyAudio`
- `self._process_audio_chunk`
- `self.audio_level_buffer.append`
- `self.audio_level_buffer.clear`
- `self.audio_level_buffer.pop`
- `self.audio_level_changed.emit`
- `self.audio_queue.append`
- `self.audio_queue.clear`
- `self.audio_queue.pop`
- `self.cleanup`
- `self.eq_bars_changed.emit`
- `self.playback_error.emit`
- `self.playback_finished.emit`
- `self.player_started.emit`
- `self.pyaudio.get_default_output_device_info`
- `self.pyaudio.get_device_count`
- `self.pyaudio.get_device_info_by_index`
- `self.pyaudio.open`
- `self.pyaudio.terminate`
- `self.stop_playback`
- `self.stream.close`
- `self.stream.stop_stream`
- `self.stream.write`
- `term_thread.is_alive`
- `term_thread.start`
- `threading.Thread`
- `time.sleep`
- `traceback.format_exc`

**`features\voice\tts\streaming_audio_worker.py`:**
- `CustomLogger.get_logger`
- `audio.astype`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `np.abs`
- `np.array`
- `np.max`
- `np.min`
- `part.strip`
- `re.split`
- `s.strip`
- `self._adjust_audio_speed`
- `self._generate_audio_chunk`
- `self._split_text_into_sentences`
- `self.audio_chunk_ready.emit`
- `self.progress_updated.emit`
- `self.streaming_error.emit`
- `self.streaming_finished.emit`
- `self.tts_service.tts_model.tts`
- `signal.resample`
- `split_sentences.append`
- `text.strip`
- `time.sleep`
- `traceback.format_exc`

**`features\voice\tts\tts_service.py`:**
- `CoquiTTSService.get_instance`
- `CustomLogger.get_logger`
- `QTimer.singleShot`
- `logger.debug`
- `logger.error`
- `logger.info`
- `platform.system`
- `self._check_availability`
- `self._speak_with_espeak`
- `self.coqui_service.audio_level_changed.connect`
- `self.coqui_service.cleanup`
- `self.coqui_service.eq_bars_changed.connect`
- `self.coqui_service.get_available_models`
- `self.coqui_service.get_available_voices`
- `self.coqui_service.get_current_model_info`
- `self.coqui_service.is_available`
- `self.coqui_service.load_model`
- `self.coqui_service.set_speed`
- `self.coqui_service.set_voice`
- `self.coqui_service.speak_text`
- `self.coqui_service.stop_playback`
- `self.coqui_service.tts_error.connect`
- `self.coqui_service.tts_finished.connect`
- `self.coqui_service.tts_started.connect`
- `self.media_player.stop`
- `self.speak_text`
- `self.tts_error.emit`
- `self.tts_finished.emit`
- `self.tts_started.emit`
- `subprocess.Popen`
- `text.split`

**`features\voice\voice_service.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_audio_operation`
- `LoggingHelpers.log_warning_with_context`
- `QCoreApplication.instance`
- `QTimer.singleShot`
- `TTSService.get_instance`
- `audio_files.append`
- `audio_files.sort`
- `cleaned_text.lower`
- `data.get`
- `filename.endswith`
- `files_to_delete.append`
- `files_to_delete.extend`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `os.getcwd`
- `os.listdir`
- `os.path.exists`
- `os.path.getmtime`
- `os.path.getsize`
- `os.path.join`
- `os.remove`
- `self._active_voice_operations.clear`
- `self._check_and_emit_ready`
- `self._complete_request`
- `self._handle_tts_request`
- `self._handle_voice_input_request`
- `self._initialize_services`
- `self._process_request_queue`
- `self._request_queue.append`
- `self._request_queue.clear`
- `self._request_queue.pop`
- `self._setup_connections`
- `self._setup_service_connections`
- `self._speak_text_impl`
- `self.audio_level_changed.emit`
- `self.can_handle_new_request`
- `self.cancel_current_request`
- `self.cleanup_all_audio_files`
- `self.cleanup_old_audio_files`
- `self.clear_request_queue`
- `self.get_audio_folder_path`
- `self.handle_user_interruption`
- `self.is_voice_available`
- `self.list_audio_files`
- `self.persistent_thread_pool.cleanup`
- `self.queue_request`
- `self.recording_error.emit`
- `self.recording_service.audio_level_changed.connect`
- `self.recording_service.cleanup`
- `self.recording_service.eq_bars_changed.connect`
- `self.recording_service.get_current_audio_level`
- `self.recording_service.is_initialized`
- `self.recording_service.recording_auto_stopped.connect`
- `self.recording_service.recording_error.connect`
- `self.recording_service.recording_started.connect`
- `self.recording_service.recording_stopped.connect`
- `self.recording_service.set_audio_gate_enabled`
- `self.recording_service.start_recording`
- `self.recording_service.stop_recording`
- `self.recording_started.emit`
- `self.recording_stopped.emit`
- `self.recording_timer.setSingleShot`
- `self.recording_timer.timeout.connect`
- `self.request_cancelled.emit`
- `self.response_queue.put`
- `self.start_voice_input`
- `self.stop_tts`
- `self.stop_voice_input`
- `self.stt_service.cleanup`
- `self.stt_service.error_occurred.connect`
- `self.stt_service.is_initialized`
- `self.stt_service.process_audio_file`
- `self.stt_service.text_received.connect`
- `self.threading_service.cleanup`
- `self.tts_error.emit`
- `self.tts_finished.emit`
- `self.tts_service.audio_level_changed.connect`
- `self.tts_service.cleanup`
- `self.tts_service.eq_bars_changed.connect`
- `self.tts_service.is_available`
- `self.tts_service.is_initialized`
- `self.tts_service.speak_text`
- `self.tts_service.speak_text_streaming`
- `self.tts_service.stop_playback`
- `self.tts_service.tts_error.connect`
- `self.tts_service.tts_finished.connect`
- `self.tts_service.tts_started.connect`
- `self.tts_started.emit`
- `self.user_interrupted.emit`
- `self.voice_input_error.emit`
- `self.voice_input_received.emit`
- `self.voice_processing_finished.emit`
- `self.voice_processing_started.emit`
- `self.voice_service_ready.emit`
- `self.voice_settings.get`
- `self.voice_settings.update`
- `text.strip`
- `time.time`
- `traceback.format_exc`
- `uuid.uuid4`

**`features\voice\voice_service_manager.py`:**
- `CustomLogger.get_logger`
- `ServiceManager.get_instance`
- `VoiceService.get_instance`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `self._cached_settings.clear`
- `self._cached_settings.copy`
- `self._cached_settings.update`
- `self._initialize_voice_service`
- `self._ready_callbacks.append`
- `self._ready_callbacks.clear`
- `self._reset_voice_service`
- `self._voice_service.cleanup_on_exit`
- `self._voice_service.update_settings`
- `self._voice_service.voice_settings.copy`
- `self.is_ready`
- `self.voice_service_error.emit`
- `self.voice_service_initializing.emit`
- `self.voice_service_ready.emit`
- `service_manager.get_voice_service`
- `threading.Lock`
- `voice_service.is_voice_available`
- `voice_service.update_settings`
- `voice_service.voice_service_ready.connect`

**`features\voice\voice_service_wrapper.py`:**
- `CustomLogger.get_logger`
- `VoiceService.get_instance`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `self._cached_state.get`
- `self._cached_state.update`
- `self._init_direct_service`
- `self._init_process_manager`
- `self._ready_check_timer.start`
- `self._ready_check_timer.stop`
- `self._ready_check_timer.timeout.connect`
- `self.direct_service.cleanup_all_audio_files`
- `self.direct_service.cleanup_old_audio_files`
- `self.direct_service.cleanup_on_exit`
- `self.direct_service.get_audio_folder_path`
- `self.direct_service.get_current_audio_level`
- `self.direct_service.get_recording_timeout`
- `self.direct_service.get_silence_duration`
- `self.direct_service.get_silence_threshold`
- `self.direct_service.is_continuous_voice_mode`
- `self.direct_service.is_voice_available`
- `self.direct_service.list_audio_files`
- `self.direct_service.request_cancelled.connect`
- `self.direct_service.set_audio_gate_enabled`
- `self.direct_service.set_continuous_voice_mode`
- `self.direct_service.set_recording_timeout`
- `self.direct_service.set_silence_duration`
- `self.direct_service.set_silence_threshold`
- `self.direct_service.speak_text`
- `self.direct_service.speak_text_non_streaming`
- `self.direct_service.speak_text_streaming`
- `self.direct_service.start_voice_input`
- `self.direct_service.stop_tts`
- `self.direct_service.stop_voice_input`
- `self.direct_service.update_settings`
- `self.direct_service.user_interrupted.connect`
- `self.direct_service.voice_service_ready.connect`
- `self.process_manager.get_process_info`
- `self.process_manager.is_process_running`
- `self.process_manager.request_cancelled.connect`
- `self.process_manager.send_command`
- `self.process_manager.stop_voice_process`
- `self.process_manager.user_interrupted.connect`
- `self.voice_service_ready.emit`
- `traceback.format_exc`

**`startup\dependency_checker.py`:**
- `checker.get_dependency_summary`
- `checker.run_comprehensive_check`
- `checker.run_install_dependencies`
- `checker2.run_comprehensive_check`
- `expected_versions.items`
- `importlib.import_module`
- `line.split`
- `line.strip`
- `os.path.abspath`
- `os.path.dirname`
- `os.path.exists`
- `os.path.join`
- `result.stdout.strip`
- `self.broken_imports.append`
- `self.broken_imports.copy`
- `self.check_core_dependencies`
- `self.check_ml_dependencies`
- `self.check_package_versions`
- `self.check_tts_options`
- `self.optional_broken.append`
- `self.test_import`
- `self.version_conflicts.append`
- `self.version_conflicts.copy`
- `self.working_imports.append`
- `subprocess.run`

**`startup\python_installer.py`:**
- `os.path.abspath`
- `os.path.dirname`
- `os.path.exists`
- `os.path.join`
- `subprocess.run`
- `sys.exit`

**`startup\system_installer.py`:**
- `ctypes.windll.shell32.IsUserAnAdmin`
- `os.path.exists`
- `shutil.which`
- `subprocess.run`

**`ui\Widgets\chat_navigation.py`:**
- `QCursor.pos`
- `QInputDialog.getText`
- `QMessageBox.question`
- `QMessageBox.warning`
- `conversations.sort`
- `current_item.data`
- `delete_action.triggered.connect`
- `generate_name_action.triggered.connect`
- `header_layout.addStretch`
- `header_layout.addWidget`
- `item.data`
- `item.setData`
- `item.setSelected`
- `item.setToolTip`
- `layout.addLayout`
- `layout.addWidget`
- `layout.setContentsMargins`
- `layout.setSpacing`
- `menu.addAction`
- `menu.addSeparator`
- `menu.exec_`
- `metadata.get_display_name`
- `metadata.get_formatted_created_time`
- `new_filename.endswith`
- `open_action.triggered.connect`
- `os.path.basename`
- `os.path.dirname`
- `os.path.exists`
- `os.path.join`
- `parent.clear_chat`
- `parent.parent`
- `rename_action.triggered.connect`
- `self.clear_all_btn.clicked.connect`
- `self.clear_all_btn.setMaximumHeight`
- `self.clear_all_btn.setMinimumWidth`
- `self.clear_all_btn.setStyleSheet`
- `self.clear_all_btn.setToolTip`
- `self.conversation_deleted.emit`
- `self.conversation_manager.delete_conversation`
- `self.conversation_manager.list_conversations`
- `self.conversation_manager.load_conversation`
- `self.conversation_manager.rename_conversation`
- `self.conversation_manager.update_conversation_name`
- `self.conversation_renamed.emit`
- `self.conversation_selected.emit`
- `self.conversations_list.addItem`
- `self.conversations_list.clear`
- `self.conversations_list.currentItem`
- `self.conversations_list.customContextMenuRequested.connect`
- `self.conversations_list.itemAt`
- `self.conversations_list.itemDoubleClicked.connect`
- `self.conversations_list.setContextMenuPolicy`
- `self.conversations_list.setStyleSheet`
- `self.create_conversation_item`
- `self.delete_conversation`
- `self.new_btn.clicked.connect`
- `self.new_btn.setMaximumHeight`
- `self.new_btn.setMinimumWidth`
- `self.new_btn.setStyleSheet`
- `self.new_btn.setToolTip`
- `self.parent`
- `self.refresh_conversations`
- `self.rename_conversation`
- `self.setup_connections`
- `self.setup_ui`
- `self.status_label.setAlignment`
- `self.status_label.setStyleSheet`
- `self.status_label.setText`
- `self.summarization_service.generate_chat_name`
- `self.summarization_service.summarization_completed.connect`
- `self.summarization_service.summarization_failed.connect`
- `self.trigger_name_generation`
- `separator.setFixedHeight`
- `separator.setFrameShape`
- `separator.setStyleSheet`
- `time.time`
- `title_label.setFont`
- `title_label.setStyleSheet`

**`ui\Widgets\complexity_widget.py`:**
- `bar.setMaximumWidth`
- `bar.setRange`
- `bar.setValue`
- `color.name`
- `color_map.get`
- `label.setText`
- `layout.addLayout`
- `layout.addWidget`
- `layout.setContentsMargins`
- `layout.setSpacing`
- `metric_layout.addWidget`
- `metrics_layout.addLayout`
- `palette.setColor`
- `progress_bar.setStyleSheet`
- `recommendation_layout.addWidget`
- `request.strip`
- `score_layout.addWidget`
- `self._get_color_for_value`
- `self._set_progress_bar_color`
- `self._set_widget_color`
- `self._update_display`
- `self._update_model_recommendation`
- `self.analyzer.analyze_complexity`
- `self.analyzer.get_model_recommendation`
- `self.current_metrics.level.value.replace`
- `self.hide`
- `self.hide_btn.clicked.connect`
- `self.hide_btn.setMaximumWidth`
- `self.level_label.setAlignment`
- `self.level_label.setFont`
- `self.level_label.setText`
- `self.metric_bars.items`
- `self.model_recommendation_signal.emit`
- `self.recommendation_label.setText`
- `self.recommendation_label.setWordWrap`
- `self.recommendations_text.clear`
- `self.recommendations_text.setMaximumHeight`
- `self.recommendations_text.setPlaceholderText`
- `self.recommendations_text.setPlainText`
- `self.recommendations_text.setReadOnly`
- `self.score_bar.setRange`
- `self.score_bar.setValue`
- `self.setup_ui`
- `self.show`
- `self.switch_model_btn.clicked.connect`
- `self.switch_model_btn.setEnabled`
- `title.setAlignment`
- `title.setFont`
- `title_layout.addWidget`
- `value_label.setMinimumWidth`
- `widget.palette`
- `widget.setPalette`

**`ui\Widgets\message_editor.py`:**
- `button_layout.addStretch`
- `button_layout.addWidget`
- `button_layout.setContentsMargins`
- `container_layout.addWidget`
- `container_layout.setContentsMargins`
- `content_layout.addWidget`
- `content_layout.setContentsMargins`
- `edit_layout.addLayout`
- `edit_layout.addWidget`
- `edit_layout.setContentsMargins`
- `layout.addWidget`
- `layout.setContentsMargins`
- `layout.setSpacing`
- `self.cancel_button.clicked.connect`
- `self.cancel_button.setStyleSheet`
- `self.container.setFrameStyle`
- `self.content_area.setVisible`
- `self.edit_area.setVisible`
- `self.edit_button.clicked.connect`
- `self.edit_button.setFixedSize`
- `self.edit_button.setToolTip`
- `self.finish_editing`
- `self.message_display.setText`
- `self.message_display.setTextInteractionFlags`
- `self.message_display.setWordWrap`
- `self.message_edit_cancelled.emit`
- `self.message_edited.emit`
- `self.save_button.clicked.connect`
- `self.save_button.setStyleSheet`
- `self.setStyleSheet`
- `self.setup_styles`
- `self.setup_ui`
- `self.text_editor.selectAll`
- `self.text_editor.setFocus`
- `self.text_editor.setMaximumHeight`
- `self.text_editor.setPlaceholderText`
- `self.text_editor.setPlainText`
- `self.text_editor.toPlainText`

**`ui\Widgets\spellchecker_widget.py`:**
- `CustomLogger.get_logger`
- `action.triggered.connect`
- `add_action.triggered.connect`
- `after_cursor.anchor`
- `after_cursor.position`
- `current_cursor.anchor`
- `current_cursor.position`
- `cursor.atEnd`
- `cursor.insertText`
- `cursor.isNull`
- `cursor.mergeCharFormat`
- `cursor.movePosition`
- `cursor.position`
- `cursor.select`
- `cursor.selectedText`
- `cursor.setCharFormat`
- `enchant.Dict`
- `event.key`
- `format.setUnderlineColor`
- `format.setUnderlineStyle`
- `ignore_action.triggered.connect`
- `logger.debug`
- `menu.addAction`
- `menu.addSeparator`
- `menu.exec_`
- `new_cursor.setPosition`
- `re.findall`
- `self.add_to_dictionary`
- `self.clear`
- `self.cursorForPosition`
- `self.customContextMenuRequested.connect`
- `self.document`
- `self.highlight_misspelled_words`
- `self.ignore_word`
- `self.mapToGlobal`
- `self.replace_word`
- `self.setContextMenuPolicy`
- `self.setPlainText`
- `self.setTextCursor`
- `self.setup_context_menu`
- `self.setup_spellchecker`
- `self.spellcheck_timer.deleteLater`
- `self.spellcheck_timer.setSingleShot`
- `self.spellcheck_timer.start`
- `self.spellcheck_timer.stop`
- `self.spellcheck_timer.timeout.connect`
- `self.spellchecker.add_to_pwl`
- `self.spellchecker.check`
- `self.spellchecker.suggest`
- `self.textChanged.connect`
- `self.textCursor`
- `self.toPlainText`
- `word.isalpha`

**`ui\dialogs\coqui_model_dialog.py`:**
- `CoquiTTSService.get_instance`
- `CustomLogger.get_logger`
- `QMessageBox.critical`
- `QMessageBox.information`
- `QMessageBox.question`
- `QMessageBox.warning`
- `button_layout.addStretch`
- `button_layout.addWidget`
- `coqui_service.download_model`
- `datetime.now`
- `item.data`
- `item.setData`
- `item.setText`
- `item.text`
- `item_data.get`
- `layout.addLayout`
- `layout.addWidget`
- `model_layout.addWidget`
- `self.accept`
- `self.cancel_button.clicked.connect`
- `self.coqui_service.get_available_models`
- `self.coqui_service.get_available_voices`
- `self.coqui_service.get_model_download_size`
- `self.coqui_service.is_model_downloaded`
- `self.coqui_service.load_model`
- `self.create_model_panel`
- `self.create_speaker_panel`
- `self.download_button.clicked.connect`
- `self.download_button.setEnabled`
- `self.download_completed.emit`
- `self.download_progress.emit`
- `self.download_thread.download_completed.connect`
- `self.download_thread.download_progress.connect`
- `self.download_thread.start`
- `self.get_current_time`
- `self.load_models`
- `self.load_speakers_for_model`
- `self.log_status`
- `self.model_info_label.setStyleSheet`
- `self.model_info_label.setText`
- `self.model_info_label.setWordWrap`
- `self.model_list.addItem`
- `self.model_list.clear`
- `self.model_list.itemClicked.connect`
- `self.model_selected.emit`
- `self.progress_bar.setRange`
- `self.progress_bar.setVisible`
- `self.refresh_button.clicked.connect`
- `self.refresh_button.setEnabled`
- `self.select_button.clicked.connect`
- `self.select_button.setEnabled`
- `self.setMinimumHeight`
- `self.setMinimumWidth`
- `self.setModal`
- `self.setStyleSheet`
- `self.setWindowTitle`
- `self.setup_ui`
- `self.speaker_info_label.setStyleSheet`
- `self.speaker_info_label.setText`
- `self.speaker_info_label.setWordWrap`
- `self.speaker_list.addItem`
- `self.speaker_list.clear`
- `self.speaker_list.itemClicked.connect`
- `self.start_download`
- `self.status_text.append`
- `self.status_text.setMaximumHeight`
- `self.status_text.setReadOnly`
- `self.status_text.setStyleSheet`
- `self.status_text.verticalScrollBar`
- `self.update_selection_button`
- `speaker_layout.addWidget`
- `splitter.addWidget`
- `splitter.setSizes`

**`ui\dialogs\error_dialog.py`:**
- `CustomLogger.get_logger`
- `QTimer.singleShot`
- `button.setStyleSheet`
- `button.setText`
- `button_layout.addStretch`
- `button_layout.addWidget`
- `child.setStyleSheet`
- `child.setText`
- `child.text`
- `clipboard.setText`
- `copy_button.clicked.connect`
- `copy_button.setStyleSheet`
- `copy_button.setText`
- `copy_button.text`
- `details_label.setFont`
- `dialog.exec`
- `header_layout.addStretch`
- `header_layout.addWidget`
- `icon_label.setFont`
- `layout.addLayout`
- `layout.addWidget`
- `logger.debug`
- `logger.error`
- `message_label.setFont`
- `message_label.setWordWrap`
- `ok_button.clicked.connect`
- `self.addButton`
- `self.details_text.setMaximumHeight`
- `self.details_text.setPlainText`
- `self.details_text.setReadOnly`
- `self.findChild`
- `self.findChildren`
- `self.reset_copy_button`
- `self.setIcon`
- `self.setMinimumSize`
- `self.setModal`
- `self.setStyleSheet`
- `self.setText`
- `self.setWindowTitle`
- `self.setup_styles`
- `self.setup_ui`

**`ui\dialogs\settings_dialog.py`:**
- `CustomLogger.get_logger`
- `QMessageBox.critical`
- `QMessageBox.information`
- `QMessageBox.question`
- `QMessageBox.warning`
- `QTimer.singleShot`
- `button_layout.addWidget`
- `cancel_button.clicked.connect`
- `chat_settings.get`
- `description.setStyleSheet`
- `description.setWordWrap`
- `explanation.setStyleSheet`
- `explanation.setWordWrap`
- `layout.addLayout`
- `layout.addStretch`
- `layout.addWidget`
- `logger.debug`
- `model_layout.addRow`
- `options_layout.addWidget`
- `params_layout.addRow`
- `personality_layout.addRow`
- `reset_button.clicked.connect`
- `save_button.clicked.connect`
- `self.accept`
- `self.auto_save_checkbox.isChecked`
- `self.auto_save_checkbox.setChecked`
- `self.auto_save_checkbox.setToolTip`
- `self.config_manager.get`
- `self.config_manager.get_chat_settings`
- `self.config_manager.get_default_model`
- `self.config_manager.get_default_personality`
- `self.config_manager.get_default_temperature`
- `self.config_manager.get_window_size`
- `self.config_manager.is_auto_save_enabled`
- `self.config_manager.is_enhancement_enabled`
- `self.config_manager.is_history_enabled`
- `self.config_manager.is_json_format_enabled`
- `self.config_manager.is_spellcheck_enabled`
- `self.config_manager.is_think_enabled`
- `self.config_manager.is_verbose_enabled`
- `self.config_manager.is_wordwrap_enabled`
- `self.config_manager.set`
- `self.config_manager.set_auto_save_enabled`
- `self.config_manager.set_default_model`
- `self.config_manager.set_default_personality`
- `self.config_manager.set_default_temperature`
- `self.config_manager.set_enhancement_enabled`
- `self.config_manager.set_history_enabled`
- `self.config_manager.set_json_format_enabled`
- `self.config_manager.set_spellcheck_enabled`
- `self.config_manager.set_think_enabled`
- `self.config_manager.set_verbose_enabled`
- `self.config_manager.set_window_size`
- `self.config_manager.set_wordwrap_enabled`
- `self.create_chat_tab`
- `self.create_developer_tab`
- `self.create_general_tab`
- `self.create_session_tab`
- `self.enhancement_checkbox.isChecked`
- `self.enhancement_checkbox.setChecked`
- `self.enhancement_checkbox.setToolTip`
- `self.height_spin.setRange`
- `self.height_spin.setSuffix`
- `self.height_spin.setValue`
- `self.height_spin.value`
- `self.history_checkbox.isChecked`
- `self.history_checkbox.setChecked`
- `self.history_checkbox.setToolTip`
- `self.json_format_checkbox.isChecked`
- `self.json_format_checkbox.setChecked`
- `self.json_format_checkbox.setToolTip`
- `self.load_current_settings`
- `self.logging_checkbox.isChecked`
- `self.logging_checkbox.setChecked`
- `self.logging_checkbox.setToolTip`
- `self.max_tokens_spin.setRange`
- `self.max_tokens_spin.setSuffix`
- `self.max_tokens_spin.setValue`
- `self.max_tokens_spin.value`
- `self.memory_checkbox.isChecked`
- `self.memory_checkbox.setChecked`
- `self.memory_checkbox.setToolTip`
- `self.model_combo.addItems`
- `self.model_combo.currentText`
- `self.model_combo.setCurrentText`
- `self.personality_combo.addItems`
- `self.personality_combo.currentText`
- `self.personality_combo.setCurrentText`
- `self.setGeometry`
- `self.setWindowTitle`
- `self.setup_ui`
- `self.spellcheck_checkbox.isChecked`
- `self.spellcheck_checkbox.setChecked`
- `self.spellcheck_checkbox.setToolTip`
- `self.temp_spin.setRange`
- `self.temp_spin.setSuffix`
- `self.temp_spin.setToolTip`
- `self.temp_spin.setValue`
- `self.temp_spin.value`
- `self.theme_combo.addItems`
- `self.theme_combo.currentText`
- `self.theme_combo.setCurrentText`
- `self.think_checkbox.isChecked`
- `self.think_checkbox.setChecked`
- `self.think_checkbox.setToolTip`
- `self.top_p_spin.setRange`
- `self.top_p_spin.setSuffix`
- `self.top_p_spin.setToolTip`
- `self.top_p_spin.setValue`
- `self.top_p_spin.value`
- `self.typewriter_checkbox.isChecked`
- `self.typewriter_checkbox.setChecked`
- `self.typewriter_checkbox.setToolTip`
- `self.verbose_checkbox.isChecked`
- `self.verbose_checkbox.setChecked`
- `self.verbose_checkbox.setToolTip`
- `self.width_spin.setRange`
- `self.width_spin.setSuffix`
- `self.width_spin.setValue`
- `self.width_spin.value`
- `self.wordwrap_checkbox.isChecked`
- `self.wordwrap_checkbox.setChecked`
- `self.wordwrap_checkbox.setToolTip`
- `session_layout.addWidget`
- `tabs.addTab`
- `temp_layout.addRow`
- `theme_layout.addRow`
- `window_layout.addRow`

**`ui\dialogs\voice_settings_dialog.py`:**
- `CoquiTTSService.get_instance`
- `CustomLogger.get_logger`
- `QMessageBox.critical`
- `QMessageBox.information`
- `QMessageBox.warning`
- `QTimer.singleShot`
- `TTSService.get_instance`
- `api_info.get`
- `api_name.replace`
- `audio.open`
- `audio.terminate`
- `audio_gate_layout.addLayout`
- `audio_gate_layout.addWidget`
- `button_layout.addStretch`
- `button_layout.addWidget`
- `coqui_layout.addLayout`
- `coqui_layout.addWidget`
- `dialog.exec_`
- `dialog.get_result`
- `eq_layout.addStretch`
- `eq_layout.addWidget`
- `filtered_speakers.append`
- `general_layout.addWidget`
- `internet_layout.addWidget`
- `interruption_layout.addLayout`
- `interruption_layout.addWidget`
- `layout.addLayout`
- `layout.addStretch`
- `layout.addWidget`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `math.log10`
- `math.sqrt`
- `model_layout.addWidget`
- `model_text.replace`
- `preview_tts.set_coqui_model`
- `preview_tts.speak_text_non_streaming`
- `preview_tts.update_voice`
- `pyaudio.PyAudio`
- `self._finish`
- `self._start_recording`
- `self._start_step`
- `self.accept`
- `self.allow_interruptions_checkbox.setChecked`
- `self.allow_interruptions_checkbox.setToolTip`
- `self.audio.open`
- `self.audio.terminate`
- `self.auto_speak_checkbox.setChecked`
- `self.calibrate_button.clicked.connect`
- `self.calibrate_button.setToolTip`
- `self.cancel_button.clicked.connect`
- `self.cancel_button.setStyleSheet`
- `self.check_completed.emit`
- `self.check_internet_connection`
- `self.config_manager.get_voice_settings`
- `self.config_manager.set_voice_settings`
- `self.coqui_controls.setVisible`
- `self.coqui_service.download_model`
- `self.coqui_service.get_available_models`
- `self.coqui_service.get_model_download_size`
- `self.coqui_service.get_speaker_info`
- `self.coqui_service.is_model_downloaded`
- `self.coqui_service.load_coqui_model`
- `self.coqui_service.load_model`
- `self.coqui_service.set_voice`
- `self.coqui_service.update_voice`
- `self.create_general_tab`
- `self.create_stt_tab`
- `self.create_tts_tab`
- `self.current_settings.copy`
- `self.current_settings.update`
- `self.download_button.clicked.connect`
- `self.download_button.setVisible`
- `self.eq_selector.addItems`
- `self.eq_selector.currentTextChanged.connect`
- `self.eq_selector.findText`
- `self.eq_selector.setCurrentIndex`
- `self.eq_selector.setMinimumWidth`
- `self.eq_visualizer_changed.emit`
- `self.get_speaker_info`
- `self.internet_status_label.setStyleSheet`
- `self.internet_status_label.setText`
- `self.internet_thread.check_completed.connect`
- `self.internet_thread.start`
- `self.interruption_threshold_spinbox.setRange`
- `self.interruption_threshold_spinbox.setSingleStep`
- `self.interruption_threshold_spinbox.setToolTip`
- `self.interruption_threshold_spinbox.setValue`
- `self.layout.addWidget`
- `self.load_coqui_models`
- `self.load_coqui_speakers`
- `self.main_tts_service.load_model`
- `self.main_tts_service.set_voice`
- `self.model_combo.addItem`
- `self.model_combo.clear`
- `self.model_combo.count`
- `self.model_combo.currentText`
- `self.model_combo.currentTextChanged.connect`
- `self.model_combo.itemText`
- `self.model_combo.setCurrentIndex`
- `self.model_info_label.setStyleSheet`
- `self.model_info_label.setText`
- `self.model_info_label.setWordWrap`
- `self.on_coqui_model_changed`
- `self.on_silence_threshold_changed`
- `self.on_tts_api_changed`
- `self.preview_speaker_button.clicked.connect`
- `self.preview_speaker_button.setEnabled`
- `self.preview_speaker_button.setText`
- `self.preview_speaker_button.setToolTip`
- `self.refresh_coqui_ui`
- `self.refresh_internet_button.clicked.connect`
- `self.refresh_internet_button.setMaximumWidth`
- `self.refresh_internet_button.setStyleSheet`
- `self.samples.append`
- `self.save_button.clicked.connect`
- `self.save_button.setStyleSheet`
- `self.sensitivity_label.setStyleSheet`
- `self.sensitivity_label.setText`
- `self.setMinimumHeight`
- `self.setMinimumWidth`
- `self.setModal`
- `self.setStyleSheet`
- `self.setWindowTitle`
- `self.settings_changed.emit`
- `self.setup_connections`
- `self.setup_ui`
- `self.silence_duration_spinbox.setRange`
- `self.silence_duration_spinbox.setStyleSheet`
- `self.silence_duration_spinbox.setToolTip`
- `self.silence_duration_spinbox.setValue`
- `self.silence_threshold_spinbox.setDecimals`
- `self.silence_threshold_spinbox.setRange`
- `self.silence_threshold_spinbox.setSingleStep`
- `self.silence_threshold_spinbox.setStyleSheet`
- `self.silence_threshold_spinbox.setToolTip`
- `self.silence_threshold_spinbox.setValue`
- `self.silence_threshold_spinbox.valueChanged.connect`
- `self.speaker_combo.addItem`
- `self.speaker_combo.clear`
- `self.speaker_combo.count`
- `self.speaker_combo.currentIndex`
- `self.speaker_combo.currentText`
- `self.speaker_combo.currentTextChanged.connect`
- `self.speaker_combo.itemData`
- `self.speaker_combo.itemText`
- `self.speaker_combo.setCurrentIndex`
- `self.speaker_combo.setEnabled`
- `self.speaker_filter_combo.addItems`
- `self.speaker_filter_combo.currentTextChanged.connect`
- `self.speaker_filter_widget.setVisible`
- `self.speaker_info_label.setStyleSheet`
- `self.speaker_info_label.setText`
- `self.speaker_info_label.setWordWrap`
- `self.standard_voice_layout.addWidget`
- `self.standard_voice_widget.setVisible`
- `self.stream.close`
- `self.stream.read`
- `self.streaming_checkbox.setChecked`
- `self.streaming_checkbox.setToolTip`
- `self.stt_api_combo.addItem`
- `self.stt_api_combo.count`
- `self.stt_api_combo.currentTextChanged.connect`
- `self.stt_api_combo.findText`
- `self.stt_api_combo.itemText`
- `self.stt_api_combo.setCurrentIndex`
- `self.stt_api_combo.setItemText`
- `self.stt_apis.get`
- `self.stt_apis.items`
- `self.stt_description_label.setStyleSheet`
- `self.stt_description_label.setText`
- `self.stt_description_label.setWordWrap`
- `self.test_button.clicked.connect`
- `self.test_button.setStyleSheet`
- `self.timeout_spinbox.setRange`
- `self.timeout_spinbox.setToolTip`
- `self.timeout_spinbox.setValue`
- `self.timer.start`
- `self.timer.stop`
- `self.timer.timeout.connect`
- `self.tts_api_combo.addItem`
- `self.tts_api_combo.count`
- `self.tts_api_combo.currentText`
- `self.tts_api_combo.currentTextChanged.connect`
- `self.tts_api_combo.findText`
- `self.tts_api_combo.itemText`
- `self.tts_api_combo.setCurrentIndex`
- `self.tts_api_combo.setItemText`
- `self.tts_apis.get`
- `self.tts_apis.items`
- `self.tts_description_label.setStyleSheet`
- `self.tts_description_label.setText`
- `self.tts_description_label.setWordWrap`
- `self.update_api_availability`
- `self.voice_combo.addItem`
- `self.voice_combo.clear`
- `self.voice_combo.currentTextChanged.connect`
- `self.voice_combo.findText`
- `self.voice_combo.setCurrentIndex`
- `settings.copy`
- `settings.get`
- `signal.disconnect`
- `silence_duration_layout.addStretch`
- `silence_duration_layout.addWidget`
- `silence_threshold_layout.addStretch`
- `silence_threshold_layout.addWidget`
- `speaker.strip`
- `speaker_filter_layout.addWidget`
- `speaker_filter_layout.setContentsMargins`
- `speaker_info.get`
- `speaker_layout.addWidget`
- `speaker_name.lower`
- `streaming_description.setStyleSheet`
- `streaming_description.setWordWrap`
- `streaming_layout.addWidget`
- `struct.unpack`
- `stt_layout.addWidget`
- `tab_widget.addTab`
- `test_stream.close`
- `test_stream.read`
- `threshold_layout.addStretch`
- `threshold_layout.addWidget`
- `time.time`
- `timeout_layout.addStretch`
- `timeout_layout.addWidget`
- `traceback.format_exc`
- `tts_layout.addWidget`
- `tts_streaming_layout.addWidget`
- `voice_layout.addWidget`

**`ui\tabs\chat_tab\chat_display.py`:**
- `CustomLogger.get_logger`
- `QTimer.singleShot`
- `block.text`
- `block_text.strip`
- `button_layout.addWidget`
- `button_pos.setX`
- `button_pos.setY`
- `button_pos.x`
- `button_pos.y`
- `cancel_button.clicked.connect`
- `cancel_button.setStyleSheet`
- `conversation_service.add_message`
- `conversation_service.finalize_streaming_message`
- `conversation_service.get_messages`
- `conversation_service.update_streaming_message`
- `cursor.block`
- `cursor.movePosition`
- `dialog.accept`
- `dialog.exec`
- `dialog.setMinimumSize`
- `dialog.setModal`
- `dialog.setStyleSheet`
- `dialog.setWindowTitle`
- `event.pos`
- `layout.addLayout`
- `layout.addWidget`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `m.get`
- `message.get`
- `message.startswith`
- `msg.get`
- `new_content.strip`
- `renderer_messages.append`
- `save_button.clicked.connect`
- `self._sync_messages_from_conversation_service`
- `self.chat_display.clear`
- `self.chat_display.cursorForPosition`
- `self.chat_display.mapFromGlobal`
- `self.chat_display.mapToGlobal`
- `self.chat_display.setLineWrapMode`
- `self.chat_display.setMouseTracking`
- `self.chat_display.setReadOnly`
- `self.chat_display.setStyleSheet`
- `self.chat_display.setTextCursor`
- `self.chat_display.textCursor`
- `self.chat_display.update`
- `self.chat_renderer.clear_messages`
- `self.chat_renderer.edit_message`
- `self.chat_renderer.get_messages`
- `self.chat_renderer.render_completed.connect`
- `self.chat_renderer.render_error.connect`
- `self.chat_renderer.request_render`
- `self.chat_renderer.sync_messages_from_conversation`
- `self.edit_button_widget.clicked.connect`
- `self.edit_button_widget.deleteLater`
- `self.edit_button_widget.hide`
- `self.edit_button_widget.move`
- `self.edit_button_widget.setFixedSize`
- `self.edit_button_widget.setStyleSheet`
- `self.edit_button_widget.show`
- `self.edit_message_at_index`
- `self.force_update_display`
- `self.get_ai_name`
- `self.hide_edit_button`
- `self.message_edited.emit`
- `self.save_message_edit`
- `self.scroll_area.setHorizontalScrollBarPolicy`
- `self.scroll_area.setVerticalScrollBarPolicy`
- `self.scroll_area.setWidget`
- `self.scroll_area.setWidgetResizable`
- `self.setup_chat_renderer`
- `self.setup_ui_components`
- `self.show_edit_button`
- `self.show_message_edit_dialog`
- `self.start_streaming`
- `self.streaming_handler.clear_messages`
- `self.streaming_handler.edit_message`
- `self.streaming_handler.message_edited.connect`
- `text_edit.setMaximumHeight`
- `text_edit.setPlainText`
- `text_edit.toPlainText`
- `traceback.format_exc`
- `traceback.format_stack`

**`ui\tabs\chat_tab\chat_renderer.py`:**
- `CustomLogger.get_logger`
- `MessageFormatter.detect_and_format_code`
- `MessageFormatter.format_markdown`
- `MessageFormatter.split_thoughts_and_answer`
- `MessageFormatter.syntax_highlight_code`
- `QApplication.instance`
- `QTimer.singleShot`
- `conversation_messages.copy`
- `cursor.movePosition`
- `handler_messages.copy`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `msg.get`
- `self._emergency_reset`
- `self._emergency_reset_timer.isActive`
- `self._emergency_reset_timer.setInterval`
- `self._emergency_reset_timer.setSingleShot`
- `self._emergency_reset_timer.start`
- `self._emergency_reset_timer.stop`
- `self._emergency_reset_timer.timeout.connect`
- `self._get_current_streaming_message`
- `self._get_next_message_id`
- `self._render_chat_display`
- `self._render_timer.isActive`
- `self._render_timer.setInterval`
- `self._render_timer.setSingleShot`
- `self._render_timer.start`
- `self._render_timer.stop`
- `self._render_timer.timeout.connect`
- `self._typewriter_timer.setInterval`
- `self._typewriter_timer.setSingleShot`
- `self._typewriter_timer.timeout.connect`
- `self.add_message`
- `self.chat_display.clear`
- `self.chat_display.insertHtml`
- `self.chat_display.setTextCursor`
- `self.chat_display.textCursor`
- `self.chat_display.thread`
- `self.clear_messages`
- `self.config_manager.get`
- `self.messages.append`
- `self.messages.clear`
- `self.messages.copy`
- `self.messages.index`
- `self.render_completed.emit`
- `self.render_error.emit`
- `self.request_render`
- `self.start_streaming_message`
- `traceback.format_exc`

**`ui\tabs\chat_tab\chat_tab.py`:**
- `ConversationMetadata.from_file`
- `CustomLogger.get_logger`
- `QMessageBox.critical`
- `QMessageBox.warning`
- `QTimer.singleShot`
- `chat_controller.get_ai_name`
- `chat_layout.addWidget`
- `chat_layout.setContentsMargins`
- `chat_renderer.add_message`
- `chat_renderer.clear_messages`
- `chat_renderer.request_render`
- `chat_splitter.addWidget`
- `chat_splitter.setSizes`
- `child.widget`
- `clicked.connect`
- `controls_layout.addWidget`
- `controls_layout.setContentsMargins`
- `conversation_service.conversation_updated.connect`
- `conversation_service.conversation_updated.disconnect`
- `conversation_service.finalize_streaming_message`
- `conversation_service.load_conversation`
- `conversation_service.start_streaming_message`
- `cursor.movePosition`
- `data.get`
- `dialog.eq_visualizer_changed.connect`
- `dialog.exec`
- `dialog.get_settings`
- `dialog.set_settings`
- `dialog.settings_changed.connect`
- `json.load`
- `layout.addWidget`
- `layout.setContentsMargins`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `main_splitter.addWidget`
- `main_splitter.setSizes`
- `message.get`
- `new_settings.get`
- `os.path.basename`
- `personality_service.get_ai_name`
- `personality_tab.personality_model.get_ai_name`
- `self._append_response_chunk_safe`
- `self._ensure_chat_display_visible`
- `self._ensure_voice_controls_initialized`
- `self._load_conversation_fallback`
- `self.append_to_chat`
- `self.chat_display._sync_messages_from_conversation_service`
- `self.chat_display.append_response_chunk`
- `self.chat_display.append_to_chat`
- `self.chat_display.chat_display.isVisible`
- `self.chat_display.chat_display.setEnabled`
- `self.chat_display.chat_display.setTextCursor`
- `self.chat_display.chat_display.setVisible`
- `self.chat_display.chat_display.show`
- `self.chat_display.chat_display.textCursor`
- `self.chat_display.chat_display.update`
- `self.chat_display.chat_display.updateGeometry`
- `self.chat_display.clear_chat`
- `self.chat_display.get_streaming_handler`
- `self.chat_display.get_ui_components`
- `self.chat_display.message_edited.connect`
- `self.chat_display.scroll_area.update`
- `self.clear_chat`
- `self.eq_visualizer._update_eq_widget_safe`
- `self.eq_visualizer.current_eq_widget.isVisible`
- `self.eq_visualizer.eq_mode_changed.connect`
- `self.eq_visualizer.get_eq_mode`
- `self.eq_visualizer.switch_to_chat_display`
- `self.eq_visualizer.switch_to_eq_visualizer`
- `self.eq_visualizer.update_eq_visualizer`
- `self.eq_visualizer.update_eq_visualizer_mode`
- `self.finalize_streaming_and_start_tts`
- `self.get_ai_name`
- `self.get_current_personality`
- `self.input_controls.get_current_model`
- `self.input_controls.get_current_personality`
- `self.input_controls.get_current_response`
- `self.input_controls.get_temperature`
- `self.input_controls.get_ui_components`
- `self.input_controls.input_mode_changed.connect`
- `self.input_controls.message_cancelled.connect`
- `self.input_controls.message_sent.connect`
- `self.input_controls.model_changed.connect`
- `self.input_controls.model_combo.count`
- `self.input_controls.model_combo.itemText`
- `self.input_controls.model_combo.setCurrentText`
- `self.input_controls.personality_changed.connect`
- `self.input_controls.personality_combo.count`
- `self.input_controls.personality_combo.itemText`
- `self.input_controls.personality_combo.setCurrentText`
- `self.input_controls.temperature_changed.connect`
- `self.input_controls.update_model_list`
- `self.input_controls.update_personality_list`
- `self.message_cancelled.emit`
- `self.message_edited.emit`
- `self.message_sent.emit`
- `self.navigation_widget.conversation_deleted.connect`
- `self.navigation_widget.conversation_renamed.connect`
- `self.navigation_widget.conversation_selected.connect`
- `self.navigation_widget.new_conversation_requested.connect`
- `self.navigation_widget.refresh_conversations`
- `self.navigation_widget.setMaximumWidth`
- `self.navigation_widget.setMinimumWidth`
- `self.navigation_widget.set_current_conversation`
- `self.parent.get_chat_controller`
- `self.parent.get_service_manager`
- `self.parent.get_ui_manager`
- `self.process_voice_input`
- `self.setStyleSheet`
- `self.set_current_conversation_file`
- `self.setup_components`
- `self.setup_connections`
- `self.setup_ui`
- `self.speak_ai_response`
- `self.start_streaming`
- `self.stop_streaming`
- `self.voice_controls.audio_level_label.setText`
- `self.voice_controls.force_ui_refresh`
- `self.voice_controls.get_ui_components`
- `self.voice_controls.get_voice_settings`
- `self.voice_controls.is_tts_playing`
- `self.voice_controls.is_voice_service_ready`
- `self.voice_controls.speak_ai_response`
- `self.voice_controls.update_voice_settings`
- `self.voice_controls.voice_service.stop_voice_input`
- `self.voice_controls.voice_status_changed.emit`
- `self.voice_controls_widget.hide`
- `self.voice_controls_widget.layout`
- `self.voice_controls_widget.show`
- `service_manager.get_personality_service`
- `settings.get`
- `signal.connect`
- `signal.disconnect`
- `streaming_handler.finalize_streaming_message`
- `streaming_handler.start_streaming_message`
- `time.time`
- `traceback.format_exc`
- `traceback.format_stack`
- `ui_manager.get_personality_tab`
- `voice_controls_layout.addStretch`
- `voice_controls_layout.addWidget`
- `voice_controls_layout.count`
- `voice_controls_layout.setContentsMargins`
- `voice_controls_layout.takeAt`

**`ui\tabs\chat_tab\eq_visualizer.py`:**
- `CustomLogger.get_logger`
- `QTimer.singleShot`
- `bar_values.append`
- `chat_display.hide`
- `chat_display.isVisible`
- `chat_display.parent`
- `chat_display.setEnabled`
- `chat_display.setVisible`
- `chat_display.show`
- `chat_display.update`
- `chat_display.updateGeometry`
- `current_parent.parent`
- `logger.debug`
- `logger.error`
- `random.random`
- `scroll_area.setWidget`
- `scroll_area.takeWidget`
- `scroll_area.update`
- `scroll_area.updateGeometry`
- `scroll_area.widget`
- `self._update_eq_widget_safe`
- `self.current_eq_widget.hide`
- `self.current_eq_widget.isVisible`
- `self.current_eq_widget.parent`
- `self.current_eq_widget.set_eq_bars`
- `self.current_eq_widget.show`
- `self.current_eq_widget.start_animation`
- `self.current_eq_widget.stop_animation`
- `self.current_eq_widget.update`
- `self.current_eq_widget.updateGeometry`
- `self.eq_mode_changed.emit`
- `self.eq_widgets.keys`
- `self.setup_eq_visualizers`
- `traceback.format_exc`

**`ui\tabs\chat_tab\input_controls.py`:**
- `CustomLogger.get_logger`
- `cursor.insertText`
- `event.key`
- `event.modifiers`
- `event.type`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `model_layout.addWidget`
- `personality_layout.addWidget`
- `self.cancel_button.clicked.connect`
- `self.cancel_button.hide`
- `self.cancel_button.isVisible`
- `self.cancel_button.setStyleSheet`
- `self.cancel_button.setVisible`
- `self.cancel_button.update`
- `self.input_layout.addWidget`
- `self.input_layout.setContentsMargins`
- `self.input_mode_changed.emit`
- `self.message_cancelled.emit`
- `self.message_input.clear`
- `self.message_input.hide`
- `self.message_input.installEventFilter`
- `self.message_input.setMaximumHeight`
- `self.message_input.setPlaceholderText`
- `self.message_input.setStyleSheet`
- `self.message_input.show`
- `self.message_input.textCursor`
- `self.message_input.toPlainText`
- `self.message_sent.emit`
- `self.mode_combo.addItems`
- `self.mode_combo.currentText`
- `self.mode_combo.currentTextChanged.connect`
- `self.mode_combo.setCurrentText`
- `self.mode_combo.setMinimumWidth`
- `self.mode_combo.setStyleSheet`
- `self.mode_combo.setToolTip`
- `self.model_changed.emit`
- `self.model_combo.addItems`
- `self.model_combo.clear`
- `self.model_combo.currentText`
- `self.model_combo.currentTextChanged.connect`
- `self.model_combo.setCurrentIndex`
- `self.model_combo.setCurrentText`
- `self.personality_changed.emit`
- `self.personality_combo.addItems`
- `self.personality_combo.clear`
- `self.personality_combo.currentText`
- `self.personality_combo.currentTextChanged.connect`
- `self.personality_combo.setCurrentIndex`
- `self.personality_combo.setCurrentText`
- `self.send_button.clicked.connect`
- `self.send_button.hide`
- `self.send_button.isEnabled`
- `self.send_button.setEnabled`
- `self.send_button.setStyleSheet`
- `self.send_button.show`
- `self.send_button.update`
- `self.send_message`
- `self.set_input_mode`
- `self.setup_connections`
- `self.setup_ui_components`
- `self.start_streaming`
- `self.stop_streaming`
- `self.temperature_changed.emit`
- `self.temperature_label.setAlignment`
- `self.temperature_label.setStyleSheet`
- `self.temperature_label.setText`
- `self.temperature_slider.setRange`
- `self.temperature_slider.setStyleSheet`
- `self.temperature_slider.setValue`
- `self.temperature_slider.valueChanged.connect`
- `settings_layout.addWidget`
- `settings_layout.setContentsMargins`
- `temperature_layout.addWidget`

**`ui\tabs\chat_tab\voice_controls.py`:**
- `CustomLogger.get_logger`
- `QTimer.singleShot`
- `audio_layout.addWidget`
- `audio_layout.setContentsMargins`
- `bar_values.append`
- `error.lower`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `missing_methods.append`
- `self._clear_voice_input_timer.setSingleShot`
- `self._clear_voice_input_timer.start`
- `self._clear_voice_input_timer.stop`
- `self._clear_voice_input_timer.timeout.connect`
- `self._crash_recovery_timer.setSingleShot`
- `self._crash_recovery_timer.start`
- `self._crash_recovery_timer.timeout.connect`
- `self._disable_voice_features`
- `self._disconnect_voice_signals`
- `self._error_reset_timer.setSingleShot`
- `self._error_reset_timer.start`
- `self._error_reset_timer.timeout.connect`
- `self._handle_recording_error_safe`
- `self._handle_service_error`
- `self._handle_tts_error_safe`
- `self._handle_tts_finished_continuous`
- `self._handle_voice_input_error_safe`
- `self._handle_voice_input_safe`
- `self._initialize_voice_service_manager`
- `self._is_similar_voice_input`
- `self._is_voice_service_ready`
- `self._reinitialize_voice_service`
- `self._reset_duplicate_detection_state`
- `self._reset_voice_button`
- `self._reset_voice_ui`
- `self._restart_voice_input_after_cancellation`
- `self._restart_voice_input_after_interruption`
- `self._setup_voice_connections`
- `self._start_continuous_voice_mode`
- `self._stop_all_voice_operations`
- `self._ui_refresh_timer.start`
- `self._ui_refresh_timer.timeout.connect`
- `self._update_audio_level_ui_safe`
- `self._update_eq_bars`
- `self._update_voice_button_state`
- `self._update_voice_state`
- `self._validate_voice_service_capabilities`
- `self._voice_state.values`
- `self.audio_level_changed.emit`
- `self.audio_level_label.setAlignment`
- `self.audio_level_label.setStyleSheet`
- `self.audio_level_label.setText`
- `self.audio_level_label.setToolTip`
- `self.audio_level_meter.setRange`
- `self.audio_level_meter.setStyleSheet`
- `self.audio_level_meter.setValue`
- `self.audio_level_widget.hide`
- `self.audio_level_widget.setStyleSheet`
- `self.audio_level_widget.setVisible`
- `self.cleanup`
- `self.config_manager.get_voice_settings`
- `self.eq_bars_changed.emit`
- `self.eq_visualizer.update_bars`
- `self.eq_visualizer_changed.emit`
- `self.force_reinitialize_voice_service`
- `self.get_voice_service`
- `self.is_tts_playing`
- `self.recording_error.emit`
- `self.recording_started.emit`
- `self.recording_stopped.emit`
- `self.reset_voice_service`
- `self.reset_voice_signal_connections`
- `self.setup_connections`
- `self.setup_ui_components`
- `self.status_label.setText`
- `self.tts_error.emit`
- `self.tts_finished.emit`
- `self.tts_started.emit`
- `self.update_voice_status`
- `self.user_interrupted.emit`
- `self.voice_button.clicked.connect`
- `self.voice_button.hide`
- `self.voice_button.isEnabled`
- `self.voice_button.setEnabled`
- `self.voice_button.setStyleSheet`
- `self.voice_button.setText`
- `self.voice_button.setToolTip`
- `self.voice_input_error.emit`
- `self.voice_input_received.emit`
- `self.voice_mode_changed.emit`
- `self.voice_processing_finished.emit`
- `self.voice_processing_started.emit`
- `self.voice_service.stop_tts`
- `self.voice_service.stop_voice_input`
- `self.voice_service_manager.force_reinitialize`
- `self.voice_service_manager.get_last_error`
- `self.voice_service_manager.get_settings`
- `self.voice_service_manager.get_voice_service`
- `self.voice_service_manager.is_initializing`
- `self.voice_service_manager.is_ready`
- `self.voice_service_manager.update_settings`
- `self.voice_service_manager.voice_service_error.connect`
- `self.voice_service_manager.voice_service_initializing.connect`
- `self.voice_service_manager.voice_service_ready.connect`
- `self.voice_settings.copy`
- `self.voice_settings.update`
- `self.voice_settings_button.hide`
- `self.voice_settings_button.setFixedSize`
- `self.voice_settings_button.setStyleSheet`
- `self.voice_settings_button.setToolTip`
- `self.voice_status_changed.emit`
- `signal.disconnect`
- `status.lower`
- `t1.split`
- `t2.split`
- `text.strip`
- `text1.lower`
- `text2.lower`
- `time.time`
- `traceback.format_exc`
- `voice_service.can_handle_new_request`
- `voice_service.clear_request_queue`
- `voice_service.get_silence_duration`
- `voice_service.get_silence_threshold`
- `voice_service.is_continuous_voice_mode`
- `voice_service.is_voice_available`
- `voice_service.recording_service.audio_level_to_db`
- `voice_service.set_continuous_voice_mode`
- `voice_service.speak_text`
- `voice_service.start_voice_input`
- `voice_service.stop_tts`
- `voice_service.stop_voice_input`
- `voice_service.voice_settings.get`
- `words1.intersection`
- `words1.union`

**`ui\tabs\memory_tab.py`:**
- `CustomLogger.get_logger`
- `QMessageBox.critical`
- `QMessageBox.information`
- `QMessageBox.question`
- `QMessageBox.warning`
- `actions_group.setLayout`
- `actions_layout.addWidget`
- `activity_group.setLayout`
- `activity_layout.addWidget`
- `all_entries.append`
- `context_group.setLayout`
- `context_hbox.addWidget`
- `context_layout.addLayout`
- `context_layout.addWidget`
- `current_item.data`
- `datetime.fromisoformat`
- `details_buttons.addStretch`
- `details_buttons.addWidget`
- `details_group.setLayout`
- `details_layout.addLayout`
- `details_layout.addWidget`
- `filter_layout.addStretch`
- `filter_layout.addWidget`
- `hashlib.md5`
- `item.setData`
- `layout.addLayout`
- `layout.addStretch`
- `layout.addWidget`
- `logger.debug`
- `logger.error`
- `memory.get`
- `search_layout.addWidget`
- `self.auto_summarize_checkbox.setChecked`
- `self.avg_importance_label.setText`
- `self.cleanup_memory_btn.clicked.connect`
- `self.clear_memory_btn.clicked.connect`
- `self.context_messages_label.setText`
- `self.context_slider.setRange`
- `self.context_slider.setValue`
- `self.context_slider.valueChanged.connect`
- `self.context_spinbox.setRange`
- `self.context_spinbox.setValue`
- `self.context_spinbox.valueChanged.connect`
- `self.conversation_service.get_messages`
- `self.create_memories_tab`
- `self.create_overview_tab`
- `self.create_settings_tab`
- `self.create_summaries_tab`
- `self.delete_memory_btn.clicked.connect`
- `self.include_memories_checkbox.setChecked`
- `self.key_points_list.addItem`
- `self.key_points_list.clear`
- `self.key_points_list.setMaximumHeight`
- `self.memories_table.currentRow`
- `self.memories_table.horizontalHeader`
- `self.memories_table.item`
- `self.memories_table.itemSelectionChanged.connect`
- `self.memories_table.setColumnCount`
- `self.memories_table.setHorizontalHeaderLabels`
- `self.memories_table.setItem`
- `self.memories_table.setRowCount`
- `self.memory_details_text.setMaximumHeight`
- `self.memory_details_text.setReadOnly`
- `self.memory_details_text.setText`
- `self.memory_scope_filter.addItems`
- `self.memory_scope_filter.currentIndexChanged.connect`
- `self.memory_scope_filter.currentText`
- `self.memory_service.cleanup_memory_entries`
- `self.memory_service.clear_memory`
- `self.memory_service.delete_memory`
- `self.memory_service.get_memory_stats`
- `self.memory_service.ltm_service.get_entries`
- `self.memory_service.memory_updated.connect`
- `self.memory_service.search_memories`
- `self.memory_service.set_max_context_messages`
- `self.memory_service.stm_service.get_messages`
- `self.memory_service.summarize_conversation`
- `self.memory_service.summary_updated.connect`
- `self.memory_type_filter.addItems`
- `self.memory_type_filter.currentText`
- `self.memory_types_table.horizontalHeader`
- `self.memory_types_table.setColumnCount`
- `self.memory_types_table.setHorizontalHeaderLabels`
- `self.memory_types_table.setItem`
- `self.memory_types_table.setRowCount`
- `self.recent_activity_list.addItem`
- `self.recent_activity_list.clear`
- `self.refresh_data`
- `self.refresh_memories`
- `self.refresh_overview`
- `self.refresh_summaries`
- `self.search_btn.clicked.connect`
- `self.search_input.setPlaceholderText`
- `self.search_input.text`
- `self.semantic_count_label.setText`
- `self.semantic_model_label.setText`
- `self.semantic_status_label.setText`
- `self.setLayout`
- `self.setup_connections`
- `self.setup_ui`
- `self.summaries_list.addItem`
- `self.summaries_list.clear`
- `self.summaries_list.currentItem`
- `self.summaries_list.itemSelectionChanged.connect`
- `self.summarize_btn.clicked.connect`
- `self.summary_details_text.setReadOnly`
- `self.summary_details_text.setText`
- `self.tab_widget.addTab`
- `self.total_memories_label.setText`
- `self.total_summaries_label.setText`
- `semantic_stats.get`
- `signal.disconnect`
- `stats.get`
- `stats_group.setLayout`
- `stats_layout.addWidget`
- `types_group.setLayout`
- `types_layout.addWidget`
- `widget.setLayout`

**`ui\tabs\model_tab.py`:**
- `QMessageBox.critical`
- `QMessageBox.question`
- `QMessageBox.warning`
- `buttons_layout.addWidget`
- `current_item.text`
- `cursor.movePosition`
- `datetime.now`
- `input_layout.addWidget`
- `layout.addWidget`
- `list_layout.addWidget`
- `model_name_label.setStyleSheet`
- `models_group.setStyleSheet`
- `models_layout.addWidget`
- `operation.capitalize`
- `operations_group.setStyleSheet`
- `operations_layout.addWidget`
- `operations_layout_ops.addLayout`
- `parent.addWidget`
- `pull_group.setStyleSheet`
- `pull_layout.addLayout`
- `refresh_button.clicked.connect`
- `refresh_button.setStyleSheet`
- `self.append_status`
- `self.clear_status_button.clicked.connect`
- `self.clear_status_button.setFixedWidth`
- `self.clear_status_button.setToolTip`
- `self.get_current_time`
- `self.model_list.addItem`
- `self.model_list.clear`
- `self.model_list.currentItem`
- `self.model_list.itemSelectionChanged.connect`
- `self.model_list.setStyleSheet`
- `self.model_name_input.setPlaceholderText`
- `self.model_name_input.setStyleSheet`
- `self.model_name_input.text`
- `self.model_pull_requested.emit`
- `self.model_remove_requested.emit`
- `self.model_update_requested.emit`
- `self.parent.ollama_service.get_models`
- `self.progress_bar.setRange`
- `self.progress_bar.setStyleSheet`
- `self.progress_bar.setVisible`
- `self.pull_button.clicked.connect`
- `self.pull_button.setEnabled`
- `self.pull_button.setStyleSheet`
- `self.refresh_models`
- `self.remove_button.clicked.connect`
- `self.remove_button.setEnabled`
- `self.remove_button.setStyleSheet`
- `self.setStyleSheet`
- `self.setup_connections`
- `self.setup_model_list`
- `self.setup_operations`
- `self.setup_ui`
- `self.start_operation`
- `self.status_text.append`
- `self.status_text.clear`
- `self.status_text.setMaximumHeight`
- `self.status_text.setReadOnly`
- `self.status_text.setStyleSheet`
- `self.status_text.setTextCursor`
- `self.status_text.textCursor`
- `self.stop_operation`
- `self.update_button.clicked.connect`
- `self.update_button.setEnabled`
- `self.update_button.setStyleSheet`
- `self.update_model_list`
- `splitter.setSizes`
- `status_group.setStyleSheet`
- `status_layout.addWidget`

**`ui\tabs\personality_tab.py`:**
- `CustomLogger.get_logger`
- `QMessageBox.critical`
- `QMessageBox.information`
- `QMessageBox.question`
- `QMessageBox.warning`
- `basic_group.setStyleSheet`
- `basic_group.styleSheet`
- `basic_layout.addRow`
- `basic_layout.setLabelAlignment`
- `buttons_layout.addStretch`
- `buttons_layout.addWidget`
- `config_layout.addRow`
- `config_layout.setLabelAlignment`
- `constraints_text.split`
- `context_template_layout.addWidget`
- `conversation_style_layout.addWidget`
- `create_button.clicked.connect`
- `create_button.setStyleSheet`
- `creation_widget.setStyleSheet`
- `current_group.setStyleSheet`
- `current_item.text`
- `current_layout.addLayout`
- `current_layout.addWidget`
- `custom_group.setStyleSheet`
- `custom_layout.addLayout`
- `custom_layout.addWidget`
- `datetime.now`
- `delete_button.clicked.connect`
- `delete_button.setStyleSheet`
- `delete_button.setToolTip`
- `examples_text.split`
- `expertise_text.split`
- `export_button.clicked.connect`
- `export_button.setStyleSheet`
- `export_button.setToolTip`
- `item.text`
- `keywords_label.setStyleSheet`
- `keywords_text.setStyleSheet`
- `keywords_text.setWordWrap`
- `layout.addStretch`
- `layout.addWidget`
- `line.strip`
- `logger.debug`
- `logger.error`
- `metadata.get`
- `metadata_layout.addRow`
- `metadata_layout.setLabelAlignment`
- `personality.split`
- `personality_data.get`
- `personality_label.setStyleSheet`
- `prompt_layout.addLayout`
- `prompt_layout.addWidget`
- `refresh_button.clicked.connect`
- `refresh_button.setStyleSheet`
- `refresh_button.setToolTip`
- `scroll_area.setStyleSheet`
- `scroll_area.setWidget`
- `scroll_area.setWidgetResizable`
- `scroll_layout.addWidget`
- `selector_layout.addWidget`
- `self.category_combo.addItems`
- `self.category_combo.currentText`
- `self.category_combo.setCurrentIndex`
- `self.clear_creation_form`
- `self.code_formatting_check.isChecked`
- `self.code_formatting_check.setChecked`
- `self.constraints_edit.clear`
- `self.constraints_edit.setMaximumHeight`
- `self.constraints_edit.setPlaceholderText`
- `self.constraints_edit.toPlainText`
- `self.context_template_combo.addItems`
- `self.context_template_combo.currentText`
- `self.context_template_combo.currentTextChanged.connect`
- `self.context_template_combo.setCurrentIndex`
- `self.conversation_style_combo.addItems`
- `self.conversation_style_combo.currentText`
- `self.conversation_style_combo.setCurrentIndex`
- `self.conversation_style_template_combo.addItems`
- `self.conversation_style_template_combo.currentText`
- `self.conversation_style_template_combo.currentTextChanged.connect`
- `self.conversation_style_template_combo.setCurrentIndex`
- `self.custom_context_edit.clear`
- `self.custom_context_edit.setFocus`
- `self.custom_context_edit.setMaximumHeight`
- `self.custom_context_edit.setPlaceholderText`
- `self.custom_context_edit.setVisible`
- `self.custom_context_edit.toPlainText`
- `self.custom_conversation_edit.clear`
- `self.custom_conversation_edit.setFocus`
- `self.custom_conversation_edit.setPlaceholderText`
- `self.custom_conversation_edit.setVisible`
- `self.custom_conversation_edit.text`
- `self.custom_personalities_list.addItem`
- `self.custom_personalities_list.clear`
- `self.custom_personalities_list.currentItem`
- `self.custom_personalities_list.itemClicked.connect`
- `self.custom_personalities_list.setStyleSheet`
- `self.description_edit.clear`
- `self.description_edit.setMaximumHeight`
- `self.description_edit.setPlaceholderText`
- `self.description_edit.toPlainText`
- `self.emoji_usage_check.isChecked`
- `self.emoji_usage_check.setChecked`
- `self.examples_edit.clear`
- `self.examples_edit.setMaximumHeight`
- `self.examples_edit.setPlaceholderText`
- `self.examples_edit.toPlainText`
- `self.examples_usage_check.isChecked`
- `self.examples_usage_check.setChecked`
- `self.expertise_edit.clear`
- `self.expertise_edit.setMaximumHeight`
- `self.expertise_edit.setPlaceholderText`
- `self.expertise_edit.toPlainText`
- `self.formality_level_combo.addItems`
- `self.formality_level_combo.currentText`
- `self.formality_level_combo.setCurrentIndex`
- `self.frequency_penalty_spin.setDecimals`
- `self.frequency_penalty_spin.setRange`
- `self.frequency_penalty_spin.setSingleStep`
- `self.frequency_penalty_spin.setValue`
- `self.frequency_penalty_spin.value`
- `self.get_context_prompt`
- `self.get_current_personality`
- `self.get_user_prompt_template`
- `self.humor_level_combo.addItems`
- `self.humor_level_combo.currentText`
- `self.humor_level_combo.setCurrentIndex`
- `self.load_personalities`
- `self.max_tokens_spin.setRange`
- `self.max_tokens_spin.setSingleStep`
- `self.max_tokens_spin.setValue`
- `self.max_tokens_spin.value`
- `self.name_edit.clear`
- `self.name_edit.setPlaceholderText`
- `self.name_edit.text`
- `self.personality_changed.emit`
- `self.personality_combo.addItem`
- `self.personality_combo.clear`
- `self.personality_combo.currentTextChanged.connect`
- `self.personality_combo.setCurrentText`
- `self.personality_combo.setStyleSheet`
- `self.personality_info.setMaximumHeight`
- `self.personality_info.setPlainText`
- `self.personality_info.setReadOnly`
- `self.personality_info.setStyleSheet`
- `self.personality_model.create_custom_personality`
- `self.personality_model.delete_custom_personality`
- `self.personality_model.get_available_personalities`
- `self.personality_model.get_personality`
- `self.personality_model.get_selected_model`
- `self.personality_model.refresh_personalities`
- `self.personality_model.service.get_custom_personalities`
- `self.personality_model.service.get_system_personalities`
- `self.personality_model.service.is_custom_personality`
- `self.personality_model.set_current_personality`
- `self.presence_penalty_spin.setDecimals`
- `self.presence_penalty_spin.setRange`
- `self.presence_penalty_spin.setSingleStep`
- `self.presence_penalty_spin.setValue`
- `self.presence_penalty_spin.value`
- `self.questions_usage_check.isChecked`
- `self.questions_usage_check.setChecked`
- `self.response_length_combo.addItems`
- `self.response_length_combo.currentText`
- `self.response_length_combo.setCurrentIndex`
- `self.setStyleSheet`
- `self.setup_creation_tab`
- `self.setup_management_tab`
- `self.setup_selection_tab`
- `self.setup_ui`
- `self.style_edit.clear`
- `self.style_edit.setPlaceholderText`
- `self.style_edit.text`
- `self.system_personalities_list.addItem`
- `self.system_personalities_list.clear`
- `self.system_personalities_list.itemClicked.connect`
- `self.system_personalities_list.setStyleSheet`
- `self.system_personality_info.setMaximumHeight`
- `self.system_personality_info.setReadOnly`
- `self.system_personality_info.setStyleSheet`
- `self.system_personality_info.setText`
- `self.system_prompt_edit.clear`
- `self.system_prompt_edit.setMaximumHeight`
- `self.system_prompt_edit.setPlaceholderText`
- `self.system_prompt_edit.toPlainText`
- `self.tabs.addTab`
- `self.tabs.setStyleSheet`
- `self.tags_edit.clear`
- `self.tags_edit.setPlaceholderText`
- `self.tags_edit.text`
- `self.temperature_spin.setDecimals`
- `self.temperature_spin.setRange`
- `self.temperature_spin.setSingleStep`
- `self.temperature_spin.setValue`
- `self.temperature_spin.value`
- `self.tone_edit.clear`
- `self.tone_edit.setPlaceholderText`
- `self.tone_edit.text`
- `self.top_p_spin.setDecimals`
- `self.top_p_spin.setRange`
- `self.top_p_spin.setSingleStep`
- `self.top_p_spin.setValue`
- `self.top_p_spin.value`
- `self.update_custom_personalities_list`
- `self.update_personality_info`
- `self.update_system_personalities_list`
- `self.update_system_personality_info`
- `self.use_prompt_templates_check.isChecked`
- `self.use_prompt_templates_check.setChecked`
- `system_group.setStyleSheet`
- `system_layout.addWidget`
- `tag.strip`
- `tags_text.split`
- `text.split`
- `traceback.format_exc`
- `traits.get`
- `traits_layout.addRow`
- `traits_layout.setLabelAlignment`
- `x.count`

**`ui\themes\message_formatter.py`:**
- `CustomLogger.get_logger`
- `MessageFormatter._protect_code_blocks`
- `MessageFormatter.cleanup_message`
- `MessageFormatter.detect_and_format_code`
- `MessageFormatter.detect_code_type`
- `MessageFormatter.format_markdown`
- `MessageFormatter.handle_html_tags`
- `MessageFormatter.syntax_highlight_code`
- `code_blocks.append`
- `escaped_message.replace`
- `formatted_lines.append`
- `formatted_lines.extend`
- `line.strip`
- `list_items.append`
- `logger.debug`
- `match.group`
- `message.strip`
- `protected_message.split`
- `re.compile`
- `re.search`
- `re.sub`

**`ui\ui_manager.py`:**
- `CustomLogger.get_logger`
- `PromptFormatter.format_status_message`
- `PromptFormatter.get_menu_text`
- `QMessageBox.about`
- `QMessageBox.question`
- `TabStyles.get_tab_style`
- `about_action.setStatusTip`
- `clear_chat_action.setShortcut`
- `clear_chat_action.setStatusTip`
- `edit_menu.addAction`
- `exit_action.setShortcut`
- `exit_action.setStatusTip`
- `file_menu.addAction`
- `file_menu.addSeparator`
- `help_menu.addAction`
- `load_chat_action.setShortcut`
- `load_chat_action.setStatusTip`
- `logger.error`
- `logger.info`
- `main_layout.addWidget`
- `menubar.addMenu`
- `new_conversation_action.setShortcut`
- `new_conversation_action.setStatusTip`
- `refresh_models_action.setStatusTip`
- `save_chat_action.setShortcut`
- `save_chat_action.setStatusTip`
- `self.main_window.menuBar`
- `self.main_window.setCentralWidget`
- `self.main_window.setGeometry`
- `self.main_window.setStatusBar`
- `self.main_window.setStyleSheet`
- `self.main_window.setWindowTitle`
- `self.memory_tab.set_conversation_service`
- `self.menu_actions.get`
- `self.status_bar.showMessage`
- `self.tabs.addTab`
- `self.tabs.setStyleSheet`
- `settings_action.setShortcut`
- `settings_action.setStatusTip`
- `tools_menu.addAction`

**`ui\utils\message_utils.py`:**
- `CustomLogger.get_logger`
- `dialog.exec`
- `dialog.setIcon`
- `operation.lower`
- `traceback.format_exc`

**`ui\visualizers\widgets\bar_eq_widget.py`:**
- `gradient.setColorAt`
- `painter.drawRect`
- `painter.fillRect`
- `painter.setBrush`
- `painter.setPen`
- `painter.setRenderHint`
- `self._bar_values.copy`
- `self._calculate_bar_geometry`
- `self._create_bar_gradient`
- `self._draw_bar`
- `self._setup_animation_timer`
- `self._target_values.copy`
- `self._timer.start`
- `self._timer.stop`
- `self._timer.timeout.connect`
- `self.height`
- `self.setMinimumSize`
- `self.update`
- `self.width`
- `validated_values.append`
- `validated_values.extend`

**`ui\visualizers\widgets\circle_eq_widget.py`:**
- `gradient.setColorAt`
- `painter.drawPie`
- `painter.fillRect`
- `painter.setBrush`
- `painter.setPen`
- `painter.setRenderHint`
- `self._create_section_gradient`
- `self._section_values.copy`
- `self._setup_animation_timer`
- `self._target_values.copy`
- `self._timer.start`
- `self._timer.stop`
- `self._timer.timeout.connect`
- `self.height`
- `self.setMinimumSize`
- `self.update`
- `self.width`
- `validated_values.append`
- `validated_values.extend`

**`ui\visualizers\widgets\circular_gradient_eq_widget.py`:**
- `c.setAlpha`
- `c2.setAlpha`
- `fill_color.setAlpha`
- `glow_color.setAlpha`
- `grad.setColorAt`
- `math.cos`
- `math.sin`
- `painter.drawEllipse`
- `painter.drawPath`
- `painter.setBrush`
- `painter.setPen`
- `painter.setRenderHint`
- `path.closeSubpath`
- `path.moveTo`
- `path.quadTo`
- `points.append`
- `random.uniform`
- `self._smooth_radii`
- `self._timer.start`
- `self._timer.stop`
- `self._timer.timeout.connect`
- `self.height`
- `self.setMinimumSize`
- `self.start_animation`
- `self.update`
- `self.width`
- `smoothed.append`
- `validated.append`
- `validated.extend`

**`ui\visualizers\widgets\circular_net_eq_widget.py`:**
- `color.setAlpha`
- `dot_color.setAlpha`
- `main_color.setAlpha`
- `math.cos`
- `math.sin`
- `painter.drawEllipse`
- `painter.drawLine`
- `painter.setBrush`
- `painter.setPen`
- `painter.setRenderHint`
- `points.append`
- `random.uniform`
- `self._timer.start`
- `self._timer.stop`
- `self._timer.timeout.connect`
- `self.height`
- `self.setMinimumSize`
- `self.update`
- `self.width`
- `validated.append`
- `validated.extend`


---

## 📈 Statistics

### Classes by Directory

- `app/`: 6 classes
- `config/`: 1 classes
- `core\logging/`: 8 classes
- `core\models/`: 3 classes
- `core\threading/`: 17 classes
- `core\utils/`: 7 classes
- `features\chat/`: 2 classes
- `features\chat\complexity_analyser/`: 3 classes
- `features\chat\enhancers/`: 1 classes
- `features\chat\summarization/`: 1 classes
- `features\memory/`: 12 classes
- `features\ollama/`: 2 classes
- `features\personality/`: 2 classes
- `features\personality\models/`: 7 classes
- `features\personality\services/`: 1 classes
- `features\user/`: 1 classes
- `features\voice/`: 3 classes
- `features\voice\audio/`: 1 classes
- `features\voice\orchestrator/`: 2 classes
- `features\voice\stt/`: 1 classes
- `features\voice\tts/`: 3 classes
- `startup/`: 1 classes
- `ui/`: 1 classes
- `ui\Widgets/`: 4 classes
- `ui\dialogs/`: 8 classes
- `ui\tabs/`: 4 classes
- `ui\tabs\chat_tab/`: 6 classes
- `ui\themes/`: 1 classes
- `ui\visualizers\widgets/`: 4 classes

### Functions by Directory

- `app/`: 149 functions
- `config/`: 43 functions
- `core\logging/`: 61 functions
- `core\models/`: 28 functions
- `core\shared_imports/`: 16 functions
- `core\threading/`: 138 functions
- `core\utils/`: 101 functions
- `features\chat/`: 44 functions
- `features\chat\complexity_analyser/`: 14 functions
- `features\chat\enhancers/`: 4 functions
- `features\chat\summarization/`: 10 functions
- `features\memory/`: 58 functions
- `features\ollama/`: 31 functions
- `features\personality/`: 21 functions
- `features\personality\models/`: 20 functions
- `features\personality\services/`: 28 functions
- `features\user/`: 3 functions
- `features\voice/`: 110 functions
- `features\voice\audio/`: 16 functions
- `features\voice\orchestrator/`: 14 functions
- `features\voice\stt/`: 8 functions
- `features\voice\tts/`: 38 functions
- `startup/`: 17 functions
- `ui/`: 14 functions
- `ui\Widgets/`: 48 functions
- `ui\dialogs/`: 73 functions
- `ui\tabs/`: 68 functions
- `ui\tabs\chat_tab/`: 228 functions
- `ui\themes/`: 13 functions
- `ui\utils/`: 7 functions
- `ui\visualizers\widgets/`: 37 functions

### Call Statistics

- **Total Function Calls:** 1032
- **Total Method Calls:** 3635
- **Files with Function Calls:** 78
- **Files with Method Calls:** 79

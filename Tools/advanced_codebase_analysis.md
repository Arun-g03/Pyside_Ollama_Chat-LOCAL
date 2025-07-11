# Advanced Codebase Analysis Report

**Generated on:** 2025-07-09 01:24:29  
**Root Path:** pyside_chat  
**Total Files Analyzed:** 81

---

## 📊 Summary

- **Total Classes:** 91
- **Total Functions:** 1107
- **Total Files:** 81

### Files by Directory

- `MainApp/`: 6 files
- `Personalities/`: 2 files
- `Personalities\models/`: 3 files
- `Personalities\services/`: 3 files
- `Personalities\utils/`: 2 files
- `config/`: 2 files
- `controllers/`: 2 files
- `models/`: 2 files
- `services/`: 7 files
- `services\Voice_STT_TTS_SERVICES/`: 7 files
- `services\start_up/`: 3 files
- `services\worker/`: 1 files
- `ui/`: 1 files
- `ui\Audio_visualisers/`: 2 files
- `ui\Audio_visualisers\eq_widgets/`: 5 files
- `ui\Widgets/`: 8 files
- `ui\styles/`: 4 files
- `ui\tabs/`: 4 files
- `ui\tabs\chat_tab/`: 8 files
- `utils/`: 7 files
- `utils\Logging/`: 2 files

---

## 🔗 Dependency Analysis

### Most Dependent Files (High In-Degree)

- `config\config_manager`: 45 dependencies
- `utils\Logging\logging_helpers`: 44 dependencies
- `Personalities\services\personality_service`: 42 dependencies
- `models\conversation_metadata`: 42 dependencies
- `services\ollama_service`: 42 dependencies
- `utils\internet_connection`: 42 dependencies
- `services\Voice_STT_TTS_SERVICES\coqui_tts_service`: 42 dependencies
- `services\start_up\install_dependencies`: 42 dependencies
- `MainApp\ui_manager`: 41 dependencies
- `services\worker\worker`: 41 dependencies

### Most Influential Files (High Out-Degree)

- `controllers\chat_controller.py`: 55 dependents
- `utils\streaming_handler.py`: 55 dependents
- `MainApp\ollama_chat.py`: 54 dependents
- `models\conversation_metadata.py`: 54 dependents
- `services\conversation_service.py`: 54 dependents
- `services\memory_service.py`: 54 dependents
- `services\ollama_service.py`: 54 dependents
- `services\semantic_search_service.py`: 54 dependents
- `services\summarization_service.py`: 54 dependents
- `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`: 54 dependents

### ✅ No Circular Dependencies Found


---

## 📁 File Structure

### `MainApp\__init__.py`

---

### `MainApp\app_lifecycle.py`

**Classes:**
- `AppLifecycleManager` (line 14)

**Functions:**
- `__init__` (line 17)
- `initialize_application` (line 27)
- `handle_show_event` (line 49)
- `handle_close_event` (line 70)
- `show_initialization_error` (line 108)
- `show_ollama_connection_error` (line 119)
- `check_ollama_connection` (line 158)
- `is_initialization_complete` (line 163)
- `set_ollama_error_shown` (line 167)
- `get_ollama_error_shown` (line 171)

---

### `MainApp\event_handler.py`

**Classes:**
- `EventBus` (line 12)

**Functions:**
- `__init__` (line 15)
- `setup_connections` (line 36)
- `_connect_menu_actions` (line 91)
- `_on_status_updated` (line 133)
- `_on_error_occurred` (line 137)
- `_on_conversation_updated` (line 142)
- `_on_name_generation_requested` (line 148)
- `_on_models_updated` (line 173)
- `_on_message_sent` (line 187)
- `_send_to_ollama` (line 203)
- `_create_worker_thread` (line 287)
- `_start_worker_stream` (line 345)
- `_on_worker_detailed_error` (line 375)
- `_on_worker_thread_finished` (line 389)
- `_on_worker_chunk` (line 405)
- `_on_worker_finished` (line 419)
- `_on_tts_finished` (line 443)
- `_handle_tts_finished_delayed` (line 452)
- `_cleanup_worker_thread` (line 473)
- `_cleanup_worker_thread_once` (line 485)
- `_final_worker_cleanup` (line 559)
- `_on_worker_error` (line 585)
- `_on_message_finished` (line 601)
- `_on_message_cancelled` (line 610)
- `_on_conversation_selected` (line 637)
- `_on_conversation_deleted` (line 645)
- `_on_conversation_renamed` (line 649)
- `_on_personality_changed` (line 671)
- `_on_model_operation_progress` (line 696)
- `_on_model_operation_error` (line 702)
- `_on_conversation_metadata_updated` (line 716)
- `_on_new_conversation_requested` (line 722)
- `_on_new_conversation` (line 726)
- `_on_clear_chat` (line 743)
- `_on_save_chat` (line 754)
- `_on_load_chat` (line 760)
- `_on_open_settings` (line 766)
- `_create_chat_controller` (line 793)
- `_setup_ui_with_new_services` (line 805)
- `_on_refresh_models` (line 811)
- `_on_refresh_personalities` (line 836)
- `_on_show_about` (line 850)
- `_on_delayed_model_update` (line 854)
- `_check_ollama_connection` (line 870)
- `_show_ollama_connection_error` (line 875)
- `cleanup_on_exit` (line 916)

---

### `MainApp\ollama_chat.py`

**Classes:**
- `OllamaChat` (line 23)

**Functions:**
- `__init__` (line 26)
- `_setup_ui` (line 82)
- `showEvent` (line 110)
- `closeEvent` (line 115)
- `show_ollama_connection_error` (line 119)
- `check_ollama_connection` (line 123)
- `get_service_manager` (line 128)
- `get_ui_manager` (line 132)
- `get_event_handler` (line 136)
- `get_lifecycle_manager` (line 140)
- `get_chat_controller` (line 144)

---

### `MainApp\service_manager.py`

**Classes:**
- `ServiceManager` (line 17)

**Functions:**
- `__init__` (line 20)
- `_initialize_services` (line 33)
- `reinitialize_services` (line 75)
- `get_ollama_service` (line 80)
- `get_conversation_service` (line 84)
- `get_enhancement_service` (line 88)
- `get_memory_service` (line 92)
- `get_summarization_service` (line 96)
- `get_conversation_manager` (line 100)
- `is_memory_enabled` (line 104)
- `get_session_variables` (line 108)
- `cleanup` (line 112)

---

### `MainApp\ui_manager.py`

**Classes:**
- `UIManager` (line 23)

**Functions:**
- `__init__` (line 26)
- `setup_ui` (line 40)
- `setup_menu_bar` (line 93)
- `apply_theme` (line 174)
- `update_status` (line 187)
- `get_menu_action` (line 196)
- `get_chat_tab` (line 200)
- `get_model_tab` (line 204)
- `get_personality_tab` (line 208)
- `get_memory_tab` (line 212)
- `get_tabs` (line 216)
- `show_about_dialog` (line 220)
- `show_clear_chat_dialog` (line 228)

---

### `Personalities\__init__.py`

---

### `Personalities\models\__init__.py`

---

### `Personalities\models\personality_pronouns.py`

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

### `Personalities\models\personality_types.py`

**Classes:**
- `PersonalityType` (line 13)
- `PersonalityTraits` (line 28)
- `PersonalityConfig` (line 46)
- `PersonalityMetadata` (line 57)
- `PersonalityPrompt` (line 72)

**Functions:**
- `__post_init__` (line 66)

---

### `Personalities\personality_model.py`

**Classes:**
- `PersonalityModel` (line 18)

**Functions:**
- `__init__` (line 26)
- `_initialize_default_personalities` (line 34)
- `_find_personality_files` (line 41)
- `_extract_personality_name` (line 45)
- `_load_custom_personalities` (line 49)
- `_find_personality_file_by_name` (line 54)
- `save_custom_personality` (line 58)
- `get_personality_loader` (line 64)
- `get_personality_formatter` (line 68)

---

### `Personalities\services\__init__.py`

---

### `Personalities\services\personality_loader.py`

**Classes:**
- `PersonalityLoader` (line 20)

**Functions:**
- `__init__` (line 23)
- `find_personality_files` (line 35)
- `extract_personality_name` (line 53)
- `load_personality_from_file` (line 68)
- `load_all_personalities` (line 78)
- `save_personality_to_file` (line 90)
- `find_personality_file_by_name` (line 117)
- `delete_personality_file` (line 132)
- `create_personality_data` (line 144)
- `validate_personality_file` (line 162)
- `backup_personality` (line 181)
- `restore_personality_from_backup` (line 210)
- `get_personality_file_info` (line 241)
- `list_backup_files` (line 261)

---

### `Personalities\services\personality_service.py`

**Classes:**
- `PersonalityService` (line 20)

**Functions:**
- `__init__` (line 23)
- `_initialize_personalities` (line 36)
- `is_system_personality` (line 59)
- `is_custom_personality` (line 68)
- `get_system_personalities` (line 72)
- `get_custom_personalities` (line 80)
- `get_available_personalities` (line 88)
- `get_personality` (line 92)
- `set_current_personality` (line 96)
- `get_current_personality` (line 103)
- `create_custom_personality` (line 109)
- `delete_custom_personality` (line 138)
- `update_custom_personality` (line 169)
- `refresh_personalities` (line 194)
- `format_prompt_with_personality` (line 215)
- `get_system_prompt` (line 232)
- `get_personality_info` (line 249)
- `get_personality_config` (line 254)
- `update_personality_metadata` (line 265)
- `build_comprehensive_system_prompt` (line 289)
- `get_user_context_messages` (line 300)
- `get_personality_categories` (line 368)
- `get_personalities_by_category` (line 379)
- `get_personalities_by_folder` (line 392)
- `search_personalities` (line 402)
- `get_selected_model` (line 431)
- `get_ai_name` (line 435)

---

### `Personalities\utils\__init__.py`

---

### `Personalities\utils\personality_formatter.py`

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

### `config\__init__.py`

---

### `config\config_manager.py`

**Classes:**
- `ConfigManager` (line 8)

**Functions:**
- `__init__` (line 11)
- `load_config` (line 15)
- `merge_configs` (line 63)
- `save_config` (line 73)
- `get` (line 86)
- `set` (line 99)
- `get_default_model` (line 116)
- `set_default_model` (line 120)
- `get_default_temperature` (line 124)
- `set_default_temperature` (line 128)
- `get_default_personality` (line 132)
- `set_default_personality` (line 136)
- `get_window_size` (line 140)
- `set_window_size` (line 145)
- `get_chat_settings` (line 149)
- `is_auto_save_enabled` (line 158)
- `set_auto_save_enabled` (line 162)
- `is_spellcheck_enabled` (line 166)
- `set_spellcheck_enabled` (line 170)
- `get_ollama_url` (line 174)
- `set_ollama_url` (line 179)
- `get_history_directory` (line 183)
- `set_history_directory` (line 187)
- `is_enhancement_enabled` (line 191)
- `set_enhancement_enabled` (line 195)
- `is_history_enabled` (line 199)
- `set_history_enabled` (line 203)
- `is_wordwrap_enabled` (line 207)
- `set_wordwrap_enabled` (line 211)
- `is_json_format_enabled` (line 215)
- `set_json_format_enabled` (line 219)
- `is_verbose_enabled` (line 223)
- `set_verbose_enabled` (line 227)
- `is_think_enabled` (line 231)
- `set_think_enabled` (line 235)
- `get_max_tokens` (line 239)
- `get_top_p` (line 242)
- `get_frequency_penalty` (line 245)
- `get_presence_penalty` (line 248)
- `get_max_context_messages` (line 252)
- `set_max_context_messages` (line 256)
- `get_voice_settings` (line 260)
- `set_voice_settings` (line 277)

---

### `controllers\__init__.py`

---

### `controllers\chat_controller.py`

**Classes:**
- `ChatController` (line 41)

**Functions:**
- `remove_emojis` (line 25)
- `__init__` (line 52)
- `is_memory_active` (line 72)
- `process_user_message` (line 76)
- `_handle_memory_operations` (line 113)
- `_extract_and_store_facts` (line 126)
- `_extract_facts_with_llm` (line 144)
- `_store_extracted_facts` (line 206)
- `_send_to_ollama` (line 231)
- `_detect_new_conversation` (line 256)
- `_build_context` (line 270)
- `_select_model` (line 276)
- `accumulate_assistant_response` (line 297)
- `clear_pending_assistant_response` (line 301)
- `handle_ai_response` (line 304)
- `_trigger_tts_for_response` (line 329)
- `set_chat_tab_reference` (line 344)
- `_trigger_name_generation` (line 348)
- `start_new_conversation` (line 355)
- `clear_conversation` (line 402)
- `load_conversation` (line 408)
- `delete_conversation` (line 430)
- `rename_conversation` (line 443)

---

### `models\__init__.py`

---

### `models\conversation_metadata.py`

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

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py`

**Classes:**
- `RecordingService` (line 12)

**Functions:**
- `__init__` (line 21)
- `__del__` (line 50)
- `_check_availability` (line 56)
- `is_available` (line 71)
- `start_recording` (line 74)
- `_record_audio` (line 91)
- `_calculate_audio_level` (line 180)
- `audio_level_to_db` (line 194)
- `get_current_audio_level` (line 205)
- `set_audio_gate_enabled` (line 208)
- `set_speech_detection_parameters` (line 215)
- `get_speech_detection_parameters` (line 225)
- `cleanup` (line 234)
- `stop_recording` (line 243)

---

### `services\Voice_STT_TTS_SERVICES\STT_Service.py`

**Classes:**
- `STTService` (line 9)

**Functions:**
- `__init__` (line 15)
- `_check_availability` (line 21)
- `is_available` (line 43)
- `convert_audio_to_text` (line 46)
- `_convert_with_vosk` (line 53)
- `update_api` (line 86)

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py`

**Classes:**
- `TTSService` (line 16)

**Functions:**
- `__init__` (line 24)
- `_check_availability` (line 47)
- `is_available` (line 56)
- `speak_text` (line 59)
- `speak_text_streaming` (line 74)
- `speak_text_non_streaming` (line 90)
- `_speak_with_espeak` (line 107)
- `_simulate_tts_finished` (line 130)
- `stop_playback` (line 133)
- `update_api` (line 142)
- `update_voice` (line 150)
- `update_speed` (line 158)
- `is_coqui_available` (line 167)
- `get_coqui_models` (line 171)
- `get_coqui_voices` (line 177)
- `get_coqui_model_info` (line 183)
- `load_coqui_model` (line 189)
- `set_coqui_model` (line 195)

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`

**Classes:**
- `StreamingAudioPlayer` (line 32)
- `StreamingAudioWorker` (line 211)
- `CoquiTTSService` (line 355)

**Functions:**
- `__init__` (line 377)
- `run` (line 226)
- `_process_audio_chunk` (line 100)
- `_emit_audio_level` (line 144)
- `set_volume` (line 154)
- `add_audio_chunk` (line 158)
- `end_stream` (line 163)
- `stop_playback` (line 689)
- `cleanup` (line 736)
- `_split_text_into_sentences` (line 258)
- `_generate_audio_chunk` (line 285)
- `_adjust_audio_speed` (line 326)
- `stop` (line 350)
- `__new__` (line 371)
- `_initialize_service` (line 407)
- `_load_default_model` (line 428)
- `_load_available_voices` (line 456)
- `is_available` (line 472)
- `_get_tts_model_cache_dirs` (line 476)
- `_model_name_to_folder` (line 498)
- `_is_model_fully_downloaded` (line 501)
- `get_downloaded_models` (line 517)
- `is_model_downloaded` (line 532)
- `is_model_loaded` (line 535)
- `get_available_voices` (line 544)
- `download_model` (line 553)
- `set_voice` (line 570)
- `set_speed` (line 580)
- `set_streaming_volume` (line 585)
- `speak_text` (line 591)
- `_speak_text_streaming` (line 617)
- `_on_streaming_generation_finished` (line 660)
- `_on_streaming_generation_error` (line 665)
- `_on_streaming_finished` (line 671)
- `_on_streaming_error` (line 683)
- `clear_model_cache` (line 747)
- `get_cache_info` (line 756)
- `get_model_info` (line 769)
- `get_model_download_size` (line 809)
- `get_comprehensive_model_list` (line 834)
- `get_current_model_info` (line 867)
- `get_available_models` (line 879)
- `load_model` (line 901)
- `is_multi_speaker` (line 984)
- `get_model_config` (line 1017)
- `_generate_audio` (line 1031)
- `_play_audio` (line 1067)
- `_on_media_status_changed` (line 1100)
- `_cleanup_audio_file` (line 1109)
- `refresh_model_list` (line 1118)
- `terminate_pyaudio` (line 192)

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`

**Classes:**
- `VoiceProcessManager` (line 24)
- `VoiceProcessMonitor` (line 272)

**Functions:**
- `_voice_process_worker` (line 349)
- `create_voice_process_manager` (line 445)
- `stop_voice_process_manager` (line 462)
- `__init__` (line 278)
- `start_voice_process` (line 52)
- `stop_voice_process` (line 105)
- `send_command` (line 185)
- `_handle_response` (line 202)
- `_handle_monitor_error` (line 241)
- `is_process_running` (line 249)
- `get_process_info` (line 255)
- `run` (line 289)
- `stop` (line 324)
- `get_stats` (line 339)

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py`

**Classes:**
- `VoiceService` (line 31)

**Functions:**
- `__init__` (line 47)
- `__del__` (line 88)
- `start_voice_input` (line 97)
- `stop_voice_input` (line 150)
- `_on_recording_timeout` (line 227)
- `_on_recording_auto_stopped` (line 233)
- `_on_stt_text_received` (line 239)
- `_on_stt_error` (line 271)
- `_on_tts_finished` (line 293)
- `_on_tts_error` (line 311)
- `speak_text` (line 324)
- `speak_text_streaming` (line 353)
- `speak_text_non_streaming` (line 373)
- `stop_tts` (line 393)
- `is_voice_available` (line 399)
- `update_settings` (line 407)
- `get_recording_timeout` (line 456)
- `set_recording_timeout` (line 460)
- `get_silence_duration` (line 465)
- `set_silence_duration` (line 469)
- `get_silence_threshold` (line 474)
- `set_silence_threshold` (line 478)
- `set_min_speech_duration` (line 483)
- `get_min_speech_duration` (line 488)
- `set_speech_detection_sensitivity` (line 492)
- `get_speech_detection_sensitivity` (line 514)
- `set_audio_gate_enabled` (line 523)
- `get_current_audio_level` (line 528)
- `set_continuous_voice_mode` (line 532)
- `is_continuous_voice_mode` (line 537)
- `get_eq_visualizer` (line 541)
- `cleanup_on_exit` (line 545)
- `get_audio_folder_path` (line 560)
- `list_audio_files` (line 564)
- `cleanup_old_audio_files` (line 586)
- `cleanup_all_audio_files` (line 620)
- `_forward_recording_started` (line 639)
- `_forward_recording_stopped` (line 647)
- `_forward_recording_error` (line 655)
- `_forward_voice_processing_started` (line 663)
- `_cleanup_resources` (line 671)
- `_reset_error_count` (line 680)
- `_initialize_services` (line 685)
- `_connect_signals` (line 764)

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`

**Classes:**
- `VoiceServiceWrapper` (line 17)

**Functions:**
- `__init__` (line 33)
- `_init_process_manager` (line 49)
- `_init_direct_service` (line 76)
- `start_voice_input` (line 103)
- `stop_voice_input` (line 112)
- `speak_text` (line 121)
- `speak_text_streaming` (line 130)
- `speak_text_non_streaming` (line 139)
- `stop_tts` (line 148)
- `is_voice_available` (line 157)
- `update_settings` (line 166)
- `get_recording_timeout` (line 175)
- `set_recording_timeout` (line 181)
- `get_silence_duration` (line 186)
- `set_silence_duration` (line 192)
- `get_silence_threshold` (line 197)
- `set_silence_threshold` (line 203)
- `set_audio_gate_enabled` (line 208)
- `get_current_audio_level` (line 213)
- `set_continuous_voice_mode` (line 219)
- `is_continuous_voice_mode` (line 228)
- `cleanup_on_exit` (line 234)
- `get_audio_folder_path` (line 241)
- `list_audio_files` (line 247)
- `cleanup_old_audio_files` (line 253)
- `cleanup_all_audio_files` (line 258)
- `get_process_info` (line 263)
- `test_connection` (line 269)
- `_update_cached_state` (line 275)
- `_update_cached_state_from_signal` (line 281)
- `is_recording` (line 286)
- `is_processing_voice` (line 293)
- `is_playing_tts` (line 300)
- `recording_service` (line 307)

---

### `services\__init__.py`

---

### `services\conversation_service.py`

**Classes:**
- `ConversationService` (line 14)

**Functions:**
- `__init__` (line 19)
- `set_memory_service` (line 28)
- `add_message` (line 32)
- `_add_to_memory` (line 48)
- `get_messages` (line 84)
- `get_context_messages` (line 90)
- `save_conversation` (line 97)
- `load_conversation` (line 126)
- `clear_conversation` (line 146)
- `auto_save` (line 153)

---

### `services\enhancement_service.py`

**Classes:**
- `EnhancementService` (line 8)

**Functions:**
- `__init__` (line 11)
- `should_enhance_response` (line 14)
- `detect_follow_up_question` (line 25)
- `generate_enhanced_response` (line 34)

---

### `services\memory_service.py`

**Classes:**
- `MemoryEntry` (line 20)
- `LongTermMemoryEntry` (line 34)
- `MemoryClassifier` (line 54)
- `PronounNormalizer` (line 161)
- `MemoryRetriever` (line 250)
- `ShortTermMemoryService` (line 323)
- `LongTermMemoryService` (line 377)
- `MemoryService` (line 439)

**Functions:**
- `__post_init__` (line 47)
- `classify_message` (line 92)
- `normalize_pronouns` (line 191)
- `should_normalize` (line 226)
- `calculate_relevance` (line 254)
- `get_relevant_memories` (line 543)
- `__init__` (line 445)
- `_load` (line 385)
- `add_message` (line 847)
- `get_messages` (line 355)
- `clear` (line 909)
- `_save` (line 420)
- `add_entry` (line 400)
- `get_entries` (line 410)
- `update_access_stats` (line 430)
- `_load_memory` (line 470)
- `_save_memory` (line 478)
- `_on_embeddings_updated` (line 486)
- `add_memory` (line 494)
- `add_summary` (line 525)
- `intelligent_add_message` (line 595)
- `extract_facts_from_message` (line 641)
- `get_user_info` (line 670)
- `get_user_name` (line 685)
- `get_context_messages` (line 694)
- `summarize_conversation` (line 721)
- `clear_memory` (line 738)
- `_verify_memory_files_cleared` (line 763)
- `delete_memory` (line 782)
- `get_memory_stats` (line 793)
- `add_fact` (line 854)
- `set_max_context_messages` (line 871)
- `search_memories` (line 880)
- `cleanup_memory_entries` (line 916)

---

### `services\ollama_service.py`

**Classes:**
- `OllamaService` (line 20)

**Functions:**
- `__init__` (line 30)
- `get_models` (line 41)
- `test_connection` (line 90)
- `send_chat_message` (line 102)
- `pull_model` (line 219)
- `_pull_model_thread` (line 231)
- `remove_model` (line 267)
- `_remove_model_thread` (line 279)
- `update_model` (line 315)
- `_update_model_thread` (line 327)
- `_extract_system_prompt` (line 363)
- `_build_session_commands` (line 372)
- `cancel_request` (line 388)
- `reset_cancellation` (line 396)
- `is_connected` (line 404)

---

### `services\semantic_search_service.py`

**Classes:**
- `VectorizedMemory` (line 21)
- `SemanticSearchService` (line 32)

**Functions:**
- `__init__` (line 38)
- `_init_model` (line 56)
- `_load_embeddings` (line 70)
- `_save_embeddings` (line 104)
- `add_memory` (line 138)
- `remove_memory` (line 192)
- `search_semantic` (line 221)
- `search_hybrid` (line 274)
- `update_memory_importance` (line 353)
- `get_memory_stats` (line 380)
- `clear_all` (line 427)
- `is_ready` (line 454)

---

### `services\start_up\__init__.py`

---

### `services\start_up\dependency_checker.py`

**Classes:**
- `DependencyChecker` (line 16)

**Functions:**
- `check_and_install_dependencies` (line 206)
- `__init__` (line 19)
- `test_import` (line 25)
- `check_core_dependencies` (line 41)
- `check_ml_dependencies` (line 82)
- `check_tts_options` (line 101)
- `check_package_versions` (line 117)
- `run_comprehensive_check` (line 154)
- `get_missing_dependencies` (line 165)
- `get_version_conflicts` (line 169)
- `run_install_dependencies` (line 173)
- `get_dependency_summary` (line 198)

---

### `services\start_up\install_dependencies.py`

**Classes:**
- `DependencyInstaller` (line 23)

**Functions:**
- `main` (line 592)
- `__init__` (line 26)
- `print_header` (line 187)
- `check_python_version` (line 194)
- `check_virtual_environment` (line 203)
- `upgrade_pip` (line 213)
- `setup_spellchecker` (line 229)
- `run_stage` (line 275)
- `verify_installation` (line 396)
- `print_summary` (line 475)
- `install_all` (line 553)
- `get_version` (line 401)

---

### `services\summarization_service.py`

**Classes:**
- `SummarizationService` (line 15)

**Functions:**
- `__init__` (line 22)
- `generate_chat_name` (line 28)
- `_create_summarization_prompt` (line 117)
- `_clean_generated_name` (line 142)
- `_has_enough_substance` (line 215)
- `_ai_evaluate_conversation_quality` (line 232)
- `_fallback_quality_check` (line 308)
- `_ai_evaluate_name_quality` (line 337)
- `set_summarization_model` (line 409)
- `set_min_messages_threshold` (line 413)

---

### `services\worker\worker.py`

**Classes:**
- `Worker` (line 10)

**Functions:**
- `__init__` (line 16)
- `_log_thread_info` (line 28)
- `run` (line 35)
- `stop` (line 66)
- `is_running` (line 88)
- `run_stream` (line 94)
- `get_stats` (line 197)

---

### `ui\Audio_visualisers\eq_orchestrator.py`

**Classes:**
- `MainWindow` (line 148)

**Functions:**
- `map_frequency_to_bars` (line 54)
- `band_energy` (line 122)
- `print_sound_devices` (line 647)
- `__init__` (line 152)
- `switch_mode` (line 305)
- `select_audio_file` (line 363)
- `load_audio_preset` (line 371)
- `play_audio` (line 388)
- `stop_audio` (line 399)
- `toggle_mute` (line 414)
- `toggle_system_audio` (line 418)
- `on_device_selected` (line 434)
- `_play_audio_thread` (line 445)
- `_play_microphone_audio` (line 451)
- `_play_file_audio` (line 486)
- `_process_audio_chunk` (line 516)
- `_reset_visualizers` (line 582)
- `populate_device_list` (line 598)
- `refresh_device_list` (line 607)
- `auto_select_microphone` (line 615)
- `resizeEvent` (line 620)
- `callback` (line 493)

---

### `ui\Audio_visualisers\eq_widgets\__init__.py`

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`

**Classes:**
- `BarEQWidget` (line 5)

**Functions:**
- `__init__` (line 25)
- `_setup_animation_timer` (line 49)
- `_animate` (line 55)
- `set_eq_bars` (line 68)
- `set_idle` (line 104)
- `start_animation` (line 109)
- `stop_animation` (line 113)
- `get_current_values` (line 117)
- `_calculate_bar_geometry` (line 131)
- `_create_bar_gradient` (line 154)
- `_draw_bar` (line 208)
- `paintEvent` (line 237)

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`

**Classes:**
- `CircleEQWidget` (line 6)

**Functions:**
- `__init__` (line 24)
- `_setup_animation_timer` (line 48)
- `_animate` (line 54)
- `set_eq_sections` (line 68)
- `set_idle` (line 104)
- `start_animation` (line 109)
- `stop_animation` (line 113)
- `get_current_values` (line 117)
- `_create_section_gradient` (line 131)
- `paintEvent` (line 171)

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`

**Classes:**
- `CircularGradientEQWidget` (line 7)

**Functions:**
- `__init__` (line 17)
- `_smooth_radii` (line 41)
- `_animate` (line 49)
- `set_net_radii` (line 58)
- `set_idle` (line 77)
- `start_animation` (line 83)
- `stop_animation` (line 86)
- `paintEvent` (line 89)

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`

**Classes:**
- `CircularNetEQWidget` (line 7)

**Functions:**
- `__init__` (line 20)
- `_animate` (line 41)
- `set_net_radii` (line 51)
- `set_idle` (line 70)
- `start_animation` (line 74)
- `stop_animation` (line 77)
- `paintEvent` (line 80)

---

### `ui\Audio_visualisers\voice_ring_animation.py`

**Classes:**
- `CircleEQWidget` (line 117)
- `BarEQWidget` (line 325)
- `CircularNetEQWidget` (line 587)
- `CircularGradientEQWidget` (line 710)
- `MainWindow` (line 846)

**Functions:**
- `map_frequency_to_bars` (line 49)
- `print_sound_devices` (line 1625)
- `__init__` (line 850)
- `_setup_animation_timer` (line 369)
- `_animate` (line 752)
- `set_eq_sections` (line 179)
- `set_idle` (line 780)
- `start_animation` (line 786)
- `stop_animation` (line 788)
- `get_current_values` (line 437)
- `_create_section_gradient` (line 242)
- `paintEvent` (line 791)
- `set_eq_bars` (line 388)
- `_calculate_bar_geometry` (line 451)
- `_create_bar_gradient` (line 474)
- `_draw_bar` (line 528)
- `set_net_radii` (line 761)
- `_smooth_radii` (line 744)
- `switch_mode` (line 992)
- `select_audio_file` (line 1093)
- `load_audio_preset` (line 1101)
- `play_audio` (line 1124)
- `stop_audio` (line 1135)
- `toggle_mute` (line 1162)
- `toggle_system_audio` (line 1166)
- `on_device_selected` (line 1183)
- `_play_audio_thread` (line 1195)
- `populate_device_list` (line 1574)
- `refresh_device_list` (line 1585)
- `auto_select_microphone` (line 1595)
- `resizeEvent` (line 1600)
- `callback` (line 1376)
- `band_energy` (line 1328)

---

### `ui\Widgets\__init__.py`

---

### `ui\Widgets\chat_navigation.py`

**Classes:**
- `ChatNavigationWidget` (line 20)

**Functions:**
- `__init__` (line 29)
- `setup_ui` (line 40)
- `setup_connections` (line 154)
- `refresh_conversations` (line 166)
- `create_conversation_item` (line 196)
- `on_conversation_double_clicked` (line 217)
- `show_context_menu` (line 223)
- `rename_conversation` (line 260)
- `delete_conversation` (line 297)
- `set_current_conversation` (line 324)
- `get_selected_conversation` (line 329)
- `clear_all_conversations` (line 336)
- `trigger_name_generation` (line 359)
- `on_summarization_completed` (line 391)
- `on_summarization_failed` (line 417)

---

### `ui\Widgets\coqui_model_dialog.py`

**Classes:**
- `ModelDownloadThread` (line 21)
- `CoquiModelDialog` (line 48)

**Functions:**
- `__init__` (line 54)
- `run` (line 30)
- `setup_ui` (line 70)
- `create_model_panel` (line 199)
- `create_speaker_panel` (line 228)
- `load_models` (line 251)
- `on_model_selected` (line 280)
- `load_speakers_for_model` (line 301)
- `on_speaker_selected` (line 334)
- `download_selected_model` (line 340)
- `start_download` (line 356)
- `on_download_completed` (line 368)
- `update_selection_button` (line 383)
- `accept_selection` (line 390)
- `log_status` (line 398)
- `get_current_time` (line 406)

---

### `ui\Widgets\editable_message_widget.py`

**Classes:**
- `EditableMessageWidget` (line 14)

**Functions:**
- `__init__` (line 21)
- `setup_ui` (line 31)
- `setup_styles` (line 93)
- `start_editing` (line 172)
- `save_edit` (line 181)
- `cancel_edit` (line 191)
- `finish_editing` (line 196)
- `get_content` (line 202)
- `set_content` (line 206)

---

### `ui\Widgets\personality_widget.py`

**Classes:**
- `PersonalityWidget` (line 14)

**Functions:**
- `__init__` (line 19)
- `setup_ui` (line 25)
- `setup_selection_tab` (line 55)
- `setup_creation_tab` (line 91)
- `setup_management_tab` (line 281)
- `load_personalities` (line 319)
- `on_personality_changed` (line 622)
- `set_personality` (line 370)
- `update_personality_info` (line 380)
- `create_personality` (line 447)
- `clear_creation_form` (line 514)
- `on_custom_personality_selected` (line 545)
- `delete_custom_personality` (line 552)
- `export_personality` (line 572)
- `get_current_personality` (line 581)
- `get_formatted_prompt` (line 587)
- `get_system_prompt` (line 591)
- `get_available_personalities` (line 595)
- `get_comprehensive_system_prompt` (line 599)
- `get_user_context_messages` (line 604)
- `refresh_personalities` (line 608)

---

### `ui\Widgets\settings_dialog.py`

**Classes:**
- `SettingsDialog` (line 11)

**Functions:**
- `__init__` (line 14)
- `setup_ui` (line 25)
- `create_general_tab` (line 69)
- `create_chat_tab` (line 133)
- `create_session_tab` (line 180)
- `create_developer_tab` (line 220)
- `_delayed_load_settings` (line 238)
- `load_current_settings` (line 243)
- `save_settings` (line 302)
- `reset_to_defaults` (line 352)

---

### `ui\Widgets\spellchecker_widget.py`

**Classes:**
- `SpellCheckerTextEdit` (line 23)

**Functions:**
- `__init__` (line 26)
- `setup_spellchecker` (line 36)
- `setup_context_menu` (line 53)
- `show_context_menu` (line 58)
- `replace_word` (line 102)
- `add_to_dictionary` (line 112)
- `ignore_word` (line 123)
- `highlight_misspelled_words` (line 127)
- `keyPressEvent` (line 172)
- `on_text_changed` (line 182)
- `enable_spellcheck` (line 189)
- `disable_spellcheck` (line 196)
- `cleanup` (line 208)

---

### `ui\Widgets\voice_settings_dialog.py`

**Classes:**
- `InternetCheckThread` (line 25)
- `VoiceSettingsDialog` (line 38)

**Functions:**
- `run` (line 29)
- `__init__` (line 44)
- `setup_ui` (line 126)
- `create_stt_tab` (line 260)
- `create_tts_tab` (line 300)
- `create_general_tab` (line 398)
- `setup_connections` (line 569)
- `check_internet_connection` (line 581)
- `on_internet_check_completed` (line 590)
- `update_api_availability` (line 604)
- `on_stt_api_changed` (line 626)
- `on_tts_api_changed` (line 638)
- `on_voice_changed` (line 670)
- `on_eq_visualizer_changed` (line 674)
- `load_coqui_models` (line 680)
- `on_coqui_model_changed` (line 707)
- `load_coqui_speakers` (line 737)
- `on_coqui_speaker_changed` (line 760)
- `download_selected_model` (line 765)
- `start_coqui_download` (line 783)
- `on_coqui_download_completed` (line 803)
- `on_silence_threshold_changed` (line 817)
- `test_settings` (line 835)
- `save_settings` (line 889)
- `get_settings` (line 922)
- `set_settings` (line 926)
- `on_tts_settings_changed` (line 997)

---

### `ui\__init__.py`

---

### `ui\styles\__init__.py`

---

### `ui\styles\message_formatter.py`

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

### `ui\styles\styles.py`

---

### `ui\styles\tab_styles.py`

**Classes:**
- `TabStyles` (line 9)

**Functions:**
- `get_tab_style` (line 40)

---

### `ui\tabs\__init__.py`

---

### `ui\tabs\chat_tab\__init__.py`

---

### `ui\tabs\chat_tab\chat_display.py`

**Classes:**
- `ChatDisplay` (line 16)

**Functions:**
- `__init__` (line 22)
- `setup_ui_components` (line 36)
- `setup_streaming_handler` (line 64)
- `get_ai_name` (line 71)
- `chat_display_mouse_move_event` (line 75)
- `show_edit_button` (line 101)
- `hide_edit_button` (line 135)
- `edit_message_at_index` (line 143)
- `show_message_edit_dialog` (line 154)
- `save_message_edit` (line 244)
- `on_message_edited` (line 260)
- `append_to_chat` (line 265)
- `append_response_chunk` (line 280)
- `start_streaming` (line 298)
- `stop_streaming` (line 306)
- `clear_chat` (line 312)
- `get_ui_components` (line 319)
- `get_streaming_handler` (line 326)

---

### `ui\tabs\chat_tab\chat_tab.py`

**Classes:**
- `ChatTab` (line 31)

**Functions:**
- `__init__` (line 45)
- `setup_components` (line 71)
- `setup_ui` (line 91)
- `setup_connections` (line 254)
- `on_message_sent` (line 295)
- `on_message_cancelled` (line 303)
- `on_input_mode_changed` (line 308)
- `on_temperature_changed` (line 357)
- `on_personality_changed` (line 362)
- `on_model_changed` (line 367)
- `on_eq_mode_changed` (line 372)
- `on_voice_input_received` (line 380)
- `on_voice_input_error` (line 396)
- `on_tts_started` (line 401)
- `on_tts_finished` (line 411)
- `on_tts_error` (line 437)
- `on_recording_started` (line 441)
- `on_recording_stopped` (line 445)
- `on_recording_error` (line 449)
- `on_voice_processing_started` (line 453)
- `on_voice_processing_finished` (line 457)
- `on_audio_level_changed` (line 461)
- `on_message_edited` (line 473)
- `get_ai_name` (line 479)
- `get_current_personality` (line 486)
- `get_current_model` (line 490)
- `get_temperature` (line 494)
- `get_current_response` (line 498)
- `append_to_chat` (line 502)
- `append_response_chunk` (line 511)
- `_append_response_chunk_safe` (line 517)
- `start_streaming` (line 535)
- `_start_streaming_safe` (line 541)
- `stop_streaming` (line 570)
- `_stop_streaming_safe` (line 576)
- `force_enable_send_button` (line 608)
- `_force_enable_send_button_safe` (line 614)
- `clear_chat` (line 636)
- `update_model_list` (line 640)
- `update_personality_list` (line 644)
- `speak_ai_response` (line 648)
- `open_voice_settings` (line 652)
- `on_voice_settings_changed` (line 670)
- `load_conversation` (line 680)
- `refresh_navigation` (line 727)
- `set_current_conversation_file` (line 732)
- `get_streaming_handler` (line 737)
- `streaming_handler` (line 742)

---

### `ui\tabs\chat_tab\eq_visualizer.py`

**Classes:**
- `EQVisualizer` (line 20)

**Functions:**
- `__init__` (line 26)
- `setup_eq_visualizers` (line 38)
- `switch_to_eq_visualizer` (line 52)
- `switch_to_chat_display` (line 148)
- `update_eq_visualizer` (line 243)
- `_update_eq_widget_safe` (line 354)
- `is_eq_visualizer_active` (line 367)
- `update_eq_visualizer_mode` (line 373)
- `get_eq_mode` (line 381)
- `get_available_eq_modes` (line 385)

---

### `ui\tabs\chat_tab\input_controls.py`

**Classes:**
- `InputControls` (line 17)

**Functions:**
- `__init__` (line 28)
- `setup_ui_components` (line 43)
- `setup_connections` (line 215)
- `set_input_mode` (line 233)
- `on_temperature_changed` (line 252)
- `on_personality_combo_changed` (line 259)
- `on_model_changed` (line 265)
- `send_message` (line 270)
- `cancel_message` (line 285)
- `start_streaming` (line 290)
- `stop_streaming` (line 313)
- `force_enable_send_button` (line 339)
- `update_model_list` (line 359)
- `update_personality_list` (line 370)
- `get_current_model` (line 381)
- `get_temperature` (line 385)
- `get_current_response` (line 389)
- `get_current_personality` (line 393)
- `get_ui_components` (line 397)
- `eventFilter` (line 411)

---

### `ui\tabs\chat_tab\test_modular_imports.py`

**Functions:**
- `test_imports` (line 5)

---

### `ui\tabs\chat_tab\test_pyside6_imports.py`

**Functions:**
- `test_pyside6_imports` (line 5)
- `test_component_imports` (line 49)

---

### `ui\tabs\chat_tab\voice_controls.py`

**Classes:**
- `VoiceControls` (line 15)

**Functions:**
- `__init__` (line 32)
- `setup_ui_components` (line 112)
- `_update_voice_state` (line 196)
- `is_voice_busy` (line 201)
- `_handle_voice_crash` (line 206)
- `_attempt_recovery` (line 219)
- `_stop_all_voice_operations` (line 229)
- `_reset_voice_ui` (line 240)
- `_reinitialize_voice_service` (line 251)
- `_disable_voice_features` (line 259)
- `_reset_error_count` (line 268)
- `_handle_service_error` (line 272)
- `setup_connections` (line 284)
- `toggle_voice_mode` (line 314)
- `_start_continuous_voice_mode` (line 366)
- `_handle_voice_input_safe` (line 383)
- `_handle_tts_finished_continuous` (line 400)
- `_restart_voice_input` (line 410)
- `_reset_voice_button` (line 424)
- `on_voice_input_received` (line 446)
- `on_voice_input_error` (line 454)
- `_handle_voice_input_error_safe` (line 464)
- `on_tts_started` (line 479)
- `on_tts_finished` (line 484)
- `on_tts_error` (line 495)
- `_handle_tts_error_safe` (line 505)
- `on_recording_started` (line 509)
- `_handle_recording_started_safe` (line 516)
- `on_recording_stopped` (line 537)
- `_handle_recording_stopped_safe` (line 544)
- `on_recording_error` (line 558)
- `_handle_recording_error_safe` (line 565)
- `on_voice_processing_started` (line 580)
- `on_voice_processing_finished` (line 587)
- `on_audio_level_changed` (line 593)
- `_update_audio_level_ui_safe` (line 603)
- `speak_ai_response` (line 662)
- `update_voice_settings` (line 673)
- `get_voice_settings` (line 682)
- `is_voice_mode_active` (line 686)
- `is_tts_playing` (line 690)
- `get_ui_components` (line 700)

---

### `ui\tabs\memory_tab.py`

**Classes:**
- `MemoryTab` (line 20)

**Functions:**
- `__init__` (line 23)
- `setup_ui` (line 30)
- `create_settings_tab` (line 56)
- `create_overview_tab` (line 116)
- `create_memories_tab` (line 176)
- `create_summaries_tab` (line 241)
- `setup_connections` (line 271)
- `update_context_messages` (line 295)
- `refresh_data` (line 300)
- `refresh_overview` (line 306)
- `refresh_memories` (line 362)
- `refresh_summaries` (line 393)
- `search_memories` (line 406)
- `show_memory_details` (line 428)
- `show_summary_details` (line 462)
- `summarize_current_conversation` (line 478)
- `set_conversation_service` (line 484)
- `_summarize_with_service` (line 491)
- `clear_all_memories` (line 512)
- `cleanup_memory_entries` (line 525)
- `delete_selected_memory` (line 541)

---

### `ui\tabs\model_tab.py`

**Classes:**
- `ModelTab` (line 15)

**Functions:**
- `__init__` (line 23)
- `setup_ui` (line 46)
- `setup_model_list` (line 63)
- `setup_operations` (line 139)
- `setup_connections` (line 359)
- `refresh_models` (line 369)
- `update_model_list` (line 377)
- `pull_model` (line 387)
- `remove_selected_model` (line 405)
- `update_selected_model` (line 425)
- `on_model_selection_changed` (line 445)
- `start_operation` (line 452)
- `stop_operation` (line 461)
- `append_status` (line 469)
- `get_current_time` (line 478)
- `on_operation_progress` (line 483)
- `on_operation_finished` (line 487)
- `on_operation_error` (line 495)
- `get_selected_model` (line 501)
- `clear_status` (line 506)

---

### `ui\tabs\personality_tab.py`

**Classes:**
- `PersonalityTab` (line 17)

**Functions:**
- `__init__` (line 23)
- `setup_ui` (line 30)
- `setup_selection_tab` (line 90)
- `setup_creation_tab` (line 197)
- `setup_management_tab` (line 380)
- `load_personalities` (line 553)
- `update_system_personalities_list` (line 589)
- `update_custom_personalities_list` (line 600)
- `on_system_personality_selected` (line 611)
- `update_system_personality_info` (line 617)
- `on_custom_personality_selected` (line 638)
- `on_personality_changed` (line 644)
- `update_personality_info` (line 650)
- `create_personality` (line 673)
- `clear_creation_form` (line 730)
- `delete_custom_personality` (line 738)
- `export_personality` (line 771)
- `refresh_personalities` (line 792)
- `get_current_personality` (line 801)
- `get_system_prompt` (line 805)
- `get_available_personalities` (line 816)

---

### `utils\Logging\Custom_Logger.py`

**Classes:**
- `PrintOnLogMixin` (line 35)
- `CustomLogger` (line 64)
- `PrintLogger` (line 151)
- `DummyLogger` (line 117)

**Functions:**
- `_sanitize_filename` (line 17)
- `strip_emojis` (line 20)
- `_print` (line 36)
- `info` (line 118)
- `debug` (line 119)
- `warning` (line 120)
- `error` (line 121)
- `critical` (line 122)
- `_check_config_for_logging` (line 83)
- `__new__` (line 95)
- `set_logging_enabled` (line 102)
- `_clear_log_file` (line 106)
- `get_logger` (line 113)
- `_filter_non_ascii` (line 177)

---

### `utils\Logging\logging_helpers.py`

**Classes:**
- `LoggingHelpers` (line 19)
- `ThreadMonitor` (line 207)
- `ThreadSafeLogger` (line 370)

**Functions:**
- `get_thread_monitor` (line 417)
- `cleanup_thread_monitor` (line 424)
- `log_exception_with_context` (line 23)
- `log_warning_with_context` (line 30)
- `log_info_with_context` (line 36)
- `log_debug` (line 42)
- `log_error` (line 47)
- `log_network_request` (line 52)
- `log_file_operation` (line 62)
- `log_audio_operation` (line 70)
- `log_memory_operation` (line 78)
- `log_ui_operation` (line 86)
- `log_performance_metric` (line 94)
- `log_json_parsing_error` (line 100)
- `log_json_parsing_success` (line 106)
- `log_critical_error` (line 111)
- `log_fact_extraction_start` (line 118)
- `log_fact_extraction_end` (line 123)
- `log_fact_extraction_result` (line 128)
- `log_fact_processing` (line 133)
- `log_fact_storage_start` (line 138)
- `log_fact_storage_end` (line 143)
- `log_fact_storage_summary` (line 148)
- `log_fact_skipped` (line 153)
- `log_memory_result` (line 158)
- `log_memory_ltm_status` (line 163)
- `log_llm_call` (line 168)
- `log_llm_response` (line 173)
- `log_json_extraction` (line 178)
- `log_message_sent` (line 183)
- `log_message_sent_end` (line 188)
- `log_conversation_detection` (line 193)
- `log_service_initialization` (line 198)
- `__init__` (line 214)
- `register_thread` (line 222)
- `unregister_thread` (line 252)
- `_on_thread_started` (line 272)
- `_on_thread_finished` (line 284)
- `get_thread_info` (line 298)
- `get_all_threads` (line 302)
- `get_thread_history` (line 306)
- `get_thread_stats` (line 310)
- `cleanup` (line 350)
- `log_thread_context` (line 374)
- `log_thread_safety_check` (line 392)
- `log_thread_operation` (line 407)

---

### `utils\__init__.py`

---

### `utils\complexity_analyzer.py`

**Classes:**
- `ComplexityLevel` (line 9)
- `ComplexityMetrics` (line 17)
- `RequestComplexityAnalyzer` (line 31)

**Functions:**
- `__init__` (line 34)
- `analyze_complexity` (line 114)
- `_estimate_tokens` (line 180)
- `_analyze_reasoning_depth` (line 186)
- `_analyze_knowledge_breadth` (line 222)
- `_analyze_ambiguity` (line 247)
- `_count_constraints` (line 266)
- `_analyze_context_dependency` (line 281)
- `_analyze_output_complexity` (line 301)
- `_determine_complexity_level` (line 321)
- `_generate_recommendations` (line 332)
- `get_model_recommendation` (line 374)
- `format_complexity_report` (line 395)
- `extract_size` (line 377)

---

### `utils\complexity_widget.py`

**Classes:**
- `ComplexityWidget` (line 8)

**Functions:**
- `__init__` (line 13)
- `setup_ui` (line 19)
- `analyze_request` (line 112)
- `_update_display` (line 132)
- `_update_model_recommendation` (line 184)
- `_on_switch_model` (line 190)
- `_set_widget_color` (line 195)
- `_set_progress_bar_color` (line 201)
- `_get_color_for_value` (line 217)
- `clear_analysis` (line 231)
- `get_current_metrics` (line 239)

---

### `utils\error_handler.py`

**Classes:**
- `ErrorHandler` (line 20)

**Functions:**
- `error_context` (line 229)
- `network_error_context` (line 252)
- `file_operation_context` (line 269)
- `audio_operation_context` (line 286)
- `memory_operation_context` (line 302)
- `ui_operation_context` (line 319)
- `safe_json_parse` (line 335)
- `safe_file_read` (line 357)
- `safe_file_write` (line 377)
- `safe_network_request` (line 401)
- `validate_input` (line 423)
- `cleanup_resources` (line 448)
- `handle_critical_error` (line 467)
- `safe_execute` (line 24)
- `retry_on_failure` (line 49)
- `handle_network_errors` (line 91)
- `handle_file_operations` (line 125)
- `handle_audio_operations` (line 159)
- `handle_memory_operations` (line 182)
- `handle_ui_operations` (line 205)
- `wrapper` (line 216)

---

### `utils\internet_connection.py`

**Classes:**
- `InternetConnectionTester` (line 15)

**Functions:**
- `test_internet_connection` (line 125)
- `test_internet_connection_detailed` (line 139)
- `is_online` (line 153)
- `check_internet` (line 164)
- `__init__` (line 22)
- `test_socket_connection` (line 41)
- `test_http_connection` (line 58)
- `test_connection` (line 75)
- `test_connection_with_details` (line 94)

---

### `utils\prompts.py`

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

### `utils\streaming_handler.py`

**Classes:**
- `StreamingHandler` (line 17)

**Functions:**
- `__init__` (line 23)
- `_get_next_message_id` (line 36)
- `_flush_stream_buffer` (line 41)
- `append_message` (line 60)
- `start_streaming_message` (line 76)
- `edit_message` (line 90)
- `get_message_by_id` (line 103)
- `get_editable_messages` (line 110)
- `get_messages` (line 123)
- `_render_chat_display` (line 127)
- `_render_chat_display_safe` (line 133)
- `_safe_ui_update` (line 279)
- `update_streaming_message` (line 298)
- `finalize_streaming_message` (line 320)
- `update_last_system_switch` (line 349)
- `remove_streaming_placeholder` (line 366)
- `cleanup` (line 384)
- `clear_chat` (line 396)
- `update_ai_name` (line 408)

---

## 🏗️ Classes

### `MainApp\app_lifecycle.py.AppLifecycleManager`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 14
- **Docstring:** Manages application startup, shutdown, and error handling...

**Methods:**
- `__init__` (line 17)
- `initialize_application` (line 27)
- `handle_show_event` (line 49)
- `handle_close_event` (line 70)
- `show_initialization_error` (line 108)
- `show_ollama_connection_error` (line 119)
- `check_ollama_connection` (line 158)
- `is_initialization_complete` (line 163)
- `set_ollama_error_shown` (line 167)
- `get_ollama_error_shown` (line 171)

---

### `MainApp\event_handler.py.EventBus`

- **File:** `MainApp\event_handler.py`
- **Line:** 12
- **Docstring:** Manages signal connections and event handling...

**Methods:**
- `__init__` (line 15)
- `setup_connections` (line 36)
- `_connect_menu_actions` (line 91)
- `_on_status_updated` (line 133)
- `_on_error_occurred` (line 137)
- `_on_conversation_updated` (line 142)
- `_on_name_generation_requested` (line 148)
- `_on_models_updated` (line 173)
- `_on_message_sent` (line 187)
- `_send_to_ollama` (line 203)
- `_create_worker_thread` (line 287)
- `_start_worker_stream` (line 345)
- `_on_worker_detailed_error` (line 375)
- `_on_worker_thread_finished` (line 389)
- `_on_worker_chunk` (line 405)
- `_on_worker_finished` (line 419)
- `_on_tts_finished` (line 443)
- `_handle_tts_finished_delayed` (line 452)
- `_cleanup_worker_thread` (line 473)
- `_cleanup_worker_thread_once` (line 485)
- `_final_worker_cleanup` (line 559)
- `_on_worker_error` (line 585)
- `_on_message_finished` (line 601)
- `_on_message_cancelled` (line 610)
- `_on_conversation_selected` (line 637)
- `_on_conversation_deleted` (line 645)
- `_on_conversation_renamed` (line 649)
- `_on_personality_changed` (line 671)
- `_on_model_operation_progress` (line 696)
- `_on_model_operation_error` (line 702)
- `_on_conversation_metadata_updated` (line 716)
- `_on_new_conversation_requested` (line 722)
- `_on_new_conversation` (line 726)
- `_on_clear_chat` (line 743)
- `_on_save_chat` (line 754)
- `_on_load_chat` (line 760)
- `_on_open_settings` (line 766)
- `_create_chat_controller` (line 793)
- `_setup_ui_with_new_services` (line 805)
- `_on_refresh_models` (line 811)
- `_on_refresh_personalities` (line 836)
- `_on_show_about` (line 850)
- `_on_delayed_model_update` (line 854)
- `_check_ollama_connection` (line 870)
- `_show_ollama_connection_error` (line 875)
- `cleanup_on_exit` (line 916)

---

### `MainApp\ollama_chat.py.OllamaChat`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 23
- **Bases:** QMainWindow
- **Docstring:** Main application window - refactored with modular components...

**Methods:**
- `__init__` (line 26)
- `_setup_ui` (line 82)
- `showEvent` (line 110)
- `closeEvent` (line 115)
- `show_ollama_connection_error` (line 119)
- `check_ollama_connection` (line 123)
- `get_service_manager` (line 128)
- `get_ui_manager` (line 132)
- `get_event_handler` (line 136)
- `get_lifecycle_manager` (line 140)
- `get_chat_controller` (line 144)

---

### `MainApp\service_manager.py.ServiceManager`

- **File:** `MainApp\service_manager.py`
- **Line:** 17
- **Docstring:** Manages all application services and their initialization...

**Methods:**
- `__init__` (line 20)
- `_initialize_services` (line 33)
- `reinitialize_services` (line 75)
- `get_ollama_service` (line 80)
- `get_conversation_service` (line 84)
- `get_enhancement_service` (line 88)
- `get_memory_service` (line 92)
- `get_summarization_service` (line 96)
- `get_conversation_manager` (line 100)
- `is_memory_enabled` (line 104)
- `get_session_variables` (line 108)
- `cleanup` (line 112)

---

### `MainApp\ui_manager.py.UIManager`

- **File:** `MainApp\ui_manager.py`
- **Line:** 23
- **Docstring:** Manages UI setup, menu creation, and styling...

**Methods:**
- `__init__` (line 26)
- `setup_ui` (line 40)
- `setup_menu_bar` (line 93)
- `apply_theme` (line 174)
- `update_status` (line 187)
- `get_menu_action` (line 196)
- `get_chat_tab` (line 200)
- `get_model_tab` (line 204)
- `get_personality_tab` (line 208)
- `get_memory_tab` (line 212)
- `get_tabs` (line 216)
- `show_about_dialog` (line 220)
- `show_clear_chat_dialog` (line 228)

---

### `Personalities\models\personality_pronouns.py.PersonalityPronouns`

- **File:** `Personalities\models\personality_pronouns.py`
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

### `Personalities\models\personality_types.py.PersonalityConfig`

- **File:** `Personalities\models\personality_types.py`
- **Line:** 46
- **Decorators:** dataclass
- **Docstring:** Data class for personality-specific configuration...

---

### `Personalities\models\personality_types.py.PersonalityMetadata`

- **File:** `Personalities\models\personality_types.py`
- **Line:** 57
- **Decorators:** dataclass
- **Docstring:** Data class for personality metadata...

**Methods:**
- `__post_init__` (line 66)

---

### `Personalities\models\personality_types.py.PersonalityPrompt`

- **File:** `Personalities\models\personality_types.py`
- **Line:** 72
- **Decorators:** dataclass
- **Docstring:** Data class for personality prompt templates...

---

### `Personalities\models\personality_types.py.PersonalityTraits`

- **File:** `Personalities\models\personality_types.py`
- **Line:** 28
- **Decorators:** dataclass
- **Docstring:** Data class for personality traits...

---

### `Personalities\models\personality_types.py.PersonalityType`

- **File:** `Personalities\models\personality_types.py`
- **Line:** 13
- **Bases:** Enum
- **Docstring:** Enumeration of available personality types...

---

### `Personalities\personality_model.py.PersonalityModel`

- **File:** `Personalities\personality_model.py`
- **Line:** 18
- **Bases:** PersonalityService
- **Docstring:** Main class for managing AI personalities

This is the refactored version that inherits from Personal...

**Methods:**
- `__init__` (line 26)
- `_initialize_default_personalities` (line 34)
- `_find_personality_files` (line 41)
- `_extract_personality_name` (line 45)
- `_load_custom_personalities` (line 49)
- `_find_personality_file_by_name` (line 54)
- `save_custom_personality` (line 58)
- `get_personality_loader` (line 64)
- `get_personality_formatter` (line 68)

---

### `Personalities\services\personality_loader.py.PersonalityLoader`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 20
- **Docstring:** Handles loading and saving personality data from/to files...

**Methods:**
- `__init__` (line 23)
- `find_personality_files` (line 35)
- `extract_personality_name` (line 53)
- `load_personality_from_file` (line 68)
- `load_all_personalities` (line 78)
- `save_personality_to_file` (line 90)
- `find_personality_file_by_name` (line 117)
- `delete_personality_file` (line 132)
- `create_personality_data` (line 144)
- `validate_personality_file` (line 162)
- `backup_personality` (line 181)
- `restore_personality_from_backup` (line 210)
- `get_personality_file_info` (line 241)
- `list_backup_files` (line 261)

---

### `Personalities\services\personality_service.py.PersonalityService`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 20
- **Docstring:** Main service for managing AI personalities...

**Methods:**
- `__init__` (line 23)
- `_initialize_personalities` (line 36)
- `is_system_personality` (line 59)
- `is_custom_personality` (line 68)
- `get_system_personalities` (line 72)
- `get_custom_personalities` (line 80)
- `get_available_personalities` (line 88)
- `get_personality` (line 92)
- `set_current_personality` (line 96)
- `get_current_personality` (line 103)
- `create_custom_personality` (line 109)
- `delete_custom_personality` (line 138)
- `update_custom_personality` (line 169)
- `refresh_personalities` (line 194)
- `format_prompt_with_personality` (line 215)
- `get_system_prompt` (line 232)
- `get_personality_info` (line 249)
- `get_personality_config` (line 254)
- `update_personality_metadata` (line 265)
- `build_comprehensive_system_prompt` (line 289)
- `get_user_context_messages` (line 300)
- `get_personality_categories` (line 368)
- `get_personalities_by_category` (line 379)
- `get_personalities_by_folder` (line 392)
- `search_personalities` (line 402)
- `get_selected_model` (line 431)
- `get_ai_name` (line 435)

---

### `Personalities\utils\personality_formatter.py.PersonalityFormatter`

- **File:** `Personalities\utils\personality_formatter.py`
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

### `config\config_manager.py.ConfigManager`

- **File:** `config\config_manager.py`
- **Line:** 8
- **Docstring:** Manages application configuration settings...

**Methods:**
- `__init__` (line 11)
- `load_config` (line 15)
- `merge_configs` (line 63)
- `save_config` (line 73)
- `get` (line 86)
- `set` (line 99)
- `get_default_model` (line 116)
- `set_default_model` (line 120)
- `get_default_temperature` (line 124)
- `set_default_temperature` (line 128)
- `get_default_personality` (line 132)
- `set_default_personality` (line 136)
- `get_window_size` (line 140)
- `set_window_size` (line 145)
- `get_chat_settings` (line 149)
- `is_auto_save_enabled` (line 158)
- `set_auto_save_enabled` (line 162)
- `is_spellcheck_enabled` (line 166)
- `set_spellcheck_enabled` (line 170)
- `get_ollama_url` (line 174)
- `set_ollama_url` (line 179)
- `get_history_directory` (line 183)
- `set_history_directory` (line 187)
- `is_enhancement_enabled` (line 191)
- `set_enhancement_enabled` (line 195)
- `is_history_enabled` (line 199)
- `set_history_enabled` (line 203)
- `is_wordwrap_enabled` (line 207)
- `set_wordwrap_enabled` (line 211)
- `is_json_format_enabled` (line 215)
- `set_json_format_enabled` (line 219)
- `is_verbose_enabled` (line 223)
- `set_verbose_enabled` (line 227)
- `is_think_enabled` (line 231)
- `set_think_enabled` (line 235)
- `get_max_tokens` (line 239)
- `get_top_p` (line 242)
- `get_frequency_penalty` (line 245)
- `get_presence_penalty` (line 248)
- `get_max_context_messages` (line 252)
- `set_max_context_messages` (line 256)
- `get_voice_settings` (line 260)
- `set_voice_settings` (line 277)

---

### `controllers\chat_controller.py.ChatController`

- **File:** `controllers\chat_controller.py`
- **Line:** 41
- **Bases:** QObject
- **Docstring:** Controller class that mediates between UI components and business logic...

**Methods:**
- `__init__` (line 52)
- `is_memory_active` (line 72)
- `process_user_message` (line 76)
- `_handle_memory_operations` (line 113)
- `_extract_and_store_facts` (line 126)
- `_extract_facts_with_llm` (line 144)
- `_store_extracted_facts` (line 206)
- `_send_to_ollama` (line 231)
- `_detect_new_conversation` (line 256)
- `_build_context` (line 270)
- `_select_model` (line 276)
- `accumulate_assistant_response` (line 297)
- `clear_pending_assistant_response` (line 301)
- `handle_ai_response` (line 304)
- `_trigger_tts_for_response` (line 329)
- `set_chat_tab_reference` (line 344)
- `_trigger_name_generation` (line 348)
- `start_new_conversation` (line 355)
- `clear_conversation` (line 402)
- `load_conversation` (line 408)
- `delete_conversation` (line 430)
- `rename_conversation` (line 443)

---

### `models\conversation_metadata.py.ConversationManager`

- **File:** `models\conversation_metadata.py`
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

### `models\conversation_metadata.py.ConversationMetadata`

- **File:** `models\conversation_metadata.py`
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

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.RecordingService`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 12
- **Bases:** QObject
- **Docstring:** Audio recording service for capturing voice input...

**Methods:**
- `__init__` (line 21)
- `__del__` (line 50)
- `_check_availability` (line 56)
- `is_available` (line 71)
- `start_recording` (line 74)
- `_record_audio` (line 91)
- `_calculate_audio_level` (line 180)
- `audio_level_to_db` (line 194)
- `get_current_audio_level` (line 205)
- `set_audio_gate_enabled` (line 208)
- `set_speech_detection_parameters` (line 215)
- `get_speech_detection_parameters` (line 225)
- `cleanup` (line 234)
- `stop_recording` (line 243)

---

### `services\Voice_STT_TTS_SERVICES\STT_Service.py.STTService`

- **File:** `services\Voice_STT_TTS_SERVICES\STT_Service.py`
- **Line:** 9
- **Bases:** QObject
- **Docstring:** Speech-to-Text service for converting voice to text...

**Methods:**
- `__init__` (line 15)
- `_check_availability` (line 21)
- `is_available` (line 43)
- `convert_audio_to_text` (line 46)
- `_convert_with_vosk` (line 53)
- `update_api` (line 86)

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.TTSService`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 16
- **Bases:** QObject
- **Docstring:** Text-to-Speech service for converting text to speech...

**Methods:**
- `__init__` (line 24)
- `_check_availability` (line 47)
- `is_available` (line 56)
- `speak_text` (line 59)
- `speak_text_streaming` (line 74)
- `speak_text_non_streaming` (line 90)
- `_speak_with_espeak` (line 107)
- `_simulate_tts_finished` (line 130)
- `stop_playback` (line 133)
- `update_api` (line 142)
- `update_voice` (line 150)
- `update_speed` (line 158)
- `is_coqui_available` (line 167)
- `get_coqui_models` (line 171)
- `get_coqui_voices` (line 177)
- `get_coqui_model_info` (line 183)
- `load_coqui_model` (line 189)
- `set_coqui_model` (line 195)

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.CoquiTTSService`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 355
- **Bases:** QObject
- **Docstring:** Advanced TTS service using Coqui TTS library with streaming support...

**Methods:**
- `__new__` (line 371)
- `__init__` (line 377)
- `_initialize_service` (line 407)
- `_load_default_model` (line 428)
- `_load_available_voices` (line 456)
- `is_available` (line 472)
- `_get_tts_model_cache_dirs` (line 476)
- `_model_name_to_folder` (line 498)
- `_is_model_fully_downloaded` (line 501)
- `get_downloaded_models` (line 517)
- `is_model_downloaded` (line 532)
- `is_model_loaded` (line 535)
- `get_available_voices` (line 544)
- `download_model` (line 553)
- `set_voice` (line 570)
- `set_speed` (line 580)
- `set_streaming_volume` (line 585)
- `speak_text` (line 591)
- `_speak_text_streaming` (line 617)
- `_on_streaming_generation_finished` (line 660)
- `_on_streaming_generation_error` (line 665)
- `_on_streaming_finished` (line 671)
- `_on_streaming_error` (line 683)
- `stop_playback` (line 689)
- `cleanup` (line 736)
- `clear_model_cache` (line 747)
- `get_cache_info` (line 756)
- `get_model_info` (line 769)
- `get_model_download_size` (line 809)
- `get_comprehensive_model_list` (line 834)
- `get_current_model_info` (line 867)
- `get_available_models` (line 879)
- `load_model` (line 901)
- `is_multi_speaker` (line 984)
- `get_model_config` (line 1017)
- `_generate_audio` (line 1031)
- `_play_audio` (line 1067)
- `_on_media_status_changed` (line 1100)
- `_cleanup_audio_file` (line 1109)
- `refresh_model_list` (line 1118)

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.StreamingAudioPlayer`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 32
- **Bases:** QThread
- **Docstring:** Thread for streaming audio playback...

**Methods:**
- `__init__` (line 40)
- `run` (line 61)
- `_process_audio_chunk` (line 100)
- `_emit_audio_level` (line 144)
- `set_volume` (line 154)
- `add_audio_chunk` (line 158)
- `end_stream` (line 163)
- `stop_playback` (line 168)
- `cleanup` (line 178)

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.StreamingAudioWorker`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 211
- **Bases:** QObject
- **Docstring:** Worker for streaming audio generation in a separate thread...

**Methods:**
- `__init__` (line 220)
- `run` (line 226)
- `_split_text_into_sentences` (line 258)
- `_generate_audio_chunk` (line 285)
- `_adjust_audio_speed` (line 326)
- `stop` (line 350)

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.VoiceProcessManager`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 24
- **Bases:** QObject
- **Docstring:** Manages voice services in a separate process...

**Methods:**
- `__init__` (line 41)
- `start_voice_process` (line 52)
- `stop_voice_process` (line 105)
- `send_command` (line 185)
- `_handle_response` (line 202)
- `_handle_monitor_error` (line 241)
- `is_process_running` (line 249)
- `get_process_info` (line 255)

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.VoiceProcessMonitor`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 272
- **Bases:** QThread
- **Docstring:** Thread to monitor responses from the voice process...

**Methods:**
- `__init__` (line 278)
- `run` (line 289)
- `stop` (line 324)
- `get_stats` (line 339)

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.VoiceService`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 31
- **Bases:** QObject
- **Docstring:** Main voice service that orchestrates STT and TTS functionality...

**Methods:**
- `__init__` (line 47)
- `__del__` (line 88)
- `start_voice_input` (line 97)
- `stop_voice_input` (line 150)
- `_on_recording_timeout` (line 227)
- `_on_recording_auto_stopped` (line 233)
- `_on_stt_text_received` (line 239)
- `_on_stt_error` (line 271)
- `_on_tts_finished` (line 293)
- `_on_tts_error` (line 311)
- `speak_text` (line 324)
- `speak_text_streaming` (line 353)
- `speak_text_non_streaming` (line 373)
- `stop_tts` (line 393)
- `is_voice_available` (line 399)
- `update_settings` (line 407)
- `get_recording_timeout` (line 456)
- `set_recording_timeout` (line 460)
- `get_silence_duration` (line 465)
- `set_silence_duration` (line 469)
- `get_silence_threshold` (line 474)
- `set_silence_threshold` (line 478)
- `set_min_speech_duration` (line 483)
- `get_min_speech_duration` (line 488)
- `set_speech_detection_sensitivity` (line 492)
- `get_speech_detection_sensitivity` (line 514)
- `set_audio_gate_enabled` (line 523)
- `get_current_audio_level` (line 528)
- `set_continuous_voice_mode` (line 532)
- `is_continuous_voice_mode` (line 537)
- `get_eq_visualizer` (line 541)
- `cleanup_on_exit` (line 545)
- `get_audio_folder_path` (line 560)
- `list_audio_files` (line 564)
- `cleanup_old_audio_files` (line 586)
- `cleanup_all_audio_files` (line 620)
- `_forward_recording_started` (line 639)
- `_forward_recording_stopped` (line 647)
- `_forward_recording_error` (line 655)
- `_forward_voice_processing_started` (line 663)
- `_cleanup_resources` (line 671)
- `_reset_error_count` (line 680)
- `_initialize_services` (line 685)
- `_connect_signals` (line 764)

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.VoiceServiceWrapper`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 17
- **Bases:** QObject
- **Docstring:** Wrapper for voice services that runs in a separate process...

**Methods:**
- `__init__` (line 33)
- `_init_process_manager` (line 49)
- `_init_direct_service` (line 76)
- `start_voice_input` (line 103)
- `stop_voice_input` (line 112)
- `speak_text` (line 121)
- `speak_text_streaming` (line 130)
- `speak_text_non_streaming` (line 139)
- `stop_tts` (line 148)
- `is_voice_available` (line 157)
- `update_settings` (line 166)
- `get_recording_timeout` (line 175)
- `set_recording_timeout` (line 181)
- `get_silence_duration` (line 186)
- `set_silence_duration` (line 192)
- `get_silence_threshold` (line 197)
- `set_silence_threshold` (line 203)
- `set_audio_gate_enabled` (line 208)
- `get_current_audio_level` (line 213)
- `set_continuous_voice_mode` (line 219)
- `is_continuous_voice_mode` (line 228)
- `cleanup_on_exit` (line 234)
- `get_audio_folder_path` (line 241)
- `list_audio_files` (line 247)
- `cleanup_old_audio_files` (line 253)
- `cleanup_all_audio_files` (line 258)
- `get_process_info` (line 263)
- `test_connection` (line 269)
- `_update_cached_state` (line 275)
- `_update_cached_state_from_signal` (line 281)
- `is_recording` (line 286)
- `is_processing_voice` (line 293)
- `is_playing_tts` (line 300)
- `recording_service` (line 307)

---

### `services\conversation_service.py.ConversationService`

- **File:** `services\conversation_service.py`
- **Line:** 14
- **Bases:** QObject
- **Docstring:** Service for managing conversation state and persistence...

**Methods:**
- `__init__` (line 19)
- `set_memory_service` (line 28)
- `add_message` (line 32)
- `_add_to_memory` (line 48)
- `get_messages` (line 84)
- `get_context_messages` (line 90)
- `save_conversation` (line 97)
- `load_conversation` (line 126)
- `clear_conversation` (line 146)
- `auto_save` (line 153)

---

### `services\enhancement_service.py.EnhancementService`

- **File:** `services\enhancement_service.py`
- **Line:** 8
- **Docstring:** Service for response enhancement and follow-up detection...

**Methods:**
- `__init__` (line 11)
- `should_enhance_response` (line 14)
- `detect_follow_up_question` (line 25)
- `generate_enhanced_response` (line 34)

---

### `services\memory_service.py.LongTermMemoryEntry`

- **File:** `services\memory_service.py`
- **Line:** 34
- **Decorators:** dataclass
- **Docstring:** Represents a long-term memory entry...

**Methods:**
- `__post_init__` (line 47)

---

### `services\memory_service.py.LongTermMemoryService`

- **File:** `services\memory_service.py`
- **Line:** 377
- **Docstring:** Manages long-term memory storage and retrieval...

**Methods:**
- `__init__` (line 380)
- `_load` (line 385)
- `add_entry` (line 400)
- `get_entries` (line 410)
- `_save` (line 420)
- `update_access_stats` (line 430)

---

### `services\memory_service.py.MemoryClassifier`

- **File:** `services\memory_service.py`
- **Line:** 54
- **Docstring:** Intelligent classifier for determining memory type and importance...

**Methods:**
- `classify_message` (line 92)

---

### `services\memory_service.py.MemoryEntry`

- **File:** `services\memory_service.py`
- **Line:** 20
- **Decorators:** dataclass
- **Docstring:** Represents a single memory entry...

---

### `services\memory_service.py.MemoryRetriever`

- **File:** `services\memory_service.py`
- **Line:** 250
- **Docstring:** Retrieves relevant memories based on query similarity...

**Methods:**
- `calculate_relevance` (line 254)
- `get_relevant_memories` (line 304)

---

### `services\memory_service.py.MemoryService`

- **File:** `services\memory_service.py`
- **Line:** 439
- **Bases:** QObject
- **Docstring:** Service for managing LLM memory across conversations...

**Methods:**
- `__init__` (line 445)
- `_load_memory` (line 470)
- `_save_memory` (line 478)
- `_on_embeddings_updated` (line 486)
- `add_memory` (line 494)
- `add_summary` (line 525)
- `get_relevant_memories` (line 543)
- `intelligent_add_message` (line 595)
- `extract_facts_from_message` (line 641)
- `get_user_info` (line 670)
- `get_user_name` (line 685)
- `get_context_messages` (line 694)
- `summarize_conversation` (line 721)
- `clear_memory` (line 738)
- `_verify_memory_files_cleared` (line 763)
- `delete_memory` (line 782)
- `get_memory_stats` (line 793)
- `add_message` (line 847)
- `add_fact` (line 854)
- `set_max_context_messages` (line 871)
- `search_memories` (line 880)
- `clear` (line 909)
- `cleanup_memory_entries` (line 916)

---

### `services\memory_service.py.PronounNormalizer`

- **File:** `services\memory_service.py`
- **Line:** 161
- **Docstring:** Normalizes pronouns in user messages to avoid AI confusion...

**Methods:**
- `normalize_pronouns` (line 191)
- `should_normalize` (line 226)

---

### `services\memory_service.py.ShortTermMemoryService`

- **File:** `services\memory_service.py`
- **Line:** 323
- **Docstring:** Manages short-term memory (recent conversation context)...

**Methods:**
- `__init__` (line 326)
- `_load` (line 332)
- `add_message` (line 345)
- `get_messages` (line 355)
- `clear` (line 359)
- `_save` (line 367)

---

### `services\ollama_service.py.OllamaService`

- **File:** `services\ollama_service.py`
- **Line:** 20
- **Bases:** QObject
- **Docstring:** Service for handling all Ollama API communication...

**Methods:**
- `__init__` (line 30)
- `get_models` (line 41)
- `test_connection` (line 90)
- `send_chat_message` (line 102)
- `pull_model` (line 219)
- `_pull_model_thread` (line 231)
- `remove_model` (line 267)
- `_remove_model_thread` (line 279)
- `update_model` (line 315)
- `_update_model_thread` (line 327)
- `_extract_system_prompt` (line 363)
- `_build_session_commands` (line 372)
- `cancel_request` (line 388)
- `reset_cancellation` (line 396)
- `is_connected` (line 404)

---

### `services\semantic_search_service.py.SemanticSearchService`

- **File:** `services\semantic_search_service.py`
- **Line:** 32
- **Bases:** QObject
- **Docstring:** Service for semantic memory retrieval using vector embeddings...

**Methods:**
- `__init__` (line 38)
- `_init_model` (line 56)
- `_load_embeddings` (line 70)
- `_save_embeddings` (line 104)
- `add_memory` (line 138)
- `remove_memory` (line 192)
- `search_semantic` (line 221)
- `search_hybrid` (line 274)
- `update_memory_importance` (line 353)
- `get_memory_stats` (line 380)
- `clear_all` (line 427)
- `is_ready` (line 454)

---

### `services\semantic_search_service.py.VectorizedMemory`

- **File:** `services\semantic_search_service.py`
- **Line:** 21
- **Decorators:** dataclass
- **Docstring:** Represents a memory entry with its vector embedding...

---

### `services\start_up\dependency_checker.py.DependencyChecker`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 16
- **Docstring:** Handles dependency checking and installation....

**Methods:**
- `__init__` (line 19)
- `test_import` (line 25)
- `check_core_dependencies` (line 41)
- `check_ml_dependencies` (line 82)
- `check_tts_options` (line 101)
- `check_package_versions` (line 117)
- `run_comprehensive_check` (line 154)
- `get_missing_dependencies` (line 165)
- `get_version_conflicts` (line 169)
- `run_install_dependencies` (line 173)
- `get_dependency_summary` (line 198)

---

### `services\start_up\install_dependencies.py.DependencyInstaller`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 23
- **Docstring:** Handles staged installation of dependencies with error recovery....

**Methods:**
- `__init__` (line 26)
- `print_header` (line 187)
- `check_python_version` (line 194)
- `check_virtual_environment` (line 203)
- `upgrade_pip` (line 213)
- `setup_spellchecker` (line 229)
- `run_stage` (line 275)
- `verify_installation` (line 396)
- `print_summary` (line 475)
- `install_all` (line 553)

---

### `services\summarization_service.py.SummarizationService`

- **File:** `services\summarization_service.py`
- **Line:** 15
- **Bases:** QObject
- **Docstring:** Service for generating AI-powered conversation summaries and names...

**Methods:**
- `__init__` (line 22)
- `generate_chat_name` (line 28)
- `_create_summarization_prompt` (line 117)
- `_clean_generated_name` (line 142)
- `_has_enough_substance` (line 215)
- `_ai_evaluate_conversation_quality` (line 232)
- `_fallback_quality_check` (line 308)
- `_ai_evaluate_name_quality` (line 337)
- `set_summarization_model` (line 409)
- `set_min_messages_threshold` (line 413)

---

### `services\worker\worker.py.Worker`

- **File:** `services\worker\worker.py`
- **Line:** 10
- **Bases:** QObject

**Methods:**
- `__init__` (line 16)
- `_log_thread_info` (line 28)
- `run` (line 35)
- `stop` (line 66)
- `is_running` (line 88)
- `run_stream` (line 94)
- `get_stats` (line 197)

---

### `ui\Audio_visualisers\eq_orchestrator.py.MainWindow`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 148
- **Bases:** QMainWindow

**Methods:**
- `__init__` (line 152)
- `switch_mode` (line 305)
- `select_audio_file` (line 363)
- `load_audio_preset` (line 371)
- `play_audio` (line 388)
- `stop_audio` (line 399)
- `toggle_mute` (line 414)
- `toggle_system_audio` (line 418)
- `on_device_selected` (line 434)
- `_play_audio_thread` (line 445)
- `_play_microphone_audio` (line 451)
- `_play_file_audio` (line 486)
- `_process_audio_chunk` (line 516)
- `_reset_visualizers` (line 582)
- `populate_device_list` (line 598)
- `refresh_device_list` (line 607)
- `auto_select_microphone` (line 615)
- `resizeEvent` (line 620)

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.BarEQWidget`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 5
- **Bases:** QWidget
- **Docstring:** A bar equalizer widget that displays audio frequency data as animated bars.

This widget renders a s...

**Methods:**
- `__init__` (line 25)
- `_setup_animation_timer` (line 49)
- `_animate` (line 55)
- `set_eq_bars` (line 68)
- `set_idle` (line 104)
- `start_animation` (line 109)
- `stop_animation` (line 113)
- `get_current_values` (line 117)
- `_calculate_bar_geometry` (line 131)
- `_create_bar_gradient` (line 154)
- `_draw_bar` (line 208)
- `paintEvent` (line 237)

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.CircleEQWidget`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 6
- **Bases:** QWidget
- **Docstring:** A simplified circular equalizer widget that displays audio frequency data in circular sections.

Thi...

**Methods:**
- `__init__` (line 24)
- `_setup_animation_timer` (line 48)
- `_animate` (line 54)
- `set_eq_sections` (line 68)
- `set_idle` (line 104)
- `start_animation` (line 109)
- `stop_animation` (line 113)
- `get_current_values` (line 117)
- `_create_section_gradient` (line 131)
- `paintEvent` (line 171)

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.CircularGradientEQWidget`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 7
- **Bases:** QWidget
- **Docstring:** Like CircularNetEQWidget, but fills the area defined by the animated points with a soft, faded gradi...

**Methods:**
- `__init__` (line 17)
- `_smooth_radii` (line 41)
- `_animate` (line 49)
- `set_net_radii` (line 58)
- `set_idle` (line 77)
- `start_animation` (line 83)
- `stop_animation` (line 86)
- `paintEvent` (line 89)

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.CircularNetEQWidget`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`
- **Line:** 7
- **Bases:** QWidget
- **Docstring:** A Vanta.js-inspired circular net visualizer: points around a circle, connected by glowing lines, wit...

**Methods:**
- `__init__` (line 20)
- `_animate` (line 41)
- `set_net_radii` (line 51)
- `set_idle` (line 70)
- `start_animation` (line 74)
- `stop_animation` (line 77)
- `paintEvent` (line 80)

---

### `ui\Audio_visualisers\voice_ring_animation.py.BarEQWidget`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 325
- **Bases:** QWidget
- **Docstring:** A bar equalizer widget that displays audio frequency data as animated bars.

This widget renders a s...

**Methods:**
- `__init__` (line 345)
- `_setup_animation_timer` (line 369)
- `_animate` (line 375)
- `set_eq_bars` (line 388)
- `set_idle` (line 424)
- `start_animation` (line 429)
- `stop_animation` (line 433)
- `get_current_values` (line 437)
- `_calculate_bar_geometry` (line 451)
- `_create_bar_gradient` (line 474)
- `_draw_bar` (line 528)
- `paintEvent` (line 557)

---

### `ui\Audio_visualisers\voice_ring_animation.py.CircleEQWidget`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 117
- **Bases:** QWidget
- **Docstring:** A simplified circular equalizer widget that displays audio frequency data in circular sections.

Thi...

**Methods:**
- `__init__` (line 135)
- `_setup_animation_timer` (line 159)
- `_animate` (line 165)
- `set_eq_sections` (line 179)
- `set_idle` (line 215)
- `start_animation` (line 220)
- `stop_animation` (line 224)
- `get_current_values` (line 228)
- `_create_section_gradient` (line 242)
- `paintEvent` (line 282)

---

### `ui\Audio_visualisers\voice_ring_animation.py.CircularGradientEQWidget`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 710
- **Bases:** QWidget
- **Docstring:** Like CircularNetEQWidget, but fills the area defined by the animated points with a soft, faded gradi...

**Methods:**
- `__init__` (line 720)
- `_smooth_radii` (line 744)
- `_animate` (line 752)
- `set_net_radii` (line 761)
- `set_idle` (line 780)
- `start_animation` (line 786)
- `stop_animation` (line 788)
- `paintEvent` (line 791)

---

### `ui\Audio_visualisers\voice_ring_animation.py.CircularNetEQWidget`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 587
- **Bases:** QWidget
- **Docstring:** A Vanta.js-inspired circular net visualizer: points around a circle, connected by glowing lines, wit...

**Methods:**
- `__init__` (line 600)
- `_animate` (line 621)
- `set_net_radii` (line 631)
- `set_idle` (line 650)
- `start_animation` (line 654)
- `stop_animation` (line 656)
- `paintEvent` (line 659)

---

### `ui\Audio_visualisers\voice_ring_animation.py.MainWindow`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 846
- **Bases:** QMainWindow

**Methods:**
- `__init__` (line 850)
- `switch_mode` (line 992)
- `select_audio_file` (line 1093)
- `load_audio_preset` (line 1101)
- `play_audio` (line 1124)
- `stop_audio` (line 1135)
- `toggle_mute` (line 1162)
- `toggle_system_audio` (line 1166)
- `on_device_selected` (line 1183)
- `_play_audio_thread` (line 1195)
- `populate_device_list` (line 1574)
- `refresh_device_list` (line 1585)
- `auto_select_microphone` (line 1595)
- `resizeEvent` (line 1600)

---

### `ui\Widgets\chat_navigation.py.ChatNavigationWidget`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 20
- **Bases:** QWidget
- **Docstring:** Widget for navigating between previous conversations...

**Methods:**
- `__init__` (line 29)
- `setup_ui` (line 40)
- `setup_connections` (line 154)
- `refresh_conversations` (line 166)
- `create_conversation_item` (line 196)
- `on_conversation_double_clicked` (line 217)
- `show_context_menu` (line 223)
- `rename_conversation` (line 260)
- `delete_conversation` (line 297)
- `set_current_conversation` (line 324)
- `get_selected_conversation` (line 329)
- `clear_all_conversations` (line 336)
- `trigger_name_generation` (line 359)
- `on_summarization_completed` (line 391)
- `on_summarization_failed` (line 417)

---

### `ui\Widgets\coqui_model_dialog.py.CoquiModelDialog`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 48
- **Bases:** QDialog
- **Docstring:** Dialog for selecting Coqui TTS models and speakers...

**Methods:**
- `__init__` (line 54)
- `setup_ui` (line 70)
- `create_model_panel` (line 199)
- `create_speaker_panel` (line 228)
- `load_models` (line 251)
- `on_model_selected` (line 280)
- `load_speakers_for_model` (line 301)
- `on_speaker_selected` (line 334)
- `download_selected_model` (line 340)
- `start_download` (line 356)
- `on_download_completed` (line 368)
- `update_selection_button` (line 383)
- `accept_selection` (line 390)
- `log_status` (line 398)
- `get_current_time` (line 406)

---

### `ui\Widgets\coqui_model_dialog.py.ModelDownloadThread`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 21
- **Bases:** QThread
- **Docstring:** Thread for downloading Coqui TTS models...

**Methods:**
- `__init__` (line 26)
- `run` (line 30)

---

### `ui\Widgets\editable_message_widget.py.EditableMessageWidget`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 14
- **Bases:** QWidget
- **Docstring:** Widget for displaying and editing user messages...

**Methods:**
- `__init__` (line 21)
- `setup_ui` (line 31)
- `setup_styles` (line 93)
- `start_editing` (line 172)
- `save_edit` (line 181)
- `cancel_edit` (line 191)
- `finish_editing` (line 196)
- `get_content` (line 202)
- `set_content` (line 206)

---

### `ui\Widgets\personality_widget.py.PersonalityWidget`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 14
- **Bases:** QWidget
- **Docstring:** Widget for managing AI personalities...

**Methods:**
- `__init__` (line 19)
- `setup_ui` (line 25)
- `setup_selection_tab` (line 55)
- `setup_creation_tab` (line 91)
- `setup_management_tab` (line 281)
- `load_personalities` (line 319)
- `on_personality_changed` (line 357)
- `set_personality` (line 370)
- `update_personality_info` (line 380)
- `create_personality` (line 447)
- `clear_creation_form` (line 514)
- `on_custom_personality_selected` (line 545)
- `delete_custom_personality` (line 552)
- `export_personality` (line 572)
- `get_current_personality` (line 581)
- `get_formatted_prompt` (line 587)
- `get_system_prompt` (line 591)
- `get_available_personalities` (line 595)
- `get_comprehensive_system_prompt` (line 599)
- `get_user_context_messages` (line 604)
- `refresh_personalities` (line 608)
- `on_personality_changed` (line 622)

---

### `ui\Widgets\settings_dialog.py.SettingsDialog`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 11
- **Bases:** QDialog
- **Docstring:** Dialog for configuring application settings...

**Methods:**
- `__init__` (line 14)
- `setup_ui` (line 25)
- `create_general_tab` (line 69)
- `create_chat_tab` (line 133)
- `create_session_tab` (line 180)
- `create_developer_tab` (line 220)
- `_delayed_load_settings` (line 238)
- `load_current_settings` (line 243)
- `save_settings` (line 302)
- `reset_to_defaults` (line 352)

---

### `ui\Widgets\spellchecker_widget.py.SpellCheckerTextEdit`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 23
- **Bases:** QTextEdit
- **Docstring:** Custom QTextEdit with spell checking functionality...

**Methods:**
- `__init__` (line 26)
- `setup_spellchecker` (line 36)
- `setup_context_menu` (line 53)
- `show_context_menu` (line 58)
- `replace_word` (line 102)
- `add_to_dictionary` (line 112)
- `ignore_word` (line 123)
- `highlight_misspelled_words` (line 127)
- `keyPressEvent` (line 172)
- `on_text_changed` (line 182)
- `enable_spellcheck` (line 189)
- `disable_spellcheck` (line 196)
- `cleanup` (line 208)

---

### `ui\Widgets\voice_settings_dialog.py.InternetCheckThread`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 25
- **Bases:** QThread
- **Docstring:** Thread for checking internet connectivity...

**Methods:**
- `run` (line 29)

---

### `ui\Widgets\voice_settings_dialog.py.VoiceSettingsDialog`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 38
- **Bases:** QDialog
- **Docstring:** Dialog for configuring voice settings...

**Methods:**
- `__init__` (line 44)
- `setup_ui` (line 126)
- `create_stt_tab` (line 260)
- `create_tts_tab` (line 300)
- `create_general_tab` (line 398)
- `setup_connections` (line 569)
- `check_internet_connection` (line 581)
- `on_internet_check_completed` (line 590)
- `update_api_availability` (line 604)
- `on_stt_api_changed` (line 626)
- `on_tts_api_changed` (line 638)
- `on_voice_changed` (line 670)
- `on_eq_visualizer_changed` (line 674)
- `load_coqui_models` (line 680)
- `on_coqui_model_changed` (line 707)
- `load_coqui_speakers` (line 737)
- `on_coqui_speaker_changed` (line 760)
- `download_selected_model` (line 765)
- `start_coqui_download` (line 783)
- `on_coqui_download_completed` (line 803)
- `on_silence_threshold_changed` (line 817)
- `test_settings` (line 835)
- `save_settings` (line 889)
- `get_settings` (line 922)
- `set_settings` (line 926)
- `on_tts_settings_changed` (line 997)

---

### `ui\styles\message_formatter.py.MessageFormatter`

- **File:** `ui\styles\message_formatter.py`
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

### `ui\styles\tab_styles.py.TabStyles`

- **File:** `ui\styles\tab_styles.py`
- **Line:** 9
- **Docstring:** Centralized tab styling for the application...

**Methods:**
- `get_tab_style` (line 40)

---

### `ui\tabs\chat_tab\chat_display.py.ChatDisplay`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 16
- **Bases:** QObject
- **Docstring:** Chat Display component for message display and editing...

**Methods:**
- `__init__` (line 22)
- `setup_ui_components` (line 36)
- `setup_streaming_handler` (line 64)
- `get_ai_name` (line 71)
- `chat_display_mouse_move_event` (line 75)
- `show_edit_button` (line 101)
- `hide_edit_button` (line 135)
- `edit_message_at_index` (line 143)
- `show_message_edit_dialog` (line 154)
- `save_message_edit` (line 244)
- `on_message_edited` (line 260)
- `append_to_chat` (line 265)
- `append_response_chunk` (line 280)
- `start_streaming` (line 298)
- `stop_streaming` (line 306)
- `clear_chat` (line 312)
- `get_ui_components` (line 319)
- `get_streaming_handler` (line 326)

---

### `ui\tabs\chat_tab\chat_tab.py.ChatTab`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 31
- **Bases:** QWidget
- **Docstring:** Main chat interface tab that orchestrates all components...

**Methods:**
- `__init__` (line 45)
- `setup_components` (line 71)
- `setup_ui` (line 91)
- `setup_connections` (line 254)
- `on_message_sent` (line 295)
- `on_message_cancelled` (line 303)
- `on_input_mode_changed` (line 308)
- `on_temperature_changed` (line 357)
- `on_personality_changed` (line 362)
- `on_model_changed` (line 367)
- `on_eq_mode_changed` (line 372)
- `on_voice_input_received` (line 380)
- `on_voice_input_error` (line 396)
- `on_tts_started` (line 401)
- `on_tts_finished` (line 411)
- `on_tts_error` (line 437)
- `on_recording_started` (line 441)
- `on_recording_stopped` (line 445)
- `on_recording_error` (line 449)
- `on_voice_processing_started` (line 453)
- `on_voice_processing_finished` (line 457)
- `on_audio_level_changed` (line 461)
- `on_message_edited` (line 473)
- `get_ai_name` (line 479)
- `get_current_personality` (line 486)
- `get_current_model` (line 490)
- `get_temperature` (line 494)
- `get_current_response` (line 498)
- `append_to_chat` (line 502)
- `append_response_chunk` (line 511)
- `_append_response_chunk_safe` (line 517)
- `start_streaming` (line 535)
- `_start_streaming_safe` (line 541)
- `stop_streaming` (line 570)
- `_stop_streaming_safe` (line 576)
- `force_enable_send_button` (line 608)
- `_force_enable_send_button_safe` (line 614)
- `clear_chat` (line 636)
- `update_model_list` (line 640)
- `update_personality_list` (line 644)
- `speak_ai_response` (line 648)
- `open_voice_settings` (line 652)
- `on_voice_settings_changed` (line 670)
- `load_conversation` (line 680)
- `refresh_navigation` (line 727)
- `set_current_conversation_file` (line 732)
- `get_streaming_handler` (line 737)
- `streaming_handler` (line 742)

---

### `ui\tabs\chat_tab\eq_visualizer.py.EQVisualizer`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 20
- **Bases:** QObject
- **Docstring:** EQ Visualizer component for audio visualization...

**Methods:**
- `__init__` (line 26)
- `setup_eq_visualizers` (line 38)
- `switch_to_eq_visualizer` (line 52)
- `switch_to_chat_display` (line 148)
- `update_eq_visualizer` (line 243)
- `_update_eq_widget_safe` (line 354)
- `is_eq_visualizer_active` (line 367)
- `update_eq_visualizer_mode` (line 373)
- `get_eq_mode` (line 381)
- `get_available_eq_modes` (line 385)

---

### `ui\tabs\chat_tab\input_controls.py.InputControls`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 17
- **Bases:** QObject
- **Docstring:** Input Controls component for message input and settings...

**Methods:**
- `__init__` (line 28)
- `setup_ui_components` (line 43)
- `setup_connections` (line 215)
- `set_input_mode` (line 233)
- `on_temperature_changed` (line 252)
- `on_personality_combo_changed` (line 259)
- `on_model_changed` (line 265)
- `send_message` (line 270)
- `cancel_message` (line 285)
- `start_streaming` (line 290)
- `stop_streaming` (line 313)
- `force_enable_send_button` (line 339)
- `update_model_list` (line 359)
- `update_personality_list` (line 370)
- `get_current_model` (line 381)
- `get_temperature` (line 385)
- `get_current_response` (line 389)
- `get_current_personality` (line 393)
- `get_ui_components` (line 397)
- `eventFilter` (line 411)

---

### `ui\tabs\chat_tab\voice_controls.py.VoiceControls`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 15
- **Bases:** QObject
- **Docstring:** Voice Controls component for voice mode, TTS, and audio level handling...

**Methods:**
- `__init__` (line 32)
- `setup_ui_components` (line 112)
- `_update_voice_state` (line 196)
- `is_voice_busy` (line 201)
- `_handle_voice_crash` (line 206)
- `_attempt_recovery` (line 219)
- `_stop_all_voice_operations` (line 229)
- `_reset_voice_ui` (line 240)
- `_reinitialize_voice_service` (line 251)
- `_disable_voice_features` (line 259)
- `_reset_error_count` (line 268)
- `_handle_service_error` (line 272)
- `setup_connections` (line 284)
- `toggle_voice_mode` (line 314)
- `_start_continuous_voice_mode` (line 366)
- `_handle_voice_input_safe` (line 383)
- `_handle_tts_finished_continuous` (line 400)
- `_restart_voice_input` (line 410)
- `_reset_voice_button` (line 424)
- `on_voice_input_received` (line 446)
- `on_voice_input_error` (line 454)
- `_handle_voice_input_error_safe` (line 464)
- `on_tts_started` (line 479)
- `on_tts_finished` (line 484)
- `on_tts_error` (line 495)
- `_handle_tts_error_safe` (line 505)
- `on_recording_started` (line 509)
- `_handle_recording_started_safe` (line 516)
- `on_recording_stopped` (line 537)
- `_handle_recording_stopped_safe` (line 544)
- `on_recording_error` (line 558)
- `_handle_recording_error_safe` (line 565)
- `on_voice_processing_started` (line 580)
- `on_voice_processing_finished` (line 587)
- `on_audio_level_changed` (line 593)
- `_update_audio_level_ui_safe` (line 603)
- `speak_ai_response` (line 662)
- `update_voice_settings` (line 673)
- `get_voice_settings` (line 682)
- `is_voice_mode_active` (line 686)
- `is_tts_playing` (line 690)
- `get_ui_components` (line 700)

---

### `ui\tabs\memory_tab.py.MemoryTab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 20
- **Bases:** QWidget
- **Docstring:** Memory management tab for LLM memory settings and overview...

**Methods:**
- `__init__` (line 23)
- `setup_ui` (line 30)
- `create_settings_tab` (line 56)
- `create_overview_tab` (line 116)
- `create_memories_tab` (line 176)
- `create_summaries_tab` (line 241)
- `setup_connections` (line 271)
- `update_context_messages` (line 295)
- `refresh_data` (line 300)
- `refresh_overview` (line 306)
- `refresh_memories` (line 362)
- `refresh_summaries` (line 393)
- `search_memories` (line 406)
- `show_memory_details` (line 428)
- `show_summary_details` (line 462)
- `summarize_current_conversation` (line 478)
- `set_conversation_service` (line 484)
- `_summarize_with_service` (line 491)
- `clear_all_memories` (line 512)
- `cleanup_memory_entries` (line 525)
- `delete_selected_memory` (line 541)

---

### `ui\tabs\model_tab.py.ModelTab`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 15
- **Bases:** QWidget
- **Docstring:** Model management tab...

**Methods:**
- `__init__` (line 23)
- `setup_ui` (line 46)
- `setup_model_list` (line 63)
- `setup_operations` (line 139)
- `setup_connections` (line 359)
- `refresh_models` (line 369)
- `update_model_list` (line 377)
- `pull_model` (line 387)
- `remove_selected_model` (line 405)
- `update_selected_model` (line 425)
- `on_model_selection_changed` (line 445)
- `start_operation` (line 452)
- `stop_operation` (line 461)
- `append_status` (line 469)
- `get_current_time` (line 478)
- `on_operation_progress` (line 483)
- `on_operation_finished` (line 487)
- `on_operation_error` (line 495)
- `get_selected_model` (line 501)
- `clear_status` (line 506)

---

### `ui\tabs\personality_tab.py.PersonalityTab`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 17
- **Bases:** QWidget
- **Docstring:** Personality management tab...

**Methods:**
- `__init__` (line 23)
- `setup_ui` (line 30)
- `setup_selection_tab` (line 90)
- `setup_creation_tab` (line 197)
- `setup_management_tab` (line 380)
- `load_personalities` (line 553)
- `update_system_personalities_list` (line 589)
- `update_custom_personalities_list` (line 600)
- `on_system_personality_selected` (line 611)
- `update_system_personality_info` (line 617)
- `on_custom_personality_selected` (line 638)
- `on_personality_changed` (line 644)
- `update_personality_info` (line 650)
- `create_personality` (line 673)
- `clear_creation_form` (line 730)
- `delete_custom_personality` (line 738)
- `export_personality` (line 771)
- `refresh_personalities` (line 792)
- `get_current_personality` (line 801)
- `get_system_prompt` (line 805)
- `get_available_personalities` (line 816)

---

### `utils\Logging\Custom_Logger.py.CustomLogger`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 64
- **Bases:** logging.Logger
- **Docstring:** Custom Logging class for the PyChat project.

This class provides enhanced logging functionality wit...

**Methods:**
- `_check_config_for_logging` (line 83)
- `__new__` (line 95)
- `set_logging_enabled` (line 102)
- `_clear_log_file` (line 106)
- `get_logger` (line 113)
- `info` (line 157)
- `debug` (line 162)
- `warning` (line 167)
- `error` (line 172)
- `_filter_non_ascii` (line 177)

---

### `utils\Logging\Custom_Logger.py.DummyLogger`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 117

**Methods:**
- `info` (line 118)
- `debug` (line 119)
- `warning` (line 120)
- `error` (line 121)
- `critical` (line 122)

---

### `utils\Logging\Custom_Logger.py.PrintLogger`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 151
- **Bases:** PrintOnLogMixin

---

### `utils\Logging\Custom_Logger.py.PrintOnLogMixin`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 35

**Methods:**
- `_print` (line 36)
- `info` (line 38)
- `debug` (line 43)
- `warning` (line 48)
- `error` (line 53)
- `critical` (line 58)

---

### `utils\Logging\logging_helpers.py.LoggingHelpers`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 19
- **Docstring:** Centralized logging helper methods for consistent logging across the application...

**Methods:**
- `log_exception_with_context` (line 23)
- `log_warning_with_context` (line 30)
- `log_info_with_context` (line 36)
- `log_debug` (line 42)
- `log_error` (line 47)
- `log_network_request` (line 52)
- `log_file_operation` (line 62)
- `log_audio_operation` (line 70)
- `log_memory_operation` (line 78)
- `log_ui_operation` (line 86)
- `log_performance_metric` (line 94)
- `log_json_parsing_error` (line 100)
- `log_json_parsing_success` (line 106)
- `log_critical_error` (line 111)
- `log_fact_extraction_start` (line 118)
- `log_fact_extraction_end` (line 123)
- `log_fact_extraction_result` (line 128)
- `log_fact_processing` (line 133)
- `log_fact_storage_start` (line 138)
- `log_fact_storage_end` (line 143)
- `log_fact_storage_summary` (line 148)
- `log_fact_skipped` (line 153)
- `log_memory_result` (line 158)
- `log_memory_ltm_status` (line 163)
- `log_llm_call` (line 168)
- `log_llm_response` (line 173)
- `log_json_extraction` (line 178)
- `log_message_sent` (line 183)
- `log_message_sent_end` (line 188)
- `log_conversation_detection` (line 193)
- `log_service_initialization` (line 198)

---

### `utils\Logging\logging_helpers.py.ThreadMonitor`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 207
- **Bases:** QObject
- **Docstring:** Monitor for tracking QThread lifecycle and debugging thread issues...

**Methods:**
- `__init__` (line 214)
- `register_thread` (line 222)
- `unregister_thread` (line 252)
- `_on_thread_started` (line 272)
- `_on_thread_finished` (line 284)
- `get_thread_info` (line 298)
- `get_all_threads` (line 302)
- `get_thread_history` (line 306)
- `get_thread_stats` (line 310)
- `cleanup` (line 350)

---

### `utils\Logging\logging_helpers.py.ThreadSafeLogger`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 370
- **Docstring:** Thread-safe logging utilities...

**Methods:**
- `log_thread_context` (line 374)
- `log_thread_safety_check` (line 392)
- `log_thread_operation` (line 407)

---

### `utils\complexity_analyzer.py.ComplexityLevel`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 9
- **Bases:** Enum
- **Docstring:** Enumeration for complexity levels...

---

### `utils\complexity_analyzer.py.ComplexityMetrics`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 17
- **Decorators:** dataclass
- **Docstring:** Data class to hold complexity analysis results...

---

### `utils\complexity_analyzer.py.RequestComplexityAnalyzer`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 31
- **Docstring:** Analyzes the complexity of requests to help choose appropriate models...

**Methods:**
- `__init__` (line 34)
- `analyze_complexity` (line 114)
- `_estimate_tokens` (line 180)
- `_analyze_reasoning_depth` (line 186)
- `_analyze_knowledge_breadth` (line 222)
- `_analyze_ambiguity` (line 247)
- `_count_constraints` (line 266)
- `_analyze_context_dependency` (line 281)
- `_analyze_output_complexity` (line 301)
- `_determine_complexity_level` (line 321)
- `_generate_recommendations` (line 332)
- `get_model_recommendation` (line 374)
- `format_complexity_report` (line 395)

---

### `utils\complexity_widget.py.ComplexityWidget`

- **File:** `utils\complexity_widget.py`
- **Line:** 8
- **Bases:** QWidget
- **Docstring:** Widget to display request complexity analysis...

**Methods:**
- `__init__` (line 13)
- `setup_ui` (line 19)
- `analyze_request` (line 112)
- `_update_display` (line 132)
- `_update_model_recommendation` (line 184)
- `_on_switch_model` (line 190)
- `_set_widget_color` (line 195)
- `_set_progress_bar_color` (line 201)
- `_get_color_for_value` (line 217)
- `clear_analysis` (line 231)
- `get_current_metrics` (line 239)

---

### `utils\error_handler.py.ErrorHandler`

- **File:** `utils\error_handler.py`
- **Line:** 20
- **Docstring:** Centralized error handling utilities...

**Methods:**
- `safe_execute` (line 24)
- `retry_on_failure` (line 49)
- `handle_network_errors` (line 91)
- `handle_file_operations` (line 125)
- `handle_audio_operations` (line 159)
- `handle_memory_operations` (line 182)
- `handle_ui_operations` (line 205)

---

### `utils\internet_connection.py.InternetConnectionTester`

- **File:** `utils\internet_connection.py`
- **Line:** 15
- **Docstring:** A utility class for testing internet connectivity.

Tests multiple reliable endpoints to determine i...

**Methods:**
- `__init__` (line 22)
- `test_socket_connection` (line 41)
- `test_http_connection` (line 58)
- `test_connection` (line 75)
- `test_connection_with_details` (line 94)

---

### `utils\prompts.py.PromptFormatter`

- **File:** `utils\prompts.py`
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

### `utils\prompts.py.PromptTemplates`

- **File:** `utils\prompts.py`
- **Line:** 11
- **Docstring:** Centralized prompt templates for the application...

---

### `utils\streaming_handler.py.StreamingHandler`

- **File:** `utils\streaming_handler.py`
- **Line:** 17
- **Bases:** QObject
- **Docstring:** Handles streaming response processing and display updates...

**Methods:**
- `__init__` (line 23)
- `_get_next_message_id` (line 36)
- `_flush_stream_buffer` (line 41)
- `append_message` (line 60)
- `start_streaming_message` (line 76)
- `edit_message` (line 90)
- `get_message_by_id` (line 103)
- `get_editable_messages` (line 110)
- `get_messages` (line 123)
- `_render_chat_display` (line 127)
- `_render_chat_display_safe` (line 133)
- `_safe_ui_update` (line 279)
- `update_streaming_message` (line 298)
- `finalize_streaming_message` (line 320)
- `update_last_system_switch` (line 349)
- `remove_streaming_placeholder` (line 366)
- `cleanup` (line 384)
- `clear_chat` (line 396)
- `update_ai_name` (line 408)

---

## ⚙️ Functions

### `MainApp\app_lifecycle.py.__init__`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 17
- **Arguments:** self, main_window, service_manager, ui_manager, event_handler

---

### `MainApp\app_lifecycle.py.check_ollama_connection`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 158
- **Arguments:** self
- **Docstring:** Check if Ollama is running and accessible...

---

### `MainApp\app_lifecycle.py.get_ollama_error_shown`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 171
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Get the Ollama error shown flag...

---

### `MainApp\app_lifecycle.py.handle_close_event`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 70
- **Arguments:** self, event
- **Docstring:** Handle application close event...

---

### `MainApp\app_lifecycle.py.handle_show_event`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 49
- **Arguments:** self
- **Docstring:** Handle application show event...

---

### `MainApp\app_lifecycle.py.initialize_application`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 27
- **Arguments:** self
- **Docstring:** Initialize the application...

---

### `MainApp\app_lifecycle.py.is_initialization_complete`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 163
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if initialization is complete...

---

### `MainApp\app_lifecycle.py.set_ollama_error_shown`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 167
- **Arguments:** self, shown
- **Docstring:** Set the Ollama error shown flag...

---

### `MainApp\app_lifecycle.py.show_initialization_error`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 108
- **Arguments:** self, error_message
- **Docstring:** Show initialization error dialog...

---

### `MainApp\app_lifecycle.py.show_ollama_connection_error`

- **File:** `MainApp\app_lifecycle.py`
- **Line:** 119
- **Arguments:** self, context, force_show
- **Docstring:** Show a user-friendly error dialog when Ollama is not running...

---

### `MainApp\event_handler.py.__init__`

- **File:** `MainApp\event_handler.py`
- **Line:** 15
- **Arguments:** self, main_window, service_manager, ui_manager, chat_controller

---

### `MainApp\event_handler.py._check_ollama_connection`

- **File:** `MainApp\event_handler.py`
- **Line:** 870
- **Arguments:** self
- **Docstring:** Check if Ollama is running and accessible...

---

### `MainApp\event_handler.py._cleanup_worker_thread`

- **File:** `MainApp\event_handler.py`
- **Line:** 473
- **Arguments:** self
- **Docstring:** Clean up worker thread safely in the main thread...

---

### `MainApp\event_handler.py._cleanup_worker_thread_once`

- **File:** `MainApp\event_handler.py`
- **Line:** 485
- **Arguments:** self
- **Docstring:** Clean up worker thread once without recursion...

---

### `MainApp\event_handler.py._connect_menu_actions`

- **File:** `MainApp\event_handler.py`
- **Line:** 91
- **Arguments:** self
- **Docstring:** Connect menu actions to their handlers...

---

### `MainApp\event_handler.py._create_chat_controller`

- **File:** `MainApp\event_handler.py`
- **Line:** 793
- **Arguments:** self
- **Docstring:** Create a new chat controller with current services...

---

### `MainApp\event_handler.py._create_worker_thread`

- **File:** `MainApp\event_handler.py`
- **Line:** 287
- **Arguments:** self, context_messages, chosen_model, temperature
- **Docstring:** Create and start worker thread for Ollama communication...

---

### `MainApp\event_handler.py._final_worker_cleanup`

- **File:** `MainApp\event_handler.py`
- **Line:** 559
- **Arguments:** self
- **Docstring:** Final cleanup to ensure worker thread is properly destroyed...

---

### `MainApp\event_handler.py._handle_tts_finished_delayed`

- **File:** `MainApp\event_handler.py`
- **Line:** 452
- **Arguments:** self
- **Docstring:** Handle TTS finished with a delay to ensure proper coordination...

---

### `MainApp\event_handler.py._on_clear_chat`

- **File:** `MainApp\event_handler.py`
- **Line:** 743
- **Arguments:** self
- **Docstring:** Clear the chat display...

---

### `MainApp\event_handler.py._on_conversation_deleted`

- **File:** `MainApp\event_handler.py`
- **Line:** 645
- **Arguments:** self, filepath
- **Docstring:** Handle conversation deletion from navigation...

---

### `MainApp\event_handler.py._on_conversation_metadata_updated`

- **File:** `MainApp\event_handler.py`
- **Line:** 716
- **Arguments:** self
- **Docstring:** Handle conversation metadata updates...

---

### `MainApp\event_handler.py._on_conversation_renamed`

- **File:** `MainApp\event_handler.py`
- **Line:** 649
- **Arguments:** self, old_filepath, new_filepath
- **Docstring:** Handle conversation rename from AI naming...

---

### `MainApp\event_handler.py._on_conversation_selected`

- **File:** `MainApp\event_handler.py`
- **Line:** 637
- **Arguments:** self, filepath
- **Docstring:** Handle conversation selection from navigation...

---

### `MainApp\event_handler.py._on_conversation_updated`

- **File:** `MainApp\event_handler.py`
- **Line:** 142
- **Arguments:** self
- **Docstring:** Handle conversation updates from controller...

---

### `MainApp\event_handler.py._on_delayed_model_update`

- **File:** `MainApp\event_handler.py`
- **Line:** 854
- **Arguments:** self
- **Docstring:** Delayed model update to ensure UI is ready...

---

### `MainApp\event_handler.py._on_error_occurred`

- **File:** `MainApp\event_handler.py`
- **Line:** 137
- **Arguments:** self, error_message
- **Docstring:** Handle errors from controller...

---

### `MainApp\event_handler.py._on_load_chat`

- **File:** `MainApp\event_handler.py`
- **Line:** 760
- **Arguments:** self
- **Docstring:** Load a chat from a file...

---

### `MainApp\event_handler.py._on_message_cancelled`

- **File:** `MainApp\event_handler.py`
- **Line:** 610
- **Arguments:** self
- **Docstring:** Handle message cancellation...

---

### `MainApp\event_handler.py._on_message_finished`

- **File:** `MainApp\event_handler.py`
- **Line:** 601
- **Arguments:** self
- **Docstring:** Handle message finished...

---

### `MainApp\event_handler.py._on_message_sent`

- **File:** `MainApp\event_handler.py`
- **Line:** 187
- **Arguments:** self, message
- **Docstring:** Handle new message sent from chat tab...

---

### `MainApp\event_handler.py._on_model_operation_error`

- **File:** `MainApp\event_handler.py`
- **Line:** 702
- **Arguments:** self, error
- **Docstring:** Handle model operation errors...

---

### `MainApp\event_handler.py._on_model_operation_progress`

- **File:** `MainApp\event_handler.py`
- **Line:** 696
- **Arguments:** self, message
- **Docstring:** Handle model operation progress...

---

### `MainApp\event_handler.py._on_models_updated`

- **File:** `MainApp\event_handler.py`
- **Line:** 173
- **Arguments:** self, models
- **Docstring:** Handle model list updates...

---

### `MainApp\event_handler.py._on_name_generation_requested`

- **File:** `MainApp\event_handler.py`
- **Line:** 148
- **Arguments:** self, filepath
- **Docstring:** Handle name generation request from controller...

---

### `MainApp\event_handler.py._on_new_conversation`

- **File:** `MainApp\event_handler.py`
- **Line:** 726
- **Arguments:** self
- **Docstring:** Start a new conversation...

---

### `MainApp\event_handler.py._on_new_conversation_requested`

- **File:** `MainApp\event_handler.py`
- **Line:** 722
- **Arguments:** self
- **Docstring:** Handle new conversation request...

---

### `MainApp\event_handler.py._on_open_settings`

- **File:** `MainApp\event_handler.py`
- **Line:** 766
- **Arguments:** self
- **Docstring:** Open the settings dialog...

---

### `MainApp\event_handler.py._on_personality_changed`

- **File:** `MainApp\event_handler.py`
- **Line:** 671
- **Arguments:** self, personality_name
- **Docstring:** Handle personality changes...

---

### `MainApp\event_handler.py._on_refresh_models`

- **File:** `MainApp\event_handler.py`
- **Line:** 811
- **Arguments:** self
- **Docstring:** Refresh the list of available models...

---

### `MainApp\event_handler.py._on_refresh_personalities`

- **File:** `MainApp\event_handler.py`
- **Line:** 836
- **Arguments:** self
- **Docstring:** Refresh the list of available personalities...

---

### `MainApp\event_handler.py._on_save_chat`

- **File:** `MainApp\event_handler.py`
- **Line:** 754
- **Arguments:** self
- **Docstring:** Save the current chat to a file...

---

### `MainApp\event_handler.py._on_show_about`

- **File:** `MainApp\event_handler.py`
- **Line:** 850
- **Arguments:** self
- **Docstring:** Show about dialog...

---

### `MainApp\event_handler.py._on_status_updated`

- **File:** `MainApp\event_handler.py`
- **Line:** 133
- **Arguments:** self, message
- **Docstring:** Handle status updates from controller...

---

### `MainApp\event_handler.py._on_tts_finished`

- **File:** `MainApp\event_handler.py`
- **Line:** 443
- **Arguments:** self
- **Docstring:** Handle TTS completion...

---

### `MainApp\event_handler.py._on_worker_chunk`

- **File:** `MainApp\event_handler.py`
- **Line:** 405
- **Arguments:** self, chunk
- **Docstring:** Handle worker chunk signal...

---

### `MainApp\event_handler.py._on_worker_detailed_error`

- **File:** `MainApp\event_handler.py`
- **Line:** 375
- **Arguments:** self, error_message
- **Docstring:** Handle detailed worker error with logging...

---

### `MainApp\event_handler.py._on_worker_error`

- **File:** `MainApp\event_handler.py`
- **Line:** 585
- **Arguments:** self, error_message
- **Docstring:** Handle worker error...

---

### `MainApp\event_handler.py._on_worker_finished`

- **File:** `MainApp\event_handler.py`
- **Line:** 419
- **Arguments:** self
- **Docstring:** Handle worker completion...

---

### `MainApp\event_handler.py._on_worker_thread_finished`

- **File:** `MainApp\event_handler.py`
- **Line:** 389
- **Arguments:** self
- **Docstring:** Handle worker thread finished signal...

---

### `MainApp\event_handler.py._send_to_ollama`

- **File:** `MainApp\event_handler.py`
- **Line:** 203
- **Arguments:** self, message, model, temperature
- **Docstring:** Send message to Ollama and handle response asynchronously...

---

### `MainApp\event_handler.py._setup_ui_with_new_services`

- **File:** `MainApp\event_handler.py`
- **Line:** 805
- **Arguments:** self
- **Docstring:** Setup UI with new services after configuration change...

---

### `MainApp\event_handler.py._show_ollama_connection_error`

- **File:** `MainApp\event_handler.py`
- **Line:** 875
- **Arguments:** self, context, force_show
- **Docstring:** Show a user-friendly error dialog when Ollama is not running...

---

### `MainApp\event_handler.py._start_worker_stream`

- **File:** `MainApp\event_handler.py`
- **Line:** 345
- **Arguments:** self, context_messages, chosen_model, temperature, config_manager
- **Docstring:** Start the worker stream in the worker thread...

---

### `MainApp\event_handler.py.cleanup_on_exit`

- **File:** `MainApp\event_handler.py`
- **Line:** 916
- **Arguments:** self
- **Docstring:** Clean up all resources when application is exiting...

---

### `MainApp\event_handler.py.setup_connections`

- **File:** `MainApp\event_handler.py`
- **Line:** 36
- **Arguments:** self
- **Docstring:** Setup all signal connections between components...

---

### `MainApp\ollama_chat.py.__init__`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 26
- **Arguments:** self

---

### `MainApp\ollama_chat.py._setup_ui`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 82
- **Arguments:** self
- **Docstring:** Setup the UI components...

---

### `MainApp\ollama_chat.py.check_ollama_connection`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 123
- **Arguments:** self
- **Docstring:** Check if Ollama is running and accessible...

---

### `MainApp\ollama_chat.py.closeEvent`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 115
- **Arguments:** self, event
- **Docstring:** Handle application close event...

---

### `MainApp\ollama_chat.py.get_chat_controller`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 144
- **Arguments:** self
- **Docstring:** Get the chat controller...

---

### `MainApp\ollama_chat.py.get_event_handler`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 136
- **Arguments:** self
- **Docstring:** Get the Event Bus...

---

### `MainApp\ollama_chat.py.get_lifecycle_manager`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 140
- **Arguments:** self
- **Docstring:** Get the lifecycle manager...

---

### `MainApp\ollama_chat.py.get_service_manager`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 128
- **Arguments:** self
- **Docstring:** Get the service manager...

---

### `MainApp\ollama_chat.py.get_ui_manager`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 132
- **Arguments:** self
- **Docstring:** Get the UI manager...

---

### `MainApp\ollama_chat.py.showEvent`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 110
- **Arguments:** self, event
- **Docstring:** Handle application show event...

---

### `MainApp\ollama_chat.py.show_ollama_connection_error`

- **File:** `MainApp\ollama_chat.py`
- **Line:** 119
- **Arguments:** self, context, force_show
- **Docstring:** Show Ollama connection error dialog...

---

### `MainApp\service_manager.py.__init__`

- **File:** `MainApp\service_manager.py`
- **Line:** 20
- **Arguments:** self, config_manager

---

### `MainApp\service_manager.py._initialize_services`

- **File:** `MainApp\service_manager.py`
- **Line:** 33
- **Arguments:** self
- **Docstring:** Initialize all application services...

---

### `MainApp\service_manager.py.cleanup`

- **File:** `MainApp\service_manager.py`
- **Line:** 112
- **Arguments:** self
- **Docstring:** Clean up services on application shutdown...

---

### `MainApp\service_manager.py.get_conversation_manager`

- **File:** `MainApp\service_manager.py`
- **Line:** 100
- **Arguments:** self
- **Returns:** ConversationManager
- **Docstring:** Get the conversation manager instance...

---

### `MainApp\service_manager.py.get_conversation_service`

- **File:** `MainApp\service_manager.py`
- **Line:** 84
- **Arguments:** self
- **Returns:** ConversationService
- **Docstring:** Get the conversation service instance...

---

### `MainApp\service_manager.py.get_enhancement_service`

- **File:** `MainApp\service_manager.py`
- **Line:** 88
- **Arguments:** self
- **Returns:** EnhancementService
- **Docstring:** Get the enhancement service instance...

---

### `MainApp\service_manager.py.get_memory_service`

- **File:** `MainApp\service_manager.py`
- **Line:** 92
- **Arguments:** self
- **Docstring:** Get the memory service instance (may be None if disabled)...

---

### `MainApp\service_manager.py.get_ollama_service`

- **File:** `MainApp\service_manager.py`
- **Line:** 80
- **Arguments:** self
- **Returns:** OllamaService
- **Docstring:** Get the Ollama service instance...

---

### `MainApp\service_manager.py.get_session_variables`

- **File:** `MainApp\service_manager.py`
- **Line:** 108
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get session variables...

---

### `MainApp\service_manager.py.get_summarization_service`

- **File:** `MainApp\service_manager.py`
- **Line:** 96
- **Arguments:** self
- **Returns:** SummarizationService
- **Docstring:** Get the summarization service instance...

---

### `MainApp\service_manager.py.is_memory_enabled`

- **File:** `MainApp\service_manager.py`
- **Line:** 104
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if memory is enabled...

---

### `MainApp\service_manager.py.reinitialize_services`

- **File:** `MainApp\service_manager.py`
- **Line:** 75
- **Arguments:** self
- **Docstring:** Reinitialize services (used when configuration changes)...

---

### `MainApp\ui_manager.py.__init__`

- **File:** `MainApp\ui_manager.py`
- **Line:** 26
- **Arguments:** self, main_window, config_manager

---

### `MainApp\ui_manager.py.apply_theme`

- **File:** `MainApp\ui_manager.py`
- **Line:** 174
- **Arguments:** self, theme
- **Docstring:** Apply the specified theme...

---

### `MainApp\ui_manager.py.get_chat_tab`

- **File:** `MainApp\ui_manager.py`
- **Line:** 200
- **Arguments:** self
- **Docstring:** Get the chat tab instance...

---

### `MainApp\ui_manager.py.get_memory_tab`

- **File:** `MainApp\ui_manager.py`
- **Line:** 212
- **Arguments:** self
- **Docstring:** Get the memory tab instance...

---

### `MainApp\ui_manager.py.get_menu_action`

- **File:** `MainApp\ui_manager.py`
- **Line:** 196
- **Arguments:** self, action_name
- **Docstring:** Get a menu action by name...

---

### `MainApp\ui_manager.py.get_model_tab`

- **File:** `MainApp\ui_manager.py`
- **Line:** 204
- **Arguments:** self
- **Docstring:** Get the model tab instance...

---

### `MainApp\ui_manager.py.get_personality_tab`

- **File:** `MainApp\ui_manager.py`
- **Line:** 208
- **Arguments:** self
- **Docstring:** Get the personality tab instance...

---

### `MainApp\ui_manager.py.get_tabs`

- **File:** `MainApp\ui_manager.py`
- **Line:** 216
- **Arguments:** self
- **Docstring:** Get the tab widget instance...

---

### `MainApp\ui_manager.py.setup_menu_bar`

- **File:** `MainApp\ui_manager.py`
- **Line:** 93
- **Arguments:** self
- **Docstring:** Setup the menu bar with all actions...

---

### `MainApp\ui_manager.py.setup_ui`

- **File:** `MainApp\ui_manager.py`
- **Line:** 40
- **Arguments:** self, conversation_manager, summarization_service, memory_enabled, memory_service
- **Docstring:** Setup the main UI components...

---

### `MainApp\ui_manager.py.show_about_dialog`

- **File:** `MainApp\ui_manager.py`
- **Line:** 220
- **Arguments:** self
- **Docstring:** Show the about dialog...

---

### `MainApp\ui_manager.py.show_clear_chat_dialog`

- **File:** `MainApp\ui_manager.py`
- **Line:** 228
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Show clear chat confirmation dialog...

---

### `MainApp\ui_manager.py.update_status`

- **File:** `MainApp\ui_manager.py`
- **Line:** 187
- **Arguments:** self, message
- **Docstring:** Update status bar message...

---

### `Personalities\models\personality_pronouns.py.format_user_reference`

- **File:** `Personalities\models\personality_pronouns.py`
- **Line:** 134
- **Arguments:** self, template
- **Returns:** str
- **Docstring:** Format a template with appropriate user references...

---

### `Personalities\models\personality_pronouns.py.get_formal_title`

- **File:** `Personalities\models\personality_pronouns.py`
- **Line:** 63
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the most formal title from the list...

---

### `Personalities\models\personality_pronouns.py.get_primary_title`

- **File:** `Personalities\models\personality_pronouns.py`
- **Line:** 53
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the primary (first) user title...

---

### `Personalities\models\personality_pronouns.py.get_pronoun_guide`

- **File:** `Personalities\models\personality_pronouns.py`
- **Line:** 80
- **Arguments:** self
- **Returns:** str
- **Docstring:** Generate a comprehensive pronoun guide for the AI...

---

### `Personalities\models\personality_pronouns.py.get_random_title`

- **File:** `Personalities\models\personality_pronouns.py`
- **Line:** 58
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get a random user title for variety...

---

### `Personalities\models\personality_pronouns.py.get_user_address`

- **File:** `Personalities\models\personality_pronouns.py`
- **Line:** 123
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the appropriate way to address the user...

---

### `Personalities\models\personality_pronouns.py.get_user_titles`

- **File:** `Personalities\models\personality_pronouns.py`
- **Line:** 37
- **Arguments:** self
- **Docstring:** Get user titles as a list, handling both string and list formats...

---

### `Personalities\models\personality_types.py.__post_init__`

- **File:** `Personalities\models\personality_types.py`
- **Line:** 66
- **Arguments:** self

---

### `Personalities\personality_model.py.__init__`

- **File:** `Personalities\personality_model.py`
- **Line:** 26
- **Arguments:** self, personalities_dir

---

### `Personalities\personality_model.py._extract_personality_name`

- **File:** `Personalities\personality_model.py`
- **Line:** 45
- **Arguments:** self, filepath
- **Returns:** str
- **Docstring:** Extract personality name - now handled by loader...

---

### `Personalities\personality_model.py._find_personality_file_by_name`

- **File:** `Personalities\personality_model.py`
- **Line:** 54
- **Arguments:** self, personality_name
- **Docstring:** Find personality file by name - now handled by loader...

---

### `Personalities\personality_model.py._find_personality_files`

- **File:** `Personalities\personality_model.py`
- **Line:** 41
- **Arguments:** self, directory
- **Docstring:** Find personality files - now handled by loader...

---

### `Personalities\personality_model.py._initialize_default_personalities`

- **File:** `Personalities\personality_model.py`
- **Line:** 34
- **Arguments:** self
- **Docstring:** Initialize the default personality set - now handled by service...

---

### `Personalities\personality_model.py._load_custom_personalities`

- **File:** `Personalities\personality_model.py`
- **Line:** 49
- **Arguments:** self
- **Docstring:** Load custom personalities - now handled by service...

---

### `Personalities\personality_model.py.get_personality_formatter`

- **File:** `Personalities\personality_model.py`
- **Line:** 68
- **Arguments:** self
- **Docstring:** Get access to the personality formatter for advanced operations...

---

### `Personalities\personality_model.py.get_personality_loader`

- **File:** `Personalities\personality_model.py`
- **Line:** 64
- **Arguments:** self
- **Docstring:** Get access to the personality loader for advanced operations...

---

### `Personalities\personality_model.py.save_custom_personality`

- **File:** `Personalities\personality_model.py`
- **Line:** 58
- **Arguments:** self, name, personality_data
- **Returns:** bool
- **Docstring:** Save a custom personality - for backward compatibility...

---

### `Personalities\services\personality_loader.py.__init__`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 23
- **Arguments:** self, personalities_dir

---

### `Personalities\services\personality_loader.py.backup_personality`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 181
- **Arguments:** self, name, backup_dir
- **Returns:** bool
- **Docstring:** Create a backup of a personality file...

---

### `Personalities\services\personality_loader.py.create_personality_data`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 144
- **Arguments:** self, traits, prompt, config, metadata
- **Docstring:** Create personality data dictionary from component objects...

---

### `Personalities\services\personality_loader.py.delete_personality_file`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 132
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Delete a personality file...

---

### `Personalities\services\personality_loader.py.extract_personality_name`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 53
- **Arguments:** self, filepath
- **Returns:** str
- **Docstring:** Extract personality name from file path, preserving folder structure for uniqueness...

---

### `Personalities\services\personality_loader.py.find_personality_file_by_name`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 117
- **Arguments:** self, personality_name
- **Docstring:** Find the actual file path for a personality by its name...

---

### `Personalities\services\personality_loader.py.find_personality_files`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 35
- **Arguments:** self, directory
- **Docstring:** Recursively find all personality JSON files in the given directory and subdirectories...

---

### `Personalities\services\personality_loader.py.get_personality_file_info`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 241
- **Arguments:** self, filepath
- **Docstring:** Get information about a personality file...

---

### `Personalities\services\personality_loader.py.list_backup_files`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 261
- **Arguments:** self, backup_dir
- **Docstring:** List all backup files...

---

### `Personalities\services\personality_loader.py.load_all_personalities`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 78
- **Arguments:** self
- **Docstring:** Load all personalities from JSON files recursively...

---

### `Personalities\services\personality_loader.py.load_personality_from_file`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 68
- **Arguments:** self, filepath
- **Docstring:** Load a single personality from a JSON file...

---

### `Personalities\services\personality_loader.py.restore_personality_from_backup`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 210
- **Arguments:** self, backup_filepath
- **Returns:** bool
- **Docstring:** Restore a personality from a backup file...

---

### `Personalities\services\personality_loader.py.save_personality_to_file`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 90
- **Arguments:** self, name, personality_data
- **Returns:** bool
- **Docstring:** Save a personality to a JSON file...

---

### `Personalities\services\personality_loader.py.validate_personality_file`

- **File:** `Personalities\services\personality_loader.py`
- **Line:** 162
- **Arguments:** self, filepath
- **Docstring:** Validate a personality file and return list of errors...

---

### `Personalities\services\personality_service.py.__init__`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 23
- **Arguments:** self, personalities_dir

---

### `Personalities\services\personality_service.py._initialize_personalities`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 36
- **Arguments:** self
- **Docstring:** Initialize personalities by loading from files...

---

### `Personalities\services\personality_service.py.build_comprehensive_system_prompt`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 289
- **Arguments:** self, memory_service
- **Returns:** str
- **Docstring:** Build a comprehensive system prompt with pronoun guidance...

---

### `Personalities\services\personality_service.py.create_custom_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 109
- **Arguments:** self, name, traits, prompt, config, metadata
- **Returns:** bool
- **Docstring:** Create a new custom personality in the Custom folder...

---

### `Personalities\services\personality_service.py.delete_custom_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 138
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Delete a custom personality (only if it's in the Custom folder)...

---

### `Personalities\services\personality_service.py.format_prompt_with_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 215
- **Arguments:** self, user_input, context
- **Returns:** str
- **Docstring:** Format a prompt using the current personality's prompt templates...

---

### `Personalities\services\personality_service.py.get_ai_name`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 435
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the AI's name from the current personality...

---

### `Personalities\services\personality_service.py.get_available_personalities`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 88
- **Arguments:** self
- **Docstring:** Get list of all available personality names...

---

### `Personalities\services\personality_service.py.get_current_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 103
- **Arguments:** self
- **Docstring:** Get the current active personality...

---

### `Personalities\services\personality_service.py.get_custom_personalities`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 80
- **Arguments:** self
- **Docstring:** Get custom personalities (editable/deletable)...

---

### `Personalities\services\personality_service.py.get_personalities_by_category`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 379
- **Arguments:** self, category
- **Docstring:** Get personalities by category...

---

### `Personalities\services\personality_service.py.get_personalities_by_folder`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 392
- **Arguments:** self, folder_name
- **Docstring:** Get personalities by folder name...

---

### `Personalities\services\personality_service.py.get_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 92
- **Arguments:** self, name
- **Docstring:** Get personality by name...

---

### `Personalities\services\personality_service.py.get_personality_categories`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 368
- **Arguments:** self
- **Docstring:** Get list of all personality categories...

---

### `Personalities\services\personality_service.py.get_personality_config`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 254
- **Arguments:** self, name
- **Docstring:** Get configuration for a personality...

---

### `Personalities\services\personality_service.py.get_personality_info`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 249
- **Arguments:** self, name
- **Docstring:** Get detailed information about a personality...

---

### `Personalities\services\personality_service.py.get_selected_model`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 431
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality name...

---

### `Personalities\services\personality_service.py.get_system_personalities`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 72
- **Arguments:** self
- **Docstring:** Get system personalities (read-only)...

---

### `Personalities\services\personality_service.py.get_system_prompt`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 232
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the system prompt for the current personality...

---

### `Personalities\services\personality_service.py.get_user_context_messages`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 300
- **Arguments:** self, memory_service, is_new_conversation
- **Docstring:** Get dynamic user context messages that should be added to conversation...

---

### `Personalities\services\personality_service.py.is_custom_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 68
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Check if a personality is a custom personality (editable/deletable)...

---

### `Personalities\services\personality_service.py.is_system_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 59
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Check if a personality is a system personality (read-only)...

---

### `Personalities\services\personality_service.py.refresh_personalities`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 194
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Refresh personalities from disk, reloading all JSON files...

---

### `Personalities\services\personality_service.py.search_personalities`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 402
- **Arguments:** self, query
- **Docstring:** Search personalities by name, description, or tags...

---

### `Personalities\services\personality_service.py.set_current_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 96
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Set the current active personality...

---

### `Personalities\services\personality_service.py.update_custom_personality`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 169
- **Arguments:** self, name, traits, prompt, config, metadata
- **Returns:** bool
- **Docstring:** Update a custom personality (only if it's in the Custom folder)...

---

### `Personalities\services\personality_service.py.update_personality_metadata`

- **File:** `Personalities\services\personality_service.py`
- **Line:** 265
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Update metadata for a personality...

---

### `Personalities\utils\personality_formatter.py.build_comprehensive_system_prompt`

- **File:** `Personalities\utils\personality_formatter.py`
- **Line:** 53
- **Arguments:** personality_data
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Build a comprehensive system prompt with pronoun guidance...

---

### `Personalities\utils\personality_formatter.py.create_personality_template`

- **File:** `Personalities\utils\personality_formatter.py`
- **Line:** 244
- **Arguments:** name, description
- **Decorators:** staticmethod
- **Docstring:** Create a template personality data structure...

---

### `Personalities\utils\personality_formatter.py.format_personality_summary`

- **File:** `Personalities\utils\personality_formatter.py`
- **Line:** 204
- **Arguments:** personality_data
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format a brief summary of a personality...

---

### `Personalities\utils\personality_formatter.py.format_prompt_with_personality`

- **File:** `Personalities\utils\personality_formatter.py`
- **Line:** 17
- **Arguments:** personality_data, user_input, context
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format a prompt using the personality's prompt templates...

---

### `Personalities\utils\personality_formatter.py.get_personality_info`

- **File:** `Personalities\utils\personality_formatter.py`
- **Line:** 147
- **Arguments:** personality_data
- **Decorators:** staticmethod
- **Docstring:** Get detailed information about a personality...

---

### `Personalities\utils\personality_formatter.py.get_system_prompt`

- **File:** `Personalities\utils\personality_formatter.py`
- **Line:** 140
- **Arguments:** personality_data
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Get the system prompt for a personality...

---

### `Personalities\utils\personality_formatter.py.validate_personality_data`

- **File:** `Personalities\utils\personality_formatter.py`
- **Line:** 173
- **Arguments:** personality_data
- **Decorators:** staticmethod
- **Docstring:** Validate personality data and return list of errors...

---

### `config\config_manager.py.__init__`

- **File:** `config\config_manager.py`
- **Line:** 11
- **Arguments:** self, config_file

---

### `config\config_manager.py.get`

- **File:** `config\config_manager.py`
- **Line:** 86
- **Arguments:** self, key, default
- **Returns:** Any
- **Docstring:** Get a configuration value...

---

### `config\config_manager.py.get_chat_settings`

- **File:** `config\config_manager.py`
- **Line:** 149
- **Arguments:** self
- **Docstring:** Get chat settings...

---

### `config\config_manager.py.get_default_model`

- **File:** `config\config_manager.py`
- **Line:** 116
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the default model name...

---

### `config\config_manager.py.get_default_personality`

- **File:** `config\config_manager.py`
- **Line:** 132
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the default personality...

---

### `config\config_manager.py.get_default_temperature`

- **File:** `config\config_manager.py`
- **Line:** 124
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get the default temperature...

---

### `config\config_manager.py.get_frequency_penalty`

- **File:** `config\config_manager.py`
- **Line:** 245
- **Arguments:** self

---

### `config\config_manager.py.get_history_directory`

- **File:** `config\config_manager.py`
- **Line:** 183
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the chat history directory...

---

### `config\config_manager.py.get_max_context_messages`

- **File:** `config\config_manager.py`
- **Line:** 252
- **Arguments:** self
- **Returns:** int
- **Docstring:** Get the maximum number of context messages for memory management...

---

### `config\config_manager.py.get_max_tokens`

- **File:** `config\config_manager.py`
- **Line:** 239
- **Arguments:** self

---

### `config\config_manager.py.get_ollama_url`

- **File:** `config\config_manager.py`
- **Line:** 174
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the Ollama API URL...

---

### `config\config_manager.py.get_presence_penalty`

- **File:** `config\config_manager.py`
- **Line:** 248
- **Arguments:** self
- **Docstring:** Get the presence penalty setting...

---

### `config\config_manager.py.get_top_p`

- **File:** `config\config_manager.py`
- **Line:** 242
- **Arguments:** self

---

### `config\config_manager.py.get_voice_settings`

- **File:** `config\config_manager.py`
- **Line:** 260
- **Arguments:** self
- **Docstring:** Get voice settings...

---

### `config\config_manager.py.get_window_size`

- **File:** `config\config_manager.py`
- **Line:** 140
- **Arguments:** self
- **Returns:** tuple
- **Docstring:** Get the default window size...

---

### `config\config_manager.py.is_auto_save_enabled`

- **File:** `config\config_manager.py`
- **Line:** 158
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if auto-save is enabled...

---

### `config\config_manager.py.is_enhancement_enabled`

- **File:** `config\config_manager.py`
- **Line:** 191
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if response enhancement is enabled...

---

### `config\config_manager.py.is_history_enabled`

- **File:** `config\config_manager.py`
- **Line:** 199
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if history is enabled...

---

### `config\config_manager.py.is_json_format_enabled`

- **File:** `config\config_manager.py`
- **Line:** 215
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if JSON format is enabled...

---

### `config\config_manager.py.is_spellcheck_enabled`

- **File:** `config\config_manager.py`
- **Line:** 166
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if spellcheck is enabled...

---

### `config\config_manager.py.is_think_enabled`

- **File:** `config\config_manager.py`
- **Line:** 231
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if think mode is enabled...

---

### `config\config_manager.py.is_verbose_enabled`

- **File:** `config\config_manager.py`
- **Line:** 223
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if verbose is enabled...

---

### `config\config_manager.py.is_wordwrap_enabled`

- **File:** `config\config_manager.py`
- **Line:** 207
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if wordwrap is enabled...

---

### `config\config_manager.py.load_config`

- **File:** `config\config_manager.py`
- **Line:** 15
- **Arguments:** self
- **Docstring:** Load configuration from file or create default if not exists...

---

### `config\config_manager.py.merge_configs`

- **File:** `config\config_manager.py`
- **Line:** 63
- **Arguments:** self, default, loaded
- **Docstring:** Merge loaded config with defaults, ensuring all keys exist...

---

### `config\config_manager.py.save_config`

- **File:** `config\config_manager.py`
- **Line:** 73
- **Arguments:** self, config
- **Returns:** bool
- **Docstring:** Save configuration to file...

---

### `config\config_manager.py.set`

- **File:** `config\config_manager.py`
- **Line:** 99
- **Arguments:** self, key, value
- **Returns:** bool
- **Docstring:** Set a configuration value...

---

### `config\config_manager.py.set_auto_save_enabled`

- **File:** `config\config_manager.py`
- **Line:** 162
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set auto-save enabled/disabled...

---

### `config\config_manager.py.set_default_model`

- **File:** `config\config_manager.py`
- **Line:** 120
- **Arguments:** self, model_name
- **Returns:** bool
- **Docstring:** Set the default model name...

---

### `config\config_manager.py.set_default_personality`

- **File:** `config\config_manager.py`
- **Line:** 136
- **Arguments:** self, personality
- **Returns:** bool
- **Docstring:** Set the default personality...

---

### `config\config_manager.py.set_default_temperature`

- **File:** `config\config_manager.py`
- **Line:** 128
- **Arguments:** self, temperature
- **Returns:** bool
- **Docstring:** Set the default temperature...

---

### `config\config_manager.py.set_enhancement_enabled`

- **File:** `config\config_manager.py`
- **Line:** 195
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set response enhancement enabled/disabled...

---

### `config\config_manager.py.set_history_directory`

- **File:** `config\config_manager.py`
- **Line:** 187
- **Arguments:** self, directory
- **Returns:** bool
- **Docstring:** Set the chat history directory...

---

### `config\config_manager.py.set_history_enabled`

- **File:** `config\config_manager.py`
- **Line:** 203
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set history enabled/disabled...

---

### `config\config_manager.py.set_json_format_enabled`

- **File:** `config\config_manager.py`
- **Line:** 219
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set JSON format enabled/disabled...

---

### `config\config_manager.py.set_max_context_messages`

- **File:** `config\config_manager.py`
- **Line:** 256
- **Arguments:** self, max_messages
- **Returns:** bool
- **Docstring:** Set the maximum number of context messages for memory management...

---

### `config\config_manager.py.set_ollama_url`

- **File:** `config\config_manager.py`
- **Line:** 179
- **Arguments:** self, url
- **Returns:** bool
- **Docstring:** Set the Ollama API URL...

---

### `config\config_manager.py.set_spellcheck_enabled`

- **File:** `config\config_manager.py`
- **Line:** 170
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set spellcheck enabled/disabled...

---

### `config\config_manager.py.set_think_enabled`

- **File:** `config\config_manager.py`
- **Line:** 235
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set think mode enabled/disabled...

---

### `config\config_manager.py.set_verbose_enabled`

- **File:** `config\config_manager.py`
- **Line:** 227
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set verbose enabled/disabled...

---

### `config\config_manager.py.set_voice_settings`

- **File:** `config\config_manager.py`
- **Line:** 277
- **Arguments:** self, settings
- **Returns:** bool
- **Docstring:** Set voice settings...

---

### `config\config_manager.py.set_window_size`

- **File:** `config\config_manager.py`
- **Line:** 145
- **Arguments:** self, width, height
- **Returns:** bool
- **Docstring:** Set the default window size...

---

### `config\config_manager.py.set_wordwrap_enabled`

- **File:** `config\config_manager.py`
- **Line:** 211
- **Arguments:** self, enabled
- **Returns:** bool
- **Docstring:** Set wordwrap enabled/disabled...

---

### `controllers\chat_controller.py.__init__`

- **File:** `controllers\chat_controller.py`
- **Line:** 52
- **Arguments:** self, ollama_service, conversation_service, enhancement_service, memory_service, conversation_manager

---

### `controllers\chat_controller.py._build_context`

- **File:** `controllers\chat_controller.py`
- **Line:** 270
- **Arguments:** self, context_messages, is_new_conversation
- **Docstring:** Build the final context for the AI...

---

### `controllers\chat_controller.py._detect_new_conversation`

- **File:** `controllers\chat_controller.py`
- **Line:** 256
- **Arguments:** self, context_messages
- **Returns:** bool
- **Docstring:** Detect if this is a new conversation...

---

### `controllers\chat_controller.py._extract_and_store_facts`

- **File:** `controllers\chat_controller.py`
- **Line:** 126
- **Arguments:** self, message
- **Docstring:** Extract facts from the message using LLM and store in long-term memory...

---

### `controllers\chat_controller.py._extract_facts_with_llm`

- **File:** `controllers\chat_controller.py`
- **Line:** 144
- **Arguments:** self, message
- **Docstring:** Use qwen3:0.6b to extract facts as key-value pairs from a message...

---

### `controllers\chat_controller.py._handle_memory_operations`

- **File:** `controllers\chat_controller.py`
- **Line:** 113
- **Arguments:** self, message
- **Docstring:** Handle memory-related operations for a message...

---

### `controllers\chat_controller.py._select_model`

- **File:** `controllers\chat_controller.py`
- **Line:** 276
- **Arguments:** self, requested_model, message, context_messages
- **Returns:** str
- **Docstring:** Select the appropriate model for the request...

---

### `controllers\chat_controller.py._send_to_ollama`

- **File:** `controllers\chat_controller.py`
- **Line:** 231
- **Arguments:** self, message, model, temperature
- **Docstring:** Send message to Ollama and handle response...

---

### `controllers\chat_controller.py._store_extracted_facts`

- **File:** `controllers\chat_controller.py`
- **Line:** 206
- **Arguments:** self, facts
- **Docstring:** Store extracted facts in memory...

---

### `controllers\chat_controller.py._trigger_name_generation`

- **File:** `controllers\chat_controller.py`
- **Line:** 348
- **Arguments:** self, filepath
- **Docstring:** Trigger AI name generation for a conversation...

---

### `controllers\chat_controller.py._trigger_tts_for_response`

- **File:** `controllers\chat_controller.py`
- **Line:** 329
- **Arguments:** self, response
- **Docstring:** Trigger TTS for AI response if voice mode is active...

---

### `controllers\chat_controller.py.accumulate_assistant_response`

- **File:** `controllers\chat_controller.py`
- **Line:** 297
- **Arguments:** self, chunk
- **Docstring:** Accumulate assistant response chunk....

---

### `controllers\chat_controller.py.clear_conversation`

- **File:** `controllers\chat_controller.py`
- **Line:** 402
- **Arguments:** self
- **Docstring:** Clear the current conversation...

---

### `controllers\chat_controller.py.clear_pending_assistant_response`

- **File:** `controllers\chat_controller.py`
- **Line:** 301
- **Arguments:** self

---

### `controllers\chat_controller.py.delete_conversation`

- **File:** `controllers\chat_controller.py`
- **Line:** 430
- **Arguments:** self, filepath
- **Docstring:** Delete a conversation...

---

### `controllers\chat_controller.py.handle_ai_response`

- **File:** `controllers\chat_controller.py`
- **Line:** 304
- **Arguments:** self
- **Docstring:** Handle AI response completion using accumulated response....

---

### `controllers\chat_controller.py.is_memory_active`

- **File:** `controllers\chat_controller.py`
- **Line:** 72
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if memory is enabled and available...

---

### `controllers\chat_controller.py.load_conversation`

- **File:** `controllers\chat_controller.py`
- **Line:** 408
- **Arguments:** self, filepath
- **Docstring:** Load a conversation from file...

---

### `controllers\chat_controller.py.process_user_message`

- **File:** `controllers\chat_controller.py`
- **Line:** 76
- **Arguments:** self, message, model, temperature
- **Docstring:** Process a user message through the complete pipeline...

---

### `controllers\chat_controller.py.remove_emojis`

- **File:** `controllers\chat_controller.py`
- **Line:** 25
- **Arguments:** text

---

### `controllers\chat_controller.py.rename_conversation`

- **File:** `controllers\chat_controller.py`
- **Line:** 443
- **Arguments:** self, old_filepath, new_filepath
- **Docstring:** Handle conversation rename...

---

### `controllers\chat_controller.py.set_chat_tab_reference`

- **File:** `controllers\chat_controller.py`
- **Line:** 344
- **Arguments:** self, chat_tab
- **Docstring:** Set reference to chat tab for TTS functionality...

---

### `controllers\chat_controller.py.start_new_conversation`

- **File:** `controllers\chat_controller.py`
- **Line:** 355
- **Arguments:** self
- **Docstring:** Start a new conversation...

---

### `models\conversation_metadata.py.__init__`

- **File:** `models\conversation_metadata.py`
- **Line:** 135
- **Arguments:** self, history_dir

---

### `models\conversation_metadata.py.__post_init__`

- **File:** `models\conversation_metadata.py`
- **Line:** 30
- **Arguments:** self
- **Docstring:** Initialize default values after object creation...

---

### `models\conversation_metadata.py._create_safe_filename`

- **File:** `models\conversation_metadata.py`
- **Line:** 252
- **Arguments:** self, ai_generated_name
- **Returns:** str
- **Docstring:** Create a safe filename from the AI-generated name

Args:
    ai_generated_name: The AI-generated nam...

---

### `models\conversation_metadata.py.auto_save_conversation`

- **File:** `models\conversation_metadata.py`
- **Line:** 324
- **Arguments:** self, conversation
- **Docstring:** Auto-save conversation if enabled

Args:
    conversation: List of conversation messages
    
Return...

---

### `models\conversation_metadata.py.clear_current_conversation`

- **File:** `models\conversation_metadata.py`
- **Line:** 469
- **Arguments:** self
- **Docstring:** Clear current conversation metadata...

---

### `models\conversation_metadata.py.delete_conversation`

- **File:** `models\conversation_metadata.py`
- **Line:** 427
- **Arguments:** self, filepath
- **Returns:** bool
- **Docstring:** Delete a conversation file

Args:
    filepath: Path to conversation file
    
Returns:
    True if ...

---

### `models\conversation_metadata.py.find_blank_conversation`

- **File:** `models\conversation_metadata.py`
- **Line:** 483
- **Arguments:** self
- **Docstring:** Find the most recent blank conversation (0 messages)

Returns:
    Filepath of the most recent blank...

---

### `models\conversation_metadata.py.from_dict`

- **File:** `models\conversation_metadata.py`
- **Line:** 74
- **Arguments:** cls, data
- **Decorators:** classmethod
- **Docstring:** Create metadata from dictionary...

---

### `models\conversation_metadata.py.get_current_metadata`

- **File:** `models\conversation_metadata.py`
- **Line:** 474
- **Arguments:** self
- **Returns:** ConversationMetadata
- **Docstring:** Get current metadata...

---

### `models\conversation_metadata.py.get_display_info`

- **File:** `models\conversation_metadata.py`
- **Line:** 116
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get formatted display information...

---

### `models\conversation_metadata.py.get_display_name`

- **File:** `models\conversation_metadata.py`
- **Line:** 124
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the display name for the conversation...

---

### `models\conversation_metadata.py.get_formatted_created_time`

- **File:** `models\conversation_metadata.py`
- **Line:** 96
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get formatted creation time for display...

---

### `models\conversation_metadata.py.get_formatted_modified_time`

- **File:** `models\conversation_metadata.py`
- **Line:** 106
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get formatted last modified time for display...

---

### `models\conversation_metadata.py.list_conversations`

- **File:** `models\conversation_metadata.py`
- **Line:** 398
- **Arguments:** self
- **Docstring:** List all saved conversations with their metadata

Returns:
    List of tuples (filepath, metadata)...

---

### `models\conversation_metadata.py.load_conversation`

- **File:** `models\conversation_metadata.py`
- **Line:** 292
- **Arguments:** self, filepath
- **Docstring:** Load conversation and metadata from file

Args:
    filepath: Path to conversation file
    
Returns...

---

### `models\conversation_metadata.py.rename_conversation`

- **File:** `models\conversation_metadata.py`
- **Line:** 444
- **Arguments:** self, old_filepath, new_filepath
- **Returns:** bool
- **Docstring:** Rename a conversation file and update references

Args:
    old_filepath: Original file path
    new...

---

### `models\conversation_metadata.py.reset`

- **File:** `models\conversation_metadata.py`
- **Line:** 86
- **Arguments:** self
- **Docstring:** Reset metadata to initial state...

---

### `models\conversation_metadata.py.save_conversation`

- **File:** `models\conversation_metadata.py`
- **Line:** 143
- **Arguments:** self, conversation, filename
- **Returns:** str
- **Docstring:** Save conversation with metadata to file

Args:
    conversation: List of conversation messages
    f...

---

### `models\conversation_metadata.py.set_auto_save_enabled`

- **File:** `models\conversation_metadata.py`
- **Line:** 478
- **Arguments:** self, enabled
- **Docstring:** Enable or disable auto-save...

---

### `models\conversation_metadata.py.to_dict`

- **File:** `models\conversation_metadata.py`
- **Line:** 61
- **Arguments:** self
- **Docstring:** Convert metadata to dictionary for JSON serialization...

---

### `models\conversation_metadata.py.update_ai_generated_name`

- **File:** `models\conversation_metadata.py`
- **Line:** 56
- **Arguments:** self, name
- **Docstring:** Update the AI-generated name...

---

### `models\conversation_metadata.py.update_conversation_name`

- **File:** `models\conversation_metadata.py`
- **Line:** 180
- **Arguments:** self, filepath, ai_generated_name
- **Docstring:** Update the AI-generated name for a conversation and rename the file

Args:
    filepath: Path to the...

---

### `models\conversation_metadata.py.update_message_count`

- **File:** `models\conversation_metadata.py`
- **Line:** 41
- **Arguments:** self, count
- **Docstring:** Update the message count...

---

### `models\conversation_metadata.py.update_model`

- **File:** `models\conversation_metadata.py`
- **Line:** 46
- **Arguments:** self, model
- **Docstring:** Update the model information...

---

### `models\conversation_metadata.py.update_personality`

- **File:** `models\conversation_metadata.py`
- **Line:** 51
- **Arguments:** self, personality
- **Docstring:** Update the personality information...

---

### `models\conversation_metadata.py.update_timestamp`

- **File:** `models\conversation_metadata.py`
- **Line:** 37
- **Arguments:** self
- **Docstring:** Update the last modified timestamp...

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.__del__`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 50
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 21
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py._calculate_audio_level`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 180
- **Arguments:** self, audio_data
- **Returns:** float

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py._check_availability`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 56
- **Arguments:** self
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py._record_audio`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 91
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.audio_level_to_db`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 194
- **Arguments:** self, audio_level
- **Returns:** float

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.cleanup`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 234
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.get_current_audio_level`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 205
- **Arguments:** self
- **Returns:** float

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.get_speech_detection_parameters`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 225
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get current speech detection parameters...

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.is_available`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 71
- **Arguments:** self
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.set_audio_gate_enabled`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 208
- **Arguments:** self, enabled

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.set_speech_detection_parameters`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 215
- **Arguments:** self, silence_duration, silence_threshold, min_speech_duration
- **Docstring:** Configure speech detection parameters for better user experience...

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.start_recording`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 74
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py.stop_recording`

- **File:** `services\Voice_STT_TTS_SERVICES\Recording_Service.py`
- **Line:** 243
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__`

- **File:** `services\Voice_STT_TTS_SERVICES\STT_Service.py`
- **Line:** 15
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\STT_Service.py._check_availability`

- **File:** `services\Voice_STT_TTS_SERVICES\STT_Service.py`
- **Line:** 21
- **Arguments:** self
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\STT_Service.py._convert_with_vosk`

- **File:** `services\Voice_STT_TTS_SERVICES\STT_Service.py`
- **Line:** 53
- **Arguments:** self, audio_file

---

### `services\Voice_STT_TTS_SERVICES\STT_Service.py.convert_audio_to_text`

- **File:** `services\Voice_STT_TTS_SERVICES\STT_Service.py`
- **Line:** 46
- **Arguments:** self, audio_file

---

### `services\Voice_STT_TTS_SERVICES\STT_Service.py.is_available`

- **File:** `services\Voice_STT_TTS_SERVICES\STT_Service.py`
- **Line:** 43
- **Arguments:** self
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\STT_Service.py.update_api`

- **File:** `services\Voice_STT_TTS_SERVICES\STT_Service.py`
- **Line:** 86
- **Arguments:** self, api_name

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 24
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py._check_availability`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 47
- **Arguments:** self
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py._simulate_tts_finished`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 130
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py._speak_with_espeak`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 107
- **Arguments:** self, text

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.get_coqui_model_info`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 183
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get information about the current Coqui TTS model...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.get_coqui_models`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 171
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get available Coqui TTS models...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.get_coqui_voices`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 177
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get available Coqui TTS voices for current model...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.is_available`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 56
- **Arguments:** self
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.is_coqui_available`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 167
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Coqui TTS is available...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.load_coqui_model`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 189
- **Arguments:** self, model_name
- **Returns:** bool
- **Docstring:** Load a specific Coqui TTS model...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.set_coqui_model`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 195
- **Arguments:** self, model_name
- **Returns:** bool
- **Docstring:** Set the Coqui TTS model to use...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.speak_text`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 59
- **Arguments:** self, text

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.speak_text_non_streaming`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 90
- **Arguments:** self, text
- **Docstring:** Convert text to speech using non-streaming synthesis...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.speak_text_streaming`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 74
- **Arguments:** self, text
- **Docstring:** Convert text to speech using streaming synthesis (Coqui TTS only)...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.stop_playback`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 133
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.update_api`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 142
- **Arguments:** self, api_name

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.update_speed`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 158
- **Arguments:** self, speed
- **Docstring:** Update speech speed (1.0 = normal, 1.5 = faster, 0.5 = slower)...

---

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py.update_voice`

- **File:** `services\Voice_STT_TTS_SERVICES\TTS_Service.py`
- **Line:** 150
- **Arguments:** self, voice_name

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 377
- **Arguments:** self
- **Docstring:** Initialize the Coqui TTS service (singleton)...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__new__`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 371
- **Arguments:** cls
- **Docstring:** Singleton pattern to prevent multiple model loading...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._adjust_audio_speed`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 326
- **Arguments:** self, audio
- **Returns:** np.ndarray
- **Docstring:** Adjust audio speed using simple resampling...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._cleanup_audio_file`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 1109
- **Arguments:** self, file_path
- **Docstring:** Clean up temporary audio file...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._emit_audio_level`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 144
- **Arguments:** self
- **Docstring:** Emit averaged audio level for EQ visualization...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._generate_audio`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 1031
- **Arguments:** self, text
- **Docstring:** Generate audio file from text (for non-streaming mode)...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._generate_audio_chunk`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 285
- **Arguments:** self, text
- **Docstring:** Generate audio chunk for a piece of text...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._get_tts_model_cache_dirs`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 476
- **Arguments:** self

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._initialize_service`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 407
- **Arguments:** self
- **Docstring:** Initialize the Coqui TTS service...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._is_model_fully_downloaded`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 501
- **Arguments:** self, model_name
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._load_available_voices`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 456
- **Arguments:** self
- **Docstring:** Load available voices for the current model...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._load_default_model`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 428
- **Arguments:** self
- **Docstring:** Load the default TTS model...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._model_name_to_folder`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 498
- **Arguments:** self, model_name
- **Returns:** str

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._on_media_status_changed`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 1100
- **Arguments:** self, status
- **Docstring:** Handle media player status changes...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._on_streaming_error`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 683
- **Arguments:** self, error
- **Docstring:** Handle streaming playback error...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._on_streaming_finished`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 671
- **Arguments:** self
- **Docstring:** Handle streaming playback finished...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._on_streaming_generation_error`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 665
- **Arguments:** self, error
- **Docstring:** Handle streaming generation error...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._on_streaming_generation_finished`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 660
- **Arguments:** self
- **Docstring:** Handle streaming generation finished...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._play_audio`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 1067
- **Arguments:** self, audio_file, text
- **Docstring:** Play the generated audio file (for non-streaming mode)...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._process_audio_chunk`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 100
- **Arguments:** self, audio_chunk
- **Returns:** np.ndarray
- **Docstring:** Process audio chunk for better quality...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._speak_text_streaming`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 617
- **Arguments:** self, text
- **Docstring:** Convert text to speech using streaming synthesis...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py._split_text_into_sentences`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 258
- **Arguments:** self, text
- **Docstring:** Split text into sentences for chunked processing...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.add_audio_chunk`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 158
- **Arguments:** self, audio_chunk
- **Docstring:** Add audio chunk to playback queue...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.cleanup`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 736
- **Arguments:** self
- **Docstring:** Clean up resources...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.clear_model_cache`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 747
- **Arguments:** self
- **Docstring:** Clear the model cache to free memory...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.download_model`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 553
- **Arguments:** self, model_name
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.end_stream`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 163
- **Arguments:** self
- **Docstring:** Signal end of audio stream...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_available_models`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 879
- **Arguments:** self
- **Returns:** list
- **Docstring:** Return a list of all models: downloaded first, then a curated list of popular downloadable models....

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_available_voices`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 544
- **Arguments:** self
- **Returns:** list

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_cache_info`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 756
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get information about the model cache...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_comprehensive_model_list`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 834
- **Arguments:** self
- **Docstring:** Get a comprehensive list of available models for download...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_current_model_info`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 867
- **Arguments:** self
- **Docstring:** Get information about the current loaded model...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_downloaded_models`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 517
- **Arguments:** self
- **Returns:** list

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_model_config`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 1017
- **Arguments:** self, model_name

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_model_download_size`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 809
- **Arguments:** self, model_name
- **Returns:** str
- **Docstring:** Get estimated download size for a model...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.get_model_info`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 769
- **Arguments:** self, model_name
- **Docstring:** Get information about a specific model without downloading it...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.is_available`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 472
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Coqui TTS is available...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.is_model_downloaded`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 532
- **Arguments:** self, model_name
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.is_model_loaded`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 535
- **Arguments:** self, model_name
- **Returns:** bool
- **Docstring:** Check if a model is currently loaded in memory...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.is_multi_speaker`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 984
- **Arguments:** self
- **Returns:** bool

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.load_model`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 901
- **Arguments:** self, model_name
- **Returns:** bool
- **Docstring:** Load a specific TTS model and update available voices.
Uses caching to prevent duplicate loading....

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.refresh_model_list`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 1118
- **Arguments:** self
- **Docstring:** Refresh the list of available models...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.run`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 226
- **Arguments:** self
- **Docstring:** Generate audio in chunks and stream to player...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.set_speed`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 580
- **Arguments:** self, speed
- **Docstring:** Set speech speed (0.5 to 2.0)...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.set_streaming_volume`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 585
- **Arguments:** self, volume
- **Docstring:** Set streaming audio volume (0.0 to 1.0)...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.set_voice`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 570
- **Arguments:** self, voice_name
- **Returns:** bool
- **Docstring:** Set the current voice...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.set_volume`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 154
- **Arguments:** self, volume
- **Docstring:** Set playback volume (0.0 to 1.0)...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.speak_text`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 591
- **Arguments:** self, text, use_streaming
- **Docstring:** Convert text to speech using Coqui TTS with optional streaming...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.stop`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 350
- **Arguments:** self
- **Docstring:** Stop the worker...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.stop_playback`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 689
- **Arguments:** self
- **Docstring:** Stop current TTS playback (both streaming and non-streaming)...

---

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.terminate_pyaudio`

- **File:** `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`
- **Line:** 192
- **Arguments:** 

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 278
- **Arguments:** self, response_queue, parent

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py._handle_monitor_error`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 241
- **Arguments:** self, error_message
- **Docstring:** Handle monitor thread error...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py._handle_response`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 202
- **Arguments:** self, response
- **Docstring:** Handle response from the voice process...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py._voice_process_worker`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 349
- **Arguments:** command_queue, response_queue
- **Docstring:** Worker function that runs in the separate voice process...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.create_voice_process_manager`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 445
- **Arguments:** 
- **Returns:** VoiceProcessManager
- **Docstring:** Create and start a voice process manager...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.get_process_info`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 255
- **Arguments:** self
- **Docstring:** Get information about the voice process...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.get_stats`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 339
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get monitor statistics for debugging...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.is_process_running`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 249
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if the voice process is running...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.run`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 289
- **Arguments:** self
- **Docstring:** Monitor the response queue...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.send_command`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 185
- **Arguments:** self, command, data
- **Docstring:** Send a command to the voice process...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.start_voice_process`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 52
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Start the voice process and monitoring thread...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.stop`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 324
- **Arguments:** self
- **Docstring:** Stop the monitoring thread safely...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.stop_voice_process`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 105
- **Arguments:** self
- **Docstring:** Stop the voice process and monitoring thread safely...

---

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py.stop_voice_process_manager`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`
- **Line:** 462
- **Arguments:** manager
- **Docstring:** Stop a voice process manager...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.__del__`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 88
- **Arguments:** self
- **Docstring:** Cleanup when voice service is destroyed...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.__init__`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 47
- **Arguments:** self, response_queue

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._cleanup_resources`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 671
- **Arguments:** self
- **Docstring:** Clean up resources when the cleanup timer fires...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._connect_signals`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 764
- **Arguments:** self
- **Docstring:** Connect signals with QueuedConnection for thread safety...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._forward_recording_error`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 655
- **Arguments:** self, error
- **Docstring:** Forward recording error signal to response queue...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._forward_recording_started`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 639
- **Arguments:** self
- **Docstring:** Forward recording started signal to response queue...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._forward_recording_stopped`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 647
- **Arguments:** self
- **Docstring:** Forward recording stopped signal to response queue...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._forward_voice_processing_started`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 663
- **Arguments:** self
- **Docstring:** Forward voice processing started signal to response queue...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._initialize_services`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 685
- **Arguments:** self
- **Docstring:** Initialize voice services with error handling...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._on_recording_auto_stopped`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 233
- **Arguments:** self
- **Docstring:** Handle recording auto-stopped due to silence detection...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._on_recording_timeout`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 227
- **Arguments:** self
- **Docstring:** Handle recording timeout - automatically stop recording...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._on_stt_error`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 271
- **Arguments:** self, error
- **Docstring:** Handle STT error...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._on_stt_text_received`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 239
- **Arguments:** self, text
- **Docstring:** Handle STT text received...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._on_tts_error`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 311
- **Arguments:** self, error
- **Docstring:** Handle TTS error...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._on_tts_finished`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 293
- **Arguments:** self
- **Docstring:** Handle TTS finished...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py._reset_error_count`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 680
- **Arguments:** self
- **Docstring:** Reset error count after a delay...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.cleanup_all_audio_files`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 620
- **Arguments:** self
- **Docstring:** Clean up all audio files (since they're only for STT processing)...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.cleanup_old_audio_files`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 586
- **Arguments:** self, max_files, max_age_days
- **Docstring:** Clean up old audio files to prevent folder from getting too large...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.cleanup_on_exit`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 545
- **Arguments:** self
- **Docstring:** Enhanced cleanup with timeout...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.get_audio_folder_path`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 560
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the path to the audio folder...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.get_current_audio_level`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 528
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current audio level for debugging...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.get_eq_visualizer`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 541
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get current EQ visualizer setting...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.get_min_speech_duration`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 488
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get minimum speech duration setting...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.get_recording_timeout`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 456
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current recording timeout in seconds...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.get_silence_duration`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 465
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current silence duration in seconds...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.get_silence_threshold`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 474
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current silence threshold (0-1)...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.get_speech_detection_sensitivity`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 514
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get current speech detection sensitivity...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.is_continuous_voice_mode`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 537
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if continuous voice mode is enabled...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.is_voice_available`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 399
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice functionality is available...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.list_audio_files`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 564
- **Arguments:** self
- **Returns:** list
- **Docstring:** List all audio files in the audio folder...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.set_audio_gate_enabled`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 523
- **Arguments:** self, enabled
- **Docstring:** Enable or disable audio gate detection...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.set_continuous_voice_mode`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 532
- **Arguments:** self, enabled
- **Docstring:** Enable or disable continuous voice mode...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.set_min_speech_duration`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 483
- **Arguments:** self, duration
- **Docstring:** Set minimum speech duration before considering valid...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.set_recording_timeout`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 460
- **Arguments:** self, timeout
- **Docstring:** Set recording timeout in seconds...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.set_silence_duration`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 469
- **Arguments:** self, duration
- **Docstring:** Set silence duration in seconds...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.set_silence_threshold`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 478
- **Arguments:** self, threshold
- **Docstring:** Set silence threshold (0-1)...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.set_speech_detection_sensitivity`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 492
- **Arguments:** self, sensitivity
- **Docstring:** Set speech detection sensitivity (low, medium, high)...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.speak_text`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 324
- **Arguments:** self, text
- **Docstring:** Convert text to speech and play it...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.speak_text_non_streaming`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 373
- **Arguments:** self, text
- **Docstring:** Convert text to speech using non-streaming synthesis...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.speak_text_streaming`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 353
- **Arguments:** self, text
- **Docstring:** Convert text to speech using streaming synthesis...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.start_voice_input`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 97
- **Arguments:** self
- **Docstring:** Start voice recording and convert to text...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.stop_tts`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 393
- **Arguments:** self
- **Docstring:** Stop current TTS playback...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.stop_voice_input`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 150
- **Arguments:** self
- **Docstring:** Stop voice recording and process the audio...

---

### `services\Voice_STT_TTS_SERVICES\voice_service.py.update_settings`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service.py`
- **Line:** 407
- **Arguments:** self, settings
- **Docstring:** Update voice service settings...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 33
- **Arguments:** self, use_separate_process

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py._init_direct_service`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 76
- **Arguments:** self
- **Docstring:** Initialize direct voice service (fallback)...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py._init_process_manager`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 49
- **Arguments:** self
- **Docstring:** Initialize the process manager...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py._update_cached_state`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 275
- **Arguments:** self
- **Docstring:** Update cached state from process manager...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py._update_cached_state_from_signal`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 281
- **Arguments:** self, state
- **Docstring:** Update cached state from signal...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.cleanup_all_audio_files`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 258
- **Arguments:** self
- **Docstring:** Clean up all audio files...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.cleanup_old_audio_files`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 253
- **Arguments:** self, max_files, max_age_days
- **Docstring:** Clean up old audio files to prevent folder from getting too large...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.cleanup_on_exit`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 234
- **Arguments:** self
- **Docstring:** Clean up resources on application exit...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.get_audio_folder_path`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 241
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the path to the audio folder...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.get_current_audio_level`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 213
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current audio level for debugging...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.get_process_info`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 263
- **Arguments:** self
- **Docstring:** Get information about the voice process...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.get_recording_timeout`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 175
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current recording timeout in seconds...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.get_silence_duration`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 186
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current silence duration in seconds...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.get_silence_threshold`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 197
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get current silence threshold (0-1)...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.is_continuous_voice_mode`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 228
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if continuous voice mode is enabled...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.is_playing_tts`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 300
- **Arguments:** self
- **Returns:** bool
- **Decorators:** property
- **Docstring:** Check if TTS is currently playing...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.is_processing_voice`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 293
- **Arguments:** self
- **Returns:** bool
- **Decorators:** property
- **Docstring:** Check if currently processing voice input...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.is_recording`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 286
- **Arguments:** self
- **Returns:** bool
- **Decorators:** property
- **Docstring:** Check if currently recording...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.is_voice_available`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 157
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice functionality is available...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.list_audio_files`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 247
- **Arguments:** self
- **Returns:** list
- **Docstring:** List all audio files in the audio folder...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.recording_service`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 307
- **Arguments:** self
- **Decorators:** property
- **Docstring:** Get the recording service (only available in direct mode)...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.set_audio_gate_enabled`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 208
- **Arguments:** self, enabled
- **Docstring:** Enable or disable audio gate detection...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.set_continuous_voice_mode`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 219
- **Arguments:** self, enabled
- **Docstring:** Enable or disable continuous voice mode...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.set_recording_timeout`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 181
- **Arguments:** self, timeout
- **Docstring:** Set recording timeout in seconds...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.set_silence_duration`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 192
- **Arguments:** self, duration
- **Docstring:** Set silence duration in seconds...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.set_silence_threshold`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 203
- **Arguments:** self, threshold
- **Docstring:** Set silence threshold (0-1)...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.speak_text`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 121
- **Arguments:** self, text
- **Docstring:** Convert text to speech and play it...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.speak_text_non_streaming`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 139
- **Arguments:** self, text
- **Docstring:** Convert text to speech using non-streaming synthesis...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.speak_text_streaming`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 130
- **Arguments:** self, text
- **Docstring:** Convert text to speech using streaming synthesis...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.start_voice_input`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 103
- **Arguments:** self
- **Docstring:** Start voice recording and convert to text...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.stop_tts`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 148
- **Arguments:** self
- **Docstring:** Stop current TTS playback...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.stop_voice_input`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 112
- **Arguments:** self
- **Docstring:** Stop voice recording and process the audio...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.test_connection`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 269
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Test connection to voice process...

---

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.update_settings`

- **File:** `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`
- **Line:** 166
- **Arguments:** self, settings
- **Docstring:** Update voice service settings...

---

### `services\conversation_service.py.__init__`

- **File:** `services\conversation_service.py`
- **Line:** 19
- **Arguments:** self, history_dir, memory_service

---

### `services\conversation_service.py._add_to_memory`

- **File:** `services\conversation_service.py`
- **Line:** 48
- **Arguments:** self, role, content
- **Docstring:** Add message to memory service...

---

### `services\conversation_service.py.add_message`

- **File:** `services\conversation_service.py`
- **Line:** 32
- **Arguments:** self, role, content, message_id
- **Docstring:** Add a message to the conversation...

---

### `services\conversation_service.py.auto_save`

- **File:** `services\conversation_service.py`
- **Line:** 153
- **Arguments:** self
- **Docstring:** Auto-save the current conversation (overwrites last file)...

---

### `services\conversation_service.py.clear_conversation`

- **File:** `services\conversation_service.py`
- **Line:** 146
- **Arguments:** self
- **Docstring:** Clear the current conversation...

---

### `services\conversation_service.py.get_context_messages`

- **File:** `services\conversation_service.py`
- **Line:** 90
- **Arguments:** self
- **Docstring:** Get messages for context window, including relevant memories...

---

### `services\conversation_service.py.get_messages`

- **File:** `services\conversation_service.py`
- **Line:** 84
- **Arguments:** self
- **Docstring:** Get the current conversation messages...

---

### `services\conversation_service.py.load_conversation`

- **File:** `services\conversation_service.py`
- **Line:** 126
- **Arguments:** self, filename
- **Docstring:** Load a conversation from a file...

---

### `services\conversation_service.py.save_conversation`

- **File:** `services\conversation_service.py`
- **Line:** 97
- **Arguments:** self, filename
- **Returns:** str
- **Docstring:** Save the conversation to a file...

---

### `services\conversation_service.py.set_memory_service`

- **File:** `services\conversation_service.py`
- **Line:** 28
- **Arguments:** self, memory_service
- **Docstring:** Set the memory service for integration...

---

### `services\enhancement_service.py.__init__`

- **File:** `services\enhancement_service.py`
- **Line:** 11
- **Arguments:** self, ollama_service

---

### `services\enhancement_service.py.detect_follow_up_question`

- **File:** `services\enhancement_service.py`
- **Line:** 25
- **Arguments:** self, response
- **Docstring:** Detect a follow-up question in the response (placeholder logic)...

---

### `services\enhancement_service.py.generate_enhanced_response`

- **File:** `services\enhancement_service.py`
- **Line:** 34
- **Arguments:** self, original_response, context
- **Returns:** str
- **Docstring:** Generate an enhanced response (placeholder logic)...

---

### `services\enhancement_service.py.should_enhance_response`

- **File:** `services\enhancement_service.py`
- **Line:** 14
- **Arguments:** self, response
- **Returns:** bool
- **Docstring:** Determine if a response should be enhanced (placeholder logic)...

---

### `services\memory_service.py.__init__`

- **File:** `services\memory_service.py`
- **Line:** 445
- **Arguments:** self, max_context_messages

---

### `services\memory_service.py.__post_init__`

- **File:** `services\memory_service.py`
- **Line:** 47
- **Arguments:** self

---

### `services\memory_service.py._load`

- **File:** `services\memory_service.py`
- **Line:** 385
- **Arguments:** self
- **Docstring:** Load long-term memory from file...

---

### `services\memory_service.py._load_memory`

- **File:** `services\memory_service.py`
- **Line:** 470
- **Arguments:** self
- **Docstring:** Load memory from storage...

---

### `services\memory_service.py._on_embeddings_updated`

- **File:** `services\memory_service.py`
- **Line:** 486
- **Arguments:** self
- **Docstring:** Handle embeddings update...

---

### `services\memory_service.py._save`

- **File:** `services\memory_service.py`
- **Line:** 420
- **Arguments:** self
- **Docstring:** Save long-term memory to file...

---

### `services\memory_service.py._save_memory`

- **File:** `services\memory_service.py`
- **Line:** 478
- **Arguments:** self
- **Docstring:** Save memory to storage...

---

### `services\memory_service.py._verify_memory_files_cleared`

- **File:** `services\memory_service.py`
- **Line:** 763
- **Arguments:** self
- **Docstring:** Verify that memory files have been cleared...

---

### `services\memory_service.py.add_entry`

- **File:** `services\memory_service.py`
- **Line:** 400
- **Arguments:** self, entry
- **Docstring:** Add an entry to long-term memory...

---

### `services\memory_service.py.add_fact`

- **File:** `services\memory_service.py`
- **Line:** 854
- **Arguments:** self, key, value, importance, tags
- **Docstring:** Add a fact to long-term memory...

---

### `services\memory_service.py.add_memory`

- **File:** `services\memory_service.py`
- **Line:** 494
- **Arguments:** self, content, conversation_id, importance, tags, memory_type, metadata
- **Returns:** str
- **Docstring:** Add a memory entry...

---

### `services\memory_service.py.add_message`

- **File:** `services\memory_service.py`
- **Line:** 847
- **Arguments:** self, message
- **Docstring:** Add a message to memory (legacy method)...

---

### `services\memory_service.py.add_summary`

- **File:** `services\memory_service.py`
- **Line:** 525
- **Arguments:** self, summary, importance, tags
- **Docstring:** Add a conversation summary to memory...

---

### `services\memory_service.py.calculate_relevance`

- **File:** `services\memory_service.py`
- **Line:** 254
- **Arguments:** query, memory_entry
- **Returns:** float
- **Decorators:** staticmethod
- **Docstring:** Calculate relevance score between query and memory entry...

---

### `services\memory_service.py.classify_message`

- **File:** `services\memory_service.py`
- **Line:** 92
- **Arguments:** message, role
- **Returns:** Dict
- **Decorators:** staticmethod
- **Docstring:** Classify a message and determine its memory characteristics...

---

### `services\memory_service.py.cleanup_memory_entries`

- **File:** `services\memory_service.py`
- **Line:** 916
- **Arguments:** self
- **Docstring:** Clean up old or low-importance memory entries...

---

### `services\memory_service.py.clear`

- **File:** `services\memory_service.py`
- **Line:** 909
- **Arguments:** self
- **Docstring:** Clear all memory...

---

### `services\memory_service.py.clear_memory`

- **File:** `services\memory_service.py`
- **Line:** 738
- **Arguments:** self, memory_type
- **Docstring:** Clear memory entries...

---

### `services\memory_service.py.delete_memory`

- **File:** `services\memory_service.py`
- **Line:** 782
- **Arguments:** self, memory_id
- **Docstring:** Delete a specific memory entry...

---

### `services\memory_service.py.extract_facts_from_message`

- **File:** `services\memory_service.py`
- **Line:** 641
- **Arguments:** self, message
- **Docstring:** Extract facts from a message using LLM...

---

### `services\memory_service.py.get_context_messages`

- **File:** `services\memory_service.py`
- **Line:** 694
- **Arguments:** self, current_query
- **Docstring:** Get context messages for AI conversation...

---

### `services\memory_service.py.get_entries`

- **File:** `services\memory_service.py`
- **Line:** 410
- **Arguments:** self, type_filter
- **Docstring:** Get entries from long-term memory, optionally filtered by type...

---

### `services\memory_service.py.get_memory_stats`

- **File:** `services\memory_service.py`
- **Line:** 793
- **Arguments:** self
- **Returns:** Dict
- **Docstring:** Get memory statistics...

---

### `services\memory_service.py.get_messages`

- **File:** `services\memory_service.py`
- **Line:** 355
- **Arguments:** self
- **Docstring:** Get all messages in short-term memory...

---

### `services\memory_service.py.get_relevant_memories`

- **File:** `services\memory_service.py`
- **Line:** 543
- **Arguments:** self, query, limit, use_semantic
- **Docstring:** Get relevant memories for a query...

---

### `services\memory_service.py.get_user_info`

- **File:** `services\memory_service.py`
- **Line:** 670
- **Arguments:** self
- **Docstring:** Get user information from memory...

---

### `services\memory_service.py.get_user_name`

- **File:** `services\memory_service.py`
- **Line:** 685
- **Arguments:** self
- **Docstring:** Get the user's name from memory...

---

### `services\memory_service.py.intelligent_add_message`

- **File:** `services\memory_service.py`
- **Line:** 595
- **Arguments:** self, message
- **Returns:** Dict
- **Docstring:** Intelligently add a message to memory with classification...

---

### `services\memory_service.py.normalize_pronouns`

- **File:** `services\memory_service.py`
- **Line:** 191
- **Arguments:** text, user_name
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Convert first-person pronouns to third-person references to avoid AI confusion

Args:
    text: The ...

---

### `services\memory_service.py.search_memories`

- **File:** `services\memory_service.py`
- **Line:** 880
- **Arguments:** self, query, memory_type
- **Docstring:** Search memories with optional type filter...

---

### `services\memory_service.py.set_max_context_messages`

- **File:** `services\memory_service.py`
- **Line:** 871
- **Arguments:** self, max_messages
- **Docstring:** Set the maximum number of context messages...

---

### `services\memory_service.py.should_normalize`

- **File:** `services\memory_service.py`
- **Line:** 226
- **Arguments:** text
- **Returns:** bool
- **Decorators:** staticmethod
- **Docstring:** Check if text contains first-person pronouns that should be normalized...

---

### `services\memory_service.py.summarize_conversation`

- **File:** `services\memory_service.py`
- **Line:** 721
- **Arguments:** self, conversation_messages, conversation_id
- **Returns:** str
- **Docstring:** Summarize a conversation...

---

### `services\memory_service.py.update_access_stats`

- **File:** `services\memory_service.py`
- **Line:** 430
- **Arguments:** self, entry
- **Docstring:** Update access statistics for a memory entry...

---

### `services\ollama_service.py.__init__`

- **File:** `services\ollama_service.py`
- **Line:** 30
- **Arguments:** self, base_url

---

### `services\ollama_service.py._build_session_commands`

- **File:** `services\ollama_service.py`
- **Line:** 372
- **Arguments:** self, session_variables
- **Docstring:** Build session commands from variables...

---

### `services\ollama_service.py._extract_system_prompt`

- **File:** `services\ollama_service.py`
- **Line:** 363
- **Arguments:** self, messages
- **Returns:** str
- **Docstring:** Extract system prompt from messages...

---

### `services\ollama_service.py._pull_model_thread`

- **File:** `services\ollama_service.py`
- **Line:** 231
- **Arguments:** self, model_name
- **Docstring:** Background thread for pulling models...

---

### `services\ollama_service.py._remove_model_thread`

- **File:** `services\ollama_service.py`
- **Line:** 279
- **Arguments:** self, model_name
- **Docstring:** Background thread for removing models...

---

### `services\ollama_service.py._update_model_thread`

- **File:** `services\ollama_service.py`
- **Line:** 327
- **Arguments:** self, model_name
- **Docstring:** Background thread for updating models...

---

### `services\ollama_service.py.cancel_request`

- **File:** `services\ollama_service.py`
- **Line:** 388
- **Arguments:** self
- **Docstring:** Cancel the current request...

---

### `services\ollama_service.py.get_models`

- **File:** `services\ollama_service.py`
- **Line:** 41
- **Arguments:** self
- **Docstring:** Get list of available models from Ollama...

---

### `services\ollama_service.py.is_connected`

- **File:** `services\ollama_service.py`
- **Line:** 404
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Ollama is connected...

---

### `services\ollama_service.py.pull_model`

- **File:** `services\ollama_service.py`
- **Line:** 219
- **Arguments:** self, model_name
- **Docstring:** Pull a model from Ollama...

---

### `services\ollama_service.py.remove_model`

- **File:** `services\ollama_service.py`
- **Line:** 267
- **Arguments:** self, model_name
- **Docstring:** Remove a model from Ollama...

---

### `services\ollama_service.py.reset_cancellation`

- **File:** `services\ollama_service.py`
- **Line:** 396
- **Arguments:** self
- **Docstring:** Reset the cancellation flag...

---

### `services\ollama_service.py.send_chat_message`

- **File:** `services\ollama_service.py`
- **Line:** 102
- **Arguments:** self, model, messages, temperature, stream, session_variables
- **Docstring:** Send a chat message to Ollama and yield streaming responses.

Args:
    model: The model to use
    ...

---

### `services\ollama_service.py.test_connection`

- **File:** `services\ollama_service.py`
- **Line:** 90
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Test if Ollama is running and accessible without emitting signals...

---

### `services\ollama_service.py.update_model`

- **File:** `services\ollama_service.py`
- **Line:** 315
- **Arguments:** self, model_name
- **Docstring:** Update a model from Ollama...

---

### `services\semantic_search_service.py.__init__`

- **File:** `services\semantic_search_service.py`
- **Line:** 38
- **Arguments:** self, model_name, cache_dir

---

### `services\semantic_search_service.py._init_model`

- **File:** `services\semantic_search_service.py`
- **Line:** 56
- **Arguments:** self
- **Docstring:** Initialize the sentence transformer model...

---

### `services\semantic_search_service.py._load_embeddings`

- **File:** `services\semantic_search_service.py`
- **Line:** 70
- **Arguments:** self
- **Docstring:** Load existing embeddings from cache...

---

### `services\semantic_search_service.py._save_embeddings`

- **File:** `services\semantic_search_service.py`
- **Line:** 104
- **Arguments:** self
- **Docstring:** Save embeddings to cache...

---

### `services\semantic_search_service.py.add_memory`

- **File:** `services\semantic_search_service.py`
- **Line:** 138
- **Arguments:** self, memory_id, content, memory_type, importance, tags, metadata
- **Returns:** bool
- **Docstring:** Add a new memory with vector embedding...

---

### `services\semantic_search_service.py.clear_all`

- **File:** `services\semantic_search_service.py`
- **Line:** 427
- **Arguments:** self
- **Docstring:** Clear all memories and embeddings...

---

### `services\semantic_search_service.py.get_memory_stats`

- **File:** `services\semantic_search_service.py`
- **Line:** 380
- **Arguments:** self
- **Returns:** Dict
- **Docstring:** Get statistics about the semantic search service...

---

### `services\semantic_search_service.py.is_ready`

- **File:** `services\semantic_search_service.py`
- **Line:** 454
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if the semantic search service is ready...

---

### `services\semantic_search_service.py.remove_memory`

- **File:** `services\semantic_search_service.py`
- **Line:** 192
- **Arguments:** self, memory_id
- **Returns:** bool
- **Docstring:** Remove a memory and its embedding...

---

### `services\semantic_search_service.py.search_hybrid`

- **File:** `services\semantic_search_service.py`
- **Line:** 274
- **Arguments:** self, query, max_results, min_similarity, memory_types, keyword_weight, semantic_weight
- **Docstring:** Search memories using both semantic and keyword matching...

---

### `services\semantic_search_service.py.search_semantic`

- **File:** `services\semantic_search_service.py`
- **Line:** 221
- **Arguments:** self, query, max_results, min_similarity, memory_types
- **Docstring:** Search memories using semantic similarity...

---

### `services\semantic_search_service.py.update_memory_importance`

- **File:** `services\semantic_search_service.py`
- **Line:** 353
- **Arguments:** self, memory_id, new_importance
- **Returns:** bool
- **Docstring:** Update the importance of a memory...

---

### `services\start_up\dependency_checker.py.__init__`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 19
- **Arguments:** self

---

### `services\start_up\dependency_checker.py.check_and_install_dependencies`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 206
- **Arguments:** auto_install, verbose
- **Returns:** bool
- **Docstring:** Check dependencies and optionally install missing ones.

Args:
    auto_install: If True, automatica...

---

### `services\start_up\dependency_checker.py.check_core_dependencies`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 41
- **Arguments:** self
- **Docstring:** Check core application dependencies....

---

### `services\start_up\dependency_checker.py.check_ml_dependencies`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 82
- **Arguments:** self
- **Docstring:** Check machine learning dependencies (all optional)....

---

### `services\start_up\dependency_checker.py.check_package_versions`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 117
- **Arguments:** self
- **Docstring:** Check for version conflicts....

---

### `services\start_up\dependency_checker.py.check_tts_options`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 101
- **Arguments:** self
- **Docstring:** Check if at least one TTS option is available....

---

### `services\start_up\dependency_checker.py.get_dependency_summary`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 198
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get a concise summary of dependency status....

---

### `services\start_up\dependency_checker.py.get_missing_dependencies`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 165
- **Arguments:** self
- **Docstring:** Get list of missing dependencies....

---

### `services\start_up\dependency_checker.py.get_version_conflicts`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 169
- **Arguments:** self
- **Docstring:** Get list of version conflicts....

---

### `services\start_up\dependency_checker.py.run_comprehensive_check`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 154
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Run the complete dependency check and return if fixes are needed....

---

### `services\start_up\dependency_checker.py.run_install_dependencies`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 173
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Run the install_dependencies.py script....

---

### `services\start_up\dependency_checker.py.test_import`

- **File:** `services\start_up\dependency_checker.py`
- **Line:** 25
- **Arguments:** self, module_name, description
- **Docstring:** Test if a module can be imported successfully and return version....

---

### `services\start_up\install_dependencies.py.__init__`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 26
- **Arguments:** self

---

### `services\start_up\install_dependencies.py.check_python_version`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 194
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if Python version is compatible....

---

### `services\start_up\install_dependencies.py.check_virtual_environment`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 203
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if running in a virtual environment....

---

### `services\start_up\install_dependencies.py.get_version`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 401
- **Arguments:** module_name
- **Docstring:** Get version of a module....

---

### `services\start_up\install_dependencies.py.install_all`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 553
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Run the complete installation process....

---

### `services\start_up\install_dependencies.py.main`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 592
- **Arguments:** 
- **Docstring:** Main entry point....

---

### `services\start_up\install_dependencies.py.print_header`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 187
- **Arguments:** self
- **Docstring:** Print installation header....

---

### `services\start_up\install_dependencies.py.print_summary`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 475
- **Arguments:** self
- **Docstring:** Print installation summary....

---

### `services\start_up\install_dependencies.py.run_stage`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 275
- **Arguments:** self, stage, stage_num, total_stages
- **Returns:** bool
- **Docstring:** Run a single installation stage....

---

### `services\start_up\install_dependencies.py.setup_spellchecker`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 229
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Set up spellchecker with dictionary verification....

---

### `services\start_up\install_dependencies.py.upgrade_pip`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 213
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Upgrade pip to latest version....

---

### `services\start_up\install_dependencies.py.verify_installation`

- **File:** `services\start_up\install_dependencies.py`
- **Line:** 396
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Verify that key packages can be imported....

---

### `services\summarization_service.py.__init__`

- **File:** `services\summarization_service.py`
- **Line:** 22
- **Arguments:** self, ollama_service

---

### `services\summarization_service.py._ai_evaluate_conversation_quality`

- **File:** `services\summarization_service.py`
- **Line:** 232
- **Arguments:** self, user_messages
- **Returns:** bool
- **Docstring:** Use AI to evaluate if a conversation has enough substance for naming

Args:
    user_messages: List ...

---

### `services\summarization_service.py._ai_evaluate_name_quality`

- **File:** `services\summarization_service.py`
- **Line:** 337
- **Arguments:** self, name
- **Returns:** bool
- **Docstring:** Use AI to evaluate if a generated name is suitable

Args:
    name: The generated name to evaluate
 ...

---

### `services\summarization_service.py._clean_generated_name`

- **File:** `services\summarization_service.py`
- **Line:** 142
- **Arguments:** self, response
- **Docstring:** Clean and validate the generated name...

---

### `services\summarization_service.py._create_summarization_prompt`

- **File:** `services\summarization_service.py`
- **Line:** 117
- **Arguments:** self, user_messages
- **Returns:** str
- **Docstring:** Create a prompt for generating a concise chat name...

---

### `services\summarization_service.py._fallback_quality_check`

- **File:** `services\summarization_service.py`
- **Line:** 308
- **Arguments:** self, user_messages
- **Returns:** bool
- **Docstring:** Fallback quality check if AI evaluation fails

Args:
    user_messages: List of user messages
    
R...

---

### `services\summarization_service.py._has_enough_substance`

- **File:** `services\summarization_service.py`
- **Line:** 215
- **Arguments:** self, user_messages
- **Returns:** bool
- **Docstring:** Check if the conversation has enough substance for meaningful naming
Uses AI to evaluate conversatio...

---

### `services\summarization_service.py.generate_chat_name`

- **File:** `services\summarization_service.py`
- **Line:** 28
- **Arguments:** self, conversation, filepath
- **Docstring:** Generate an AI-powered name for a conversation

Args:
    conversation: List of conversation message...

---

### `services\summarization_service.py.set_min_messages_threshold`

- **File:** `services\summarization_service.py`
- **Line:** 413
- **Arguments:** self, threshold
- **Docstring:** Set the minimum number of messages required for summarization...

---

### `services\summarization_service.py.set_summarization_model`

- **File:** `services\summarization_service.py`
- **Line:** 409
- **Arguments:** self, model
- **Docstring:** Set the model to use for summarization...

---

### `services\worker\worker.py.__init__`

- **File:** `services\worker\worker.py`
- **Line:** 16
- **Arguments:** self, parent

---

### `services\worker\worker.py._log_thread_info`

- **File:** `services\worker\worker.py`
- **Line:** 28
- **Arguments:** self, action
- **Docstring:** Log thread information for debugging...

---

### `services\worker\worker.py.get_stats`

- **File:** `services\worker\worker.py`
- **Line:** 197
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get worker statistics for debugging...

---

### `services\worker\worker.py.is_running`

- **File:** `services\worker\worker.py`
- **Line:** 88
- **Arguments:** self
- **Docstring:** Check if the worker is currently running....

---

### `services\worker\worker.py.run`

- **File:** `services\worker\worker.py`
- **Line:** 35
- **Arguments:** self, message
- **Docstring:** Run the worker task....

---

### `services\worker\worker.py.run_stream`

- **File:** `services\worker\worker.py`
- **Line:** 94
- **Arguments:** self, messages, model, temperature, ollama_url, max_tokens, top_p, frequency_penalty, presence_penalty

---

### `services\worker\worker.py.stop`

- **File:** `services\worker\worker.py`
- **Line:** 66
- **Arguments:** self
- **Docstring:** Stop the worker safely....

---

### `ui\Audio_visualisers\eq_orchestrator.py.__init__`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 152
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py._play_audio_thread`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 445
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py._play_file_audio`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 486
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py._play_microphone_audio`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 451
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py._process_audio_chunk`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 516
- **Arguments:** self, chunk, samplerate
- **Docstring:** Process audio chunk and update appropriate visualizer based on current mode....

---

### `ui\Audio_visualisers\eq_orchestrator.py._reset_visualizers`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 582
- **Arguments:** self
- **Docstring:** Reset all visualizers to idle state....

---

### `ui\Audio_visualisers\eq_orchestrator.py.auto_select_microphone`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 615
- **Arguments:** self
- **Docstring:** Auto-select the first available microphone device....

---

### `ui\Audio_visualisers\eq_orchestrator.py.band_energy`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 122
- **Arguments:** mag, sr, n_points, f_lo, f_hi
- **Docstring:** Calculate energy for a specific frequency band....

---

### `ui\Audio_visualisers\eq_orchestrator.py.callback`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 493
- **Arguments:** outdata, frames, time, status

---

### `ui\Audio_visualisers\eq_orchestrator.py.load_audio_preset`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 371
- **Arguments:** self, file_path, preset_name
- **Docstring:** Load an audio file from a preset....

---

### `ui\Audio_visualisers\eq_orchestrator.py.map_frequency_to_bars`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 54
- **Arguments:** fft_magnitude, sample_rate, num_bars
- **Docstring:** Map FFT frequency bins to bar ranges based on frequency bands.

Args:
    fft_magnitude: FFT magnitu...

---

### `ui\Audio_visualisers\eq_orchestrator.py.on_device_selected`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 434
- **Arguments:** self, idx

---

### `ui\Audio_visualisers\eq_orchestrator.py.play_audio`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 388
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py.populate_device_list`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 598
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py.print_sound_devices`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 647
- **Arguments:** 

---

### `ui\Audio_visualisers\eq_orchestrator.py.refresh_device_list`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 607
- **Arguments:** self
- **Docstring:** Refresh the device list and repopulate the dropdown....

---

### `ui\Audio_visualisers\eq_orchestrator.py.resizeEvent`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 620
- **Arguments:** self, event

---

### `ui\Audio_visualisers\eq_orchestrator.py.select_audio_file`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 363
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py.stop_audio`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 399
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py.switch_mode`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 305
- **Arguments:** self, idx

---

### `ui\Audio_visualisers\eq_orchestrator.py.toggle_mute`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 414
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_orchestrator.py.toggle_system_audio`

- **File:** `ui\Audio_visualisers\eq_orchestrator.py`
- **Line:** 418
- **Arguments:** self, state

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 25
- **Arguments:** self, parent, num_bars
- **Docstring:** Initialize the bar equalizer widget.

Args:
    parent: Parent widget
    num_bars: Number of freque...

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py._animate`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 55
- **Arguments:** self
- **Docstring:** Animate the bars by smoothly interpolating current values toward target values.
This method is calle...

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py._calculate_bar_geometry`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 131
- **Arguments:** self, widget_width, widget_height
- **Docstring:** Calculate bar dimensions and positioning.

Args:
    widget_width: Width of the widget
    widget_he...

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py._create_bar_gradient`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 154
- **Arguments:** self, x, y, width, height, is_reflection, bar_index
- **Docstring:** Create a gradient for a bar.

Args:
    x: X position of the bar
    y: Y position of the bar
    wi...

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py._draw_bar`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 208
- **Arguments:** self, painter, x, y, width, height, value, max_height, bar_index
- **Docstring:** Draw a single bar with its reflection.

Args:
    painter: QPainter instance
    x: X position of th...

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py._setup_animation_timer`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 49
- **Arguments:** self
- **Docstring:** Initialize and configure the animation timer....

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.get_current_values`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 117
- **Arguments:** self
- **Docstring:** Get current bar values for debugging/monitoring.

Returns:
    dict: Current state information...

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.paintEvent`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 237
- **Arguments:** self, event
- **Docstring:** Paint the bar equalizer widget.

Args:
    event: Paint event...

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.set_eq_bars`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 68
- **Arguments:** self, values
- **Decorators:** Slot
- **Docstring:** Set the target values for the frequency bars.

Args:
    values: List of float values representing t...

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.set_idle`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 104
- **Arguments:** self
- **Docstring:** Reset all bars to their idle state....

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.start_animation`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 109
- **Arguments:** self
- **Docstring:** Start the animation timer....

---

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.stop_animation`

- **File:** `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`
- **Line:** 113
- **Arguments:** self
- **Docstring:** Stop the animation timer....

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 24
- **Arguments:** self, parent, num_sections
- **Docstring:** Initialize the circular equalizer widget.

Args:
    parent: Parent widget
    num_sections: Number ...

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py._animate`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 54
- **Arguments:** self
- **Docstring:** Animate the sections by smoothly interpolating current values toward target values.
This method is c...

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py._create_section_gradient`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 131
- **Arguments:** self, center_x, center_y, inner_radius, outer_radius, angle_start, angle_span, value, section_index
- **Docstring:** Create a gradient for a circular section.

Args:
    center_x, center_y: Center of the circle
    in...

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py._setup_animation_timer`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 48
- **Arguments:** self
- **Docstring:** Initialize and configure the animation timer....

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.get_current_values`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 117
- **Arguments:** self
- **Docstring:** Get current section values for debugging/monitoring.

Returns:
    dict: Current state information...

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.paintEvent`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 171
- **Arguments:** self, event
- **Docstring:** Paint the circular equalizer widget.

Args:
    event: Paint event...

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.set_eq_sections`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 68
- **Arguments:** self, values
- **Decorators:** Slot
- **Docstring:** Set the target values for the circular sections.

Args:
    values: List of float values representin...

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.set_idle`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 104
- **Arguments:** self
- **Docstring:** Reset all sections to their idle state....

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.start_animation`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 109
- **Arguments:** self
- **Docstring:** Start the animation timer....

---

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.stop_animation`

- **File:** `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`
- **Line:** 113
- **Arguments:** self
- **Docstring:** Stop the animation timer....

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 17
- **Arguments:** self, parent, num_points, color, alpha, radius_scale, radius_ratio, energy_mult

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py._animate`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 49
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py._smooth_radii`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 41
- **Arguments:** self, radii, window

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.paintEvent`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 89
- **Arguments:** self, event

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.set_idle`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 77
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.set_net_radii`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 58
- **Arguments:** self, values
- **Decorators:** Slot

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.start_animation`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 83
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.stop_animation`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`
- **Line:** 86
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`
- **Line:** 20
- **Arguments:** self, parent, num_points, color

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py._animate`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`
- **Line:** 41
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.paintEvent`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`
- **Line:** 80
- **Arguments:** self, event

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.set_idle`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`
- **Line:** 70
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.set_net_radii`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`
- **Line:** 51
- **Arguments:** self, values
- **Decorators:** Slot

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.start_animation`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`
- **Line:** 74
- **Arguments:** self

---

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.stop_animation`

- **File:** `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`
- **Line:** 77
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.__init__`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 850
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py._animate`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 752
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py._calculate_bar_geometry`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 451
- **Arguments:** self, widget_width, widget_height
- **Docstring:** Calculate bar dimensions and positioning.

Args:
    widget_width: Width of the widget
    widget_he...

---

### `ui\Audio_visualisers\voice_ring_animation.py._create_bar_gradient`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 474
- **Arguments:** self, x, y, width, height, is_reflection, bar_index
- **Docstring:** Create a gradient for a bar.

Args:
    x: X position of the bar
    y: Y position of the bar
    wi...

---

### `ui\Audio_visualisers\voice_ring_animation.py._create_section_gradient`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 242
- **Arguments:** self, center_x, center_y, inner_radius, outer_radius, angle_start, angle_span, value, section_index
- **Docstring:** Create a gradient for a circular section.

Args:
    center_x, center_y: Center of the circle
    in...

---

### `ui\Audio_visualisers\voice_ring_animation.py._draw_bar`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 528
- **Arguments:** self, painter, x, y, width, height, value, max_height, bar_index
- **Docstring:** Draw a single bar with its reflection.

Args:
    painter: QPainter instance
    x: X position of th...

---

### `ui\Audio_visualisers\voice_ring_animation.py._play_audio_thread`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1195
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py._setup_animation_timer`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 369
- **Arguments:** self
- **Docstring:** Initialize and configure the animation timer....

---

### `ui\Audio_visualisers\voice_ring_animation.py._smooth_radii`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 744
- **Arguments:** self, radii, window

---

### `ui\Audio_visualisers\voice_ring_animation.py.auto_select_microphone`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1595
- **Arguments:** self
- **Docstring:** Auto-select the first available microphone device....

---

### `ui\Audio_visualisers\voice_ring_animation.py.band_energy`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1328
- **Arguments:** mag, sr, n_points, f_lo, f_hi

---

### `ui\Audio_visualisers\voice_ring_animation.py.callback`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1376
- **Arguments:** outdata, frames, time, status

---

### `ui\Audio_visualisers\voice_ring_animation.py.get_current_values`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 437
- **Arguments:** self
- **Docstring:** Get current bar values for debugging/monitoring.

Returns:
    dict: Current state information...

---

### `ui\Audio_visualisers\voice_ring_animation.py.load_audio_preset`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1101
- **Arguments:** self, file_path, preset_name
- **Docstring:** Load an audio file from a preset.

Args:
    file_path: Path to the audio file
    preset_name: Name...

---

### `ui\Audio_visualisers\voice_ring_animation.py.map_frequency_to_bars`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 49
- **Arguments:** fft_magnitude, sample_rate, num_bars
- **Docstring:** Map FFT frequency bins to bar ranges based on frequency bands.

Args:
    fft_magnitude: FFT magnitu...

---

### `ui\Audio_visualisers\voice_ring_animation.py.on_device_selected`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1183
- **Arguments:** self, idx

---

### `ui\Audio_visualisers\voice_ring_animation.py.paintEvent`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 791
- **Arguments:** self, event

---

### `ui\Audio_visualisers\voice_ring_animation.py.play_audio`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1124
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.populate_device_list`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1574
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.print_sound_devices`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1625
- **Arguments:** 

---

### `ui\Audio_visualisers\voice_ring_animation.py.refresh_device_list`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1585
- **Arguments:** self
- **Docstring:** Refresh the device list and repopulate the dropdown....

---

### `ui\Audio_visualisers\voice_ring_animation.py.resizeEvent`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1600
- **Arguments:** self, event

---

### `ui\Audio_visualisers\voice_ring_animation.py.select_audio_file`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1093
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.set_eq_bars`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 388
- **Arguments:** self, values
- **Decorators:** Slot
- **Docstring:** Set the target values for the frequency bars.

Args:
    values: List of float values representing t...

---

### `ui\Audio_visualisers\voice_ring_animation.py.set_eq_sections`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 179
- **Arguments:** self, values
- **Decorators:** Slot
- **Docstring:** Set the target values for the circular sections.

Args:
    values: List of float values representin...

---

### `ui\Audio_visualisers\voice_ring_animation.py.set_idle`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 780
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.set_net_radii`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 761
- **Arguments:** self, values
- **Decorators:** Slot

---

### `ui\Audio_visualisers\voice_ring_animation.py.start_animation`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 786
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.stop_animation`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 788
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.stop_audio`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1135
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.switch_mode`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 992
- **Arguments:** self, idx

---

### `ui\Audio_visualisers\voice_ring_animation.py.toggle_mute`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1162
- **Arguments:** self

---

### `ui\Audio_visualisers\voice_ring_animation.py.toggle_system_audio`

- **File:** `ui\Audio_visualisers\voice_ring_animation.py`
- **Line:** 1166
- **Arguments:** self, state

---

### `ui\Widgets\chat_navigation.py.__init__`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 29
- **Arguments:** self, conversation_manager, summarization_service, parent

---

### `ui\Widgets\chat_navigation.py.clear_all_conversations`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 336
- **Arguments:** self
- **Docstring:** Delete all conversations after confirmation...

---

### `ui\Widgets\chat_navigation.py.create_conversation_item`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 196
- **Arguments:** self, filepath, metadata
- **Returns:** QListWidgetItem
- **Docstring:** Create a list item for a conversation...

---

### `ui\Widgets\chat_navigation.py.delete_conversation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 297
- **Arguments:** self, filepath
- **Docstring:** Delete a conversation...

---

### `ui\Widgets\chat_navigation.py.get_selected_conversation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 329
- **Arguments:** self
- **Docstring:** Get the currently selected conversation filepath...

---

### `ui\Widgets\chat_navigation.py.on_conversation_double_clicked`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 217
- **Arguments:** self, item
- **Docstring:** Handle double-click on conversation item...

---

### `ui\Widgets\chat_navigation.py.on_summarization_completed`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 391
- **Arguments:** self, filepath, generated_name
- **Docstring:** Handle successful summarization...

---

### `ui\Widgets\chat_navigation.py.on_summarization_failed`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 417
- **Arguments:** self, filepath, error_message
- **Docstring:** Handle summarization failure...

---

### `ui\Widgets\chat_navigation.py.refresh_conversations`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 166
- **Arguments:** self
- **Docstring:** Refresh the list of conversations...

---

### `ui\Widgets\chat_navigation.py.rename_conversation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 260
- **Arguments:** self, filepath
- **Docstring:** Rename a conversation file...

---

### `ui\Widgets\chat_navigation.py.set_current_conversation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 324
- **Arguments:** self, filepath
- **Docstring:** Set the currently active conversation...

---

### `ui\Widgets\chat_navigation.py.setup_connections`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 154
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\Widgets\chat_navigation.py.setup_ui`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 40
- **Arguments:** self
- **Docstring:** Setup the navigation UI...

---

### `ui\Widgets\chat_navigation.py.show_context_menu`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 223
- **Arguments:** self, position
- **Docstring:** Show context menu for conversation items...

---

### `ui\Widgets\chat_navigation.py.trigger_name_generation`

- **File:** `ui\Widgets\chat_navigation.py`
- **Line:** 359
- **Arguments:** self, filepath
- **Docstring:** Trigger AI name generation for a conversation...

---

### `ui\Widgets\coqui_model_dialog.py.__init__`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 54
- **Arguments:** self, parent

---

### `ui\Widgets\coqui_model_dialog.py.accept_selection`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 390
- **Arguments:** self
- **Docstring:** Accept the current model and speaker selection...

---

### `ui\Widgets\coqui_model_dialog.py.create_model_panel`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 199
- **Arguments:** self
- **Docstring:** Create the model selection panel...

---

### `ui\Widgets\coqui_model_dialog.py.create_speaker_panel`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 228
- **Arguments:** self
- **Docstring:** Create the speaker selection panel...

---

### `ui\Widgets\coqui_model_dialog.py.download_selected_model`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 340
- **Arguments:** self
- **Docstring:** Download the selected model...

---

### `ui\Widgets\coqui_model_dialog.py.get_current_time`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 406
- **Arguments:** self
- **Docstring:** Get current time string...

---

### `ui\Widgets\coqui_model_dialog.py.load_models`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 251
- **Arguments:** self
- **Docstring:** Load available Coqui TTS models...

---

### `ui\Widgets\coqui_model_dialog.py.load_speakers_for_model`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 301
- **Arguments:** self, model_name
- **Docstring:** Load available speakers for the selected model...

---

### `ui\Widgets\coqui_model_dialog.py.log_status`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 398
- **Arguments:** self, message
- **Docstring:** Log a status message...

---

### `ui\Widgets\coqui_model_dialog.py.on_download_completed`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 368
- **Arguments:** self, success, message
- **Docstring:** Handle download completion...

---

### `ui\Widgets\coqui_model_dialog.py.on_model_selected`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 280
- **Arguments:** self, item
- **Docstring:** Handle model selection...

---

### `ui\Widgets\coqui_model_dialog.py.on_speaker_selected`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 334
- **Arguments:** self, item
- **Docstring:** Handle speaker selection...

---

### `ui\Widgets\coqui_model_dialog.py.run`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 30
- **Arguments:** self

---

### `ui\Widgets\coqui_model_dialog.py.setup_ui`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 70
- **Arguments:** self
- **Docstring:** Setup the dialog UI...

---

### `ui\Widgets\coqui_model_dialog.py.start_download`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 356
- **Arguments:** self, model_name
- **Docstring:** Start downloading a model...

---

### `ui\Widgets\coqui_model_dialog.py.update_selection_button`

- **File:** `ui\Widgets\coqui_model_dialog.py`
- **Line:** 383
- **Arguments:** self
- **Docstring:** Update the selection button state...

---

### `ui\Widgets\editable_message_widget.py.__init__`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 21
- **Arguments:** self, content, message_id, parent

---

### `ui\Widgets\editable_message_widget.py.cancel_edit`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 191
- **Arguments:** self
- **Docstring:** Cancel editing and revert to original content...

---

### `ui\Widgets\editable_message_widget.py.finish_editing`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 196
- **Arguments:** self
- **Docstring:** Finish editing mode...

---

### `ui\Widgets\editable_message_widget.py.get_content`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 202
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the current message content...

---

### `ui\Widgets\editable_message_widget.py.save_edit`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 181
- **Arguments:** self
- **Docstring:** Save the edited message...

---

### `ui\Widgets\editable_message_widget.py.set_content`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 206
- **Arguments:** self, content
- **Docstring:** Set the message content...

---

### `ui\Widgets\editable_message_widget.py.setup_styles`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 93
- **Arguments:** self
- **Docstring:** Setup widget styles...

---

### `ui\Widgets\editable_message_widget.py.setup_ui`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 31
- **Arguments:** self
- **Docstring:** Setup the widget UI...

---

### `ui\Widgets\editable_message_widget.py.start_editing`

- **File:** `ui\Widgets\editable_message_widget.py`
- **Line:** 172
- **Arguments:** self
- **Docstring:** Start editing the message...

---

### `ui\Widgets\personality_widget.py.__init__`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 19
- **Arguments:** self, parent

---

### `ui\Widgets\personality_widget.py.clear_creation_form`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 514
- **Arguments:** self
- **Docstring:** Clear the personality creation form...

---

### `ui\Widgets\personality_widget.py.create_personality`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 447
- **Arguments:** self
- **Docstring:** Create a new custom personality...

---

### `ui\Widgets\personality_widget.py.delete_custom_personality`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 552
- **Arguments:** self
- **Docstring:** Delete the selected custom personality...

---

### `ui\Widgets\personality_widget.py.export_personality`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 572
- **Arguments:** self
- **Docstring:** Export the selected personality (placeholder for future implementation)...

---

### `ui\Widgets\personality_widget.py.get_available_personalities`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 595
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get list of available personality names...

---

### `ui\Widgets\personality_widget.py.get_comprehensive_system_prompt`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 599
- **Arguments:** self, memory_service, is_new_conversation
- **Returns:** str
- **Docstring:** Get a comprehensive system prompt that includes all personality components and user information from...

---

### `ui\Widgets\personality_widget.py.get_current_personality`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 581
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality name...

---

### `ui\Widgets\personality_widget.py.get_formatted_prompt`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 587
- **Arguments:** self, user_input, context
- **Returns:** str
- **Docstring:** Get a formatted prompt using the current personality...

---

### `ui\Widgets\personality_widget.py.get_system_prompt`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 591
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the system prompt for the current personality...

---

### `ui\Widgets\personality_widget.py.get_user_context_messages`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 604
- **Arguments:** self, memory_service, is_new_conversation
- **Docstring:** Get dynamic user context messages that should be added to conversation...

---

### `ui\Widgets\personality_widget.py.load_personalities`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 319
- **Arguments:** self
- **Docstring:** Load available personalities into the combo box...

---

### `ui\Widgets\personality_widget.py.on_custom_personality_selected`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 545
- **Arguments:** self, item
- **Docstring:** Handle custom personality selection in management tab...

---

### `ui\Widgets\personality_widget.py.on_personality_changed`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 622
- **Arguments:** self, personality_name
- **Docstring:** Handle personality selection change...

---

### `ui\Widgets\personality_widget.py.refresh_personalities`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 608
- **Arguments:** self
- **Docstring:** Refresh personalities from disk...

---

### `ui\Widgets\personality_widget.py.set_personality`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 370
- **Arguments:** self, personality_name
- **Docstring:** Set a specific personality...

---

### `ui\Widgets\personality_widget.py.setup_creation_tab`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 91
- **Arguments:** self
- **Docstring:** Setup the personality creation tab...

---

### `ui\Widgets\personality_widget.py.setup_management_tab`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 281
- **Arguments:** self
- **Docstring:** Setup the personality management tab...

---

### `ui\Widgets\personality_widget.py.setup_selection_tab`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 55
- **Arguments:** self
- **Docstring:** Setup the personality selection tab...

---

### `ui\Widgets\personality_widget.py.setup_ui`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 25
- **Arguments:** self
- **Docstring:** Setup the user interface...

---

### `ui\Widgets\personality_widget.py.update_personality_info`

- **File:** `ui\Widgets\personality_widget.py`
- **Line:** 380
- **Arguments:** self, personality_name
- **Docstring:** Update the personality info display...

---

### `ui\Widgets\settings_dialog.py.__init__`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 14
- **Arguments:** self, config_manager, available_models, available_personalities, parent

---

### `ui\Widgets\settings_dialog.py._delayed_load_settings`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 238
- **Arguments:** self
- **Docstring:** Load settings after UI is fully ready...

---

### `ui\Widgets\settings_dialog.py.create_chat_tab`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 133
- **Arguments:** self
- **Docstring:** Create the chat settings tab...

---

### `ui\Widgets\settings_dialog.py.create_developer_tab`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 220
- **Arguments:** self

---

### `ui\Widgets\settings_dialog.py.create_general_tab`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 69
- **Arguments:** self
- **Docstring:** Create the general settings tab...

---

### `ui\Widgets\settings_dialog.py.create_session_tab`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 180
- **Arguments:** self
- **Docstring:** Create the session variables tab...

---

### `ui\Widgets\settings_dialog.py.load_current_settings`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 243
- **Arguments:** self
- **Docstring:** Load current settings into the UI...

---

### `ui\Widgets\settings_dialog.py.reset_to_defaults`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 352
- **Arguments:** self
- **Docstring:** Reset all settings to defaults...

---

### `ui\Widgets\settings_dialog.py.save_settings`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 302
- **Arguments:** self
- **Docstring:** Save the current settings...

---

### `ui\Widgets\settings_dialog.py.setup_ui`

- **File:** `ui\Widgets\settings_dialog.py`
- **Line:** 25
- **Arguments:** self
- **Docstring:** Setup the user interface...

---

### `ui\Widgets\spellchecker_widget.py.__init__`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 26
- **Arguments:** self, parent

---

### `ui\Widgets\spellchecker_widget.py.add_to_dictionary`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 112
- **Arguments:** self, word
- **Docstring:** Add word to personal dictionary...

---

### `ui\Widgets\spellchecker_widget.py.cleanup`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 208
- **Arguments:** self
- **Docstring:** Clean up resources...

---

### `ui\Widgets\spellchecker_widget.py.disable_spellcheck`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 196
- **Arguments:** self
- **Docstring:** Disable spell checking by clearing highlights...

---

### `ui\Widgets\spellchecker_widget.py.enable_spellcheck`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 189
- **Arguments:** self
- **Docstring:** Enable spell checking...

---

### `ui\Widgets\spellchecker_widget.py.highlight_misspelled_words`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 127
- **Arguments:** self
- **Docstring:** Highlight misspelled words in the text...

---

### `ui\Widgets\spellchecker_widget.py.ignore_word`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 123
- **Arguments:** self, word
- **Docstring:** Ignore the word (add to personal dictionary)...

---

### `ui\Widgets\spellchecker_widget.py.keyPressEvent`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 172
- **Arguments:** self, event
- **Docstring:** Override key press event to check spelling on space/enter...

---

### `ui\Widgets\spellchecker_widget.py.on_text_changed`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 182
- **Arguments:** self
- **Docstring:** Handle text changes for spell checking...

---

### `ui\Widgets\spellchecker_widget.py.replace_word`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 102
- **Arguments:** self, cursor, new_word
- **Docstring:** Replace the misspelled word with the suggestion...

---

### `ui\Widgets\spellchecker_widget.py.setup_context_menu`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 53
- **Arguments:** self
- **Docstring:** Setup context menu for spell checking...

---

### `ui\Widgets\spellchecker_widget.py.setup_spellchecker`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 36
- **Arguments:** self
- **Docstring:** Initialize the spellchecker...

---

### `ui\Widgets\spellchecker_widget.py.show_context_menu`

- **File:** `ui\Widgets\spellchecker_widget.py`
- **Line:** 58
- **Arguments:** self, position
- **Docstring:** Show context menu with spell check suggestions...

---

### `ui\Widgets\voice_settings_dialog.py.__init__`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 44
- **Arguments:** self, parent, config_manager

---

### `ui\Widgets\voice_settings_dialog.py.check_internet_connection`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 581
- **Arguments:** self
- **Docstring:** Check internet connectivity...

---

### `ui\Widgets\voice_settings_dialog.py.create_general_tab`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 398
- **Arguments:** self
- **Docstring:** Create the general settings tab...

---

### `ui\Widgets\voice_settings_dialog.py.create_stt_tab`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 260
- **Arguments:** self
- **Docstring:** Create the STT configuration tab...

---

### `ui\Widgets\voice_settings_dialog.py.create_tts_tab`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 300
- **Arguments:** self
- **Docstring:** Create the TTS configuration tab...

---

### `ui\Widgets\voice_settings_dialog.py.download_selected_model`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 765
- **Arguments:** self
- **Docstring:** Download the selected Coqui TTS model...

---

### `ui\Widgets\voice_settings_dialog.py.get_settings`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 922
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get current settings...

---

### `ui\Widgets\voice_settings_dialog.py.load_coqui_models`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 680
- **Arguments:** self
- **Docstring:** Load available Coqui TTS models...

---

### `ui\Widgets\voice_settings_dialog.py.load_coqui_speakers`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 737
- **Arguments:** self, model_name
- **Docstring:** Load available speakers for the selected model...

---

### `ui\Widgets\voice_settings_dialog.py.on_coqui_download_completed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 803
- **Arguments:** self, success, message
- **Docstring:** Handle Coqui TTS download completion...

---

### `ui\Widgets\voice_settings_dialog.py.on_coqui_model_changed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 707
- **Arguments:** self, model_text
- **Docstring:** Handle Coqui TTS model selection...

---

### `ui\Widgets\voice_settings_dialog.py.on_coqui_speaker_changed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 760
- **Arguments:** self, speaker_name
- **Docstring:** Handle Coqui TTS speaker selection...

---

### `ui\Widgets\voice_settings_dialog.py.on_eq_visualizer_changed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 674
- **Arguments:** self, eq_type
- **Docstring:** Handle EQ visualizer selection change...

---

### `ui\Widgets\voice_settings_dialog.py.on_internet_check_completed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 590
- **Arguments:** self, is_connected, status
- **Docstring:** Handle internet check completion...

---

### `ui\Widgets\voice_settings_dialog.py.on_silence_threshold_changed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 817
- **Arguments:** self, value
- **Docstring:** Handle silence threshold value change...

---

### `ui\Widgets\voice_settings_dialog.py.on_stt_api_changed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 626
- **Arguments:** self, api_name
- **Docstring:** Handle STT API selection change...

---

### `ui\Widgets\voice_settings_dialog.py.on_tts_api_changed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 638
- **Arguments:** self, api_name
- **Docstring:** Handle TTS API selection change...

---

### `ui\Widgets\voice_settings_dialog.py.on_tts_settings_changed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 997
- **Arguments:** self, settings

---

### `ui\Widgets\voice_settings_dialog.py.on_voice_changed`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 670
- **Arguments:** self, voice
- **Docstring:** Handle voice selection change...

---

### `ui\Widgets\voice_settings_dialog.py.run`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 29
- **Arguments:** self

---

### `ui\Widgets\voice_settings_dialog.py.save_settings`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 889
- **Arguments:** self
- **Docstring:** Save the current settings...

---

### `ui\Widgets\voice_settings_dialog.py.set_settings`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 926
- **Arguments:** self, settings
- **Docstring:** Set current settings...

---

### `ui\Widgets\voice_settings_dialog.py.setup_connections`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 569
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\Widgets\voice_settings_dialog.py.setup_ui`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 126
- **Arguments:** self
- **Docstring:** Setup the dialog UI...

---

### `ui\Widgets\voice_settings_dialog.py.start_coqui_download`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 783
- **Arguments:** self, model_name
- **Docstring:** Start downloading a Coqui TTS model...

---

### `ui\Widgets\voice_settings_dialog.py.test_settings`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 835
- **Arguments:** self
- **Docstring:** Test the current voice settings...

---

### `ui\Widgets\voice_settings_dialog.py.update_api_availability`

- **File:** `ui\Widgets\voice_settings_dialog.py`
- **Line:** 604
- **Arguments:** self
- **Docstring:** Update API availability based on internet connection...

---

### `ui\styles\message_formatter.py._protect_code_blocks`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 133
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Helper function to protect code blocks from processing...

---

### `ui\styles\message_formatter.py.cleanup_message`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 250
- **Arguments:** sender, message, is_code
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Prepares a message for display by adding sender and formatting....

---

### `ui\styles\message_formatter.py.detect_and_format_code`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 97
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Detects code and applies formatting. Highlights syntax using Pygments.
It handles inline and block c...

---

### `ui\styles\message_formatter.py.detect_code_in_message`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 19
- **Arguments:** message
- **Returns:** bool
- **Decorators:** staticmethod
- **Docstring:** Detect if a message contains code blocks or inline code.
Returns True if code is detected, False oth...

---

### `ui\styles\message_formatter.py.detect_code_type`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 48
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Detects the programming language of a code block using Pygments....

---

### `ui\styles\message_formatter.py.format_block_code`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 107
- **Arguments:** match

---

### `ui\styles\message_formatter.py.format_chat_message`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 278
- **Arguments:** sender, message, is_code
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format a complete chat message with styling based on sender type....

---

### `ui\styles\message_formatter.py.format_markdown`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 149
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Enhanced markdown formatting for better AI output presentation.
Handles headers, lists, emphasis, an...

---

### `ui\styles\message_formatter.py.handle_html_tags`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 221
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Properly handle HTML tags in messages - escape them for display when they're part of discussions
but...

---

### `ui\styles\message_formatter.py.protect_code_blocks`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 137
- **Arguments:** match

---

### `ui\styles\message_formatter.py.split_thoughts_and_answer`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 315
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Splits a message into (thoughts, main_answer) if <think>...</think> is present.
Returns a tuple (tho...

---

### `ui\styles\message_formatter.py.syntax_highlight_code`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 60
- **Arguments:** message, language
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Highlight the code using Pygments and return formatted HTML....

---

### `ui\styles\message_formatter.py.to_plain_text`

- **File:** `ui\styles\message_formatter.py`
- **Line:** 331
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Convert a message with markdown, code, and HTML to plain text for TTS.
Removes formatting, code bloc...

---

### `ui\styles\tab_styles.py.get_tab_style`

- **File:** `ui\styles\tab_styles.py`
- **Line:** 40
- **Arguments:** 
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Get the tab widget style...

---

### `ui\tabs\chat_tab\chat_display.py.__init__`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 22
- **Arguments:** self, parent

---

### `ui\tabs\chat_tab\chat_display.py.append_response_chunk`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 280
- **Arguments:** self, chunk, model_name
- **Docstring:** Append a streaming response chunk...

---

### `ui\tabs\chat_tab\chat_display.py.append_to_chat`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 265
- **Arguments:** self, sender, message, is_code
- **Docstring:** Add a message to the chat display...

---

### `ui\tabs\chat_tab\chat_display.py.chat_display_mouse_move_event`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 75
- **Arguments:** self, event
- **Docstring:** Handle mouse move events to show/hide edit buttons...

---

### `ui\tabs\chat_tab\chat_display.py.clear_chat`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 312
- **Arguments:** self
- **Docstring:** Clear the chat display...

---

### `ui\tabs\chat_tab\chat_display.py.edit_message_at_index`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 143
- **Arguments:** self, message_index
- **Docstring:** Edit message at specific index...

---

### `ui\tabs\chat_tab\chat_display.py.get_ai_name`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 71
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the AI name - this should be overridden by parent...

---

### `ui\tabs\chat_tab\chat_display.py.get_streaming_handler`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 326
- **Arguments:** self
- **Docstring:** Get the streaming handler...

---

### `ui\tabs\chat_tab\chat_display.py.get_ui_components`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 319
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get UI components for integration with parent...

---

### `ui\tabs\chat_tab\chat_display.py.hide_edit_button`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 135
- **Arguments:** self
- **Docstring:** Hide the edit button...

---

### `ui\tabs\chat_tab\chat_display.py.on_message_edited`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 260
- **Arguments:** self, message_index, new_content
- **Docstring:** Handle message edit...

---

### `ui\tabs\chat_tab\chat_display.py.save_message_edit`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 244
- **Arguments:** self, dialog, message_index, new_content
- **Docstring:** Save the edited message...

---

### `ui\tabs\chat_tab\chat_display.py.setup_streaming_handler`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 64
- **Arguments:** self
- **Docstring:** Setup the streaming handler for chat display...

---

### `ui\tabs\chat_tab\chat_display.py.setup_ui_components`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 36
- **Arguments:** self
- **Docstring:** Setup UI components for chat display...

---

### `ui\tabs\chat_tab\chat_display.py.show_edit_button`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 101
- **Arguments:** self, pos, message_index
- **Docstring:** Show edit button for a specific message...

---

### `ui\tabs\chat_tab\chat_display.py.show_message_edit_dialog`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 154
- **Arguments:** self, message_index, current_content
- **Docstring:** Show dialog to edit a message...

---

### `ui\tabs\chat_tab\chat_display.py.start_streaming`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 298
- **Arguments:** self
- **Docstring:** Start streaming state...

---

### `ui\tabs\chat_tab\chat_display.py.stop_streaming`

- **File:** `ui\tabs\chat_tab\chat_display.py`
- **Line:** 306
- **Arguments:** self
- **Docstring:** Stop streaming state...

---

### `ui\tabs\chat_tab\chat_tab.py.__init__`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 45
- **Arguments:** self, parent, conversation_manager, summarization_service, config_manager

---

### `ui\tabs\chat_tab\chat_tab.py._append_response_chunk_safe`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 517
- **Arguments:** self, chunk, model_name
- **Docstring:** Append a streaming response chunk safely in the main thread...

---

### `ui\tabs\chat_tab\chat_tab.py._force_enable_send_button_safe`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 614
- **Arguments:** self
- **Docstring:** Force enable the send button safely in the main thread...

---

### `ui\tabs\chat_tab\chat_tab.py._start_streaming_safe`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 541
- **Arguments:** self
- **Docstring:** Start streaming state safely in the main thread...

---

### `ui\tabs\chat_tab\chat_tab.py._stop_streaming_safe`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 576
- **Arguments:** self
- **Docstring:** Stop streaming state safely in the main thread...

---

### `ui\tabs\chat_tab\chat_tab.py.append_response_chunk`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 511
- **Arguments:** self, chunk, model_name
- **Docstring:** Append a streaming response chunk...

---

### `ui\tabs\chat_tab\chat_tab.py.append_to_chat`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 502
- **Arguments:** self, sender, message, is_code
- **Docstring:** Add a message to the chat display...

---

### `ui\tabs\chat_tab\chat_tab.py.clear_chat`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 636
- **Arguments:** self
- **Docstring:** Clear the chat display...

---

### `ui\tabs\chat_tab\chat_tab.py.force_enable_send_button`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 608
- **Arguments:** self
- **Docstring:** Force enable the send button and ensure UI is updated...

---

### `ui\tabs\chat_tab\chat_tab.py.get_ai_name`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 479
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the AI name based on current personality...

---

### `ui\tabs\chat_tab\chat_tab.py.get_current_model`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 490
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected model...

---

### `ui\tabs\chat_tab\chat_tab.py.get_current_personality`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 486
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality...

---

### `ui\tabs\chat_tab\chat_tab.py.get_current_response`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 498
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the current streaming response...

---

### `ui\tabs\chat_tab\chat_tab.py.get_streaming_handler`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 737
- **Arguments:** self
- **Docstring:** Get the streaming handler for backward compatibility...

---

### `ui\tabs\chat_tab\chat_tab.py.get_temperature`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 494
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get the current temperature setting...

---

### `ui\tabs\chat_tab\chat_tab.py.load_conversation`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 680
- **Arguments:** self, filepath
- **Docstring:** Load a conversation from file...

---

### `ui\tabs\chat_tab\chat_tab.py.on_audio_level_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 461
- **Arguments:** self, audio_level
- **Docstring:** Handle audio level changes...

---

### `ui\tabs\chat_tab\chat_tab.py.on_eq_mode_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 372
- **Arguments:** self, mode
- **Docstring:** Handle EQ mode change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_input_mode_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 308
- **Arguments:** self, mode
- **Docstring:** Handle input mode change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_message_cancelled`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 303
- **Arguments:** self
- **Docstring:** Handle message cancelled from input controls...

---

### `ui\tabs\chat_tab\chat_tab.py.on_message_edited`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 473
- **Arguments:** self, message_index, new_content
- **Docstring:** Handle message edit...

---

### `ui\tabs\chat_tab\chat_tab.py.on_message_sent`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 295
- **Arguments:** self, message
- **Docstring:** Handle message sent from input controls...

---

### `ui\tabs\chat_tab\chat_tab.py.on_model_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 367
- **Arguments:** self, model_name
- **Docstring:** Handle model change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_personality_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 362
- **Arguments:** self, personality_name
- **Docstring:** Handle personality change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_recording_error`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 449
- **Arguments:** self, error
- **Docstring:** Handle recording error...

---

### `ui\tabs\chat_tab\chat_tab.py.on_recording_started`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 441
- **Arguments:** self
- **Docstring:** Handle recording started...

---

### `ui\tabs\chat_tab\chat_tab.py.on_recording_stopped`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 445
- **Arguments:** self
- **Docstring:** Handle recording stopped...

---

### `ui\tabs\chat_tab\chat_tab.py.on_temperature_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 357
- **Arguments:** self, temperature
- **Docstring:** Handle temperature change...

---

### `ui\tabs\chat_tab\chat_tab.py.on_tts_error`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 437
- **Arguments:** self, error
- **Docstring:** Handle TTS error...

---

### `ui\tabs\chat_tab\chat_tab.py.on_tts_finished`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 411
- **Arguments:** self
- **Docstring:** Handle TTS finished...

---

### `ui\tabs\chat_tab\chat_tab.py.on_tts_started`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 401
- **Arguments:** self
- **Docstring:** Handle TTS started...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_input_error`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 396
- **Arguments:** self, error
- **Docstring:** Handle voice input error...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_input_received`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 380
- **Arguments:** self, text
- **Docstring:** Handle voice input received...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_processing_finished`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 457
- **Arguments:** self
- **Docstring:** Handle voice processing finished...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_processing_started`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 453
- **Arguments:** self
- **Docstring:** Handle voice processing started...

---

### `ui\tabs\chat_tab\chat_tab.py.on_voice_settings_changed`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 670
- **Arguments:** self, settings
- **Docstring:** Handle voice settings changes...

---

### `ui\tabs\chat_tab\chat_tab.py.open_voice_settings`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 652
- **Arguments:** self
- **Docstring:** Open voice settings dialog...

---

### `ui\tabs\chat_tab\chat_tab.py.refresh_navigation`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 727
- **Arguments:** self
- **Docstring:** Refresh the navigation widget...

---

### `ui\tabs\chat_tab\chat_tab.py.set_current_conversation_file`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 732
- **Arguments:** self, filepath
- **Docstring:** Set the current conversation file in the navigation widget...

---

### `ui\tabs\chat_tab\chat_tab.py.setup_components`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 71
- **Arguments:** self
- **Docstring:** Initialize all modular components...

---

### `ui\tabs\chat_tab\chat_tab.py.setup_connections`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 254
- **Arguments:** self
- **Docstring:** Setup signal connections between components...

---

### `ui\tabs\chat_tab\chat_tab.py.setup_ui`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 91
- **Arguments:** self
- **Docstring:** Setup the chat interface UI...

---

### `ui\tabs\chat_tab\chat_tab.py.speak_ai_response`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 648
- **Arguments:** self, text
- **Docstring:** Trigger TTS for AI response...

---

### `ui\tabs\chat_tab\chat_tab.py.start_streaming`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 535
- **Arguments:** self
- **Docstring:** Start streaming state...

---

### `ui\tabs\chat_tab\chat_tab.py.stop_streaming`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 570
- **Arguments:** self
- **Docstring:** Stop streaming state...

---

### `ui\tabs\chat_tab\chat_tab.py.streaming_handler`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 742
- **Arguments:** self
- **Decorators:** property
- **Docstring:** Property to access streaming handler for backward compatibility...

---

### `ui\tabs\chat_tab\chat_tab.py.update_model_list`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 640
- **Arguments:** self, models
- **Docstring:** Update the model combo box with available models...

---

### `ui\tabs\chat_tab\chat_tab.py.update_personality_list`

- **File:** `ui\tabs\chat_tab\chat_tab.py`
- **Line:** 644
- **Arguments:** self, personalities
- **Docstring:** Update the personality combo box with available personalities...

---

### `ui\tabs\chat_tab\eq_visualizer.py.__init__`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 26
- **Arguments:** self, parent

---

### `ui\tabs\chat_tab\eq_visualizer.py._update_eq_widget_safe`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 354
- **Arguments:** self, bar_values
- **Docstring:** Update the EQ widget safely in the main thread...

---

### `ui\tabs\chat_tab\eq_visualizer.py.get_available_eq_modes`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 385
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get list of available EQ visualizer modes...

---

### `ui\tabs\chat_tab\eq_visualizer.py.get_eq_mode`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 381
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the current EQ visualizer mode...

---

### `ui\tabs\chat_tab\eq_visualizer.py.is_eq_visualizer_active`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 367
- **Arguments:** self, voice_mode, tts_playing
- **Docstring:** Check if EQ visualizer should be active...

---

### `ui\tabs\chat_tab\eq_visualizer.py.setup_eq_visualizers`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 38
- **Arguments:** self
- **Docstring:** Initialize EQ visualizer widgets...

---

### `ui\tabs\chat_tab\eq_visualizer.py.switch_to_chat_display`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 148
- **Arguments:** self, chat_display
- **Docstring:** Switch back to chat display mode...

---

### `ui\tabs\chat_tab\eq_visualizer.py.switch_to_eq_visualizer`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 52
- **Arguments:** self, chat_display, voice_mode
- **Docstring:** Switch the chat display to EQ visualizer mode...

---

### `ui\tabs\chat_tab\eq_visualizer.py.update_eq_visualizer`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 243
- **Arguments:** self, audio_level, tts_playing
- **Docstring:** Update the EQ visualizer with audio level data....

---

### `ui\tabs\chat_tab\eq_visualizer.py.update_eq_visualizer_mode`

- **File:** `ui\tabs\chat_tab\eq_visualizer.py`
- **Line:** 373
- **Arguments:** self, mode
- **Docstring:** Update the EQ visualizer mode...

---

### `ui\tabs\chat_tab\input_controls.py.__init__`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 28
- **Arguments:** self, parent

---

### `ui\tabs\chat_tab\input_controls.py.cancel_message`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 285
- **Arguments:** self
- **Docstring:** Cancel the current message...

---

### `ui\tabs\chat_tab\input_controls.py.eventFilter`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 411
- **Arguments:** self, obj, event
- **Docstring:** Handle key events in message input...

---

### `ui\tabs\chat_tab\input_controls.py.force_enable_send_button`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 339
- **Arguments:** self
- **Docstring:** Force enable the send button and ensure UI is updated...

---

### `ui\tabs\chat_tab\input_controls.py.get_current_model`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 381
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected model...

---

### `ui\tabs\chat_tab\input_controls.py.get_current_personality`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 393
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality...

---

### `ui\tabs\chat_tab\input_controls.py.get_current_response`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 389
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the current streaming response...

---

### `ui\tabs\chat_tab\input_controls.py.get_temperature`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 385
- **Arguments:** self
- **Returns:** float
- **Docstring:** Get the current temperature setting...

---

### `ui\tabs\chat_tab\input_controls.py.get_ui_components`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 397
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get UI components for integration with parent...

---

### `ui\tabs\chat_tab\input_controls.py.on_model_changed`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 265
- **Arguments:** self, model_name
- **Docstring:** Handle model combo box change...

---

### `ui\tabs\chat_tab\input_controls.py.on_personality_combo_changed`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 259
- **Arguments:** self, personality_name
- **Docstring:** Handle personality combo box change...

---

### `ui\tabs\chat_tab\input_controls.py.on_temperature_changed`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 252
- **Arguments:** self, value
- **Docstring:** Handle temperature slider value change...

---

### `ui\tabs\chat_tab\input_controls.py.send_message`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 270
- **Arguments:** self
- **Docstring:** Send the current message...

---

### `ui\tabs\chat_tab\input_controls.py.set_input_mode`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 233
- **Arguments:** self, mode
- **Docstring:** Set the input mode (Chat or Voice)...

---

### `ui\tabs\chat_tab\input_controls.py.setup_connections`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 215
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\tabs\chat_tab\input_controls.py.setup_ui_components`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 43
- **Arguments:** self
- **Docstring:** Setup UI components for input controls...

---

### `ui\tabs\chat_tab\input_controls.py.start_streaming`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 290
- **Arguments:** self
- **Docstring:** Start streaming state...

---

### `ui\tabs\chat_tab\input_controls.py.stop_streaming`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 313
- **Arguments:** self
- **Docstring:** Stop streaming state...

---

### `ui\tabs\chat_tab\input_controls.py.update_model_list`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 359
- **Arguments:** self, models
- **Docstring:** Update the model combo box with available models...

---

### `ui\tabs\chat_tab\input_controls.py.update_personality_list`

- **File:** `ui\tabs\chat_tab\input_controls.py`
- **Line:** 370
- **Arguments:** self, personalities
- **Docstring:** Update the personality combo box with available personalities...

---

### `ui\tabs\chat_tab\test_modular_imports.py.test_imports`

- **File:** `ui\tabs\chat_tab\test_modular_imports.py`
- **Line:** 5
- **Arguments:** 
- **Docstring:** Test that all modular components can be imported...

---

### `ui\tabs\chat_tab\test_pyside6_imports.py.test_component_imports`

- **File:** `ui\tabs\chat_tab\test_pyside6_imports.py`
- **Line:** 49
- **Arguments:** 
- **Docstring:** Test that all modular components can be imported...

---

### `ui\tabs\chat_tab\test_pyside6_imports.py.test_pyside6_imports`

- **File:** `ui\tabs\chat_tab\test_pyside6_imports.py`
- **Line:** 5
- **Arguments:** 
- **Docstring:** Test that all PySide6 imports and enums work correctly...

---

### `ui\tabs\chat_tab\voice_controls.py.__init__`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 32
- **Arguments:** self, parent, config_manager

---

### `ui\tabs\chat_tab\voice_controls.py._attempt_recovery`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 219
- **Arguments:** self
- **Docstring:** Attempt to recover voice service...

---

### `ui\tabs\chat_tab\voice_controls.py._disable_voice_features`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 259
- **Arguments:** self
- **Docstring:** Disable voice features after failed recovery...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_recording_error_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 565
- **Arguments:** self, error
- **Docstring:** Handle recording error safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_recording_started_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 516
- **Arguments:** self
- **Docstring:** Handle recording started safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_recording_stopped_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 544
- **Arguments:** self
- **Docstring:** Handle recording stopped safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_service_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 272
- **Arguments:** self, error
- **Docstring:** Handle service errors with exponential backoff...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_tts_error_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 505
- **Arguments:** self, error
- **Docstring:** Handle TTS error safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_tts_finished_continuous`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 400
- **Arguments:** self
- **Docstring:** Handle TTS finished in continuous voice mode...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_voice_crash`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 206
- **Arguments:** self
- **Docstring:** Handle voice service crashes gracefully...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_voice_input_error_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 464
- **Arguments:** self, error
- **Docstring:** Handle voice input error safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._handle_voice_input_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 383
- **Arguments:** self, text
- **Docstring:** Handle voice input safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._reinitialize_voice_service`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 251
- **Arguments:** self
- **Docstring:** Reinitialize voice service...

---

### `ui\tabs\chat_tab\voice_controls.py._reset_error_count`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 268
- **Arguments:** self
- **Docstring:** Reset error count after timeout...

---

### `ui\tabs\chat_tab\voice_controls.py._reset_voice_button`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 424
- **Arguments:** self
- **Docstring:** Reset voice button to initial state...

---

### `ui\tabs\chat_tab\voice_controls.py._reset_voice_ui`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 240
- **Arguments:** self
- **Docstring:** Reset voice UI to safe state...

---

### `ui\tabs\chat_tab\voice_controls.py._restart_voice_input`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 410
- **Arguments:** self
- **Docstring:** Restart voice input for continuous mode...

---

### `ui\tabs\chat_tab\voice_controls.py._start_continuous_voice_mode`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 366
- **Arguments:** self
- **Docstring:** Start continuous voice mode cycle...

---

### `ui\tabs\chat_tab\voice_controls.py._stop_all_voice_operations`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 229
- **Arguments:** self
- **Docstring:** Stop all voice operations safely...

---

### `ui\tabs\chat_tab\voice_controls.py._update_audio_level_ui_safe`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 603
- **Arguments:** self, audio_level
- **Docstring:** Update audio level UI safely in the main thread...

---

### `ui\tabs\chat_tab\voice_controls.py._update_voice_state`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 196
- **Arguments:** self, key, value
- **Docstring:** Thread-safe voice state update...

---

### `ui\tabs\chat_tab\voice_controls.py.get_ui_components`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 700
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get UI components for integration with parent...

---

### `ui\tabs\chat_tab\voice_controls.py.get_voice_settings`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 682
- **Arguments:** self
- **Returns:** dict
- **Docstring:** Get current voice settings...

---

### `ui\tabs\chat_tab\voice_controls.py.is_tts_playing`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 690
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if TTS is currently playing...

---

### `ui\tabs\chat_tab\voice_controls.py.is_voice_busy`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 201
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Thread-safe check if voice is busy...

---

### `ui\tabs\chat_tab\voice_controls.py.is_voice_mode_active`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 686
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if voice mode is active...

---

### `ui\tabs\chat_tab\voice_controls.py.on_audio_level_changed`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 593
- **Arguments:** self, audio_level
- **Docstring:** Handle audio level changes...

---

### `ui\tabs\chat_tab\voice_controls.py.on_recording_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 558
- **Arguments:** self, error
- **Docstring:** Handle recording error...

---

### `ui\tabs\chat_tab\voice_controls.py.on_recording_started`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 509
- **Arguments:** self
- **Docstring:** Handle recording started...

---

### `ui\tabs\chat_tab\voice_controls.py.on_recording_stopped`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 537
- **Arguments:** self
- **Docstring:** Handle recording stopped...

---

### `ui\tabs\chat_tab\voice_controls.py.on_tts_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 495
- **Arguments:** self, error
- **Docstring:** Handle TTS error...

---

### `ui\tabs\chat_tab\voice_controls.py.on_tts_finished`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 484
- **Arguments:** self
- **Docstring:** Handle TTS finished...

---

### `ui\tabs\chat_tab\voice_controls.py.on_tts_started`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 479
- **Arguments:** self
- **Docstring:** Handle TTS started...

---

### `ui\tabs\chat_tab\voice_controls.py.on_voice_input_error`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 454
- **Arguments:** self, error
- **Docstring:** Handle voice input error...

---

### `ui\tabs\chat_tab\voice_controls.py.on_voice_input_received`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 446
- **Arguments:** self, text
- **Docstring:** Handle voice input received...

---

### `ui\tabs\chat_tab\voice_controls.py.on_voice_processing_finished`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 587
- **Arguments:** self
- **Docstring:** Handle voice processing finished...

---

### `ui\tabs\chat_tab\voice_controls.py.on_voice_processing_started`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 580
- **Arguments:** self
- **Docstring:** Handle voice processing started...

---

### `ui\tabs\chat_tab\voice_controls.py.setup_connections`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 284
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\tabs\chat_tab\voice_controls.py.setup_ui_components`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 112
- **Arguments:** self
- **Docstring:** Setup UI components for voice controls...

---

### `ui\tabs\chat_tab\voice_controls.py.speak_ai_response`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 662
- **Arguments:** self, text
- **Docstring:** Speak AI response using TTS...

---

### `ui\tabs\chat_tab\voice_controls.py.toggle_voice_mode`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 314
- **Arguments:** self
- **Docstring:** Toggle voice mode on/off...

---

### `ui\tabs\chat_tab\voice_controls.py.update_voice_settings`

- **File:** `ui\tabs\chat_tab\voice_controls.py`
- **Line:** 673
- **Arguments:** self, settings
- **Docstring:** Update voice settings...

---

### `ui\tabs\memory_tab.py.__init__`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 23
- **Arguments:** self, memory_service

---

### `ui\tabs\memory_tab.py._summarize_with_service`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 491
- **Arguments:** self
- **Docstring:** Summarize the current conversation using the conversation service...

---

### `ui\tabs\memory_tab.py.cleanup_memory_entries`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 525
- **Arguments:** self
- **Docstring:** Clean up duplicate and conflicting memory entries...

---

### `ui\tabs\memory_tab.py.clear_all_memories`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 512
- **Arguments:** self
- **Docstring:** Clear all memories...

---

### `ui\tabs\memory_tab.py.create_memories_tab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 176
- **Arguments:** self
- **Docstring:** Create the memories management tab...

---

### `ui\tabs\memory_tab.py.create_overview_tab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 116
- **Arguments:** self
- **Docstring:** Create the memory overview tab...

---

### `ui\tabs\memory_tab.py.create_settings_tab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 56
- **Arguments:** self
- **Docstring:** Create the memory settings tab...

---

### `ui\tabs\memory_tab.py.create_summaries_tab`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 241
- **Arguments:** self
- **Docstring:** Create the summaries management tab...

---

### `ui\tabs\memory_tab.py.delete_selected_memory`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 541
- **Arguments:** self
- **Docstring:** Delete the selected memory...

---

### `ui\tabs\memory_tab.py.refresh_data`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 300
- **Arguments:** self
- **Docstring:** Refresh all data displays...

---

### `ui\tabs\memory_tab.py.refresh_memories`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 362
- **Arguments:** self
- **Docstring:** Refresh the memories table based on STM/LTM filter...

---

### `ui\tabs\memory_tab.py.refresh_overview`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 306
- **Arguments:** self
- **Docstring:** Refresh the overview tab data...

---

### `ui\tabs\memory_tab.py.refresh_summaries`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 393
- **Arguments:** self
- **Docstring:** Refresh the summaries list...

---

### `ui\tabs\memory_tab.py.search_memories`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 406
- **Arguments:** self
- **Docstring:** Search memories based on input...

---

### `ui\tabs\memory_tab.py.set_conversation_service`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 484
- **Arguments:** self, conversation_service
- **Docstring:** Set the conversation service for summarization...

---

### `ui\tabs\memory_tab.py.setup_connections`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 271
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\tabs\memory_tab.py.setup_ui`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 30
- **Arguments:** self
- **Docstring:** Setup the memory tab UI...

---

### `ui\tabs\memory_tab.py.show_memory_details`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 428
- **Arguments:** self
- **Docstring:** Show details for selected memory...

---

### `ui\tabs\memory_tab.py.show_summary_details`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 462
- **Arguments:** self
- **Docstring:** Show details for selected summary...

---

### `ui\tabs\memory_tab.py.summarize_current_conversation`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 478
- **Arguments:** self
- **Docstring:** Summarize the current conversation...

---

### `ui\tabs\memory_tab.py.update_context_messages`

- **File:** `ui\tabs\memory_tab.py`
- **Line:** 295
- **Arguments:** self, value
- **Docstring:** Update the maximum context messages...

---

### `ui\tabs\model_tab.py.__init__`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 23
- **Arguments:** self, parent

---

### `ui\tabs\model_tab.py.append_status`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 469
- **Arguments:** self, message
- **Docstring:** Append a status message to the status text area...

---

### `ui\tabs\model_tab.py.clear_status`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 506
- **Arguments:** self
- **Docstring:** Clear the status text area...

---

### `ui\tabs\model_tab.py.get_current_time`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 478
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get current time as string...

---

### `ui\tabs\model_tab.py.get_selected_model`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 501
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected model...

---

### `ui\tabs\model_tab.py.on_model_selection_changed`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 445
- **Arguments:** self
- **Docstring:** Handle model selection change...

---

### `ui\tabs\model_tab.py.on_operation_error`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 495
- **Arguments:** self, error
- **Docstring:** Handle operation errors...

---

### `ui\tabs\model_tab.py.on_operation_finished`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 487
- **Arguments:** self, operation
- **Docstring:** Handle operation completion...

---

### `ui\tabs\model_tab.py.on_operation_progress`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 483
- **Arguments:** self, message
- **Docstring:** Handle operation progress updates...

---

### `ui\tabs\model_tab.py.pull_model`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 387
- **Arguments:** self
- **Docstring:** Pull a new model...

---

### `ui\tabs\model_tab.py.refresh_models`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 369
- **Arguments:** self
- **Docstring:** Refresh the list of available models...

---

### `ui\tabs\model_tab.py.remove_selected_model`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 405
- **Arguments:** self
- **Docstring:** Remove the selected model...

---

### `ui\tabs\model_tab.py.setup_connections`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 359
- **Arguments:** self
- **Docstring:** Setup signal connections...

---

### `ui\tabs\model_tab.py.setup_model_list`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 63
- **Arguments:** self, parent
- **Docstring:** Setup the model list area...

---

### `ui\tabs\model_tab.py.setup_operations`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 139
- **Arguments:** self, parent
- **Docstring:** Setup the operations area...

---

### `ui\tabs\model_tab.py.setup_ui`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 46
- **Arguments:** self
- **Docstring:** Setup the model management UI...

---

### `ui\tabs\model_tab.py.start_operation`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 452
- **Arguments:** self
- **Docstring:** Start an operation (disable UI elements)...

---

### `ui\tabs\model_tab.py.stop_operation`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 461
- **Arguments:** self
- **Docstring:** Stop an operation (enable UI elements)...

---

### `ui\tabs\model_tab.py.update_model_list`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 377
- **Arguments:** self, models
- **Docstring:** Update the model list display...

---

### `ui\tabs\model_tab.py.update_selected_model`

- **File:** `ui\tabs\model_tab.py`
- **Line:** 425
- **Arguments:** self
- **Docstring:** Update the selected model...

---

### `ui\tabs\personality_tab.py.__init__`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 23
- **Arguments:** self, parent

---

### `ui\tabs\personality_tab.py.clear_creation_form`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 730
- **Arguments:** self
- **Docstring:** Clear the personality creation form...

---

### `ui\tabs\personality_tab.py.create_personality`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 673
- **Arguments:** self
- **Docstring:** Create a new personality...

---

### `ui\tabs\personality_tab.py.delete_custom_personality`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 738
- **Arguments:** self
- **Docstring:** Delete the selected custom personality...

---

### `ui\tabs\personality_tab.py.export_personality`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 771
- **Arguments:** self
- **Docstring:** Export the selected personality to a file...

---

### `ui\tabs\personality_tab.py.get_available_personalities`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 816
- **Arguments:** self
- **Returns:** list
- **Docstring:** Get list of available personality names...

---

### `ui\tabs\personality_tab.py.get_current_personality`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 801
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the currently selected personality name...

---

### `ui\tabs\personality_tab.py.get_system_prompt`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 805
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get the system prompt for the current personality...

---

### `ui\tabs\personality_tab.py.load_personalities`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 553
- **Arguments:** self
- **Docstring:** Load available personalities into the combo box and lists...

---

### `ui\tabs\personality_tab.py.on_custom_personality_selected`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 638
- **Arguments:** self, item
- **Docstring:** Handle custom personality selection...

---

### `ui\tabs\personality_tab.py.on_personality_changed`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 644
- **Arguments:** self, personality_name
- **Docstring:** Handle personality selection change...

---

### `ui\tabs\personality_tab.py.on_system_personality_selected`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 611
- **Arguments:** self, item
- **Docstring:** Handle system personality selection...

---

### `ui\tabs\personality_tab.py.refresh_personalities`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 792
- **Arguments:** self
- **Docstring:** Refresh personalities from disk...

---

### `ui\tabs\personality_tab.py.setup_creation_tab`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 197
- **Arguments:** self
- **Docstring:** Setup the personality creation tab...

---

### `ui\tabs\personality_tab.py.setup_management_tab`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 380
- **Arguments:** self
- **Docstring:** Setup the personality management tab...

---

### `ui\tabs\personality_tab.py.setup_selection_tab`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 90
- **Arguments:** self
- **Docstring:** Setup the personality selection tab...

---

### `ui\tabs\personality_tab.py.setup_ui`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 30
- **Arguments:** self
- **Docstring:** Setup the personality management UI...

---

### `ui\tabs\personality_tab.py.update_custom_personalities_list`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 600
- **Arguments:** self
- **Docstring:** Update the custom personalities list...

---

### `ui\tabs\personality_tab.py.update_personality_info`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 650
- **Arguments:** self, personality_name
- **Docstring:** Update the personality info display...

---

### `ui\tabs\personality_tab.py.update_system_personalities_list`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 589
- **Arguments:** self
- **Docstring:** Update the system personalities list...

---

### `ui\tabs\personality_tab.py.update_system_personality_info`

- **File:** `ui\tabs\personality_tab.py`
- **Line:** 617
- **Arguments:** self, personality_name
- **Docstring:** Update the system personality info display...

---

### `utils\Logging\Custom_Logger.py.__new__`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 95
- **Arguments:** cls

---

### `utils\Logging\Custom_Logger.py._check_config_for_logging`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 83
- **Arguments:** cls
- **Decorators:** classmethod

---

### `utils\Logging\Custom_Logger.py._clear_log_file`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 106
- **Arguments:** cls, filepath
- **Decorators:** classmethod

---

### `utils\Logging\Custom_Logger.py._filter_non_ascii`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 177
- **Arguments:** self, s

---

### `utils\Logging\Custom_Logger.py._print`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 36
- **Arguments:** self, msg

---

### `utils\Logging\Custom_Logger.py._sanitize_filename`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 17
- **Arguments:** name

---

### `utils\Logging\Custom_Logger.py.critical`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 122
- **Arguments:** self

---

### `utils\Logging\Custom_Logger.py.debug`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 119
- **Arguments:** self

---

### `utils\Logging\Custom_Logger.py.error`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 121
- **Arguments:** self

---

### `utils\Logging\Custom_Logger.py.get_logger`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 113
- **Arguments:** cls, name
- **Decorators:** classmethod

---

### `utils\Logging\Custom_Logger.py.info`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 118
- **Arguments:** self

---

### `utils\Logging\Custom_Logger.py.set_logging_enabled`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 102
- **Arguments:** cls, enabled
- **Decorators:** classmethod

---

### `utils\Logging\Custom_Logger.py.strip_emojis`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 20
- **Arguments:** text

---

### `utils\Logging\Custom_Logger.py.warning`

- **File:** `utils\Logging\Custom_Logger.py`
- **Line:** 120
- **Arguments:** self

---

### `utils\Logging\logging_helpers.py.__init__`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 214
- **Arguments:** self

---

### `utils\Logging\logging_helpers.py._on_thread_finished`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 284
- **Arguments:** self, thread_name
- **Docstring:** Handle thread finished signal...

---

### `utils\Logging\logging_helpers.py._on_thread_started`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 272
- **Arguments:** self, thread_name
- **Docstring:** Handle thread started signal...

---

### `utils\Logging\logging_helpers.py.cleanup`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 350
- **Arguments:** self
- **Docstring:** Clean up the thread monitor...

---

### `utils\Logging\logging_helpers.py.cleanup_thread_monitor`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 424
- **Arguments:** 
- **Docstring:** Clean up the global thread monitor...

---

### `utils\Logging\logging_helpers.py.get_all_threads`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 302
- **Arguments:** self
- **Docstring:** Get information about all active threads...

---

### `utils\Logging\logging_helpers.py.get_thread_history`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 306
- **Arguments:** self
- **Docstring:** Get history of completed threads...

---

### `utils\Logging\logging_helpers.py.get_thread_info`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 298
- **Arguments:** self, thread_name
- **Docstring:** Get information about a specific thread...

---

### `utils\Logging\logging_helpers.py.get_thread_monitor`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 417
- **Arguments:** 
- **Returns:** ThreadMonitor
- **Docstring:** Get the global thread monitor instance...

---

### `utils\Logging\logging_helpers.py.get_thread_stats`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 310
- **Arguments:** self
- **Returns:** Dict
- **Docstring:** Get statistics about thread usage...

---

### `utils\Logging\logging_helpers.py.log_audio_operation`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 70
- **Arguments:** operation, success, error, details
- **Decorators:** staticmethod
- **Docstring:** Log audio operation information...

---

### `utils\Logging\logging_helpers.py.log_conversation_detection`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 193
- **Arguments:** conversation_type
- **Decorators:** staticmethod
- **Docstring:** Log conversation detection...

---

### `utils\Logging\logging_helpers.py.log_critical_error`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 111
- **Arguments:** component, error, recovery_action
- **Decorators:** staticmethod
- **Docstring:** Log a critical error with recovery action...

---

### `utils\Logging\logging_helpers.py.log_debug`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 42
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Log a debug message...

---

### `utils\Logging\logging_helpers.py.log_error`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 47
- **Arguments:** message
- **Decorators:** staticmethod
- **Docstring:** Log an error message...

---

### `utils\Logging\logging_helpers.py.log_exception_with_context`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 23
- **Arguments:** operation, exception, context
- **Decorators:** staticmethod
- **Docstring:** Log an exception with context information...

---

### `utils\Logging\logging_helpers.py.log_fact_extraction_end`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 123
- **Arguments:** facts_count
- **Decorators:** staticmethod
- **Docstring:** Log fact extraction end...

---

### `utils\Logging\logging_helpers.py.log_fact_extraction_result`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 128
- **Arguments:** facts
- **Decorators:** staticmethod
- **Docstring:** Log fact extraction result...

---

### `utils\Logging\logging_helpers.py.log_fact_extraction_start`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 118
- **Arguments:** query
- **Decorators:** staticmethod
- **Docstring:** Log fact extraction start...

---

### `utils\Logging\logging_helpers.py.log_fact_processing`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 133
- **Arguments:** fact_type, fact_count
- **Decorators:** staticmethod
- **Docstring:** Log fact processing...

---

### `utils\Logging\logging_helpers.py.log_fact_skipped`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 153
- **Arguments:** reason, fact_type
- **Decorators:** staticmethod
- **Docstring:** Log skipped fact...

---

### `utils\Logging\logging_helpers.py.log_fact_storage_end`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 143
- **Arguments:** fact_type, stored_count
- **Decorators:** staticmethod
- **Docstring:** Log fact storage end...

---

### `utils\Logging\logging_helpers.py.log_fact_storage_start`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 138
- **Arguments:** fact_type, fact_count
- **Decorators:** staticmethod
- **Docstring:** Log fact storage start...

---

### `utils\Logging\logging_helpers.py.log_fact_storage_summary`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 148
- **Arguments:** total_facts, stored_facts
- **Decorators:** staticmethod
- **Docstring:** Log fact storage summary...

---

### `utils\Logging\logging_helpers.py.log_file_operation`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 62
- **Arguments:** operation, filepath, success, error
- **Decorators:** staticmethod
- **Docstring:** Log file operation information...

---

### `utils\Logging\logging_helpers.py.log_info_with_context`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 36
- **Arguments:** message, context
- **Decorators:** staticmethod
- **Docstring:** Log an info message with context information...

---

### `utils\Logging\logging_helpers.py.log_json_extraction`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 178
- **Arguments:** json_data
- **Decorators:** staticmethod
- **Docstring:** Log JSON extraction...

---

### `utils\Logging\logging_helpers.py.log_json_parsing_error`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 100
- **Arguments:** error, json_str
- **Decorators:** staticmethod
- **Docstring:** Log JSON parsing error...

---

### `utils\Logging\logging_helpers.py.log_json_parsing_success`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 106
- **Arguments:** json_str
- **Decorators:** staticmethod
- **Docstring:** Log successful JSON parsing...

---

### `utils\Logging\logging_helpers.py.log_llm_call`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 168
- **Arguments:** model, prompt_length
- **Decorators:** staticmethod
- **Docstring:** Log LLM call...

---

### `utils\Logging\logging_helpers.py.log_llm_response`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 173
- **Arguments:** model, response_length
- **Decorators:** staticmethod
- **Docstring:** Log LLM response...

---

### `utils\Logging\logging_helpers.py.log_memory_ltm_status`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 163
- **Arguments:** ltm_count, stm_count
- **Decorators:** staticmethod
- **Docstring:** Log memory status...

---

### `utils\Logging\logging_helpers.py.log_memory_operation`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 78
- **Arguments:** operation, memory_type, success, error
- **Decorators:** staticmethod
- **Docstring:** Log memory operation information...

---

### `utils\Logging\logging_helpers.py.log_memory_result`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 158
- **Arguments:** query, memory_count
- **Decorators:** staticmethod
- **Docstring:** Log memory search result...

---

### `utils\Logging\logging_helpers.py.log_message_sent`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 183
- **Arguments:** message_length
- **Decorators:** staticmethod
- **Docstring:** Log message sent...

---

### `utils\Logging\logging_helpers.py.log_message_sent_end`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 188
- **Arguments:** message_length, response_length
- **Decorators:** staticmethod
- **Docstring:** Log message sent end...

---

### `utils\Logging\logging_helpers.py.log_network_request`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 52
- **Arguments:** url, method, status_code, error
- **Decorators:** staticmethod
- **Docstring:** Log network request information...

---

### `utils\Logging\logging_helpers.py.log_performance_metric`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 94
- **Arguments:** operation, duration, context
- **Decorators:** staticmethod
- **Docstring:** Log performance metric...

---

### `utils\Logging\logging_helpers.py.log_service_initialization`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 198
- **Arguments:** service_name, success, error
- **Decorators:** staticmethod
- **Docstring:** Log service initialization...

---

### `utils\Logging\logging_helpers.py.log_thread_context`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 374
- **Arguments:** message, thread
- **Decorators:** staticmethod
- **Docstring:** Log a message with thread context information...

---

### `utils\Logging\logging_helpers.py.log_thread_operation`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 407
- **Arguments:** operation, thread_name, details
- **Decorators:** staticmethod
- **Docstring:** Log thread operation...

---

### `utils\Logging\logging_helpers.py.log_thread_safety_check`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 392
- **Arguments:** operation, current_thread, target_thread
- **Decorators:** staticmethod
- **Docstring:** Log thread safety check...

---

### `utils\Logging\logging_helpers.py.log_ui_operation`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 86
- **Arguments:** component, operation, success, error
- **Decorators:** staticmethod
- **Docstring:** Log UI operation information...

---

### `utils\Logging\logging_helpers.py.log_warning_with_context`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 30
- **Arguments:** message, context
- **Decorators:** staticmethod
- **Docstring:** Log a warning with context information...

---

### `utils\Logging\logging_helpers.py.register_thread`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 222
- **Arguments:** self, thread, thread_type
- **Docstring:** Register a thread for monitoring...

---

### `utils\Logging\logging_helpers.py.unregister_thread`

- **File:** `utils\Logging\logging_helpers.py`
- **Line:** 252
- **Arguments:** self, thread_name
- **Docstring:** Unregister a thread from monitoring...

---

### `utils\complexity_analyzer.py.__init__`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 34
- **Arguments:** self

---

### `utils\complexity_analyzer.py._analyze_ambiguity`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 247
- **Arguments:** self, text
- **Returns:** float
- **Docstring:** Analyze the ambiguity level of the request...

---

### `utils\complexity_analyzer.py._analyze_context_dependency`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 281
- **Arguments:** self, text, conversation_history
- **Returns:** float
- **Docstring:** Analyze how much the request depends on conversation context...

---

### `utils\complexity_analyzer.py._analyze_knowledge_breadth`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 222
- **Arguments:** self, text
- **Returns:** float
- **Docstring:** Analyze the breadth of knowledge domains required...

---

### `utils\complexity_analyzer.py._analyze_output_complexity`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 301
- **Arguments:** self, text
- **Returns:** float
- **Docstring:** Analyze the complexity of expected output...

---

### `utils\complexity_analyzer.py._analyze_reasoning_depth`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 186
- **Arguments:** self, text
- **Returns:** float
- **Docstring:** Analyze the depth of reasoning required...

---

### `utils\complexity_analyzer.py._count_constraints`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 266
- **Arguments:** self, text
- **Returns:** int
- **Docstring:** Count the number of constraints in the request...

---

### `utils\complexity_analyzer.py._determine_complexity_level`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 321
- **Arguments:** self, overall_score, factors
- **Returns:** ComplexityLevel
- **Docstring:** Determine the complexity level based on overall score and factors...

---

### `utils\complexity_analyzer.py._estimate_tokens`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 180
- **Arguments:** self, text
- **Returns:** int
- **Docstring:** Rough token estimation (words + punctuation)...

---

### `utils\complexity_analyzer.py._generate_recommendations`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 332
- **Arguments:** self, level, factors
- **Docstring:** Generate recommendations based on complexity analysis...

---

### `utils\complexity_analyzer.py.analyze_complexity`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 114
- **Arguments:** self, request, conversation_history
- **Returns:** ComplexityMetrics
- **Docstring:** Analyze the complexity of a request and return detailed metrics.

Args:
    request: The user's requ...

---

### `utils\complexity_analyzer.py.extract_size`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 377
- **Arguments:** model_name

---

### `utils\complexity_analyzer.py.format_complexity_report`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 395
- **Arguments:** self, metrics
- **Returns:** str
- **Docstring:** Format complexity analysis as a readable report...

---

### `utils\complexity_analyzer.py.get_model_recommendation`

- **File:** `utils\complexity_analyzer.py`
- **Line:** 374
- **Arguments:** self, complexity_metrics, available_models
- **Returns:** str
- **Docstring:** Get model recommendation based on complexity analysis...

---

### `utils\complexity_widget.py.__init__`

- **File:** `utils\complexity_widget.py`
- **Line:** 13
- **Arguments:** self, parent

---

### `utils\complexity_widget.py._get_color_for_value`

- **File:** `utils\complexity_widget.py`
- **Line:** 217
- **Arguments:** self, value, reverse
- **Returns:** QColor
- **Docstring:** Get color based on value (0-1)...

---

### `utils\complexity_widget.py._on_switch_model`

- **File:** `utils\complexity_widget.py`
- **Line:** 190
- **Arguments:** self
- **Docstring:** Handle model switch button click...

---

### `utils\complexity_widget.py._set_progress_bar_color`

- **File:** `utils\complexity_widget.py`
- **Line:** 201
- **Arguments:** self, progress_bar, color
- **Docstring:** Set progress bar color...

---

### `utils\complexity_widget.py._set_widget_color`

- **File:** `utils\complexity_widget.py`
- **Line:** 195
- **Arguments:** self, widget, color
- **Docstring:** Set widget text color...

---

### `utils\complexity_widget.py._update_display`

- **File:** `utils\complexity_widget.py`
- **Line:** 132
- **Arguments:** self
- **Docstring:** Update the display with current metrics...

---

### `utils\complexity_widget.py._update_model_recommendation`

- **File:** `utils\complexity_widget.py`
- **Line:** 184
- **Arguments:** self, recommended_model
- **Docstring:** Update the model recommendation display...

---

### `utils\complexity_widget.py.analyze_request`

- **File:** `utils\complexity_widget.py`
- **Line:** 112
- **Arguments:** self, request, conversation_history, available_models
- **Docstring:** Analyze a request and update the display...

---

### `utils\complexity_widget.py.clear_analysis`

- **File:** `utils\complexity_widget.py`
- **Line:** 231
- **Arguments:** self
- **Docstring:** Clear the current analysis...

---

### `utils\complexity_widget.py.get_current_metrics`

- **File:** `utils\complexity_widget.py`
- **Line:** 239
- **Arguments:** self
- **Docstring:** Get the current complexity metrics...

---

### `utils\complexity_widget.py.setup_ui`

- **File:** `utils\complexity_widget.py`
- **Line:** 19
- **Arguments:** self
- **Docstring:** Setup the user interface...

---

### `utils\error_handler.py.audio_operation_context`

- **File:** `utils\error_handler.py`
- **Line:** 286
- **Arguments:** operation
- **Decorators:** contextmanager
- **Docstring:** Context manager for audio operations with error handling

Args:
    operation: Audio operation being...

---

### `utils\error_handler.py.cleanup_resources`

- **File:** `utils\error_handler.py`
- **Line:** 448
- **Arguments:** resources
- **Docstring:** Safely cleanup a list of resources

Args:
    resources: List of resources to cleanup...

---

### `utils\error_handler.py.error_context`

- **File:** `utils\error_handler.py`
- **Line:** 229
- **Arguments:** operation, context
- **Decorators:** contextmanager
- **Docstring:** Context manager for error handling with automatic logging

Args:
    operation: Name of the operatio...

---

### `utils\error_handler.py.file_operation_context`

- **File:** `utils\error_handler.py`
- **Line:** 269
- **Arguments:** operation, filepath
- **Decorators:** contextmanager
- **Docstring:** Context manager for file operations with error handling

Args:
    operation: File operation being p...

---

### `utils\error_handler.py.handle_audio_operations`

- **File:** `utils\error_handler.py`
- **Line:** 159
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle audio operation errors

Args:
    func: Function to decorate
    
Returns:
    D...

---

### `utils\error_handler.py.handle_critical_error`

- **File:** `utils\error_handler.py`
- **Line:** 467
- **Arguments:** error, component, recovery_action
- **Docstring:** Handle critical errors that may require application restart

Args:
    error: The critical error
   ...

---

### `utils\error_handler.py.handle_file_operations`

- **File:** `utils\error_handler.py`
- **Line:** 125
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle file operation errors

Args:
    func: Function to decorate
    
Returns:
    De...

---

### `utils\error_handler.py.handle_memory_operations`

- **File:** `utils\error_handler.py`
- **Line:** 182
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle memory operation errors

Args:
    func: Function to decorate
    
Returns:
    ...

---

### `utils\error_handler.py.handle_network_errors`

- **File:** `utils\error_handler.py`
- **Line:** 91
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle network-related errors specifically

Args:
    func: Function to decorate
    
R...

---

### `utils\error_handler.py.handle_ui_operations`

- **File:** `utils\error_handler.py`
- **Line:** 205
- **Arguments:** func
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to handle UI operation errors

Args:
    func: Function to decorate
    
Returns:
    Deco...

---

### `utils\error_handler.py.memory_operation_context`

- **File:** `utils\error_handler.py`
- **Line:** 302
- **Arguments:** operation, memory_type
- **Decorators:** contextmanager
- **Docstring:** Context manager for memory operations with error handling

Args:
    operation: Memory operation bei...

---

### `utils\error_handler.py.network_error_context`

- **File:** `utils\error_handler.py`
- **Line:** 252
- **Arguments:** url, method
- **Decorators:** contextmanager
- **Docstring:** Context manager for network operations with error handling

Args:
    url: URL being accessed
    me...

---

### `utils\error_handler.py.retry_on_failure`

- **File:** `utils\error_handler.py`
- **Line:** 49
- **Arguments:** func, max_attempts, delay_seconds, exceptions
- **Returns:** Callable
- **Decorators:** staticmethod
- **Docstring:** Decorator to retry a function on failure

Args:
    func: Function to retry
    max_attempts: Maximu...

---

### `utils\error_handler.py.safe_execute`

- **File:** `utils\error_handler.py`
- **Line:** 24
- **Arguments:** func
- **Returns:** Any
- **Decorators:** staticmethod
- **Docstring:** Safely execute a function with comprehensive error handling

Args:
    func: Function to execute
   ...

---

### `utils\error_handler.py.safe_file_read`

- **File:** `utils\error_handler.py`
- **Line:** 357
- **Arguments:** filepath, encoding, default
- **Returns:** Any
- **Docstring:** Safely read a file with error handling

Args:
    filepath: Path to the file
    encoding: File enco...

---

### `utils\error_handler.py.safe_file_write`

- **File:** `utils\error_handler.py`
- **Line:** 377
- **Arguments:** filepath, content, encoding
- **Returns:** bool
- **Docstring:** Safely write to a file with error handling

Args:
    filepath: Path to the file
    content: Conten...

---

### `utils\error_handler.py.safe_json_parse`

- **File:** `utils\error_handler.py`
- **Line:** 335
- **Arguments:** json_str, default
- **Returns:** Any
- **Docstring:** Safely parse JSON string with error handling

Args:
    json_str: JSON string to parse
    default: ...

---

### `utils\error_handler.py.safe_network_request`

- **File:** `utils\error_handler.py`
- **Line:** 401
- **Arguments:** url, method
- **Docstring:** Safely make a network request with error handling

Args:
    url: URL to request
    method: HTTP me...

---

### `utils\error_handler.py.ui_operation_context`

- **File:** `utils\error_handler.py`
- **Line:** 319
- **Arguments:** component, operation
- **Decorators:** contextmanager
- **Docstring:** Context manager for UI operations with error handling

Args:
    component: UI component being opera...

---

### `utils\error_handler.py.validate_input`

- **File:** `utils\error_handler.py`
- **Line:** 423
- **Arguments:** data, expected_type, field_name
- **Returns:** bool
- **Docstring:** Validate input data with error handling

Args:
    data: Data to validate
    expected_type: Expecte...

---

### `utils\error_handler.py.wrapper`

- **File:** `utils\error_handler.py`
- **Line:** 216
- **Arguments:** 
- **Decorators:** functools.wraps

---

### `utils\internet_connection.py.__init__`

- **File:** `utils\internet_connection.py`
- **Line:** 22
- **Arguments:** self, timeout
- **Docstring:** Initialize the internet connection tester.

Args:
    timeout (float): Timeout in seconds for connec...

---

### `utils\internet_connection.py.check_internet`

- **File:** `utils\internet_connection.py`
- **Line:** 164
- **Arguments:** 
- **Returns:** bool
- **Docstring:** Alias for is_online() for backward compatibility.

Returns:
    bool: True if internet connection is...

---

### `utils\internet_connection.py.is_online`

- **File:** `utils\internet_connection.py`
- **Line:** 153
- **Arguments:** 
- **Returns:** bool
- **Docstring:** Quick check for internet connectivity using default settings.

Returns:
    bool: True if internet c...

---

### `utils\internet_connection.py.test_connection`

- **File:** `utils\internet_connection.py`
- **Line:** 75
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Test internet connectivity using multiple methods.

Returns:
    bool: True if internet connection i...

---

### `utils\internet_connection.py.test_connection_with_details`

- **File:** `utils\internet_connection.py`
- **Line:** 94
- **Arguments:** self
- **Docstring:** Test internet connectivity and return detailed results.

Returns:
    Tuple[bool, List[str]]: (is_co...

---

### `utils\internet_connection.py.test_http_connection`

- **File:** `utils\internet_connection.py`
- **Line:** 58
- **Arguments:** self, url
- **Returns:** bool
- **Docstring:** Test connection using HTTP request to a specific URL.

Args:
    url (str): URL to test
    
Returns...

---

### `utils\internet_connection.py.test_internet_connection`

- **File:** `utils\internet_connection.py`
- **Line:** 125
- **Arguments:** timeout
- **Returns:** bool
- **Docstring:** Simple function to test internet connectivity.

Args:
    timeout (float): Timeout in seconds for co...

---

### `utils\internet_connection.py.test_internet_connection_detailed`

- **File:** `utils\internet_connection.py`
- **Line:** 139
- **Arguments:** timeout
- **Docstring:** Test internet connectivity with detailed failure information.

Args:
    timeout (float): Timeout in...

---

### `utils\internet_connection.py.test_socket_connection`

- **File:** `utils\internet_connection.py`
- **Line:** 41
- **Arguments:** self, host, port
- **Returns:** bool
- **Docstring:** Test connection using socket to a specific host and port.

Args:
    host (str): Host to connect to
...

---

### `utils\prompts.py.format_auto_model_selection_info`

- **File:** `utils\prompts.py`
- **Line:** 96
- **Arguments:** model
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format auto model selection info message...

---

### `utils\prompts.py.format_conversation_status`

- **File:** `utils\prompts.py`
- **Line:** 101
- **Arguments:** status_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format conversation status message...

---

### `utils\prompts.py.format_error_message`

- **File:** `utils\prompts.py`
- **Line:** 112
- **Arguments:** error_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format error message...

---

### `utils\prompts.py.format_fact_extraction_prompt`

- **File:** `utils\prompts.py`
- **Line:** 89
- **Arguments:** message
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format the fact extraction prompt with the given message...

---

### `utils\prompts.py.format_memory_status`

- **File:** `utils\prompts.py`
- **Line:** 107
- **Arguments:** status_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format memory status message...

---

### `utils\prompts.py.format_status_message`

- **File:** `utils\prompts.py`
- **Line:** 118
- **Arguments:** status_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Format status message...

---

### `utils\prompts.py.get_menu_text`

- **File:** `utils\prompts.py`
- **Line:** 124
- **Arguments:** menu_key
- **Returns:** str
- **Decorators:** staticmethod
- **Docstring:** Get menu text...

---

### `utils\streaming_handler.py.__init__`

- **File:** `utils\streaming_handler.py`
- **Line:** 23
- **Arguments:** self, chat_display, ai_name

---

### `utils\streaming_handler.py._flush_stream_buffer`

- **File:** `utils\streaming_handler.py`
- **Line:** 41
- **Arguments:** self
- **Docstring:** Flush the stream buffer and update the display...

---

### `utils\streaming_handler.py._get_next_message_id`

- **File:** `utils\streaming_handler.py`
- **Line:** 36
- **Arguments:** self
- **Docstring:** Generate a unique message ID...

---

### `utils\streaming_handler.py._render_chat_display`

- **File:** `utils\streaming_handler.py`
- **Line:** 127
- **Arguments:** self
- **Docstring:** Re-render the entire chat display from the message list using tables for alignment and content-width...

---

### `utils\streaming_handler.py._render_chat_display_safe`

- **File:** `utils\streaming_handler.py`
- **Line:** 133
- **Arguments:** self
- **Docstring:** Re-render the chat display safely in the main thread...

---

### `utils\streaming_handler.py._safe_ui_update`

- **File:** `utils\streaming_handler.py`
- **Line:** 279
- **Arguments:** self, update_func
- **Docstring:** Safely update UI in the main thread...

---

### `utils\streaming_handler.py.append_message`

- **File:** `utils\streaming_handler.py`
- **Line:** 60
- **Arguments:** self, sender, content, is_code, tag
- **Docstring:** Append a new message (user or system) and re-render chat display...

---

### `utils\streaming_handler.py.cleanup`

- **File:** `utils\streaming_handler.py`
- **Line:** 384
- **Arguments:** self
- **Docstring:** Clean up safely...

---

### `utils\streaming_handler.py.clear_chat`

- **File:** `utils\streaming_handler.py`
- **Line:** 396
- **Arguments:** self
- **Docstring:** Clear all messages safely...

---

### `utils\streaming_handler.py.edit_message`

- **File:** `utils\streaming_handler.py`
- **Line:** 90
- **Arguments:** self, message_index, new_content
- **Docstring:** Edit a specific message by index...

---

### `utils\streaming_handler.py.finalize_streaming_message`

- **File:** `utils\streaming_handler.py`
- **Line:** 320
- **Arguments:** self
- **Docstring:** Finalize the last streaming message safely...

---

### `utils\streaming_handler.py.get_editable_messages`

- **File:** `utils\streaming_handler.py`
- **Line:** 110
- **Arguments:** self
- **Docstring:** Get list of messages that can be edited (non-streaming, non-system)...

---

### `utils\streaming_handler.py.get_message_by_id`

- **File:** `utils\streaming_handler.py`
- **Line:** 103
- **Arguments:** self, message_id
- **Docstring:** Get message index by message_id...

---

### `utils\streaming_handler.py.get_messages`

- **File:** `utils\streaming_handler.py`
- **Line:** 123
- **Arguments:** self
- **Docstring:** Get all messages as a list of dictionaries...

---

### `utils\streaming_handler.py.remove_streaming_placeholder`

- **File:** `utils\streaming_handler.py`
- **Line:** 366
- **Arguments:** self
- **Docstring:** Remove the last streaming message safely...

---

### `utils\streaming_handler.py.start_streaming_message`

- **File:** `utils\streaming_handler.py`
- **Line:** 76
- **Arguments:** self, sender, tag
- **Docstring:** Append a streaming placeholder message and re-render chat display...

---

### `utils\streaming_handler.py.update_ai_name`

- **File:** `utils\streaming_handler.py`
- **Line:** 408
- **Arguments:** self, ai_name
- **Docstring:** Update the AI name used for thoughts display...

---

### `utils\streaming_handler.py.update_last_system_switch`

- **File:** `utils\streaming_handler.py`
- **Line:** 349
- **Arguments:** self, message
- **Docstring:** Update the last system switch message safely...

---

### `utils\streaming_handler.py.update_streaming_message`

- **File:** `utils\streaming_handler.py`
- **Line:** 298
- **Arguments:** self, content, sender, message_id, is_code, tag
- **Docstring:** Update the last streaming message safely...

---

## 🔗 Relationships

### `MainApp\app_lifecycle.py`

- calls_method:utils\prompts.py.PromptFormatter.format_error_message
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_error
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger

### `MainApp\event_handler.py`

- calls_function:models\conversation_metadata.py.update_personality
- calls_method:utils\prompts.py.PromptFormatter.format_status_message
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_debug
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_error
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:services\ollama_service.py.update_model
- calls_method:utils\prompts.py.PromptFormatter.format_auto_model_selection_info
- calls_function:models\conversation_metadata.py.update_model

### `MainApp\ollama_chat.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:MainApp\ollama_chat.py.showEvent
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `MainApp\service_manager.py`

- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger

### `MainApp\ui_manager.py`

- calls_method:utils\prompts.py.PromptFormatter.get_menu_text
- calls_method:utils\prompts.py.PromptFormatter.format_status_message
- calls_method:ui\styles\tab_styles.py.TabStyles.get_tab_style
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger

### `Personalities\personality_model.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `Personalities\personality_model.py.PersonalityModel`

- inherits_from:Personalities\services\personality_service.py.PersonalityService

### `Personalities\services\personality_loader.py`

- calls_method:Personalities\utils\personality_formatter.py.PersonalityFormatter.validate_personality_data
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger

### `Personalities\services\personality_service.py`

- calls_function:config\config_manager.py.set
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:config\config_manager.py.get

### `Personalities\utils\personality_formatter.py`

- calls_function:config\config_manager.py.get

### `config\config_manager.py`

- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:config\config_manager.py.get

### `controllers\chat_controller.py`

- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_llm_call
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:models\conversation_metadata.py.update_model
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_conversation_detection
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_fact_storage_end
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_json_extraction
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_exception_with_context
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_method:utils\prompts.py.PromptFormatter.format_auto_model_selection_info
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_debug
- calls_function:services\conversation_service.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_fact_extraction_end
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_json_parsing_error
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_fact_skipped
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_fact_storage_start
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_memory_result
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_message_sent
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_fact_processing
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_fact_extraction_start
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:services\ollama_service.py.update_model
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_json_parsing_success
- calls_method:utils\prompts.py.PromptFormatter.format_fact_extraction_prompt
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:controllers\chat_controller.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:controllers\chat_controller.py.remove_emojis
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_fact_storage_summary
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_fact_extraction_result
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_method:utils\prompts.py.PromptFormatter.format_error_message
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_llm_response
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_method:utils\prompts.py.PromptFormatter.format_status_message
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_message_sent_end
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_memory_ltm_status
- calls_function:services\start_up\dependency_checker.py.__init__

### `models\conversation_metadata.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:config\config_manager.py.get
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_method:models\conversation_metadata.py.ConversationMetadata.from_dict
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\Voice_STT_TTS_SERVICES\STT_Service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:utils\Logging\Custom_Logger.py.__new__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__new__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:config\config_manager.py.set
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\Voice_STT_TTS_SERVICES\voice_service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_warning_with_context
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_info_with_context
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:config\config_manager.py.get
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_exception_with_context
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_audio_operation
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.create_voice_process_manager
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\conversation_service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\memory_service.py`

- calls_method:services\memory_service.py.MemoryRetriever.get_relevant_memories
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_memory_operation
- calls_function:services\worker\worker.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_warning_with_context
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_file_operation
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_method:services\memory_service.py.MemoryClassifier.classify_message
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_service_initialization
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_info_with_context
- calls_method:services\memory_service.py.PronounNormalizer.should_normalize
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_exception_with_context
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:config\config_manager.py.set
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_method:services\memory_service.py.MemoryRetriever.calculate_relevance
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_method:services\memory_service.py.PronounNormalizer.normalize_pronouns
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\ollama_service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_performance_metric
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_service_initialization
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_network_request
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_info_with_context
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:config\config_manager.py.get
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_exception_with_context
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_debug
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\semantic_search_service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\start_up\install_dependencies.py`

- calls_function:services\start_up\install_dependencies.py.main
- calls_function:services\start_up\install_dependencies.py.get_version

### `services\summarization_service.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `services\worker\worker.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:config\config_manager.py.get
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Audio_visualisers\eq_orchestrator.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.resizeEvent
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.map_frequency_to_bars
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.resizeEvent
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.band_energy
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.band_energy
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.map_frequency_to_bars
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Audio_visualisers\voice_ring_animation.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.resizeEvent
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.map_frequency_to_bars
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.resizeEvent
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.band_energy
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.band_energy
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.map_frequency_to_bars
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Widgets\chat_navigation.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Widgets\coqui_model_dialog.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Widgets\editable_message_widget.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Widgets\personality_widget.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Widgets\settings_dialog.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Widgets\spellchecker_widget.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.keyPressEvent
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\Widgets\voice_settings_dialog.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:utils\internet_connection.py.test_internet_connection
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\styles\message_formatter.py`

- calls_method:ui\styles\message_formatter.py.MessageFormatter.format_markdown
- calls_method:ui\styles\message_formatter.py.MessageFormatter._protect_code_blocks
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_method:ui\styles\message_formatter.py.MessageFormatter.syntax_highlight_code
- calls_method:ui\styles\message_formatter.py.MessageFormatter.detect_code_type
- calls_method:ui\styles\message_formatter.py.MessageFormatter.detect_and_format_code
- calls_method:ui\styles\message_formatter.py.MessageFormatter.handle_html_tags
- calls_method:ui\styles\message_formatter.py.MessageFormatter.cleanup_message

### `ui\tabs\chat_tab\chat_display.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\tabs\chat_tab\chat_tab.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:config\config_manager.py.get
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\tabs\chat_tab\eq_visualizer.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\tabs\chat_tab\input_controls.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.eventFilter
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\tabs\chat_tab\test_modular_imports.py`

- calls_function:ui\tabs\chat_tab\test_modular_imports.py.test_imports

### `ui\tabs\chat_tab\test_pyside6_imports.py`

- calls_function:ui\tabs\chat_tab\test_pyside6_imports.py.test_component_imports
- calls_function:ui\tabs\chat_tab\test_pyside6_imports.py.test_pyside6_imports

### `ui\tabs\chat_tab\voice_controls.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\tabs\memory_tab.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\tabs\model_tab.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `ui\tabs\personality_tab.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `utils\Logging\Custom_Logger.py`

- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__new__
- calls_function:utils\Logging\Custom_Logger.py.error
- calls_function:utils\Logging\Custom_Logger.py.info
- calls_function:utils\Logging\Custom_Logger.py._sanitize_filename
- calls_function:utils\Logging\Custom_Logger.py.debug
- calls_function:config\config_manager.py.set
- calls_function:utils\Logging\Custom_Logger.py.strip_emojis
- calls_function:utils\Logging\Custom_Logger.py.warning
- calls_function:utils\Logging\Custom_Logger.py.__new__
- calls_function:utils\Logging\Custom_Logger.py.critical

### `utils\Logging\Custom_Logger.py.PrintLogger`

- inherits_from:utils\Logging\Custom_Logger.py.PrintOnLogMixin

### `utils\Logging\logging_helpers.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `utils\complexity_widget.py`

- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_function:services\worker\worker.py.__init__
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

### `utils\error_handler.py`

- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_exception_with_context
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_performance_metric
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_critical_error
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_json_parsing_error
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_network_request
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_memory_operation
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_ui_operation
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_warning_with_context
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_file_operation
- calls_method:utils\Logging\logging_helpers.py.LoggingHelpers.log_audio_operation

### `utils\internet_connection.py`

- calls_function:utils\internet_connection.py.test_internet_connection
- calls_function:utils\internet_connection.py.test_internet_connection_detailed
- calls_function:utils\internet_connection.py.is_online

### `utils\streaming_handler.py`

- calls_method:ui\styles\message_formatter.py.MessageFormatter.format_markdown
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py.__init__
- calls_function:ui\tabs\personality_tab.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_service.py.__init__
- calls_function:Personalities\services\personality_loader.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circle_eq_widget.py.__init__
- calls_function:MainApp\ui_manager.py.__init__
- calls_method:ui\styles\message_formatter.py.MessageFormatter.syntax_highlight_code
- calls_function:services\worker\worker.py.__init__
- calls_method:ui\styles\message_formatter.py.MessageFormatter.detect_and_format_code
- calls_function:ui\tabs\chat_tab\chat_display.py.__init__
- calls_function:ui\Widgets\settings_dialog.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\voice_controls.py.__init__
- calls_function:MainApp\app_lifecycle.py.__init__
- calls_function:ui\Widgets\coqui_model_dialog.py.__init__
- calls_function:utils\complexity_widget.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\STT_Service.py.__init__
- calls_function:ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py.__init__
- calls_function:MainApp\event_handler.py.__init__
- calls_method:utils\Logging\Custom_Logger.py.CustomLogger.get_logger
- calls_function:ui\Audio_visualisers\eq_widgets\bar_eq_widget.py.__init__
- calls_function:ui\tabs\chat_tab\input_controls.py.__init__
- calls_function:ui\Widgets\voice_settings_dialog.py.__init__
- calls_function:controllers\chat_controller.py.__init__
- calls_function:models\conversation_metadata.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\Recording_Service.py.__init__
- calls_function:ui\tabs\chat_tab\chat_tab.py.__init__
- calls_function:ui\Widgets\chat_navigation.py.__init__
- calls_function:ui\Widgets\personality_widget.py.__init__
- calls_function:utils\complexity_analyzer.py.__init__
- calls_function:utils\streaming_handler.py.__init__
- calls_function:services\semantic_search_service.py.__init__
- calls_function:services\summarization_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\coqui_tts_service.py.__init__
- calls_function:ui\Widgets\editable_message_widget.py.__init__
- calls_method:ui\styles\message_formatter.py.MessageFormatter.split_thoughts_and_answer
- calls_function:services\memory_service.py.__init__
- calls_function:services\ollama_service.py.__init__
- calls_function:ui\Audio_visualisers\voice_ring_animation.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\TTS_Service.py.__init__
- calls_function:Personalities\personality_model.py.__init__
- calls_function:services\enhancement_service.py.__init__
- calls_function:services\Voice_STT_TTS_SERVICES\voice_process_manager.py.__init__
- calls_function:ui\Audio_visualisers\eq_orchestrator.py.__init__
- calls_function:ui\tabs\model_tab.py.__init__
- calls_function:utils\internet_connection.py.__init__
- calls_function:ui\tabs\chat_tab\eq_visualizer.py.__init__
- calls_function:ui\tabs\memory_tab.py.__init__
- calls_function:MainApp\ollama_chat.py.__init__
- calls_function:Personalities\services\personality_service.py.__init__
- calls_function:config\config_manager.py.__init__
- calls_function:ui\Widgets\spellchecker_widget.py.__init__
- calls_function:services\start_up\install_dependencies.py.__init__
- calls_function:services\conversation_service.py.__init__
- calls_function:utils\Logging\logging_helpers.py.__init__
- calls_function:MainApp\service_manager.py.__init__
- calls_function:services\start_up\dependency_checker.py.__init__

## 📦 Imports

### `MainApp\__init__.py`

- `app_lifecycle.AppLifecycleManager`
- `event_handler.EventBus`
- `ollama_chat.OllamaChat`
- `service_manager.ServiceManager`
- `ui_manager.UIManager`

### `MainApp\app_lifecycle.py`

- `PySide6.QtCore.Qt`
- `PySide6.QtWidgets.QMainWindow`
- `PySide6.QtWidgets.QMessageBox`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.Logging.logging_helpers.LoggingHelpers`
- `pyside_chat.utils.prompts.PromptFormatter`
- `typing.Optional`

### `MainApp\event_handler.py`

- `PySide6.QtCore.QThread`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtWidgets.QMessageBox`
- `pyside_chat.controllers.chat_controller.ChatController`
- `pyside_chat.services.worker.worker.Worker`
- `pyside_chat.ui.Widgets.settings_dialog.SettingsDialog`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.Logging.logging_helpers.LoggingHelpers`
- `pyside_chat.utils.complexity_analyzer.RequestComplexityAnalyzer`
- `pyside_chat.utils.prompts.PromptFormatter`
- `traceback`
- `typing.Callable`
- `typing.Optional`

### `MainApp\ollama_chat.py`

- `PySide6.QtCore.QEvent`
- `PySide6.QtWidgets.QMainWindow`
- `pyside_chat.MainApp.app_lifecycle.AppLifecycleManager`
- `pyside_chat.MainApp.event_handler.EventBus`
- `pyside_chat.MainApp.service_manager.ServiceManager`
- `pyside_chat.MainApp.ui_manager.UIManager`
- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.controllers.chat_controller.ChatController`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `traceback`

### `MainApp\service_manager.py`

- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.models.conversation_metadata.ConversationManager`
- `pyside_chat.services.conversation_service.ConversationService`
- `pyside_chat.services.enhancement_service.EnhancementService`
- `pyside_chat.services.memory_service.MemoryService`
- `pyside_chat.services.ollama_service.OllamaService`
- `pyside_chat.services.summarization_service.SummarizationService`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `typing.Optional`

### `MainApp\ui_manager.py`

- `PySide6.QtCore.Qt`
- `PySide6.QtGui.QAction`
- `PySide6.QtGui.QIcon`
- `PySide6.QtWidgets.QMainWindow`
- `PySide6.QtWidgets.QMenu`
- `PySide6.QtWidgets.QMenuBar`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QStatusBar`
- `PySide6.QtWidgets.QTabWidget`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.ui.styles.styles.dark_stylesheet`
- `pyside_chat.ui.styles.styles.light_stylesheet`
- `pyside_chat.ui.styles.tab_styles.TabStyles`
- `pyside_chat.ui.tabs.chat_tab.ChatTab`
- `pyside_chat.ui.tabs.memory_tab.MemoryTab`
- `pyside_chat.ui.tabs.model_tab.ModelTab`
- `pyside_chat.ui.tabs.personality_tab.PersonalityTab`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.prompts.PromptFormatter`
- `typing.Optional`

### `Personalities\__init__.py`

- `models.PersonalityConfig`
- `models.PersonalityMetadata`
- `models.PersonalityPrompt`
- `models.PersonalityPronouns`
- `models.PersonalityTraits`
- `models.PersonalityType`
- `personality_model.PersonalityModel`
- `services.personality_loader.PersonalityLoader`
- `services.personality_service.PersonalityService`
- `utils.personality_formatter.PersonalityFormatter`

### `Personalities\models\__init__.py`

- `personality_pronouns.PersonalityPronouns`
- `personality_types.PersonalityConfig`
- `personality_types.PersonalityMetadata`
- `personality_types.PersonalityPrompt`
- `personality_types.PersonalityTraits`
- `personality_types.PersonalityType`

### `Personalities\models\personality_pronouns.py`

- `dataclasses.dataclass`
- `random`
- `typing.List`

### `Personalities\models\personality_types.py`

- `dataclasses.dataclass`
- `enum.Enum`
- `typing.List`

### `Personalities\personality_model.py`

- `models.PersonalityConfig`
- `models.PersonalityMetadata`
- `models.PersonalityPrompt`
- `models.PersonalityPronouns`
- `models.PersonalityTraits`
- `models.PersonalityType`
- `services.personality_service.PersonalityService`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `Personalities\services\__init__.py`

- `personality_loader.PersonalityLoader`
- `personality_service.PersonalityService`

### `Personalities\services\personality_loader.py`

- `dataclasses.asdict`
- `datetime.datetime`
- `json`
- `models.PersonalityConfig`
- `models.PersonalityMetadata`
- `models.PersonalityPrompt`
- `models.PersonalityTraits`
- `os`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `shutil`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `utils.personality_formatter.PersonalityFormatter`

### `Personalities\services\personality_service.py`

- `datetime.datetime`
- `models.PersonalityConfig`
- `models.PersonalityMetadata`
- `models.PersonalityPrompt`
- `models.PersonalityTraits`
- `os`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `services.personality_loader.PersonalityLoader`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `utils.personality_formatter.PersonalityFormatter`

### `Personalities\utils\__init__.py`

- `personality_formatter.PersonalityFormatter`

### `Personalities\utils\personality_formatter.py`

- `models.PersonalityConfig`
- `models.PersonalityMetadata`
- `models.PersonalityPrompt`
- `models.PersonalityPronouns`
- `models.PersonalityTraits`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `config\config_manager.py`

- `json`
- `os`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

### `controllers\chat_controller.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `datetime.datetime`
- `json`
- `os`
- `pyside_chat.models.conversation_metadata.ConversationManager`
- `pyside_chat.services.conversation_service.ConversationService`
- `pyside_chat.services.enhancement_service.EnhancementService`
- `pyside_chat.services.memory_service.MemoryService`
- `pyside_chat.services.ollama_service.OllamaService`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.Logging.logging_helpers.LoggingHelpers`
- `pyside_chat.utils.complexity_analyzer.RequestComplexityAnalyzer`
- `pyside_chat.utils.prompts.PromptFormatter`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `models\conversation_metadata.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `json`
- `os`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `datetime`
- `math`
- `os`
- `pyaudio`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `struct`
- `threading`
- `time`
- `typing.Optional`
- `wave`

### `services\Voice_STT_TTS_SERVICES\STT_Service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `json`
- `os`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `vosk.KaldiRecognizer`
- `vosk.Model`
- `wave`

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `coqui_tts_service.CoquiTTSService`
- `os`
- `platform`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `subprocess`

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QThread`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.QUrl`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtMultimedia.QAudioOutput`
- `PySide6.QtMultimedia.QMediaPlayer`
- `TTS.api.TTS`
- `datetime`
- `io`
- `json`
- `numpy`
- `os`
- `pyaudio`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `queue`
- `re`
- `scipy.signal`
- `sys`
- `tempfile`
- `threading`
- `time`
- `typing.Dict`
- `typing.Generator`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `wave`

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QThread`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Signal`
- `PySide6.QtWidgets.QApplication`
- `multiprocessing`
- `os`
- `pickle`
- `pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service.VoiceService`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `queue`
- `sys`
- `time`
- `traceback`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`

### `services\Voice_STT_TTS_SERVICES\voice_service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.QUrl`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtMultimedia.QAudioOutput`
- `PySide6.QtMultimedia.QMediaPlayer`
- `Recording_Service.RecordingService`
- `STT_Service.STTService`
- `TTS_Service.TTSService`
- `json`
- `os`
- `platform`
- `pyaudio`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.Logging.logging_helpers.LoggingHelpers`
- `speech_recognition`
- `subprocess`
- `tempfile`
- `threading`
- `time`
- `typing.Callable`
- `typing.Optional`
- `wave`

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `voice_process_manager.VoiceProcessManager`
- `voice_process_manager.create_voice_process_manager`
- `voice_service.VoiceService`

### `services\conversation_service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `datetime.datetime`
- `json`
- `os`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `services\enhancement_service.py`

- `typing.Optional`

### `services\memory_service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `datetime.datetime`
- `datetime.timedelta`
- `hashlib`
- `json`
- `os`
- `pyside_chat.services.semantic_search_service.SemanticSearchService`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.Logging.logging_helpers.LoggingHelpers`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

### `services\ollama_service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `json`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.Logging.logging_helpers.LoggingHelpers`
- `requests`
- `subprocess`
- `threading.Thread`
- `time`
- `typing.Dict`
- `typing.Generator`
- `typing.List`
- `typing.Optional`

### `services\semantic_search_service.py`

- `PySide6.QtCore.QMutex`
- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QThread`
- `PySide6.QtCore.Signal`
- `dataclasses.dataclass`
- `datetime.datetime`
- `json`
- `numpy`
- `os`
- `pickle`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `sentence_transformers.SentenceTransformer`
- `sklearn.metrics.pairwise.cosine_similarity`
- `traceback`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `services\start_up\__init__.py`

- `dependency_checker.DependencyChecker`
- `dependency_checker.check_and_install_dependencies`

### `services\start_up\dependency_checker.py`

- `importlib`
- `os`
- `subprocess`
- `sys`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `services\start_up\install_dependencies.py`

- `enchant`
- `os`
- `subprocess`
- `sys`
- `time`
- `tqdm.tqdm`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `services\summarization_service.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `json`
- `pyside_chat.services.ollama_service.OllamaService`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.complexity_analyzer.RequestComplexityAnalyzer`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `services\worker\worker.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QThread`
- `PySide6.QtCore.Signal`
- `json`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `requests`
- `time`
- `traceback`

### `ui\Audio_visualisers\eq_orchestrator.py`

- `PySide6.QtCore.QMetaObject`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtCore.Slot`
- `PySide6.QtGui.QBrush`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QLinearGradient`
- `PySide6.QtGui.QPainter`
- `PySide6.QtGui.QPainterPath`
- `PySide6.QtGui.QPen`
- `PySide6.QtGui.QRadialGradient`
- `PySide6.QtGui.QTransform`
- `PySide6.QtWidgets.QApplication`
- `PySide6.QtWidgets.QCheckBox`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QFileDialog`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QMainWindow`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `math`
- `numpy`
- `os`
- `pyside_chat.ui.Audio_visualisers.eq_widgets.*`
- `random`
- `sounddevice`
- `soundfile`
- `sys`
- `threading`

### `ui\Audio_visualisers\eq_widgets\__init__.py`

- `bar_eq_widget.BarEQWidget`
- `circle_eq_widget.CircleEQWidget`
- `circular_gradient_eq_widget.CircularGradientEQWidget`
- `circular_net_eq_widget.CircularNetEQWidget`

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Slot`
- `PySide6.QtGui.QBrush`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QLinearGradient`
- `PySide6.QtGui.QPainter`
- `PySide6.QtWidgets.QWidget`

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Slot`
- `PySide6.QtGui.QBrush`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QPainter`
- `PySide6.QtGui.QRadialGradient`
- `PySide6.QtWidgets.QWidget`
- `math`

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Slot`
- `PySide6.QtGui.QBrush`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QPainter`
- `PySide6.QtGui.QPainterPath`
- `PySide6.QtGui.QRadialGradient`
- `PySide6.QtWidgets.QWidget`
- `math`
- `random`

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Slot`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QPainter`
- `PySide6.QtWidgets.QWidget`
- `math`
- `random`

### `ui\Audio_visualisers\voice_ring_animation.py`

- `PySide6.QtCore.QMetaObject`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtCore.Slot`
- `PySide6.QtGui.QBrush`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QLinearGradient`
- `PySide6.QtGui.QPainter`
- `PySide6.QtGui.QPainterPath`
- `PySide6.QtGui.QPen`
- `PySide6.QtGui.QRadialGradient`
- `PySide6.QtGui.QTransform`
- `PySide6.QtWidgets.QApplication`
- `PySide6.QtWidgets.QCheckBox`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QFileDialog`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QMainWindow`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `math`
- `numpy`
- `os`
- `random`
- `sounddevice`
- `soundfile`
- `sys`
- `threading`

### `ui\Widgets\__init__.py`

- `chat_navigation.ChatNavigationWidget`
- `editable_message_widget.EditableMessageWidget`

### `ui\Widgets\chat_navigation.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QCursor`
- `PySide6.QtGui.QFont`
- `PySide6.QtGui.QIcon`
- `PySide6.QtWidgets.QFrame`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QInputDialog`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QListWidget`
- `PySide6.QtWidgets.QListWidgetItem`
- `PySide6.QtWidgets.QMenu`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `datetime.datetime`
- `os`
- `pyside_chat.models.conversation_metadata.ConversationManager`
- `pyside_chat.models.conversation_metadata.ConversationMetadata`
- `pyside_chat.services.summarization_service.SummarizationService`
- `time`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `ui\Widgets\coqui_model_dialog.py`

- `PySide6.QtCore.QThread`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QFont`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QDialog`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QListWidget`
- `PySide6.QtWidgets.QListWidgetItem`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QProgressBar`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QSplitter`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `datetime.datetime`
- `os`
- `pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service.CoquiTTSService`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `ui\Widgets\editable_message_widget.py`

- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QTextCursor`
- `PySide6.QtWidgets.QFrame`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`

### `ui\Widgets\personality_widget.py`

- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtWidgets.QCheckBox`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QFormLayout`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QLineEdit`
- `PySide6.QtWidgets.QListWidget`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QSpinBox`
- `PySide6.QtWidgets.QSplitter`
- `PySide6.QtWidgets.QTabWidget`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `pyside_chat.Personalities.personality_model.PersonalityConfig`
- `pyside_chat.Personalities.personality_model.PersonalityMetadata`
- `pyside_chat.Personalities.personality_model.PersonalityModel`
- `pyside_chat.Personalities.personality_model.PersonalityPrompt`
- `pyside_chat.Personalities.personality_model.PersonalityTraits`
- `typing.Dict`
- `typing.List`

### `ui\Widgets\settings_dialog.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtWidgets.QCheckBox`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QDialog`
- `PySide6.QtWidgets.QFormLayout`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QSpinBox`
- `PySide6.QtWidgets.QTabWidget`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `pyside_chat.config.config_manager.ConfigManager`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`

### `ui\Widgets\spellchecker_widget.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtGui.QAction`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QTextCharFormat`
- `PySide6.QtGui.QTextCursor`
- `PySide6.QtWidgets.QMenu`
- `PySide6.QtWidgets.QTextEdit`
- `enchant`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `re`

### `ui\Widgets\voice_settings_dialog.py`

- `PySide6.QtCore.QThread`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QFont`
- `PySide6.QtWidgets.QCheckBox`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QDialog`
- `PySide6.QtWidgets.QDoubleSpinBox`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QProgressBar`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QSpinBox`
- `PySide6.QtWidgets.QTabWidget`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `math`
- `os`
- `pyaudio`
- `pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service.CoquiTTSService`
- `pyside_chat.ui.Widgets.coqui_model_dialog.ModelDownloadThread`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.internet_connection.test_internet_connection`
- `struct`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `ui\styles\message_formatter.py`

- `html.escape`
- `html.unescape`
- `pygments.formatters.HtmlFormatter`
- `pygments.highlight`
- `pygments.lexers.get_lexer_by_name`
- `pygments.lexers.guess_lexer`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `re`

### `ui\tabs\__init__.py`

- `chat_tab.chat_tab.ChatTab`
- `memory_tab.MemoryTab`
- `model_tab.ModelTab`
- `personality_tab.PersonalityTab`

### `ui\tabs\chat_tab\__init__.py`

- `chat_display.ChatDisplay`
- `chat_tab.ChatTab`
- `eq_visualizer.EQVisualizer`
- `input_controls.InputControls`
- `voice_controls.VoiceControls`

### `ui\tabs\chat_tab\chat_display.py`

- `PySide6.QtCore.QEvent`
- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QTextCursor`
- `PySide6.QtWidgets.QDialog`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QScrollArea`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `logging`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.streaming_handler.StreamingHandler`
- `typing.Optional`

### `ui\tabs\chat_tab\chat_tab.py`

- `PySide6.QtCore.QEvent`
- `PySide6.QtCore.QMutex`
- `PySide6.QtCore.QThread`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.QWaitCondition`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtWidgets.QApplication`
- `PySide6.QtWidgets.QDialog`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QScrollArea`
- `PySide6.QtWidgets.QSplitter`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `chat_display.ChatDisplay`
- `eq_visualizer.EQVisualizer`
- `input_controls.InputControls`
- `json`
- `logging`
- `os`
- `pyside_chat.models.conversation_metadata.ConversationMetadata`
- `pyside_chat.services.conversation_service.ConversationService`
- `pyside_chat.services.ollama_service.OllamaService`
- `pyside_chat.ui.Widgets.chat_navigation.ChatNavigationWidget`
- `pyside_chat.ui.Widgets.voice_settings_dialog.VoiceSettingsDialog`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `sys`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `voice_controls.VoiceControls`

### `ui\tabs\chat_tab\eq_visualizer.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Signal`
- `PySide6.QtWidgets.QApplication`
- `PySide6.QtWidgets.QScrollArea`
- `PySide6.QtWidgets.QWidget`
- `logging`
- `pyside_chat.ui.Audio_visualisers.eq_widgets.bar_eq_widget.BarEQWidget`
- `pyside_chat.ui.Audio_visualisers.eq_widgets.circle_eq_widget.CircleEQWidget`
- `pyside_chat.ui.Audio_visualisers.eq_widgets.circular_gradient_eq_widget.CircularGradientEQWidget`
- `pyside_chat.ui.Audio_visualisers.eq_widgets.circular_net_eq_widget.CircularNetEQWidget`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `random`
- `traceback`
- `typing.Dict`
- `typing.Optional`

### `ui\tabs\chat_tab\input_controls.py`

- `PySide6.QtCore.QEvent`
- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtWidgets.QApplication`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QSlider`
- `PySide6.QtWidgets.QSpinBox`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `logging`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `typing.Dict`
- `typing.Optional`

### `ui\tabs\chat_tab\test_modular_imports.py`

- `chat_display.ChatDisplay`
- `chat_tab.ChatTab`
- `eq_visualizer.EQVisualizer`
- `input_controls.InputControls`
- `voice_controls.VoiceControls`

### `ui\tabs\chat_tab\test_pyside6_imports.py`

- `PySide6.QtCore.Qt`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QProgressBar`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QScrollArea`
- `PySide6.QtWidgets.QSlider`
- `PySide6.QtWidgets.QSpinBox`
- `PySide6.QtWidgets.QSplitter`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `chat_display.ChatDisplay`
- `chat_tab.ChatTab`
- `eq_visualizer.EQVisualizer`
- `input_controls.InputControls`
- `voice_controls.VoiceControls`

### `ui\tabs\chat_tab\voice_controls.py`

- `PySide6.QtCore.QMutex`
- `PySide6.QtCore.QMutexLocker`
- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QProgressBar`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `logging`
- `pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service.VoiceService`
- `pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service_wrapper.VoiceServiceWrapper`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `time`
- `traceback`
- `typing.Dict`
- `typing.Optional`

### `ui\tabs\memory_tab.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QFont`
- `PySide6.QtWidgets.QCheckBox`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QHeaderView`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QLineEdit`
- `PySide6.QtWidgets.QListWidget`
- `PySide6.QtWidgets.QListWidgetItem`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QProgressBar`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QSlider`
- `PySide6.QtWidgets.QSpinBox`
- `PySide6.QtWidgets.QSplitter`
- `PySide6.QtWidgets.QTabWidget`
- `PySide6.QtWidgets.QTableWidget`
- `PySide6.QtWidgets.QTableWidgetItem`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `datetime.datetime`
- `hashlib`
- `pyside_chat.services.memory_service.MemoryEntry`
- `pyside_chat.services.memory_service.MemoryService`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `typing.Dict`

### `ui\tabs\model_tab.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QFont`
- `PySide6.QtGui.QTextCursor`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QLineEdit`
- `PySide6.QtWidgets.QListWidget`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QProgressBar`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QSplitter`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `datetime.datetime`
- `pyside_chat.services.ollama_service.OllamaService`

### `ui\tabs\personality_tab.py`

- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtWidgets.QCheckBox`
- `PySide6.QtWidgets.QComboBox`
- `PySide6.QtWidgets.QFormLayout`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QLineEdit`
- `PySide6.QtWidgets.QListWidget`
- `PySide6.QtWidgets.QMessageBox`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QSpinBox`
- `PySide6.QtWidgets.QSplitter`
- `PySide6.QtWidgets.QTabWidget`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `datetime.datetime`
- `pyside_chat.Personalities.personality_model.PersonalityConfig`
- `pyside_chat.Personalities.personality_model.PersonalityMetadata`
- `pyside_chat.Personalities.personality_model.PersonalityModel`
- `pyside_chat.Personalities.personality_model.PersonalityPrompt`
- `pyside_chat.Personalities.personality_model.PersonalityTraits`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`

### `utils\Logging\Custom_Logger.py`

- `json`
- `logging`
- `os`
- `re`

### `utils\Logging\logging_helpers.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QThread`
- `PySide6.QtCore.Signal`
- `logging`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `threading`
- `time`
- `traceback`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

### `utils\__init__.py`

- `internet_connection.InternetConnectionTester`
- `internet_connection.check_internet`
- `internet_connection.is_online`
- `internet_connection.test_internet_connection`
- `internet_connection.test_internet_connection_detailed`
- `pyside_chat.services.start_up.dependency_checker.DependencyChecker`
- `pyside_chat.services.start_up.dependency_checker.check_and_install_dependencies`

### `utils\complexity_analyzer.py`

- `dataclasses.dataclass`
- `enum.Enum`
- `json`
- `re`
- `requests`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

### `utils\complexity_widget.py`

- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Qt`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QFont`
- `PySide6.QtGui.QPalette`
- `PySide6.QtWidgets.QFrame`
- `PySide6.QtWidgets.QGroupBox`
- `PySide6.QtWidgets.QHBoxLayout`
- `PySide6.QtWidgets.QLabel`
- `PySide6.QtWidgets.QProgressBar`
- `PySide6.QtWidgets.QPushButton`
- `PySide6.QtWidgets.QTextEdit`
- `PySide6.QtWidgets.QVBoxLayout`
- `PySide6.QtWidgets.QWidget`
- `pyside_chat.utils.complexity_analyzer.ComplexityLevel`
- `pyside_chat.utils.complexity_analyzer.RequestComplexityAnalyzer`

### `utils\error_handler.py`

- `contextlib.contextmanager`
- `functools`
- `json`
- `os`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `pyside_chat.utils.Logging.logging_helpers.LoggingHelpers`
- `requests`
- `time`
- `traceback`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `typing.Type`
- `typing.Union`

### `utils\internet_connection.py`

- `socket`
- `time`
- `typing.List`
- `typing.Tuple`
- `urllib.error`
- `urllib.request`

### `utils\prompts.py`

- `typing.Any`
- `typing.Dict`

### `utils\streaming_handler.py`

- `PySide6.QtCore.QObject`
- `PySide6.QtCore.QThread`
- `PySide6.QtCore.QTimer`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QColor`
- `PySide6.QtGui.QTextCharFormat`
- `PySide6.QtGui.QTextCursor`
- `PySide6.QtWidgets.QApplication`
- `PySide6.QtWidgets.QTextEdit`
- `html.escape`
- `pyside_chat.ui.styles.message_formatter.MessageFormatter`
- `pyside_chat.utils.Logging.Custom_Logger.CustomLogger`
- `time`
- `traceback`

## 📞 Function Call Analysis

### `MainApp\app_lifecycle.py`

**Function Calls:**
- `QMessageBox`
- `hasattr`
- `str`

### `MainApp\event_handler.py`

**Function Calls:**
- `ChatController`
- `QMessageBox`
- `QThread`
- `QTimer`
- `RequestComplexityAnalyzer`
- `SettingsDialog`
- `Worker`
- `hasattr`
- `id`
- `len`
- `objectName`
- `str`
- `update_model`
- `update_personality`

### `MainApp\ollama_chat.py`

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

### `MainApp\service_manager.py`

**Function Calls:**
- `ConversationManager`
- `ConversationService`
- `EnhancementService`
- `MemoryService`
- `OllamaService`
- `SummarizationService`

### `MainApp\ui_manager.py`

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

### `Personalities\models\personality_pronouns.py`

**Function Calls:**
- `isinstance`
- `join`
- `len`

### `Personalities\personality_model.py`

**Function Calls:**
- `__init__`
- `super`

### `Personalities\services\personality_loader.py`

**Function Calls:**
- `PersonalityConfig`
- `PersonalityMetadata`
- `asdict`
- `isoformat`
- `len`
- `open`
- `sorted`
- `strftime`

### `Personalities\services\personality_service.py`

**Function Calls:**
- `PersonalityConfig`
- `PersonalityFormatter`
- `PersonalityLoader`
- `PersonalityMetadata`
- `get`
- `hasattr`
- `isoformat`
- `list`
- `lower`
- `set`
- `setattr`
- `sorted`

### `Personalities\utils\personality_formatter.py`

**Function Calls:**
- `PersonalityConfig`
- `PersonalityMetadata`
- `PersonalityPrompt`
- `PersonalityPronouns`
- `PersonalityTraits`
- `enumerate`
- `get`
- `join`

### `config\config_manager.py`

**Function Calls:**
- `get`
- `isinstance`
- `open`

### `controllers\chat_controller.py`

**Function Calls:**
- `RequestComplexityAnalyzer`
- `Signal`
- `__init__`
- `hasattr`
- `isinstance`
- `join`
- `len`
- `remove_emojis`
- `str`
- `strftime`
- `strip`
- `super`
- `type`
- `update_model`

### `models\conversation_metadata.py`

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

### `services\Voice_STT_TTS_SERVICES\Recording_Service.py`

**Function Calls:**
- `Signal`
- `__init__`
- `join`
- `len`
- `max`
- `str`
- `strftime`
- `sum`
- `super`

### `services\Voice_STT_TTS_SERVICES\STT_Service.py`

**Function Calls:**
- `Exception`
- `KaldiRecognizer`
- `Model`
- `Signal`
- `__init__`
- `join`
- `len`
- `print`
- `str`
- `strip`
- `super`

### `services\Voice_STT_TTS_SERVICES\TTS_Service.py`

**Function Calls:**
- `CoquiTTSService`
- `Signal`
- `__init__`
- `int`
- `len`
- `max`
- `min`
- `str`
- `super`

### `services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`

**Function Calls:**
- `QAudioOutput`
- `QMediaPlayer`
- `QThread`
- `QTimer`
- `Signal`
- `StreamingAudioPlayer`
- `StreamingAudioWorker`
- `TTS`
- `__init__`
- `__new__`
- `any`
- `enumerate`
- `hasattr`
- `int`
- `isinstance`
- `len`
- `list`
- `max`
- `min`
- `open`
- `print`
- `set`
- `setattr`
- `str`
- `strftime`
- `sum`
- `super`

### `services\Voice_STT_TTS_SERVICES\voice_process_manager.py`

**Function Calls:**
- `QApplication`
- `Signal`
- `VoiceProcessManager`
- `VoiceProcessMonitor`
- `VoiceService`
- `__init__`
- `hasattr`
- `id`
- `objectName`
- `str`
- `super`

### `services\Voice_STT_TTS_SERVICES\voice_service.py`

**Function Calls:**
- `Exception`
- `QTimer`
- `RecordingService`
- `STTService`
- `Signal`
- `TTSService`
- `__init__`
- `get`
- `getattr`
- `hasattr`
- `int`
- `len`
- `max`
- `min`
- `str`
- `super`

### `services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`

**Function Calls:**
- `Signal`
- `VoiceService`
- `__init__`
- `create_voice_process_manager`
- `super`

### `services\conversation_service.py`

**Function Calls:**
- `Signal`
- `__init__`
- `isinstance`
- `isoformat`
- `len`
- `min`
- `open`
- `strftime`
- `super`

### `services\enhancement_service.py`

**Function Calls:**
- `endswith`
- `len`
- `reversed`

### `services\memory_service.py`

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

### `services\ollama_service.py`

**Function Calls:**
- `Exception`
- `Signal`
- `Thread`
- `__init__`
- `get`
- `insert`
- `isinstance`
- `iter`
- `join`
- `len`
- `map`
- `next`
- `reversed`
- `str`
- `super`

### `services\semantic_search_service.py`

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

### `services\start_up\dependency_checker.py`

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

### `services\start_up\install_dependencies.py`

**Function Calls:**
- `DependencyInstaller`
- `__import__`
- `enumerate`
- `get_version`
- `getattr`
- `hasattr`
- `input`
- `len`
- `lower`
- `main`
- `print`
- `replace`
- `split`
- `str`
- `strip`
- `tqdm`

### `services\summarization_service.py`

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

### `services\worker\worker.py`

**Function Calls:**
- `Signal`
- `__init__`
- `get`
- `id`
- `len`
- `objectName`
- `str`
- `super`

### `ui\Audio_visualisers\eq_orchestrator.py`

**Function Calls:**
- `BarEQWidget`
- `CircleEQWidget`
- `CircularGradientEQWidget`
- `CircularNetEQWidget`
- `MainWindow`
- `QApplication`
- `QCheckBox`
- `QComboBox`
- `QHBoxLayout`
- `QLabel`
- `QPushButton`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `band_energy`
- `bool`
- `enumerate`
- `float`
- `hasattr`
- `int`
- `join`
- `len`
- `map_frequency_to_bars`
- `max`
- `min`
- `print`
- `range`
- `resizeEvent`
- `setStyleSheet`
- `super`

### `ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`

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

### `ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`

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

### `ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`

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

### `ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`

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

### `ui\Audio_visualisers\voice_ring_animation.py`

**Function Calls:**
- `BarEQWidget`
- `CircleEQWidget`
- `CircularGradientEQWidget`
- `CircularNetEQWidget`
- `MainWindow`
- `QApplication`
- `QBrush`
- `QCheckBox`
- `QColor`
- `QComboBox`
- `QHBoxLayout`
- `QLabel`
- `QLinearGradient`
- `QPainter`
- `QPainterPath`
- `QPen`
- `QPushButton`
- `QRadialGradient`
- `QTimer`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `Slot`
- `__init__`
- `band_energy`
- `bool`
- `enumerate`
- `float`
- `hasattr`
- `int`
- `isinstance`
- `join`
- `len`
- `map_frequency_to_bars`
- `max`
- `min`
- `print`
- `range`
- `resizeEvent`
- `setStyleSheet`
- `sum`
- `super`

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

### `ui\Widgets\coqui_model_dialog.py`

**Function Calls:**
- `CoquiTTSService`
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

### `ui\Widgets\editable_message_widget.py`

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

### `ui\Widgets\personality_widget.py`

**Function Calls:**
- `PersonalityConfig`
- `PersonalityMetadata`
- `PersonalityModel`
- `PersonalityPrompt`
- `PersonalityTraits`
- `QCheckBox`
- `QComboBox`
- `QFormLayout`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QLineEdit`
- `QListWidget`
- `QPushButton`
- `QSpinBox`
- `QTabWidget`
- `QTextEdit`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `enumerate`
- `join`
- `range`
- `sorted`
- `split`
- `str`
- `strip`
- `super`

### `ui\Widgets\settings_dialog.py`

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

### `ui\Widgets\voice_settings_dialog.py`

**Function Calls:**
- `CoquiTTSService`
- `InternetCheckThread`
- `ModelDownloadThread`
- `QCheckBox`
- `QComboBox`
- `QDoubleSpinBox`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QPushButton`
- `QSpinBox`
- `QTabWidget`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `__init__`
- `float`
- `getattr`
- `hasattr`
- `int`
- `len`
- `range`
- `replace`
- `split`
- `str`
- `sum`
- `super`
- `test_internet_connection`

### `ui\styles\message_formatter.py`

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

### `ui\tabs\chat_tab\chat_display.py`

**Function Calls:**
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
- `hasattr`
- `len`
- `mouseMoveEvent`
- `startswith`
- `strip`
- `super`

### `ui\tabs\chat_tab\chat_tab.py`

**Function Calls:**
- `ChatDisplay`
- `ChatNavigationWidget`
- `EQVisualizer`
- `InputControls`
- `QHBoxLayout`
- `QSplitter`
- `QVBoxLayout`
- `QWidget`
- `Signal`
- `VoiceControls`
- `VoiceSettingsDialog`
- `__init__`
- `get`
- `hasattr`
- `hide`
- `int`
- `isEnabled`
- `isVisible`
- `open`
- `range`
- `setEnabled`
- `setValue`
- `setVisible`
- `setattr`
- `show`
- `str`
- `super`
- `update`

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
- `strip`
- `super`

### `ui\tabs\chat_tab\test_modular_imports.py`

**Function Calls:**
- `print`
- `test_imports`

### `ui\tabs\chat_tab\test_pyside6_imports.py`

**Function Calls:**
- `print`
- `test_component_imports`
- `test_pyside6_imports`

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
- `VoiceService`
- `VoiceServiceWrapper`
- `__init__`
- `any`
- `hasattr`
- `int`
- `max`
- `min`
- `super`

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
- `QComboBox`
- `QFormLayout`
- `QGroupBox`
- `QHBoxLayout`
- `QLabel`
- `QLineEdit`
- `QListWidget`
- `QPushButton`
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

### `utils\Logging\Custom_Logger.py`

**Function Calls:**
- `DummyLogger`
- `__new__`
- `_sanitize_filename`
- `critical`
- `debug`
- `error`
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

### `utils\Logging\logging_helpers.py`

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

### `utils\complexity_analyzer.py`

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

### `utils\complexity_widget.py`

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

### `utils\error_handler.py`

**Function Calls:**
- `func`
- `hasattr`
- `isinstance`
- `open`
- `range`
- `str`
- `type`

### `utils\internet_connection.py`

**Function Calls:**
- `InternetConnectionTester`
- `is_online`
- `print`
- `test_internet_connection`
- `test_internet_connection_detailed`

### `utils\prompts.py`

**Function Calls:**
- `format`

### `utils\streaming_handler.py`

**Function Calls:**
- `QTimer`
- `Signal`
- `__init__`
- `enumerate`
- `escape`
- `join`
- `len`
- `objectName`
- `range`
- `reversed`
- `startswith`
- `strip`
- `super`
- `update_func`


### Method Calls

**`MainApp\app_lifecycle.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_error`
- `PromptFormatter.format_error_message`
- `QMessageBox.critical`
- `chat_tab.voice_service.cleanup_on_exit`
- `conversation_manager.auto_save_conversation`
- `conversation_service.get_messages`
- `event.accept`
- `logger.error`
- `logger.info`
- `msg_box.exec`
- `msg_box.setIcon`
- `msg_box.setText`
- `msg_box.setTextFormat`
- `msg_box.setTextInteractionFlags`
- `msg_box.setWindowTitle`
- `ollama_service.test_connection`
- `self._show_initialization_error`
- `self.event_handler._on_refresh_models`
- `self.event_handler.cleanup_on_exit`
- `self.main_window.height`
- `self.main_window.resize`
- `self.main_window.width`
- `self.service_manager.cleanup`
- `self.service_manager.config_manager.get`
- `self.service_manager.config_manager.get_window_size`
- `self.service_manager.config_manager.set_window_size`
- `self.service_manager.get_conversation_manager`
- `self.service_manager.get_conversation_service`
- `self.service_manager.get_ollama_service`
- `self.ui_manager.apply_theme`
- `self.ui_manager.get_chat_tab`

**`MainApp\event_handler.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_debug`
- `LoggingHelpers.log_error`
- `PromptFormatter.format_auto_model_selection_info`
- `PromptFormatter.format_status_message`
- `QMessageBox.critical`
- `QThread.currentThread`
- `QTimer.singleShot`
- `about_action.triggered.connect`
- `analyzer.analyze_complexity`
- `analyzer.get_model_recommendation`
- `chat_tab.append_response_signal.connect`
- `chat_tab.append_response_signal.emit`
- `chat_tab.append_to_chat`
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
- `chat_tab.on_message_cancelled`
- `chat_tab.on_personality_changed`
- `chat_tab.personality_combo.setCurrentText`
- `chat_tab.refresh_navigation`
- `chat_tab.save_chat`
- `chat_tab.set_current_conversation_file`
- `chat_tab.stop_streaming`
- `chat_tab.update_model_list`
- `chat_tab.update_personality_list`
- `clear_chat_action.triggered.connect`
- `config_manager.get_frequency_penalty`
- `config_manager.get_max_tokens`
- `config_manager.get_ollama_url`
- `config_manager.get_presence_penalty`
- `config_manager.get_top_p`
- `conversation_manager.get_current_metadata`
- `conversation_manager.load_conversation`
- `conversation_manager.metadata_updated.connect`
- `conversation_service.add_message`
- `conversation_service.clear_conversation`
- `conversation_service.get_context_messages`
- `conversation_service.get_messages`
- `dialog.exec`
- `error.lower`
- `exit_action.triggered.connect`
- `final_context.append`
- `final_context.extend`
- `load_chat_action.triggered.connect`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `memory_service.get_context_messages`
- `metadata.get_display_info`
- `model_tab.append_status`
- `model_tab.model_pull_requested.connect`
- `model_tab.model_remove_requested.connect`
- `model_tab.model_update_requested.connect`
- `model_tab.update_model_list`
- `msg.get`
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
- `personality_tab.get_available_personalities`
- `personality_tab.personality_changed.connect`
- `personality_tab.personality_model.build_comprehensive_system_prompt`
- `personality_tab.personality_model.get_available_personalities`
- `personality_tab.personality_model.get_user_context_messages`
- `refresh_models_action.triggered.connect`
- `save_chat_action.triggered.connect`
- `self._check_ollama_connection`
- `self._cleanup_worker_thread`
- `self._cleanup_worker_thread_once`
- `self._connect_menu_actions`
- `self._create_chat_controller`
- `self._create_worker_thread`
- `self._final_worker_cleanup`
- `self._on_new_conversation`
- `self._on_refresh_models`
- `self._on_refresh_personalities`
- `self._on_worker_finished`
- `self._send_to_ollama`
- `self._setup_connections`
- `self._setup_ui_with_new_services`
- `self._show_ollama_connection_error`
- `self._start_worker_stream`
- `self.chat_controller.accumulate_assistant_response`
- `self.chat_controller.conversation_updated.connect`
- `self.chat_controller.delete_conversation`
- `self.chat_controller.error_occurred.connect`
- `self.chat_controller.is_memory_active`
- `self.chat_controller.load_conversation`
- `self.chat_controller.name_generation_requested.connect`
- `self.chat_controller.process_user_message`
- `self.chat_controller.start_new_conversation`
- `self.chat_controller.status_updated.connect`
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
- `self.setup_connections`
- `self.ui_manager.get_chat_tab`
- `self.ui_manager.get_menu_action`
- `self.ui_manager.get_model_tab`
- `self.ui_manager.get_personality_tab`
- `self.ui_manager.show_about_dialog`
- `self.ui_manager.show_clear_chat_dialog`
- `self.ui_manager.update_status`
- `self.worker.error_signal.connect`
- `self.worker.error_signal.emit`
- `self.worker.finished_signal.connect`
- `self.worker.get_stats`
- `self.worker.moveToThread`
- `self.worker.run_stream`
- `self.worker.stop`
- `self.worker.stream_chunk_signal.connect`
- `self.worker.update_message_signal.connect`
- `self.worker_thread.deleteLater`
- `self.worker_thread.finished.connect`
- `self.worker_thread.isRunning`
- `self.worker_thread.quit`
- `self.worker_thread.setObjectName`
- `self.worker_thread.start`
- `self.worker_thread.started.connect`
- `self.worker_thread.wait`
- `settings_action.triggered.connect`
- `summarization_service.generate_chat_name`
- `traceback.format_exc`

**`MainApp\ollama_chat.py`:**
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

**`MainApp\service_manager.py`:**
- `CustomLogger.get_logger`
- `logger.error`
- `logger.info`
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
- `self.conversation_service.set_memory_service`
- `self.session_variables.copy`

**`MainApp\ui_manager.py`:**
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

**`Personalities\models\personality_pronouns.py`:**
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

**`Personalities\personality_model.py`:**
- `self._initialize_personalities`
- `self.loader.extract_personality_name`
- `self.loader.find_personality_file_by_name`
- `self.loader.find_personality_files`
- `self.loader.save_personality_to_file`

**`Personalities\services\personality_loader.py`:**
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

**`Personalities\services\personality_service.py`:**
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

**`Personalities\utils\personality_formatter.py`:**
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

**`controllers\chat_controller.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_conversation_detection`
- `LoggingHelpers.log_debug`
- `LoggingHelpers.log_exception_with_context`
- `LoggingHelpers.log_fact_extraction_end`
- `LoggingHelpers.log_fact_extraction_result`
- `LoggingHelpers.log_fact_extraction_start`
- `LoggingHelpers.log_fact_processing`
- `LoggingHelpers.log_fact_skipped`
- `LoggingHelpers.log_fact_storage_end`
- `LoggingHelpers.log_fact_storage_start`
- `LoggingHelpers.log_fact_storage_summary`
- `LoggingHelpers.log_json_extraction`
- `LoggingHelpers.log_json_parsing_error`
- `LoggingHelpers.log_json_parsing_success`
- `LoggingHelpers.log_llm_call`
- `LoggingHelpers.log_llm_response`
- `LoggingHelpers.log_memory_ltm_status`
- `LoggingHelpers.log_memory_result`
- `LoggingHelpers.log_message_sent`
- `LoggingHelpers.log_message_sent_end`
- `PromptFormatter.format_auto_model_selection_info`
- `PromptFormatter.format_error_message`
- `PromptFormatter.format_fact_extraction_prompt`
- `PromptFormatter.format_status_message`
- `analyzer.analyze_complexity`
- `analyzer.get_model_recommendation`
- `conversation.copy`
- `datetime.now`
- `emoji_pattern.sub`
- `facts.items`
- `json.loads`
- `json_match.group`
- `key.strip`
- `logger.debug`
- `logger.error`
- `message.strip`
- `metadata.get_display_info`
- `msg.get`
- `new_filepath.split`
- `old_filepath.split`
- `os.path.join`
- `re.compile`
- `re.search`
- `re.sub`
- `result.get`
- `self._build_context`
- `self._chat_tab_reference.speak_ai_response`
- `self._detect_new_conversation`
- `self._extract_and_store_facts`
- `self._extract_facts_with_llm`
- `self._handle_memory_operations`
- `self._select_model`
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
- `self.conversation_service.get_messages`
- `self.conversation_updated.emit`
- `self.error_occurred.emit`
- `self.is_memory_active`
- `self.memory_service.add_fact`
- `self.memory_service.get_context_messages`
- `self.memory_service.intelligent_add_message`
- `self.message_received.emit`
- `self.message_sent.emit`
- `self.name_generation_requested.emit`
- `self.ollama_service.get_models`
- `self.ollama_service.send_chat_message`
- `self.start_new_conversation`
- `self.status_updated.emit`
- `value.strip`

**`models\conversation_metadata.py`:**
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

**`services\Voice_STT_TTS_SERVICES\Recording_Service.py`:**
- `CustomLogger.get_logger`
- `datetime.datetime.now`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `math.log10`
- `math.sqrt`
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

**`services\Voice_STT_TTS_SERVICES\STT_Service.py`:**
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
- `wave.open`
- `wf.close`
- `wf.getframerate`
- `wf.readframes`

**`services\Voice_STT_TTS_SERVICES\TTS_Service.py`:**
- `CustomLogger.get_logger`
- `QTimer.singleShot`
- `logger.debug`
- `logger.error`
- `logger.info`
- `platform.system`
- `self._check_availability`
- `self._speak_with_espeak`
- `self.coqui_service.audio_level_changed.connect`
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

**`services\Voice_STT_TTS_SERVICES\coqui_tts_service.py`:**
- `CustomLogger.get_logger`
- `QTimer.singleShot`
- `QUrl.fromLocalFile`
- `all_models.append`
- `audio.astype`
- `audio_chunk.astype`
- `cache_dirs.append`
- `cached_data.get`
- `config.get`
- `datetime.datetime.now`
- `downloaded.add`
- `f.endswith`
- `item.replace`
- `json.load`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `model_name.lower`
- `model_name.replace`
- `model_name.startswith`
- `np.abs`
- `np.array`
- `np.clip`
- `np.max`
- `np.mean`
- `np.sqrt`
- `os.environ.get`
- `os.getcwd`
- `os.listdir`
- `os.makedirs`
- `os.path.exists`
- `os.path.expanduser`
- `os.path.isdir`
- `os.path.join`
- `os.remove`
- `part.strip`
- `processed_audio.tobytes`
- `pyaudio.PyAudio`
- `re.split`
- `s.strip`
- `seen_models.add`
- `self._adjust_audio_speed`
- `self._cleanup_audio_file`
- `self._generate_audio`
- `self._generate_audio_chunk`
- `self._get_tts_model_cache_dirs`
- `self._initialize_service`
- `self._is_model_fully_downloaded`
- `self._load_default_model`
- `self._loaded_models.clear`
- `self._loaded_models.keys`
- `self._model_name_to_folder`
- `self._play_audio`
- `self._process_audio_chunk`
- `self._speak_text_streaming`
- `self._split_text_into_sentences`
- `self.audio_chunk_ready.emit`
- `self.audio_level_buffer.append`
- `self.audio_level_buffer.pop`
- `self.audio_level_changed.emit`
- `self.audio_level_timer.isActive`
- `self.audio_level_timer.setInterval`
- `self.audio_level_timer.start`
- `self.audio_level_timer.stop`
- `self.audio_level_timer.timeout.connect`
- `self.audio_output.setVolume`
- `self.audio_queue.append`
- `self.audio_queue.pop`
- `self.clear_model_cache`
- `self.get_comprehensive_model_list`
- `self.get_downloaded_models`
- `self.get_model_config`
- `self.get_model_download_size`
- `self.is_available`
- `self.is_model_downloaded`
- `self.load_model`
- `self.media_player.mediaStatusChanged.connect`
- `self.media_player.play`
- `self.media_player.setAudioOutput`
- `self.media_player.setSource`
- `self.media_player.stop`
- `self.model_loaded.emit`
- `self.playback_error.emit`
- `self.playback_finished.emit`
- `self.progress_updated.emit`
- `self.pyaudio.open`
- `self.pyaudio.terminate`
- `self.stop_playback`
- `self.stream.close`
- `self.stream.stop_stream`
- `self.stream.write`
- `self.streaming_error.emit`
- `self.streaming_finished.emit`
- `self.streaming_player.audio_level_changed.connect`
- `self.streaming_player.cleanup`
- `self.streaming_player.end_stream`
- `self.streaming_player.isRunning`
- `self.streaming_player.playback_error.connect`
- `self.streaming_player.playback_finished.connect`
- `self.streaming_player.quit`
- `self.streaming_player.set_volume`
- `self.streaming_player.start`
- `self.streaming_player.stop_playback`
- `self.streaming_player.terminate`
- `self.streaming_player.wait`
- `self.streaming_thread.deleteLater`
- `self.streaming_thread.isRunning`
- `self.streaming_thread.quit`
- `self.streaming_thread.start`
- `self.streaming_thread.started.connect`
- `self.streaming_thread.terminate`
- `self.streaming_thread.wait`
- `self.streaming_worker.audio_chunk_ready.connect`
- `self.streaming_worker.moveToThread`
- `self.streaming_worker.progress_updated.connect`
- `self.streaming_worker.stop`
- `self.streaming_worker.streaming_error.connect`
- `self.streaming_worker.streaming_finished.connect`
- `self.tts_error.emit`
- `self.tts_finished.emit`
- `self.tts_model.list_voices`
- `self.tts_model.tts_to_file`
- `self.tts_service.tts_model.tts`
- `self.tts_started.emit`
- `self.voices_loaded.emit`
- `signal.resample`
- `speakers.keys`
- `split_sentences.append`
- `text.split`
- `text.strip`
- `thread.is_alive`
- `thread.join`
- `thread.start`
- `threading.Lock`
- `threading.Thread`
- `time.sleep`

**`services\Voice_STT_TTS_SERVICES\voice_process_manager.py`:**
- `CustomLogger.get_logger`
- `QApplication.instance`
- `QThread.currentThread`
- `app.processEvents`
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

**`services\Voice_STT_TTS_SERVICES\voice_service.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_audio_operation`
- `LoggingHelpers.log_exception_with_context`
- `LoggingHelpers.log_info_with_context`
- `LoggingHelpers.log_warning_with_context`
- `QTimer.singleShot`
- `audio_files.append`
- `audio_files.sort`
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
- `self._cleanup_timer.setSingleShot`
- `self._cleanup_timer.start`
- `self._cleanup_timer.timeout.connect`
- `self._connect_signals`
- `self._error_reset_timer.setSingleShot`
- `self._error_reset_timer.timeout.connect`
- `self._initialize_services`
- `self.cleanup_all_audio_files`
- `self.get_audio_folder_path`
- `self.list_audio_files`
- `self.recording_service.cleanup`
- `self.recording_service.get_current_audio_level`
- `self.recording_service.is_available`
- `self.recording_service.recording_auto_stopped.connect`
- `self.recording_service.recording_error.connect`
- `self.recording_service.recording_started.connect`
- `self.recording_service.recording_stopped.connect`
- `self.recording_service.set_audio_gate_enabled`
- `self.recording_service.set_speech_detection_parameters`
- `self.recording_service.start_recording`
- `self.recording_service.stop_recording`
- `self.recording_timer.setSingleShot`
- `self.recording_timer.start`
- `self.recording_timer.stop`
- `self.recording_timer.timeout.connect`
- `self.response_queue.put`
- `self.stop_tts`
- `self.stop_voice_input`
- `self.stt_service.convert_audio_to_text`
- `self.stt_service.error_occurred.connect`
- `self.stt_service.is_available`
- `self.stt_service.text_received.connect`
- `self.tts_error.emit`
- `self.tts_finished.emit`
- `self.tts_service.audio_level_changed.connect`
- `self.tts_service.is_available`
- `self.tts_service.set_coqui_model`
- `self.tts_service.speak_text_non_streaming`
- `self.tts_service.speak_text_streaming`
- `self.tts_service.stop_playback`
- `self.tts_service.tts_error.connect`
- `self.tts_service.tts_finished.connect`
- `self.tts_service.tts_started.connect`
- `self.tts_service.update_api`
- `self.tts_service.update_speed`
- `self.tts_service.update_voice`
- `self.voice_input_error.emit`
- `self.voice_input_received.emit`
- `self.voice_processing_finished.emit`
- `self.voice_processing_started.emit`
- `settings.copy`
- `settings.get`
- `text.strip`
- `time.time`

**`services\Voice_STT_TTS_SERVICES\voice_service_wrapper.py`:**
- `CustomLogger.get_logger`
- `logger.error`
- `logger.info`
- `self._cached_state.get`
- `self._cached_state.update`
- `self._init_direct_service`
- `self._init_process_manager`
- `self.direct_service.audio_level_changed.connect`
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
- `self.direct_service.recording_error.connect`
- `self.direct_service.recording_started.connect`
- `self.direct_service.recording_stopped.connect`
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
- `self.direct_service.tts_error.connect`
- `self.direct_service.tts_finished.connect`
- `self.direct_service.tts_started.connect`
- `self.direct_service.update_settings`
- `self.direct_service.voice_input_error.connect`
- `self.direct_service.voice_input_received.connect`
- `self.direct_service.voice_processing_finished.connect`
- `self.direct_service.voice_processing_started.connect`
- `self.process_manager.get_process_info`
- `self.process_manager.is_process_running`
- `self.process_manager.recording_error.connect`
- `self.process_manager.recording_started.connect`
- `self.process_manager.recording_stopped.connect`
- `self.process_manager.send_command`
- `self.process_manager.state_updated.connect`
- `self.process_manager.stop_voice_process`
- `self.process_manager.tts_error.connect`
- `self.process_manager.tts_finished.connect`
- `self.process_manager.tts_started.connect`
- `self.process_manager.voice_input_error.connect`
- `self.process_manager.voice_input_received.connect`
- `self.process_manager.voice_processing_finished.connect`
- `self.process_manager.voice_processing_started.connect`

**`services\conversation_service.py`:**
- `CustomLogger.get_logger`
- `content.lower`
- `data.get`
- `datetime.now`
- `filename.replace`
- `json.dump`
- `json.load`
- `logger.debug`
- `msg.get`
- `os.makedirs`
- `os.path.join`
- `self._add_to_memory`
- `self.conversation.append`
- `self.conversation.copy`
- `self.conversation_updated.emit`
- `self.memory_service.add_memory`
- `self.memory_service.get_context_messages`
- `self.memory_service.summarize_conversation`
- `self.metadata.get`
- `self.save_conversation`
- `tags.append`

**`services\enhancement_service.py`:**
- `response.split`
- `response.strip`
- `self.detect_follow_up_question`
- `sentence.strip`

**`services\memory_service.py`:**
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

**`services\ollama_service.py`:**
- `CustomLogger.get_logger`
- `LoggingHelpers.log_debug`
- `LoggingHelpers.log_exception_with_context`
- `LoggingHelpers.log_info_with_context`
- `LoggingHelpers.log_network_request`
- `LoggingHelpers.log_performance_metric`
- `LoggingHelpers.log_service_initialization`
- `LoggingHelpers.log_thread_operation`
- `base_url.rstrip`
- `chunk.get`
- `commands.append`
- `data.get`
- `json.dumps`
- `json.loads`
- `line.strip`
- `logger.debug`
- `logger.info`
- `m.get`
- `model_name.strip`
- `msg.get`
- `process.stdout.close`
- `process.terminate`
- `process.wait`
- `requests.get`
- `requests.post`
- `response.iter_lines`
- `response.json`
- `response.raise_for_status`
- `self._build_session_commands`
- `self._extract_system_prompt`
- `self.model_list_updated.emit`
- `self.model_operation_error.emit`
- `self.model_operation_finished.emit`
- `self.model_operation_progress.emit`
- `self.model_operation_started.emit`
- `self.test_connection`
- `session_variables.items`
- `subprocess.Popen`
- `thread.start`
- `time.time`

**`services\semantic_search_service.py`:**
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

**`services\start_up\dependency_checker.py`:**
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

**`services\start_up\install_dependencies.py`:**
- `d.check`
- `e.stderr.strip`
- `enchant.Dict`
- `enchant.list_dicts`
- `installer.install_all`
- `line.strip`
- `pbar.update`
- `self.check_python_version`
- `self.check_virtual_environment`
- `self.failed_stages.append`
- `self.print_header`
- `self.print_summary`
- `self.run_stage`
- `self.setup_spellchecker`
- `self.successful_stages.append`
- `self.upgrade_pip`
- `self.verify_installation`
- `stage.get`
- `stage.lower`
- `subprocess.run`
- `sys.exit`
- `time.time`

**`services\summarization_service.py`:**
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

**`services\worker\worker.py`:**
- `CustomLogger.get_logger`
- `QThread.currentThread`
- `chunk.get`
- `current_thread.objectName`
- `json.loads`
- `logger.debug`
- `logger.error`
- `logger.warning`
- `requests.post`
- `response.iter_lines`
- `response.raise_for_status`
- `self._log_thread_info`
- `self.error_signal.emit`
- `self.finished_signal.emit`
- `self.stream_chunk_signal.emit`
- `self.update_message_signal.emit`
- `time.sleep`
- `time.time`
- `traceback.format_exc`

**`ui\Audio_visualisers\eq_orchestrator.py`:**
- `AUDIO_PRESETS.items`
- `BAR_DISTRIBUTION.items`
- `FREQ_BANDS.items`
- `QFileDialog.getOpenFileName`
- `QTimer.singleShot`
- `app.exec`
- `btn.clicked.connect`
- `btn.setMaximumWidth`
- `btn.setStyleSheet`
- `chunk.mean`
- `grad.setGeometry`
- `hbox.addWidget`
- `inout.append`
- `net.setGeometry`
- `normalized_circle_vals.extend`
- `normalized_vals.extend`
- `np.abs`
- `np.any`
- `np.fft.rfft`
- `np.mean`
- `np.sqrt`
- `np.zeros`
- `os.path.exists`
- `preset_layout.addWidget`
- `rect.height`
- `rect.width`
- `sd.InputStream`
- `sd.OutputStream`
- `sd.query_devices`
- `sd.sleep`
- `self._play_file_audio`
- `self._play_microphone_audio`
- `self._process_audio_chunk`
- `self._reset_visualizers`
- `self.audio_path_label.setText`
- `self.audio_path_label.setWordWrap`
- `self.bar_values_updated.connect`
- `self.bar_values_updated.emit`
- `self.bar_widget.hide`
- `self.bar_widget.set_idle`
- `self.bar_widget.show`
- `self.bar_widget.start_animation`
- `self.bar_widget.stop_animation`
- `self.circle_widget.hide`
- `self.circle_widget.set_eq_sections`
- `self.circle_widget.show`
- `self.circle_widget.start_animation`
- `self.circle_widget.stop_animation`
- `self.device_combo.addItem`
- `self.device_combo.clear`
- `self.device_combo.count`
- `self.device_combo.currentIndexChanged.connect`
- `self.device_combo.currentText`
- `self.device_combo.itemData`
- `self.device_combo.setCurrentIndex`
- `self.device_combo.setMinimumWidth`
- `self.load_audio_preset`
- `self.mode_combo.addItems`
- `self.mode_combo.currentIndex`
- `self.mode_combo.currentIndexChanged.connect`
- `self.mute_btn.clicked.connect`
- `self.mute_btn.isChecked`
- `self.mute_btn.setCheckable`
- `self.mute_btn.setText`
- `self.play_audio`
- `self.play_btn.clicked.connect`
- `self.play_btn.setText`
- `self.play_thread.start`
- `self.populate_device_list`
- `self.preset_buttons.items`
- `self.refresh_devices_btn.clicked.connect`
- `self.resize`
- `self.select_btn.clicked.connect`
- `self.setCentralWidget`
- `self.setWindowTitle`
- `self.stop_audio`
- `self.system_audio_checkbox.stateChanged.connect`
- `self.visualizer_layout.addWidget`
- `self.visualizer_layout.setContentsMargins`
- `self.visualizer_stack.geometry`
- `self.waveform_bass.hide`
- `self.waveform_bass.set_idle`
- `self.waveform_bass.set_net_radii`
- `self.waveform_bass.show`
- `self.waveform_bass.start_animation`
- `self.waveform_bg.lower`
- `self.waveform_bg.setGeometry`
- `self.waveform_bg.setStyleSheet`
- `self.waveform_blue_bass.hide`
- `self.waveform_blue_bass.set_idle`
- `self.waveform_blue_bass.set_net_radii`
- `self.waveform_blue_bass.show`
- `self.waveform_blue_bass.start_animation`
- `self.waveform_blue_mid.hide`
- `self.waveform_blue_mid.set_idle`
- `self.waveform_blue_mid.set_net_radii`
- `self.waveform_blue_mid.show`
- `self.waveform_blue_mid.start_animation`
- `self.waveform_blue_treble.hide`
- `self.waveform_blue_treble.set_idle`
- `self.waveform_blue_treble.set_net_radii`
- `self.waveform_blue_treble.show`
- `self.waveform_blue_treble.start_animation`
- `self.waveform_bluegrad_bg.lower`
- `self.waveform_bluegrad_bg.setGeometry`
- `self.waveform_bluegrad_bg.setStyleSheet`
- `self.waveform_bluegrad_container.hide`
- `self.waveform_bluegrad_container.setAttribute`
- `self.waveform_bluegrad_container.setGeometry`
- `self.waveform_bluegrad_container.setLayout`
- `self.waveform_bluegrad_container.show`
- `self.waveform_grad_bass.hide`
- `self.waveform_grad_bass.set_idle`
- `self.waveform_grad_bass.set_net_radii`
- `self.waveform_grad_bass.show`
- `self.waveform_grad_bass.start_animation`
- `self.waveform_grad_bg.lower`
- `self.waveform_grad_bg.setGeometry`
- `self.waveform_grad_bg.setStyleSheet`
- `self.waveform_grad_container.hide`
- `self.waveform_grad_container.setAttribute`
- `self.waveform_grad_container.setGeometry`
- `self.waveform_grad_container.setLayout`
- `self.waveform_grad_container.show`
- `self.waveform_grad_mid.hide`
- `self.waveform_grad_mid.set_idle`
- `self.waveform_grad_mid.set_net_radii`
- `self.waveform_grad_mid.show`
- `self.waveform_grad_mid.start_animation`
- `self.waveform_grad_treble.hide`
- `self.waveform_grad_treble.set_idle`
- `self.waveform_grad_treble.set_net_radii`
- `self.waveform_grad_treble.show`
- `self.waveform_grad_treble.start_animation`
- `self.waveform_mid.hide`
- `self.waveform_mid.set_idle`
- `self.waveform_mid.set_net_radii`
- `self.waveform_mid.show`
- `self.waveform_mid.start_animation`
- `self.waveform_net_container.hide`
- `self.waveform_net_container.setAttribute`
- `self.waveform_net_container.setGeometry`
- `self.waveform_net_container.setLayout`
- `self.waveform_net_container.show`
- `self.waveform_treble.hide`
- `self.waveform_treble.set_idle`
- `self.waveform_treble.set_net_radii`
- `self.waveform_treble.show`
- `self.waveform_treble.start_animation`
- `sf.read`
- `stream.read`
- `sys.exit`
- `threading.Thread`
- `vals.append`
- `vbox.addLayout`
- `vbox.addWidget`
- `win.populate_device_list`
- `win.show`

**`ui\Audio_visualisers\eq_widgets\bar_eq_widget.py`:**
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

**`ui\Audio_visualisers\eq_widgets\circle_eq_widget.py`:**
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

**`ui\Audio_visualisers\eq_widgets\circular_gradient_eq_widget.py`:**
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

**`ui\Audio_visualisers\eq_widgets\circular_net_eq_widget.py`:**
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

**`ui\Audio_visualisers\voice_ring_animation.py`:**
- `AUDIO_PRESETS.items`
- `BAR_DISTRIBUTION.items`
- `FREQ_BANDS.items`
- `QFileDialog.getOpenFileName`
- `QTimer.singleShot`
- `app.exec`
- `btn.clicked.connect`
- `btn.setMaximumWidth`
- `btn.setStyleSheet`
- `c.setAlpha`
- `c2.setAlpha`
- `chunk.mean`
- `color.setAlpha`
- `dot_color.setAlpha`
- `fill_color.setAlpha`
- `glow_color.setAlpha`
- `grad.setColorAt`
- `grad.setGeometry`
- `gradient.setColorAt`
- `hbox.addWidget`
- `inout.append`
- `main_color.setAlpha`
- `math.cos`
- `math.sin`
- `net.setGeometry`
- `normalized_circle_vals.extend`
- `normalized_vals.extend`
- `np.abs`
- `np.any`
- `np.fft.rfft`
- `np.mean`
- `np.sqrt`
- `np.zeros`
- `os.path.exists`
- `painter.drawEllipse`
- `painter.drawLine`
- `painter.drawPath`
- `painter.drawPie`
- `painter.drawRect`
- `painter.fillRect`
- `painter.setBrush`
- `painter.setPen`
- `painter.setRenderHint`
- `path.closeSubpath`
- `path.moveTo`
- `path.quadTo`
- `points.append`
- `preset_layout.addWidget`
- `random.random`
- `random.uniform`
- `rect.height`
- `rect.width`
- `sd.InputStream`
- `sd.OutputStream`
- `sd.query_devices`
- `sd.sleep`
- `self._bar_values.copy`
- `self._calculate_bar_geometry`
- `self._create_bar_gradient`
- `self._create_section_gradient`
- `self._draw_bar`
- `self._section_values.copy`
- `self._setup_animation_timer`
- `self._smooth_radii`
- `self._target_values.copy`
- `self._timer.start`
- `self._timer.stop`
- `self._timer.timeout.connect`
- `self.audio_path_label.setText`
- `self.audio_path_label.setWordWrap`
- `self.bar_values_updated.connect`
- `self.bar_values_updated.emit`
- `self.bar_widget.hide`
- `self.bar_widget.set_idle`
- `self.bar_widget.show`
- `self.bar_widget.start_animation`
- `self.bar_widget.stop_animation`
- `self.circle_widget.hide`
- `self.circle_widget.set_eq_sections`
- `self.circle_widget.show`
- `self.circle_widget.start_animation`
- `self.circle_widget.stop_animation`
- `self.device_combo.addItem`
- `self.device_combo.clear`
- `self.device_combo.count`
- `self.device_combo.currentIndexChanged.connect`
- `self.device_combo.currentText`
- `self.device_combo.itemData`
- `self.device_combo.setCurrentIndex`
- `self.device_combo.setMinimumWidth`
- `self.height`
- `self.load_audio_preset`
- `self.mode_combo.addItems`
- `self.mode_combo.currentIndex`
- `self.mode_combo.currentIndexChanged.connect`
- `self.mute_btn.clicked.connect`
- `self.mute_btn.isChecked`
- `self.mute_btn.setCheckable`
- `self.mute_btn.setText`
- `self.play_audio`
- `self.play_btn.clicked.connect`
- `self.play_btn.setText`
- `self.play_thread.start`
- `self.populate_device_list`
- `self.preset_buttons.items`
- `self.refresh_devices_btn.clicked.connect`
- `self.resize`
- `self.select_btn.clicked.connect`
- `self.setCentralWidget`
- `self.setMinimumSize`
- `self.setWindowTitle`
- `self.start_animation`
- `self.stop_audio`
- `self.system_audio_checkbox.stateChanged.connect`
- `self.update`
- `self.visualizer_layout.addWidget`
- `self.visualizer_layout.setContentsMargins`
- `self.visualizer_stack.geometry`
- `self.waveform_bass.hide`
- `self.waveform_bass.set_idle`
- `self.waveform_bass.set_net_radii`
- `self.waveform_bass.show`
- `self.waveform_bass.start_animation`
- `self.waveform_bg.lower`
- `self.waveform_bg.setGeometry`
- `self.waveform_bg.setStyleSheet`
- `self.waveform_blue_bass.hide`
- `self.waveform_blue_bass.set_idle`
- `self.waveform_blue_bass.set_net_radii`
- `self.waveform_blue_bass.show`
- `self.waveform_blue_bass.start_animation`
- `self.waveform_blue_mid.hide`
- `self.waveform_blue_mid.set_idle`
- `self.waveform_blue_mid.set_net_radii`
- `self.waveform_blue_mid.show`
- `self.waveform_blue_mid.start_animation`
- `self.waveform_blue_treble.hide`
- `self.waveform_blue_treble.set_idle`
- `self.waveform_blue_treble.set_net_radii`
- `self.waveform_blue_treble.show`
- `self.waveform_blue_treble.start_animation`
- `self.waveform_bluegrad_bg.lower`
- `self.waveform_bluegrad_bg.setGeometry`
- `self.waveform_bluegrad_bg.setStyleSheet`
- `self.waveform_bluegrad_container.hide`
- `self.waveform_bluegrad_container.setAttribute`
- `self.waveform_bluegrad_container.setGeometry`
- `self.waveform_bluegrad_container.setLayout`
- `self.waveform_bluegrad_container.show`
- `self.waveform_grad_bass.hide`
- `self.waveform_grad_bass.set_idle`
- `self.waveform_grad_bass.set_net_radii`
- `self.waveform_grad_bass.show`
- `self.waveform_grad_bass.start_animation`
- `self.waveform_grad_bg.lower`
- `self.waveform_grad_bg.setGeometry`
- `self.waveform_grad_bg.setStyleSheet`
- `self.waveform_grad_container.hide`
- `self.waveform_grad_container.setAttribute`
- `self.waveform_grad_container.setGeometry`
- `self.waveform_grad_container.setLayout`
- `self.waveform_grad_container.show`
- `self.waveform_grad_mid.hide`
- `self.waveform_grad_mid.set_idle`
- `self.waveform_grad_mid.set_net_radii`
- `self.waveform_grad_mid.show`
- `self.waveform_grad_mid.start_animation`
- `self.waveform_grad_treble.hide`
- `self.waveform_grad_treble.set_idle`
- `self.waveform_grad_treble.set_net_radii`
- `self.waveform_grad_treble.show`
- `self.waveform_grad_treble.start_animation`
- `self.waveform_mid.hide`
- `self.waveform_mid.set_idle`
- `self.waveform_mid.set_net_radii`
- `self.waveform_mid.show`
- `self.waveform_mid.start_animation`
- `self.waveform_net_container.hide`
- `self.waveform_net_container.setAttribute`
- `self.waveform_net_container.setGeometry`
- `self.waveform_net_container.setLayout`
- `self.waveform_net_container.show`
- `self.waveform_treble.hide`
- `self.waveform_treble.set_idle`
- `self.waveform_treble.set_net_radii`
- `self.waveform_treble.show`
- `self.waveform_treble.start_animation`
- `self.width`
- `sf.read`
- `smoothed.append`
- `stream.read`
- `sys.exit`
- `threading.Thread`
- `validated.append`
- `validated.extend`
- `validated_values.append`
- `validated_values.extend`
- `vals.append`
- `vbox.addLayout`
- `vbox.addWidget`
- `win.populate_device_list`
- `win.show`

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

**`ui\Widgets\coqui_model_dialog.py`:**
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

**`ui\Widgets\editable_message_widget.py`:**
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

**`ui\Widgets\personality_widget.py`:**
- `QMessageBox.critical`
- `QMessageBox.information`
- `QMessageBox.question`
- `QMessageBox.warning`
- `basic_layout.addRow`
- `btn_layout.addWidget`
- `config_data.get`
- `config_layout.addRow`
- `create_btn.clicked.connect`
- `creation_widget.setStyleSheet`
- `current_item.text`
- `current_layout.addLayout`
- `current_layout.addWidget`
- `details_layout.addWidget`
- `examples_constraints_layout.addRow`
- `item.text`
- `layout.addStretch`
- `layout.addWidget`
- `list_layout.addLayout`
- `list_layout.addWidget`
- `metadata_data.get`
- `metadata_layout.addRow`
- `personality.split`
- `personality_data.get`
- `prompt_data.get`
- `prompt_layout.addRow`
- `refresh_button.clicked.connect`
- `refresh_button.setToolTip`
- `selector_layout.addWidget`
- `self.author_edit.clear`
- `self.author_edit.setPlaceholderText`
- `self.author_edit.text`
- `self.category_edit.clear`
- `self.category_edit.setPlaceholderText`
- `self.category_edit.text`
- `self.clear_creation_form`
- `self.code_checkbox.isChecked`
- `self.code_checkbox.setChecked`
- `self.constraints_edit.clear`
- `self.constraints_edit.setMaximumHeight`
- `self.constraints_edit.setPlaceholderText`
- `self.constraints_edit.toPlainText`
- `self.context_prompt_edit.clear`
- `self.context_prompt_edit.setMaximumHeight`
- `self.context_prompt_edit.setPlaceholderText`
- `self.context_prompt_edit.toPlainText`
- `self.conversation_style_combo.addItems`
- `self.conversation_style_combo.currentText`
- `self.conversation_style_combo.setCurrentIndex`
- `self.custom_list.addItems`
- `self.custom_list.clear`
- `self.custom_list.currentItem`
- `self.custom_list.itemClicked.connect`
- `self.delete_btn.clicked.connect`
- `self.description_edit.clear`
- `self.description_edit.setMaximumHeight`
- `self.description_edit.toPlainText`
- `self.details_text.setReadOnly`
- `self.details_text.setText`
- `self.emoji_checkbox.isChecked`
- `self.emoji_checkbox.setChecked`
- `self.examples_checkbox.isChecked`
- `self.examples_checkbox.setChecked`
- `self.examples_edit.clear`
- `self.examples_edit.setMaximumHeight`
- `self.examples_edit.setPlaceholderText`
- `self.examples_edit.toPlainText`
- `self.expertise_edit.clear`
- `self.expertise_edit.setMaximumHeight`
- `self.expertise_edit.setPlaceholderText`
- `self.expertise_edit.toPlainText`
- `self.export_btn.clicked.connect`
- `self.formality_combo.addItems`
- `self.formality_combo.currentText`
- `self.formality_combo.setCurrentIndex`
- `self.humor_combo.addItems`
- `self.humor_combo.currentText`
- `self.humor_combo.setCurrentIndex`
- `self.load_personalities`
- `self.max_tokens_spin.setRange`
- `self.max_tokens_spin.setSuffix`
- `self.max_tokens_spin.setValue`
- `self.max_tokens_spin.value`
- `self.name_edit.clear`
- `self.name_edit.text`
- `self.personality_changed.emit`
- `self.personality_combo.addItem`
- `self.personality_combo.clear`
- `self.personality_combo.count`
- `self.personality_combo.currentIndex`
- `self.personality_combo.currentText`
- `self.personality_combo.currentTextChanged.connect`
- `self.personality_combo.itemData`
- `self.personality_combo.setCurrentIndex`
- `self.personality_combo.setCurrentText`
- `self.personality_info.setMaximumHeight`
- `self.personality_info.setReadOnly`
- `self.personality_info.setText`
- `self.personality_model.build_comprehensive_system_prompt`
- `self.personality_model.create_custom_personality`
- `self.personality_model.delete_custom_personality`
- `self.personality_model.format_prompt_with_personality`
- `self.personality_model.get_available_personalities`
- `self.personality_model.get_current_personality`
- `self.personality_model.get_personality`
- `self.personality_model.get_personality_info`
- `self.personality_model.get_system_prompt`
- `self.personality_model.get_user_context_messages`
- `self.personality_model.refresh_personalities`
- `self.personality_model.set_current_personality`
- `self.questions_checkbox.isChecked`
- `self.questions_checkbox.setChecked`
- `self.response_length_combo.addItems`
- `self.response_length_combo.currentText`
- `self.response_length_combo.setCurrentIndex`
- `self.setStyleSheet`
- `self.setup_creation_tab`
- `self.setup_management_tab`
- `self.setup_selection_tab`
- `self.setup_ui`
- `self.style_edit.clear`
- `self.style_edit.text`
- `self.system_prompt_edit.clear`
- `self.system_prompt_edit.setMaximumHeight`
- `self.system_prompt_edit.setPlaceholderText`
- `self.system_prompt_edit.toPlainText`
- `self.tabs.addTab`
- `self.tags_edit.clear`
- `self.tags_edit.setPlaceholderText`
- `self.tags_edit.text`
- `self.temperature_spin.setRange`
- `self.temperature_spin.setSuffix`
- `self.temperature_spin.setToolTip`
- `self.temperature_spin.setValue`
- `self.temperature_spin.value`
- `self.tone_edit.clear`
- `self.tone_edit.text`
- `self.top_p_spin.setRange`
- `self.top_p_spin.setSuffix`
- `self.top_p_spin.setToolTip`
- `self.top_p_spin.setValue`
- `self.top_p_spin.value`
- `self.update_personality_info`
- `self.use_templates_checkbox.isChecked`
- `self.use_templates_checkbox.setChecked`
- `self.use_templates_checkbox.setToolTip`
- `self.user_prompt_edit.clear`
- `self.user_prompt_edit.setMaximumHeight`
- `self.user_prompt_edit.setPlaceholderText`
- `self.user_prompt_edit.toPlainText`
- `self.version_edit.setText`
- `self.version_edit.text`
- `traits_layout.addRow`
- `x.count`
- `x.strip`

**`ui\Widgets\settings_dialog.py`:**
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

**`ui\Widgets\voice_settings_dialog.py`:**
- `CustomLogger.get_logger`
- `QMessageBox.critical`
- `QMessageBox.information`
- `QMessageBox.question`
- `QMessageBox.warning`
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
- `eq_description.setStyleSheet`
- `eq_description.setWordWrap`
- `eq_layout.addLayout`
- `eq_layout.addWidget`
- `eq_selector_layout.addStretch`
- `eq_selector_layout.addWidget`
- `general_layout.addLayout`
- `general_layout.addWidget`
- `internet_layout.addWidget`
- `layout.addLayout`
- `layout.addStretch`
- `layout.addWidget`
- `logger.error`
- `logger.info`
- `math.log10`
- `math.sqrt`
- `model_layout.addWidget`
- `model_text.replace`
- `pyaudio.PyAudio`
- `self.accept`
- `self.auto_speak_checkbox.isChecked`
- `self.auto_speak_checkbox.setChecked`
- `self.cancel_button.clicked.connect`
- `self.cancel_button.setStyleSheet`
- `self.check_completed.emit`
- `self.check_internet_connection`
- `self.config_manager.get_voice_settings`
- `self.config_manager.set_voice_settings`
- `self.coqui_controls.setVisible`
- `self.coqui_service.get_available_models`
- `self.coqui_service.get_model_download_size`
- `self.coqui_service.is_model_downloaded`
- `self.coqui_service.is_multi_speaker`
- `self.coqui_service.load_model`
- `self.coqui_service.set_voice`
- `self.create_general_tab`
- `self.create_stt_tab`
- `self.create_tts_tab`
- `self.current_settings.copy`
- `self.current_settings.update`
- `self.download_button.clicked.connect`
- `self.download_button.setEnabled`
- `self.download_button.setText`
- `self.download_button.setVisible`
- `self.download_thread.download_completed.connect`
- `self.download_thread.start`
- `self.eq_selector.addItems`
- `self.eq_selector.currentText`
- `self.eq_selector.currentTextChanged.connect`
- `self.eq_selector.findText`
- `self.eq_selector.setCurrentIndex`
- `self.eq_selector.setStyleSheet`
- `self.internet_status_label.setStyleSheet`
- `self.internet_status_label.setText`
- `self.internet_thread.check_completed.connect`
- `self.internet_thread.start`
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
- `self.refresh_internet_button.clicked.connect`
- `self.refresh_internet_button.setMaximumWidth`
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
- `self.silence_duration_spinbox.value`
- `self.silence_threshold_spinbox.setDecimals`
- `self.silence_threshold_spinbox.setRange`
- `self.silence_threshold_spinbox.setSingleStep`
- `self.silence_threshold_spinbox.setStyleSheet`
- `self.silence_threshold_spinbox.setToolTip`
- `self.silence_threshold_spinbox.setValue`
- `self.silence_threshold_spinbox.value`
- `self.silence_threshold_spinbox.valueChanged.connect`
- `self.speaker_combo.addItem`
- `self.speaker_combo.clear`
- `self.speaker_combo.count`
- `self.speaker_combo.currentText`
- `self.speaker_combo.currentTextChanged.connect`
- `self.speaker_combo.itemText`
- `self.speaker_combo.setCurrentIndex`
- `self.standard_voice_layout.addWidget`
- `self.standard_voice_widget.setVisible`
- `self.start_coqui_download`
- `self.streaming_checkbox.isChecked`
- `self.streaming_checkbox.setChecked`
- `self.streaming_checkbox.setToolTip`
- `self.stt_api_combo.addItem`
- `self.stt_api_combo.count`
- `self.stt_api_combo.currentText`
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
- `self.timeout_spinbox.setStyleSheet`
- `self.timeout_spinbox.setToolTip`
- `self.timeout_spinbox.setValue`
- `self.timeout_spinbox.value`
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
- `self.voice_combo.currentText`
- `self.voice_combo.currentTextChanged.connect`
- `self.voice_combo.findText`
- `self.voice_combo.setCurrentIndex`
- `settings.copy`
- `settings.get`
- `silence_duration_layout.addStretch`
- `silence_duration_layout.addWidget`
- `silence_threshold_layout.addStretch`
- `silence_threshold_layout.addWidget`
- `speaker_layout.addWidget`
- `streaming_description.setStyleSheet`
- `streaming_description.setWordWrap`
- `streaming_layout.addWidget`
- `struct.unpack`
- `stt_layout.addWidget`
- `tab_widget.addTab`
- `test_stream.close`
- `test_stream.read`
- `threshold_description.setStyleSheet`
- `threshold_description.setWordWrap`
- `timeout_layout.addStretch`
- `timeout_layout.addWidget`
- `tts_layout.addWidget`
- `voice_layout.addWidget`

**`ui\styles\message_formatter.py`:**
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

**`ui\tabs\chat_tab\chat_display.py`:**
- `CustomLogger.get_logger`
- `QMessageBox.warning`
- `block.text`
- `block_text.strip`
- `button_layout.addWidget`
- `button_pos.setX`
- `button_pos.setY`
- `button_pos.x`
- `button_pos.y`
- `cancel_button.clicked.connect`
- `cancel_button.setStyleSheet`
- `cursor.block`
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
- `message.get`
- `message.startswith`
- `msg.get`
- `new_content.strip`
- `save_button.clicked.connect`
- `self.chat_display.clear`
- `self.chat_display.cursorForPosition`
- `self.chat_display.mapFromGlobal`
- `self.chat_display.setLineWrapMode`
- `self.chat_display.setMouseTracking`
- `self.chat_display.setReadOnly`
- `self.chat_display.setStyleSheet`
- `self.edit_button_widget.clicked.connect`
- `self.edit_button_widget.deleteLater`
- `self.edit_button_widget.hide`
- `self.edit_button_widget.move`
- `self.edit_button_widget.setFixedSize`
- `self.edit_button_widget.setStyleSheet`
- `self.edit_button_widget.show`
- `self.edit_message_at_index`
- `self.get_ai_name`
- `self.hide_edit_button`
- `self.mapToGlobal`
- `self.message_edited.emit`
- `self.save_message_edit`
- `self.scroll_area.setHorizontalScrollBarPolicy`
- `self.scroll_area.setVerticalScrollBarPolicy`
- `self.scroll_area.setWidget`
- `self.scroll_area.setWidgetResizable`
- `self.setup_streaming_handler`
- `self.setup_ui_components`
- `self.show_edit_button`
- `self.show_message_edit_dialog`
- `self.start_streaming`
- `self.streaming_handler.append_message`
- `self.streaming_handler.clear_chat`
- `self.streaming_handler.edit_message`
- `self.streaming_handler.finalize_streaming_message`
- `self.streaming_handler.get_messages`
- `self.streaming_handler.message_edited.connect`
- `self.streaming_handler.start_streaming_message`
- `self.streaming_handler.update_last_system_switch`
- `self.streaming_handler.update_streaming_message`
- `text_edit.setMaximumHeight`
- `text_edit.setPlainText`
- `text_edit.toPlainText`

**`ui\tabs\chat_tab\chat_tab.py`:**
- `ConversationMetadata.from_file`
- `CustomLogger.get_logger`
- `QApplication.processEvents`
- `QMessageBox.critical`
- `QTimer.singleShot`
- `audio_level_widget.hide`
- `chat_layout.addWidget`
- `chat_layout.setContentsMargins`
- `chat_splitter.addWidget`
- `chat_splitter.setSizes`
- `clicked.connect`
- `controls_layout.addWidget`
- `controls_layout.setContentsMargins`
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
- `self._append_response_chunk_safe`
- `self.append_to_chat`
- `self.chat_display.append_to_chat`
- `self.chat_display.chat_display.hide`
- `self.chat_display.clear_chat`
- `self.chat_display.get_streaming_handler`
- `self.chat_display.get_ui_components`
- `self.chat_display.message_edited.connect`
- `self.clear_chat`
- `self.eq_visualizer.eq_mode_changed.connect`
- `self.eq_visualizer.get_eq_mode`
- `self.eq_visualizer.is_eq_visualizer_active`
- `self.eq_visualizer.switch_to_chat_display`
- `self.eq_visualizer.switch_to_eq_visualizer`
- `self.eq_visualizer.update_eq_visualizer`
- `self.eq_visualizer.update_eq_visualizer_mode`
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
- `self.setStyleSheet`
- `self.set_current_conversation_file`
- `self.setup_components`
- `self.setup_connections`
- `self.setup_ui`
- `self.start_streaming`
- `self.stop_streaming`
- `self.voice_controls.audio_level_changed.connect`
- `self.voice_controls.get_ui_components`
- `self.voice_controls.get_voice_settings`
- `self.voice_controls.is_tts_playing`
- `self.voice_controls.recording_error.connect`
- `self.voice_controls.recording_started.connect`
- `self.voice_controls.recording_stopped.connect`
- `self.voice_controls.speak_ai_response`
- `self.voice_controls.tts_error.connect`
- `self.voice_controls.tts_finished.connect`
- `self.voice_controls.tts_started.connect`
- `self.voice_controls.update_voice_settings`
- `self.voice_controls.voice_input_error.connect`
- `self.voice_controls.voice_input_received.connect`
- `self.voice_controls.voice_processing_finished.connect`
- `self.voice_controls.voice_processing_started.connect`
- `self.voice_controls.voice_service.stop_voice_input`
- `settings.get`
- `streaming_handler.append_message`
- `streaming_handler.finalize_streaming_message`
- `streaming_handler.start_streaming_message`
- `streaming_handler.update_streaming_message`
- `voice_button.hide`
- `voice_controls_layout.addStretch`
- `voice_controls_layout.addWidget`
- `voice_controls_layout.setContentsMargins`
- `voice_settings.get`
- `voice_settings_button.hide`

**`ui\tabs\chat_tab\eq_visualizer.py`:**
- `CustomLogger.get_logger`
- `QApplication.processEvents`
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
- `QApplication.processEvents`
- `cursor.insertText`
- `event.key`
- `event.modifiers`
- `event.type`
- `logger.debug`
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
- `audio_level_layout.addWidget`
- `audio_level_layout.setContentsMargins`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.warning`
- `self._crash_recovery_timer.setSingleShot`
- `self._crash_recovery_timer.start`
- `self._crash_recovery_timer.timeout.connect`
- `self._disable_voice_features`
- `self._error_reset_timer.setSingleShot`
- `self._error_reset_timer.start`
- `self._error_reset_timer.timeout.connect`
- `self._handle_recording_error_safe`
- `self._handle_service_error`
- `self._handle_tts_error_safe`
- `self._handle_tts_finished_continuous`
- `self._handle_voice_input_error_safe`
- `self._handle_voice_input_safe`
- `self._reinitialize_voice_service`
- `self._reset_voice_button`
- `self._reset_voice_ui`
- `self._start_continuous_voice_mode`
- `self._stop_all_voice_operations`
- `self._update_audio_level_ui_safe`
- `self._update_voice_state`
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
- `self.audio_level_widget.setVisible`
- `self.config_manager.get_voice_settings`
- `self.recording_error.emit`
- `self.recording_started.emit`
- `self.recording_stopped.emit`
- `self.setup_connections`
- `self.setup_ui_components`
- `self.tts_error.emit`
- `self.tts_finished.emit`
- `self.tts_started.emit`
- `self.voice_button.clicked.connect`
- `self.voice_button.hide`
- `self.voice_button.setStyleSheet`
- `self.voice_button.setText`
- `self.voice_button.setToolTip`
- `self.voice_input_error.emit`
- `self.voice_input_received.emit`
- `self.voice_mode_changed.emit`
- `self.voice_processing_finished.emit`
- `self.voice_processing_started.emit`
- `self.voice_service.audio_level_changed.connect`
- `self.voice_service.get_silence_duration`
- `self.voice_service.get_silence_threshold`
- `self.voice_service.is_continuous_voice_mode`
- `self.voice_service.recording_error.connect`
- `self.voice_service.recording_service.audio_level_changed.connect`
- `self.voice_service.recording_service.audio_level_to_db`
- `self.voice_service.recording_started.connect`
- `self.voice_service.recording_stopped.connect`
- `self.voice_service.set_continuous_voice_mode`
- `self.voice_service.speak_text`
- `self.voice_service.start_voice_input`
- `self.voice_service.stop_tts`
- `self.voice_service.stop_voice_input`
- `self.voice_service.tts_error.connect`
- `self.voice_service.tts_finished.connect`
- `self.voice_service.tts_started.connect`
- `self.voice_service.update_settings`
- `self.voice_service.voice_input_error.connect`
- `self.voice_service.voice_input_received.connect`
- `self.voice_service.voice_processing_finished.connect`
- `self.voice_service.voice_processing_started.connect`
- `self.voice_settings.copy`
- `self.voice_settings.update`
- `self.voice_settings_button.hide`
- `self.voice_settings_button.setFixedSize`
- `self.voice_settings_button.setStyleSheet`
- `self.voice_settings_button.setToolTip`
- `time.time`
- `traceback.format_exc`

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
- `self.summarize_btn.clicked.disconnect`
- `self.summary_details_text.setReadOnly`
- `self.summary_details_text.setText`
- `self.tab_widget.addTab`
- `self.total_memories_label.setText`
- `self.total_summaries_label.setText`
- `semantic_stats.get`
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
- `export_button.clicked.connect`
- `export_button.setStyleSheet`
- `export_button.setToolTip`
- `item.text`
- `layout.addStretch`
- `layout.addWidget`
- `logger.debug`
- `metadata.get`
- `personality.split`
- `personality_data.get`
- `personality_label.setStyleSheet`
- `prompt_group.setStyleSheet`
- `prompt_layout.addWidget`
- `refresh_button.clicked.connect`
- `refresh_button.setStyleSheet`
- `refresh_button.setToolTip`
- `selector_layout.addWidget`
- `self.clear_creation_form`
- `self.custom_personalities_list.addItem`
- `self.custom_personalities_list.clear`
- `self.custom_personalities_list.currentItem`
- `self.custom_personalities_list.itemClicked.connect`
- `self.custom_personalities_list.setStyleSheet`
- `self.description_edit.clear`
- `self.description_edit.setMaximumHeight`
- `self.description_edit.setStyleSheet`
- `self.description_edit.toPlainText`
- `self.get_current_personality`
- `self.load_personalities`
- `self.name_edit.clear`
- `self.name_edit.setStyleSheet`
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
- `self.setStyleSheet`
- `self.setup_creation_tab`
- `self.setup_management_tab`
- `self.setup_selection_tab`
- `self.setup_ui`
- `self.style_edit.clear`
- `self.style_edit.setStyleSheet`
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
- `self.system_prompt_edit.setStyleSheet`
- `self.system_prompt_edit.toPlainText`
- `self.tabs.addTab`
- `self.tabs.setStyleSheet`
- `self.tone_edit.clear`
- `self.tone_edit.setStyleSheet`
- `self.tone_edit.text`
- `self.update_custom_personalities_list`
- `self.update_personality_info`
- `self.update_system_personalities_list`
- `self.update_system_personality_info`
- `system_group.setStyleSheet`
- `system_layout.addWidget`
- `traits.get`
- `x.count`

**`utils\Logging\Custom_Logger.py`:**
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
- `logging.Formatter`
- `logging.getLogger`
- `os.makedirs`
- `os.path.abspath`
- `os.path.dirname`
- `os.path.exists`
- `os.path.join`
- `re.compile`
- `re.sub`
- `self._filter_non_ascii`
- `self._print`

**`utils\Logging\logging_helpers.py`:**
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

**`utils\complexity_analyzer.py`:**
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

**`utils\complexity_widget.py`:**
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

**`utils\error_handler.py`:**
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

**`utils\internet_connection.py`:**
- `failed_tests.append`
- `self.test_http_connection`
- `self.test_socket_connection`
- `socket.create_connection`
- `tester.test_connection`
- `tester.test_connection_with_details`
- `urllib.request.Request`
- `urllib.request.urlopen`

**`utils\prompts.py`:**
- `PromptTemplates.CONVERSATION.get`
- `PromptTemplates.ERRORS.get`
- `PromptTemplates.MEMORY.get`
- `PromptTemplates.MENU.get`
- `PromptTemplates.STATUS.get`
- `template.format`

**`utils\streaming_handler.py`:**
- `CustomLogger.get_logger`
- `MessageFormatter.detect_and_format_code`
- `MessageFormatter.format_markdown`
- `MessageFormatter.split_thoughts_and_answer`
- `MessageFormatter.syntax_highlight_code`
- `QThread.currentThread`
- `QTimer.singleShot`
- `current_thread.objectName`
- `editable.append`
- `logger.debug`
- `logger.error`
- `main_thread.objectName`
- `msg.get`
- `self._get_next_message_id`
- `self._safe_ui_update`
- `self._stream_timer.setInterval`
- `self._stream_timer.timeout.connect`
- `self.chat_display.clear`
- `self.chat_display.ensureCursorVisible`
- `self.chat_display.insertHtml`
- `self.chat_display.thread`
- `self.chat_display.update`
- `self.message_edited.emit`
- `self.messages.append`
- `self.messages.clear`
- `self.messages.copy`
- `self.messages.index`
- `traceback.format_exc`


---

## 📈 Statistics

### Classes by Directory

- `MainApp/`: 5 classes
- `Personalities/`: 1 classes
- `Personalities\models/`: 6 classes
- `Personalities\services/`: 2 classes
- `Personalities\utils/`: 1 classes
- `config/`: 1 classes
- `controllers/`: 1 classes
- `models/`: 2 classes
- `services/`: 14 classes
- `services\Voice_STT_TTS_SERVICES/`: 10 classes
- `services\start_up/`: 2 classes
- `services\worker/`: 1 classes
- `ui\Audio_visualisers/`: 6 classes
- `ui\Audio_visualisers\eq_widgets/`: 4 classes
- `ui\Widgets/`: 9 classes
- `ui\styles/`: 2 classes
- `ui\tabs/`: 3 classes
- `ui\tabs\chat_tab/`: 5 classes
- `utils/`: 9 classes
- `utils\Logging/`: 7 classes

### Functions by Directory

- `MainApp/`: 92 functions
- `Personalities/`: 9 functions
- `Personalities\models/`: 8 functions
- `Personalities\services/`: 41 functions
- `Personalities\utils/`: 7 functions
- `config/`: 43 functions
- `controllers/`: 23 functions
- `models/`: 26 functions
- `services/`: 85 functions
- `services\Voice_STT_TTS_SERVICES/`: 181 functions
- `services\start_up/`: 24 functions
- `services\worker/`: 7 functions
- `ui\Audio_visualisers/`: 55 functions
- `ui\Audio_visualisers\eq_widgets/`: 37 functions
- `ui\Widgets/`: 111 functions
- `ui\styles/`: 14 functions
- `ui\tabs/`: 62 functions
- `ui\tabs\chat_tab/`: 141 functions
- `utils/`: 81 functions
- `utils\Logging/`: 60 functions

### Call Statistics

- **Total Function Calls:** 835
- **Total Method Calls:** 3227
- **Files with Function Calls:** 61
- **Files with Method Calls:** 59

# 📁 Project Directory Structure

**Generated:** July 13, 2025 at 08:30 PM
**Project:** PySide Ollama Chat
**Root Path:** `D:\Documents\Github_Repositories\Pyside_Ollama_Chat-LOCAL`

## 📋 Overview

This document shows the complete directory structure of the PySide Ollama Chat project.
Excluded directories and files are not shown to keep the structure clean and focused.

### 🔍 Excluded Items

The following items are excluded from this tree:

**Directories:**
- `chat_env/` - Virtual environment
- `documents/` - Documentation files
- `__pycache__/` - Python cache
- `.git/` - Git repository
- `.vscode/` - VS Code settings

**Files:**
- `*.pyc`, `*.pyo`, `*.pyd` - Python compiled files
- `*.log`, `*.tmp`, `*.cache` - Temporary files
- `.DS_Store`, `Thumbs.db` - System files

## 🌳 Directory Tree

```
└── ./
    ├── check_critical_issues.py (754B)
    ├── config.json (1KB)
    ├── detailed_analysis/
    │   ├── profiling_report_20250713_004307.json (7MB)
    │   ├── profiling_report_20250713_004307_summary.txt (2KB)
    │   ├── profiling_report_20250713_004705.json (7MB)
    │   └── profiling_report_20250713_004705_summary.txt (2KB)
    ├── Development_Tools/
    │   ├── Analyzers/
    │   │   ├── advanced_codebase_analyzer.py (23KB)
    │   │   ├── import_scanner.py (13KB)
    │   │   ├── logs Parser_error_detector.py (3KB)
    │   │   ├── program_flow_graph.py (4KB)
    │   │   ├── program_flow_tracer.py (22KB)
    │   │   └── refactoring_analyzer.py (49KB)
    │   ├── Legacy/
    │   │   └── LOGGER_ID_Creator.py (22KB)
    │   ├── Profiler/
    │   │   ├── profiler_helpers.py (22KB)
    │   │   ├── PROFILER_README.md (2KB)
    │   │   └── unified_profiler.py (4KB)
    │   ├── README.md (5KB)
    │   ├── Reports/
    │   │   ├── advanced_codebase_analysis.md (660KB)
    │   │   ├── log_report.md (3KB)
    │   │   ├── PROJECT_STRUCTURE.md (14KB)
    │   │   └── thread_safety_report.txt (20KB)
    │   ├── ThreadingAnalyser/
    │   │   └── thread_safety_analyzer.py (27KB)
    │   └── Utilities/
    │       ├── generate_directory_tree.py (11KB)
    │       ├── how_many_threads.py (93B)
    │       ├── run_analyzer.py (4KB)
    │       └── verify cuda.py (432B)
    ├── DOCUMENTATION/
    │   ├── agnostic_personality_examples.md (10KB)
    │   ├── AI_CHAT_NAMING.md (4KB)
    │   ├── App_Images/
    │   │   ├── Chat_Hello.png (54KB)
    │   │   ├── Main chat_blank.png (30KB)
    │   │   ├── Model_Management.png (42KB)
    │   │   ├── Personality_Creation.png (32KB)
    │   │   └── Personality_Selection.png (29KB)
    │   ├── env_commands.md (1KB)
    │   ├── FOLLOW_UP_SYSTEM.md (4KB)
    │   ├── Logging Commands.md (1KB)
    │   ├── PERSONALITY_SYSTEM_ENHANCEMENTS.md (6KB)
    │   ├── personality_template_best_practices.md (3KB)
    │   ├── pronoun_usage_guide.md (5KB)
    │   ├── SEMANTIC_SEARCH_README.md (8KB)
    │   ├── SPELLCHECKER_README.md (3KB)
    │   └── STREAMING_TTS_README.md (5KB)
    ├── LICENSE.txt (2KB)
    ├── Logs/
    ├── main.py (11KB)
    ├── models/
    │   ├── vosk-model-small-en-us-0.15/
    │   │   ├── am/
    │   │   │   └── final.mdl (15MB)
    │   │   ├── conf/
    │   │   │   ├── mfcc.conf (138B)
    │   │   │   └── model.conf (300B)
    │   │   ├── graph/
    │   │   │   ├── disambig_tid.int (119B)
    │   │   │   ├── Gr.fst (22MB)
    │   │   │   ├── HCLr.fst (21MB)
    │   │   │   └── phones/
    │   │   │       └── word_boundary.int (1KB)
    │   │   ├── ivector/
    │   │   │   ├── final.dubm (164KB)
    │   │   │   ├── final.ie (7MB)
    │   │   │   ├── final.mat (43KB)
    │   │   │   ├── global_cmvn.stats (1KB)
    │   │   │   ├── online_cmvn.conf (96B)
    │   │   │   └── splice.conf (37B)
    │   │   └── README (208B)
    │   └── vosk-model-small-en-us-0.15.zip (39MB)
    ├── PACKAGING_the_app/
    │   └── package_app.py (21KB)
    ├── pyside_chat/
    │   ├── __init__.py (0B)
    │   ├── app/
    │   │   ├── __init__.py (0B)
    │   │   ├── app_lifecycle.py (20KB)
    │   │   ├── event_bus.py (51KB)
    │   │   ├── main.py (6KB)
    │   │   ├── service_manager.py (8KB)
    │   │   └── threading_integration.py (9KB)
    │   ├── config/
    │   │   ├── __init__.py (24B)
    │   │   └── config_manager.py (10KB)
    │   ├── core/
    │   │   ├── __init__.py (0B)
    │   │   ├── logging/
    │   │   │   ├── __init__.py (0B)
    │   │   │   ├── helpers.py (18KB)
    │   │   │   └── logger.py (7KB)
    │   │   ├── models/
    │   │   │   ├── __init__.py (0B)
    │   │   │   ├── base_model.py (506B)
    │   │   │   └── conversation_metadata.py (20KB)
    │   │   ├── threading/
    │   │   │   ├── __init__.py (3KB)
    │   │   │   ├── persistent_thread_config.py (8KB)
    │   │   │   ├── persistent_thread_pool.py (16KB)
    │   │   │   ├── PERSISTENT_THREADS_README.md (8KB)
    │   │   │   ├── qrunnable_tasks.py (27KB)
    │   │   │   ├── qthread_workers.py (19KB)
    │   │   │   ├── README.md (9KB)
    │   │   │   ├── thread_calculator.py (16KB)
    │   │   │   ├── thread_calculator_examples.py (5KB)
    │   │   │   ├── thread_monitor.py (20KB)
    │   │   │   ├── thread_pool_manager.py (17KB)
    │   │   │   ├── threading_guide.md (7KB)
    │   │   │   ├── threading_service.py (24KB)
    │   │   │   └── usage_examples.py (19KB)
    │   │   └── utils/
    │   │       ├── __init__.py (0B)
    │   │       ├── error_handler.py (14KB)
    │   │       ├── internet_checker.py (5KB)
    │   │       ├── prompts.py (4KB)
    │   │       ├── streaming_handler.py (23KB)
    │   │       ├── threading_audit.py (12KB)
    │   │       └── threading_utils.py (15KB)
    │   ├── features/
    │   │   ├── __init__.py (94B)
    │   │   ├── chat/
    │   │   │   ├── __init__.py (0B)
    │   │   │   ├── chat_controller.py (23KB)
    │   │   │   ├── complexity_analyser/
    │   │   │   │   └── complexity_analyzer.py (18KB)
    │   │   │   ├── conversation_service.py (6KB)
    │   │   │   ├── enhancers/
    │   │   │   │   ├── __init__.py (0B)
    │   │   │   │   └── enhancement_service.py (1KB)
    │   │   │   └── summarization/
    │   │   │       ├── __init__.py (0B)
    │   │   │       └── summarization_service.py (18KB)
    │   │   ├── memory/
    │   │   │   ├── __init__.py (0B)
    │   │   │   ├── memory_service.py (42KB)
    │   │   │   ├── semantic_search.py (22KB)
    │   │   │   └── semantic_search_fallback.py (15KB)
    │   │   ├── ollama/
    │   │   │   ├── __init__.py (0B)
    │   │   │   ├── ollama_chat.py (5KB)
    │   │   │   └── ollama_service.py (36KB)
    │   │   ├── personality/
    │   │   │   ├── __init__.py (0B)
    │   │   │   ├── formatter.py (12KB)
    │   │   │   ├── loader.py (11KB)
    │   │   │   ├── models/
    │   │   │   │   ├── __init__.py (0B)
    │   │   │   │   ├── personality_model.py (3KB)
    │   │   │   │   ├── personality_pronouns.py (6KB)
    │   │   │   │   └── personality_types.py (2KB)
    │   │   │   ├── profiles/
    │   │   │   │   ├── __init__.py (0B)
    │   │   │   │   ├── Custom/
    │   │   │   │   ├── Family members/
    │   │   │   │   │   ├── father.json (2KB)
    │   │   │   │   │   ├── grandfather.json (2KB)
    │   │   │   │   │   ├── grandmother.json (2KB)
    │   │   │   │   │   └── mother.json (2KB)
    │   │   │   │   ├── Historic people/
    │   │   │   │   │   └── shakespeare.json (2KB)
    │   │   │   │   ├── Professions/
    │   │   │   │   │   ├── astronaut.json (2KB)
    │   │   │   │   │   ├── comedian.json (2KB)
    │   │   │   │   │   ├── guidance_counsellor.json (3KB)
    │   │   │   │   │   ├── priest.json (2KB)
    │   │   │   │   │   ├── professional.json (2KB)
    │   │   │   │   │   ├── programmer.json (2KB)
    │   │   │   │   │   └── therapist.json (2KB)
    │   │   │   │   └── Specialists/
    │   │   │   │       ├── assistant.json (1KB)
    │   │   │   │       ├── creative.json (1KB)
    │   │   │   │       └── technical.json (1KB)
    │   │   │   └── services/
    │   │   │       ├── __init__.py (0B)
    │   │   │       └── personality_service.py (20KB)
    │   │   ├── user/
    │   │   │   ├── __init__.py (0B)
    │   │   │   └── user_profile_service.py (629B)
    │   │   └── voice/
    │   │       ├── __init__.py (0B)
    │   │       ├── audio/
    │   │       │   ├── __init__.py (0B)
    │   │       │   └── recording_service.py (14KB)
    │   │       ├── orchestrator/
    │   │       │   ├── __init__.py (245B)
    │   │       │   └── voice_process_manager.py (20KB)
    │   │       ├── stt/
    │   │       │   ├── __init__.py (0B)
    │   │       │   └── stt_service.py (6KB)
    │   │       ├── tts/
    │   │       │   ├── __init__.py (0B)
    │   │       │   ├── coqui_tts_service.py (47KB)
    │   │       │   ├── streaming_audio_player.py (17KB)
    │   │       │   ├── streaming_audio_worker.py (6KB)
    │   │       │   └── tts_service.py (9KB)
    │   │       ├── voice_service.py (55KB)
    │   │       ├── voice_service_manager.py (11KB)
    │   │       └── voice_service_wrapper.py (18KB)
    │   ├── README.md (1KB)
    │   ├── startup/
    │   │   ├── __init__.py (186B)
    │   │   ├── dependency_checker.py (11KB)
    │   │   ├── install_dependencies.py (872B)
    │   │   ├── python_installer.py (1KB)
    │   │   ├── requirements.txt (5KB)
    │   │   └── system_installer.py (5KB)
    │   └── ui/
    │       ├── __init__.py (86B)
    │       ├── dialogs/
    │       │   ├── __init__.py (0B)
    │       │   ├── coqui_model_dialog.py (15KB)
    │       │   ├── settings_dialog.py (16KB)
    │       │   └── voice_settings_dialog.py (63KB)
    │       ├── tabs/
    │       │   ├── __init__.py (0B)
    │       │   ├── chat_tab/
    │       │   │   ├── __init__.py (0B)
    │       │   │   ├── chat_display.py (14KB)
    │       │   │   ├── chat_tab.py (66KB)
    │       │   │   ├── eq_visualizer.py (22KB)
    │       │   │   ├── input_controls.py (17KB)
    │       │   │   └── voice_controls.py (80KB)
    │       │   ├── memory_tab.py (26KB)
    │       │   ├── model_tab.py (17KB)
    │       │   ├── personality_tab.py (45KB)
    │       │   └── tab_styles.py (1KB)
    │       ├── themes/
    │       │   ├── __init__.py (82B)
    │       │   ├── message_formatter.py (18KB)
    │       │   └── styles.py (5KB)
    │       ├── ui_manager.py (10KB)
    │       ├── visualizers/
    │       │   ├── __init__.py (83B)
    │       │   ├── eq_orchestrator.py (29KB)
    │       │   └── widgets/
    │       │       ├── __init__.py (82B)
    │       │       ├── bar_eq_widget.py (10KB)
    │       │       ├── circle_eq_widget.py (8KB)
    │       │       ├── circular_gradient_eq_widget.py (5KB)
    │       │       └── circular_net_eq_widget.py (5KB)
    │       └── Widgets/
    │           ├── __init__.py (83B)
    │           ├── chat_navigation.py (18KB)
    │           ├── complexity_widget.py (9KB)
    │           ├── message_editor.py (7KB)
    │           └── spellchecker_widget.py (8KB)
    ├── README.md (15KB)
    ├── test_chat_fixes.py (3KB)
    ├── test_crash_fixes.py (6KB)
    ├── test_persistent_threads_integration.py (7KB)
    ├── Tests/
    ├── Tools/
    │   └── Profiler/
    │       └── unified_profiler.py (4KB)
    └── User_history/
        ├── audio/
        │   └── voice_input_20250713_180009.wav (190KB)
        ├── Chat_history/
        │   ├── conversation_20250713_200450.json (2KB)
        │   ├── conversation_20250713_201513.json (2KB)
        │   └── conversation_20250713_202043.json (2KB)
        └── memory/
            ├── embeddings/
            │   ├── embeddings.pkl (516KB)
            │   └── metadata.json (169KB)
            ├── long_term_memory.json (15KB)
            └── short_term_memory.json (8KB)
```

## 📊 Statistics

- **Total Files:** 207
- **Total Directories:** 66
- **Total Size:** 124MB
- **Python Files:** 135
- **Markdown Files:** 21
- **JSON Files:** 24

## 📝 File Types

- **.py:** 135 files
- **.json:** 24 files
- **.txt:** 5 files
- **.md:** 21 files
- **.png:** 5 files
- **.zip:** 1 files
- **:** 1 files
- **.mdl:** 1 files
- **.conf:** 4 files
- **.int:** 2 files
- **.fst:** 2 files
- **.dubm:** 1 files
- **.ie:** 1 files
- **.mat:** 1 files
- **.stats:** 1 files
- **.wav:** 1 files
- **.pkl:** 1 files

## 🔧 Usage

This structure was generated using the `generate_directory_tree.py` script.
To regenerate this file, run:

```bash
python generate_directory_tree.py
```

## 📋 Notes

- Directories are marked with `/`
- File sizes are shown in parentheses
- The tree is sorted alphabetically
- Hidden files and system files are excluded

---

*Generated automatically by Directory Tree Generator*
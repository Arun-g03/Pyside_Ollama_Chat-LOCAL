#!/usr/bin/env python3
"""
Program Flow Tracer Utility

This script analyzes the PySide Ollama Chat application and creates a comprehensive
markdown documentation of the program flow, starting from main.py and organizing
the execution into logical sections with loops and control flow.
"""

import os
import sys
import ast
import re
from typing import Dict, List, Set, Tuple, Optional
from pathlib import Path
import json

class ProgramFlowTracer:
    """Traces program flow and generates markdown documentation"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.flow_data = {
            'entry_points': [],
            'main_flow': [],
            'ui_flow': [],
            'service_flow': [],
            'event_flow': [],
            'worker_flow': [],
            'loops': [],
            'async_operations': [],
            'signal_connections': []
        }
        self.visited_files = set()
        self.loop_patterns = [
            'for', 'while', 'QTimer', 'QThread', 'worker', 'stream',
            'event_loop', 'exec()', 'run()', 'start()'
        ]
        
    def trace_program_flow(self) -> str:
        """Main method to trace the entire program flow"""
        print("🔍 Starting program flow analysis...")
        
        # Start with main.py
        self._analyze_main_entry()
        
        # Trace core application flow
        self._trace_main_application_flow()
        
        # Trace UI flow
        self._trace_ui_flow()
        
        # Trace service flow
        self._trace_service_flow()
        
        # Trace event handling flow
        self._trace_event_flow()
        
        # Trace worker/async flow
        self._trace_worker_flow()
        
        # Generate markdown
        return self._generate_markdown()
    
    def _analyze_main_entry(self):
        """Analyze the main entry point"""
        main_file = self.project_root / "main.py"
        if main_file.exists():
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.flow_data['entry_points'].append({
                'file': 'main.py',
                'function': 'main()',
                'description': 'Application entry point',
                'flow': [
                    'Parse command line arguments',
                    'Check dependencies',
                    'Create QApplication',
                    'Initialize OllamaChat window',
                    'Start event loop with app.exec()'
                ]
            })
    
    def _trace_main_application_flow(self):
        """Trace the main application initialization flow"""
        ollama_chat_file = self.project_root / "pyside_chat" / "MainApp" / "ollama_chat.py"
        
        if ollama_chat_file.exists():
            self.flow_data['main_flow'] = [
                {
                    'component': 'OllamaChat.__init__()',
                    'description': 'Main window initialization',
                    'flow': [
                        'Initialize ConfigManager',
                        'Initialize ServiceManager',
                        'Initialize ChatController',
                        'Initialize UIManager',
                        'Initialize EventHandler',
                        'Initialize AppLifecycleManager',
                        'Setup UI components',
                        'Setup signal connections',
                        'Initialize application'
                    ]
                },
                {
                    'component': 'ServiceManager._initialize_services()',
                    'description': 'Service initialization',
                    'flow': [
                        'Initialize OllamaService',
                        'Initialize ConversationService',
                        'Initialize EnhancementService',
                        'Initialize SummarizationService',
                        'Initialize MemoryService (if enabled)',
                        'Initialize ConversationManager',
                        'Setup session variables'
                    ]
                }
            ]
    
    def _trace_ui_flow(self):
        """Trace the UI initialization and management flow"""
        self.flow_data['ui_flow'] = [
            {
                'component': 'UIManager.setup_ui()',
                'description': 'UI setup and initialization',
                'flow': [
                    'Set window properties',
                    'Create central widget',
                    'Create tab widget',
                    'Initialize ChatTab',
                    'Initialize ModelTab',
                    'Initialize PersonalityTab',
                    'Initialize MemoryTab (if enabled)',
                    'Setup status bar',
                    'Apply styling'
                ]
            },
            {
                'component': 'ChatTab.setup_components()',
                'description': 'Chat interface component initialization',
                'flow': [
                    'Initialize VoiceControls',
                    'Initialize EQVisualizer',
                    'Initialize InputControls',
                    'Initialize ChatDisplay',
                    'Setup UI layout',
                    'Setup signal connections'
                ]
            },
            {
                'component': 'ChatTab.setup_connections()',
                'description': 'Signal connection setup',
                'flow': [
                    'Connect message_sent signal',
                    'Connect voice input signals',
                    'Connect TTS signals',
                    'Connect model change signals',
                    'Connect personality change signals',
                    'Connect conversation signals'
                ]
            }
        ]
    
    def _trace_service_flow(self):
        """Trace the service layer flow"""
        self.flow_data['service_flow'] = [
            {
                'component': 'OllamaService',
                'description': 'Ollama API communication',
                'flow': [
                    'Send chat messages',
                    'Stream responses',
                    'Manage model operations',
                    'Handle API errors',
                    'Emit progress signals'
                ]
            },
            {
                'component': 'ConversationService',
                'description': 'Conversation management',
                'flow': [
                    'Add messages to conversation',
                    'Retrieve conversation history',
                    'Save conversations to files',
                    'Load conversations from files',
                    'Manage conversation metadata'
                ]
            },
            {
                'component': 'MemoryService',
                'description': 'Memory and context management',
                'flow': [
                    'Intelligent message addition',
                    'Long-term memory storage',
                    'Fact extraction with LLM',
                    'Context building',
                    'Memory retrieval'
                ]
            },
            {
                'component': 'EnhancementService',
                'description': 'Message enhancement and processing',
                'flow': [
                    'Message preprocessing',
                    'Prompt formatting',
                    'Response post-processing',
                    'Content enhancement'
                ]
            }
        ]
    
    def _trace_event_flow(self):
        """Trace the event handling flow"""
        self.flow_data['event_flow'] = [
            {
                'component': 'EventHandler.setup_connections()',
                'description': 'Event handler initialization',
                'flow': [
                    'Connect controller signals',
                    'Connect Ollama service signals',
                    'Connect chat tab signals',
                    'Connect model tab signals',
                    'Connect personality tab signals',
                    'Connect conversation manager signals',
                    'Connect menu actions',
                    'Setup timer connections'
                ]
            },
            {
                'component': 'EventHandler._on_message_sent()',
                'description': 'Message processing flow',
                'flow': [
                    'Get current model and temperature',
                    'Process message through controller',
                    'Send to Ollama for processing',
                    'Create worker thread',
                    'Handle streaming response',
                    'Update UI with chunks',
                    'Handle completion'
                ]
            },
            {
                'component': 'ChatController.process_user_message()',
                'description': 'Message processing pipeline',
                'flow': [
                    'Log message sent',
                    'Update current settings',
                    'Check for new conversation',
                    'Add message to conversation',
                    'Handle memory operations',
                    'Send to Ollama',
                    'Log completion'
                ]
            }
        ]
    
    def _trace_worker_flow(self):
        """Trace the worker and async operations flow"""
        self.flow_data['worker_flow'] = [
            {
                'component': 'Worker.run_stream()',
                'description': 'Async message processing',
                'flow': [
                    'Set running state',
                    'Prepare HTTP request to Ollama',
                    'Stream response chunks',
                    'Parse JSON responses',
                    'Emit chunk signals',
                    'Handle completion',
                    'Clean up resources'
                ]
            },
            {
                'component': 'QThread Worker Management',
                'description': 'Thread management',
                'flow': [
                    'Create worker thread',
                    'Move worker to thread',
                    'Connect worker signals',
                    'Start worker execution',
                    'Handle worker completion',
                    'Clean up thread resources'
                ]
            },
            {
                'component': 'Streaming Response Handling',
                'description': 'Real-time response processing',
                'flow': [
                    'Receive chunk signals',
                    'Update UI with chunks',
                    'Accumulate response text',
                    'Handle TTS requests',
                    'Update progress indicators',
                    'Handle completion signals'
                ]
            }
        ]
    
    def _find_loops_and_async_operations(self):
        """Find loops and async operations in the codebase"""
        python_files = list(self.project_root.rglob("*.py"))
        
        for file_path in python_files:
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find loops
                    for pattern in self.loop_patterns:
                        if pattern in content:
                            self.flow_data['loops'].append({
                                'file': str(file_path.relative_to(self.project_root)),
                                'pattern': pattern,
                                'description': f'Found {pattern} pattern'
                            })
                    
                    # Find async operations
                    async_patterns = ['QTimer', 'QThread', 'worker', 'stream', 'signal']
                    for pattern in async_patterns:
                        if pattern in content:
                            self.flow_data['async_operations'].append({
                                'file': str(file_path.relative_to(self.project_root)),
                                'pattern': pattern,
                                'description': f'Found {pattern} async operation'
                            })
                            
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
    
    def _generate_markdown(self) -> str:
        """Generate comprehensive markdown documentation"""
        markdown = []
        
        # Header
        markdown.append("# PySide Ollama Chat - Program Flow Analysis")
        markdown.append("")
        markdown.append("This document traces the complete program flow of the PySide Ollama Chat application, starting from the main entry point and organizing the execution into logical sections.")
        markdown.append("")
        
        # Table of Contents
        markdown.append("## Table of Contents")
        markdown.append("")
        markdown.append("- [Entry Points](#entry-points)")
        markdown.append("- [Main Application Flow](#main-application-flow)")
        markdown.append("- [UI Flow](#ui-flow)")
        markdown.append("- [Service Flow](#service-flow)")
        markdown.append("- [Event Flow](#event-flow)")
        markdown.append("- [Worker/Async Flow](#workerasync-flow)")
        markdown.append("- [Loops and Control Flow](#loops-and-control-flow)")
        markdown.append("- [Signal Connections](#signal-connections)")
        markdown.append("")
        
        # Entry Points
        markdown.append("## Entry Points")
        markdown.append("")
        for entry in self.flow_data['entry_points']:
            markdown.append(f"### {entry['function']}")
            markdown.append(f"**File:** `{entry['file']}`")
            markdown.append(f"**Description:** {entry['description']}")
            markdown.append("")
            markdown.append("**Flow:**")
            for step in entry['flow']:
                markdown.append(f"- {step}")
            markdown.append("")
        
        # Main Application Flow
        markdown.append("## Main Application Flow")
        markdown.append("")
        markdown.append("### Application Initialization")
        markdown.append("")
        for component in self.flow_data['main_flow']:
            markdown.append(f"#### {component['component']}")
            markdown.append(f"**Description:** {component['description']}")
            markdown.append("")
            markdown.append("**Flow:**")
            for step in component['flow']:
                markdown.append(f"- {step}")
            markdown.append("")
        
        # UI Flow
        markdown.append("## UI Flow")
        markdown.append("")
        markdown.append("### UI Initialization and Management")
        markdown.append("")
        for component in self.flow_data['ui_flow']:
            markdown.append(f"#### {component['component']}")
            markdown.append(f"**Description:** {component['description']}")
            markdown.append("")
            markdown.append("**Flow:**")
            for step in component['flow']:
                markdown.append(f"- {step}")
            markdown.append("")
        
        # Service Flow
        markdown.append("## Service Flow")
        markdown.append("")
        markdown.append("### Service Layer Operations")
        markdown.append("")
        for component in self.flow_data['service_flow']:
            markdown.append(f"#### {component['component']}")
            markdown.append(f"**Description:** {component['description']}")
            markdown.append("")
            markdown.append("**Flow:**")
            for step in component['flow']:
                markdown.append(f"- {step}")
            markdown.append("")
        
        # Event Flow
        markdown.append("## Event Flow")
        markdown.append("")
        markdown.append("### Event Handling and Signal Processing")
        markdown.append("")
        for component in self.flow_data['event_flow']:
            markdown.append(f"#### {component['component']}")
            markdown.append(f"**Description:** {component['description']}")
            markdown.append("")
            markdown.append("**Flow:**")
            for step in component['flow']:
                markdown.append(f"- {step}")
            markdown.append("")
        
        # Worker/Async Flow
        markdown.append("## Worker/Async Flow")
        markdown.append("")
        markdown.append("### Asynchronous Operations and Threading")
        markdown.append("")
        for component in self.flow_data['worker_flow']:
            markdown.append(f"#### {component['component']}")
            markdown.append(f"**Description:** {component['description']}")
            markdown.append("")
            markdown.append("**Flow:**")
            for step in component['flow']:
                markdown.append(f"- {step}")
            markdown.append("")
        
        # Loops and Control Flow
        markdown.append("## Loops and Control Flow")
        markdown.append("")
        markdown.append("### Key Loops and Iterative Operations")
        markdown.append("")
        
        # Main Event Loop
        markdown.append("#### Main Event Loop")
        markdown.append("```python")
        markdown.append("# In main.py")
        markdown.append("result = app.exec()  # Qt event loop")
        markdown.append("```")
        markdown.append("")
        
        # Streaming Loop
        markdown.append("#### Streaming Response Loop")
        markdown.append("```python")
        markdown.append("# In Worker.run_stream()")
        markdown.append("for line in response.iter_lines(decode_unicode=True):")
        markdown.append("    if self._should_stop:")
        markdown.append("        break")
        markdown.append("    # Process chunk and emit signal")
        markdown.append("```")
        markdown.append("")
        
        # UI Update Loop
        markdown.append("#### UI Update Loop")
        markdown.append("```python")
        markdown.append("# In ChatTab.append_response_chunk()")
        markdown.append("for chunk in response_chunks:")
        markdown.append("    self.chat_display.append_chunk(chunk)")
        markdown.append("    QApplication.processEvents()  # Update UI")
        markdown.append("```")
        markdown.append("")
        
        # Timer Loops
        markdown.append("#### Timer-Based Operations")
        markdown.append("```python")
        markdown.append("# Various QTimer instances")
        markdown.append("self.model_update_timer = QTimer()")
        markdown.append("self.model_update_timer.timeout.connect(callback)")
        markdown.append("```")
        markdown.append("")
        
        # Signal Connections
        markdown.append("## Signal Connections")
        markdown.append("")
        markdown.append("### Key Signal-Slot Connections")
        markdown.append("")
        
        connections = [
            ("message_sent", "ChatTab → EventHandler → ChatController"),
            ("stream_chunk_signal", "Worker → ChatTab (UI update)"),
            ("finished_signal", "Worker → EventHandler (cleanup)"),
            ("model_list_updated", "OllamaService → UI components"),
            ("status_updated", "ChatController → UIManager"),
            ("conversation_updated", "ConversationService → UI refresh"),
            ("personality_changed", "PersonalityTab → ChatController"),
            ("voice_input_received", "VoiceControls → ChatTab"),
            ("tts_finished", "TTS Service → ChatTab")
        ]
        
        for signal, connection in connections:
            markdown.append(f"- **{signal}:** {connection}")
        
        markdown.append("")
        
        # Execution Summary
        markdown.append("## Execution Summary")
        markdown.append("")
        markdown.append("### Program Flow Overview")
        markdown.append("")
        markdown.append("1. **Application Startup**")
        markdown.append("   - Parse command line arguments")
        markdown.append("   - Check and install dependencies")
        markdown.append("   - Create QApplication instance")
        markdown.append("")
        markdown.append("2. **Main Window Initialization**")
        markdown.append("   - Initialize all service managers")
        markdown.append("   - Setup UI components")
        markdown.append("   - Establish signal connections")
        markdown.append("   - Show main window")
        markdown.append("")
        markdown.append("3. **Event Loop Execution**")
        markdown.append("   - Start Qt event loop with `app.exec()`")
        markdown.append("   - Handle user interactions")
        markdown.append("   - Process messages through worker threads")
        markdown.append("   - Update UI with streaming responses")
        markdown.append("")
        markdown.append("4. **Message Processing Pipeline**")
        markdown.append("   - User input → ChatController")
        markdown.append("   - Message enhancement → OllamaService")
        markdown.append("   - Streaming response → Worker thread")
        markdown.append("   - UI updates → ChatTab")
        markdown.append("   - TTS processing → Voice service")
        markdown.append("")
        markdown.append("5. **Application Shutdown**")
        markdown.append("   - Clean up worker threads")
        markdown.append("   - Save conversation state")
        markdown.append("   - Close all services")
        markdown.append("")
        
        return "\n".join(markdown)

def main():
    """Main function to run the program flow tracer"""
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Create tracer instance
    tracer = ProgramFlowTracer(project_root)
    
    # Generate flow analysis
    markdown_content = tracer.trace_program_flow()
    
    # Write to file
    output_file = os.path.join(project_root, "PROGRAM_FLOW_ANALYSIS.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Program flow analysis completed!")
    print(f"📄 Output written to: {output_file}")
    print(f"📊 Analysis includes:")
    print(f"   - Entry points and main flow")
    print(f"   - UI initialization and management")
    print(f"   - Service layer operations")
    print(f"   - Event handling and signal processing")
    print(f"   - Worker/async operations")
    print(f"   - Loops and control flow")
    print(f"   - Signal connections")

if __name__ == "__main__":
    main() 
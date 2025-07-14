#!/usr/bin/env python3
"""
Example: Using PySide6 Shared Imports

This script demonstrates how to use the new PySide6 shared imports file
to simplify Qt development and reduce import duplication.
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import PySide6 shared imports at module level
try:
    from pyside_chat.core.shared_imports.pyside_imports import *
    PYSIDE_IMPORTS_AVAILABLE = True
except ImportError:
    PYSIDE_IMPORTS_AVAILABLE = False

def demonstrate_pyside_imports():
    """Demonstrate the PySide6 shared imports functionality"""
    
    print("=== PySide6 Shared Imports Demo ===")
    
    # Example 1: Basic imports
    print("\n1. Basic PySide6 imports:")
    if PYSIDE_IMPORTS_AVAILABLE:
        print("✅ Successfully imported PySide6 shared imports")
        print("   Available components: QApplication, QMainWindow, QWidget, etc.")
    else:
        print("❌ Failed to import PySide6 shared imports")
        return
    
    # Example 2: Create a simple application
    print("\n2. Creating a simple Qt application:")
    try:
        # Create application
        app = QApplication(sys.argv)
        
        # Create main window
        window = QMainWindow()
        window.setWindowTitle("PySide6 Shared Imports Demo")
        window.setGeometry(100, 100, 400, 300)
        
        # Create central widget
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        
        # Create layout using helper functions
        layout = create_vertical_layout(central_widget)
        
        # Create widgets using helper functions
        title_label = create_label("PySide6 Shared Imports Demo", alignment=Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        
        info_label = create_label("This demonstrates the shared imports functionality")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create buttons
        button1 = create_button("Button 1")
        button2 = create_button("Button 2")
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addStretch()
        
        # Show window
        window.show()
        
        print("✅ Created Qt application with shared imports")
        print("   - Used helper functions for widget creation")
        print("   - Used helper functions for layout creation")
        
        # Don't actually run the app in demo mode
        # app.exec()
        
    except Exception as e:
        print(f"❌ Error creating Qt application: {e}")
    
    # Example 3: Demonstrate utility functions
    print("\n3. Utility functions:")
    
    # Thread safety check
    is_main = is_main_thread()
    print(f"   Main thread check: {is_main}")
    
    # Timer creation
    timer = create_timer(interval=1000, single_shot=True)
    print(f"   Created timer with interval: {timer.interval()}ms")
    
    # Message box creation
    msg_box = create_message_box("Demo", "This is a demo message box")
    print(f"   Created message box with title: {msg_box.windowTitle()}")
    
    # Example 4: Signal/slot safety
    print("\n4. Signal/slot safety:")
    
    class DemoObject(QObject):
        test_signal = Signal(str)
        
        def __init__(self):
            super().__init__()
            self.called = False
        
        def test_slot(self, message):
            self.called = True
            print(f"   Signal received: {message}")
    
    demo_obj = DemoObject()
    
    # Safe signal connection
    success = safe_signal_connect(demo_obj.test_signal, demo_obj.test_slot)
    print(f"   Signal connection: {'✅ Success' if success else '❌ Failed'}")
    
    # Emit signal
    demo_obj.test_signal.emit("Hello from shared imports!")
    
    # Safe signal disconnection
    success = safe_signal_disconnect(demo_obj.test_signal, demo_obj.test_slot)
    print(f"   Signal disconnection: {'✅ Success' if success else '❌ Failed'}")
    
    # Example 5: Before vs After comparison
    print("\n5. Before vs After comparison:")
    
    print("BEFORE (multiple individual imports):")
    print("""

""")
    
    print("AFTER (using shared imports):")
    print("""
from pyside_chat.core.shared_imports.pyside_imports import *
""")
    
    print("✅ Benefits:")
    print("   - Reduced from 20+ import lines to 1 line")
    print("   - All Qt modules available in one import")
    print("   - Includes utility functions for common tasks")
    print("   - Thread-safe signal/slot handling")
    print("   - Helper functions for widget creation")
    
    # Example 6: Advanced features
    print("\n6. Advanced features available:")
    
    print("   📦 Core Qt modules:")
    print("      - QtCore: QObject, QThread, QTimer, Signal, Qt")
    print("      - QtWidgets: QApplication, QMainWindow, QWidget, QVBoxLayout")
    print("      - QtGui: QPainter, QColor, QPen, QBrush, QFont")
    print("      - QtMultimedia: QMediaPlayer, QAudioOutput")
    print("      - QtNetwork: QNetworkAccessManager, QNetworkRequest")
    print("      - QtSql: QSqlDatabase, QSqlQuery")
    print("      - QtXml: QDomDocument, QXmlStreamReader")
    
    print("   🔧 Utility functions:")
    print("      - is_main_thread(): Check if in main thread")
    print("      - safe_ui_update(): Thread-safe UI updates")
    print("      - safe_signal_connect/disconnect(): Safe signal handling")
    print("      - create_timer(): Configured timer creation")
    print("      - create_message_box(): Configured message box")
    
    print("   🎨 Widget helpers:")
    print("      - create_button(): Configured button creation")
    print("      - create_label(): Configured label creation")
    print("      - create_text_edit(): Configured text edit")
    print("      - create_line_edit(): Configured line edit")
    print("      - create_combo_box(): Configured combo box")
    print("      - create_progress_bar(): Configured progress bar")
    
    print("   📐 Layout helpers:")
    print("      - create_vertical_layout(): Configured VBox layout")
    print("      - create_horizontal_layout(): Configured HBox layout")
    print("      - create_grid_layout(): Configured grid layout")
    print("      - create_form_layout(): Configured form layout")

def demonstrate_migration_example():
    """Show how to migrate existing code to use shared imports"""
    
    print("\n=== Migration Example ===")
    
    print("Original code:")
    print("""

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        label = QLabel("Hello World")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        button = QPushButton("Click Me")
        layout.addWidget(button)
""")
    
    print("\nMigrated code:")
    print("""
from pyside_chat.core.shared_imports.pyside_imports import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = create_vertical_layout(central_widget)
        
        label = create_label("Hello World", alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        button = create_button("Click Me")
        layout.addWidget(button)
""")
    
    print("\n✅ Migration benefits:")
    print("   - Reduced import lines from 3 to 1")
    print("   - Used helper functions for cleaner code")
    print("   - Consistent widget creation patterns")
    print("   - Better maintainability")

if __name__ == "__main__":
    demonstrate_pyside_imports()
    demonstrate_migration_example()
    
    print("\n=== Summary ===")
    print("The PySide6 shared imports file provides:")
    print("1. 📦 Comprehensive Qt module coverage")
    print("2. 🔧 Utility functions for common tasks")
    print("3. 🎨 Helper functions for widget creation")
    print("4. 🛡️ Thread-safe signal/slot handling")
    print("5. 📐 Layout creation helpers")
    print("6. 🚀 Reduced import duplication")
    print("7. 📋 Consistent coding patterns")
    print("8. 🔧 Easier maintenance and updates")
    
    print("\nTo use in your own files:")
    print("1. Replace individual PySide6 imports with the shared import")
    print("2. Use the helper functions for common tasks")
    print("3. Use the utility functions for thread safety")
    print("4. Follow the consistent patterns established") 
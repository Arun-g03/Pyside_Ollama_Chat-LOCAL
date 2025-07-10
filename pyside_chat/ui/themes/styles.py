"""
This module contains the styles for the UI.

"""

dark_stylesheet = """
QWidget {
    background-color: #232323;
    color: #f0f0f0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QMainWindow, QDialog {
    background-color: #232323;
}
QTabWidget::pane {
    border: 1px solid #444;
    border-radius: 8px;
    background: #232323;
}
QTabBar::tab {
    background: #232323;
    color: #f0f0f0;
    border: 1px solid #444;
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 8px 18px;
    font-size: 14px;
    min-width: 100px;
}
QTabBar::tab:selected {
    background: #2d2d2d;
    color: #fff;
    border-bottom: 2px solid #0078d4;
}
QGroupBox {
    border: 1px solid #444;
    border-radius: 8px;
    margin-top: 16px;
    font-weight: bold;
    color: #fff;
    padding-top: 10px;
}
QGroupBox:title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    background: #232323;
    color: #fff;
}
QLabel {
    color: #f0f0f0;
    font-size: 14px;
}
QComboBox, QSpinBox, QLineEdit, QTextEdit {
    background-color: #2d2d2d;
    color: #fff;
    border: 1px solid #555;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 14px;
}
QComboBox QAbstractItemView {
    background-color: #232323;
    color: #fff;
    border: 1px solid #555;
    selection-background-color: #0078d4;
}
QCheckBox {
    color: #fff;
    font-size: 14px;
    spacing: 8px;
}
QPushButton {
    background-color: #0078d4;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 8px 18px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #106ebe;
}
QPushButton:pressed {
    background-color: #005a9e;
}
QPushButton:disabled {
    background-color: #555;
    color: #888;
}
QSpinBox::up-button, QSpinBox::down-button {
    background: #232323;
    border: none;
}
QScrollBar:vertical, QScrollBar:horizontal {
    background: #232323;
    width: 12px;
    margin: 0px;
    border-radius: 6px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #444;
    border-radius: 6px;
    min-height: 20px;
    min-width: 20px;
}
QScrollBar::add-line, QScrollBar::sub-line {
    background: none;
    border: none;
}

QHeaderView::section {
    background-color: #232323;
    color: #fff;
    border: 1px solid #444;
    font-weight: bold;
    padding: 6px;
}

QListWidget, QWidget#Sidebar {
    background-color: #1e1e1e;
    color: #fff;
    border: 1px solid #444;
}

"""

light_stylesheet = """
QWidget {
    background-color: #f5f5f5;
    color: #222;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QMainWindow, QDialog {
    background-color: #f5f5f5;
}
QTabWidget::pane {
    border: 1px solid #bbb;
    border-radius: 8px;
    background: #f5f5f5;
}
QTabBar::tab {
    background: #eaeaea;
    color: #222;
    border: 1px solid #bbb;
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 8px 18px;
    font-size: 14px;
    min-width: 100px;
}
QTabBar::tab:selected {
    background: #fff;
    color: #0078d4;
    border-bottom: 2px solid #0078d4;
}
QGroupBox {
    border: 1px solid #bbb;
    border-radius: 8px;
    margin-top: 16px;
    font-weight: bold;
    color: #222;
    padding-top: 10px;
}
QGroupBox:title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    background: #f5f5f5;
    color: #222;
}
QLabel {
    color: #222;
    font-size: 14px;
}
QComboBox, QSpinBox, QLineEdit, QTextEdit {
    background-color: #fff;
    color: #222;
    border: 1px solid #bbb;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 14px;
}
QComboBox QAbstractItemView {
    background-color: #fff;
    color: #222;
    border: 1px solid #bbb;
    selection-background-color: #e3f1fb;
}
QCheckBox {
    color: #222;
    font-size: 14px;
    spacing: 8px;
}
QPushButton {
    background-color: #0078d4;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 8px 18px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #106ebe;
}
QPushButton:pressed {
    background-color: #005a9e;
}
QPushButton:disabled {
    background-color: #ccc;
    color: #888;
}
QSpinBox::up-button, QSpinBox::down-button {
    background: #f5f5f5;
    border: none;
}
QScrollBar:vertical, QScrollBar:horizontal {
    background: #f5f5f5;
    width: 12px;
    margin: 0px;
    border-radius: 6px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #bbb;
    border-radius: 6px;
    min-height: 20px;
    min-width: 20px;
}
QScrollBar::add-line, QScrollBar::sub-line {
    background: none;
    border: none;
}

QHeaderView::section {
    background-color: #232323;
    color: #fff;
    border: 1px solid #444;
    font-weight: bold;
    padding: 6px;
}

QListWidget, QWidget#Sidebar {
    background-color: #1e1e1e;
    color: #fff;
    border: 1px solid #444;
}

"""
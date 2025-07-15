from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
"""
Custom Error Dialog with Copy Button
"""

logger = CustomLogger.get_logger(__name__)


class ErrorDialog(QMessageBox):
    """Custom error dialog with copy button functionality"""

    def __init__(self, title="Error", message="", details="", parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle(title)
        self.setText(message)

        # Add copy button
        copy_button = QPushButton("Copy Error")
        copy_button.clicked.connect(self.copy_error)
        self.addButton(copy_button, QMessageBox.ButtonRole.ActionRole)

        # Store details for copying
        self.error_details = details if details else message

        # Style the dialog
        self.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton[text="Copy Error"] {
                background-color: #d83b01;
            }
            QPushButton[text="Copy Error"]:hover {
                background-color: #e85d04;
            }
        """)

    def copy_error(self):
        """Copy error details to clipboard"""
        try:
            clipboard = QClipboard()
            clipboard.setText(self.error_details)
            logger.debug("Error details copied to clipboard")

            # Temporarily change button text to show success
            copy_button = self.findChild(QPushButton, "")
            if copy_button and copy_button.text() == "Copy Error":
                copy_button.setText("Copied!")
                copy_button.setStyleSheet("""
                    QPushButton {
                        background-color: #107c10;
                        color: #ffffff;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 16px;
                        font-size: 12px;
                        font-weight: bold;
                        min-width: 80px;
                    }
                """)

                # Reset button text after 2 seconds

                QTimer.singleShot(
                    2000, lambda: self.reset_copy_button(copy_button))

        except Exception as e:
            logger.error(f"Failed to copy error to clipboard: {e}")

    def reset_copy_button(self, button):
        """Reset copy button to original state"""
        if button:
            button.setText("Copy Error")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #d83b01;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e85d04;
                }
            """)


class DetailedErrorDialog(QDialog):
    """Detailed error dialog with expandable details and copy functionality"""

    def __init__(self, title="Error", message="", details="", traceback="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumSize(500, 300)

        # Store error details
        self.error_details = f"Title: {title}\nMessage: {message}\nDetails: {details}\nTraceback: {traceback}"

        self.setup_ui(message, details, traceback)
        self.setup_styles()

    def setup_ui(self, message, details, traceback):
        """Setup the UI components"""
        layout = QVBoxLayout(self)

        # Error icon and message
        header_layout = QHBoxLayout()

        # Error icon (using text for simplicity)
        icon_label = QLabel("⚠️")
        icon_label.setFont(QFont("Segoe UI", 24))
        header_layout.addWidget(icon_label)

        # Error message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header_layout.addWidget(message_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Details section (collapsible)
        if details or traceback:
            details_label = QLabel("Details:")
            details_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            layout.addWidget(details_label)

            # Details text area
            self.details_text = QTextEdit()
            self.details_text.setReadOnly(True)
            self.details_text.setMaximumHeight(150)

            details_content = ""
            if details:
                details_content += f"Details:\n{details}\n\n"
            if traceback:
                details_content += f"Traceback:\n{traceback}"

            self.details_text.setPlainText(details_content)
            layout.addWidget(self.details_text)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Copy button
        copy_button = QPushButton("Copy Error")
        copy_button.clicked.connect(self.copy_error)
        button_layout.addWidget(copy_button)

        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)

    def setup_styles(self):
        """Setup the dialog styles"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton[text="Copy Error"] {
                background-color: #d83b01;
            }
            QPushButton[text="Copy Error"]:hover {
                background-color: #e85d04;
            }
        """)

    def copy_error(self):
        """Copy error details to clipboard"""
        try:
            clipboard = QClipboard()
            clipboard.setText(self.error_details)
            logger.debug("Detailed error copied to clipboard")

            # Find and update copy button
            for child in self.findChildren(QPushButton):
                if child.text() == "Copy Error":
                    child.setText("Copied!")
                    child.setStyleSheet("""
                        QPushButton {
                            background-color: #107c10;
                            color: #ffffff;
                            border: none;
                            border-radius: 4px;
                            padding: 8px 16px;
                            font-size: 12px;
                            font-weight: bold;
                            min-width: 80px;
                        }
                    """)

                    # Reset button text after 2 seconds

                    QTimer.singleShot(
                        2000, lambda: self.reset_copy_button(child))
                    break

        except Exception as e:
            logger.error(f"Failed to copy error to clipboard: {e}")

    def reset_copy_button(self, button):
        """Reset copy button to original state"""
        if button:
            button.setText("Copy Error")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #d83b01;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e85d04;
                }
            """)

    def accept(self):
        """Close the dialog"""
        super().accept()


def show_error_dialog(title="Error", message="", details="", traceback="", parent=None):
    """Show an error dialog with copy functionality"""
    if details or traceback:
        # Use detailed dialog for complex errors
        dialog = DetailedErrorDialog(
            title, message, details, traceback, parent)
        dialog.exec()
        return dialog
    else:
        # Use simple dialog for basic errors
        dialog = ErrorDialog(title, message, details, parent)
        dialog.exec()
        return dialog

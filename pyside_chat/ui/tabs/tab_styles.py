"""
Tab Styles Module

This module contains all tab-specific styling for the application.
Moving styles here makes theming and maintenance easier.
"""


class TabStyles:
    """Centralized tab styling for the application"""

    TAB_WIDGET_STYLE = """
        QTabWidget::pane {
            border: 1px solid #444;
            background-color: #1e1e1e;
        }
        QTabBar::tab {
            background: #2d2d2d;
            color: #ffffff;
            border: 1px solid #555;
            border-bottom: none;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            padding: 8px 24px;
            margin-right: 2px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }
        QTabBar::tab:selected {
            background: #0078d4;
            color: #ffffff;
        }
        QTabBar::tab:hover {
            background: #3d3d3d;
            color: #ffffff;
        }
    """

    @staticmethod
    def get_tab_style() -> str:
        """Get the tab widget style"""
        return TabStyles.TAB_WIDGET_STYLE

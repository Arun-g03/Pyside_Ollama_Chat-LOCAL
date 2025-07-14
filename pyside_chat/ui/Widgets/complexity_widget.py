
from pyside_chat.core.shared_imports.pyside_imports import *
class ComplexityWidget(QWidget):
    """Widget to display request complexity analysis"""
    
    model_recommendation_signal = Signal(str)  # Emits recommended model name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.analyzer = RequestComplexityAnalyzer()
        self.setup_ui()
        self.current_metrics = None
        
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Add a horizontal layout for the title and hide button
        title_layout = QHBoxLayout()
        title = QLabel("Request Complexity Analysis")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_layout.addWidget(title)
        # Add the hide button
        self.hide_btn = QPushButton("Hide")
        self.hide_btn.setMaximumWidth(50)
        self.hide_btn.clicked.connect(self.hide)
        title_layout.addWidget(self.hide_btn)
        layout.addLayout(title_layout)
        
        # Complexity level indicator
        self.level_label = QLabel("Level: Not Analyzed")
        self.level_label.setAlignment(Qt.AlignCenter)
        self.level_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.level_label)
        
        # Overall score progress bar
        score_layout = QHBoxLayout()
        score_layout.addWidget(QLabel("Complexity Score:"))
        self.score_bar = QProgressBar()
        self.score_bar.setRange(0, 100)
        self.score_bar.setValue(0)
        score_layout.addWidget(self.score_bar)
        layout.addLayout(score_layout)
        
        # Detailed metrics group
        metrics_group = QGroupBox("Detailed Metrics")
        metrics_layout = QVBoxLayout(metrics_group)
        
        # Create metric bars
        self.metric_bars = {}
        metrics = [
            ("reasoning_depth", "Reasoning Depth"),
            ("knowledge_breadth", "Knowledge Breadth"),
            ("ambiguity_score", "Ambiguity"),
            ("constraint_count", "Constraints"),
            ("context_dependency", "Context Dependency"),
            ("output_complexity", "Output Complexity")
        ]
        
        for metric_key, metric_name in metrics:
            metric_layout = QHBoxLayout()
            metric_layout.addWidget(QLabel(f"{metric_name}:"))
            
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(0)
            bar.setMaximumWidth(150)
            metric_layout.addWidget(bar)
            
            value_label = QLabel("0.00")
            value_label.setMinimumWidth(40)
            metric_layout.addWidget(value_label)
            
            metrics_layout.addLayout(metric_layout)
            self.metric_bars[metric_key] = (bar, value_label)
        
        layout.addWidget(metrics_group)
        
        # Model recommendation
        self.recommendation_group = QGroupBox("Model Recommendation")
        recommendation_layout = QVBoxLayout(self.recommendation_group)
        
        self.recommendation_label = QLabel("No recommendation available")
        self.recommendation_label.setWordWrap(True)
        recommendation_layout.addWidget(self.recommendation_label)
        
        self.switch_model_btn = QPushButton("Switch to Recommended Model")
        self.switch_model_btn.setEnabled(False)
        self.switch_model_btn.clicked.connect(self._on_switch_model)
        recommendation_layout.addWidget(self.switch_model_btn)
        
        layout.addWidget(self.recommendation_group)
        
        # Recommendations text
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setMaximumHeight(100)
        self.recommendations_text.setPlaceholderText("Recommendations will appear here...")
        self.recommendations_text.setReadOnly(True)
        layout.addWidget(self.recommendations_text)
        
        # Initially hide the widget
        self.hide()
        
    def analyze_request(self, request: str, conversation_history=None, available_models=None):
        """Analyze a request and update the display"""
        if not request.strip():
            self.hide()
            return
            
        # Perform analysis
        self.current_metrics = self.analyzer.analyze_complexity(request, conversation_history)
        
        # Update display
        self._update_display()
        
        # Update model recommendation
        if available_models:
            recommended_model = self.analyzer.get_model_recommendation(self.current_metrics, available_models)
            self._update_model_recommendation(recommended_model)
        
        # Show the widget
        self.show()
        
    def _update_display(self):
        """Update the display with current metrics"""
        if not self.current_metrics:
            return
            
        # Update level and color
        level_text = f"Level: {self.current_metrics.level.value.replace('_', ' ').title()}"
        self.level_label.setText(level_text)
        
        # Set color based on complexity level
        color_map = {
            ComplexityLevel.SIMPLE: QColor(76, 175, 80),      # Green
            ComplexityLevel.MEDIUM: QColor(255, 193, 7),      # Yellow
            ComplexityLevel.COMPLEX: QColor(255, 152, 0),     # Orange
            ComplexityLevel.VERY_COMPLEX: QColor(244, 67, 54) # Red
        }
        
        color = color_map.get(self.current_metrics.level, QColor(128, 128, 128))
        self._set_widget_color(self.level_label, color)
        
        # Update overall score
        score_percentage = int(self.current_metrics.score * 100)
        self.score_bar.setValue(score_percentage)
        self._set_progress_bar_color(self.score_bar, color)
        
        # Update detailed metrics
        for metric_key, (bar, label) in self.metric_bars.items():
            if hasattr(self.current_metrics, metric_key):
                value = getattr(self.current_metrics, metric_key)
                if metric_key == 'constraint_count':
                    # Constraints are counted, not percentages
                    bar.setValue(min(value * 10, 100))  # Scale for display
                    label.setText(str(value))
                else:
                    # Other metrics are already 0-1
                    bar.setValue(int(value * 100))
                    label.setText(f"{value:.2f}")
                
                # Set color based on value (green for low, red for high)
                if metric_key in ['reasoning_depth', 'knowledge_breadth', 'output_complexity']:
                    # Higher is more complex (red)
                    metric_color = self._get_color_for_value(value, reverse=False)
                else:
                    # Higher is more problematic (red)
                    metric_color = self._get_color_for_value(value, reverse=False)
                
                self._set_progress_bar_color(bar, metric_color)
        
        # Update recommendations
        recommendations_text = "\n".join(f"• {rec}" for rec in self.current_metrics.recommendations)
        self.recommendations_text.setPlainText(recommendations_text)
        
    def _update_model_recommendation(self, recommended_model: str):
        """Update the model recommendation display"""
        self.recommendation_label.setText(f"Recommended: {recommended_model}")
        self.switch_model_btn.setEnabled(True)
        self.recommended_model = recommended_model
        
    def _on_switch_model(self):
        """Handle model switch button click"""
        if hasattr(self, 'recommended_model'):
            self.model_recommendation_signal.emit(self.recommended_model)
            
    def _set_widget_color(self, widget, color):
        """Set widget text color"""
        palette = widget.palette()
        palette.setColor(QPalette.WindowText, color)
        widget.setPalette(palette)
        
    def _set_progress_bar_color(self, progress_bar, color):
        """Set progress bar color"""
        # Create stylesheet for the progress bar
        stylesheet = f"""
        QProgressBar {{
            border: 1px solid #ccc;
            border-radius: 3px;
            text-align: center;
        }}
        QProgressBar::chunk {{
            background-color: {color.name()};
            border-radius: 2px;
        }}
        """
        progress_bar.setStyleSheet(stylesheet)
        
    def _get_color_for_value(self, value: float, reverse: bool = False) -> QColor:
        """Get color based on value (0-1)"""
        if reverse:
            value = 1.0 - value
            
        if value < 0.25:
            return QColor(76, 175, 80)   # Green
        elif value < 0.5:
            return QColor(255, 193, 7)   # Yellow
        elif value < 0.75:
            return QColor(255, 152, 0)   # Orange
        else:
            return QColor(244, 67, 54)   # Red
            
    def clear_analysis(self):
        """Clear the current analysis"""
        self.current_metrics = None
        self.hide()
        self.recommendation_label.setText("No recommendation available")
        self.switch_model_btn.setEnabled(False)
        self.recommendations_text.clear()
        
    def get_current_metrics(self):
        """Get the current complexity metrics"""
        return self.current_metrics 
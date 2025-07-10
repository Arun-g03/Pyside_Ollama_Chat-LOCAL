import re
import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import requests

class ComplexityLevel(Enum):
    """Enumeration for complexity levels"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

@dataclass
class ComplexityMetrics:
    """Data class to hold complexity analysis results"""
    level: ComplexityLevel
    score: float  # 0.0 to 1.0
    token_count: int
    reasoning_depth: float
    knowledge_breadth: float
    ambiguity_score: float
    constraint_count: int
    context_dependency: float
    output_complexity: float
    factors: Dict[str, float]
    recommendations: List[str]

class RequestComplexityAnalyzer:
    """Analyzes the complexity of requests to help choose appropriate models"""
    
    def __init__(self):
        # Complexity indicators
        self.simple_patterns = [
            r'\b(?:hi|hello|hey|howdy)\b',
            r'\b(?:how are you|what\'s up|how\'s it going)\b',
            r'\b(?:thanks|thank you|thx)\b',
            r'\b(?:bye|goodbye|see you)\b',
            r'^\s*[a-zA-Z\s]{1,50}\s*$',  # Very short text
        ]
        
        self.complex_patterns = [
            # Technical/coding patterns
            r'\b(?:algorithm|optimization|performance|complexity|big o)\b',
            r'\b(?:architecture|design pattern|framework|library|api)\b',
            r'\b(?:debug|error|exception|bug|fix|issue)\b',
            r'\b(?:database|sql|query|schema|migration)\b',
            r'\b(?:testing|unit test|integration test|tdd|bdd)\b',
            r'\b(?:deployment|ci/cd|docker|kubernetes|aws|azure)\b',
            
            # Multi-step reasoning patterns
            r'\b(?:first|second|third|then|next|finally|therefore|thus|hence)\b',
            r'\b(?:if|else|while|for|when|unless|provided that|assuming)\b',
            r'\b(?:compare|analyze|evaluate|assess|examine|investigate)\b',
            r'\b(?:explain|describe|elaborate|detail|clarify|specify)\b',
            
            # Knowledge breadth indicators
            r'\b(?:multiple|various|different|several|many|numerous)\b',
            r'\b(?:integration|combination|synthesis|merge|combine)\b',
            r'\b(?:cross-platform|multi-language|polyglot|heterogeneous)\b',
            
            # Ambiguity indicators
            r'\b(?:maybe|perhaps|possibly|might|could|would|should)\b',
            r'\b(?:depends|context|situation|circumstance|case-by-case)\b',
            r'\b(?:unclear|vague|ambiguous|uncertain|unsure)\b',
        ]
        
        self.very_complex_patterns = [
            # Advanced technical concepts
            r'\b(?:machine learning|ai|neural network|deep learning)\b',
            r'\b(?:distributed system|microservices|scalability|load balancing)\b',
            r'\b(?:security|authentication|authorization|encryption|cryptography)\b',
            r'\b(?:blockchain|smart contract|web3|defi|nft)\b',
            r'\b(?:quantum computing|parallel processing|concurrency)\b',
            
            # Complex reasoning patterns
            r'\b(?:theorem|proof|mathematical|statistical|analytical)\b',
            r'\b(?:research|study|analysis|investigation|experiment)\b',
            r'\b(?:comprehensive|extensive|detailed|thorough|complete)\b',
            
            # Multi-domain knowledge
            r'\b(?:interdisciplinary|cross-domain|multi-field|hybrid)\b',
            r'\b(?:enterprise|large-scale|production|mission-critical)\b',
        ]
        
        # Constraint patterns
        self.constraint_patterns = [
            r'\b(?:only|just|exactly|precisely|specifically)\b',
            r'\b(?:must|should|need to|have to|required)\b',
            r'\b(?:format|structure|template|schema|pattern)\b',
            r'\b(?:limit|maximum|minimum|range|boundary)\b',
            r'\b(?:performance|efficiency|speed|memory|optimization)\b',
        ]
        
        # Output complexity patterns
        self.output_complexity_patterns = [
            r'\b(?:code|function|class|module|package)\b',
            r'\b(?:documentation|manual|guide|tutorial|example)\b',
            r'\b(?:report|analysis|summary|review|assessment)\b',
            r'\b(?:json|xml|yaml|csv|data structure)\b',
            r'\b(?:diagram|chart|graph|visualization|flowchart)\b',
        ]
        
        # Context dependency patterns
        self.context_patterns = [
            r'\b(?:previous|earlier|before|last time|as mentioned)\b',
            r'\b(?:continue|follow up|extend|build upon|expand)\b',
            r'\b(?:reference|refer to|see above|as shown|mentioned)\b',
            r'\b(?:context|background|history|previous conversation)\b',
        ]

    def analyze_complexity(self, request: str, conversation_history: List[Dict] = None) -> ComplexityMetrics:
        """
        Analyze the complexity of a request and return detailed metrics.
        
        Args:
            request: The user's request text
            conversation_history: Previous conversation messages for context analysis
            
        Returns:
            ComplexityMetrics object with detailed analysis
        """
        # Basic token estimation (rough approximation)
        token_count = self._estimate_tokens(request)
        
        # Analyze various complexity factors
        reasoning_depth = self._analyze_reasoning_depth(request)
        knowledge_breadth = self._analyze_knowledge_breadth(request)
        ambiguity_score = self._analyze_ambiguity(request)
        constraint_count = self._count_constraints(request)
        context_dependency = self._analyze_context_dependency(request, conversation_history)
        output_complexity = self._analyze_output_complexity(request)
        
        # Calculate overall complexity score
        factors = {
            'token_count': min(token_count / 1000, 1.0),  # Normalize to 0-1
            'reasoning_depth': reasoning_depth,
            'knowledge_breadth': knowledge_breadth,
            'ambiguity_score': ambiguity_score,
            'constraint_count': min(constraint_count / 10, 1.0),  # Normalize to 0-1
            'context_dependency': context_dependency,
            'output_complexity': output_complexity,
        }
        
        # Weighted average for overall score
        weights = {
            'token_count': 0.15,
            'reasoning_depth': 0.25,
            'knowledge_breadth': 0.20,
            'ambiguity_score': 0.10,
            'constraint_count': 0.10,
            'context_dependency': 0.10,
            'output_complexity': 0.10,
        }
        
        overall_score = sum(factors[key] * weights[key] for key in factors)
        
        # Determine complexity level
        level = self._determine_complexity_level(overall_score, factors)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(level, factors)
        
        return ComplexityMetrics(
            level=level,
            score=overall_score,
            token_count=token_count,
            reasoning_depth=reasoning_depth,
            knowledge_breadth=knowledge_breadth,
            ambiguity_score=ambiguity_score,
            constraint_count=constraint_count,
            context_dependency=context_dependency,
            output_complexity=output_complexity,
            factors=factors,
            recommendations=recommendations
        )

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (words + punctuation)"""
        # Simple approximation: ~1.3 tokens per word on average
        words = len(text.split())
        return int(words * 1.3)

    def _analyze_reasoning_depth(self, text: str) -> float:
        """Analyze the depth of reasoning required"""
        score = 0.0
        text_lower = text.lower()
        
        # Check for simple patterns (reduce score)
        for pattern in self.simple_patterns:
            if re.search(pattern, text_lower):
                score -= 0.1
                break
        
        # Check for complex reasoning patterns
        complex_matches = 0
        for pattern in self.complex_patterns:
            matches = len(re.findall(pattern, text_lower))
            complex_matches += matches
        
        # Check for very complex patterns
        very_complex_matches = 0
        for pattern in self.very_complex_patterns:
            matches = len(re.findall(pattern, text_lower))
            very_complex_matches += matches
        
        # Calculate reasoning depth score
        score += (complex_matches * 0.15) + (very_complex_matches * 0.25)
        
        # Check for multi-step instructions
        step_indicators = len(re.findall(r'\b(?:first|second|third|then|next|finally|step|phase)\b', text_lower))
        score += step_indicators * 0.1
        
        # Check for conditional logic
        conditional_indicators = len(re.findall(r'\b(?:if|else|when|unless|provided|assuming)\b', text_lower))
        score += conditional_indicators * 0.1
        
        return min(max(score, 0.0), 1.0)

    def _analyze_knowledge_breadth(self, text: str) -> float:
        """Analyze the breadth of knowledge domains required"""
        score = 0.0
        text_lower = text.lower()
        
        # Count technical domains mentioned
        domains = {
            'programming': len(re.findall(r'\b(?:code|programming|software|development|coding)\b', text_lower)),
            'database': len(re.findall(r'\b(?:database|sql|data|storage|query)\b', text_lower)),
            'web': len(re.findall(r'\b(?:web|http|api|rest|frontend|backend)\b', text_lower)),
            'system': len(re.findall(r'\b(?:system|architecture|infrastructure|deployment)\b', text_lower)),
            'security': len(re.findall(r'\b(?:security|authentication|encryption|privacy)\b', text_lower)),
            'ai_ml': len(re.findall(r'\b(?:ai|machine learning|neural|algorithm)\b', text_lower)),
        }
        
        # Calculate breadth score
        active_domains = sum(1 for count in domains.values() if count > 0)
        score = min(active_domains / 6.0, 1.0)
        
        # Bonus for interdisciplinary requests
        if active_domains > 2:
            score += 0.2
        
        return min(score, 1.0)

    def _analyze_ambiguity(self, text: str) -> float:
        """Analyze the ambiguity level of the request"""
        score = 0.0
        text_lower = text.lower()
        
        # Count ambiguous words
        ambiguous_words = len(re.findall(r'\b(?:maybe|perhaps|possibly|might|could|would|should|depends|unclear|vague)\b', text_lower))
        score += ambiguous_words * 0.1
        
        # Check for open-ended questions
        if re.search(r'\b(?:what|how|why|when|where|which)\b.*\?', text_lower):
            score += 0.2
        
        # Check for subjective language
        subjective_words = len(re.findall(r'\b(?:best|better|good|bad|better|worse|prefer|like|dislike)\b', text_lower))
        score += subjective_words * 0.05
        
        return min(score, 1.0)

    def _count_constraints(self, text: str) -> int:
        """Count the number of constraints in the request"""
        text_lower = text.lower()
        constraint_count = 0
        
        for pattern in self.constraint_patterns:
            constraint_count += len(re.findall(pattern, text_lower))
        
        # Count specific constraint types
        constraint_count += len(re.findall(r'\b(?:only|just|exactly|precisely)\b', text_lower))
        constraint_count += len(re.findall(r'\b(?:must|should|need to|have to|required)\b', text_lower))
        constraint_count += len(re.findall(r'\b(?:format|structure|template)\b', text_lower))
        
        return constraint_count

    def _analyze_context_dependency(self, text: str, conversation_history: List[Dict] = None) -> float:
        """Analyze how much the request depends on conversation context"""
        score = 0.0
        text_lower = text.lower()
        
        # Check for context-dependent language
        context_indicators = len(re.findall(r'\b(?:previous|earlier|before|last time|continue|follow up|extend)\b', text_lower))
        score += context_indicators * 0.2
        
        # Check for pronouns that need context
        pronoun_count = len(re.findall(r'\b(?:it|this|that|these|those|they|them)\b', text_lower))
        score += pronoun_count * 0.05
        
        # Check conversation history length
        if conversation_history:
            history_length = len(conversation_history)
            score += min(history_length / 20.0, 0.3)  # Cap at 0.3 for very long histories
        
        return min(score, 1.0)

    def _analyze_output_complexity(self, text: str) -> float:
        """Analyze the complexity of expected output"""
        score = 0.0
        text_lower = text.lower()
        
        # Check for complex output requirements
        for pattern in self.output_complexity_patterns:
            matches = len(re.findall(pattern, text_lower))
            score += matches * 0.1
        
        # Check for specific output formats
        format_indicators = len(re.findall(r'\b(?:json|xml|yaml|csv|html|markdown|code|function|class)\b', text_lower))
        score += format_indicators * 0.15
        
        # Check for length requirements
        if re.search(r'\b(?:long|detailed|comprehensive|extensive|thorough)\b', text_lower):
            score += 0.2
        
        return min(score, 1.0)

    def _determine_complexity_level(self, overall_score: float, factors: Dict[str, float]) -> ComplexityLevel:
        """Determine the complexity level based on overall score and factors"""
        if overall_score < 0.25:
            return ComplexityLevel.SIMPLE
        elif overall_score < 0.5:
            return ComplexityLevel.MEDIUM
        elif overall_score < 0.75:
            return ComplexityLevel.COMPLEX
        else:
            return ComplexityLevel.VERY_COMPLEX

    def _generate_recommendations(self, level: ComplexityLevel, factors: Dict[str, float]) -> List[str]:
        """Generate recommendations based on complexity analysis"""
        recommendations = []
        
        if level == ComplexityLevel.SIMPLE:
            recommendations.extend([
                "Use fast 7B model for quick responses",
                "Consider batch processing for multiple simple requests",
                "Cache common responses for efficiency"
            ])
        elif level == ComplexityLevel.MEDIUM:
            recommendations.extend([
                "7B model should handle this well",
                "Consider 32B model if accuracy is critical",
                "Monitor response quality for similar future requests"
            ])
        elif level == ComplexityLevel.COMPLEX:
            recommendations.extend([
                "Consider using 32B model for better reasoning",
                "Break down into smaller sub-requests if possible",
                "Provide additional context if needed"
            ])
        elif level == ComplexityLevel.VERY_COMPLEX:
            recommendations.extend([
                "Use 32B model for maximum capability",
                "Consider breaking into multiple focused requests",
                "Provide detailed context and examples",
                "Allow for longer processing time"
            ])
        
        # Add specific recommendations based on factors
        if factors['ambiguity_score'] > 0.5:
            recommendations.append("Request clarification to reduce ambiguity")
        
        if factors['constraint_count'] > 5:
            recommendations.append("Consider relaxing some constraints for better results")
        
        if factors['context_dependency'] > 0.5:
            recommendations.append("Ensure conversation context is maintained")
        
        return recommendations

    def get_model_recommendation(self, complexity_metrics: ComplexityMetrics, available_models: List[str]) -> str:
        """Get model recommendation based on complexity analysis"""
        # Extract model sizes from names (e.g., 1.5b, 3b, 7b, 32b, 70b)
        def extract_size(model_name):
            import re
            match = re.search(r'(\d+(?:\.\d+)?)[bB]', model_name)
            return float(match.group(1)) if match else float('inf')
        
        # Sort models by size ascending
        sorted_models = sorted(available_models, key=extract_size)
        
        if complexity_metrics.level == ComplexityLevel.SIMPLE:
            # Use the smallest model
            return sorted_models[0] if sorted_models else available_models[0] if available_models else "deepseek-r1:7b"
        elif complexity_metrics.level == ComplexityLevel.MEDIUM:
            # Use the next smallest (if available), else smallest
            return sorted_models[1] if len(sorted_models) > 1 else (sorted_models[0] if sorted_models else available_models[0] if available_models else "deepseek-r1:7b")
        else:
            # Use the largest model
            return sorted_models[-1] if sorted_models else available_models[0] if available_models else "deepseek-r1:7b"

    def format_complexity_report(self, metrics: ComplexityMetrics) -> str:
        """Format complexity analysis as a readable report"""
        report = f"""
🔍 **Request Complexity Analysis**

**Level:** {metrics.level.value.replace('_', ' ').title()}
**Score:** {metrics.score:.2f}/1.0

**Detailed Metrics:**
• Token Count: {metrics.token_count} (estimated)
• Reasoning Depth: {metrics.reasoning_depth:.2f}
• Knowledge Breadth: {metrics.knowledge_breadth:.2f}
• Ambiguity Score: {metrics.ambiguity_score:.2f}
• Constraints: {metrics.constraint_count}
• Context Dependency: {metrics.context_dependency:.2f}
• Output Complexity: {metrics.output_complexity:.2f}

**Recommendations:**
"""
        for rec in metrics.recommendations:
            report += f"• {rec}\n"
        
        return report.strip() 
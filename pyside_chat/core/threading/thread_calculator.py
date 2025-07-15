# Shared imports
from pyside_chat.core.shared_imports.shared_imports import *

"""
Thread Calculator Utility
Calculates optimal thread counts for different use cases based on system capabilities.
"""

import psutil
import platform
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Handle import for both direct execution and package import
try:
    from pyside_chat.core.logging.logger import CustomLogger
    logger = CustomLogger.get_logger(__name__)
except ImportError:
    # Fallback for direct execution
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


@dataclass
class ThreadRecommendations:
    """Thread count recommendations for different use cases"""
    cpu_count: int
    logical_cores: int
    physical_cores: int
    memory_gb: float
    system_type: str

    # Thread pool recommendations
    max_worker_threads: int
    default_worker_threads: int
    io_bound_threads: int
    cpu_bound_threads: int

    # UI thread recommendations
    ui_update_threads: int
    background_threads: int

    # Streaming recommendations
    streaming_threads: int
    chunk_processing_threads: int

    # Memory-based recommendations
    memory_safe_threads: int
    conservative_threads: int


class ThreadCalculator:
    """Calculates optimal thread counts based on system capabilities"""

    def __init__(self):
        self._cache: Optional[ThreadRecommendations] = None

    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        try:
            # CPU information
            try:
                cpu_count = os.cpu_count()
            except Exception as e:
                logger.error(f"Error getting os.cpu_count: {e}")
                cpu_count = 4
            try:
                logical_cores = psutil.cpu_count(logical=True)
            except Exception as e:
                logger.error(
                    f"Error getting psutil.cpu_count(logical=True): {e}")
                logical_cores = cpu_count
            try:
                physical_cores = psutil.cpu_count(logical=False)
            except Exception as e:
                logger.error(
                    f"Error getting psutil.cpu_count(logical=False): {e}")
                physical_cores = max(1, logical_cores // 2)

            # Memory information
            try:
                memory = psutil.virtual_memory()
                memory_gb = memory.total / (1024**3)
                memory_percent = memory.percent
                available_memory_gb = memory.available / (1024**3)
            except Exception as e:
                logger.error(f"Error getting psutil.virtual_memory: {e}")
                memory_gb = 8.0
                memory_percent = 50.0
                available_memory_gb = 4.0

            # System type
            try:
                system_type = platform.system()
            except Exception as e:
                logger.error(f"Error getting platform.system: {e}")
                system_type = "Unknown"

            return {
                'cpu_count': cpu_count,
                'logical_cores': logical_cores,
                'physical_cores': physical_cores,
                'memory_gb': memory_gb,
                'system_type': system_type,
                'memory_percent': memory_percent,
                'available_memory_gb': available_memory_gb
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            # Fallback values
            return {
                'cpu_count': 4,
                'logical_cores': 4,
                'physical_cores': 2,
                'memory_gb': 8.0,
                'system_type': 'Unknown',
                'memory_percent': 50.0,
                'available_memory_gb': 4.0
            }

    def calculate_thread_recommendations(self) -> ThreadRecommendations:
        """Calculate optimal thread counts for different use cases"""
        try:
            if self._cache:
                return self._cache

            system_info = self.get_system_info()

            # Base calculations
            cpu_count = system_info['cpu_count']
            logical_cores = system_info['logical_cores']
            physical_cores = system_info['physical_cores']
            memory_gb = system_info['memory_gb']
            system_type = system_info['system_type']

            # Calculate thread recommendations based on system capabilities
            recommendations = self._calculate_recommendations(
                cpu_count, logical_cores, physical_cores, memory_gb, system_type
            )

            self._cache = recommendations

            # Log the final statistics being used
            logger.info("=" * 60)
            logger.info("THREAD CALCULATOR FINAL STATISTICS")
            logger.info("=" * 60)
            logger.info(f"System Information:")
            logger.info(f"  Platform: {recommendations.system_type}")
            logger.info(f"  CPU Count: {recommendations.cpu_count}")
            logger.info(f"  Logical Cores: {recommendations.logical_cores}")
            logger.info(f"  Physical Cores: {recommendations.physical_cores}")
            logger.info(f"  Total Memory: {recommendations.memory_gb:.1f} GB")
            logger.info(
                f"  Available Memory: {system_info['available_memory_gb']:.1f} GB")
            logger.info(
                f"  Memory Usage: {system_info['memory_percent']:.1f}%")

            logger.info(f"Thread Recommendations:")
            logger.info(
                f"  Max Worker Threads: {recommendations.max_worker_threads}")
            logger.info(
                f"  Default Worker Threads: {recommendations.default_worker_threads}")
            logger.info(
                f"  IO-Bound Threads: {recommendations.io_bound_threads}")
            logger.info(
                f"  CPU-Bound Threads: {recommendations.cpu_bound_threads}")
            logger.info(
                f"  UI Update Threads: {recommendations.ui_update_threads}")
            logger.info(
                f"  Background Threads: {recommendations.background_threads}")
            logger.info(
                f"  Streaming Threads: {recommendations.streaming_threads}")
            logger.info(
                f"  Chunk Processing Threads: {recommendations.chunk_processing_threads}")
            logger.info(
                f"  Memory-Safe Threads: {recommendations.memory_safe_threads}")
            logger.info(
                f"  Conservative Threads: {recommendations.conservative_threads}")
            logger.info("=" * 60)

            return recommendations
        except Exception as e:
            logger.error(f"Error calculating thread recommendations: {e}")
            # Fallback to safe defaults
            return ThreadRecommendations(
                cpu_count=4,
                logical_cores=4,
                physical_cores=2,
                memory_gb=8.0,
                system_type='Unknown',
                max_worker_threads=8,
                default_worker_threads=2,
                io_bound_threads=4,
                cpu_bound_threads=2,
                ui_update_threads=2,
                background_threads=1,
                streaming_threads=2,
                chunk_processing_threads=2,
                memory_safe_threads=2,
                conservative_threads=2
            )

    def _calculate_recommendations(self, cpu_count: int, logical_cores: int,
                                   physical_cores: int, memory_gb: float,
                                   system_type: str) -> ThreadRecommendations:
        """Calculate specific thread recommendations"""
        try:
            # Base thread counts
            try:
                # Cap at 16 for stability
                max_worker_threads = min(logical_cores * 2, 16)
            except Exception as e:
                logger.error(f"Error calculating max_worker_threads: {e}")
                max_worker_threads = 8
            try:
                default_worker_threads = max(2, logical_cores // 2)
            except Exception as e:
                logger.error(f"Error calculating default_worker_threads: {e}")
                default_worker_threads = 2

            # IO-bound tasks (file operations, network requests)
            try:
                io_bound_threads = min(logical_cores * 3, 12)
            except Exception as e:
                logger.error(f"Error calculating io_bound_threads: {e}")
                io_bound_threads = 4

            # CPU-bound tasks (computations, processing)
            try:
                # Leave one core free
                cpu_bound_threads = max(2, logical_cores - 1)
            except Exception as e:
                logger.error(f"Error calculating cpu_bound_threads: {e}")
                cpu_bound_threads = 2

            # UI-related threads
            ui_update_threads = 2  # Keep UI responsive
            try:
                background_threads = max(1, logical_cores // 4)
            except Exception as e:
                logger.error(f"Error calculating background_threads: {e}")
                background_threads = 1

            # Streaming-specific threads
            streaming_threads = 3  # Dedicated streaming threads
            try:
                chunk_processing_threads = max(2, logical_cores // 2)
            except Exception as e:
                logger.error(
                    f"Error calculating chunk_processing_threads: {e}")
                chunk_processing_threads = 2

            # Memory-based adjustments
            try:
                memory_safe_threads = self._calculate_memory_safe_threads(
                    memory_gb, logical_cores)
            except Exception as e:
                logger.error(f"Error calculating memory_safe_threads: {e}")
                memory_safe_threads = 2
            try:
                conservative_threads = max(2, logical_cores // 3)
            except Exception as e:
                logger.error(f"Error calculating conservative_threads: {e}")
                conservative_threads = 2

            # System-specific adjustments
            try:
                if system_type == "Windows":
                    # Windows tends to handle threads differently
                    max_worker_threads = min(max_worker_threads, 12)
                    io_bound_threads = min(io_bound_threads, 8)
                elif system_type == "Darwin":  # macOS
                    # macOS has good thread management
                    pass
                elif system_type == "Linux":
                    # Linux can handle more threads efficiently
                    max_worker_threads = min(max_worker_threads, 20)
            except Exception as e:
                logger.error(
                    f"Error applying system-specific thread adjustments: {e}")

            return ThreadRecommendations(
                cpu_count=cpu_count,
                logical_cores=logical_cores,
                physical_cores=physical_cores,
                memory_gb=memory_gb,
                system_type=system_type,
                max_worker_threads=max_worker_threads,
                default_worker_threads=default_worker_threads,
                io_bound_threads=io_bound_threads,
                cpu_bound_threads=cpu_bound_threads,
                ui_update_threads=ui_update_threads,
                background_threads=background_threads,
                streaming_threads=streaming_threads,
                chunk_processing_threads=chunk_processing_threads,
                memory_safe_threads=memory_safe_threads,
                conservative_threads=conservative_threads
            )
        except Exception as e:
            logger.error(f"Error in _calculate_recommendations: {e}")
            return ThreadRecommendations(
                cpu_count=4,
                logical_cores=4,
                physical_cores=2,
                memory_gb=8.0,
                system_type='Unknown',
                max_worker_threads=8,
                default_worker_threads=2,
                io_bound_threads=4,
                cpu_bound_threads=2,
                ui_update_threads=2,
                background_threads=1,
                streaming_threads=2,
                chunk_processing_threads=2,
                memory_safe_threads=2,
                conservative_threads=2
            )

    def _calculate_memory_safe_threads(self, memory_gb: float, logical_cores: int) -> int:
        """Calculate thread count based on available memory"""
        try:
            # Estimate memory per thread (rough estimate)
            estimated_memory_per_thread_mb = 50  # Conservative estimate

            # Calculate how many threads we can safely run
            available_memory_mb = memory_gb * 1024
            memory_based_threads = int(
                available_memory_mb / estimated_memory_per_thread_mb)

            # Don't exceed logical cores
            memory_safe_threads = min(memory_based_threads, logical_cores)

            # Ensure minimum of 2 threads
            return max(2, memory_safe_threads)
        except Exception as e:
            logger.error(f"Error in _calculate_memory_safe_threads: {e}")
            return 2

    def get_recommendations_for_pool(self, pool_type: str) -> int:
        """Get thread count recommendation for specific pool type"""
        try:
            recommendations = self.calculate_thread_recommendations()

            pool_recommendations = {
                'worker': recommendations.default_worker_threads,
                'io_bound': recommendations.io_bound_threads,
                'cpu_bound': recommendations.cpu_bound_threads,
                'ui_update': recommendations.ui_update_threads,
                'background': recommendations.background_threads,
                'streaming': recommendations.streaming_threads,
                'chunk_processing': recommendations.chunk_processing_threads,
                'memory_safe': recommendations.memory_safe_threads,
                'conservative': recommendations.conservative_threads,
                'max': recommendations.max_worker_threads
            }

            recommended_count = pool_recommendations.get(
                pool_type, recommendations.default_worker_threads)
            logger.info(
                f"Thread Calculator: {pool_type} pool recommendation: {recommended_count} threads")
            return recommended_count
        except Exception as e:
            logger.error(f"Error in get_recommendations_for_pool: {e}")
            return 2

    def print_system_analysis(self):
        """Print detailed system analysis and recommendations"""
        try:
            recommendations = self.calculate_thread_recommendations()
            system_info = self.get_system_info()

            print("=" * 60)
            print("SYSTEM THREAD ANALYSIS")
            print("=" * 60)

            print(f"\nSystem Information:")
            print(f"  Platform: {recommendations.system_type}")
            print(f"  CPU Count: {recommendations.cpu_count}")
            print(f"  Logical Cores: {recommendations.logical_cores}")
            print(f"  Physical Cores: {recommendations.physical_cores}")
            print(f"  Total Memory: {recommendations.memory_gb:.1f} GB")
            print(
                f"  Available Memory: {system_info['available_memory_gb']:.1f} GB")
            print(f"  Memory Usage: {system_info['memory_percent']:.1f}%")

            print(f"\nThread Recommendations:")
            print(
                f"  Max Worker Threads: {recommendations.max_worker_threads}")
            print(
                f"  Default Worker Threads: {recommendations.default_worker_threads}")
            print(f"  IO-Bound Threads: {recommendations.io_bound_threads}")
            print(f"  CPU-Bound Threads: {recommendations.cpu_bound_threads}")
            print(f"  UI Update Threads: {recommendations.ui_update_threads}")
            print(
                f"  Background Threads: {recommendations.background_threads}")
            print(f"  Streaming Threads: {recommendations.streaming_threads}")
            print(
                f"  Chunk Processing Threads: {recommendations.chunk_processing_threads}")
            print(
                f"  Memory-Safe Threads: {recommendations.memory_safe_threads}")
            print(
                f"  Conservative Threads: {recommendations.conservative_threads}")

            print(f"\nUsage Examples:")
            print(
                f"  calculator.get_recommendations_for_pool('worker') -> {self.get_recommendations_for_pool('worker')}")
            print(
                f"  calculator.get_recommendations_for_pool('streaming') -> {self.get_recommendations_for_pool('streaming')}")
            print(
                f"  calculator.get_recommendations_for_pool('memory_safe') -> {self.get_recommendations_for_pool('memory_safe')}")

            print("=" * 60)
        except Exception as e:
            logger.error(f"Error in print_system_analysis: {e}")
            print("Could not print system analysis due to an error.")


# Global instance for easy access
try:
    thread_calculator = ThreadCalculator()
except Exception as e:
    logger.error(f"Error creating ThreadCalculator instance: {e}")
    thread_calculator = None


def get_thread_recommendations() -> ThreadRecommendations:
    """Get thread recommendations for the current system"""
    try:
        return thread_calculator.calculate_thread_recommendations()
    except Exception as e:
        logger.error(f"Error in get_thread_recommendations: {e}")
        return ThreadRecommendations(
            cpu_count=4,
            logical_cores=4,
            physical_cores=2,
            memory_gb=8.0,
            system_type='Unknown',
            max_worker_threads=8,
            default_worker_threads=2,
            io_bound_threads=4,
            cpu_bound_threads=2,
            ui_update_threads=2,
            background_threads=1,
            streaming_threads=2,
            chunk_processing_threads=2,
            memory_safe_threads=2,
            conservative_threads=2
        )


def get_pool_thread_count(pool_type: str) -> int:
    """Get recommended thread count for a specific pool type"""
    try:
        thread_count = thread_calculator.get_recommendations_for_pool(
            pool_type)
        logger.info(
            f"Thread Calculator: {pool_type} pool using {thread_count} threads")
        return thread_count
    except Exception as e:
        logger.error(f"Error in get_pool_thread_count: {e}")
        logger.info(
            f"Thread Calculator: {pool_type} pool using fallback 2 threads")
        return 2


def analyze_system():
    """Print system analysis (useful for debugging)"""
    try:
        thread_calculator.print_system_analysis()
    except Exception as e:
        logger.error(f"Error in analyze_system: {e}")
        print("Could not analyze system due to an error.")


if __name__ == "__main__":
    # Run system analysis when executed directly
    try:
        analyze_system()
    except Exception as e:
        logger.error(f"Error running analyze_system in __main__: {e}")
        print("Could not run system analysis due to an error.")

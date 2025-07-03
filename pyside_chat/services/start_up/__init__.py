"""
Startup Services Module

This module contains services that are used during application startup,
including dependency checking and installation.
"""

from .dependency_checker import DependencyChecker, check_and_install_dependencies

__all__ = ['DependencyChecker', 'check_and_install_dependencies'] 
"""
Shared imports for standard library and third-party modules

This file is auto-generated from import_analysis_report.json.
It includes all non-pyside_chat, non-PySide6 imports used in the codebase.

Usage:
    from pyside_chat.core.shared_imports.shared_imports import *
"""
import os

#Logging
from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.core.logging.helpers import LoggingHelpers

# Standard library imports


import traceback
import sys
import tempfile
import json
import time
import datetime
from datetime import datetime, timedelta
import threading
from threading import Lock
import subprocess
import platform
import re
import logging
import functools
import contextlib
import hashlib
import math
import random
import struct
import queue
import socket
import pickle
import shutil
import uuid
import io

# Third-party imports with error handling
try:
    import requests
except ImportError:
    requests = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import soundfile as sf
except ImportError:
    sf = None

try:
    import pyaudio
except ImportError:
    pyaudio = None

try:
    import librosa
except ImportError:
    librosa = None

try:
    import psutil
except ImportError:
    psutil = None

try:
    import enchant
except ImportError:
    enchant = None

try:
    import networkx as nx
except ImportError:
    nx = None

try:
    import sentence_transformers
except ImportError:
    sentence_transformers = None

try:
    import scipy
except ImportError:
    scipy = None

try:
    import vosk
except ImportError:
    vosk = None

try:
    import TTS
except ImportError:
    TTS = None

try:
    import pygame
except ImportError:
    pygame = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import pyenchant
except ImportError:
    pyenchant = None

try:
    import blis
except ImportError:
    blis = None

try:
    import ollama
except ImportError:
    ollama = None

try:
    import pygments
except ImportError:
    pygments = None

# Typing and dataclasses
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, Type, Generator
from dataclasses import dataclass, asdict, field
from enum import Enum

# Sklearn
try:
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    cosine_similarity = None

# HTML and parsing
from html import escape, unescape

# Pygments
try:
    from pygments import highlight
    from pygments.lexers import guess_lexer, get_lexer_by_name
    from pygments.formatters import HtmlFormatter
except ImportError:
    highlight = None
    guess_lexer = None
    get_lexer_by_name = None
    HtmlFormatter = None

# Add any other common imports as needed

# Threading service imports
try:
    from pyside_chat.core.threading.threading_service import  get_global_threading_service
    from pyside_chat.core.threading.persistent_thread_pool import get_global_persistent_thread_pool
    from pyside_chat.core.threading.qrunnable_tasks import DataProcessingTask
except ImportError:
    get_global_threading_service = None
    get_global_persistent_thread_pool = None
    DataProcessingTask = None

# Note: PySide6 and pyside_chat imports are intentionally excluded from this file. 
#!/usr/bin/env python3
"""
Pepper Robot Quiz Editor
Utility functions
"""

import sys
import importlib
from pathlib import Path

def import_quiz_generator_module():
    """
    Try to import the PepperQuizGenerator from the Quiz_generator package
    Returns the PepperQuizGenerator class or None if not found
    """
    try:
        # First try to import as a package
        from Quiz_generator.quiz_generator import PepperQuizGenerator
        return PepperQuizGenerator
    except ImportError:
        try:
            # Try to add the current directory to the path and import again
            current_dir = str(Path.cwd())
            if current_dir not in sys.path:
                sys.path.append(current_dir)
            
            # Try importing again
            from Quiz_generator.quiz_generator import PepperQuizGenerator
            return PepperQuizGenerator
        except ImportError:
            # Return None if module not found
            return None

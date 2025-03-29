#!/usr/bin/env python3
"""
Pepper Robot Quiz Generator
Base page generator class
"""

from pathlib import Path

class BasePageGenerator:
    """Base class for all page generators"""
    
    def __init__(self, output_dir):
        """
        Initialize the base page generator.
        
        Args:
            output_dir: Directory where generated HTML files will be placed
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _write_to_file(self, file_path, content):
        """Write content to a file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated {file_path}")
        
    def apply_template(self, template, data):
        """
        Apply template string with replacement variables
        
        Args:
            template: Template string with {variable} placeholders
            data: Dictionary of variables to replace in the template
            
        Returns:
            Formatted string with placeholders replaced
        """
        return template.format(**data)

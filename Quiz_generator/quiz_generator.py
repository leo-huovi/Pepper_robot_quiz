#!/usr/bin/env python3
"""
Pepper Robot Quiz Generator
Core generator class for creating quiz HTML pages
"""

import json
import shutil
from pathlib import Path

# Import all page generators
from .question_generator import QuestionPageGenerator
from .answer_generator import AnswerPageGenerator
from .info_generator import InfoPageGenerator
from .start_generator import StartPageGenerator

class PepperQuizGenerator:
    def __init__(self, config_file="quiz_config.json", output_dir="generated_quiz", image_dir="images"):
        """
        Initialize the Pepper Quiz Generator.
        
        Args:
            config_file: JSON file containing quiz configuration
            output_dir: Directory where generated HTML files will be placed
            image_dir: Directory containing button and quiz images
        """
        self.config_file = config_file
        self.output_dir = Path(output_dir)
        self.image_dir = Path(image_dir)
        self.config = None
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create html directory as parent for everything
        self.html_dir = self.output_dir / "html"
        self.html_dir.mkdir(parents=True, exist_ok=True)
        
        # Create en directory for English pages inside html
        self.en_dir = self.html_dir / "en"
        self.en_dir.mkdir(parents=True, exist_ok=True)
        
        # Create site directory inside html for CSS, JS, and images
        self.site_dir = self.html_dir / "site"
        self.site_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize page generators
        self.question_generator = QuestionPageGenerator(self.en_dir)
        self.answer_generator = AnswerPageGenerator(self.en_dir)
        self.info_generator = InfoPageGenerator(self.en_dir)
        self.start_generator = StartPageGenerator(self.en_dir)
        
    def load_config(self):
        """Load quiz configuration from JSON file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"Successfully loaded configuration from {self.config_file}")
            return True
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            return False
    
    def generate_quiz_pages(self):
        """Generate all quiz pages based on the configuration"""
        if not self.config:
            print("No configuration loaded. Please load configuration first.")
            return False
        
        # Copy common assets
        self._copy_common_assets()
        
        # Generate quiz pages
        for quiz_num, quiz_data in enumerate(self.config["quiz_pages"], 1):
            self._generate_quiz_pages_set(quiz_num, quiz_data)
            
        print(f"Successfully generated {len(self.config['quiz_pages'])} quiz page sets")
        
        # Generate the start page
        self._generate_start_page()
        
        return True
    
    def _copy_common_assets(self):
        """Copy common assets like sound files, CSS, and JS"""
        # Copy change_screen.ogg sound to html directory
        if Path(self.config.get("sound_file", "change_screen.ogg")).exists():
            shutil.copy(
                self.config.get("sound_file", "change_screen.ogg"), 
                self.html_dir / "change_screen.ogg"
            )
        
        # Copy image files if they exist and are configured
        if self.image_dir.exists():
            # Create images directory in html/site/img directory
            images_dir = self.site_dir / "img"
            images_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all images from image_dir to html/site/img
            for img_file in self.image_dir.glob("*.*"):
                if img_file.is_file() and img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                    shutil.copy(img_file, images_dir / img_file.name)
                    print(f"Copied image: {img_file.name} to html/site/img/")
        
        # Copy CSS and JS files if specified in config
        if "css_files" in self.config:
            css_dir = self.site_dir / "css"
            css_dir.mkdir(exist_ok=True)
            for css_file in self.config["css_files"]:
                if Path(css_file).exists():
                    shutil.copy(css_file, css_dir / Path(css_file).name)
                    print(f"Copied CSS file: {Path(css_file).name}")
        
        if "js_files" in self.config:
            js_dir = self.site_dir / "js"
            js_dir.mkdir(exist_ok=True)
            for js_file in self.config["js_files"]:
                if Path(js_file).exists():
                    shutil.copy(js_file, js_dir / Path(js_file).name)
                    print(f"Copied JS file: {Path(js_file).name}")
        
        # Copy web fonts if specified
        if "web_fonts" in self.config:
            fonts_dir = self.site_dir / "web-fonts-with-css"
            fonts_dir.mkdir(exist_ok=True)
            for font_dir in self.config["web_fonts"]:
                if Path(font_dir).exists() and Path(font_dir).is_dir():
                    font_name = Path(font_dir).name
                    target_dir = fonts_dir / font_name
                    target_dir.mkdir(exist_ok=True)
                    
                    # Copy all files and directories from the font directory
                    for file_path in Path(font_dir).glob("**/*"):
                        if file_path.is_file():
                            rel_path = file_path.relative_to(Path(font_dir))
                            target_file = target_dir / rel_path
                            target_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy(file_path, target_file)
                    
                    print(f"Copied web font: {font_name}")
    
    def _generate_quiz_pages_set(self, quiz_num, quiz_data):
        """Generate all three quiz pages for a single question"""
        total_questions = self.config.get("total_questions", 8)
        
        # Generate question page (main quiz question)
        self.question_generator.generate(quiz_num, quiz_data, total_questions)
        
        # Generate answer page (shown after user selects an answer)
        self.answer_generator.generate(quiz_num, quiz_data, total_questions)
        
        # Generate info page (shown when user clicks "More info")
        self.info_generator.generate(quiz_num, quiz_data, total_questions)
    
    def _generate_start_page(self):
        """Generate the quiz start page"""
        # Get start page config if available, otherwise use empty dict
        start_config = self.config.get("start_page", {})
        self.start_generator.generate(self.config.get("total_questions", 8), start_config)
        print("Generated start page")

    def validate_config(self):
        """Validate the configuration file for required fields"""
        if not self.config:
            print("No configuration loaded. Please load configuration first.")
            return False
        
        valid = True
        
        # Check if quiz_pages exists and is a list
        if "quiz_pages" not in self.config or not isinstance(self.config["quiz_pages"], list):
            print("Error: 'quiz_pages' must be a list in the configuration")
            valid = False
        else:
            # Check each quiz page for required fields
            for i, page in enumerate(self.config["quiz_pages"], 1):
                required_fields = ["question", "options", "correct_answer", "title", "info_text", "robot_speech"]
                for field in required_fields:
                    if field not in page:
                        print(f"Error: Missing required field '{field}' in quiz page {i}")
                        valid = False
                
                # Verify correct_answer is in options
                if "correct_answer" in page and "options" in page:
                    if page["correct_answer"] not in page["options"]:
                        print(f"Error: 'correct_answer' must be one of the 'options' in quiz page {i}")
                        valid = False
        
        # Check for total_questions
        if "total_questions" not in self.config:
            print("Warning: 'total_questions' not specified, using default value of 8")
        
        return valid

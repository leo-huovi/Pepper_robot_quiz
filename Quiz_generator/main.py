#!/usr/bin/env python3
"""
Pepper Robot Quiz Generator
Main script to orchestrate the generation of quiz pages
"""

import os
import json
import argparse
from pathlib import Path
from .quiz_generator import PepperQuizGenerator

def setup_argument_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description="Generate quiz pages for Pepper robot")
    parser.add_argument("--config", default="quiz_config.json", help="Path to quiz configuration JSON file")
    parser.add_argument("--output", default="generated_quiz", help="Output directory for generated files")
    parser.add_argument("--images", default="images", help="Directory containing quiz images")
    parser.add_argument("--create-sample", action="store_true", help="Create sample configuration and directory structure")
    return parser

def create_sample_config(config_file="quiz_config.json"):
    """Create a sample configuration file"""
    # Load the sample config from sample_config.json if it exists
    sample_config_path = Path(__file__).parent / "sample_config.json"
    
    if sample_config_path.exists():
        with open(sample_config_path, 'r', encoding='utf-8') as f:
            sample_config = json.load(f)
    else:
        # Use a default configuration if sample_config.json doesn't exist
        sample_config = {
            "quiz_pages": [
                {
                    "question": "Which beach?",
                    "options": [
                        "Pyynikki beach",
                        "Kaukajärvi beach",
                        "Rauhaniemi beach"
                    ],
                    "correct_answer": "Rauhaniemi beach",
                    "title": "Rauhaniemi beach",
                    "subtitle": "You can walk to Rauhaniemi beach in 30 minutes or take bus number 2 to get there.",
                    "info_text": "One of Tampere's many public saunas is located in Rauhaniemi. Saunas are very popular among humans.",
                    "robot_speech": "One of Tampere's many public saunas is located in Rauhaniemi. Saunas are very popular among humans. However, I dare not to go there, because I would melt!",
                    "body_class": "bg-secondary quiz"
                }
            ],
            "start_page": {
                "body_class": "bg-primary",
                "title": "Welcome to the Tampere Quiz!",
                "subtitle": "I've been visiting different attractions and places in Tampere and I took lots of pictures from my journey. Would you like to guess the places I visited?",
                "credits": "Pictures: Visit Tampere / Laura Vanzo, Olli-Pekka Latvala ja Kladez Zolota. Editing: Santeri Holappa."
            },
            "sound_file": "change_screen.ogg",
            "total_questions": 8
        }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, indent=4)
    
    print(f"Created sample configuration file: {config_file}")
    return True

def create_image_directories(image_dir="images"):
    """Create necessary directories for images"""
    os.makedirs(image_dir, exist_ok=True)
    print(f"Created '{image_dir}' directory for button and quiz images")
    return True

def setup_sample_environment(args):
    """Setup a sample environment with directories and files"""
    # Create sample configuration
    create_sample_config(args.config)
    
    # Create image directories
    create_image_directories(args.images)
    
    print("\nSample environment created!")
    print("To complete setup:")
    print(f"1. Add button images to the '{args.images}' directory")
    print(f"2. Edit '{args.config}' with your quiz content")
    print("3. Run this script without --create-sample to generate quiz pages")
    return True

def main():
    """Main function"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # If requested, create sample environment and exit
    if args.create_sample:
        setup_sample_environment(args)
        return
    
    # Initialize the generator
    generator = PepperQuizGenerator(
        config_file=args.config,
        output_dir=args.output,
        image_dir=args.images
    )
    
    # Load configuration and generate pages
    if generator.load_config():
        generator.generate_quiz_pages()
        print(f"\nQuiz pages generated successfully in '{args.output}' directory!")
    else:
        print(f"Failed to load configuration from '{args.config}'.")
        print("Run with --create-sample to create a sample configuration.")

if __name__ == "__main__":
    main()

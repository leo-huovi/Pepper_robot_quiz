# Pepper Robot Quiz Generator

A modular tool for generating interactive quiz pages for Pepper robot.

## Overview

This tool simplifies the creation of quiz pages for Pepper robot by allowing you to:

- Define quiz questions, answers, and information in a simple JSON configuration file
- Customize all text, images, and styles
- Generate a complete set of HTML files ready for deployment

## Structure

The generator is split into multiple Python files:

- `main.py`: Entry point script with command-line interface
- `quiz_generator.py`: Core class that orchestrates page generation
- `question_generator.py`: Generates quiz question pages
- `answer_generator.py`: Generates answer pages
- `info_generator.py`: Generates info pages
- `start_generator.py`: Generates start page
- `base_generator.py`: Base class for page generators
- `html_utils.py`: Utility functions for HTML generation

## Installation

1. Clone the repository or download the files
2. Ensure you have Python 3.6+ installed
3. Run the generator script

## Usage

### Creating a sample configuration

```bash
python main.py --create-sample
```

This creates:
- `quiz_config.json`: Sample configuration file
- `images/`: Directory for image files

### Generating quiz pages

```bash
python main.py --config quiz_config.json --output generated_quiz
```

### Command-line options

- `--config`: Path to configuration file (default: `quiz_config.json`)
- `--output`: Output directory (default: `generated_quiz`)
- `--images`: Path to images directory (default: `images`)
- `--create-sample`: Create sample configuration and directory structure

## Configuration

The configuration file is a JSON document with the following structure:

```json
{
    "quiz_pages": [
        {
            "question": "Question text",
            "options": ["Option 1", "Option 2", "Option 3"],
            "correct_answer": "Option 2",
            "title": "Page title",
            "subtitle": "Additional information shown after 'More info'",
            "info_text": "Text shown on the info page",
            "robot_speech": "What Pepper will say",
            "next_button_image": "../images/next_button.png",
            "more_button_image": "../images/info_button.png",
            "option_images": ["../images/option1.jpg", "../images/option2.jpg", "../images/option3.jpg"],
            "body_class": "bg-secondary quiz"
        }
    ],
    "start_page": {
        "body_class": "bg-primary",
        "title": "Welcome to the Quiz!",
        "subtitle": "Quiz introduction text",
        "credits": "Credit information",
        "yes_button_text": "Yes",
        "no_button_text": "No",
        "stylesheets": [
            "../site/css/bootstrap.min.css",
            "../site/css/style.css"
        ]
    },
    "sound_file": "change_screen.ogg",
    "total_questions": 8
}
```

### Customization

You can customize:
- All text content
- Image paths
- CSS classes for styling
- Stylesheets for each page
- Button text and images

## Examples

Check the `sample_config.json` file for a complete example of a quiz configuration.

## License

This project is open-source software.

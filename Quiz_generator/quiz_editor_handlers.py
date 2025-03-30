#!/usr/bin/env python3
"""
Pepper Robot Quiz Editor
Event handlers for the editor UI
"""

import os
import json
import shutil
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QColorDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from quiz_editor_utils import import_quiz_generator_module

# Try to import the quiz generator module
PepperQuizGenerator = import_quiz_generator_module()

# Question Management Methods
def add_question(self):
    """Add a new question to the quiz"""
    new_question = {
        "question": "New Question",
        "options": ["Option 1", "Option 2", "Option 3"],
        "correct_answer": "Option 1",
        "title": "Answer Title",
        "subtitle": "Answer Subtitle",
        "info_text": "Additional information about the answer.",
        "robot_speech": "What the robot will say about this answer.",
        "body_class": "bg-secondary quiz",
        "next_button_image": "../images/next_button.png",
        "more_button_image": "../images/info_button.png"
    }
    
    self.quiz_config["quiz_pages"].append(new_question)
    self.update_question_list()
    
    # Select the new question
    self.question_list.setCurrentRow(len(self.quiz_config["quiz_pages"]) - 1)

def remove_question(self):
    """Remove the selected question"""
    current_row = self.question_list.currentRow()
    if current_row >= 0:
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                     "Are you sure you want to delete this question?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.quiz_config["quiz_pages"][current_row]
            self.update_question_list()
            
            if self.quiz_config["quiz_pages"]:
                self.question_list.setCurrentRow(min(current_row, len(self.quiz_config["quiz_pages"]) - 1))
            else:
                self.clear_question_form()

def duplicate_question(self):
    """Duplicate the selected question"""
    current_row = self.question_list.currentRow()
    if current_row >= 0:
        new_question = dict(self.quiz_config["quiz_pages"][current_row])
        new_question["question"] = new_question["question"] + " (Copy)"
        
        self.quiz_config["quiz_pages"].append(new_question)
        self.update_question_list()
        
        # Select the new question
        self.question_list.setCurrentRow(len(self.quiz_config["quiz_pages"]) - 1)

def update_question_list(self):
    """Update the list of questions in the left panel"""
    self.question_list.clear()
    
    for i, page in enumerate(self.quiz_config["quiz_pages"]):
        item_text = f"{i+1}: {page['question']}"
        self.question_list.addItem(item_text)
    
    # Update total questions count
    self.quiz_config["total_questions"] = len(self.quiz_config["quiz_pages"])

def question_selected(self, row):
    """Load the selected question into the form"""
    if row >= 0 and row < len(self.quiz_config["quiz_pages"]):
        # Save any pending changes
        current_edited_row = self.question_id_label.text()
        if current_edited_row and current_edited_row.isdigit():
            current_edited_row = int(current_edited_row) - 1
            if current_edited_row >= 0 and current_edited_row < len(self.quiz_config["quiz_pages"]):
                reply = QMessageBox.question(self, "Unsaved Changes", 
                                        "You have unsaved changes. Save before switching?",
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if reply == QMessageBox.Cancel:
                    self.question_list.setCurrentRow(current_edited_row)
                    return
                elif reply == QMessageBox.Yes:
                    self.apply_question_changes()
        
        # Load the selected question
        question_data = self.quiz_config["quiz_pages"][row]
        
        # Fill the form
        self.question_id_label.setText(str(row + 1))
        self.question_text.setText(question_data.get("question", ""))
        self.question_title.setText(question_data.get("title", ""))
        self.question_subtitle.setText(question_data.get("subtitle", ""))
        
        # Options
        self.options_list.clear()
        for option in question_data.get("options", []):
            self.options_list.addItem(option)
        
        # Correct answer
        self.correct_answer_combo.clear()
        self.correct_answer_combo.addItems(question_data.get("options", []))
        correct_index = 0
        if "correct_answer" in question_data and question_data["correct_answer"] in question_data.get("options", []):
            correct_index = question_data.get("options", []).index(question_data["correct_answer"])
        self.correct_answer_combo.setCurrentIndex(correct_index)
        
        # Option images
        self.option_images_list.clear()
        for img in question_data.get("option_images", []):
            self.option_images_list.addItem(img)
        
        # Info text and robot speech
        self.info_text.setText(question_data.get("info_text", ""))
        self.robot_speech.setText(question_data.get("robot_speech", ""))
        
        # Background color
        self.bg_color_label.setText(question_data.get("body_class", "bg-secondary quiz"))
        
        # Button images
        self.next_btn_path.setText(question_data.get("next_button_image", "../images/next_button.png"))
        self.more_btn_path.setText(question_data.get("more_button_image", "../images/info_button.png"))

def apply_question_changes(self):
    """Apply changes to the current question"""
    row = self.question_id_label.text()
    if not row or not row.isdigit():
        return
    
    row = int(row) - 1
    if row < 0 or row >= len(self.quiz_config["quiz_pages"]):
        return
    
    # Get values from form
    question_data = self.quiz_config["quiz_pages"][row]
    
    question_data["question"] = self.question_text.text()
    question_data["title"] = self.question_title.text()
    question_data["subtitle"] = self.question_subtitle.text()
    
    # Options
    options = []
    for i in range(self.options_list.count()):
        options.append(self.options_list.item(i).text())
    question_data["options"] = options
    
    # Correct answer
    if self.correct_answer_combo.currentIndex() >= 0 and self.correct_answer_combo.currentIndex() < len(options):
        question_data["correct_answer"] = options[self.correct_answer_combo.currentIndex()]
    
    # Option images
    option_images = []
    for i in range(self.option_images_list.count()):
        option_images.append(self.option_images_list.item(i).text())
    if option_images:
        question_data["option_images"] = option_images
    elif "option_images" in question_data:
        del question_data["option_images"]
    
    # Info text and robot speech
    question_data["info_text"] = self.info_text.toPlainText()
    question_data["robot_speech"] = self.robot_speech.toPlainText()
    
    # Background color
    question_data["body_class"] = self.bg_color_label.text()
    
    # Button images
    question_data["next_button_image"] = self.next_btn_path.text()
    question_data["more_button_image"] = self.more_btn_path.text()
    
    # Update the question list
    self.update_question_list()
    
    # Show success message
    self.status_bar.showMessage(f"Question {row+1} updated", 3000)

def cancel_question_changes(self):
    """Cancel changes to the current question"""
    current_row = self.question_list.currentRow()
    if current_row >= 0:
        self.question_selected(current_row)

def clear_question_form(self):
    """Clear the question form"""
    self.question_id_label.setText("")
    self.question_text.setText("")
    self.question_title.setText("")
    self.question_subtitle.setText("")
    self.options_list.clear()
    self.correct_answer_combo.clear()
    self.option_images_list.clear()
    self.info_text.setText("")
    self.robot_speech.setText("")
    self.bg_color_label.setText("bg-secondary quiz")
    self.next_btn_path.setText("../images/next_button.png")
    self.more_btn_path.setText("../images/info_button.png")

# Option Management Methods
def add_option(self):
    """Add a new option"""
    option_text, ok = QMessageBox.getText(self, "Add Option", "Enter option text:")
    if ok and option_text:
        self.options_list.addItem(option_text)
        self.correct_answer_combo.addItem(option_text)

def edit_option(self):
    """Edit the selected option"""
    current_row = self.options_list.currentRow()
    if current_row >= 0:
        current_text = self.options_list.item(current_row).text()
        new_text, ok = QMessageBox.getText(self, "Edit Option", "Edit option text:", text=current_text)
        if ok and new_text:
            self.options_list.item(current_row).setText(new_text)
            if current_row < self.correct_answer_combo.count():
                self.correct_answer_combo.setItemText(current_row, new_text)

def remove_option(self):
    """Remove the selected option"""
    current_row = self.options_list.currentRow()
    if current_row >= 0:
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                     "Are you sure you want to delete this option?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.options_list.takeItem(current_row)
            if current_row < self.correct_answer_combo.count():
                self.correct_answer_combo.removeItem(current_row)

# Option Image Management Methods
def add_option_image(self):
    """Add an image for an option"""
    file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)")
    if file_path:
        # Convert to relative path if possible
        relative_path = file_path
        if self.image_dir_path:
            try:
                image_dir = Path(self.image_dir_path)
                file = Path(file_path)
                if image_dir in file.parents:
                    relative_path = f"../images/{file.name}"
            except:
                pass
        self.option_images_list.addItem(relative_path)

def remove_option_image(self):
    """Remove the selected option image"""
    current_row = self.option_images_list.currentRow()
    if current_row >= 0:
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                     "Are you sure you want to delete this image?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.option_images_list.takeItem(current_row)

# General Settings Methods
def add_css_file(self):
    """Add a CSS file"""
    file_path, _ = QFileDialog.getOpenFileName(self, "Select CSS File", "", "CSS Files (*.css)")
    if file_path:
        self.css_files_list.addItem(file_path)

def remove_css_file(self):
    """Remove the selected CSS file"""
    current_row = self.css_files_list.currentRow()
    if current_row >= 0:
        self.css_files_list.takeItem(current_row)

def add_js_file(self):
    """Add a JavaScript file"""
    file_path, _ = QFileDialog.getOpenFileName(self, "Select JavaScript File", "", "JavaScript Files (*.js)")
    if file_path:
        self.js_files_list.addItem(file_path)

def remove_js_file(self):
    """Remove the selected JavaScript file"""
    current_row = self.js_files_list.currentRow()
    if current_row >= 0:
        self.js_files_list.takeItem(current_row)

def browse_image(self, button_type):
    """Browse for button images"""
    file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)")
    if file_path:
        # Convert to relative path if possible
        relative_path = file_path
        if self.image_dir_path:
            try:
                image_dir = Path(self.image_dir_path)
                file = Path(file_path)
                if image_dir in file.parents:
                    relative_path = f"../images/{file.name}"
            except:
                pass
        
        if button_type == "next_button":
            self.next_btn_path.setText(relative_path)
        elif button_type == "more_button":
            self.more_btn_path.setText(relative_path)

def browse_sound_file_path(self):
    """Browse for sound file"""
    file_path, _ = QFileDialog.getOpenFileName(self, "Select Sound File", "", "Sound Files (*.ogg *.wav *.mp3)")
    if file_path:
        self.sound_file_path.setText(file_path)

def browse_image_directory(self):
    """Browse for image directory"""
    dir_path = QFileDialog.getExistingDirectory(self, "Select Image Directory")
    if dir_path:
        self.image_dir_path = dir_path
        self.image_dir_field.setText(dir_path)
        
        # Update assets list
        self.update_assets_list()

def browse_output_directory(self):
    """Browse for output directory"""
    dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
    if dir_path:
        self.output_dir_field.setText(dir_path)

def apply_general_settings(self):
    """Apply general settings"""
    # Total questions
    if self.total_questions.text().isdigit():
        self.quiz_config["total_questions"] = int(self.total_questions.text())
    else:
        self.quiz_config["total_questions"] = len(self.quiz_config["quiz_pages"])
        self.total_questions.setText(str(self.quiz_config["total_questions"]))
    
    # Sound file
    self.quiz_config["sound_file"] = self.sound_file_path.text()
    
    # CSS files
    css_files = []
    for i in range(self.css_files_list.count()):
        css_files.append(self.css_files_list.item(i).text())
    self.quiz_config["css_files"] = css_files
    
    # JS files
    js_files = []
    for i in range(self.js_files_list.count()):
        js_files.append(self.js_files_list.item(i).text())
    self.quiz_config["js_files"] = js_files
    
    # Show success message
    self.status_bar.showMessage("General settings applied", 3000)

def update_general_settings_form(self):
    """Update the general settings form with current values"""
    # Total questions
    self.total_questions.setText(str(self.quiz_config.get("total_questions", len(self.quiz_config["quiz_pages"]))))
    
    # Sound file
    self.sound_file_path.setText(self.quiz_config.get("sound_file", "change_screen.ogg"))
    
    # CSS files
    self.css_files_list.clear()
    for css_file in self.quiz_config.get("css_files", []):
        self.css_files_list.addItem(css_file)
    
    # JS files
    self.js_files_list.clear()
    for js_file in self.quiz_config.get("js_files", []):
        self.js_files_list.addItem(js_file)

def apply_start_page_settings(self):
    """Apply start page settings"""
    # Make sure start_page exists in config
    if "start_page" not in self.quiz_config:
        self.quiz_config["start_page"] = {}
    
    # Apply settings
    self.quiz_config["start_page"]["title"] = self.start_title.text()
    self.quiz_config["start_page"]["subtitle"] = self.start_subtitle.toPlainText()
    self.quiz_config["start_page"]["credits"] = self.start_credits.text()
    self.quiz_config["start_page"]["yes_button_text"] = self.yes_button_text.text()
    self.quiz_config["start_page"]["no_button_text"] = self.no_button_text.text()
    self.quiz_config["start_page"]["body_class"] = self.start_bg_color_label.text()
    
    # Show success message
    self.status_bar.showMessage("Start page settings applied", 3000)

def update_start_page_form(self):
    """Update the start page form with current values"""
    if "start_page" in self.quiz_config:
        start_page = self.quiz_config["start_page"]
        self.start_title.setText(start_page.get("title", "Welcome to the Quiz!"))
        self.start_subtitle.setText(start_page.get("subtitle", "Would you like to take the quiz?"))
        self.start_credits.setText(start_page.get("credits", ""))
        self.yes_button_text.setText(start_page.get("yes_button_text", "Yes"))
        self.no_button_text.setText(start_page.get("no_button_text", "No"))
        self.start_bg_color_label.setText(start_page.get("body_class", "bg-primary"))
    else:
        # Default values
        self.start_title.setText("Welcome to the Quiz!")
        self.start_subtitle.setText("Would you like to take the quiz?")
        self.start_credits.setText("")
        self.yes_button_text.setText("Yes")
        self.no_button_text.setText("No")
        self.start_bg_color_label.setText("bg-primary")

# Color and styling methods
def choose_bg_color(self):
    """Choose a background color class"""
    color_classes = [
        "bg-primary", "bg-secondary", "bg-success", "bg-danger", 
        "bg-warning", "bg-info", "bg-light", "bg-dark"
    ]
    current_class = self.bg_color_label.text().split()[0]  # Get first part of class
    
    # Create a simple dialog to select a color class
    color_dialog = QMessageBox()
    color_dialog.setWindowTitle("Choose Background Color Class")
    
    # Add buttons for each color class
    for color_class in color_classes:
        color_dialog.addButton(color_class, QMessageBox.AcceptRole)
    
    color_dialog.exec_()
    
    clicked_button = color_dialog.clickedButton()
    if clicked_button:
        selected_class = clicked_button.text()
        if "quiz" in self.bg_color_label.text():
            self.bg_color_label.setText(f"{selected_class} quiz")
        else:
            self.bg_color_label.setText(selected_class)

def choose_start_bg_color(self):
    """Choose a background color class for the start page"""
    color_classes = [
        "bg-primary", "bg-secondary", "bg-success", "bg-danger", 
        "bg-warning", "bg-info", "bg-light", "bg-dark"
    ]
    
    # Create a simple dialog to select a color class
    color_dialog = QMessageBox()
    color_dialog.setWindowTitle("Choose Background Color Class")
    
    # Add buttons for each color class
    for color_class in color_classes:
        color_dialog.addButton(color_class, QMessageBox.AcceptRole)
    
    color_dialog.exec_()
    
    clicked_button = color_dialog.clickedButton()
    if clicked_button:
        self.start_bg_color_label.setText(clicked_button.text())

# Asset management methods
def add_asset(self):
    """Add an asset to the assets list"""
    file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Assets", "", 
                                               "Image Files (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)")
    if file_paths:
        for file_path in file_paths:
            if file_path not in self.current_assets:
                self.assets_list.addItem(file_path)
                self.current_assets.append(file_path)

def remove_asset(self):
    """Remove the selected asset"""
    current_row = self.assets_list.currentRow()
    if current_row >= 0:
        asset_path = self.assets_list.item(current_row).text()
        self.assets_list.takeItem(current_row)
        if asset_path in self.current_assets:
            self.current_assets.remove(asset_path)

def copy_asset_to_images(self):
    """Copy the selected asset to the images directory"""
    current_row = self.assets_list.currentRow()
    if current_row >= 0:
        asset_path = self.assets_list.item(current_row).text()
        
        if not self.image_dir_path:
            # Ask for image directory if not set
            self.browse_image_directory()
            if not self.image_dir_path:
                QMessageBox.warning(self, "No Image Directory", 
                                  "Please select an image directory first.")
                return
        
        # Copy the file
        try:
            file_path = Path(asset_path)
            dest_path = Path(self.image_dir_path) / file_path.name
            shutil.copy2(file_path, dest_path)
            QMessageBox.information(self, "Copy Successful", 
                                   f"Asset copied to {dest_path}")
        except Exception as e:
            QMessageBox.warning(self, "Copy Failed", 
                               f"Failed to copy asset: {str(e)}")

def preview_asset(self, item):
    """Preview the selected asset"""
    file_path = item.text()
    if os.path.exists(file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            # Scale pixmap to fit the label while maintaining aspect ratio
            pixmap = pixmap.scaled(self.preview_label.size(), 
                                  Qt.KeepAspectRatio, 
                                  Qt.SmoothTransformation)
            self.preview_label.setPixmap(pixmap)
        else:
            self.preview_label.setText("Cannot preview this file type")
    else:
        self.preview_label.setText("File not found")

def update_assets_list(self):
    """Update the assets list with files from the image directory"""
    self.assets_list.clear()
    self.current_assets = []
    
    if self.image_dir_path and os.path.exists(self.image_dir_path):
        image_dir = Path(self.image_dir_path)
        image_files = list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpg")) + \
                     list(image_dir.glob("*.jpeg")) + list(image_dir.glob("*.gif")) + \
                     list(image_dir.glob("*.bmp"))
        
        for file_path in image_files:
            self.assets_list.addItem(str(file_path))
            self.current_assets.append(str(file_path))

# File operations
def new_config(self):
    """Create a new quiz configuration"""
    reply = QMessageBox.question(self, "Create New Configuration", 
                               "Are you sure you want to create a new configuration? Any unsaved changes will be lost.",
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        self.quiz_config = {
            "quiz_pages": [],
            "start_page": {
                "body_class": "bg-primary",
                "title": "Welcome to the Quiz!",
                "subtitle": "Would you like to take the quiz?",
                "yes_button_text": "Yes",
                "no_button_text": "No"
            },
            "total_questions": 0,
            "sound_file": "change_screen.ogg",
            "css_files": [],
            "js_files": []
        }
        self.config_file_path = None
        
        # Update UI
        self.update_question_list()
        self.update_general_settings_form()
        self.update_start_page_form()
        self.clear_question_form()
        
        self.status_bar.showMessage("New configuration created", 3000)

def open_config(self):
    """Open an existing quiz configuration"""
    file_path, _ = QFileDialog.getOpenFileName(self, "Open Quiz Configuration", "", "JSON Files (*.json)")
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.quiz_config = json.load(f)
            
            self.config_file_path = file_path
            
            # Update UI
            self.update_question_list()
            self.update_general_settings_form()
            self.update_start_page_form()
            
            if self.quiz_config["quiz_pages"]:
                self.question_list.setCurrentRow(0)
            else:
                self.clear_question_form()
            
            self.status_bar.showMessage(f"Opened {os.path.basename(file_path)}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error Opening File", 
                                f"Failed to open configuration file: {str(e)}")

def save_config(self):
    """Save the current quiz configuration"""
    if self.config_file_path:
        self._save_to_file(self.config_file_path)
    else:
        self.save_config_as()

def save_config_as(self):
    """Save the current quiz configuration to a new file"""
    file_path, _ = QFileDialog.getSaveFileName(self, "Save Quiz Configuration", "", "JSON Files (*.json)")
    if file_path:
        if not file_path.endswith('.json'):
            file_path += '.json'
        self._save_to_file(file_path)
        self.config_file_path = file_path

def _save_to_file(self, file_path):
    """Save configuration to a file"""
    try:
        # Ensure the quiz_config is updated with the current form values
        current_row = self.question_list.currentRow()
        if current_row >= 0:
            self.apply_question_changes()
        
        self.apply_general_settings()
        self.apply_start_page_settings()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.quiz_config, f, indent=4, ensure_ascii=False)
        
        self.status_bar.showMessage(f"Saved to {os.path.basename(file_path)}", 3000)
    except Exception as e:
        QMessageBox.critical(self, "Error Saving File", 
                            f"Failed to save configuration file: {str(e)}")

def generate_quiz(self):
    """Generate the quiz HTML files using the PepperQuizGenerator"""
    # First save the configuration
    if not self.config_file_path:
        self.save_config_as()
        if not self.config_file_path:
            return  # User cancelled save
    else:
        self.save_config()
    
    # Get output directory
    output_dir = self.output_dir_field.text()
    if not output_dir:
        output_dir = "generated_quiz"
    
    # Get image directory
    image_dir = self.image_dir_path
    if not image_dir:
        image_dir = "images"
    
    if PepperQuizGenerator:
        try:
            # Initialize the generator
            generator = PepperQuizGenerator(
                config_file=self.config_file_path,
                output_dir=output_dir,
                image_dir=image_dir
            )
            
            # Generate the quiz
            if generator.load_config():
                generator.generate_quiz_pages()
                QMessageBox.information(self, "Generation Complete", 
                                      f"Quiz pages generated successfully in '{output_dir}' directory!")
            else:
                QMessageBox.critical(self, "Generation Failed", 
                                   "Failed to load configuration.")
        except Exception as e:
            QMessageBox.critical(self, "Generation Error", 
                               f"Error generating quiz: {str(e)}")
    else:
        QMessageBox.critical(self, "Module Not Found", 
                           "PepperQuizGenerator module not found. Make sure the Quiz_generator package is in your Python path.")

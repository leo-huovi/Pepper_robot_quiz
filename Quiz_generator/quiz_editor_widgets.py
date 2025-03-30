#!/usr/bin/env python3
"""
Pepper Robot Quiz Editor
Main application window and widgets
"""

import os
import json
import shutil
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFileDialog, 
                             QTabWidget, QFormLayout, QTextEdit, QMessageBox, 
                             QComboBox, QGroupBox, QScrollArea, QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from quiz_editor_custom import DraggableListWidget
from quiz_editor_utils import import_quiz_generator_module

# Try to import the quiz generator module
PepperQuizGenerator = import_quiz_generator_module()

class QuizEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize variables
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
        self.image_dir_path = None
        self.current_assets = []
        
        # Setup UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Pepper Robot Quiz Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # File operations layout
        file_ops_layout = QHBoxLayout()
        
        # New, Open, Save, Save As buttons
        self.new_btn = QPushButton("New")
        self.open_btn = QPushButton("Open")
        self.save_btn = QPushButton("Save")
        self.save_as_btn = QPushButton("Save As")
        self.generate_btn = QPushButton("Generate Quiz")
        
        # Connect buttons to functions
        self.new_btn.clicked.connect(self.new_config)
        self.open_btn.clicked.connect(self.open_config)
        self.save_btn.clicked.connect(self.save_config)
        self.save_as_btn.clicked.connect(self.save_config_as)
        self.generate_btn.clicked.connect(self.generate_quiz)
        
        # Add buttons to layout
        file_ops_layout.addWidget(self.new_btn)
        file_ops_layout.addWidget(self.open_btn)
        file_ops_layout.addWidget(self.save_btn)
        file_ops_layout.addWidget(self.save_as_btn)
        file_ops_layout.addWidget(self.generate_btn)
        
        # Add file operations to main layout
        main_layout.addLayout(file_ops_layout)
        
        # Left panel (question list) and right panel (question editor)
        content_layout = QHBoxLayout()
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        self.question_list_label = QLabel("Quiz Questions:")
        self.question_list = DraggableListWidget()
        self.question_list.currentRowChanged.connect(self.question_selected)
        
        # Buttons for adding and removing questions
        question_buttons_layout = QHBoxLayout()
        self.add_question_btn = QPushButton("Add Question")
        self.remove_question_btn = QPushButton("Remove Question")
        self.duplicate_question_btn = QPushButton("Duplicate")
        
        self.add_question_btn.clicked.connect(self.add_question)
        self.remove_question_btn.clicked.connect(self.remove_question)
        self.duplicate_question_btn.clicked.connect(self.duplicate_question)
        
        question_buttons_layout.addWidget(self.add_question_btn)
        question_buttons_layout.addWidget(self.remove_question_btn)
        question_buttons_layout.addWidget(self.duplicate_question_btn)
        
        left_layout.addWidget(self.question_list_label)
        left_layout.addWidget(self.question_list)
        left_layout.addLayout(question_buttons_layout)
        left_panel.setLayout(left_layout)
        
        # Right panel
        right_panel = QTabWidget()
        
        # Question editor tab
        self.question_editor = QWidget()
        self.setup_question_editor()
        
        # General settings tab
        self.general_settings = QWidget()
        self.setup_general_settings()
        
        # Start page settings tab
        self.start_page_settings = QWidget()
        self.setup_start_page_settings()
        
        # Assets manager tab
        self.assets_manager = QWidget()
        self.setup_assets_manager()
        
        # Add tabs
        right_panel.addTab(self.question_editor, "Question Editor")
        right_panel.addTab(self.general_settings, "General Settings")
        right_panel.addTab(self.start_page_settings, "Start Page")
        right_panel.addTab(self.assets_manager, "Assets Manager")
        
        # Add panels to content layout
        content_layout.addWidget(left_panel, 1)
        content_layout.addWidget(right_panel, 2)
        
        # Add content layout to main layout
        main_layout.addLayout(content_layout)
        
        # Status bar for showing messages
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
        # Set the main layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Initialize with empty form
        self.clear_question_form()
        self.update_question_list()
        self.update_general_settings_form()
        self.update_start_page_form()
        
    def setup_question_editor(self):
        """Setup the question editor form"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        question_form_widget = QWidget()
        form_layout = QFormLayout()
        
        # Question ID (position)
        self.question_id_label = QLabel("Question #: ")
        form_layout.addRow(QLabel("ID:"), self.question_id_label)
        
        # Question text
        self.question_text = QLineEdit()
        form_layout.addRow(QLabel("Question:"), self.question_text)
        
        # Question title
        self.question_title = QLineEdit()
        form_layout.addRow(QLabel("Title:"), self.question_title)
        
        # Question subtitle
        self.question_subtitle = QLineEdit()
        form_layout.addRow(QLabel("Subtitle:"), self.question_subtitle)
        
        # Options group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        # Options list
        self.options_list = DraggableListWidget()
        options_layout.addWidget(self.options_list)
        
        # Options buttons
        options_buttons_layout = QHBoxLayout()
        self.add_option_btn = QPushButton("Add Option")
        self.edit_option_btn = QPushButton("Edit Option")
        self.remove_option_btn = QPushButton("Remove Option")
        
        self.add_option_btn.clicked.connect(self.add_option)
        self.edit_option_btn.clicked.connect(self.edit_option)
        self.remove_option_btn.clicked.connect(self.remove_option)
        
        options_buttons_layout.addWidget(self.add_option_btn)
        options_buttons_layout.addWidget(self.edit_option_btn)
        options_buttons_layout.addWidget(self.remove_option_btn)
        
        # Correct answer
        correct_answer_layout = QHBoxLayout()
        correct_answer_layout.addWidget(QLabel("Correct Answer:"))
        self.correct_answer_combo = QComboBox()
        correct_answer_layout.addWidget(self.correct_answer_combo)
        
        options_layout.addLayout(options_buttons_layout)
        options_layout.addLayout(correct_answer_layout)
        options_group.setLayout(options_layout)
        form_layout.addRow(options_group)
        
        # Option images
        option_images_group = QGroupBox("Option Images (optional)")
        option_images_layout = QVBoxLayout()
        
        self.option_images_list = DraggableListWidget()
        option_images_layout.addWidget(self.option_images_list)
        
        option_images_buttons_layout = QHBoxLayout()
        self.add_option_image_btn = QPushButton("Add Image")
        self.remove_option_image_btn = QPushButton("Remove Image")
        
        self.add_option_image_btn.clicked.connect(self.add_option_image)
        self.remove_option_image_btn.clicked.connect(self.remove_option_image)
        
        option_images_buttons_layout.addWidget(self.add_option_image_btn)
        option_images_buttons_layout.addWidget(self.remove_option_image_btn)
        
        option_images_layout.addLayout(option_images_buttons_layout)
        option_images_group.setLayout(option_images_layout)
        form_layout.addRow(option_images_group)
        
        # Info text
        self.info_text = QTextEdit()
        form_layout.addRow(QLabel("Info Text:"), self.info_text)
        
        # Robot speech
        self.robot_speech = QTextEdit()
        form_layout.addRow(QLabel("Robot Speech:"), self.robot_speech)
        
        # Background color
        bg_color_layout = QHBoxLayout()
        self.bg_color_label = QLabel("bg-secondary quiz")
        self.bg_color_btn = QPushButton("Choose Color")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        
        bg_color_layout.addWidget(self.bg_color_label)
        bg_color_layout.addWidget(self.bg_color_btn)
        form_layout.addRow(QLabel("Background Class:"), bg_color_layout)
        
        # Button images
        next_btn_layout = QHBoxLayout()
        self.next_btn_path = QLineEdit()
        self.next_btn_path.setReadOnly(True)
        self.browse_next_btn = QPushButton("Browse")
        self.browse_next_btn.clicked.connect(lambda: self.browse_image("next_button"))
        
        next_btn_layout.addWidget(self.next_btn_path)
        next_btn_layout.addWidget(self.browse_next_btn)
        form_layout.addRow(QLabel("Next Button Image:"), next_btn_layout)
        
        more_btn_layout = QHBoxLayout()
        self.more_btn_path = QLineEdit()
        self.more_btn_path.setReadOnly(True)
        self.browse_more_btn = QPushButton("Browse")
        self.browse_more_btn.clicked.connect(lambda: self.browse_image("more_button"))
        
        more_btn_layout.addWidget(self.more_btn_path)
        more_btn_layout.addWidget(self.browse_more_btn)
        form_layout.addRow(QLabel("More Info Button Image:"), more_btn_layout)
        
        # Apply/Cancel buttons
        buttons_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Apply Changes")
        self.cancel_btn = QPushButton("Cancel Changes")
        
        self.apply_btn.clicked.connect(self.apply_question_changes)
        self.cancel_btn.clicked.connect(self.cancel_question_changes)
        
        buttons_layout.addWidget(self.apply_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        form_layout.addRow(buttons_layout)
        
        question_form_widget.setLayout(form_layout)
        scroll_area.setWidget(question_form_widget)
        
        editor_layout = QVBoxLayout()
        editor_layout.addWidget(scroll_area)
        self.question_editor.setLayout(editor_layout)
    
    def setup_general_settings(self):
        """Setup the general settings form"""
        form_layout = QFormLayout()
        
        # Total questions
        self.total_questions = QLineEdit()
        form_layout.addRow(QLabel("Total Questions:"), self.total_questions)
        
        # Sound file
        sound_file_layout = QHBoxLayout()
        self.sound_file_path = QLineEdit()
        self.browse_sound_file = QPushButton("Browse")
        self.browse_sound_file.clicked.connect(self.browse_sound_file_path)
        
        sound_file_layout.addWidget(self.sound_file_path)
        sound_file_layout.addWidget(self.browse_sound_file)
        form_layout.addRow(QLabel("Sound File:"), sound_file_layout)
        
        # CSS files
        css_layout = QVBoxLayout()
        self.css_files_list = DraggableListWidget()
        css_buttons_layout = QHBoxLayout()
        
        self.add_css_btn = QPushButton("Add CSS")
        self.remove_css_btn = QPushButton("Remove CSS")
        
        self.add_css_btn.clicked.connect(self.add_css_file)
        self.remove_css_btn.clicked.connect(self.remove_css_file)
        
        css_buttons_layout.addWidget(self.add_css_btn)
        css_buttons_layout.addWidget(self.remove_css_btn)
        
        css_layout.addWidget(self.css_files_list)
        css_layout.addLayout(css_buttons_layout)
        form_layout.addRow(QLabel("CSS Files:"), css_layout)
        
        # JS files
        js_layout = QVBoxLayout()
        self.js_files_list = DraggableListWidget()
        js_buttons_layout = QHBoxLayout()
        
        self.add_js_btn = QPushButton("Add JavaScript")
        self.remove_js_btn = QPushButton("Remove JavaScript")
        
        self.add_js_btn.clicked.connect(self.add_js_file)
        self.remove_js_btn.clicked.connect(self.remove_js_file)
        
        js_buttons_layout.addWidget(self.add_js_btn)
        js_buttons_layout.addWidget(self.remove_js_btn)
        
        js_layout.addWidget(self.js_files_list)
        js_layout.addLayout(js_buttons_layout)
        form_layout.addRow(QLabel("JavaScript Files:"), js_layout)
        
        # Image directory
        image_dir_layout = QHBoxLayout()
        self.image_dir_field = QLineEdit()
        self.browse_image_dir = QPushButton("Browse")
        self.browse_image_dir.clicked.connect(self.browse_image_directory)
        
        image_dir_layout.addWidget(self.image_dir_field)
        image_dir_layout.addWidget(self.browse_image_dir)
        form_layout.addRow(QLabel("Image Directory:"), image_dir_layout)
        
        # Output directory
        output_dir_layout = QHBoxLayout()
        self.output_dir_field = QLineEdit()
        self.output_dir_field.setText("generated_quiz")
        self.browse_output_dir = QPushButton("Browse")
        self.browse_output_dir.clicked.connect(self.browse_output_directory)
        
        output_dir_layout.addWidget(self.output_dir_field)
        output_dir_layout.addWidget(self.browse_output_dir)
        form_layout.addRow(QLabel("Output Directory:"), output_dir_layout)
        
        # Apply button
        self.apply_general_settings_btn = QPushButton("Apply General Settings")
        self.apply_general_settings_btn.clicked.connect(self.apply_general_settings)
        form_layout.addRow(self.apply_general_settings_btn)
        
        self.general_settings.setLayout(form_layout)
    
    def setup_start_page_settings(self):
        """Setup the start page settings form"""
        form_layout = QFormLayout()
        
        # Title
        self.start_title = QLineEdit()
        form_layout.addRow(QLabel("Title:"), self.start_title)
        
        # Subtitle
        self.start_subtitle = QTextEdit()
        form_layout.addRow(QLabel("Subtitle:"), self.start_subtitle)
        
        # Credits
        self.start_credits = QLineEdit()
        form_layout.addRow(QLabel("Credits:"), self.start_credits)
        
        # Yes/No button text
        self.yes_button_text = QLineEdit()
        form_layout.addRow(QLabel("Yes Button Text:"), self.yes_button_text)
        
        self.no_button_text = QLineEdit()
        form_layout.addRow(QLabel("No Button Text:"), self.no_button_text)
        
        # Background color
        bg_color_layout = QHBoxLayout()
        self.start_bg_color_label = QLabel("bg-primary")
        self.start_bg_color_btn = QPushButton("Choose Color")
        self.start_bg_color_btn.clicked.connect(self.choose_start_bg_color)
        
        bg_color_layout.addWidget(self.start_bg_color_label)
        bg_color_layout.addWidget(self.start_bg_color_btn)
        form_layout.addRow(QLabel("Background Class:"), bg_color_layout)
        
        # Apply button
        self.apply_start_page_btn = QPushButton("Apply Start Page Settings")
        self.apply_start_page_btn.clicked.connect(self.apply_start_page_settings)
        form_layout.addRow(self.apply_start_page_btn)
        
        self.start_page_settings.setLayout(form_layout)
    
    def setup_assets_manager(self):
        """Setup the assets manager tab"""
        layout = QVBoxLayout()
        
        # Image preview and list
        self.assets_list = DraggableListWidget()
        self.assets_list.itemClicked.connect(self.preview_asset)
        
        # Preview label
        self.preview_label = QLabel("Select an asset to preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        self.add_asset_btn = QPushButton("Add Asset")
        self.remove_asset_btn = QPushButton("Remove Asset")
        self.copy_asset_btn = QPushButton("Copy to Images Directory")
        
        self.add_asset_btn.clicked.connect(self.add_asset)
        self.remove_asset_btn.clicked.connect(self.remove_asset)
        self.copy_asset_btn.clicked.connect(self.copy_asset_to_images)
        
        buttons_layout.addWidget(self.add_asset_btn)
        buttons_layout.addWidget(self.remove_asset_btn)
        buttons_layout.addWidget(self.copy_asset_btn)
        
        layout.addWidget(QLabel("Assets:"))
        layout.addWidget(self.assets_list)
        layout.addWidget(QLabel("Preview:"))
        layout.addWidget(self.preview_label)
        layout.addLayout(buttons_layout)
        
        self.assets_manager.setLayout(layout)
    
    from quiz_editor_handlers import (
        add_question, remove_question, duplicate_question,
        update_question_list, question_selected,
        apply_question_changes, cancel_question_changes, clear_question_form,
        add_option, edit_option, remove_option,
        add_option_image, remove_option_image,
        add_css_file, remove_css_file,
        add_js_file, remove_js_file,
        browse_image, browse_sound_file_path,
        browse_image_directory, browse_output_directory,
        apply_general_settings, update_general_settings_form,
        apply_start_page_settings, update_start_page_form,
        choose_bg_color, choose_start_bg_color,
        add_asset, remove_asset, copy_asset_to_images, preview_asset,
        new_config, open_config, save_config, save_config_as, generate_quiz
    )

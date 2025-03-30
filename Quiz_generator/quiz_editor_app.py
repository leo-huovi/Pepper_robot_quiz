#!/usr/bin/env python3
"""
Pepper Robot Quiz Editor
Main application entry point
"""

import sys
from PyQt5.QtWidgets import QApplication
from quiz_editor_widgets import QuizEditorApp

def main():
    app = QApplication(sys.argv)
    window = QuizEditorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

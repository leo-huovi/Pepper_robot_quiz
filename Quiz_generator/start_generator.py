#!/usr/bin/env python3
"""
Pepper Robot Quiz Generator
Start page generator
"""

from .base_generator import BasePageGenerator
from .html_utils import get_html_header

class StartPageGenerator(BasePageGenerator):
    """Generator for the quiz start page"""
    
    def __init__(self, output_dir):
        """Initialize the start page generator"""
        super().__init__(output_dir)
        
        # Default template for start page
        self.template = """
<body class="{body_class}">
        <header class="section1">
                <div class="container-fluid">
                        <div class="row">
                                <nav class="col-xs-12">
                                <a onclick="exit()" class="float-right"><i class="text-shadow fas fa-times-circle fa-3x"></i></a>
                                </nav>
                        </div>
                </div>
        </header>

                <div class="container">
                        <div class="row">
                                <div class="col-sm-12">
                                        <h1>{title}</h1>
                                        <h3>{subtitle}</h3>
                                        <h4>{credits}</h4>
                                </div>
                        </div>

                        <div class="row">
                                <div class="col-sm-12 flex-parent buttonarea">
                                        <a onclick="yes_clicked()" class="button">{yes_button_text}</a>
                                        <a onclick="no_clicked()" class="button">{no_button_text}</a>
                                </div>
                        </div>
        </div>
        <script>
        var session = new QiSession();
        var audio = new Audio('../../change_screen.ogg');

        function yes_clicked(){{
                audio.play();
                session.service('ALMemory').done(function(ALMemory) {{
                        ALMemory.raiseEvent("orientation/silence", 1);
                        ALMemory.raiseEvent("orientation/answerContinue", 0);
                }});
        }}

        function no_clicked(){{
                audio.play();
                session.service('ALMemory').done(function(ALMemory) {{
                        ALMemory.raiseEvent("orientation/silence", 1);
                        ALMemory.raiseEvent("orientation/answerStop", 1);
                }});
        }}

        function exit(){{
                audio.play();
                session.service('ALMemory').done(function(ALMemory) {{
                        ALMemory.raiseEvent("orientation/silence", 1);
                        ALMemory.raiseEvent("Orientation/Exit", 1);
                }});
        }}

        </script>
</body>
</html>"""
    
    def generate(self, total_questions, config=None):
        """Generate the quiz start page"""
        output_file = self.output_dir / "quiz-start-en.html"
        
        # Use configuration if provided, otherwise use defaults
        if config is None:
            config = {}
        
        # Create template data
        template_data = {
            "body_class": config.get("body_class", "bg-primary"),
            "title": config.get("title", "Welcome to the Tampere Quiz!"),
            "subtitle": config.get("subtitle", "I've been visiting different attractions and places in Tampere and I took lots of pictures from my journey. Would you like to guess the places I visited?"),
            "credits": config.get("credits", "Pictures: Visit Tampere / Laura Vanzo, Olli-Pekka Latvala ja Kladez Zolota. Editing: Santeri Holappa."),
            "yes_button_text": config.get("yes_button_text", "Yes"),
            "no_button_text": config.get("no_button_text", "No")
        }
        
        # Get HTML header and apply template
        header = get_html_header(
            0, 
            template_data["title"],
            config.get("stylesheets", None)
        )
        
        body = self.apply_template(self.template, template_data)
        html = header + body
        
        # Write HTML to file
        self._write_to_file(output_file, html)

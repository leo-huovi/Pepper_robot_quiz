#!/usr/bin/env python3
"""
Pepper Robot Quiz Generator
Answer page generator
"""

from .base_generator import BasePageGenerator
from .html_utils import get_html_header

class AnswerPageGenerator(BasePageGenerator):
    """Generator for quiz answer pages"""
    
    def __init__(self, output_dir):
        """Initialize the answer page generator"""
        super().__init__(output_dir)
        
        # Default template for answer pages
        self.template = """
<body id="quiz-page-{quiz_num}" class="{body_class}">
        <header class="section1">
                <div class="container-fluid">
                        <div class="row">
                                <div class="col-xs-2">
                                        <h2 class="quiz-progress"><span id="question"></span>/{total_questions}</h2>
                                </div>
                                <div class="col-xs-8">
                                        <h2 id="qtitle" class="quiz-title">{title}</h2>
                                </div>
                                <nav class="col-xs-2">
                                        <a onmouseup="exit()" class="float-right"><i class="text-shadow fas fa-times-circle fa-3x"></i></a>
                                </nav>
                        </div>
                </div>
        </header>
                <div class="container">
                        <!-- Display correct answer image if provided -->
                        <div class="row" id="correct_answer_container" style="text-align: center; margin: 20px 0;">
                                {correct_answer_html}
                        </div>
                </div>
                <div class="container" style="width:80%;position:fixed;bottom:10px;margin-left:10%">
                        <div class="row">
                                <div id="after_question" class="col-sm-12 flex-parent buttonarea wrap" style="display:block">
                                        <button type="submit" onmouseup="yes_clicked()" class="img-button">
                                            <img src="{next_button_image}" alt="Next question">
                                        </button>
                                        <button type="submit" id="more_button" onmouseup="more_clicked()" class="img-button">
                                            <img src="{more_button_image}" alt="More info">
                                        </button>
                                </div>
                        </div>
        </div>

        <script>
                var session = new QiSession();
                var audio = new Audio('../change_screen.ogg');

                document.getElementById("question").innerHTML = getUrlVars()["question"];

                function getUrlVars() {{
                        var vars = {{}};
                        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {{
                                vars[key] = value;
                        }});

                        return vars;
                }}

                function yes_clicked(){{
                        audio.play();
                        session.service('ALMemory').done(function(ALMemory) {{
                                ALMemory.raiseEvent("orientation/silence", 1);
                                ALMemory.raiseEvent("orientation/answerContinue", 0);
                        }});
                }}

                function exit(){{
                        audio.play();
                        session.service('ALMemory').done(function(ALMemory) {{
                                ALMemory.raiseEvent("orientation/silence", 1);
                                ALMemory.raiseEvent("Orientation/Exit", 0);
                        }});
                }}

                function more_clicked(){{
                        audio.play();
                        document.getElementById("more_button").style.display = 'none';
                        document.getElementById("qtitle").innerHTML = '<h2>{title}</h2><h3>{subtitle}</h3>'
                        session.service('ALMemory').done(function(ALMemory) {{
                                ALMemory.raiseEvent("orientation/silence", 1);
                                ALMemory.raiseEvent("orientation/say_info", "{robot_speech}");
                        }});
                }}

        </script>

</body>
</html>"""
    
    def generate(self, quiz_num, quiz_data, total_questions):
        """Generate the answer page shown after user selects an answer"""
        output_file = self.output_dir / f"quiz{quiz_num}_ans.html"
        
        # Update button image paths for consistency
        next_button_image = quiz_data.get("next_button_image", "../site/img/next_button.png")
        if next_button_image.startswith("../images/"):
            next_button_image = "../site/img/" + next_button_image.replace("../images/", "")
            
        more_button_image = quiz_data.get("more_button_image", "../site/img/info_button.png")
        if more_button_image.startswith("../images/"):
            more_button_image = "../site/img/" + more_button_image.replace("../images/", "")
        
        # Generate correct answer image HTML if available
        correct_answer_html = ""
        if "correct_answer_image" in quiz_data and quiz_data["correct_answer_image"]:
            # Get the correct answer image path
            image_path = quiz_data["correct_answer_image"]
            # Make sure path is relative to site structure
            if not image_path.startswith("../site/img/"):
                # If the path uses "../images/" format, update it
                if image_path.startswith("../images/"):
                    image_path = "../site/img/" + image_path.replace("../images/", "")
            
            # Generate the HTML for the image - hide the text with visibility:hidden
            correct_answer_html = f"""
                <div class="correct-answer-image">
                    <img src="{image_path}" alt="Correct answer" style="max-width: 100%; max-height: 40vh; width: auto; height: auto;">
                    <h3 style="visibility: hidden;" data-correct-option="{quiz_data['correct_answer']}">{quiz_data['correct_answer']}</h3>
                </div>
            """
        # Alternatively, find the correct answer image from option_images if available
        elif "option_images" in quiz_data and "options" in quiz_data and "correct_answer" in quiz_data:
            try:
                correct_idx = quiz_data["options"].index(quiz_data["correct_answer"])
                if correct_idx < len(quiz_data["option_images"]):
                    image_path = quiz_data["option_images"][correct_idx]
                    # Make sure path is relative to site structure
                    if not image_path.startswith("../site/img/"):
                        # If the path uses "../images/" format, update it
                        if image_path.startswith("../images/"):
                            image_path = "../site/img/" + image_path.replace("../images/", "")
                    
                    # Generate the HTML for the image - hide the text with visibility:hidden
                    correct_answer_html = f"""
                        <div class="correct-answer-image">
                            <img src="{image_path}" alt="Correct answer" style="max-width: 100%; max-height: 35vh; width: auto; height: auto;">
                            <h3 style="visibility: hidden;" data-correct-option="{quiz_data['correct_answer']}">{quiz_data['correct_answer']}</h3>
                        </div>
                    """
            except ValueError:
                # Correct answer not found in options, use empty string
                pass
        
        # Create template data
        template_data = {
            "quiz_num": quiz_num,
            "body_class": quiz_data.get("body_class", "bg-secondary quiz"),
            "total_questions": total_questions,
            "title": quiz_data["title"],
            "subtitle": quiz_data.get("subtitle", ""),
            "robot_speech": quiz_data["robot_speech"],
            "next_button_image": next_button_image,
            "more_button_image": more_button_image,
            "correct_answer_html": correct_answer_html
        }
        
        # Get HTML header and apply template
        header = get_html_header(
            quiz_num, 
            quiz_data["title"], 
            quiz_data.get("stylesheets", None)
        )
        
        body = self.apply_template(self.template, template_data)
        html = header + body
        
        # Write HTML to file
        self._write_to_file(output_file, html)

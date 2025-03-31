#!/usr/bin/env python3
"""
Pepper Robot Quiz Generator
Question page generator
"""

from pathlib import Path
from .base_generator import BasePageGenerator
from .html_utils import get_html_header

class QuestionPageGenerator(BasePageGenerator):
    """Generator for quiz question pages"""
    
    def __init__(self, output_dir):
        """Initialize the question page generator"""
        super().__init__(output_dir)
        
        # Default template for question pages
        self.template = """
<body id="quiz-page-{quiz_num}" class="{body_class}">
        <header class="section1">
                <div class="container-fluid">
                        <div class="row">
                                <div class="col-xs-2">
                                        <h2 class="quiz-progress"><span id="question"></span>/{total_questions}</h2>
                                </div>
                                <div class="col-xs-8">
                                        <h2 id="qtitle" class="quiz-title">{question}</h2>
                                </div>
                                <nav class="col-xs-2">
                                        <a onmouseup="exit()" class="float-right"><i class="text-shadow fas fa-times-circle fa-3x"></i></a>
                                </nav>
                        </div>
                </div>
        </header>
                <div class="container" style="width:80%;position:fixed;bottom:10px;margin-left:10%">
                        <div class="row">
                                <div id="ans_buttons" class="col-sm-12 flex-parent buttonarea wrap">
{option_buttons}
                                </div>
                                <div id="after_question" class="col-sm-12 flex-parent buttonarea wrap" style="display:none">
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

                var audio = new Audio('../../change_screen.ogg');
                document.getElementById("question").innerHTML = getUrlVars()["question"]
                function getUrlVars() {{
                        var vars = {{}};
                        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {{
                                vars[key] = value;
                        }});
                        return vars;
                }}
                function wrong_clicked(){{
                        audio.play();
                        session.service('ALMemory').done(function(ALMemory) {{
                                ALMemory.raiseEvent("orientation/silence", 1);
                                ALMemory.raiseEvent("orientation/answerWrong", 0);
                        }});
                        setTimeout(loadAfterTime, 3000);
                }}
                function right_clicked(){{
                        audio.play();
                        session.service('ALMemory').done(function(ALMemory) {{
                                ALMemory.raiseEvent("orientation/silence", 1);
                                ALMemory.raiseEvent("orientation/answerRight", 0);
                        }});
                        setTimeout(loadAfterTime, 3000);
                }}
                function loadAfterTime(){{
                        document.getElementById("ans_buttons").style.display = 'none';
                        document.getElementById("qtitle").innerHTML = "<h2>{title}</h2>";
                        document.getElementById("after_question").style.display = 'block';
                        document.getElementById("continue_text").style.display = 'block';
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
                                ALMemory.raiseEvent("orientation/info", 0);
                        }});
                }}
        </script>

</body>
</html>"""
    
    def generate(self, quiz_num, quiz_data, total_questions):
        """Generate the main quiz question page with choices"""
        output_file = self.output_dir / f"quiz{quiz_num}.html"
        
        # Generate option buttons HTML
        option_buttons = ""
        for i, option in enumerate(quiz_data["options"]):
            button_class = "right-answer" if option == quiz_data["correct_answer"] else "wrong-answer"
            button_action = "right_clicked()" if option == quiz_data["correct_answer"] else "wrong_clicked()"
            
            # Use image if provided, otherwise use text
            if "option_images" in quiz_data and i < len(quiz_data["option_images"]):
                img_path = quiz_data["option_images"][i]
                # Make sure path is relative to site structure
                if not img_path.startswith("../../site/img/"):
                    # If the path uses "../images/" format, update it
                    if img_path.startswith("../images/"):
                        img_path = "../../site/img/" + img_path.replace("../images/", "")
                
                option_buttons += f"""
                                        <button type="submit" class="{button_class}" onmouseup="{button_action}">
                                            <img src="{img_path}" alt="{option}">
                                            <span class="button-text">{option}</span>
                                        </button>"""
            else:
                option_buttons += f"""
                                        <button type="submit" class="{button_class}" onmouseup="{button_action}">{option}</button>"""
        
        # Update button image paths for consistency
        next_button_image = quiz_data.get("next_button_image", "../../site/img/next_button.png")
        if next_button_image.startswith("../images/"):
            next_button_image = "../../site/img/" + next_button_image.replace("../images/", "")
            
        more_button_image = quiz_data.get("more_button_image", "../../site/img/info_button.png")
        if more_button_image.startswith("../images/"):
            more_button_image = "../../site/img/" + more_button_image.replace("../images/", "")
        
        # Create template data
        template_data = {
            "quiz_num": quiz_num,
            "body_class": quiz_data.get("body_class", "bg-secondary quiz"),
            "total_questions": total_questions,
            "question": quiz_data["question"],
            "title": quiz_data["title"],
            "subtitle": quiz_data.get("subtitle", ""),
            "option_buttons": option_buttons,
            "next_button_image": next_button_image,
            "more_button_image": more_button_image
        }
        
        # Get HTML header and apply template
        header = get_html_header(
            quiz_num, 
            quiz_data["question"],
            quiz_data.get("stylesheets", None)
        )
        
        body = self.apply_template(self.template, template_data)
        html = header + body
        
        # Write HTML to file
        self._write_to_file(output_file, html)

#!/usr/bin/env python3
"""
Pepper Robot Quiz Generator
HTML Utilities
"""

def get_html_header(quiz_num, title, stylesheets=None):
    """Generate the common HTML header"""
    
    if stylesheets is None:
        stylesheets = [
            "../site/css/bootstrap.min.css",
            "../site/css/style.css",
            "../site/web-fonts-with-css/css/fontawesome-all.min.css"
        ]
    
    stylesheets_html = ""
    for stylesheet in stylesheets:
        stylesheets_html += f'<link href="{stylesheet}" rel="stylesheet" type="text/css">\n'
    
    return f'''<!doctype html>
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fi" lang="fi">
        <head>
                        <meta charset="utf-8">
                        <title>TTY-Robot</title>
                        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                        <meta content='width=1280, user-scalable=0' name='viewport' />
                        <script src="/libs/qimessaging/1.0/qimessaging.js"></script>

                        <link href="https://fonts.googleapis.com/css?family=Abril+Fatface|Ubuntu" rel="stylesheet"> 

                <link rel="apple-touch-icon" sizes="57x57" href="<?= SITEPATH ?>img/ico/apple-icon-57x57.png">
                <link rel="apple-touch-icon" sizes="60x60" href="<?= SITEPATH ?>img/ico/apple-icon-60x60.png">
                <link rel="apple-touch-icon" sizes="72x72" href="<?= SITEPATH ?>img/ico/apple-icon-72x72.png">
                <link rel="apple-touch-icon" sizes="76x76" href="<?= SITEPATH ?>img/ico/apple-icon-76x76.png">
                <link rel="apple-touch-icon" sizes="114x114" href="<?= SITEPATH ?>img/ico/apple-icon-114x114.png">
                <link rel="apple-touch-icon" sizes="120x120" href="<?= SITEPATH ?>img/ico/apple-icon-120x120.png">
                <link rel="apple-touch-icon" sizes="144x144" href="<?= SITEPATH ?>img/ico/apple-icon-144x144.png">
                <link rel="apple-touch-icon" sizes="152x152" href="<?= SITEPATH ?>img/ico/apple-icon-152x152.png">
                <link rel="apple-touch-icon" sizes="180x180" href="<?= SITEPATH ?>img/ico/apple-icon-180x180.png">
                <link rel="icon" type="image/png" sizes="192x192"  href="<?= SITEPATH ?>img/ico/android-icon-192x192.png">
                <link rel="icon" type="image/png" sizes="32x32" href="<?= SITEPATH ?>img/ico/favicon-32x32.png">
                <link rel="icon" type="image/png" sizes="96x96" href="<?= SITEPATH ?>img/ico/favicon-96x96.png">
                <link rel="icon" type="image/png" sizes="16x16" href="<?= SITEPATH ?>img/ico/favicon-16x16.png">
                <link rel="manifest" href="<?= SITEPATH ?>img/ico/manifest.json">

        {stylesheets_html}
                <script src="../site/js/bootstrap.min.js"></script>
                <style>
                    .img-button {
                        background: none;
                        border: none;
                        padding: 0;
                    }
                    .img-button img {
                        max-width: 100%;
                        height: auto;
                    }
                    .button-text {
                        display: block;
                        margin-top: 10px;
                    }
                </style>
        </head>
'''

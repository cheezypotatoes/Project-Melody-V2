
class StyleSheet:

    @staticmethod
    def progress_bar():
        return """
            QProgressBar {
                border: 1px solid #1DB954;  /* Spotify green border */
                border-radius: 5px;
                background: #121212;  /* Dark background */
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: #1DB954;  /* Spotify green chunk color */
                border-radius: 5px;
            }
        """

    @staticmethod
    def control_button_style():
        return """
            QPushButton {
                background-color: #1DB954;  /* Spotify green background */
                color: white;
                border: 2px solid #121212;  /* Dark border */
                border-radius: 5px;
                
            }
            QPushButton:hover {
                background-color: #169c4e;  /* Slightly darker green on hover */
            }
        """

    @staticmethod
    def picker_style():
        return """
            QWidget { 
                background-color: #191414; 
                color: #FFFFFF; 
            }
            
            QPushButton { 
                background-color: #1DB954; 
                color: #FFFFFF; 
                border: none; 
            }
            
            QPushButton:hover { 
                background-color: #169c4e; 
            }
        """

    @staticmethod
    def warning_style():
        return """
            QWidget { 
                background-color: #191414; 
                color: #FFFFFF; 
            }
            
            QLabel { 
                color: #FFFFFF; 
            }
            
            QPushButton { 
                background-color: #1DB954; 
                color: #FFFFFF; 
                border: none; 
            }
            
            QPushButton:hover { 
                background-color: #169c4e; 
            }
        """

    @staticmethod
    def vertical_scrollbar_style():
        return """
               QScrollBar:vertical {
                   background: #191414;  /* Dark background */
                   width: 12px;  /* Adjust the width as needed */
               }
               QScrollBar::handle:vertical {
                   background: #1DB954;  /* Spotify green handle color */
                   border-radius: 6px;  /* Adjust the border radius as needed */
               }
               QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                   background: none;
               }
               QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                   background: none;
               }
           """

    @staticmethod
    def horizontal_scrollbar_style():
        return """
               QScrollBar:horizontal {
                   background: #191414;  /* Dark background */
                   height: 12px;  /* Adjust the height as needed */
               }
               QScrollBar::handle:horizontal {
                   background: #1DB954;  /* Spotify green handle color */
                   border-radius: 6px;  /* Adjust the border radius as needed */
               }
               QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                   background: none;
               }
               QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                   background: none;
               }
           """

    @staticmethod
    def vertical_horizontal_scrollbar_style():
        return """
            QScrollBar:vertical {
                background: #191414;  /* Dark background */
                width: 8px;  /* Adjust the width as needed */
            }
            QScrollBar::handle:vertical {
                background: #1DB954;  /* Spotify green handle color */
                border-radius: 6px;  /* Adjust the border radius as needed */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            QScrollBar:horizontal {
                background: #191414;  /* Dark background */
                height: 8px;  /* Adjust the height as needed */
            }
            QScrollBar::handle:horizontal {
                background: #1DB954;  /* Spotify green handle color */
                border-radius: 6px;  /* Adjust the border radius as needed */
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """

    @staticmethod
    def button_style():
        return f"""
            QPushButton {{
                background-color: rgb(29, 150, 70);  /* Darker green background */
                color: rgb(200, 200, 200);  /* Light gray text */
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: rgb(60, 120, 50);  /* Darker green on hover */
                color: rgb(255, 255, 255);  /* White text on hover */
            }}
            QPushButton:pressed {{
                background-color: rgb(40, 90, 30);  /* Even darker green when pressed */
            }}
        """

    @staticmethod
    def line_edit_style():
        return """
            QLineEdit {
                background-color: #282828; /* Spotify dark background color */
                color: #FFFFFF; /* Text color */
                border: 1px solid #1DB954; /* Spotify green border color */
                padding: 5px;
            }

            QLineEdit::focus {
                border: 2px solid #1DB954; /* Spotify green border color when focused */
            }
        """

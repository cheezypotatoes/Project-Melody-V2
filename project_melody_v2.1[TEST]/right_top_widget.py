# Third party library
from PyQt6.QtGui import QPalette, QColor, QPixmap, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QSizePolicy, QScrollArea, QLabel, QPushButton, QFrame

# Helper file
from general_helpers.file_handler_helpers import return_all_file


class RightTopWidget(QWidget):

    def __init__(self, music_player_class, right_bottom_widget, style_sheet_class):
        super().__init__()

        self.list_of_titles_and_images = None  # Initialize first to avoid warning
        self.none_sense = None  # Handle the slight warning (Doesn't do anything)

        self.style_sheet_class = style_sheet_class
        self.music_player_class = music_player_class  # Music player class
        self.right_bottom_widget = right_bottom_widget  # Right bottom widget to reach their stuff

        self.music_box_gridlayout = QGridLayout(self)  # Layout to put all song widget box
        self.music_box_gridlayout.setSpacing(10)  # Spacing

        self.iteration = 0

        self.init_ui()

    def init_ui(self):
        self.set_style()  # Set the style of the
        self.set_layout()

    def set_style(self):
        self.setFixedWidth(600)  # Main widget width
        self.setFixedHeight(800)  # Main widget height
        self.setAutoFillBackground(True)  # Autofill the whole cell

        wdg_pal = self.palette()  # Color
        wdg_pal.setColor(QPalette.ColorRole.Window, QColor(40, 40, 40))
        self.setPalette(wdg_pal)

        self.setContentsMargins(10, 10, 10, 10)  # Padding

    def set_layout(self):

        self.list_of_titles_and_images = return_all_file()

        # For every song create a new widget box for each
        for i, title_with_image in enumerate(self.list_of_titles_and_images):
            self.add_song_widget_box(title_with_image, self.music_box_gridlayout, i)

        self.reset_button_widget_box()

        self.add_scroll_bar(self.music_box_gridlayout)  # Add the scrollbar

    def reset_button_widget_box(self):
        iteration = self.iteration

        widget = QWidget()  # Widget that hold the widget_layout
        widget_layout = QVBoxLayout()  # Widget layout
        widget_layout.setContentsMargins(10, 10, 10, 10)  # Padding

        # Create a button
        button = QPushButton("RESET PLAYLIST")

        # Set width and height for the button
        button.setFixedWidth(180)
        button.setFixedHeight(180)

        # Connect to the method
        button.clicked.connect(self.reset_layout)

        # Add stylesheet
        button_style = self.style_sheet_class.button_style()
        button.setStyleSheet(button_style)

        # Add the button to the layout
        widget_layout.addWidget(button)

        # Set the layout for the widget
        widget.setLayout(widget_layout)

        self.music_box_gridlayout.addWidget(widget, iteration // 2, iteration % 2)

    def add_song_widget_box(self, title_with_image, grid_layout, i):
        widget = QWidget()  # Widget that hold the widget_layout
        widget_layout = QVBoxLayout()  # Widget layout
        widget_layout.setContentsMargins(10, 10, 10, 10)  # Padding

        image_label = self.create_image_label(title_with_image)  # Image for the widget box
        title_label = self.create_title_label(title_with_image)  # title for the widget box
        button_label = self.create_button_label(title_with_image)  # Button for the widget box

        # Add the labels to widget_layout then add it to the widget
        widget_layout.addWidget(image_label)
        widget_layout.addWidget(title_label)
        widget_layout.addWidget(button_label)
        widget.setLayout(widget_layout)

        widget.setFixedSize(200, 200)  # Set a fixed size for the widget

        grid_layout.addWidget(widget, i // 2, i % 2)  # The math on getting the next location of grid

        self.iteration = i + 1

    def create_button_label(self, title):
        self.none_sense = None  # None sense to remove the self. warning

        button = QPushButton(f"Play")  # Title
        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)  # Take whole space
        button.setFont(QFont("Synthwave", 12))  # Font and size

        # Style
        style = self.style_sheet_class.button_style()

        button.clicked.connect(lambda _: self.start_music(title))  # Call method that start the music

        button.setStyleSheet(style)  # Add style to button

        return button

    def create_title_label(self, title):
        self.none_sense = None  # None sense to remove the self. warning

        title_label = QLabel(title)  # Create a new label with the title inside it
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the title text within the title_label
        title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)  # Set size policy
        title_label.setFont(QFont("Synthwave", 10, QFont.Weight.Bold))  # Add the font
        title_label.setStyleSheet("color: #1DB954;")  # Spotify green color

        return title_label

    def create_image_label(self, song_name):
        self.none_sense = None  # None sense to remove the self. warning
        image_label = QLabel()  # Create new label to put the title
        image_path = rf'thumbnail\{song_name}.png'  # Format the song to png

        target_width = 150  # Adjust the desired width as needed
        target_height = 150  # Adjust the desired height as needed

        original_pixmap = QPixmap(image_path)  # Get the image
        scaled_pixmap = original_pixmap.scaled(target_width, target_height)  # Scale it to desirable size

        image_label.setPixmap(scaled_pixmap)  # Set the image to label
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image to the label

        return image_label

    def add_scroll_bar(self, grid_layout):
        # Create a scroll area and add some attributes to it
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(grid_layout)
        scroll_area.verticalScrollBar().setStyleSheet(self.style_sheet_class.vertical_scrollbar_style())
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        # Set a fixed size for the RightTopWidget
        self.setFixedWidth(600)
        self.setFixedHeight(800)

        # Add the scroll area to the RightTopWidget
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def start_music(self, title):
        self.music_player_class.start_music(title)  # Start the music by calling start_music from music player
        self.right_bottom_widget.timer.start(1000)  # Start the progress bar
        self.music_player_class.song_playing = title  # Set the text to the title

        # Reset the button
        self.right_bottom_widget.pause_button.setText("Pause")
        self.right_bottom_widget.music_player.music_is_running = True

    def reset_layout(self):
        # Remove all widgets from the layout
        for i in reversed(range(self.music_box_gridlayout.count())):
            widget = self.music_box_gridlayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
            self.music_box_gridlayout.takeAt(i)

        self.list_of_titles_and_images = return_all_file()  # GET THE LATEST LIST OF SONGS

        # For every song create a new widget box for each
        for i, title_with_image in enumerate(self.list_of_titles_and_images):
            self.add_song_widget_box(title_with_image, self.music_box_gridlayout, i)

        # TODO FIX THIS
        self.reset_button_widget_box()

        print("RESET SUCCESS")

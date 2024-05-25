from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QScrollArea, QLabel,  QPushButton, QGroupBox, QFrame,
                             QListWidget)

from general_helpers.playlist_grabber import get_playlist_amount, get_song_from_playlist


#  TODO: MAYBE A WAY TO REMOVE ALL PLAYLIST BOX AND ADD IT AGAIN TRY REMOVING THE WIDGET FROM LOOP THEN ADD AGAIN
class LeftTopWidget(QWidget):
    def __init__(self, musicplayer, right_bottom_widget, stylesheet_class):
        super().__init__()
        self.player = musicplayer  # Musicplayer class
        self.right_bottom_widget = right_bottom_widget  # Right bottom widget
        self.stylesheet_class = stylesheet_class

        # Initialize
        self.none_sense = None  # Avoid weak warnings (Doesn't do anything)
        self.title_widget = None
        self.button_widget = None
        self.group_layout = None
        self.playlist_amount = None

        self.playlist_list = []

        self.init_ui()  # Whole ui

    def init_ui(self):
        self.set_style()  # Set the style
        self.set_layout()  # Set the layout

    def set_style(self):
        self.setAutoFillBackground(True)  # Autofill the whole cell

        # Color
        wdg_pal = self.palette()
        wdg_pal.setColor(QPalette.ColorRole.Window, QColor(40, 40, 40))
        self.setStyleSheet("background-color: rgb(40, 40, 40);")
        self.setPalette(wdg_pal)

        self.setContentsMargins(10, 10, 10, 10)  # Padding

    def set_layout(self):
        # Set up the main layout
        main_layout = QVBoxLayout(self)

        scroll_bar = self.create_scroll_bar()  # Create the scroll bar

        # Create a QGroupBox with a grid layout
        group_box = QGroupBox("Playlists:")

        self.group_layout = self.create_group_box_layout(group_box)  # Layout for group box

        self.playlist_amount = get_playlist_amount()  # Get the amount of playlist

        self.create_group_box_for_i(self.playlist_amount, self.group_layout)  # For loop that create playlist box

        group_box.setLayout(self.group_layout)  # Set the layout of the QGroupBox

        scroll_bar.setWidget(group_box)  # Set the QGroupBox as the widget for the QScrollArea

        # Set the style for the vertical scrollbar
        scroll_bar.verticalScrollBar().setStyleSheet(self.stylesheet_class.vertical_scrollbar_style())

        # Set the style for the horizontal scrollbar
        scroll_bar.horizontalScrollBar().setStyleSheet(self.stylesheet_class.horizontal_scrollbar_style())

        main_layout.addWidget(scroll_bar)  # Add the QScrollArea to the main layout

        self.setLayout(main_layout)

    # TODO: ADD ONE BUTTON THAT MAKES PLAYLIST
    def create_group_box_for_i(self, playlist_amount, group_layout):
        # For every playlist make a playlist box with their songs in it
        for i, playlist_amount_value in enumerate(playlist_amount):
            list_of_songs = get_song_from_playlist(playlist_amount_value)  # Get the song of the specific playlist name

            # Create playlist box widget
            widget = self.create_widget_playlist_box(f'{playlist_amount_value}', [f'{j}' for j in list_of_songs])

            self.playlist_list.append(widget)  # Record song to a list

            group_layout.addWidget(widget, i // 2, i % 2)  # Add playlist box widget to the grid

    def create_group_box_layout(self, group_box):
        self.none_sense = None  # Avoid weak warnings (Doesn't do anything)

        group_layout = QGridLayout(group_box)  # Create layout for groupbox

        # Styling
        group_layout.setContentsMargins(10, 20, 10, 10)
        group_box.setStyleSheet("QGroupBox { border: 2px solid rgb(50, 50, 50); margin-top: 10px; color: white; }")

        return group_layout

    def create_scroll_bar(self):
        self.none_sense = None  # Avoid weak warnings (Doesn't do anything)

        # Create a QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.verticalScrollBar().setStyleSheet(self.stylesheet_class.vertical_scrollbar_style())

        # Remove the frame around the QScrollArea
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)

        return scroll_area

    def create_widget_playlist_box(self, title, names):  # Create a widget with a title and a list of names

        # Main widget to put the layout with
        playlist_box_widget = self.playlist_box_layout_widget()

        # Layout
        layout = QVBoxLayout(playlist_box_widget)
        layout.addSpacing(10)

        # Title widget
        self.title_widget = self.playlist_box_title(title)
        layout.addWidget(self.title_widget)

        # List widget for names
        names_list = QListWidget()
        names_list.addItems(names)
        names_list.setStyleSheet("color: white;")

        # Set scrollbar style for both vertical and horizontal
        scrollbar_style = self.stylesheet_class.vertical_horizontal_scrollbar_style()

        names_list.verticalScrollBar().setStyleSheet(scrollbar_style)
        names_list.horizontalScrollBar().setStyleSheet(scrollbar_style)
        layout.addWidget(names_list)

        # Button widget
        self.button_widget = self.playlist_box_button(title)
        layout.addWidget(self.button_widget)

        playlist_box_widget.setLayout(layout)
        return playlist_box_widget

    def playlist_box_title(self, title):
        self.none_sense = None  # Avoid weak warnings (Doesn't do anything)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the title

        font = title_label.font()
        font.setPointSize(12)  # Set the font size (adjust as needed)
        title_label.setStyleSheet("color: white; background-color: rgb(35, 35, 35);")
        title_label.setFont(font)

        # Set a minimum height for the title label
        title_label.setMinimumHeight(30)  # Adjust the minimum height as needed

        return title_label

    def playlist_box_button(self, title):
        self.none_sense = None  # Avoid weak warnings (Doesn't do anything)

        button = QPushButton("Play")
        button.setStyleSheet(self.stylesheet_class.button_style())

        button.clicked.connect(lambda _x: self.playlist_button_clicked(title))

        return button

    def playlist_box_layout_widget(self):
        self.none_sense = None  # Avoid weak warnings (Doesn't do anything)

        widget = QWidget()
        widget.setFixedSize(250, 200)  # Set the fixed size (adjust as needed)
        widget.setStyleSheet("background-color: rgb(35, 35, 35);")  # Set the background color for the widget

        return widget

    def playlist_button_clicked(self, title):
        self.player.play_playlist_step_1(title)  # Play the playlist

        # Reset the pause button text
        self.right_bottom_widget.pause_button.setText("Pause")
        self.right_bottom_widget.music_player.music_is_running = True

        self.right_bottom_widget.timer.start(1000)  # Start the update time for bottom right widget

    def remove_playlist_box(self):
        for widget in self.playlist_list:  # Remove the widget from its layout
            layout = widget.parent()
            if layout is not None:
                if isinstance(layout, QGridLayout):
                    position = layout.indexOf(widget)
                    if position != -1:
                        layout.removeItem(layout.itemAt(position))

            # Delete the widget
            widget.deleteLater()

        self.playlist_list = []  # Clear the playlist_list

        self.playlist_amount = get_playlist_amount()

        self.create_group_box_for_i(self.playlist_amount, self.group_layout)  # Create the playlist box again

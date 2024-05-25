# Base library
import sys

# Third party library
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout

# Main class widgets
from right_bottom_widget import RightBottomWidget
from right_top_widget import RightTopWidget
from left_top_widget import LeftTopWidget
from left_bottom_widget import LeftBottomWidget
from style_sheet_class import StyleSheet

# Helper class widget
from music_handler.m_t_directory_checker import check_for_directories
from music_handler.music_player import MusicPlayer  # Import the MusicPlayer class
from general_helpers.playlist_grabber import get_song_from_playlist
from general_helpers.file_handler_helpers import check_if_ini_exist


# TODO Loading Screen
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.right_bottom_widget = None  # Avoids weak warning
        self.left_top_widget = None

        self.music_player = MusicPlayer(get_song_from_playlist)
        self.set_style()  # Style
        self.init_ui()  # Widgets

    def set_style(self):
        self.setWindowTitle("Project Melody")  # Title
        self.setGeometry(100, 100, 800, 600)  # Window Size

        palette = QPalette()  # Color
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        self.setPalette(palette)

    def init_ui(self):
        # Now create instances of other widgets

        style_sheet_class = StyleSheet()

        self.right_bottom_widget = RightBottomWidget(self.music_player, style_sheet_class, None)
        self.left_top_widget = LeftTopWidget(self.music_player, self.right_bottom_widget, style_sheet_class)
        right_top_widget = RightTopWidget(self.music_player, self.right_bottom_widget, style_sheet_class)
        left_bottom_widget = LeftBottomWidget(self.music_player, self.left_top_widget, style_sheet_class)

        self.right_bottom_widget.left_top_widget = self.left_top_widget  # Add left top widget after initializing it

        main_layout = QGridLayout()
        main_layout.addWidget(self.left_top_widget, 0, 0, 1, 1)
        main_layout.addWidget(left_bottom_widget, 1, 0, 1, 1)
        main_layout.addWidget(right_top_widget, 0, 1, 1, 1)  # Right top widget
        main_layout.addWidget(self.right_bottom_widget, 1, 1, 1, 1)  # Right bottom widget with default height

        self.right_bottom_widget.setMaximumHeight(150)  # Set the maximum height (adjust the value as needed)
        left_bottom_widget.setMaximumHeight(150)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


def main():
    check_for_directories()  # Check if thumbnail and mp3 file existed
    check_if_ini_exist()  # Check if ini file exist
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

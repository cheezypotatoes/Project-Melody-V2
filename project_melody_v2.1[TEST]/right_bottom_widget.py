# Third party library
import pygame
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QProgressBar, QLabel, QMessageBox,\
    QInputDialog

# Helper
from general_helpers.playlist_grabber import get_playlist_amount
from general_helpers.playlist_inserter import insert_song


class RightBottomWidget(QWidget):

    def __init__(self, music_player, style_sheet_class, left_top_widget):
        super().__init__()

        # Timer for the update time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.style_sheet_class = style_sheet_class

        self.left_top_widget = left_top_widget

        self.music_player = music_player  # Music player class

        # Initializing some widgets to avoid weak error
        self.title_playing = None
        self.duration_label = None
        self.stop_button = None
        self.pause_button = None
        self.playlist_add = None
        self.progress_bar = None

        self.init_ui()  # Initialize the ui

    def init_ui(self):
        self.set_styles()
        self.set_layout()

    def set_styles(self):
        # Color
        self.setAutoFillBackground(True)
        wdg_pal = self.palette()
        wdg_pal.setColor(QPalette.ColorRole.Window, QColor(40, 40, 40))
        self.setPalette(wdg_pal)
        self.setContentsMargins(10, 10, 10, 10)
        self.setFixedWidth(600)

        # Title label
        self.title_playing = QLabel("Play Music To Start")
        self.title_playing.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_playing.setStyleSheet("font-size: 15px; color: #1DB954;")  # Spotify green color

        # Duration label
        self.duration_label = QLabel("Duration: 0:00 / 0:00")
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.duration_label.setStyleSheet("font-size: 20px; color: #1DB954;")  # Spotify green color

    def set_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title_playing)
        main_layout.addWidget(self.duration_label)
        main_layout.addWidget(self.create_progress_bar())
        main_layout.addLayout(self.create_control_layout())

    def create_progress_bar(self):
        progressbar_style_sheet = self.style_sheet_class.progress_bar()
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(560)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setStyleSheet(progressbar_style_sheet)
        return self.progress_bar

    def create_control_layout(self):
        control_layout = QHBoxLayout()
        button_style = self.style_sheet_class.control_button_style()

        self.stop_button = self.create_button("Stop", 183, button_style)
        self.pause_button = self.create_button("Pause", 183, button_style)
        self.playlist_add = self.create_button("Add To Playlist", 183, button_style)

        self.stop_button.clicked.connect(self.stop_music_class)
        self.pause_button.clicked.connect(self.pause_play_class)
        self.playlist_add.clicked.connect(self.playlist_picker_message_box)

        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.playlist_add)

        return control_layout

    @staticmethod
    def create_button(text, width, style):
        button = QPushButton(text)
        button.setFixedWidth(width)
        button.setStyleSheet(style)
        return button

    def stop_music_class(self):
        self.title_playing.setText("Play Music To Start")

        self.duration_label.setText("0:00 / 0:00")

        self.timer.stop()
        try:
            self.music_player.stop_music()
            # Reset the button
            self.pause_button.setText("Play")
            self.music_player.music_is_running = False
        except Exception as e:
            print(f"{e} Already stopped")

    def pause_play_class(self):
        if self.music_player.music_started:
            if self.music_player.music_is_running:
                self.music_player.pause_music()
                self.pause_button.setText("Play")
                self.music_player.music_is_running = False
            else:
                self.music_player.unpause_music()
                self.pause_button.setText("Pause")
                self.music_player.music_is_running = True

    def update_time(self):
        self.title_playing.setText(f"Now Playing : {self.music_player.song_playing}")

        current_time = pygame.mixer.music.get_pos() / 1000.0
        formatted_current_time = self.music_player.format_time(current_time)
        formatted_music_length = self.music_player.format_time(self.music_player.music_length)
        self.duration_label.setText(f"{formatted_current_time} / {formatted_music_length}")

        progress = int((current_time / self.music_player.music_length) * 100)
        self.progress_bar.setValue(progress)

        if progress == 100:
            self.music_player.music_is_running = False

    def playlist_picker_message_box(self):
        message_box = self.create_playlist_picker()
        message_box.exec()

    def create_playlist_picker(self):
        # Create a QMessageBox
        picker = QMessageBox()

        # Set dark purple theme for the main widget
        picker.setStyleSheet(self.style_sheet_class.picker_style())

        picker.setWindowTitle('Pick a playlist')
        picker.setText('Choose a playlist:')

        list_of_playlists = get_playlist_amount()

        if len(list_of_playlists) != 0:
            # Create a layout for the buttons
            button_layout = QVBoxLayout()

            for playlist in list_of_playlists:
                button = QPushButton(f'{playlist}')
                button.clicked.connect(lambda x, playlist_=playlist: self.add_song_to_playlist(playlist_))
                button_layout.addWidget(button)

            # Create a widget for the layout
            widget = QWidget()
            widget.setLayout(button_layout)

            # Set the layout of the QMessageBox to the widget
            picker.layout().addWidget(widget, 1, 0, 1, -1)
        else:
            picker.setText("NO PLAYLIST")  # TEMP

        # Make a new playlist
        make_playlist_button = QPushButton('Make playlist')
        make_playlist_button.setStyleSheet("background-color: #2C68FF; color: #FFFFFF; border: none;")
        make_playlist_button.clicked.connect(self.create_playlist_and_add_music)
        picker.addButton(make_playlist_button, QMessageBox.ButtonRole.ActionRole)

        # Add Cancel button
        cancel_button = QPushButton('Cancel')
        cancel_button.setStyleSheet("background-color: #FF5555; color: #FFFFFF; border: none;")
        cancel_button.clicked.connect(picker.reject)
        picker.addButton(cancel_button, QMessageBox.ButtonRole.RejectRole)

        return picker

    def create_playlist_and_add_music(self):
        # Create input dialog to make the playlist
        text, ok = QInputDialog.getText(self, 'Make Playlist', 'Playlist Name:')

        # Test if valid
        if ok and self.music_player.music_started is True and text.strip():
            self.add_song_to_playlist(playlist=text)  # Make the playlist and song
        elif not self.music_player.music_started:
            self.show_warning('Warning', 'Music Not Selected')
        elif not text.strip():
            self.show_warning('Warning', 'Invalid Name')

    def add_song_to_playlist(self, playlist):
        # Check if there's a song selected
        if not self.music_player.song_playing == "":
            insert_song(self.music_player.song_playing, playlist)
        else:
            self.show_warning('Warning', 'Music Not Selected')

        #  Part of the resetting the playlist boxes
        self.left_top_widget.remove_playlist_box()

    def show_warning(self, title, message):
        # Create a QMessageBox with Spotify-like styles
        warning_box = QMessageBox()
        warning_box.setStyleSheet(self.style_sheet_class.warning_style())
        warning_box.setIcon(QMessageBox.Icon.Warning)
        warning_box.setWindowTitle(title)
        warning_box.setText(message)
        warning_box.exec()

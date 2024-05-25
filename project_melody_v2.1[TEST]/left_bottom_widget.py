from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox)

import time
import os
from threading import Thread, Event

from music_handler.music_downloader import download


class LeftBottomWidget(QWidget):
    def __init__(self, musicplayer, right_bottom_widget, style_sheet_class):
        super().__init__()
        self.none_sense = None
        self.line_edit = None

        self.player = musicplayer  # Musicplayer class
        self.right_bottom_widget = right_bottom_widget  # Right bottom widget
        self.style_sheet_class = style_sheet_class

        self.download_button = self.download_button()

        self.timer = QTimer()
        self.timer.timeout.connect(self.download_music)

        # Use an event to signal the thread to stop
        self.stop_event = Event()

        self.download_stack = []

        self.current_directory = os.getcwd()

        self.mp3_directory = r"mp3"
        self.thumbnail_directory = r"thumbnail"

        # Create and start the thread
        self.thread = Thread(target=self.download_music_method, daemon=True)
        self.thread.start()

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
        self.setFixedWidth(655)

        self.setContentsMargins(10, 10, 10, 10)  # Padding

    def set_layout(self):
        # Set up the main layout
        main_layout = QVBoxLayout(self)

        self.line_edit = self.create_line_edit()

        self.download_button.clicked.connect(self.download_button_clicked)

        # Add the QLineEdit to the main layout
        main_layout.addWidget(self.line_edit)

        main_layout.addWidget(self.download_button)

        # Set the main layout for the widget
        self.setLayout(main_layout)

    def download_button(self):
        self.none_sense = None

        button_style = self.style_sheet_class.button_style()

        button = QPushButton("Download")
        button.setFixedHeight(50)
        button.setStyleSheet(button_style)
        return button

    def create_line_edit(self):
        # Create a QLineEdit
        line_edit = QLineEdit(self)

        # Set some properties for the QLineEdit
        line_edit.setPlaceholderText("Insert Link Here")

        # Apply a Spotify-inspired stylesheet
        stylesheet = self.style_sheet_class.line_edit_style()

        line_edit.setStyleSheet(stylesheet)

        return line_edit

    def download_button_clicked(self):
        link = self.line_edit.text()

        if link.startswith("https://www.youtube.com/watch?v="):
            self.download_stack.append(link)
            self.line_edit.clear()
            self.show_notification("Downloading", "Downloading Music Please Wait")
        else:
            self.show_warning("Invalid Link", "Link Is Invalid")
            self.line_edit.clear()

    def download_music_method(self):
        while not self.stop_event.is_set():
            # Check if the list is not empty
            if self.download_stack:

                self.download_music()  # Download the music using the download music method

                self.download_stack.pop(0)  # Pop the item from the list

            time.sleep(2)

    def download_music(self):
        link_for_yt = self.download_stack[-1]

        download(link_for_yt, self.thumbnail_directory, self.mp3_directory)

    def show_warning(self, title, message):
        self.none_sense = None
        # Create a QMessageBox with Spotify-like styles
        warning_box = QMessageBox()
        warning_box.setStyleSheet(self.style_sheet_class.warning_style())
        warning_box.setIcon(QMessageBox.Icon.Warning)
        warning_box.setWindowTitle(title)
        warning_box.setText(message)
        warning_box.exec()

    def show_notification(self, title, message):
        self.none_sense = None
        # Create a QMessageBox with Spotify-like styles
        warning_box = QMessageBox()
        warning_box.setStyleSheet(self.style_sheet_class.warning_style())
        warning_box.setIcon(QMessageBox.Icon.Information)
        warning_box.setWindowTitle(title)
        warning_box.setText(message)
        warning_box.exec()

# Third party libraries
import pygame
import mutagen.mp3
from PyQt6.QtCore import QTimer

# Built in libraries
import os


# TODO: CLEAN CODE THEN MAKE PLAYLIST ADD YOU HAVE 2 TITLE CHANGER
class MusicPlayer:
    def __init__(self, get_song_from_playlist):
        self.get_song_from_playlist = get_song_from_playlist

        self.music_is_running = False
        self.music_started = False
        self.music_length = None
        self.none_sense = None
        self.playlist_starting = False
        self.song_playing = ""

        pygame.mixer.init()

        self.current_playlist = []
        self.current_song_index = 0

        # Create QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_next_song)

    def stop_music(self):
        # Stop single music
        if self.music_is_running or self.music_started or self.playlist_starting:
            self.music_is_running = False
            self.music_started = False
            self.playlist_starting = False
            self.song_playing = ""

            pygame.mixer.music.stop()

    @staticmethod
    def pause_music():
        pygame.mixer_music.pause()

    @staticmethod
    def unpause_music():
        pygame.mixer_music.unpause()

    def start_music(self, title):
        if self.playlist_starting:
            self.stop_playlist()

        title = self.formatting_title(title)

        pygame.mixer.music.load(title)
        pygame.mixer.music.play()

        audio = mutagen.mp3.MP3(title)
        self.music_length = audio.info.length

        self.music_is_running = True
        self.music_started = True

    def formatting_title(self, title):
        self.none_sense = None

        title = title

        if not title.startswith("mp3/"):
            title = f"mp3/{title}"

        if not title.endswith(".mp3"):
            title += ".mp3"

        return title

    def add_to_playlist(self):
        pass

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"

    def play_playlist_step_1(self, playlist_title):
        # Get the songs from the title and make it a path
        song_grabbed = self.get_song_from_playlist(playlist_title)
        song_grabbed_with_path = ["mp3/" + file_name + ".mp3" for file_name in song_grabbed]

        self.stop_music()  # Stop the current music

        try:
            self.stop_playlist()  # If there's a playlist currently playing
        finally:
            self.set_playlist(song_grabbed_with_path)  # Set the new playlist and start it

    def set_playlist(self, playlist):
        # Set the playlist
        self.current_playlist = playlist
        self.current_song_index = 0

        # If playlist exist in list then start
        if playlist:
            self.play_song(playlist[0])  # Start song

    def play_song(self, song_path):
        # Initialize that the song is running
        self.playlist_starting = True
        self.music_is_running = True
        self.music_started = True

        # Play the song
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        # Get the length and put it as variable so that update method can
        audio = mutagen.mp3.MP3(song_path)
        self.music_length = audio.info.length

        # Set the song playing variable to the song currently playing
        self.song_playing = song_path.split("/")[-1]

        # Set the timer interval to the duration of the sound in milliseconds
        self.timer.start(int(self.music_length * 1000))

    def play_next_song(self):
        # Stop the timer
        self.timer.stop()

        # Move to the next song in the playlist
        self.current_song_index += 1

        # Check if there are more songs to play
        if self.current_song_index < len(self.current_playlist):
            # Play the next song
            print(f"Playing: {os.path.basename(self.current_playlist[self.current_song_index])}")

            self.play_song(self.current_playlist[self.current_song_index])

        else:
            # Stop the timer if there are no more songs
            self.timer.stop()

    # Stops the song but exclusive for playlist
    def stop_playlist(self):
        pygame.mixer.stop()
        self.timer.stop()

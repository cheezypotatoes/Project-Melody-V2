import configparser
import os


def create_ini_file():
    with open('list.ini', 'w', encoding='utf-8') as file:
        file.write("[List_of_playlist]")


def add_playlist_the_master_list(playlist_name):
    config = configparser.ConfigParser()

    # Read the existing INI file
    config.read('list.ini', encoding='utf-8')

    # If the playlist section doesn't exist, create it
    if not config.has_section(playlist_name):
        config.add_section(playlist_name)

    # Get all values from the 'List_of_playlist' section
    list_of_playlist_values = config.items('List_of_playlist')

    # Convert the result to a dictionary for easier access
    list_of_playlist_dict = dict(list_of_playlist_values)

    playlist_list = []

    # Put it all value in a list
    for key, value in list_of_playlist_dict.items():
        playlist_list.append(value)

    if playlist_name not in playlist_list:
        # If not in the list, append it
        playlist_list.append(playlist_name)

    # Remove all entries inside the 'List_of_playlist' section
    for key in config.options('List_of_playlist'):
        config.remove_option('List_of_playlist', key)

    # Add it all back to the 'List_of_playlist' section
    for index, playlist_name in enumerate(playlist_list):
        config.set("List_of_playlist", f"playlist_{index}", playlist_name)

    # Write the changes back to the INI file
    with open('list.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def add_song_to_playlist(new_song, playlist_name):
    # Creating a ConfigParser object
    config = configparser.ConfigParser()

    # Read the existing configuration from the INI file
    config.read('list.ini', encoding='utf-8')

    # Get all values from the 'List_of_playlist' section
    list_of_song = config.items(playlist_name)

    # Convert the result to a dictionary for easier access
    list_of_song_dict = dict(list_of_song)

    song_list = []

    # Put it all value in a list
    for key, value in list_of_song_dict.items():
        song_list.append(value)

    if new_song not in song_list:
        # If not in the list, append it
        song_list.append(new_song)

    for index, song_name in enumerate(song_list):
        config.set(playlist_name, f"song_{index}", song_name)

    # Write the changes back to the INI file
    with open('list.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def insert_song(new_song, playlist_name):

    # If file doesn't exist make one
    if not os.path.isfile('list.ini'):
        create_ini_file()

    # Add the new playlist to the master list
    add_playlist_the_master_list(playlist_name)

    add_song_to_playlist(new_song, playlist_name)



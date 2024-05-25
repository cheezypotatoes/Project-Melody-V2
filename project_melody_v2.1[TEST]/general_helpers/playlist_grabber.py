import configparser


def get_playlist_amount():
    config = configparser.ConfigParser()

    config.read('list.ini', encoding='utf-8')

    list_of_all_playlist_dic = dict(config.items('List_of_playlist'))

    list_of_all_playlist = []

    for key, value in list_of_all_playlist_dic.items():
        list_of_all_playlist.append(value)

    return list_of_all_playlist


def get_song_from_playlist(playlist):
    config = configparser.ConfigParser()

    config.read('list.ini', encoding='utf-8')

    list_of_all_song_dic = dict(config.items(playlist))

    list_of_all_song = []

    for key, value in list_of_all_song_dic.items():
        list_of_all_song.append(value)

    return list_of_all_song

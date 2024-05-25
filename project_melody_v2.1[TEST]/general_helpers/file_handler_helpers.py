import os


# Function to strip file extensions
def strip_extension(file):
    return os.path.splitext(file)[0]


def return_all_file():
    # Define the two directories you want to compare
    directory1 = r"thumbnail"
    directory2 = r"mp3"

    # Get the list of files in each directory (excluding the file extension)
    files1 = [strip_extension(file) for file in os.listdir(directory1)]
    files2 = [strip_extension(file) for file in os.listdir(directory2)]

    # Convert the lists of filenames to sets for easier comparison
    file_set1 = set(files1)
    file_set2 = set(files2)

    # Find the common filenames in both directories
    common_files = sorted(list(file_set1.intersection(file_set2)))



    return common_files


def check_if_ini_exist():
    if not os.path.isfile('list.ini'):
        with open('list.ini', 'w', encoding='utf-8') as file:
            file.write("[List_of_playlist]")

import os


def check_for_directories():
    # Get the directory of the script
    script_directory = os.path.dirname(__file__)

    # Define the directories in the same folder as the script
    directory1 = os.path.join(script_directory, "../thumbnail")
    directory2 = os.path.join(script_directory, "../mp3")

    # Create directories if they don't exist
    try:
        os.makedirs(directory1)
        print(f"Directory created: {directory1}")
    except FileExistsError:
        print(f"Directory already exists: {directory1}")

    try:
        os.makedirs(directory2)
        print(f"Directory created: {directory2}")
    except FileExistsError:
        print(f"Directory already exists: {directory2}")

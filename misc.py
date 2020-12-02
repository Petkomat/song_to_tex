import random
import os
import shutil
import re


def create_temp_folder(root_directory):
    """
    Creates a temporal folder with a random name in a given root directory.
    :param root_directory: root directory, do not use backslashes in it
    :return: The new of the just created folder.
    """
    folder = root_directory + "/" + str(random.random())[2:]
    while os.path.exists(folder):
        folder = root_directory + "/" + str(random.random())[2:]
    os.makedirs(folder)
    return folder


def remove_temp_folder(folder):
    """
    Removes the specified folder.
    :param folder: a/path/to/directory
    :return: folder
    """
    shutil.rmtree(folder)
    return folder


def nicify_path(path):
    nicer = re.sub("\\\\", "/", path)
    return re.sub("/+", "/", nicer)

import hashlib
import os
import shutil
import time
from datetime import datetime


def log_and_print(log_directory, message):
    """
    Prints message to console and to log file
    :param log_directory: directory where log file will be saved
    :param message: message to be printed
    :return: None
    """
    print(message)
    with open(f"{log_directory}/sync_log.txt", mode="a") as file:
        file.write(f"{message}\n")  # Write to file, append mode


def define_interval():
    """
    Takes synchronization interval as input from user
    :return: interval in seconds
    """
    while True:
        int_min = input("Please define the interval to synchronize the directories in minutes: ")
        if not int_min.isdigit() or int(int_min) == 0:
            print("The interval must be a whole number greater than 0.")
        else:
            break
    return int(int_min) * 60


def verify_directory(directory):
    """
    Checks if directory exists
    :param directory: absolute path to the directory
    :return: absolute path to the directory stripped of unwanted characters
    """
    directory = directory.strip(" \\/")                 # .replace("\\", "/") - not needed, both / and \ are OK
    while not os.path.exists(directory):
        directory = input(f"Directory does not exist. Please enter correct absolute path: \n")
    return directory


def define_directories():
    """
    Takes absolute paths to directories as input from user
    :return: source directory, destination directory, log directory
    """
    print("Please define absolute paths to source and destination directories and the directory to store the log file.")
    src_dir = verify_directory(input("Source (original) directory: \n"))
    dst_dir = verify_directory(input("Destination (replica) directory: \n"))
    log_dir = verify_directory(input("Log file directory: \n").strip(" \\/"))

    return src_dir, dst_dir, log_dir


def file_hash(full_path):
    """
    Generates SHA256 hash for selected file
    :param full_path: absolute path to selected file
    :return: SHA256 hash
    """
    with open(full_path, mode="rb") as file:
        file_content = file.read()
        sha256 = hashlib.sha256(file_content).hexdigest()
        return sha256


def synchronise_directories(source: str, destination: str, log_directory: str) -> None:
    """
    Synchronises contents of source directory and destination directory
    :param source: absolute path to source directory
    :param destination: absolute path do destination directory
    :param log_directory: absolute path do log directory
    :return: None
    """
    msg = f"{datetime.now()} Synchronization started"
    log_and_print(log_directory, msg)

    # Step 1: Synchronise files and directories (copy new and modified files from source directory)
    for root, dirs, files in os.walk(source):
        relative_path_to_subdir = os.path.relpath(root, source)
        dst_path_to_subdir = os.path.join(destination, relative_path_to_subdir)

        # Create new directory in destination
        if not os.path.exists(dst_path_to_subdir):
            os.makedirs(dst_path_to_subdir)

        # Copy files from source to destination if needed
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_path_to_subdir, file)
            if not os.path.exists(dst_file):                            # New file
                try:
                    shutil.copy2(src_file, dst_file)
                    msg = f"{datetime.now()} New file {file} copied from {source} to {destination}"
                    log_and_print(log_directory, msg)
                except OSError as e:
                    msg = f"{datetime.now()} ERROR: File {file} cannot be copied: {e.filename} - {e.strerror}."
                    log_and_print(log_directory, msg)
            else:
                if file_hash(src_file) == file_hash(dst_file):          # Existing file - no change
                    msg = f"{datetime.now()} Existing file {file} checked, no changes"
                    log_and_print(log_directory, msg)
                else:                                                   # Existing file - modified
                    try:
                        shutil.copy2(src_file, dst_file)
                        msg = f"{datetime.now()} Modified file {file} copied from {source} to {destination}"
                        log_and_print(log_directory, msg)
                    except OSError as e:
                        msg = f"{datetime.now()} ERROR: File {file} cannot be copied: {e.filename} - {e.strerror}."
                        log_and_print(log_directory, msg)

    # Step 2: Remove files and directories from destination directory which are no longer in source
    for root, dirs, files in os.walk(destination):
        relative_path_to_subdir = os.path.relpath(root, destination)
        src_path_to_subdir = os.path.join(source, relative_path_to_subdir)

        # Remove directories from destination
        for subdir in dirs:
            dst_dir = os.path.join(root, subdir)
            src_dir = os.path.join(src_path_to_subdir, subdir)
            if not os.path.exists(src_dir):
                try:
                    shutil.rmtree(dst_dir)
                    msg = f"{datetime.now()} Abandoned directory /{subdir} removed from {destination}"
                    log_and_print(log_directory, msg)
                except OSError as e:
                    msg = f"{datetime.now()} ERROR: Directory {subdir} cannot be removed: {e.filename} - {e.strerror}."
                    log_and_print(log_directory, msg)

        # Remove files from destination
        for file in files:
            dst_file = os.path.join(root, file)
            src_file = os.path.join(src_path_to_subdir, file)
            if not os.path.exists(src_file):
                try:
                    os.remove(dst_file)
                    msg = f"{datetime.now()} Abandoned file {file} removed from {destination}"
                    log_and_print(log_directory, msg)
                except OSError as e:
                    msg = f"{datetime.now()} ERROR: File {file} cannot be removed: {e.filename} - {e.strerror}."
                    log_and_print(log_directory, msg)

    msg = f"{datetime.now()} Synchronization finished\n"
    log_and_print(log_directory, msg)


if __name__ == "__main__":
    source_dir, destination_dir, logging_dir = define_directories()
    interval = define_interval()

    while True:
        synchronise_directories(source=source_dir, destination=destination_dir, log_directory=logging_dir)
        time.sleep(interval)

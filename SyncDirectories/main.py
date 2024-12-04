import hashlib
import os
import shutil
import time
from datetime import datetime


def log_and_print(log_directory, message):
    """
    Prints message to the console and to the log file
    :param log_directory: directory where the log file will be saved
    :param message: message to be printed
    :return: None
    """
    print(message)
    with open(f"{log_directory}/sync_log.txt", mode="a") as file:
        file.write(f"{message}\n")  # Write to file, append mode


def define_interval():
    """
    Takes synchronization interval as input from the user
    :return: interval in seconds
    """
    while True:
        int_min = input("Please define the directory synchronization interval in minutes: ")
        if not int_min.isdigit() or int(int_min) <= 0:
            print("The interval must be a whole number greater than 0.")
        else:
            break
    return int(int_min) * 60


def verify_directory(directory):
    """
    Checks if the directory exists
    :param directory: absolute path to the directory
    :return: absolute path to the directory stripped of unwanted characters
    """
    directory = directory.strip()
    while not os.path.exists(directory):
        directory = input(f"Directory does not exist. Please enter correct absolute path: \n").strip()
    return os.path.abspath(directory)


def define_directories():
    """
    Takes absolute paths to the directories as input from the user
    :return: source directory, destination directory, log directory
    """
    print("Please define absolute paths to source and destination directories and the directory to store the log file.")
    src_dir = verify_directory(input("Source (original) directory: \n"))
    dst_dir = verify_directory(input("Destination (replica) directory: \n"))
    log_dir = verify_directory(input("Log file directory: \n"))

    return src_dir, dst_dir, log_dir


def file_hash(full_path):
    """
    Generates a SHA256 hash for the selected file
    :param full_path: absolute path to the selected file
    :return: SHA256 hash
    """
    with open(full_path, mode="rb") as file:
        file_content = file.read()
        sha256 = hashlib.sha256(file_content).hexdigest()
        return sha256


def synchronise_directories(source: str, destination: str, log_directory: str) -> None:  # PyCharm warning: Unexpected
    """                                                                                  # type if type not defined
    Synchronizes the contents of the source and destination directories
    :param source: absolute path to the source directory
    :param destination: absolute path do the destination directory
    :param log_directory: absolute path do the log directory
    :return: None
    """
    msg = f"{datetime.now()} Synchronization started"
    log_and_print(log_directory, msg)

    # Step 1: Synchronise files and directories (copy new and modified files from the source directory)
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        dst_path = os.path.join(destination, relative_path)

        # Create new subdirectory in destination
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        # Copy new or modified files from the source directory to the destination directory
        for file in files:
            src_file = os.path.normpath(os.path.join(root, file))
            dst_file = os.path.normpath(os.path.join(dst_path, file))

            if not os.path.exists(dst_file):                            # New file
                try:
                    shutil.copy2(src_file, dst_file)
                    msg = f"{datetime.now()} New file {file} copied from {src_file} to {dst_file}"
                    log_and_print(log_directory, msg)
                except (shutil.Error, OSError) as e:
                    msg = f"{datetime.now()} ERROR: File {file} cannot be copied: {e.filename} - {e.strerror}"
                    log_and_print(log_directory, msg)
            else:
                if file_hash(src_file) == file_hash(dst_file):          # Existing file - no change
                    msg = f"{datetime.now()} Existing file {file} checked, no changes in {src_file}"
                    log_and_print(log_directory, msg)
                else:                                                   # Existing file - modified
                    try:
                        shutil.copy2(src_file, dst_file)
                        msg = f"{datetime.now()} Modified file {file} copied from {src_file} to {dst_file}"
                        log_and_print(log_directory, msg)
                    except (shutil.Error, OSError) as e:
                        msg = f"{datetime.now()} ERROR: File {file} cannot be copied: {e.filename} - {e.strerror}"
                        log_and_print(log_directory, msg)

    # Step 2: Delete files and directories from the destination directory which are no longer in the source directory
    for root, dirs, files in os.walk(destination):
        relative_path = os.path.relpath(root, destination)
        src_path = os.path.join(source, relative_path)

        # Remove directories from destination
        for subdir in dirs:
            dst_dir = os.path.normpath(os.path.join(root, subdir))
            src_dir = os.path.normpath(os.path.join(src_path, subdir))
            if not os.path.exists(src_dir):
                try:
                    shutil.rmtree(dst_dir)
                    msg = f"{datetime.now()} Abandoned directory /{subdir} removed from {dst_dir}"
                    log_and_print(log_directory, msg)
                except (shutil.Error, OSError) as e:
                    msg = f"{datetime.now()} ERROR: Directory {subdir} cannot be removed: {e.filename} - {e.strerror}"
                    log_and_print(log_directory, msg)

        # Remove files from destination
        for file in files:
            dst_file = os.path.normpath(os.path.join(root, file))
            src_file = os.path.normpath(os.path.join(src_path, file))
            if not os.path.exists(src_file):
                try:
                    os.remove(dst_file)
                    msg = f"{datetime.now()} Abandoned file {file} removed from {dst_file}"
                    log_and_print(log_directory, msg)
                except (shutil.Error, OSError) as e:
                    msg = f"{datetime.now()} ERROR: File {file} cannot be removed: {e.filename} - {e.strerror}"
                    log_and_print(log_directory, msg)

    msg = f"{datetime.now()} Synchronization finished\n"
    log_and_print(log_directory, msg)


if __name__ == "__main__":
    source_dir, destination_dir, logging_dir = define_directories()
    interval = define_interval()

    while True:
        synchronise_directories(source=source_dir, destination=destination_dir, log_directory=logging_dir)
        time.sleep(interval)

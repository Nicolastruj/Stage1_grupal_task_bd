import os
import shutil
import time

import schedule

from indexer.indexer_dict import indexer_dict


def job(books_directory, tray, words_directory, output_directory_metadata, stopwords_filepath):
    """
    Execute the job to process files from the specified books directory,
    copy them to a temporary tray, and index their contents.

    :param books_directory: The directory containing the book files to be processed.
    :param tray: The directory where files will be temporarily copied for processing.
    :param words_directory: The directory where the indexed words will be saved.
    :param stopwords_filepath: The directory containing the stopwords TXT file.
    :param output_directory_metadata: The directory containing the metadata JSON file.
    :return: None
    """
    files = get_latest_files(books_directory)

    if not files:
        print("No files found to process.")
        return

    copy_files_to_temp_directory(files, tray)
    print(f"Files copied to the temporary tray: {files}")

    indexer_dict(tray, words_directory, output_directory_metadata, stopwords_filepath)
    print("Indexing completed.")

    delete_temp_directory(tray)
    print(f"Temporary directory deleted: {tray}")


def delete_temp_directory(temp_directory):
    """
    Delete the specified temporary directory and all its contents.

    :param temp_directory: The path to the temporary directory to be deleted.
    :return: None
    """
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)
        print(f"Temporary directory deleted: {temp_directory}")
    else:
        print(f"The temporary directory does not exist: {temp_directory}")


def get_latest_files(source_directory, num_files=3):
    """
    Retrieve the most recently modified text files from a specified directory.

    :param source_directory: The directory to search for text files.
    :param num_files: The maximum number of recent files to return (default is 3).
    :return: A list of paths to the most recently modified text files.
    """
    print(f"Looking for the last {num_files} files in: {source_directory}")
    files = [f for f in os.listdir(source_directory) if f.endswith('.txt')]

    files_with_path = [os.path.join(source_directory, f) for f in files]
    files_with_path = [f for f in files_with_path if os.path.isfile(f)]

    # Sort files by modification date
    files_with_path.sort(key=os.path.getmtime, reverse=True)

    # Return the last 'num_files' files
    return files_with_path[:num_files]


def copy_files_to_temp_directory(latest_files, temp_directory):
    """
    Copy a list of files to a specified temporary directory.

    :param latest_files: A list of file paths to be copied.
    :param temp_directory: The temporary directory where the files will be copied.
    :return: None
    """
    print(f"Copying files to: {temp_directory}")
    os.makedirs(temp_directory, exist_ok=True)

    for file in latest_files:
        shutil.copy(file, temp_directory)
        print(f"File copied: {file}")


def execute_indexer(books_directory, tray, words_directory, output_directory_metadata, stopwords_filepath):
    """
    Execute the indexing process immediately and set up a scheduler for subsequent runs.


    :param books_directory: The directory containing the book files to be indexed.
    :param tray: The directory where files will be temporarily copied for processing.
    :param words_directory: The directory where the indexed words will be saved.
    :param stopwords_filepath: The directory containing the stopwords TXT file.
    :param output_directory_metadata: The directory containing the metadata JSON file.
    :return: None
    """
    # Run the job immediately
    print("Running the initial task immediately...")
    job(books_directory, tray, words_directory, output_directory_metadata, stopwords_filepath)

    # Set up the scheduler for later runs
    setup_schedule(books_directory, tray, words_directory)
    print("Scheduler set. Waiting for scheduled executions...")

    while True:
        schedule.run_pending()   # Run scheduled tasks
        time.sleep(1)


def setup_schedule(books_directory, tray, words_directory):
    """
    Set up a schedule to run the indexing job every 5 minutes.

    :param books_directory: The directory containing the book files to be indexed.
    :param tray: The directory where files will be temporarily copied for processing.
    :param words_directory: The directory where the indexed words will be saved.
    :return: None
    """
    print("Setting up the schedule for the scheduled task.")
    schedule.every(5).minutes.do(lambda: job(books_directory, tray, words_directory))
    print("Task scheduled every 5 minutes.")

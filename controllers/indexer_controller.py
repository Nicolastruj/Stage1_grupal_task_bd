import os
import shutil
import time

import schedule

from indexer.indexer_dict import indexer_dict


def job(books_directory, tray, words_directory):
    print(f"Running the job with the directories:\n"
          f"Books: {books_directory}\n"
          f"Tray: {tray}\n"
          f"Words: {words_directory}")
    time.sleep(20)
    files = get_latest_files(books_directory)
    print(f"Files found: {files}")

    if not files:
        print("No files found to process.")
        return

    copy_files_to_temp_directory(files, tray)
    print(f"Files copied to the temporary tray: {files}")

    indexer_dict(tray, words_directory)
    print("Indexing completed.")

    delete_temp_directory(tray)
    print(f"Temporary directory deleted: {tray}")


def delete_temp_directory(temp_directory):
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)
        print(f"Temporary directory deleted: {temp_directory}")
    else:
        print(f"The temporary directory does not exist: {temp_directory}")


def get_latest_files(source_directory, num_files=3):
    print(f"Looking for the last {num_files} files in: {source_directory}")
    files = [f for f in os.listdir(source_directory) if f.endswith('.txt')]

    files_with_path = [os.path.join(source_directory, f) for f in files]
    files_with_path = [f for f in files_with_path if os.path.isfile(f)]

    # Sort files by modification date
    files_with_path.sort(key=os.path.getmtime, reverse=True)

    # Return the last 'num_files' files
    return files_with_path[:num_files]


def copy_files_to_temp_directory(latest_files, temp_directory):
    print(f"Copying files to: {temp_directory}")
    os.makedirs(temp_directory, exist_ok=True)

    for file in latest_files:
        shutil.copy(file, temp_directory)
        print(f"File copied: {file}")


def execute_indexer(books_directory, tray, words_directory):
    # Run the job immediately
    print("Running the initial task immediately...")
    job(books_directory, tray, words_directory)

    # Set up the scheduler for later runs
    setup_schedule(books_directory, tray, words_directory)
    print("Scheduler set. Waiting for scheduled executions...")

    while True:
        schedule.run_pending()   # Run scheduled tasks
        time.sleep(1)


def setup_schedule(books_directory, tray, words_directory):
    print("Setting up the schedule for the scheduled task.")
    schedule.every(5).minutes.do(lambda: job(books_directory, tray, words_directory))
    print("Task scheduled every 5 minutes.")

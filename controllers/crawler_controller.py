import os
import time

from crawler import crawler


def obtain_last_id(datamart_path):
    """
    Obtain the most recently added numerical ID from TXT files in the specified directory.

    :param datamart_path: The path to the directory containing the TXT files.
    :return: The most recently added ID found in the file names, or 0 if no valid IDs are found.
    """
    files = os.listdir(datamart_path)
    ids = []

    for file in files:
        if file.endswith(".txt"):
            try:
                id_str = file.split('_')[-1].replace('.txt', '')
                ids.append(int(id_str))
            except ValueError:
                continue

    if ids:
        return max(ids)
    else:
        return 0


def downloading_process(datamart_path):
    """
    Downloads three books sequentially from Gutenberg starting from the next available ID.

    This function checks the specified datamart path to find the last downloaded book ID,
    then attempts to download the next three books based on that ID.

    :param datamart_path: The directory where the downloaded books will be saved.
    :return: None
    """
    last_id = obtain_last_id(datamart_path)

    successful_downloads = 0

    while successful_downloads < 3:
        next_id = last_id + 1
        last_id += 1

        status = crawler.download_book(next_id, datamart_path)

        if status == 200:
            successful_downloads += 1

    print("Three books downloaded successfully.")


def periodic_task(interval, datamart_path):
    """
    Executes the downloading process at a specified interval.

    This function repeatedly calls the downloading_process function to download
    books from Gutenberg every `interval` seconds.

    :param interval: The time interval (in seconds) to wait between downloads.
    :param datamart_path: The path to the directory where the downloaded books will be stored.
    :return: None
    """
    while True:
        downloading_process(datamart_path)
        print(f"Wait {interval} seconds")
        time.sleep(interval)

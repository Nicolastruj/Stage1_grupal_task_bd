import time
import os
from crawler import crawler


def obtain_last_id(datamart_path):
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
    while True:
        downloading_process(datamart_path)
        print(f"Wait {interval} seconds")
        time.sleep(interval)

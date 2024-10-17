# def main():
# interval = 20  # Crawler interval in seconds
# path = "./Datamart_libros"
from controllers.indexer_controller import execute_indexer

# # Start the crawler periodic task
# crawler_controller.periodic_task(interval, path)

# while True:
#     time.sleep(1)
# Run the indexer after the crawler has completed

execute_indexer(r'./Datamart_books',
                r'./Books_Datamart/books_tray',
                r'Words_Datamart',
                "./metadata_datamart",
                "./indexer/stopwords.txt")



# Execute the search engine controller
# search_engine_controller()

# Keep the script alive, for any future scheduling


# if __name__ == "__main__":
#     main()

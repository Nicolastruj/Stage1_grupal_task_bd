
from controllers.indexer_controller import execute_indexer


def main():
    """execute_crawl(300, r'./Books_Datamart')"""
    execute_indexer(r'./Books_Datamart', r'./Books_Datamart/Books_Tray', r'./Words_Datamart')


if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     main()

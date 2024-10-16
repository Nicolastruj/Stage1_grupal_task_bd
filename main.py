from data_model.object_type.Word import Word
from indexer_objt.indexer import indexer5_parallel, indexer5


def main():
    indexer5_parallel(r"Datamart_Books",
            r"Datamart_Words")

if __name__ == "__main__":
    main()
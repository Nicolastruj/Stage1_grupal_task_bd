from data_model.object_type.Palabra import Palabra
from indexer.indexer import indexer, indexer2, indexer3, indexer4, indexer5, indexer5_parallel


def main():
    indexer5_parallel(r"Datamart_libros",
            r"Datamart_palabras")

if __name__ == "__main__":
    main()
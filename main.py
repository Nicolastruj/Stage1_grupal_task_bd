from data_model.object_type.Palabra import Palabra
from indexer_objt.indexer import indexer5_parallel, indexer5


def main():
    indexer5_parallel(r"Datamart_libros",
            r"Datamart_palabras")

if __name__ == "__main__":
    main()
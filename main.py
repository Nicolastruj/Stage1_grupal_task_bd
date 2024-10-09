from data_model.object_type.Palabra import Palabra
from indexer_object.indexer import indexer, indexer2


def main():
    indexer2(r"Datamart_libros",
            r"Datamart_palabras")

if __name__ == "__main__":
    main()
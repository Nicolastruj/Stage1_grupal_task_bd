from indexer_dict.indexer_dict import indexer_dict
from indexer_controller.indexer_controller import execute_indexer
from indexer_objt.indexer import indexer


def main():
    execute_indexer(r'./Datamart_libros', r'./Datamart_libros/bandeja_libros', r'Datamart_palabras')
    """indexer_dict(r'./Datamart_libros/bandeja_libros', r'Datamart_palabras')"""

if __name__ == "__main__":
    main()
from data_model.object_type.Palabra import Palabra
from indexer.indexer import indexer, indexer2


def main():
    indexer2(r"C:\Users\carlo\PycharmProjects\Stage1_individual_task_bd\Datamart_libros",
            r"C:\Users\carlo\PycharmProjects\Stage1_individual_task_bd\Datamart_palabras")

if __name__ == "__main__":
    main()
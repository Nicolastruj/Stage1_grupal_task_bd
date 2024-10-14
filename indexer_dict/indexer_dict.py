from reader.book_reader import read_words
from reader.path_reader import extract_files_from_directory
import re


def add_words_to_dict(words, id_book, dictionary):
    """Add words and its indexes in a dictionary."""
    for idx, word in enumerate(words):
        if word not in dictionary:
            dictionary[word] = {id_book: [idx]}
        else:
            if id_book not in dictionary:
                dictionary[word][id_book] = [idx]
            else:
                if id_book in dictionary[word]:
                    dictionary[word][id_book].append(idx)
    return dictionary


def id_search(filepath):
    pattern = r'\d+'
    coindidencies = re.findall(pattern, filepath)

    if coindidencies:
        result = coindidencies[0]
    else:
        result = ''
    return result


def main():
    indexer = {}
    directory_path = '../Datamart_libros'
    filepaths = extract_files_from_directory(directory_path)
    for filepath in filepaths:
        words = read_words(filepath)
        indexer = add_words_to_dict(words, id_search(str(filepath)), indexer)
    print(indexer)


if __name__ == "__main__":
    main()

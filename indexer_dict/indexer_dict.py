import os
import json
import re
from reader.book_reader import read_words
from reader.path_reader import extract_files_from_directory


def add_words_to_dict(words, id_book, dictionary):
    """Add words and their indexes in a dictionary."""
    for idx, word in enumerate(words):
        if word not in dictionary:
            dictionary[word] = {id_book: [idx]}
        else:
            if id_book not in dictionary[word]:
                dictionary[word][id_book] = [idx]
            else:
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


def save_partial_indexers(indexer, output_directory):
    """Divide the indexer into smaller parts and save them as separate JSON files."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    partial_indexers = {}

    for word, data in indexer.items():
        first_letter = word[0].lower()
        if first_letter not in partial_indexers:
            partial_indexers[first_letter] = {}
        partial_indexers[first_letter][word] = data

    for letter, partial_indexer in partial_indexers.items():
        output_file = os.path.join(output_directory, f'indexer_{letter}.json')
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(partial_indexer, file, ensure_ascii=False, indent=4)
        print(f"Partial indexer for '{letter}' saved to {output_file}")


def main():
    indexer = {}
    directory_path = '../Datamart_libros'
    output_directory = '../books_datamart_dict'
    filepaths = extract_files_from_directory(directory_path)

    for filepath in filepaths:
        words = read_words(filepath)
        indexer = add_words_to_dict(words, id_search(str(filepath)), indexer)

    save_partial_indexers(indexer, output_directory)


if __name__ == "__main__":
    main()

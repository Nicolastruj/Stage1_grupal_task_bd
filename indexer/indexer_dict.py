import json
import os
import re

from indexer.book_reader import read_words, save_metadata_to_json
from indexer.path_reader import extract_files_from_directory


def add_words_to_dict(words, id_book, dictionary):
    """
    Add words and their indexes to a dictionary.

    :param words: A list of words to be added.
    :param id_book: The ID of the book from which the words are extracted.
    :param dictionary: The dictionary where words and their indexes will be stored.
    :return: The updated dictionary with words and their corresponding indexes.
    """
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
    """
    Extract the first numeric ID from the given file path.

    :param filepath: The path of the file from which to extract the ID.
    :return: The first numeric ID found in the file path, or an empty string if no ID is found.
    """
    pattern = r'\d+'
    coindidencies = re.findall(pattern, filepath)

    if coindidencies:
        result = coindidencies[0]
    else:
        result = ''
    return result


def save_partial_indexers(indexer, output_directory):
    """
    Divide the indexer into smaller parts and save them as separate JSON files.

    :param indexer: A dictionary containing the indexer data to be divided.
    :param output_directory: The directory where the partial indexer files will be saved.
    :return: None
    """
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


def indexer_dict(books_datamart, words_datamart, output_directory_metadata, stopwords_filepath):
    """
    Create an indexer from book files, filtering out stopwords, and save metadata and partial indexers.

    :param books_datamart: The path to the directory containing the book files.
    :param words_datamart: The output directory for saving partial indexers.
    :param stopwords_filepath: The directory containing the stopwords TXT file.
    :param output_directory_metadata: The directory containing the metadata JSON file.
    :return: None
    """
    indexer = {}
    directory_path = books_datamart
    output_directory = words_datamart
    filepaths = extract_files_from_directory(directory_path)

    for filepath in filepaths:
        try:
            words = read_words(filepath, stopwords_filepath)
            if words:
                indexer = add_words_to_dict(words, id_search(str(filepath)), indexer)
            else:
                print(f"Warning: No words found in {filepath}")

            save_metadata_to_json(str(filepath), output_directory_metadata)

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    save_partial_indexers(indexer, output_directory)

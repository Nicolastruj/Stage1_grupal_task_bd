import json
import os
import re

from indexer.book_reader import read_words, save_metadata_to_json
from indexer.path_reader import extract_files_from_directory


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


def indexer_dict(books_datamart, words_datamart):
    indexer = {}
    directory_path = books_datamart  # Path to the directory containing the book files
    output_directory = words_datamart  # Output directory for the partial indexers
    output_directory_metadata = "./metadata_datamart"
    stopwords_filepath = "./stopwords.txt"
    filepaths = extract_files_from_directory(directory_path)  # Get all file paths

    for filepath in filepaths:
        try:
            words = read_words(filepath, stopwords_filepath)  # Read words from the book file
            if words:
                indexer = add_words_to_dict(words, id_search(str(filepath)), indexer)
            else:
                print(f"Warning: No words found in {filepath}")

            save_metadata_to_json(str(filepath), output_directory_metadata)  # Save book metadata

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    save_partial_indexers(indexer, output_directory)  # Save the partial indexers

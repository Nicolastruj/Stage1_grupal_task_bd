import os
import json

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_model.object_type.Palabra import Palabra


def load_indexes(index_folder):
    """Load all index files into a single dictionary."""
    indexer = {}

    # Load all JSON index files from the directory
    for filename in os.listdir(index_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(index_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                partial_index = json.load(file)
                # Merge the partial index into the main indexer
                indexer.update(partial_index)
    
    return indexer

def search_word(word, indexer):
    """Search for a word in the index and return the book IDs and positions."""
    word = word.lower()  # Convert the word to lowercase to match the index
    if word in indexer:
        return indexer[word]
    else:
        return None  # Return None if the word is not found

def display_search_results(results):
    """Display the search results in a readable format."""
    if not results:
        print("No results found.")
    else:
        for book_id, positions in results.items():
            print(f"Book ID: {book_id}")
            print(f"Occurrences at positions: {positions}\n")

def main():
    # Path to the folder where index files are stored
    index_folder = '../books_datamart_dict'

    # Load the index data
    indexer = load_indexes(index_folder)

    # Input word to search
    input_word = input("Enter a word to search for: ").strip()

    # Search for the word
    search_results = search_word(input_word, indexer)

    # Display the results
    display_search_results(search_results)

if __name__ == "__main__":
    main()
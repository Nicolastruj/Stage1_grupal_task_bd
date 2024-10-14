import os
import json

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_model.object_type.Palabra import Palabra


def load_palabras(index_folder):
    """Load all Palabra objects from the JSON index files."""
    palabras = {}

    # Load all JSON index files from the directory
    for filepath in glob.glob(f"{index_folder}/*.json"):
        with open(filepath, "r", encoding='utf-8') as file:
            data = json.load(file)
            palabra_obj = Palabra.from_dict(data)  # Convert JSON to Palabra object
            palabras[palabra_obj.id_nombre.lower()] = palabra_obj  # Use lowercase id_nombre for case-insensitive search

    return palabras

def search_word(word, palabras):
    """Search for a word in the Palabra objects and return book IDs and positions."""
    word = word.lower()  # Ensure case-insensitive search
    if word in palabras:
        palabra_obj = palabras[word]
        return palabra_obj.obtener_diccionario()  # Return the dictionary of book IDs and positions
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
    index_folder = '../Datamart_palabras'

    # Load the Palabra objects
    palabras = load_palabras(index_folder)

    # Input word to search
    input_word = input("Enter a word to search for: ").strip()

    # Search for the word
    search_results = search_word(input_word, palabras)

    # Display the results
    display_search_results(search_results)

if __name__ == "__main__":
    main()
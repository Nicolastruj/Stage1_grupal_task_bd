import json
import os
import re

from reader.stopwords_reader import load_stopwords_from_file


def read_words(filepath, stopwords_filepath):
    """Extract words from a TXT file and return a list of words."""

    words = []
    encodings = ['utf-8', 'utf-8-sig', 'windows-1252', 'latin1']

    stopwords = load_stopwords_from_file(stopwords_filepath)

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                content = file.read()
                words = re.findall(r"\b[a-zA-Z0-9]+(?:[-'/.][a-zA-Z0-9]+)*\b", content.lower())
                filtered_words = [word for word in words if word not in stopwords]
                return filtered_words
        except UnicodeDecodeError:
            print(f"Error decoding with {encoding}, trying next...")
            continue
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            return words
        except Exception as e:
            print(f"Error: {e}")
            return words

    print("Error: Could not decode the file with any of the attempted encodings.")
    return words


def read_metadata(filepath):
    """
    Extract book's name, author, book's id, and URL.

    :param filepath: Book's path.
    :return: a dictionary with book's name, author, book's id, and URL.
    """

    base_name = os.path.basename(filepath)

    match = re.match(r'^(.+?) by (.+?)_(\d+)\.txt$', base_name)
    if not match:
        return None  # Invalid file

    book_name = match.group(1)
    author = match.group(2)
    id_book = match.group(3)
    url = f'https://www.gutenberg.org/ebooks/{id_book}'
    return {"book_name": book_name, "author": author, "id_book": id_book, "URL": url}


def save_metadata_to_json(filepath, output_directory):
    """
    Read the metadata of a book and save it to a JSON file.
    The filename is based on the hundreds range of the book's id.

    :param filepath: Path to the book file.
    :param output_directory: Directory to save the JSON file.
    """
    # Read metadata from the book
    metadata = read_metadata(filepath)
    if not metadata:
        print(f"File '{filepath}' is invalid.")
        return

    # Create output directory if it does not exist
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Get the book's id and determine its hundred range
    id_book = metadata['id_book']
    hundred_range = (int(id_book) // 100) * 100  # Calculate the lower bound of the hundreds range
    json_filename = f"books_metadata_{hundred_range}-{hundred_range + 99}.json"
    json_filepath = os.path.join(output_directory, json_filename)  # Combine directory and filename

    # If the JSON file already exists, load it; otherwise, create an empty list
    if os.path.exists(json_filepath):
        with open(json_filepath, 'r', encoding='utf-8') as json_file:  # Ensure UTF-8 encoding
            books_data = json.load(json_file)
    else:
        books_data = []

    # Check if the book is already in the JSON data
    if any(book['id_book'] == id_book for book in books_data):
        print(f"Metadata for '{metadata['book_name']}' already exists. Skipping save.")
        return

    # Add new metadata to the existing JSON data
    books_data.append(metadata)

    # Save the updated list back to the JSON file
    with open(json_filepath, 'w', encoding='utf-8') as json_file:  # Ensure UTF-8 encoding
        json.dump(books_data, json_file, ensure_ascii=False, indent=4)

    print(f"Metadata for '{metadata['book_name']}' saved to '{json_filepath}'.")
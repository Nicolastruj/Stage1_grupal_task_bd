import json
import glob
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from data_model.object_type.Palabra import Palabra  # Ensure this import path is correct

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

def load_book_metadata(book_folder):
    """Load metadata of books (title, author, etc.) from book files."""
    books_metadata = {}

    # Assuming book files have the format "title_author_id.txt"
    for filepath in glob.glob(f"{book_folder}/*.txt"):
        filename = os.path.basename(filepath)
        parts = filename.split('_')
        if len(parts) >= 3:
            title = parts[0]
            author = parts[1]
            book_id = parts[2].split('.')[0]  # Extract the ID before ".txt"
            books_metadata[book_id] = {
                'title': title,
                'author': author,
                'url': filepath
            }

    return books_metadata

def get_paragraphs_from_book(book_file, positions):
    """Return the paragraphs that contain the word at the given positions."""
    with open(book_file, 'r', encoding='utf-8') as file:
        text = file.read()

    metadata = extract_metadata(text)

    print(metadata["title"])
    print(metadata["author"])
    print(metadata["language"])
    
    # Split text into paragraphs
    paragraphs = text.split('\n\n')

    for position in positions:
        print(paragraphs[position]) #f"Paragraph: 

    # Find paragraphs with the word at specified positions
    relevant_paragraphs = []
    # for pos in positions:
    #     for paragraph in paragraphs:
    #         if str(pos) in paragraph:  # You can adjust the condition if needed (e.g., exact matching logic)
    #             relevant_paragraphs.append(paragraph.strip())
    #             break

    return relevant_paragraphs

def display_search_results(results, books_metadata):
    """Display the search results with book metadata and paragraphs."""
    if not results:
        print("No results found.")
    else:
        for book_id, positions in results.items():
            if book_id in books_metadata:
                metadata = books_metadata[book_id]
                print(f"Book Title: {metadata['title']}")
                print(f"Author: {metadata['author']}")
                print(f"URL: {metadata['url']}")
                print(f"Occurrences at positions: {positions}")
                
                # Print the paragraphs with the occurrences
                paragraphs = get_paragraphs_from_book(metadata['url'], positions)
                for paragraph in paragraphs:
                    print(f"Paragraph: {paragraph}\n")
            else:
                print(f"Metadata for Book ID {book_id} not found.")

def extract_metadata(text):
    """Extract Title, Author, and Language from the book text."""
    title = re.search(r"^Title:\s*(.+)$", text, re.MULTILINE)
    author = re.search(r"^Author:\s*(.+)$", text, re.MULTILINE)
    language = re.search(r"^Language:\s*(.+)$", text, re.MULTILINE)

    return {
        "title": title.group(1).strip() if title else "Unknown",
        "author": author.group(1).strip() if author else "Unknown",
        "language": language.group(1).strip() if language else "Unknown"
    }


def main():
    # Path to the folder where index files are stored
    index_folder = '../Datamart_palabras'
    book_folder = '../Datamart_libros'

    # Load the Palabra objects
    palabras = load_palabras(index_folder)

    # Load book metadata (title, author, URL)
    books_metadata = load_book_metadata(book_folder)

    # Input word to search
    input_word = input("Enter a word to search for: ").strip()

    # Search for the word
    search_results = search_word(input_word, palabras)

    # Display the results
    display_search_results(search_results, books_metadata)

if __name__ == "__main__":
    main()
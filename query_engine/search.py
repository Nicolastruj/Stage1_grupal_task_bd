import json
import os
import re


def load_json_index(word, index_folder):
    """
    Loads the JSON file for the word's index based on its first letter.

    :param word: The word whose index is to be loaded.
    :param index_folder: The directory containing the index JSON files.
    :return: A dictionary with the index data, or an empty dictionary if the file is not found.
    """
    first_letter = word[0].lower()
    json_path = os.path.join(index_folder, f'indexer_{first_letter}.json')

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        print(f"Index file for letter '{first_letter}' not found.")
        return {}


def load_metadata(book_id, metadata_folder):
    """
    Loads the metadata of a book based on its book ID.

    :param book_id: The ID of the book whose metadata is to be loaded.
    :param metadata_folder: The directory containing the metadata JSON files.
    :return: A dictionary with the book's metadata, or None if not found.
    """
    # Calculate the range of the book's id to find the corresponding metadata file
    hundred_range = (int(book_id) // 100) * 100
    json_filename = f"books_metadata_{hundred_range}-{hundred_range + 99}.json"
    json_filepath = os.path.join(metadata_folder, json_filename)

    if os.path.exists(json_filepath):
        with open(json_filepath, 'r', encoding='utf-8') as file:
            books_data = json.load(file)
            # Find the book metadata by id
            for book in books_data:
                if book['id_book'] == book_id:
                    return book
    return None


def extract_paragraphs(book_filename, occurrences_dict, search_words):
    """
    Extract paragraphs from the book based on occurrences dictionary and search words.

    :param book_filename: The path to the book file from which to extract paragraphs.
    :param occurrences_dict: A dictionary containing occurrences data (not used in this version).
    :param search_words: A list of words to search for in the book paragraphs.
    :return: A list of relevant paragraphs containing the search words.
    """
    try:
        with open(book_filename, "r", encoding="utf-8") as file:
            text = file.read()

        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        relevant_paragraphs = []
        occurrences = 0
        word_patterns = {word: re.compile(rf"\b{word}\b", re.IGNORECASE) for word in
                         search_words}  # Compile patterns for search words

        for paragraph in paragraphs:
            # Check for occurrences of any search word in the paragraph
            for word, pattern in word_patterns.items():
                if pattern.search(paragraph):
                    # Count occurrences of the word
                    occurrences += len(pattern.findall(paragraph))

                    # Highlight the word in the paragraph
                    highlighted_paragraph = pattern.sub(f"\033[94m{word}\033[0m", paragraph)
                    relevant_paragraphs.append(highlighted_paragraph.strip())
                    break  # Exit the loop after the first match to prevent duplication
        # Return the relevant paragraphs and total occurrences
        return relevant_paragraphs

    except FileNotFoundError:
        print(f"Error: Book file not found: {book_filename}")
        return [], 0  # Return empty list and zero occurrences on error


def query_engine(input, index_folder="../words_datamart_dict", metadata_folder="../metadata_datamart",
                 book_folder="../Datamart_libros", max_occurrences=3):
    """
    Searches for books containing the words in the input query and returns relevant paragraphs.

    :param input: The search query (a string of words).
    :param index_folder: Directory where the word index files are stored.
    :param metadata_folder: Directory where the book metadata JSON files are stored.
    :param book_folder: Directory where the book files are stored.
    :param max_occurrences: Maximum number of paragraphs to return for each book.
    :return: List of dictionaries with book information and paragraphs containing the search words.
    """
    input = input.lower()
    words = input.split()
    results = []

    # Dictionary to store word occurrences across books
    word_occurrences = {}

    # Step 1: Load word indices for all search words
    for word in words:
        index_data = load_json_index(word, index_folder)
        if word in index_data:
            word_occurrences[word] = index_data[word]
        else:
            print(f"Word '{word}' not found in any index.")
            return []  # Exit early if any word is missing

    # Step 2: Find common books that contain all the search words
    common_books = None
    for word, occurrences in word_occurrences.items():
        if common_books is None:
            common_books = set(occurrences.keys())
        else:
            common_books &= set(occurrences.keys())
    # Step 3: Process each book that contains all the words
    if common_books:
        for book_id in common_books:
            # Step 4: Load book metadata
            metadata = load_metadata(book_id, metadata_folder)
            if not metadata:
                print(f"Metadata for book ID '{book_id}' not found.")
                continue

            book_name = metadata["book_name"]
            author_name = metadata["author"]
            url = metadata["URL"]

            # Step 5: Load the book content
            book_path = os.path.join(book_folder, f"{book_name} by {author_name}_{book_id}.txt")

            combined_positions = []
            for word in words:
                combined_positions.extend(word_occurrences[word][book_id])
            # Step 6: Extract relevant paragraphs
            paragraphs = extract_paragraphs(book_path, combined_positions, words)
            if paragraphs:
                results.append({
                    "book_name": book_name,
                    "author_name": author_name,
                    "url": url,
                    "paragraphs": paragraphs[:max_occurrences],
                    "total_occurrences": len(paragraphs)
                })

    return results


if __name__ == "__main__":
    while True:
        search_input = input("Enter the words you want to search: ")
        search_results = query_engine(search_input)
        for result in search_results:
            print(f"Book: {result['book_name']}")
            for paragraph in result['paragraphs']:
                print(paragraph)
            print(f"Author: {result['author_name']}")
            print(f"URL: {result['url']}")
            print(f"Total occurrences: {result['total_occurrences']}\n")

import glob
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def find_book(book_id, book_folder):
    for filename in os.listdir(book_folder):
        if filename.endswith(f"_{book_id}.txt"):  # Find files that end witb _{book_id}.txt
            return os.path.join(book_folder, filename)
    return None


def load_json_file(filepath):
    """
    Loads a JSOn file and gives back a tuple with the word and its information.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "id_name" in data and "dictionary" in data:
                word_key = data["id_name"]
                dictionary_info = data["dictionary"]
                return (word_key, dictionary_info)
    except Exception as e:
        print(f"Error when loading JSON file: {filepath}: {e}")
    return None


def process_book(book_key, book_folder, input_word, max_occurrences):
    """
    Processes only 1 book to find relevant paragraphs.
    """
    try:
        book_info = book_key.split(" by ")
        book_name = book_info[0].strip()
        author_and_id = book_info[1].split(" - ")
        author_name = author_and_id[0].strip()
        book_id = author_and_id[1].strip()

        book_filename = find_book(book_id, book_folder)

        if not book_filename:
            print(f"Error: The Book with ID {book_id} was not found in {book_folder}.")
            return None

        with open(book_filename, "r", encoding="utf-8") as file:
            text = file.read()

        paragraphs = text.split('\n\n')
        relevant_paragraphs = []
        occurrences = 0

        # Create search pattern with the word
        word_pattern = re.compile(rf"\b{re.escape(input_word)}\b", re.IGNORECASE)

        for paragraph in paragraphs:
            matches = word_pattern.findall(paragraph)
            if matches:
                occurrences += len(matches)
                # Highlight found word/words
                highlighted_paragraph = word_pattern.sub(f"\033[94m{input_word}\033[0m", paragraph)
                relevant_paragraphs.append(highlighted_paragraph.strip())

        if relevant_paragraphs:
            return {
                "book_name": book_name,
                "author_name": author_name,
                "URL": f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt',
                "paragraphs": relevant_paragraphs[:max_occurrences],
                "total_occurrences": occurrences
            }
    except FileNotFoundError:
        print(f"Error: The file {book_filename} was not found.")
    except Exception as e:
        print(f"Error processing the book {book_key}: {e}")
    return None


def query_engine(input_query, book_folder="../Datamart_libros", index_folder="../Datamart_palabras", max_occurrences=3):
    """
    Perform a word search in the books using JSON indexes.

    :param input_query: The search query (can be a word or a phrase).
    :param book_folder: Path to the directory containing the books.
    :param index_folder: Path to the directory containing the JSON index files.
    :param max_occurrences: Maximum number of relevant paragraphs to return per book.
    :return: List of results with information about the occurrences found.
    """
    input_query = input_query.lower()
    words = input_query.split()
    results = []
    loaded_words = {}

    # Load JSON files in parallel
    with ThreadPoolExecutor() as executor:
        # Send tasks to load each JSON file
        future_to_filepath = {executor.submit(load_json_file, filepath): filepath for filepath in
                              glob.glob(f"{index_folder}/*.json")}
        for future in as_completed(future_to_filepath):
            result = future.result()
            if result:
                word_key, dictionary_info = result
                loaded_words[word_key] = {"dictionary": dictionary_info}

    # Verify if all the words are in the index
    words_present = all(word in loaded_words for word in words)

    if not words_present:
        print("Some of the words are not in the index.")
        return results

    # Find books that contain all the words
    books_in_common = None
    for word in words:
        word_info = loaded_words[word]["dictionary"]
        if books_in_common is None:
            books_in_common = set(word_info.keys())
        else:
            books_in_common &= set(word_info.keys())

    if not books_in_common:
        print("No books were found with all the words.")
        return results

    # Process each book in parallel
    with ThreadPoolExecutor() as executor:
        # Send tasks to process each book
        future_to_book = {executor.submit(process_book, book_key, book_folder, input_query, max_occurrences): book_key
                          for book_key in books_in_common}
        for future in as_completed(future_to_book):
            result = future.result()
            if result:
                results.append(result)

    return results


# Example for testing
input = "almost"
search_results = query_engine(input)

# output
print(f"Results for '{input}':")
if search_results:
    for result in search_results:
        print(f"Book Name: {result['book_name']}")
        print(f"Author: {result['author_name']}")
        print(f"URL: ")
        print(f"Total Ocurrencies: {result['total_occurrences']}")
        print("Paragraphs:")
        for paragraph in result['paragraphs']:
            print(f"Paragraph: {paragraph}\n")
else:
    print("No results were found.")

import glob
import json
import os
import re


def find_book(book_id, book_folder):
    """
    Searches for a book file in the specified folder by its ID.

    This function looks for a file that ends with '_{book_id}.txt' in the provided
    book folder and returns the full path if found.

    :param book_id: The ID of the book to search for.
    :param book_folder: The folder where the book files are stored.
    :return: The full path to the book file if found, otherwise None.
    """
    for filename in os.listdir(book_folder):
        if filename.endswith(f"_{book_id}.txt"):  # find file that ends with _{book_id}.txt
            return os.path.join(book_folder, filename)
    return None


def query_engine(input, book_folder, index_folder, max_occurrences=3):
    input = input.lower()
    words = input.split()
    results = []
    loaded_words = {}

    # save the JSON objects
    for filepath in glob.glob(f"{index_folder}/*.json"):
        with open(filepath, "r") as file:
            data = json.load(file)

            if "id_name" in data and "dictionary" in data:
                word_key = data["id_name"]
                dictionary_info = data["dictionary"]
                loaded_words[word_key] = {"dictionary": dictionary_info}
            else:
                print(f"Invalid structure in file: {filepath}")

    # Check if all the words are there
    words_looked_for = all(word in loaded_words for word in words)

    if words_looked_for:
        books_in_common = None
        for word in words:
            word_info = loaded_words[word]["dictionary"]
            if books_in_common is None:
                books_in_common = set(word_info.keys())
            else:
                books_in_common &= set(word_info.keys())

        if books_in_common:
            for book_key in books_in_common:

                book_info = book_key.split(" by ")
                book_name = book_info[0].strip()
                author_and_id = book_info[1].split(" - ")
                author_name = author_and_id[0].strip()
                book_id = author_and_id[1].strip()

                book_filename = find_book(book_id, book_folder)

                if book_filename:
                    try:
                        with open(book_filename, "r", encoding="utf-8") as file:  # we have to specify the encoding
                            text = file.read()

                        paragraphs = text.split('\n\n')
                        relevant_paragraphs = []
                        occurrences = 0

                        word_pattern = re.compile(rf"\b{input}\b", re.IGNORECASE)

                        for paragraph in paragraphs:
                            if word_pattern.search(paragraph):
                                occurrences += len(word_pattern.findall(paragraph))

                                highlighted_paragraph = word_pattern.sub(f"\033[94m{input}\033[0m", paragraph)
                                relevant_paragraphs.append(highlighted_paragraph.strip())

                        if relevant_paragraphs:
                            results.append({
                                "book_name": book_name,
                                "author_name": author_name,
                                "URL": f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt',
                                "paragraphs": relevant_paragraphs[:max_occurrences],
                                "total_occurrences": occurrences
                            })

                    except FileNotFoundError:
                        print(f"Error: The Book {book_filename} was not found.")

    return results

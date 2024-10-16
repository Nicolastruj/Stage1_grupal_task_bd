import os
import re
import json


def load_json_index(word, index_folder):
    first_letter = word[0].lower()
    json_path = os.path.join(index_folder, f'indexer_{first_letter}.json')

    print(f"Attempting to load index file: {json_path}")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"No index file found for letter '{first_letter}'.")
        return None


def get_book_metadata(filepath, target_id):
    """Get book metadata: title, author, and URL."""
    try:
        with open(filepath, 'r') as file:
            books = json.load(file)

        for book in books:
            if book['id_book'] == target_id:
                title = book["book_name"]
                author = book["author"]
                url = book["URL"]

                return title, author, url

        return "Unknown", "Unknown", "Unknown"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_paragraphs_from_positions(book_path, positions, search_phrase):
    """Given the list of positions, extract the surrounding paragraphs containing the search phrase."""
    paragraphs = []

    try:
        with open(book_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Adjust paragraph detection to include cases where paragraphs are split by single newlines
        book_paragraphs = re.split(r'\n\s*\n|\n{2,}', text)

        word_count = 0
        paragraph_positions = []

        for paragraph in book_paragraphs:
            # Splitting on whitespace keeps punctuation
            words_in_paragraph = re.findall(r'\S+', paragraph)
            paragraph_word_count = len(words_in_paragraph)

            # Track the word start and end for this paragraph
            paragraph_positions.append((word_count, word_count + paragraph_word_count))
            word_count += paragraph_word_count

        # Find the paragraph containing the phrase at the indicated position
        for position in positions:
            for i, (start_pos, end_pos) in enumerate(paragraph_positions):
                if start_pos <= position < end_pos:
                    # Ensure the paragraph contains the search phrase and add it
                    if search_phrase in book_paragraphs[i].lower():
                        paragraphs.append(book_paragraphs[i].strip())
                    break

    except FileNotFoundError:
        print(f"Book file not found: {book_path}")

    return paragraphs


def find_book_by_id(book_id, book_folder):
    for filename in os.listdir(book_folder):
        if f"_{book_id}.txt" in filename:
            return os.path.join(book_folder, filename)
    return None


def query_engine(search_phrase, book_folder="../Datamart_libros", index_folder="../books_datamart_dict",
                 metadata_folder="../metadata_datamart"):
    search_phrase = search_phrase.lower().strip()
    results = []

    # Split the phrase into words to look up the dictionary entries
    words = search_phrase.split()
    if not words:
        print(f"Invalid input, please provide a valid phrase.")
        return results

    word_index = load_json_index(words[0], index_folder)

    if word_index is None:
        print(f"No index file found for the word: {words[0]}")
        return results

    # If the first word of the phrase is not found, the phrase cannot be in the index
    if words[0] not in word_index:
        print(f"Word '{words[0]}' not found in the loaded index.")
        return results

    # Retrieve the positions of the first word
    word_data = word_index[words[0]]

    # Iterate through the books where the first word occurs
    for book_id, positions in word_data.items():
        book_path = find_book_by_id(book_id, book_folder)

        if not book_path:
            print(f"Book file not found for book ID {book_id}.")
            continue

        hundred_range = (int(book_id) // 100) * 100
        json_filename = f"books_metadata_{hundred_range}-{hundred_range + 99}.json"
        metadata_path = os.path.join(metadata_folder, json_filename)

        title, author, url = get_book_metadata(metadata_path, book_id)

        # Now check the paragraphs in this book
        paragraphs = get_paragraphs_from_positions(book_path, positions, search_phrase)

        if paragraphs:
            results.append({
                "book_id": book_id,
                "title": title,
                "author": author,
                "url": url,
                "paragraphs": paragraphs
            })

    return results


while True:
    phrase = input("Enter a phrase to search for: ")
    search_results = query_engine(phrase)

    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Author: {result['author']}")
        print(f"URL: {result['url']}")
        print(f"Occurrences at positions: {len(result['paragraphs'])} occurrence(s)\n")

        for paragraph in result['paragraphs']:
            print(paragraph)
            print("")
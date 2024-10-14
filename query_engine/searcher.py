import os
import json
import re

def load_json_index(word, index_folder):
    """Loads the appropriate partial indexer JSON file for the word."""
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

def get_book_metadata(book_path):
    """Extract metadata such as Title, Author, and Language from the book."""
    title, author, language = "Unknown", "Unknown", "Unknown"

    try:
        with open(book_path, 'r', encoding='utf-8') as file:
            text = file.read()
            title_match = re.search(r"Title:\s*(.*)", text)
            author_match = re.search(r"Author:\s*(.*)", text)
            language_match = re.search(r"Language:\s*(.*)", text)

            if title_match:
                title = title_match.group(1).strip()
            if author_match:
                author = author_match.group(1).strip()
            if language_match:
                language = language_match.group(1).strip()

    except FileNotFoundError:
        print(f"Book file not found: {book_path}")

    return title, author, language

def get_paragraphs_from_positions(book_path, positions):
    """Given the list of positions, extract the surrounding paragraphs."""
    paragraphs = []

    try:
        with open(book_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Split the book into paragraphs
        book_paragraphs = text.split('\n\n')
        book_text = text.replace("\n", "")  # Remove line breaks for easier position handling

        for position in positions:
            for paragraph in book_paragraphs:
                if paragraph.lower().find(book_text[position:position + 20].lower()) != -1:
                    paragraphs.append(paragraph.strip())
                    break  # Stop after finding the first match for the position

    except FileNotFoundError:
        print(f"Book file not found: {book_path}")

    return paragraphs

def find_book_by_id(book_id, book_folder):
    """Find the book file in the folder based on the book ID."""
    for filename in os.listdir(book_folder):
        if f"_{book_id}.txt" in filename:
            return os.path.join(book_folder, filename)
    return None

def query_engine(word, book_folder="../Datamart_libros", index_folder="../books_datamart_dict"):
    """Search for a word and print the book details and paragraphs where the word occurs."""
    word = word.lower().strip()
    results = []

    # Load the appropriate JSON indexer for the word
    word_index = load_json_index(word, index_folder)
    
    if word_index is None:
        print(f"No index file found for the word: {word}")
        return results

    if word not in word_index:
        print(f"Word '{word}' not found in the loaded index.")
        return results

    # Get the book IDs and positions where the word occurs
    word_data = word_index[word]

    for book_id, positions in word_data.items():
        # Find the correct book file based on its ID
        book_path = find_book_by_id(book_id, book_folder)

        if not book_path:
            print(f"Book file not found for book ID {book_id}.")
            continue

        # Extract metadata from the book
        title, author, language = get_book_metadata(book_path)

        # Extract the paragraphs where the word occurs
        paragraphs = get_paragraphs_from_positions(book_path, positions)

        if paragraphs:
            results.append({
                "book_id": book_id,
                "title": title,
                "author": author,
                "language": language,
                "paragraphs": paragraphs
            })

    return results

def main():
    word = input("Enter a word to search for: ")
    search_results = query_engine(word)

    # Display results
    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Author: {result['author']}")
        print(f"Language: {result['language']}")
        print(f"Occurrences at positions: {len(result['paragraphs'])} occurrence(s)\n")
        
        for paragraph in result['paragraphs']:
            print(f"Paragraph: {paragraph}\n")


if __name__ == "__main__":
    main()
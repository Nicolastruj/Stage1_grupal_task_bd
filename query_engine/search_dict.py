import glob
import json
import re


def extract_metadata(text):
    """Extract Title, Author, and Language from the book text."""
    title_match = re.search(r"(?:^|\n)Title:\s*(.+)$", text, re.MULTILINE)
    author_match = re.search(r"(?:^|\n)Author:\s*(.+)$", text, re.MULTILINE)
    language_match = re.search(r"(?:^|\n)Language:\s*(.+)$", text, re.MULTILINE)

    return {
        "title": title_match.group(1).strip() if title_match else "Unknown",
        "author": author_match.group(1).strip() if author_match else "Unknown",
        "language": language_match.group(1).strip() if language_match else "Unknown"
    }


def get_paragraphs_from_book(book_file, word):
    """Return the metadata and paragraphs that contain the word."""
    with open(book_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Extract metadata
    metadata = extract_metadata(text)

    # Clean the text and remove Project Gutenberg boilerplate
    start_marker = "*** START OF"
    end_marker = "*** END OF"
    if start_marker in text:
        text = text.split(start_marker, 1)[-1]  # Skip everything before the actual content
    if end_marker in text:
        text = text.split(end_marker, 1)[0]  # Skip everything after the actual content

    # Split the text into paragraphs using a more robust method (splitting on double newlines)
    paragraphs = re.split(r'\n\s*\n', text)

    # Find paragraphs that include the word (case-insensitive)
    relevant_paragraphs = []
    for paragraph in paragraphs:
        if word.lower() in paragraph.lower():
            relevant_paragraphs.append(paragraph.strip())

    return metadata, relevant_paragraphs


def query_engine(input_word, book_folder="../Datamart_libros", index_folder="../Datamart_palabras"):
    input_word = input_word.lower()
    results = []
    loaded_words = {}

    # Load all word index JSON files
    for filepath in glob.glob(f"{index_folder}/*.json"):
        with open(filepath, "r") as file:
            data = json.load(file)
            word_key = data.get("id_nombre", "").lower()
            if word_key:
                loaded_words[word_key] = data["diccionario"]

    # Check if the input word exists in the index
    if input_word in loaded_words:
        books_with_word = loaded_words[input_word]
        for book_id, positions in books_with_word.items():
            book_file = f"{book_folder}/libro_{book_id}.txt"

            try:
                # Extract metadata and paragraphs from the book
                metadata, paragraphs = get_paragraphs_from_book(book_file, input_word)

                if paragraphs:
                    # Add book metadata and paragraphs to results
                    results.append({
                        "book_id": book_id,
                        "title": metadata["title"],
                        "author": metadata["author"],
                        "language": metadata["language"],
                        "paragraphs": paragraphs
                    })

            except FileNotFoundError:
                print(f"Error: The file {book_file} was not found.")  # Handle missing book file

    return results


def main():
    input_word = input("Enter a word to search for: ")
    search_results = query_engine(input_word)

    # Display results
    if search_results:
        for result in search_results:
            print(f"Title: {result['title']}")
            print(f"Author: {result['author']}")
            print(f"Language: {result['language']}")
            print(f"Occurrences at positions: {len(result['paragraphs'])} occurrence(s)\n")
            for paragraph in result['paragraphs']:
                print(f"Paragraph: {paragraph}\n")
    else:
        print(f"No results found for '{input_word}'.")


if __name__ == "__main__":
    main()

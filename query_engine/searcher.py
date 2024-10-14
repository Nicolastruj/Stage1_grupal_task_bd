import json
import glob
import re
import os

def extract_metadata(text):
    """Extract Title, Author, and Language from the book text."""
    title_match = re.search(r"Title:\s*(.*)", text, re.IGNORECASE)
    author_match = re.search(r"Author:\s*(.*)", text, re.IGNORECASE)
    language_match = re.search(r"Language:\s*(.*)", text, re.IGNORECASE)

    title = title_match.group(1).strip() if title_match else "Unknown"
    author = author_match.group(1).strip() if author_match else "Unknown"
    language = language_match.group(1).strip() if language_match else "Unknown"

    return {
        "title": title,
        "author": author,
        "language": language
    }

def get_paragraph_by_index(text, word_indexes):
    """Extract paragraphs containing the word at specified indexes."""
    paragraphs = text.split('\n\n')  # Assume paragraphs are separated by double newlines
    relevant_paragraphs = []

    # Flatten the text and track the position of each word to match indexes
    words = text.split()
    for index in word_indexes:
        if index < len(words):
            word_position = words[index]
            for paragraph in paragraphs:
                if word_position in paragraph:
                    relevant_paragraphs.append(paragraph.strip())
                    break

    return relevant_paragraphs

def get_paragraphs_from_book(book_file, word_indexes):
    """Return the metadata and paragraphs that contain the word."""
    with open(book_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Extract metadata
    metadata = extract_metadata(text)

    # Remove Project Gutenberg boilerplate
    start_marker = "*** START OF"
    end_marker = "*** END OF"
    if start_marker in text:
        text = text.split(start_marker, 1)[-1]  # Skip everything before the actual content
    if end_marker in text:
        text = text.split(end_marker, 1)[0]  # Skip everything after the actual content

    # Get paragraphs that contain the word using the indexes from the JSON index file
    relevant_paragraphs = get_paragraph_by_index(text, word_indexes)

    return metadata, relevant_paragraphs

def query_engine(input_word, book_folder="../Datamart_libros", index_file="index.json"):
    input_word = input_word.lower()
    results = []

    # Load the dictionary JSON file (like the one you shared)
    with open(index_file, "r") as file:
        loaded_words = json.load(file)

    # Check if the input word exists in the index (by its prefix)
    prefix = input_word[:3]  # Assume first three characters are the prefix (this may vary)
    
    if prefix in loaded_words:
        books_with_word = loaded_words[prefix]
        for book_id, word_indexes in books_with_word.items():
            book_file = f"{book_folder}/libro_{book_id}.txt"

            try:
                # Extract metadata and paragraphs from the book
                metadata, paragraphs = get_paragraphs_from_book(book_file, word_indexes)

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
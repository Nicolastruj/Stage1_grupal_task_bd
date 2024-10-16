import glob
import json
import re

def query_engine(input, book_folder="../Datamart_libros",
                 index_folder="../Datamart_palabras"):
    input = input.lower()
    words = input.split()  # Split input into individual words
    results = []
    loaded_words = {}

    # Load all dictionary files
    for filepath in glob.glob(f"{index_folder}/*.json"):
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "id_nombre" in data and "diccionario" in data:
                word_key = data["id_nombre"]
                dictionary_info = data["diccionario"]
                loaded_words[word_key] = {"diccionario": dictionary_info}

    # Check if all words exist in the dictionary
    words_looked_for = all(word in loaded_words for word in words)
    if words_looked_for:
        books_in_common = None
        # Get the common books that contain all words
        for word in words:
            word_info = loaded_words[word]["diccionario"]
            if books_in_common is None:
                books_in_common = set(word_info.keys())
            else:
                books_in_common &= set(word_info.keys())  # Find intersection of book sets

        # If there are common books, check the order of the words
        if books_in_common:
            for book_id in books_in_common:
                print(book_id)
                book_filename = f"{book_folder}/libro_{book_id}.txt"

                try:
                    with open(book_filename, "r", encoding="utf-8") as file:
                        text = file.read()

                    # Splitting the text into paragraphs
                    paragraphs = text.split('\n\n')
                    relevant_paragraphs = []  # To save found paragraphs that include the words in order

                    # Find the paragraphs where the words appear in the specified order
                    for paragraph in paragraphs:
                        paragraph_text = paragraph.lower()
                        # Check if the exact sequence of words exists in the paragraph
                        if phrase_in_order(paragraph_text, words):
                            relevant_paragraphs.append(paragraph.strip())  # Save the paragraph

                    # If relevant paragraphs are found, append to the results
                    if relevant_paragraphs:
                        results.append({
                            "document_id": book_id,
                            "paragraphs": relevant_paragraphs
                        })

                except FileNotFoundError:
                    print(f"Error: The file {book_filename} was not found.")

    return results


def phrase_in_order(paragraph, words):
    """Check if the words appear consecutively in the given order in the paragraph."""
    # Create a regex pattern to match words in order, allowing for any spaces or punctuation in between
    pattern = r'\b' + r'\b.*?\b'.join(re.escape(word) for word in words) + r'\b'
    return re.search(pattern, paragraph) is not None


# Main loop for searching
while True:
    word_input = input("Enter a phrase to search for: ")

    search_results = query_engine(word_input)

    # Show the results
    print(f"Results for '{word_input}':")
    if search_results:
        for result in search_results:
            print(f"Document ID: {result['document_id']}")
            print(f"Paragraphs where the phrase is included:\n")
            for paragraph in result['paragraphs']:
                print(f"Paragraph: {paragraph} \n")
    else:
        print("No results found.")
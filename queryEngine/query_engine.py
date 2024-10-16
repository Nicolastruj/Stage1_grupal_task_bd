import json
import glob
import re
import os

def find_book(book_id, book_folder):
    for filename in os.listdir(book_folder):
        if filename.endswith(f"_{book_id}.txt"):  # Buscar archivo que termine con _{book_id}.txt
            return os.path.join(book_folder, filename)
    return None

def query_engine(input, book_folder="../Datamart_libros", index_folder="../Datamart_palabras", max_occurrences=3):
    input = input.lower()
    words = input.split()
    results = []
    loaded_words = {}

    # save the JSON objects
    for filepath in glob.glob(f"{index_folder}/*.json"):
        with open(filepath, "r") as file:
            data = json.load(file)
            if "id_nombre" in data and "diccionario" in data:
                word_key = data["id_nombre"]
                dictionary_info = data["diccionario"]
                loaded_words[word_key] = {"diccionario": dictionary_info}

    # Check if all the words are there
    words_looked_for = all(word in loaded_words for word in words)

    if words_looked_for:
        books_in_common = None
        for word in words:
            word_info = loaded_words[word]["diccionario"]
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
                        with open(book_filename, "r", encoding="utf-8") as file: #hay que especificar el encoding
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
                                #"URL": ,
                                "paragraphs": relevant_paragraphs[:max_occurrences],
                                "total_occurrences": occurrences
                            })

                    except FileNotFoundError:
                        print(f"Error: The Book {book_filename} was not found.")

    return results


#Example for testing
input = "almost"
search_results = query_engine(input)

# output
print(f"Resultados para '{input}':")
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
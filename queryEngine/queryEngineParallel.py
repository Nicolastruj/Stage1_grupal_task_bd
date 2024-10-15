import glob
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def find_book(book_id, book_folder):
    for filename in os.listdir(book_folder):
        if filename.endswith(f"_{book_id}.txt"):  # Buscar archivo que termine con _{book_id}.txt
            return os.path.join(book_folder, filename)
    return None


def load_json_file(filepath):
    """
    Carga un archivo JSON y devuelve una tupla con la palabra y su información.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "id_nombre" in data and "diccionario" in data:
                word_key = data["id_nombre"]
                dictionary_info = data["diccionario"]
                return (word_key, dictionary_info)
    except Exception as e:
        print(f"Error al cargar el archivo JSON {filepath}: {e}")
    return None


def process_book(book_key, book_folder, input_word, max_occurrences):
    """
    Procesa un solo libro para encontrar párrafos relevantes.
    """
    try:
        book_info = book_key.split(" by ")
        book_name = book_info[0].strip()
        author_and_id = book_info[1].split(" - ")
        author_name = author_and_id[0].strip()
        book_id = author_and_id[1].strip()

        book_filename = find_book(book_id, book_folder)

        if not book_filename:
            print(f"Error: El libro con ID {book_id} no fue encontrado en {book_folder}.")
            return None

        with open(book_filename, "r", encoding="utf-8") as file:
            text = file.read()

        paragraphs = text.split('\n\n')
        relevant_paragraphs = []
        occurrences = 0

        # Crear patrón de búsqueda para la palabra
        word_pattern = re.compile(rf"\b{re.escape(input_word)}\b", re.IGNORECASE)

        for paragraph in paragraphs:
            matches = word_pattern.findall(paragraph)
            if matches:
                occurrences += len(matches)
                # Resaltar las coincidencias
                highlighted_paragraph = word_pattern.sub(f"\033[94m{input_word}\033[0m", paragraph)
                relevant_paragraphs.append(highlighted_paragraph.strip())

        if relevant_paragraphs:
            return {
                "book_name": book_name,
                "author_name": author_name,
                # "URL": ,  # Puedes agregar una URL si está disponible
                "paragraphs": relevant_paragraphs[:max_occurrences],
                "total_occurrences": occurrences
            }
    except FileNotFoundError:
        print(f"Error: El archivo {book_filename} no fue encontrado.")
    except Exception as e:
        print(f"Error procesando el libro {book_key}: {e}")
    return None


def query_engine(input_query, book_folder="../Datamart_libros", index_folder="../Datamart_palabras", max_occurrences=3):
    """
    Realiza una búsqueda de palabras en los libros utilizando índices JSON.

    :param input_query: La consulta de búsqueda (puede ser una palabra o una frase).
    :param book_folder: Ruta al directorio que contiene los libros.
    :param index_folder: Ruta al directorio que contiene los archivos JSON de índices.
    :param max_occurrences: Número máximo de párrafos relevantes a devolver por libro.
    :return: Lista de resultados con información sobre las ocurrencias encontradas.
    """
    input_query = input_query.lower()
    words = input_query.split()
    results = []
    loaded_words = {}

    # Cargar archivos JSON en paralelo
    with ThreadPoolExecutor() as executor:
        # Enviar tareas para cargar cada archivo JSON
        future_to_filepath = {executor.submit(load_json_file, filepath): filepath for filepath in
                              glob.glob(f"{index_folder}/*.json")}
        for future in as_completed(future_to_filepath):
            result = future.result()
            if result:
                word_key, dictionary_info = result
                loaded_words[word_key] = {"diccionario": dictionary_info}

    # Verificar si todas las palabras están en el índice
    words_present = all(word in loaded_words for word in words)

    if not words_present:
        print("Algunas palabras de la consulta no están en el índice.")
        return results  # Retorna vacío o podrías manejar esto de otra manera

    # Encontrar libros que contienen todas las palabras de la consulta
    books_in_common = None
    for word in words:
        word_info = loaded_words[word]["diccionario"]
        if books_in_common is None:
            books_in_common = set(word_info.keys())
        else:
            books_in_common &= set(word_info.keys())

    if not books_in_common:
        print("No se encontraron libros que contengan todas las palabras de la consulta.")
        return results

    # Procesar cada libro en paralelo
    with ThreadPoolExecutor() as executor:
        # Enviar tareas para procesar cada libro
        future_to_book = {executor.submit(process_book, book_key, book_folder, input_query, max_occurrences): book_key
                          for book_key in books_in_common}
        for future in as_completed(future_to_book):
            result = future.result()
            if result:
                results.append(result)

    return results


# Example for testing
input = "españa"
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

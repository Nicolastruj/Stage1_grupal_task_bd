import json
import glob
import re  # Importar el módulo de expresiones regulares

# Función del motor de consultas
def query_engine(word, book_folder="/Users/elisa/Desktop/BDGrupoGit/Datamart_libros",
                 index_folder="/Users/elisa/Desktop/BDGrupoGit/Datamart_palabras"):
    word = word.lower()  # Convertir a minúsculas para evitar problemas de coincidencia
    results = []
    indexer = {}

    # Cargar todos los índices JSON desde la carpeta
    for filepath in glob.glob(f"{index_folder}/*.json"):
        with open(filepath, "r") as file:
            data = json.load(file)
            # Suponiendo que el JSON tiene la estructura mencionada
            if "id_nombre" in data and "diccionario" in data:
                word_key = data["id_nombre"]  # Extraer la palabra
                dictionary_info = data["diccionario"]  # Obtener el diccionario

                # Guardar en el índice
                indexer[word_key] = {"diccionario": dictionary_info}

    # Verificar si la palabra está en el índice
    if word in indexer:
        info = indexer[word]["diccionario"]  # Obtener el diccionario de IDs de libros y posiciones

        for book_id, positions in info.items():
            # Construir el nombre del archivo del libro
            book_filename = f"{book_folder}/libro_{book_id}.txt"  # Concatenar la ruta y el nombre del archivo

            # Leer el texto del libro
            try:
                with open(book_filename, "r") as book_file:
                    text = book_file.read()

                # Separar el texto en párrafos
                paragraphs = text.split('\n\n')
                relevant_paragraphs = []

                # Buscar en los párrafos para encontrar los relevantes
                for position in positions:
                    for paragraph in paragraphs:
                        # Comprobar si la palabra exacta está en el párrafo
                        if re.search(r'\b' + re.escape(word) + r'\b', paragraph.lower()):  # Buscar solo coincidencias exactas
                            relevant_paragraphs.append(paragraph.strip())
                            break  # Salir del bucle una vez que se encuentre el párrafo

                # Agregar el resultado solo si hay párrafos relevantes
                if relevant_paragraphs:
                    results.append({
                        "document_id": book_id,
                        "paragraphs": relevant_paragraphs
                    })

            except FileNotFoundError:
                print(f"Error: The file {book_filename} was not found.")  # Mensaje de error si el archivo no existe

    return results


# Ejemplo de uso
word = "abandon"  # Palabra a buscar
search_results = query_engine(word)

# Mostrar resultados
print(f"Results for '{word}':")
if search_results:  # Solo imprimir si hay resultados
    for result in search_results:
        print(f"Book Name: {result['document_id']}")
        print(f"URL: \n")
        print(f"Paragraphs where the word is included: \n")
        for paragraph in result['paragraphs']:
            print(f"{paragraph} \n")  # Mostrar los párrafos relevantes
else:
    print("No results found.")

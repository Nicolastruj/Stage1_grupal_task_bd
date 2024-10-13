# main.py
import json


#  import os

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import re
from  data_model.object_type.Palabra import Palabra

def indexer(datamart_txt_path, datamart_json_path):
    """
    Procesa archivos de texto en `datamart_txt_path` y actualiza objetos Palabra en `datamart_json_path`.

    :param datamart_txt_path: Ruta al directorio que contiene los archivos de texto.
    :param datamart_json_path: Ruta al directorio donde se almacenarán los archivos JSON.
    """
    # Asegurarse de que el directorio de JSON exista
    "os.makedirs(datamart_json_path, exist_ok=True)"

    # Obtener todos los archivos txt que siguen el patrón 'libro_indice.txt'
    txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^libro_\d+\.txt$', f)]

    for txt_file in txt_files:
        # Extraer el índice numérico del nombre del archivo
        match = re.match(r'^libro_(\d+)\.txt$', txt_file)
        if not match:
            continue  # Saltar archivos que no coincidan

        indice_libro = match.group(1)
        txt_file_path = os.path.join(datamart_txt_path, txt_file)

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            contenido = file.read()

        # Tokenizar el contenido en palabras usando regex (considerando palabras alfanuméricas)
        palabras = re.findall(r'\b\w+\b', contenido.lower())

        for posicion, palabra in enumerate(palabras, start=1):
            # Ruta al archivo JSON correspondiente a la palabra
            json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")

            if os.path.exists(json_file_path):
                # Cargar el objeto Palabra existente
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    palabra_obj = Palabra.from_dict(data)

                # Verificar si el índice del libro ya está en el diccionario
                if indice_libro in palabra_obj.diccionario:
                    palabra_obj.diccionario[indice_libro].append(posicion)
                else:
                    palabra_obj.diccionario[indice_libro] = [posicion]
            else:
                # Crear un nuevo objeto Palabra
                palabra_obj = Palabra(id_nombre=palabra, diccionario={indice_libro: [posicion]})

            # Guardar el objeto Palabra actualizado en JSON
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

    print("Indexación completada.")


# def indexer2(datamart_txt_path, datamart_json_path):
#     """
#     Procesa archivos de texto en `datamart_txt_path` y actualiza objetos Palabra en `datamart_json_path`.
#     Solo procesa palabras, excluyendo números u otros caracteres, y almacena el número de párrafo donde
#     aparece cada palabra. Si no encuentra un párrafo, se guarda 'np'.

#     :param datamart_txt_path: Ruta al directorio que contiene los archivos de texto.
#     :param datamart_json_path: Ruta al directorio donde se almacenarán los archivos JSON.
#     """
#     # Asegurarse de que el directorio de JSON exista
#     "os.makedirs(datamart_json_path, exist_ok=True)"

#     # Obtener todos los archivos txt que siguen el patrón 'libro_indice.txt'
#     txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^libro_\d+\.txt$', f)]
#     #txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^\d+\.txt$', f)]

#     print(txt_files)

#     for txt_file in txt_files:
#         # Extraer el índice numérico del nombre del archivo
#         match = re.match(r'^libro_(\d+)\.txt$', txt_file)
#         if not match:
#             continue  # Saltar archivos que no coincidan

#         indice_libro = match.group(1)
#         txt_file_path = os.path.join(datamart_txt_path, txt_file)

#         with open(txt_file_path, 'r', encoding='utf-8') as file:
#             contenido = file.read()

#         # Dividir el contenido en párrafos
#         parrafos = contenido.split("\n\n")  # Asumiendo que los párrafos están separados por una línea vacía

#         for num_parrafo, parrafo in enumerate(parrafos, start=1):
#             # Tokenizar solo palabras alfabéticas (excluyendo números y caracteres especiales)
#             palabras = re.findall(r'\b[a-zA-Z]+\b', parrafo.lower())

#             for palabra in palabras:
#                 # Ruta al archivo JSON correspondiente a la palabra
#                 json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")

#                 if os.path.exists(json_file_path):
#                     # Cargar el objeto Palabra existente
#                     with open(json_file_path, 'r', encoding='utf-8') as json_file:
#                         data = json.load(json_file)
#                         palabra_obj = Palabra.from_dict(data)

#                     # Verificar si el índice del libro ya está en el diccionario
#                     if indice_libro in palabra_obj.diccionario:
#                         palabra_obj.diccionario[indice_libro].append(num_parrafo)
#                     else:
#                         palabra_obj.diccionario[indice_libro] = [num_parrafo]
#                 else:
#                     # Crear un nuevo objeto Palabra
#                     palabra_obj = Palabra(id_nombre=palabra, diccionario={indice_libro: [num_parrafo]})

#                 # Guardar el objeto Palabra actualizado en JSON
#                 with open(json_file_path, 'w', encoding='utf-8') as json_file:
#                     json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

#         # Si no hay párrafos identificados, registrar 'np'
#         if not parrafos:
#             palabras_sin_parrafo = re.findall(r'\b[a-zA-Z]+\b', contenido.lower())
#             for palabra in palabras_sin_parrafo:
#                 json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")

#                 if os.path.exists(json_file_path):
#                     with open(json_file_path, 'r', encoding='utf-8') as json_file:
#                         data = json.load(json_file)
#                         palabra_obj = Palabra.from_dict(data)
#                     if indice_libro in palabra_obj.diccionario:
#                         palabra_obj.diccionario[indice_libro].append('np')
#                     else:
#                         palabra_obj.diccionario[indice_libro] = ['np']
#                 else:
#                     palabra_obj = Palabra(id_nombre=palabra, diccionario={indice_libro: ['np']})

#                 with open(json_file_path, 'w', encoding='utf-8') as json_file:
#                     json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

#     print("Indexación completada.")


def indexer2(datamart_txt_path, datamart_json_path):
    os.makedirs(datamart_json_path, exist_ok=True)
    txt_files = [f for f in os.listdir(datamart_txt_path) if f.endswith('.txt')]

    for txt_file in txt_files:
        match = re.match(r'^libro_(\d+)\.txt$', txt_file)
        if not match:
            continue

        indice_libro = match.group(1)
        txt_file_path = os.path.join(datamart_txt_path, txt_file)

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            contenido = file.read()

        parrafos = contenido.split("\n\n")

        for num_parrafo, parrafo in enumerate(parrafos, start=1):
            palabras = re.findall(r'\b[a-zA-Z]+\b', parrafo.lower())

            for palabra in palabras:
                json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")
                os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        palabra_obj = Palabra.from_dict(data)

                    if indice_libro in palabra_obj.diccionario:
                        palabra_obj.diccionario[indice_libro].append(num_parrafo)
                    else:
                        palabra_obj.diccionario[indice_libro] = [num_parrafo]
                else:
                    palabra_obj = Palabra(id_nombre=palabra, diccionario={indice_libro: [num_parrafo]})

                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

        if not parrafos:
            palabras_sin_parrafo = re.findall(r'\b[a-zA-Z]+\b', contenido.lower())
            for palabra in palabras_sin_parrafo:
                json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")
                os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        palabra_obj = Palabra.from_dict(data)
                    if indice_libro in palabra_obj.diccionario:
                        palabra_obj.diccionario[indice_libro].append('np')
                    else:
                        palabra_obj.diccionario[indice_libro] = ['np']
                else:
                    palabra_obj = Palabra(id_nombre=palabra, diccionario={indice_libro: ['np']})

                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

    print("Indexación completada.")


# main.py
import multiprocessing
import os
import json
import re
from  data_model.object_type.Palabra import Palabra
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

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
        match = re.match(r'^(.+?) by (.+?)_(\d+)\.txt$', txt_file)
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


def indexer2(datamart_txt_path, datamart_json_path):
    """
    Procesa archivos de texto en `datamart_txt_path` y actualiza objetos Palabra en `datamart_json_path`.
    Solo procesa palabras, excluyendo números u otros caracteres, y almacena el número de párrafo donde
    aparece cada palabra. Si no encuentra un párrafo, se guarda 'np'.

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

        # Dividir el contenido en párrafos
        parrafos = contenido.split("\n\n")  # Asumiendo que los párrafos están separados por una línea vacía

        for num_parrafo, parrafo in enumerate(parrafos, start=1):
            # Tokenizar solo palabras alfabéticas (excluyendo números y caracteres especiales)
            palabras = re.findall(r'\b[a-zA-Z]+\b', parrafo.lower())

            for palabra in palabras:
                # Ruta al archivo JSON correspondiente a la palabra
                json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")

                if os.path.exists(json_file_path):
                    # Cargar el objeto Palabra existente
                    with open(json_file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        palabra_obj = Palabra.from_dict(data)

                    # Verificar si el índice del libro ya está en el diccionario
                    if indice_libro in palabra_obj.diccionario:
                        palabra_obj.diccionario[indice_libro].append(num_parrafo)
                    else:
                        palabra_obj.diccionario[indice_libro] = [num_parrafo]
                else:
                    # Crear un nuevo objeto Palabra
                    palabra_obj = Palabra(id_nombre=palabra, diccionario={indice_libro: [num_parrafo]})

                # Guardar el objeto Palabra actualizado en JSON
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

        # Si no hay párrafos identificados, registrar 'np'
        if not parrafos:
            palabras_sin_parrafo = re.findall(r'\b[a-zA-Z]+\b', contenido.lower())
            for palabra in palabras_sin_parrafo:
                json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")

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

def indexer3(datamart_txt_path, datamart_json_path):
    """
    Procesa archivos de texto en `datamart_txt_path` que siguen el patrón 'The Title by Author_indice.txt'
    y actualiza objetos Palabra en `datamart_json_path`. Las claves en el diccionario son una cadena con
    el nombre del libro, el autor y el índice.

    :param datamart_txt_path: Ruta al directorio que contiene los archivos de texto.
    :param datamart_json_path: Ruta al directorio donde se almacenarán los archivos JSON.
    """
    # Asegurarse de que el directorio de JSON exista
    os.makedirs(datamart_json_path, exist_ok=True)

    # Obtener todos los archivos txt que siguen el patrón 'The Title by Author_indice.txt'
    txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^.+? by .+?_\d+\.txt$', f)]

    for txt_file in txt_files:
        # Extraer el nombre del libro, el autor y el índice numérico del nombre del archivo
        match = re.match(r'^(.+?) by (.+?)_(\d+)\.txt$', txt_file)
        if not match:
            continue  # Saltar archivos que no coincidan

        nombre_libro = match.group(1)
        autor = match.group(2)
        indice = match.group(3)
        clave_diccionario = f"{nombre_libro} by {autor} {indice}"  # Crear la clave como cadena

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

                # Verificar si la clave ya está en el diccionario
                if clave_diccionario in palabra_obj.diccionario:
                    palabra_obj.diccionario[clave_diccionario].append(posicion)
                else:
                    palabra_obj.diccionario[clave_diccionario] = [posicion]
            else:
                # Crear un nuevo objeto Palabra
                palabra_obj = Palabra(id_nombre=palabra, diccionario={clave_diccionario: [posicion]})

            # Guardar el objeto Palabra actualizado en JSON
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

    print("Indexación completada.")

def indexer4(datamart_txt_path, datamart_json_path):
    """
    Procesa archivos de texto en `datamart_txt_path` que siguen el patrón 'The Title by Author_indice.txt'
    y actualiza objetos Palabra en `datamart_json_path`. Las claves en el diccionario son una cadena con
    el nombre del libro, el autor y el índice.

    Devuelve la linea con texto en la que esta

    :param datamart_txt_path: Ruta al directorio que contiene los archivos de texto.
    :param datamart_json_path: Ruta al directorio donde se almacenarán los archivos JSON.
    """
    # Asegurarse de que el directorio de JSON exista
    os.makedirs(datamart_json_path, exist_ok=True)

    # Obtener todos los archivos txt que siguen el patrón 'The Title by Author_indice.txt'
    txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^.+? by .+?_\d+\.txt$', f)]

    for txt_file in txt_files:
        # Extraer el nombre del libro, el autor y el índice numérico del nombre del archivo
        match = re.match(r'^(.+?) by (.+?)_(\d+)\.txt$', txt_file)
        if not match:
            continue  # Saltar archivos que no coincidan

        nombre_libro = match.group(1)
        autor = match.group(2)
        indice = match.group(3)
        clave_diccionario = f"{nombre_libro} by {autor} {indice}"  # Crear la clave como cadena

        txt_file_path = os.path.join(datamart_txt_path, txt_file)

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            contenido = file.read()

        # Dividir el contenido en párrafos
        parrafos = re.split(r'\n{2,}', contenido)

        for num_parrafo, parrafo in enumerate(parrafos, start=1):
            # Tokenizar solo palabras alfabéticas (excluyendo números y caracteres especiales)
            palabras = re.findall(r'\b[a-zA-Z]+\b', parrafo.lower())

            for palabra in palabras:
                # Ruta al archivo JSON correspondiente a la palabra
                json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")

                if os.path.exists(json_file_path):
                    # Cargar el objeto Palabra existente
                    with open(json_file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        palabra_obj = Palabra.from_dict(data)

                    # Verificar si la clave ya está en el diccionario
                    if clave_diccionario in palabra_obj.diccionario:
                        palabra_obj.diccionario[clave_diccionario].append(num_parrafo)
                    else:
                        palabra_obj.diccionario[clave_diccionario] = [num_parrafo]
                else:
                    # Crear un nuevo objeto Palabra
                    palabra_obj = Palabra(id_nombre=palabra, diccionario={clave_diccionario: [num_parrafo]})

                # Guardar el objeto Palabra actualizado en JSON
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

    print("Indexación completada.")

def indexer5(datamart_txt_path, datamart_json_path):
    """
    Procesa archivos de texto en `datamart_txt_path` y actualiza objetos Palabra en `datamart_json_path`.
    Las claves en el diccionario son el índice del libro, el autor y el nombre.

    :param datamart_txt_path: Ruta al directorio que contiene los archivos de texto.
    :param datamart_json_path: Ruta al directorio donde se almacenarán los archivos JSON.
    """
    # Asegurarse de que el directorio de JSON exista
    os.makedirs(datamart_json_path, exist_ok=True)

    # Obtener todos los archivos txt que siguen el patrón 'The Title by Author_indice.txt'
    txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^.+? by .+?_\d+\.txt$', f)]

    for txt_file in txt_files:
        # Extraer el nombre del libro, el autor y el índice numérico del nombre del archivo
        match = re.match(r'^(.+?) by (.+?)_(\d+)\.txt$', txt_file)
        print(f"Procesando archivo: {txt_file}")
        if not match:
            continue  # Saltar archivos que no coincidan

        print(f"Archivos encontrados: {match}")
        nombre_libro = match.group(1)
        autor = match.group(2)
        indice = match.group(3)
        print(f"Coincidencias: {nombre_libro}, {autor}, {indice}")
        clave_diccionario = f"{nombre_libro} by {autor} - {indice}"  # Crear la clave como cadena

        txt_file_path = os.path.join(datamart_txt_path, txt_file)

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            contenido = file.read()

        # Tokenizar el contenido en palabras usando regex (considerando palabras alfanuméricas)
        palabras = re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+\b', contenido.lower())
        palabras = [palabra for palabra in palabras if
                    palabra not in ['in', 'on', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                                    'into', 'through', 'during', 'before', 'after', 'above', 'below',
                                    'to', 'from', 'up', 'down', 'of', 'off', 'over', 'under', 'again',
                                    'further', 'once', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                                    'you', 'your', 'yours',
                                    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                                    'herself',
                                    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
                                    'which',
                                    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were',
                                    'be',
                                    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
                                    'an',
                                    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                                    'by',
                                    'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                                    'after',
                                    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
                                    'under',
                                    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                                    'all',
                                    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                                    'not',
                                    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
                                    'don',
                                    'should', 'now']]

        for posicion, palabra in enumerate(palabras, start=1):
            # Ruta al archivo JSON correspondiente a la palabra
            json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")

            if os.path.exists(json_file_path):
                # Cargar el objeto Palabra existente
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    palabra_obj = Palabra.from_dict(data)

                # Verificar si la clave ya está en el diccionario
                if clave_diccionario in palabra_obj.diccionario:
                    palabra_obj.diccionario[clave_diccionario].append(posicion)
                else:
                    palabra_obj.diccionario[clave_diccionario] = [posicion]
            else:
                # Crear un nuevo objeto Palabra
                palabra_obj = Palabra(id_nombre=palabra, diccionario={clave_diccionario: [posicion]})

            # Guardar el objeto Palabra actualizado en JSON
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

    print("Indexación completada.")


lock = Lock()


def procesar_palabra(palabra, posicion, clave_diccionario, datamart_json_path):
    json_file_path = os.path.join(datamart_json_path, f"{palabra}.json")

    with lock:  # Asegurar que solo un hilo acceda a este bloque a la vez
        if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                palabra_obj = Palabra.from_dict(data)
        else:
            palabra_obj = Palabra(id_nombre=palabra, diccionario={})

        # Actualizar el objeto Palabra
        if clave_diccionario in palabra_obj.diccionario:
            palabra_obj.diccionario[clave_diccionario].append(posicion)
        else:
            palabra_obj.diccionario[clave_diccionario] = [posicion]

        # Guardar el objeto Palabra actualizado en JSON
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(palabra_obj.to_dict(), json_file, ensure_ascii=False, indent=4)


def indexer5_parallel(datamart_txt_path, datamart_json_path):
    os.makedirs(datamart_json_path, exist_ok=True)
    txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^.+? by .+?_\d+\.txt$', f)]

    for txt_file in txt_files:
        match = re.match(r'^(.+?) by (.+?)_(\d+)\.txt$', txt_file)
        if not match:
            continue

        nombre_libro = match.group(1)
        autor = match.group(2)
        indice = match.group(3)
        clave_diccionario = f"{nombre_libro} by {autor} - {indice}"
        txt_file_path = os.path.join(datamart_txt_path, txt_file)

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            contenido = file.read()

        palabras = re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+\b', contenido.lower())
        palabras = [palabra for palabra in palabras if palabra not in ['in', 'on', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                                    'into', 'through', 'during', 'before', 'after', 'above', 'below',
                                    'to', 'from', 'up', 'down', 'of', 'off', 'over', 'under', 'again',
                                    'further', 'once', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                                    'you', 'your', 'yours',
                                    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                                    'herself',
                                    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
                                    'which',
                                    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were',
                                    'be',
                                    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
                                    'an',
                                    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                                    'by',
                                    'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                                    'after',
                                    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
                                    'under',
                                    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                                    'all',
                                    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                                    'not',
                                    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
                                    'don',
                                    'should', 'now']]  # Tus palabras a excluir

        with ThreadPoolExecutor() as executor:
            for posicion, palabra in enumerate(palabras, start=1):
                executor.submit(procesar_palabra, palabra, posicion, clave_diccionario, datamart_json_path)

    print("Indexación completada.")
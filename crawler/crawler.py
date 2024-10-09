import os
import requests


def descargar_libro(id_libro, ruta_descarga):
    url = f'https://www.gutenberg.org/files/{id_libro}/{id_libro}-0.txt'
    if not os.path.exists(ruta_descarga):
        os.makedirs(ruta_descarga)

    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        # Leer el contenido del libro
        contenido = respuesta.text

        # Extraer el título y el autor del contenido
        lineas = contenido.splitlines()
        titulo = ""
        autor = ""

        for linea in lineas:
            # El título está en la primera línea, el autor suele estar en la segunda
            if linea.startswith("Title:"):
                titulo = linea.replace("Title:", "").strip()
            elif linea.startswith("Author:"):
                autor = linea.replace("Author:", "").strip()
            # Salir si ya se tienen ambos
            if titulo and autor:
                break

        # Formatear el nombre del archivo
        nombre_archivo = f"{titulo}_{autor}_{id_libro}.txt"
        nombre_archivo = os.path.join(ruta_descarga, nombre_archivo.replace('/', '-').replace('\\', '-'))

        # Guardar el contenido en el archivo
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        print(f"Libro {id_libro} descargado correctamente como {nombre_archivo}")
    elif respuesta.status_code == 404:
        print(f"Libro {id_libro} no encontrado.")
    else:
        print(f"Error al intentar descargar el libro {id_libro}: {respuesta.status_code}")


# Definir la ruta específica donde guardar los libros
ruta_descarga = r"C:\Users\Nico\PycharmProjects\pythonProject5\Datamart_libros"  # Cambia esto a la ruta deseada

# Descargar libros desde el ID 1340 hasta el 1350 en la ruta especificada
for id_libro in range(4, 25):
    descargar_libro(id_libro, ruta_descarga)

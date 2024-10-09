import os
import requests

def descargar_libro(id_libro, ruta_descarga):
    url = f'https://www.gutenberg.org/files/{id_libro}/{id_libro}-0.txt'
    if not os.path.exists(ruta_descarga):
        os.makedirs(ruta_descarga)
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        # Crear la ruta completa donde se guardará el archivo
        nombre_archivo = os.path.join(ruta_descarga, f'libro_{id_libro}.txt')

        # Guardar el contenido en el archivo
        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(respuesta.content)
        print(f"Libro {id_libro} descargado correctamente como {nombre_archivo}")
    elif respuesta.status_code == 404:
        print(f"Libro {id_libro} no encontrado.")
    else:
        print(f"Error al intentar descargar el libro {id_libro}: {respuesta.status_code}")


# Definir la ruta específica donde guardar los libros
ruta_descarga = r"C:\Users\Nico\PycharmProjects\pythonProject5\Datamart_libros"  # Cambia esto a la ruta deseada

# Descargar libros desde el ID 1340 hasta el 1350 en la ruta especificada
for id_libro in range(1340, 1351):
    descargar_libro(id_libro, ruta_descarga)
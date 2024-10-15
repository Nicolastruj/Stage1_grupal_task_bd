# import os
# import requests
# from bs4 import BeautifulSoup



# def obtener_titulo(url):
#     try:
#         # Realizar la solicitud GET a la URL
#         respuesta = requests.get(url)

#         # Comprobar si la solicitud fue exitosa
#         if respuesta.status_code == 200:
#             # Analizar el contenido HTML de la página
#             soup = BeautifulSoup(respuesta.text, 'html.parser')

#             # Buscar el primer <h1> en la página
#             h1 = soup.find('h1')

#             # Si se encontró un <h1>, devolver su texto
#             if h1:
#                 return h1.get_text().strip()
#             else:
#                 return "No se encontró ningún <h1> en la página."
#         else:
#             return f"Error al acceder a la página. Código de estado: {respuesta.status_code}"

#     except requests.RequestException as e:
#         return f"Error al realizar la solicitud: {e}"
# def descargar_libro(id_libro, ruta_descarga):
#     url = f'https://www.gutenberg.org/files/{id_libro}/{id_libro}-0.txt'
#     if not os.path.exists(ruta_descarga):
#         os.makedirs(ruta_descarga)
#     respuesta = requests.get(url)

#     if respuesta.status_code == 200:
#         # Extraer contenido como texto
#         contenido = respuesta.text

#         # Llamar a la función assign_tittle para obtener el nombre del archivo
#         nombre_archivo = obtener_titulo(f"https://www.gutenberg.org/ebooks/{id_libro}")
#         nombre_archivo = os.path.join(ruta_descarga, f'{nombre_archivo}_{id_libro}.txt')

#         # Guardar el contenido en el archivo
#         with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
#             archivo.write(contenido)

#         print(f"Libro {id_libro} descargado correctamente como {nombre_archivo}")
#     elif respuesta.status_code == 404:
#         print(f"Libro {id_libro} no encontrado.")
#     else:
#         print(f"Error al intentar descargar el libro {id_libro}: {respuesta.status_code}")


# # Definir la ruta específica donde guardar los libros
# ruta_descarga = r"./Datamart_libros"  # Cambia esto a la ruta deseada

# # Descargar libros desde el ID 1340 hasta el 1350 en la ruta especificada
# for id_libro in range(1340, 1351):
#     descargar_libro(id_libro, ruta_descarga)


import os
import requests
from bs4 import BeautifulSoup



def obtener_titulo(url):
    try:
        # Realizar la solicitud GET a la URL
        respuesta = requests.get(url)

        # Comprobar si la solicitud fue exitosa
        if respuesta.status_code == 200:
            # Analizar el contenido HTML de la página
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar el primer <h1> en la página
            h1 = soup.find('h1')

            # Si se encontró un <h1>, devolver su texto
            if h1:
                return h1.get_text().strip()
            else:
                return "No se encontró ningún <h1> en la página."
        else:
            return f"Error al acceder a la página. Código de estado: {respuesta.status_code}"

    except requests.RequestException as e:
        return f"Error al realizar la solicitud: {e}"
def descargar_libro(id_libro, ruta_descarga):
    url = f'https://www.gutenberg.org/files/{id_libro}/{id_libro}-0.txt'
    if not os.path.exists(ruta_descarga):
        os.makedirs(ruta_descarga)
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        # Extraer contenido como texto
        contenido = respuesta.text

        # Llamar a la función assign_tittle para obtener el nombre del archivo
        nombre_archivo = obtener_titulo(f"https://www.gutenberg.org/ebooks/{id_libro}")
        nombre_archivo = os.path.join(ruta_descarga, f'{nombre_archivo}_{id_libro}.txt')

        # Guardar el contenido en el archivo
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)

        print(f"Libro {id_libro} descargado correctamente como {nombre_archivo}")
    elif respuesta.status_code == 404:
        print(f"Libro {id_libro} no encontrado.")
    else:
        print(f"Error al intentar descargar el libro {id_libro}: {respuesta.status_code}")


# Definir la ruta específica donde guardar los libros
ruta_descarga = r"../Datamart_libros"  # Cambia esto a la ruta deseada

# Descargar libros desde el ID 1340 hasta el 1350 en la ruta especificada
for id_libro in range(1340, 1351):
    descargar_libro(id_libro, ruta_descarga)
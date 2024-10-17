import os
import shutil
import schedule
import time

from indexer_dict.indexer_dict import indexer_dict


def job(books_directory, tray, words_directory):
    print(f"Ejecutando el trabajo con los directorios:\n"
          f"Libros: {books_directory}\n"
          f"Bandeja: {tray}\n"
          f"Palabras: {words_directory}")
    time.sleep(20)
    files = get_latest_files(books_directory)
    print(f"Archivos encontrados: {files}")

    if not files:
        print("No se encontraron archivos para procesar.")
        return

    copy_files_to_temp_directory(files, tray)
    print(f"Archivos copiados a la bandeja temporal: {files}")

    indexer_dict(tray, words_directory)
    print("Indexación completada.")

    delete_temp_directory(tray)
    print(f"Directorio temporal eliminado: {tray}")


def delete_temp_directory(temp_directory):
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)
        print(f"Directorio temporal eliminado: {temp_directory}")
    else:
        print(f"El directorio temporal no existe: {temp_directory}")


def get_latest_files(source_directory, num_files=3):
    print(f"Buscando los últimos {num_files} archivos en: {source_directory}")
    files = [f for f in os.listdir(source_directory) if f.endswith('.txt')]

    files_with_path = [os.path.join(source_directory, f) for f in files]
    files_with_path = [f for f in files_with_path if os.path.isfile(f)]

    # Ordenar archivos por fecha de modificación
    files_with_path.sort(key=os.path.getmtime, reverse=True)

    # Retornar los últimos 'num_files' archivos
    return files_with_path[:num_files]


def copy_files_to_temp_directory(latest_files, temp_directory):
    print(f"Copiando archivos a: {temp_directory}")
    os.makedirs(temp_directory, exist_ok=True)

    for file in latest_files:
        shutil.copy(file, temp_directory)
        print(f"Archivo copiado: {file}")


def execute_indexer(books_directory, tray, words_directory):
    # Ejecutar el trabajo inmediatamente
    print("Ejecutando la tarea inicial inmediatamente...")
    job(books_directory, tray, words_directory)

    # Configurar el scheduler para ejecuciones posteriores
    setup_schedule(books_directory, tray, words_directory)
    print("Scheduler configurado. Esperando ejecuciones programadas...")

    while True:
        schedule.run_pending()  # Ejecuta las tareas programadas
        time.sleep(1)


def setup_schedule(books_directory, tray, words_directory):
    print("Configurando el cronograma para la tarea programada.")
    schedule.every(5).minutes.do(lambda: job(books_directory, tray, words_directory))
    print("Tarea programada cada 5 minutos.")
from pathlib import Path


def extract_files_from_directory(directory):
    path = Path(directory)
    files_paths = []

    for file_path in path.iterdir():
        if file_path.is_file():
            files_paths.append(file_path)
    return files_paths


directory_path = './Datamart_libros'
files_paths = extract_files_from_directory(directory_path)
print(files_paths)

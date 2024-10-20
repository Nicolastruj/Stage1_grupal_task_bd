from pathlib import Path


def extract_files_from_directory(directory):
    """
    Extract and return a list of file paths from the specified directory.

    :param directory: The path to the directory from which to extract files.
    :return: A list of file paths in the directory.
    """
    path = Path(directory)
    files_paths = []

    for file_path in path.iterdir():
        if file_path.is_file():
            files_paths.append(file_path)
    return files_paths

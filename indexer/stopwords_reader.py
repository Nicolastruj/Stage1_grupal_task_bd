def load_stopwords_from_file(file_path):
    """
    Reads words from a file and returns them in a list.

    :param file_path: The path to the text file containing the words.
    :return: A list of words read from the file, stripped of whitespace.
    """
    words_list = []

    with open(file_path, "r") as file:
        for line in file:
            words_list.append(line.strip())

    return words_list

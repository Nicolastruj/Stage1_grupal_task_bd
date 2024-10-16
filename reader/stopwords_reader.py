def load_stopwords_from_file(file_path):
    """Reads words from a file and returns them in a list.

    Args:
        file_path (str): The path to the text file containing the words.

    Returns:
        list: A list of words read from the file.
    """
    words_list = []

    with open(file_path, "r") as file:
        for line in file:
            words_list.append(line.strip())

    return words_list


def main():
    file_path = "../stopwords.txt"
    words_list = load_stopwords_from_file(file_path)

    print(words_list)


if __name__ == "__main__":
    main()
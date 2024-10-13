import re


def read_words(filepath):
    """Extract words from a TXT file and return a list of words."""

    # TODO check regex pattern. English words can accept "-" in the middle of the word
    # TODO exclude stop words
    words = []
    encodings = ['utf-8', 'utf-8-sig', 'windows-1252', 'latin1']

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                content = file.read()
                words = re.findall(r'\b\w+\b', content.lower())
                return words
        except UnicodeDecodeError:
            print(f"Error decoding with {encoding}, trying next...")
            continue
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            return words
        except Exception as e:
            print(f"Error: {e}")
            return words

    print("Error: Could not decode the file with any of the attempted encodings.")
    return words

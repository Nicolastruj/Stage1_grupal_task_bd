import re


# TODO check regex

def read_words(filepath):
    """Extract words from a TXT file and return a list of words."""
    words = []

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", content.lower())
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as file:
                content = file.read()
                words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", content.lower())
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            return words
        except Exception as e:
            print(f"Error: {e}")
            return words
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return words
    except Exception as e:
        print(f"Error: {e}")
        return words

    return words

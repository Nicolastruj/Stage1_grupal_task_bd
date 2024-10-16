# main.py
import multiprocessing
import os
import json
import re
from  data_model.object_type.Word import Word
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

def indexer5(datamart_txt_path, datamart_json_path):
    """
    Process text tiles in `datamart_txt_path` and update the Word objects in `datamart_json_path`.
    The keys in the dictionary are the index of the book, the author and the name.

    :param datamart_txt_path: Path to the directory containing the text files.
    :param datamart_json_path: Path to the directory where the JSON files will be stored.
    """
    # Make sure the directory for JSON exists
    os.makedirs(datamart_json_path, exist_ok=True)

    # Find all the files that follow the pattern 'The Title by Author_indice.txt'
    txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^.+? by .+?_\d+\.txt$', f)]

    for txt_file in txt_files:
        # Extract the name of the book, its author and the index of the file name
        match = re.match(r'^(.+?) by (.+?)_(\d+)\.txt$', txt_file)
        print(f"Processing file: {txt_file}")
        if not match:
            continue  # Skip files that don't coincide

        print(f"Files Found: {match}")
        book_name = match.group(1)
        author = match.group(2)
        index = match.group(3)
        print(f"Ocurrences: {book_name}, {author}, {index}")
        dictionary_key = f"{book_name} by {author} - {index}"

        txt_file_path = os.path.join(datamart_txt_path, txt_file)

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Token the content into words using regex (only taking into consideration alphanumerics)
        # Skips Stop Words
        words = re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+\b', content.lower())
        words = [word for word in words if
                    word not in ['in', 'on', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                                    'into', 'through', 'during', 'before', 'after', 'above', 'below',
                                    'to', 'from', 'up', 'down', 'of', 'off', 'over', 'under', 'again',
                                    'further', 'once', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                                    'you', 'your', 'yours',
                                    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                                    'herself',
                                    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
                                    'which',
                                    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were',
                                    'be',
                                    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
                                    'an',
                                    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                                    'by',
                                    'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                                    'after',
                                    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
                                    'under',
                                    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                                    'all',
                                    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                                    'not',
                                    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
                                    'don',
                                    'should', 'now']]

        for position, word in enumerate(words, start=1):
            # Route to the JSON file of the word
            json_file_path = os.path.join(datamart_json_path, f"{word}.json")

            if os.path.exists(json_file_path):
                # Load the Word object that exists
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    word_obj = Word.from_dict(data)

                # Verify if the key is in the dictionary
                if dictionary_key in word_obj.dictionary:
                    word_obj.dictionary[dictionary_key].append(position)
                else:
                    word_obj.dictionary[dictionary_key] = [position]
            else:
                # Create a new Word object
                word_obj = Word(id_name=word, dictionary={dictionary_key: [position]})

            # Save the updates Word object to the JSON
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(word_obj.to_dict(), json_file, ensure_ascii=False, indent=4)

    print("Indexation Completed.")


lock = Lock()


def process_word(word, position, dictionary_key, datamart_json_path):
    json_file_path = os.path.join(datamart_json_path, f"{word}.json")

    with lock:  # Make sure only one Thread accesses at a time
        if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                word_obj = Word.from_dict(data)
        else:
            word_obj = Word(id_name=word, dictionary={})

        # Update the Word object
        if dictionary_key in word_obj.dictionary:
            word_obj.dictionary[dictionary_key].append(position)
        else:
            word_obj.dictionary[dictionary_key] = [position]

        # Save the Word object in the JSON
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(word_obj.to_dict(), json_file, ensure_ascii=False, indent=4)


def indexer5_parallel(datamart_txt_path, datamart_json_path):
    os.makedirs(datamart_json_path, exist_ok=True)
    txt_files = [f for f in os.listdir(datamart_txt_path) if re.match(r'^.+? by .+?_\d+\.txt$', f)]

    for txt_file in txt_files:
        match = re.match(r'^(.+?) by (.+?)_(\d+)\.txt$', txt_file)
        if not match:
            continue

        book_name = match.group(1)
        author = match.group(2)
        index = match.group(3)
        dictionary_key = f"{book_name} by {author} - {index}"
        txt_file_path = os.path.join(datamart_txt_path, txt_file)

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        words = re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+\b', content.lower())
        words = [word for word in words if word not in ['in', 'on', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                                    'into', 'through', 'during', 'before', 'after', 'above', 'below',
                                    'to', 'from', 'up', 'down', 'of', 'off', 'over', 'under', 'again',
                                    'further', 'once', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                                    'you', 'your', 'yours',
                                    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                                    'herself',
                                    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
                                    'which',
                                    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were',
                                    'be',
                                    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
                                    'an',
                                    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                                    'by',
                                    'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                                    'after',
                                    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
                                    'under',
                                    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                                    'all',
                                    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                                    'not',
                                    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
                                    'don',
                                    'should', 'now']]

        with ThreadPoolExecutor() as executor:
            for position, word in enumerate(words, start=1):
                executor.submit(process_word, word, position, dictionary_key, datamart_json_path)

    print("Indexation Completed.")
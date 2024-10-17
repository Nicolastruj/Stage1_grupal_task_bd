import os
import re
import json
import time
import psutil

def load_json_index(word, index_folder):
    first_letter = word[0].lower()
    json_path = os.path.join(index_folder, f'indexer_{first_letter}.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None


def get_book_metadata(filepath, target_id):
    try:
        with open(filepath, 'r') as file:
            books = json.load(file)

        for book in books:
            if book['id_book'] == target_id:
                title = book["book_name"]
                author = book["author"]
                url = book["URL"]
                return title, author, url

        return "Unknown", "Unknown", "Unknown"
    except Exception as e:
        return None


def get_paragraphs_from_positions(book_path, positions, search_phrase):
    paragraphs = []
    try:
        with open(book_path, 'r', encoding='utf-8') as file:
            text = file.read()
        book_paragraphs = re.split(r'\n\s*\n|\n{2,}', text)

        word_count = 0
        paragraph_positions = []

        for paragraph in book_paragraphs:
            words_in_paragraph = re.findall(r'\S+', paragraph)
            paragraph_word_count = len(words_in_paragraph)
            paragraph_positions.append((word_count, word_count + paragraph_word_count))
            word_count += paragraph_word_count

        for position in positions:
            for i, (start_pos, end_pos) in enumerate(paragraph_positions):
                if start_pos <= position < end_pos:
                    if search_phrase in book_paragraphs[i].lower():
                        paragraphs.append(book_paragraphs[i].strip())
                    break
    except FileNotFoundError:
        return []

    return paragraphs


def find_book_by_id(book_id, book_folder):
    for filename in os.listdir(book_folder):
        if f"_{book_id}.txt" in filename:
            return os.path.join(book_folder, filename)
    return None


def query_engine(search_phrase, book_folder="../Datamart_libros", index_folder="../books_datamart_dict",
                 metadata_folder="../metadata_datamart"):
    search_phrase = search_phrase.lower().strip()
    results = []

    words = search_phrase.split()
    if not words:
        return results

    word_index = load_json_index(words[0], index_folder)
    if word_index is None or words[0] not in word_index:
        return results

    word_data = word_index[words[0]]

    for book_id, positions in word_data.items():
        book_path = find_book_by_id(book_id, book_folder)
        if not book_path:
            continue

        hundred_range = (int(book_id) // 100) * 100
        json_filename = f"books_metadata_{hundred_range}-{hundred_range + 99}.json"
        metadata_path = os.path.join(metadata_folder, json_filename)
        title, author, url = get_book_metadata(metadata_path, book_id)

        paragraphs = get_paragraphs_from_positions(book_path, positions, search_phrase)
        if paragraphs:
            results.append({
                "book_id": book_id,
                "title": title,
                "author": author,
                "url": url,
                "paragraphs": paragraphs
            })

    return results


def benchmark_query(phrase):
    start_wall_time = time.time()
    start_cpu_time = time.process_time()
    
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss

    search_results = query_engine(phrase)

    end_wall_time = time.time()
    end_cpu_time = time.process_time()
    end_memory = process.memory_info().rss

    wall_time = end_wall_time - start_wall_time
    cpu_time = end_cpu_time - start_cpu_time
    memory_usage = (end_memory - start_memory) / (1024 ** 2)  # in MB

    print(f"Wall clock time: {wall_time:.4f} seconds")
    print(f"CPU time: {cpu_time:.4f} seconds")
    print(f"Memory used: {memory_usage:.4f} MB")

    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Author: {result['author']}")
        print(f"URL: {result['url']}")
        print(f"Occurrences at positions: {len(result['paragraphs'])} occurrence(s)\n")
        for paragraph in result['paragraphs']:
            print(paragraph)
            print("")


while True:
    phrase = input("Enter a phrase to search for: ")
    benchmark_query(phrase)
import os
import json
import re

def load_json_index(word, index_folder):
    first_letter = word[0].lower()
    json_path = os.path.join(index_folder, f'indexer_{first_letter}.json')

    print(f"Attempting to load index file: {json_path}")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"No index file found for letter '{first_letter}'.")
        return None

def get_book_metadata(book_path):
    title, author, language = "Unknown", "Unknown", "Unknown"

    try:
        with open(book_path, 'r', encoding='utf-8') as file:
            text = file.read()
            title_match = re.search(r"Title:\s*(.*)", text)
            author_match = re.search(r"Author:\s*(.*)", text)
            language_match = re.search(r"Language:\s*(.*)", text)

            if title_match:
                title = title_match.group(1).strip()
            if author_match:
                author = author_match.group(1).strip()
            if language_match:
                language = language_match.group(1).strip()

    except FileNotFoundError:
        print(f"Book file not found: {book_path}")

    return title, author, language


# def get_paragraphs_from_positions(book_path, positions, search_word):
#     """Given the list of positions, extract the surrounding paragraphs."""
#     paragraphs = []
    
#     try:
#         with open(book_path, 'r', encoding='utf-8') as file:
#             text = file.read()
        
#         book_paragraphs = text.split('\n\n')
        
#         word_count = 0
#         paragraph_positions = [] 
        
#         for paragraph in book_paragraphs:
#             words_in_paragraph = paragraph.split()
#             paragraph_word_count = len(words_in_paragraph)
            
#             paragraph_positions.append((word_count, word_count + paragraph_word_count))
            
#             word_count += paragraph_word_count
        
#         for position in positions:
#             for i, (start_pos, end_pos) in enumerate(paragraph_positions):
#                 if start_pos <= position < end_pos:
#                     paragraphs.append(book_paragraphs[i].strip())
#                     break  

#     except FileNotFoundError:
#         print(f"Book file not found: {book_path}")

#     return paragraphs


def get_paragraphs_from_positions(book_path, positions, search_word):
    """Given the list of positions, extract the surrounding paragraphs containing the search word."""
    paragraphs = []
    
    try:
        with open(book_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Adjust paragraph detection to include cases where paragraphs are split by single newlines
        book_paragraphs = re.split(r'\n\s*\n|\n{2,}', text)
        
        word_count = 0
        paragraph_positions = [] 
        
        for paragraph in book_paragraphs:
            # Splitting on whitespace keeps punctuation
            words_in_paragraph = re.findall(r'\S+', paragraph)
            paragraph_word_count = len(words_in_paragraph)
            
            # Track the word start and end for this paragraph
            paragraph_positions.append((word_count, word_count + paragraph_word_count))
            word_count += paragraph_word_count
        
        # Find the paragraph containing the word at the indicated position
        for position in positions:
            for i, (start_pos, end_pos) in enumerate(paragraph_positions):
                if start_pos <= position < end_pos:
                    # Ensure the paragraph contains the search word and add it
                    if search_word in book_paragraphs[i].lower():
                        paragraphs.append(book_paragraphs[i].strip())
                    break  

    except FileNotFoundError:
        print(f"Book file not found: {book_path}")

    return paragraphs

    

def find_book_by_id(book_id, book_folder):
   
    for filename in os.listdir(book_folder):
        if f"_{book_id}.txt" in filename:
            return os.path.join(book_folder, filename)
    return None

def query_engine(word, book_folder="../Datamart_libros", index_folder="../books_datamart_dict"):
   
    word = word.lower().strip()
    results = []

    word_index = load_json_index(word, index_folder)
    
    if word_index is None:
        print(f"No index file found for the word: {word}")
        return results

    if word not in word_index:
        print(f"Word '{word}' not found in the loaded index.")
        return results

    word_data = word_index[word]

    for book_id, positions in word_data.items():
        book_path = find_book_by_id(book_id, book_folder)

        if not book_path:
            print(f"Book file not found for book ID {book_id}.")
            continue

        title, author, language = get_book_metadata(book_path)

        paragraphs = get_paragraphs_from_positions(book_path, positions, word)

        if paragraphs:
            results.append({
                "book_id": book_id,
                "title": title,
                "author": author,
                "language": language,
                "paragraphs": paragraphs
            })

    return results

def main():

    while(True):
        word = input("Enter a word to search for: ")
        search_results = query_engine(word)

        for result in search_results:
            print(f"Title: {result['title']}")
            print(f"Author: {result['author']}")
            print(f"Language: {result['language']}")
            print(f"Occurrences at positions: {len(result['paragraphs'])} occurrence(s)\n")
            
            for paragraph in result['paragraphs']:
                print(paragraph)
                print("")


if __name__ == "__main__":
    main()
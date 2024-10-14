import json
import glob

def query_engine(input, book_folder="../Datamart_libros",
                 index_folder="../Datamart_palabras"):
    input = input.lower()
    words = input.split()
    results = []
    loaded_words = {}

    for filepath in glob.glob(f"{index_folder}/*.json"):
        try:
            #print(filepath)
            #with open(filepath, "r") as file:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if "id_nombre" in data and "diccionario" in data:
                    word_key = data["id_nombre"]
                    dictionary_info = data["diccionario"]  #getting the information out of the diccionary in the JSON object
                    loaded_words[word_key] = {"diccionario": dictionary_info} #saving the information of the word in a diccionary
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {filepath}")
        except FileNotFoundError:
            print(f"Error: {filepath} not found")
        except Exception as e:
            print(f"An error occurred while processing {filepath}: {e}")


    words_looked_for= all(word in loaded_words for word in words) #here we check if all the words looked for are in the diccionary we just created
    if words_looked_for:
        books_in_common = None
        for word in words:
            word_info = loaded_words[word]["diccionario"]
            if books_in_common is None:
                books_in_common = set(word_info.keys())  # common books that include the word
            else:
                books_in_common &= set(word_info.keys())  # So that it only takes into account books that include all of the words together

        # If there are books in common with all the words looked for
        if books_in_common:
            for book_id in books_in_common:
                book_filename = f"{book_folder}/libro_{book_id}.txt"

                try:
                    # with open(book_filename, "r") as file:
                    with open(book_filename, "r", encoding="utf-8") as file:
                        text = file.read()

                    # separating the text into paragraphs
                    paragraphs = text.split('\n\n')
                    relevant_paragraphs = [] #to save the found paragraphs that include the word or words

                    # Finding the word/words
                    for paragraph in paragraphs:
                        if input in paragraph.lower():  # Check to see if the exact word/words are in the paragraph
                            relevant_paragraphs.append(paragraph.strip()) #and save them

                    # if there are any, we append them to the paragraphs
                    if relevant_paragraphs:
                        results.append({
                            "document_id": book_id,
                            "paragraphs": relevant_paragraphs
                        })

                except FileNotFoundError:
                    print(f"Error: The file {book_filename} was not found.")  # Error message if there is no boook foudn

    return results


# For trying out the code
input = "beauty"  # words as AND
#input = "abandon" #word to check
search_results = query_engine(input)

# Showing the results - output
print(f"Results for '{input}':")
if search_results:  # Only if there are results, otherwise "else"
    for result in search_results:
        print(f"Document ID: {result['document_id']}")
        print(f"URL: \n")
        print(f"Paragraphs where the word is included: \n")

        for paragraph in result['paragraphs']: #printing out all the paragraphs found
            print(f"Paragraph: {paragraph} \n")
else:
    print("No results found.")


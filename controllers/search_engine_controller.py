from queryEngine.query_engine_dict import query_engine as query_engine_dict


def search_engine_controller():
    """
    Start the search engine interface for querying words in the indexed books.

    This function allows users to input words to search for and displays the results,
    including book name, author, URL, total occurrences, and relevant paragraphs.
    The user can exit the search engine by typing 'EXIT'.

    :return: None
    """
    print("\nWelcome to the Search Engine!")
    print("If you desire to exit the search engine, type 'EXIT'")

    while True:
        user_input = input("\nWhat word/words would you like to look for? ").strip()

        if user_input == "EXIT":
            print("\nSearch Engine Stopped Successfully!\n"
                  "Have a nice day! :)\n")
            break

        ## Code for JSON structure
        # results = query_engine(user_input)

        ## Code for dictionary structure
        indexer_folder = "../Words_Datamart"
        metadata_datamart_folder = "../Books_Metadata"
        book_datamart_folder = "../Books_Datamart"
        results = query_engine_dict(user_input, indexer_folder, metadata_datamart_folder, book_datamart_folder)

        if results:
            print(f"\nResults for '{user_input}':\n")
            for result in results:
                print(f"Book Name: {result['book_name']}")
                print(f"Author: {result['author_name']}")
                print(f"URL: {result['URL']}")
                print(f"Total Occurrences: {result['total_occurrences']}")
                print("Paragraphs:\n")
                for paragraph in result['paragraphs']:
                    print(f"Paragraph: {paragraph}\n")
        else:
            print("\nSorry! No results were found for that word.\n")


def main():
    search_engine_controller()


if __name__ == "__main__":
    main()

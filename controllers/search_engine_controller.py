from queryEngine.query_engine import query_engine

def search_engine_controller():
    print("\nWelcome to the Search Engine!")
    print("If you desire to exit the search engine, type 'EXIT'")

    while True:
        user_input = input("\nWhat word/words would you like to look for? ").strip()

        if user_input == "EXIT":
            print("\nSearch Engine Stopped Successfully!\n"
                  "Have a nice day! :)\n")
            break

        results = query_engine(user_input)

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
search_engine_controller()
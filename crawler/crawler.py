import os

import requests
from bs4 import BeautifulSoup


def get_title(url):
    """
    Fetch the title of a webpage by retrieving the text from the first <h1> tag.

    :param url: The URL of the webpage to fetch the title from.
    :return: The text of the first <h1> tag if found; otherwise, an error message or indication of failure.
    """
    try:
        # GET request to URL
        answer = requests.get(url)

        # See if request was successful
        if answer.status_code == 200:
            # Analyze HTML
            soup = BeautifulSoup(answer.text, 'html.parser')

            # find the first <h1>
            h1 = soup.find('h1')

            # If found, give back the text
            if h1:
                return h1.get_text().strip()
            else:
                return "There was no <h1> found."
        else:
            return f"Error accessing the page. Status code: {answer.status_code}"

    except requests.RequestException as e:
        return f"Error making the request: {e}"


def download_book(book_id, download_route):
    """
    Download a book from Project Gutenberg using its book ID and save it to a specified directory.

    :param book_id: The ID of the book to be downloaded from Project Gutenberg.
    :param download_route: The directory where the downloaded book will be saved.
    :return: None
    """
    url = f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt'
    if not os.path.exists(download_route):
        os.makedirs(download_route)
    answer = requests.get(url)

    if answer.status_code == 200:
        # Extract content as text
        content = answer.text

        # Call assign_title to find the file name
        file_name = get_title(f"https://www.gutenberg.org/ebooks/{book_id}")
        file_name = os.path.join(download_route, f'{file_name}_{book_id}.txt')

        # Save content in file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Book {book_id} downloaded correctly under {file_name}")
    elif answer.status_code == 404:
        print(f"Book {book_id} not found.")
    else:
        print(f"Error when downloading Book {book_id}: {answer.status_code}")
    return answer.status_code


# # Route to store the book
# download_route = r"../Datamart_books"  # Change this to the desired route
#
# # download books with ID 1340 until 1350 in the specific route
# for book_id in range(1343, 1346):
#     download_book(book_id, download_route)

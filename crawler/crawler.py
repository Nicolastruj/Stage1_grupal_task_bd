import os

import requests
from bs4 import BeautifulSoup


def get_title(url):
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


# Route to store the book
download_route = r"../Datamart_books"  # Change this to the desired route

# download books with ID 1340 untin 1350 in the specific route
for book_id in range(1343, 1346):
    download_book(book_id, download_route)

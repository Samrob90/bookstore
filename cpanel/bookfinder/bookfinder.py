import requests
import pprint


def search_books(title):
    # Google Books API endpoint for searching books
    url = "https://www.googleapis.com/books/v1/volumes?q=" + title.replace(" ", "+")

    # Request the URL
    response = requests.get(url)
    data = response.json()

    # Check if there are any results
    if data["totalItems"] == 0:
        return None

    # Extract the first result
    book = data["items"][0]["volumeInfo"]
    bookid = data["items"][0]["id"]
    # print(book["categories"])
    # print(book["imageLinks"])

    # imge_url = f"https://books.google.com/books/publisher/content/images/frontcover/\{bookid}?fife=w400-h600&source=gbs_api"

    # Extract the title, author, and description of the book
    book_title = book.get("title", "")
    book_author = book.get("authors", [])[0] if "authors" in book else ""
    book_description = book.get("description", "")
    book_thumbnail = (
        book["imageLinks"].get("thumbnail", "") if "imageLinks" in book else ""
    )
    subtitle = book.get("subtitle", None)

    # Return the details as a dictionary
    pagecount = book.get("pageCount", "")
    publishedDate = book.get("publishedDate", "")
    publisher = book.get("publisher", "")
    language = book.get("language", "")
    ISBN0 = [
        book["industryIdentifiers"][1]["type"],
        book["industryIdentifiers"][1]["identifier"],
    ]
    ISBN1 = [
        book["industryIdentifiers"][0]["type"],
        book["industryIdentifiers"][0]["identifier"],
    ]

    # ebook
    dimensions = book.get("dimensions", [])
    print(book.get("category"))
    text_to_speach = book.get("textToSpeechPermission", "")

    ebook = {
        "text_to_speach": "Enabled",
        "Screen_Reader": "Suported",
        "Enhanced_typesetting": "Enabled",
        "X_RAY": "Enabled",
        "Word_Wide": "Enabled",
    }
    # if subtitle is not None:
    #     title = f"{title} : {subtitle}"

    bookInfo = {
        "title": title,
        "author": book_author,
        "description": book_description,
        "book_thumbnail": book_thumbnail,
    }
    paperback_bookdetails = {
        "publisher": publisher,
        "language": language,
        "bookpages": pagecount,
        ISBN0[0]: ISBN0[1],
        ISBN1[0]: ISBN1[1],
        "dimensions": f"{dimensions['height']} x {dimensions['width']} x {dimensions['thickness']}"
        if "dimensions" in book
        else "",
        "published_date": publishedDate,
    }
    return [paperback_bookdetails, bookInfo, ebook]


# def get_book_image(book_id):
#     url = f"https://books.google.com/books/content?id={book_id}&printsec=frontcover&img=1&zoom=1&source=gbs_api"
#     response = requests.get(url)
#     print(response.content)


if __name__ == "__main__":
    isbn = "9781400079278"
    endpoint = "https://www.googleapis.com/books/v1/volumes"
    parameters = {"q": f"isbn:{isbn}", "fields": "volumeInfo(dimensions)"}
    response = requests.get(endpoint, params=parameters)
    data = response.json()
    print(data)
    # dimensions = data["items"][0]["volumeInfo"].get("dimensions")

    # # Return the dimensions or None if not found
    # print(dimensions)

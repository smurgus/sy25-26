import requests
from bs4 import BeautifulSoup
import time

class TomeRaiders:
    def __init__(self):
        self.books = []

    def fetch_books(self, url):
        headers = {'User-Agent': 'TomeRaidersBot/1.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        book_list = soup.select('article.product_pod')

        for book in book_list:
            title = book.h3.a['title']
            relative_url = book.h3.a['href']
            book_url = "https://books.toscrape.com/catalogue/" + relative_url.replace('../../../', '')

            author, genre = self.fetch_book_details(book_url)

            price_text = book.find('p', class_='price_color').text.strip('£')
            try:
                price = float(price_text)
            except:
                price = 0.0

            rating_class = book.find('p', class_='star-rating')['class'][1]
            rating = self.convert_rating(rating_class)

            self.books.append({
                'title': title,
                'url': book_url,
                'price': price,
                'rating': rating,
                'author': author,
                'genre': genre
            })

            # Delay for politeness
            time.sleep(0.2)

    def fetch_book_details(self, url):
        headers = {'User-Agent': 'TomeRaidersBot/1.0'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            author = 'Unknown'
            author_tag = soup.find('a', href=True, rel='author')
            if author_tag:
                author = author_tag.text.strip()

            genre = 'Unknown'
            breadcrumb = soup.select('ul.breadcrumb li a')
            if len(breadcrumb) >= 3:
                genre = breadcrumb[-2].text.strip()

            return author, genre
        except Exception:
            return 'Unknown', 'Unknown'

    def convert_rating(self, rating_str):
        ratings = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        return ratings.get(rating_str, 0)

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b['title'].lower()]

    def search_by_author(self, author):
        return [b for b in self.books if author.lower() in b['author'].lower()]

    def search_by_genre(self, genre):
        return [b for b in self.books if genre.lower() in b['genre'].lower()]

    def filter_by_price(self, ascending=True):
        return sorted(self.books, key=lambda x: x['price'], reverse=not ascending)

    def filter_by_rating(self, highest=True):
        return sorted(self.books, key=lambda x: x['rating'], reverse=highest)

    def display_books(self, books):
        if not books:
            print("No books found.")
            return
        for b in books:
            print(f"Title: {b['title']}")
            print(f"Author: {b['author']}")
            print(f"Genre: {b['genre']}")
            print(f"Price: £{b['price']}")
            print(f"Rating: {b['rating']} stars")
            print(f"URL: {b['url']}")
            print("-" * 50)

def get_categories():
    url = "https://books.toscrape.com/"
    headers = {'User-Agent': 'TomeRaidersBot/1.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = {}
    for li in soup.select('ul.nav li ul li a'):
        name = li.text.strip()
        link = "https://books.toscrape.com/" + li['href']
        categories[name] = link
    return categories

def main():
    print("Welcome to Tome Raiders!")
    categories = get_categories()
    print("\nAvailable categories:")
    for idx, name in enumerate(categories.keys(), 1):
        print(f"{idx}. {name}")

    choice = input("Select a category by number: ").strip()

    try:
        choice_idx = int(choice)
        if choice_idx < 1 or choice_idx > len(categories):
            print("Invalid selection. Exiting.")
            return
        selected_category = list(categories.items())[choice_idx - 1]
    except:
        print("Invalid input. Exiting.")
        return

    category_name, category_url = selected_category
    print(f"\nScraping books from category: {category_name}")
    raider = TomeRaiders()
    print("Fetching books, please wait...")
    raider.fetch_books(category_url)
    print(f"Fetched {len(raider.books)} books from {category_name}.\n")

    while True:
        print("\nWhat would you like to do?")
        print("1. View all books")
        print("2. Search by title")
        print("3. Search by author")
        print("4. Search by genre")
        print("5. Filter by price")
        print("6. Filter by rating")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            raider.display_books(raider.books)
        elif choice == '2':
            title = input("Enter title keyword: ").strip()
            results = raider.search_by_title(title)
            raider.display_books(results)
        elif choice == '3':
            author = input("Enter author keyword: ").strip()
            results = raider.search_by_author(author)
            raider.display_books(results)
        elif choice == '4':
            genre = input("Enter genre keyword: ").strip()
            results = raider.search_by_genre(genre)
            raider.display_books(results)
        elif choice == '5':
            order = input("Sort by price ascending or descending? (a/d): ").strip().lower()
            ascending = True if order == 'a' else False
            results = raider.filter_by_price(ascending=ascending)
            raider.display_books(results)
        elif choice == '6':
            order = input("Sort by rating highest or lowest? (h/l): ").strip().lower()
            highest = True if order == 'h' else False
            results = raider.filter_by_rating(highest=highest)
            raider.display_books(results)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
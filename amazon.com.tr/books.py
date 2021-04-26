# %%
from bs4 import BeautifulSoup
import requests
import csv

csv_file = open('bestsellers.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Rank', 'Title', 'Author', 'Price'])

source = requests.get('https://www.amazon.com.tr/gp/bestsellers/books/').text

soup = BeautifulSoup(source, 'lxml')

rank = 0
for book_section in soup.find_all('li', class_='zg-item-immersion'):
    rank += 1
    book_rank = '#{}'.format(rank)
    print('#',rank)
    title = book_section.find('div', class_='p13n-sc-truncate p13n-sc-line-clamp-1').text
    # Remove spaces at the beginning and at the end of the string
    title = title.strip()
    print(title)

    author = book_section.find('div', class_='a-row a-size-small').span.text
    print(author)

    price = book_section.find('span', class_='a-size-base a-color-price').span.text
    print(price)
    print()

    csv_writer.writerow([book_rank, title, author, price])

csv_file.close()
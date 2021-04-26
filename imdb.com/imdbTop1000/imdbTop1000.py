# %%
import requests
from bs4 import BeautifulSoup
import csv
import json
import time

# write the data into a csv file
csv_file = open('imdbTop1000.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Rank', 'Title', 'Year', 'Director', 'Genre', 'Length (in minutes)', 'IMDb Rating', 'Metascore Rating'])

result = []
t0 = time.perf_counter()
for top_in_the_page in range(1, 1001, 50):

    page_url = 'https://www.imdb.com/search/title/?groups=top_1000&start={}'.format(top_in_the_page)
    source = requests.get(page_url)
    soup = BeautifulSoup(source.text, 'lxml')

    # find the data of the first movie in the list
    # movie = soup.find('div', class_='lister-item-content')
    for movie in soup.find_all('div', class_='lister-item-content'):
        rank = int(movie.h3.span.text[:-1].replace(',', ''))
        # print(f'#{rank}')
        title = movie.h3.a.text
        # print(title)
        year = movie.find('span', class_='lister-item-year text-muted unbold').text
        year = int(year.split()[-1][1:-1])
        # print(year)
        director = movie.find('p', class_='').a.text
        # print(director)
        genre = movie.p.find('span', class_='genre').text.strip()
        # print(genre)
        length = int(movie.p.find('span', class_='runtime').text.split()[0])
        # print(length)
        ratings_bar = movie.div
        imdb_rating = float(ratings_bar.find('div', class_='inline-block ratings-imdb-rating').strong.text)
        # print(imdb_rating)
        try:
            metascore_rating = int(ratings_bar.find('div', class_='inline-block ratings-metascore').span.text.strip())
        except Exception as e:
            metascore_rating = None
        # print(metascore_rating)
        # print()

        data = {
            'rank': rank,
            'title': title,
            'year': year,
            'director': director,
            'genre': genre,
            'length (in min)': length,
            'ratings': {
                'imdb': imdb_rating,
                'metascore': metascore_rating
            }
        }
        result.append(data)

        csv_writer.writerow([f'#{rank}', title, year, director, genre, length, imdb_rating, metascore_rating])

    # sleep the program between requests to not hammer the website.
    time.sleep(source.elapsed.total_seconds())
    print(f'Got {top_in_the_page} to {top_in_the_page+49} in {source.elapsed.total_seconds()} seconds...')

t1 = time.perf_counter()
print(f'Finished in {t1-t0} seconds.')

# prevent to get non-ascii characters as unicode escape sequences
# by setting ensure_ascii to False and leaving encoding to the file object.
with open('imdbTop1000.json', 'w', encoding='utf8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

csv_file.close()

# %%

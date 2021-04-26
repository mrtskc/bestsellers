# %%
import requests
from bs4 import BeautifulSoup
import csv
import json

# write the data into a csv file
csv_file = open('imdbTop50.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Rank', 'Title', 'Year', 'Director', 'Genre', 'Length (in minutes)', 'IMDb Rating', 'Metascore Rating'])

source = requests.get('https://www.imdb.com/search/title/?groups=top_1000&start=1').text
soup = BeautifulSoup(source, 'lxml')

result = []
# find the data of the first movie in the list
# movie = soup.find('div', class_='lister-item-content')
for movie in soup.find_all('div', class_='lister-item-content'):
    rank = int(movie.h3.span.text[:-1].replace(',', ''))
    print(f'#{rank}')

    title = movie.h3.a.text
    print(title)

    year = movie.find('span', class_='lister-item-year text-muted unbold').text
    year = int(year.split()[-1][1:-1])
    print(year)

    director = movie.find('p', class_='').a.text
    print(director)

    genre = movie.p.find('span', class_='genre').text.strip()
    print(genre)

    length = int(movie.p.find('span', class_='runtime').text.split()[0])
    print(length)
    
    ratings_bar = movie.div
    imdb_rating = float(ratings_bar.find('div', class_='inline-block ratings-imdb-rating').strong.text)
    print(imdb_rating)

    try:
        metascore_rating = int(ratings_bar.find('div', class_='inline-block ratings-metascore').span.text.strip())
    except Exception as e:
        metascore_rating = None

    print(metascore_rating)
    print()

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

    csv_writer.writerow(['#{}'.format(rank), title, year, director, genre, length, imdb_rating, metascore_rating])

    with open('imdbTop50.json', 'w') as f:
        json.dump(result, f, indent=2)

csv_file.close()

# %%

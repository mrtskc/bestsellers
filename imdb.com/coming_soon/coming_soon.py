# %%
from bs4 import BeautifulSoup
import requests
import csv

csv_file = open('coming_soon.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Production year', 'Director', 'Metascore'])

source = requests.get('https://www.imdb.com/movies-coming-soon/').text
soup = BeautifulSoup(source, 'lxml')

# table = soup.find('table', class_="nm-title-overview-widget-layout")
for table in soup.find_all('table', class_="nm-title-overview-widget-layout"):
    #1 title
    title = table.h4.a.text
    name = title.split('(')[0].strip()
    prod_year = title.split('(')[1][:-1]
    print(name)
    print(prod_year)
    # 2 director 
    director = table.find('div', class_='txt-block').a.text
    print(director)

    try:
        # 3 metascore
        metascore = table.find('div', class_='rating_txt').span.text
    except Exception as e:
        metascore = 'Not yet scored'
    print(metascore)
    print()
    csv_writer.writerow([name, prod_year, director, metascore])

csv_file.close()
# %%

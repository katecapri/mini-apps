import csv
import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.mk.ru/anekdoti/')
html_data = BeautifulSoup(response.text, 'html.parser')
jokes = html_data.find_all(class_='article-listing__list-item')
with open('jokes.csv', 'w') as file:
    headers_list = ['Date', 'Joke']
    csv_writer = csv.DictWriter(file, fieldnames=headers_list)
    csv_writer.writeheader()
    for joke in jokes:
        csv_writer.writerow({
            'Date': '\n'+joke.h2.text,
            'Joke': joke.find(class_='listing-preview__desc').text
        })

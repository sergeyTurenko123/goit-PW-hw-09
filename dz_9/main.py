import requests
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
import json
from model import Authors, Quotes
from mongoengine import connect
import configparser

def quotes():
    store_ = []
    for i in range(11):
        url = f'http://quotes.toscrape.com/page/{i+1}'
        html_doc = requests.get(url)
        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            quotes = soup.find_all('div', class_= 'quote')
            for quote in quotes:
                tags = [tag.text for tag in quote.find_all('a', class_='tag')]
                author = quote.find('small', class_='author').text
                quote = quote.find('span', class_='text').text
                store_.append({
                    'tags': tags,
                    'author': author,
                    'quote': quote
                })
    return store_

def authors():
    store_ = []
    for i in range(11):
        url = f'http://quotes.toscrape.com/page/{i+1}'
        html_doc = requests.get(url)
        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            authors = soup.find_all('div', class_= 'quote')
            for author in authors:
                fullname = author.find('small', class_='author').text
                link = author.find("a")
                url2 = f'http://quotes.toscrape.com{link['href']}'
                html_doc = requests.get(url2)
                soup= BeautifulSoup(html_doc.content, 'html.parser')
                texts= soup.find_all('div', class_="author-details")
                for text in texts:
                    born_date= text.find('span', class_="author-born-date").text
                    born_location= text.find('span', class_="author-born-location").text
                    description= text.find('div', class_="author-description").text
                    store_.append({
                        'fullname': fullname,
                        'born_date': born_date,
                        'born_location': born_location,
                        'description': description
                        })
    return store_




if __name__ == '__main__':
    store = quotes()
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(store, f)
    author = authors()
    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(author, f)
    config = configparser.ConfigParser()
    connect(host=f"""mongodb+srv://sturenko4:31122014@sturenko4.e02me8x.mongodb.net/base.authors?retryWrites=true&w=majority&appName=sturenko4""", ssl=True)
    with open('authors.json') as f:
        lists = json.load(f)

    for list in lists:
        u2 = Authors()
        u2 = u2.from_json(json.dumps(list)).save()

    with open('quotes.json') as f:
        lists = json.load(f)

    for list in lists:
        quote = Quotes(quote=list.get('quote'), tags=list.get('tags'), author=Authors.objects(fullname=list.get('author')).first())
        quote.save()
    
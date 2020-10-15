"""

"""
import sys, csv, requests, re
# import numpy as np
from bs4 import BeautifulSoup


class ArticleScraper():

    def __init__(self, keyword_location="keywords.txt", article_location="articles.txt"):
        print("Initializing Article Scaper...")
        self.keyword_location = keyword_location
        self.article_location = article_location

        print(f'Loading keywords from {self.keyword_location}')
        self.keywords = self.load_from_file(self.keyword_location)
        print(f'Parsed {len(self.keywords)} Keywords: {self.keywords}')

        print(f'Loading articles from {self.article_location}')
        self.articles = self.load_from_file(self.article_location)
        print(f'Parsed {len(self.articles)} articles: {self.articles}')

        print('Inializing TLDs')
        self.domains = { 'www.huffpost.com': 'Huffington Post',
                         'www.nytimes.com': 'New York Times',
                         'www.apnews.com': 'Associated Press',
                         'www.foxnews.com': 'Fox News',
                         'www.breitbart.com': 'Breitbart'
                       }

        self.html_parsing = {
            'New York Times': {
                'articleBody': 'section',
                'identifiers': { 'name': 'articleBody' }
            }
        }

        print('Starting parser...')
        self.parser()

    def load_from_file(self, location) -> list:
        try:
            with open(location, newline='') as keyword_file:
                reader = csv.reader(keyword_file, delimiter=',')
                return list(reader)[0]
        except FileNotFoundError as e:
            sys.exit(f'File {location} not found')

    def parser(self) -> None:
        for article in self.articles:
            try:
                content = self.get_article_content(article)
            except ValueError as e:
                print(f'\nCannot parse article {article}:')
                print(e)
                print("Continuing to parse...\n")

    def get_news_source(self, url) -> str:
        search = re.match(r'https:\/\/(.[^/]+)', url)
        if search and search.groups(0)[0] in self.domains:
            print(f'{url} is from {self.domains[search.groups(0)[0]]}')
            return self.domains[ search.groups(0)[0] ]
        else:
            raise ValueError(f'Cannot find news source for article "{url}". Is the domain listed as a TLD?')

    def get_article_content(self, url) -> str:
        print(f'Parsing {url}...')
        source = self.get_news_source(url)
        with requests.get(url) as article:
            article_content = article.content
            parsed_article = BeautifulSoup(article_content, 'html.parser')

            body = parsed_article.find( self.html_parsing[source]['articleBody'], self.html_parsing[source]['identifiers'] )
            paragraphs = body.find_all('p')

            article_paragraphs = []
            for paragraph in paragraphs:
                p = paragraph.get_text()
                article_paragraphs.append(p)

            return(" ".join(article_paragraphs))

    def get_keywords_frequencies_from_article(self, content) -> int:
        pass






scraper = ArticleScraper()

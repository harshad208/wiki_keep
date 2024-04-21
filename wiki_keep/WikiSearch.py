import requests
from lxml import html


class WikiSearch:
    def __init__(self):
        pass

    def wiki_search_article(self, subject):
        try:
            url = 'https://en.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'titles': subject,
                'prop': 'extracts',
                'explaintext': True,
                'format': 'json',
            }
            response = requests.get(url, params=params)
            data = response.json()

            # Extract the page content
            page = next(iter(data['query']['pages'].values()))

            # Get the full article content
            full_article = page['extract']

            return full_article[:-1]
        except Exception as e:
            print(e)

    def wiki_search_article_ext(self, subject):
        try:
            url = 'https://en.wikipedia.org/w/api.php'
            params = {
                'action': 'parse',
                'format': 'json',
                'page': subject,
                'prop': 'text',
                'redirects': ''
            }

            response = requests.get(url, params=params).json()
            raw_html = response['parse']['text']['*']
            document = html.document_fromstring(raw_html)

            text = ''
            for p in document.xpath('//p'):
                text += p.text_content() + '\n'
            return text
        except Exception as e:
            print(e)
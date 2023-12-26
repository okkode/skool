import re
from bs4 import BeautifulSoup
import urllib.request
import ssl

context = ssl._create_unverified_context()

with open("baleset.html", "r", encoding="utf-8") as html_file:
    html = html_file.read()

parsed_html = BeautifulSoup(html, 'html.parser')
articles = parsed_html.body.find_all('article')


for i in range(20):
    article = articles[i]
    link_element = article.find("h1").find("a")

    # Check if link_element is not None before proceeding
    if link_element:
        article_url = "https://www.police.hu" + link_element.get("href")

        # Fetch the content of the article
        with urllib.request.urlopen(article_url, context=context) as news_item:
            news_bytes = news_item.read()
            news_str = news_bytes.decode("utf-8")

        # Parse the article content with BeautifulSoup
        article_soup = BeautifulSoup(news_str, 'html.parser')
        #print(article_soup)
        # Find the body-text element
        dates = article_soup.find('div', class_='icon-update')
        span_content = dates.find('span').text
        #print(dates)
        # Define a regular expression pattern for matching dates in the format "YYYY. MM. DD."
        date_pattern = re.compile(r'\d{4}\. \d{2}\. \d{2}\.')

        # Find all text in the date that matches the date pattern
        date_matches = re.findall(date_pattern, span_content)
        
        print(date_matches)

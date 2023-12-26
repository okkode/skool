import re
from bs4 import BeautifulSoup
import urllib.request
import ssl
import pymysql
from info import username, passwrd
from datetime import datetime

context = ssl._create_unverified_context()

def get_db():
    conn = pymysql.connect(host='localhost',
                           user=username,
                           password=passwrd,
                           database='police')
    cursor = conn.cursor()
    return conn, cursor

def parse_date(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y. %m. %d.')
    # Format the datetime object as a string in SQL date format
    return date_obj.strftime('%Y-%m-%d')

def scrapper(conn, cursor, page):
    url = f"https://www.police.hu/hu/hirek-es-informaciok/utinfo/baleseti-hirek?field_feltolto_szerv_target_id=All&page={page}"
    with urllib.request.urlopen(url, context=context) as fp:
        mybytes = fp.read()
        mystr = mybytes.decode("utf-8")

    parsed_html = BeautifulSoup(mystr, 'html.parser')
    articles = parsed_html.body.find_all('article')

    for i in range(20):
        article = articles[i]
        link_element = article.find("h1").find("a")

        if link_element:
            article_url = "https://www.police.hu" + link_element.get("href")

            with urllib.request.urlopen(article_url, context=context) as news_item:
                news_bytes = news_item.read()
                news_str = news_bytes.decode("utf-8")

            article_soup = BeautifulSoup(news_str, 'html.parser')
            elements = article_soup.find('div', class_='body-text')
            text_element = elements.text.strip()

            dates = article_soup.find('div', class_='icon-update')
            span_content = dates.find('span').text
            date_pattern = re.compile(r'\d{4}\. \d{2}\. \d{2}\.')
            date_matches = re.findall(date_pattern, span_content)
            
            # Use the parse_date function to convert the date to SQL format
            dates = parse_date(date_matches[0])

            locations = article_soup.find('span', class_='location')
            text_loc = locations.text.strip()
            
            
            print(text_loc)
            print(dates)
            print(text_element)
            print("...")
            
            
            insert_query = "INSERT INTO info (police_location, accident_description, accident_date) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (text_loc, text_element, dates))
            conn.commit()

if __name__ == "__main__":
    conn, cursor = get_db()

    for page in range(0, 501):
        scrapper(conn, cursor, page)

    cursor.close()
    conn.close()

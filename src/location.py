  
import re
from bs4 import BeautifulSoup
import urllib.request
import ssl
import pymysql
from info import passwrd
from info import username
import mysql.connector

context = ssl._create_unverified_context()

with open("baleset.html", "r", encoding="utf-8") as html_file:
    html = html_file.read()

parsed_html = BeautifulSoup(html, 'html.parser')
articles = parsed_html.body.find_all('article')
loc_list = []

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
        locations = article_soup.find('span', class_='location')
        #print(locations)
        text_loc = locations.text.strip()
        #print(text_loc)
        loc_list.append(text_loc)
        #print(loc_list)
print(loc_list)
print(len(loc_list))


"""
conn = pymysql.connect(host ='localhost',
                             user = username,
                             password = passwrd,
                             database = 'police'
                             )



# Create a cursor object to execute SQL queries
cursor = conn.cursor()

insert_query = "INSERT INTO info (police_location) VALUES %r;" % (tuple(loc_list))

for loc_value in (loc_list):
    # Execute the query with the tuple of values
    cursor.execute(insert_query, (loc_value))

conn.commit()
# Close the cursor and conn
cursor.close()
conn.close()

        


    """
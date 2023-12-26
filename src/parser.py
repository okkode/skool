import re
from bs4 import BeautifulSoup
import urllib.request
import ssl
import pymysql
from info import username, passwrd



context = ssl._create_unverified_context()
def get_db():
    conn = pymysql.connect(host ='localhost',
                             user = username,
                             password = passwrd,
                             database = 'police'
                             )
    cursor = conn.cursor()
    return conn, cursor


x = 0
while x <= 20 :
    
    def scrapper(conn, cursor):
        fp = urllib.request.urlopen(f"https://www.police.hu/hu/hirek-es-informaciok/utinfo/baleseti-hirek?field_feltolto_szerv_target_id=All&page={str(x)}", context=context)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        print(mystr)
        with open("r", encoding="utf-8") as html_file:
            html = html_file.read()
        x=+1


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
                elements = article_soup.find('div', class_='body-text')
                #print(elements)
                text_element = elements.text.strip()
                
                        # Parse the article content with BeautifulSoup
                #print(article_soup)
                # Find the body-text element
                dates = article_soup.find('div', class_='icon-update')
                span_content = dates.find('span').text
                #print(dates)
                # Define a regular expression pattern for matching dates in the format "YYYY. MM. DD."
                date_pattern = re.compile(r'\d{4}\. \d{2}\. \d{2}\.')

                # Find all text in the date that matches the date pattern
                date_matches = re.findall(date_pattern, span_content)
                dates = date_matches[0]
                
                        # Parse the article content with BeautifulSoup
                #print(article_soup)
                # Find the body-text element
                locations = article_soup.find('span', class_='location')
                #print(locations)
                text_loc = locations.text.strip()
                
                
                print(text_loc)
                
                print(dates)
                
                print(text_element)


                insert_query = "INSERT INTO info (police_location, accident_description, accident_date) VALUES ('{}', '{}', '{}');".format(text_loc, text_element, dates)
                print(insert_query)
                cursor.execute(insert_query)

                conn.commit()


            
    if __name__ == "__main__":
        conn, cursor = get_db()
        scrapper(conn, cursor)

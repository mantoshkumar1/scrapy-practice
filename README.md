# Scrapy Practice
This project is solely made to practice *Scrapy* (Python web-crawling framework).

#### Prerequisites:
- Python version: 3.8.2
- Pip version: 20.1.1
- OS: Windows 10

#### Install dependencies
```
cd scrapers
pip install -r requirements.txt
```

#### Database setup
ORM of this project is PostgreSQL.
- Please install [PostgreSQL](https://www.postgresql.org/download/).
- Open Windows Command Prompt and create a db named quotes (Database settings are defined in scrapers/settings.py at LN 89).
```
psql -U postgres
password is: psql
create database quotes;
```
Then come to project root directory and execute: 
```
cd scrapers
set PYTHONPATH=.
python database_setup.py
```
This will create and initialize the PostgreSQL database.

#### Execute Scrapy Project
```
cd scrapers
set PYTHONPATH=.
scrapy crawl quotes
```

#### Project Details (Developer's Note):
The quote information is defined by two models (or tables):
###### Author
The Author model contains basic author information:
- Name `Albert Einstein`
- URL of Author Page `http://quotes.toscrape.com/author/Albert-Einstein`

###### Quotes
The Quotes model contains the attributes of an author. There is one-to-many relation between Author and Quotes tables.
- Content (Quote Text) `“The world as we have created it is a process of our thinking.”`
- Tags of Content `change, deep-thoughts, thinking, world`

###### Developer Note
Many websites does not allow to render its web pages if our browser does not support Javascript. There are multiple wayarounds.   
1. We can fool the website to believe that we support JS and once that is done, the website will send us the response with the 
information we need to scrape. To do it, We can make our Scrapy request more like our browser's request including cookies in our requests. It is implemented. You only need to fill the cookies in scrapers/spiders/quotes_spider.py (LN 57).
2. We can use Selenium/Splash/Chrome Driver. It is not implemented. 

#### Possible Enhancements
Reference: [How to scrape websites without getting blocked](https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/)
1. Do not follow the same crawling pattern. Implement few random actions that will make a spider look like a human.
2. Make Anonymous Requests using TorRequests. Through this, it is possible to get a different IP address for each request.
3. Rotate User Agents and corresponding HTTP Request Headers between requests.
4. Use a headless browser like Puppeteer, Selenium or Playwright
5. When following links always take care that the link has proper visibility with no nofollow tag. Some honeypot links to detect spiders will have the CSS style display:none or will be color disguised to blend in with the page’s background color.

References:
1. [Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)
2. http://newcoder.io/scrape/part-0/
3. [How To Crawl A Web Page with Scrapy and Python 3
](https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3)
4. [Scrape an ecommerce dataset with Scrapy, step-by-step](https://medium.com/@tobritton/scrape-an-ecommerce-dataset-with-scrapy-from-start-to-finish-b31540df9bfa)
5. [How to scrape websites without getting blocked](https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/)
6. [Store Scrapy crawled data in PostgresSQL
](https://medium.com/codelog/store-scrapy-crawled-data-in-postgressql-2da9e62ae272)


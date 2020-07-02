import scrapy
from scrapers.items import AuthorQuoteItem


class QuotesSpider(scrapy.Spider):
    # name: identifies the Spider. It must be unique within a project, that is,
    # you can’t set the same name for different Spiders.
    name = "quotes"
    allowed_domains = [
        'quotes.toscrape.com',
    ]
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def __init__(self):
        self._declare_xpath()

    def _declare_xpath(self):
        self.quote_blocks_xpath = "//div[@class='quote']"
        self.author_xpath = "span/small[@class='author']/text()"
        self.author_url_xpath = "span[2]/a/@href"
        self.content_xpath = "span[@class='text']/text()"
        self.tags_xpath = "div[@class='tags']/a[@class='tag']/text()"
        self.next_page_xpath = "//li[@class='next']/a/@href"

    def request(self, url, callback):
        """Wrapper for scrapy.request
         :parameter
         url (str): URL of start url
         callback (func): callback function
         :returns
         Request object which is used to represent HTTP requests in Scrapy
        """
        # copied from browser network details
        chrome_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'quotes.toscrape.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        }
        request = scrapy.Request(
            url=url, callback=callback, dont_filter=True, headers=chrome_headers
        )

        # Some website needs our browser to be JS-capable. We can fool it to
        # believe we do support JS and then the website will send you the
        # response with the information we need to scrape. To do it, try to
        # make our Scrapy request more like your browser's request. i.e.:
        # cookies. Other ways to achieve is using advanced web-application
        # frameworks such as Selenium/Splash/Chrome Driver.
        # Update Cookies in scrapy.Request.
        # request.cookies.update({})

        return request

    def start_requests(self):
        """start_requests(): must return an iterable of Requests (you can return
        a list of requests or write a generator function) which the Spider will
        begin to crawl from. Subsequent requests will be generated successively
        from these initial requests.
        """
        for url in self.start_urls:
            yield self.request(url=url, callback=self.parse)

    def parse(self, response):
        """parse(): a method that will be called to handle the response
        downloaded for each of the requests made. The response parameter is an
        instance of TextResponse that holds the page content and has further
        helpful methods to handle it.

        The parse() method usually parses the response, extracting the scraped
        data as dicts and also finding new URLs to follow and creating new
        requests (Request) from them.
        """
        text_block = response.xpath(self.quote_blocks_xpath)
        for text in text_block:
            yield self.parse_single_quote_block(response, text)

        # Pagination
        # '/page/2/'

        next_page = response.xpath(self.next_page_xpath).extract()
        if not next_page:
            # Last page will not have 'Next' button
            next_page = next_page[0]
        try:
            next_page_url = response.urljoin(next_page)
        except Exception:
            print(f"Mantosh: {next_page}")
            return None

        try:
            yield self.request(url=next_page_url, callback=self.parse)
        except Exception as e:
            self.logger.error(f"Error: {next_page_url} could not parsed with error: {str(e)}")

    def parse_single_quote_block(self, response, text):
        item = AuthorQuoteItem()
        # Author Xpaths
        author_name = text.xpath(self.author_xpath).extract()[0]
        item['name'] = author_name

        # "/author/Albert-Einstein"
        author_url = text.xpath(self.author_url_xpath).extract()[0]
        author_url = response.urljoin(author_url)
        item['author_url'] = author_url

        # '“It is our choices, Harry.”'
        content = text.xpath(self.content_xpath).extract()[0]
        item['content'] = content

        # ['change', 'deep-thoughts', 'thinking', 'world']
        tags = text.xpath(self.tags_xpath).extract()
        tags = ", ".join(tags)
        item['tags'] = tags
        return item

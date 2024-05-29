import requests
import re
from bs4 import BeautifulSoup
from classes.listing import Listing
import scrapy
from scrapy.crawler import CrawlerProcess
import warnings
import logging

# warn_msg = "Unverified HTTPS request is being made to host 'www.subito.it'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings"
# warnings.filterwarnings("ignore", message=warn_msg)
# logging.getLogger("requests").setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)

class PageNoSpider(scrapy.Spider):
    def __init__(self, url):
        self.url = url
    name = "page_no"
    total_pages = 0

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        html_content = response.text

        # Find total number of result pages
        match = re.search(r'"totalPages":(\d+)', html_content)
        if match:
            self.total_pages = int(match.group(1))
            self.log(f"Total pages found: {self.total_pages}")
        else:
            self.log("Pattern not found in the HTML content.")

        return self.total_pages

class BrowseSpider(scrapy.Spider):
    def __init__(self, url):
        self.url = url
    name = "browse"
    listings = []
    
    def parse(self, response):
        # Loop to paginate through the first 10 pages
        for page in range(10):
            page_no = f"&o{page}"
            next_page = response.urljoin(page_no)
            item = self.parse_page(next_page)
            self.listings.append(item)
        return self.listings

    def parse_page(self, response):
        class_name = "SmallCard-module_card__3hfzu items__item item-card item-card--small"
        elements = response.css(f'.{class_name}')
        
        for element in elements:
            link = element.css('a::attr(href)').get()
            title = element.css('.index-module_sbt-text-atom__ed5J9.index-module_token-h6__FGmXw.size-normal.index-module_weight-semibold__MWtJJ.ItemTitle-module_item-title__VuKDo.SmallCard-module_item-title__1y5U3::text').get()
            price = element.css('.index-module_price__N7M2x.SmallCard-module_price__yERv7.index-module_small__4SyUf::text').get(default='n/a')
            img = element.css('img::attr(src)').get()
            desc = get_desc()
            
            item = Listing(link, title, price, desc, img)
            
            yield item
        

def get_page_no(url): 
    process = CrawlerProcess()
    process.crawl(PageNoSpider, url)
    process.start() 
    PageNoSpider.start_requests() 
    return int(PageNoSpider.total_pages)

def browse(url, n_pages):
    process = CrawlerProcess()
    process.crawl(BrowseSpider, url)
    process.start()  
    BrowseSpider.parse()
    return BrowseSpider.listings

def get_desc(link):
    response = requests.get(link,verify=False)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    soup = BeautifulSoup(html_content, 'html.parser')
    desc = (soup.find(class_="index-module_sbt-text-atom__ed5J9 index-module_token-body__GXE1P size-normal index-module_weight-book__WdOfA AdDescription_description__gUbvH index-module_preserve-new-lines__ZOcGy")).get_text()
    return desc
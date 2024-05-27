import requests
import re
from bs4 import BeautifulSoup
from classes.listing import Listing

def get_page_no(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    ## Find total number of result pages
    match = re.search(r'"totalPages":(\d+)', html_content)
    if match:
        total_pages = match.group(1)
    else:
        print("Pattern not found in the HTML content.")
    
    return int(total_pages)


def browse(url, n_pages):
    all_results = ""
    
    #for page in range(int(total_pages)):
    for page in range(10):
        page_no = "&o" + str(n_pages)
        response = requests.get(url+page_no)
        all_results += response.text

    soup = BeautifulSoup(all_results, 'html.parser')

    listings = []
    # Find all search results by class name
    class_name = "SmallCard-module_card__3hfzu items__item item-card item-card--small"
    elements = soup.find_all(class_=class_name)

    for element in elements:
        link    = element.find("a")["href"]
        title   = (element.find(class_="index-module_sbt-text-atom__ed5J9 index-module_token-h6__FGmXw size-normal index-module_weight-semibold__MWtJJ ItemTitle-module_item-title__VuKDo SmallCard-module_item-title__1y5U3")).get_text()
        price   = (element.find(class_="index-module_price__N7M2x SmallCard-module_price__yERv7 index-module_small__4SyUf")).get_text()
        descr   = get_desc(link)
        img     = element.find("img")["src"]
        lis = Listing(link, title, price, descr, img)
        listings.append(lis)

    return listings

def get_desc(link):
    response = requests.get(link)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    soup = BeautifulSoup(html_content, 'html.parser')
    desc = (soup.find(class_="index-module_sbt-text-atom__ed5J9 index-module_token-body__GXE1P size-normal index-module_weight-book__WdOfA AdDescription_description__gUbvH index-module_preserve-new-lines__ZOcGy")).get_text()
    return desc
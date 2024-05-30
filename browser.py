import requests
import re
import lxml
from lxml import etree
from classes.listing import Listing

def get_page_no(url):
    response = requests.get(url,verify=False)

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
        response = requests.get(url+page_no,verify=False)
        all_results += response.text

    parser = etree.HTMLParser()
    tree = etree.fromstring(all_results, parser)

    listings = []
    # Find all search results by class name
    class_name = 'SmallCard-module_card__3hfzu items__item item-card item-card--small'
    elements = tree.xpath("//*[@class='"+class_name+"']")

    for element in elements:
        link    = element.find(".//a").get("href")
        class_name = "index-module_sbt-text-atom__ed5J9 index-module_token-h6__FGmXw size-normal index-module_weight-semibold__MWtJJ ItemTitle-module_item-title__VuKDo SmallCard-module_item-title__1y5U3"
        title   = element.find(".//*[@class='"+class_name+"']").text
        try:
            class_name = "index-module_price__N7M2x SmallCard-module_price__yERv7 index-module_small__4SyUf"
            price   = element.find(".//*[@class='"+class_name+"']").text
        except:
            price = "n/a"
        descr   = get_desc(link)
        img     = element.find(".//img").get("src")
        lis = Listing(link, title, price, descr, img)
        listings.append(lis)

    return listings

def get_desc(link):
    response = requests.get(link,verify=False)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    parser = etree.HTMLParser()
    tree = etree.fromstring(html_content, parser)
    class_name = "index-module_sbt-text-atom__ed5J9 index-module_token-body__GXE1P size-normal index-module_weight-book__WdOfA AdDescription_description__gUbvH index-module_preserve-new-lines__ZOcGy"
    desc = tree.find(".//*[@class='"+class_name+"']").text
    return desc
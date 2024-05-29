import browser

def fai_le_cose():
    base_url = 'https://www.subito.it/'
    location = 'annunci-lombardia/vendita/usato/milano/milano/'
    query = '?q=seiko'
    order = '&order=priceasc'

    # url = base_url + location + query + order
    url = base_url + location + query

    page_no = browser.get_page_no(url)

    listings = browser.browse(url, 1)
    return listings
    # print(listings[0])



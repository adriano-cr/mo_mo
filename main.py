import browser

def fai_le_cose():
    base_url = 'https://www.subito.it/'
    location = 'annunci-lombardia/vendita/usato/milano/milano/'
    query = '?q=tappeto'
    order = '&order=priceasc'

    url = base_url + location + query + order

    page_no = browser.get_page_no(url)

    listings = browser.browse(url, 1)
    return listings[0]
    # print(listings[0])



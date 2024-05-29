import browser
import asyncio

async def fai_le_cose():
    base_url = 'https://www.subito.it/'
    location = 'annunci-lombardia/vendita/usato/milano/milano/'
    query = '?q=seiko'
    order = '&order=priceasc'

    # url = base_url + location + query + order
    url = base_url + location + query

    page_no = browser.get_page_no(url)

    listings = await browser.browse(url, 1)
    return listings
    # print(listings[0])
    
if __name__ == "__fai_le_cose__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fai_le_cose())



from ikman_scraper import IkmanScraper
from ikman_persist import IkmanPersist

# Configurable options (Ideally fed through a json file)
MAX_PAGES = 100  # max pages that can be scrapped. Set to prevent infinite loops
PAGE_NO = 1  # Start page number from where to scrape
QUERY = 'Picanto'  # search string


def unit_test():
    scarper = IkmanScraper()  # Instantiate the scarper class for operations
    page_no = PAGE_NO
    query = QUERY

    output = IkmanPersist()
    while page_no <= MAX_PAGES:
        print(f'-------------------Scraping page = {page_no} -------------------')
        url = f'https://ikman.lk/en/ads?by_paying_member=0&sort=relevance&buy_now=0&query={query}&page={page_no}'

        status = scarper.scrape(url, output)

        if not status:
            break
        page_no += 1

    output.save()

unit_test()

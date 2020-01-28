from bs4 import BeautifulSoup
import requests
from ikman_logger import getlog
from ikman_tag import IkmanTag


class IkmanScraper(object):
    me = None

    def __new__(cls):  # Make this a singleton
        if cls.me is None:
            cls.me = super(IkmanScraper, cls).__new__(cls)
        return cls.me

    def download(self, url):
        try:
            source = requests.get(url).text
            html = BeautifulSoup(source, 'lxml')
        except Exception as e:
            getlog().critical(e)
            html = None
        return html

    def scrape(self, url, output):

        html = self.download(url)
        if html is None:
            return False

        # The pagination 'Next' disable is injected through javascript using the CSS class "a.disabled--qTbQf".
        # Therefore bs4 cannot parse this currently. We need to install the correct version of google webdriver
        # (or splash) on the system to use selenium to parse the document. Since this is a short task, a
        # simplified approach of navigating beyond the end of the pagination list and looking for
        # 'div.no-result-text--16bWr' is used to terminate the search.
        try:
            is_end = html.find('div', 'no-result-text--16bWr')
            if is_end is not None:
                return False

            for liTag in html.find_all('li', ['normal--2QYVk gtm-normal-ad', 'top-ads-container--1Jeoq gtm-top-ad']):

                output.new()
                title = IkmanTag(liTag).find_tag('span', 'title--3yncE')
                output.set_title(title.text)

                price = IkmanTag(liTag).find_tag('div', 'price--3SnqI color--t0tGX')
                price = IkmanTag(price.tag.span)
                output.set_price(price.text)

                category = IkmanTag(liTag).find_tag('div', 'description--2-ez3')
                if category.tag is not None:
                    category.text = category.text.split(',')[1].strip()
                output.set_category(category.text)

                url = IkmanTag(liTag).find_tag('a', 'card-link--3ssYv')
                if url.tag is not None:
                    url.text = f"https://ikman.lk{url.tag['href']}"
                output.set_url(url.text)

                inner_html = self.download(url.text)
                if inner_html is None:
                    continue

                ad_date = IkmanTag(inner_html).find_tag('p', 'item-intro').find_tag('span', 'date')
                output.set_date(ad_date.text)

                contacts = IkmanTag(inner_html).find_tag('div', 'item-contact-more is-showable')
                if contacts.tag is None:
                    output.set_contact(contacts.text)
                else:
                    for contact in contacts.tag.find_all('span', 'h3'):
                        contact = IkmanTag(contact)
                        output.set_contact(contact.text)

                descriptions = IkmanTag(inner_html).find_tag('div', 'item-description')
                if descriptions.tag is None:
                    output.set_description(descriptions.text)
                else:
                    description = ''
                    for des in descriptions.tag.find_all('p'):
                        des = IkmanTag(des)
                        description = description + des.text
                    output.set_description(description)

                galleries = IkmanTag(inner_html).find_tag('div', 'gallery-items')
                if galleries.tag is None:
                    output.set_image(galleries.text)
                else:
                    for gal in galleries.tag.find_all('div', 'gallery-item'):
                        gal = IkmanTag(gal).find_tag('img')
                        if gal.tag is not None:
                            gal.text = gal.tag['data-srcset']
                            arr = gal.text.split(',')
                            img1 = arr[0].strip().split(' ')
                            img2 = arr[1].strip().split(' ')
                            output.set_image(f"https:{img1[0]}")
                            output.set_image(f"https:{img2[0]}")

                output.add()
            return True

        except Exception as e:
            getlog().critical(e)
            return False

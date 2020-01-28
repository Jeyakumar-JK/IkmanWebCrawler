import json
from ikman_logger import getlog


class IkmanPersist(object):

    me = None

    def __new__(cls):  # Make this a singleton
        if cls.me is None:
            cls.me = super(IkmanPersist, cls).__new__(cls)
        return cls.me

    def __init__(self):
        self.cache = None
        self.base = []
        try:
            self.json_file = open('output.json', 'w', encoding="utf-8")

        except Exception as e:
            getlog().critical(e)

    def new(self):
        self.cache = dict()
        self.cache['contacts'] = []
        self.cache['details'] = {'description': '', 'image_urls': []}

    def save(self):
        try:
            json.dump(self.base, self.json_file, indent=4, sort_keys=True)
            self.json_file.close()
        except Exception as e:
            getlog().critical(e)

    def add(self):
        self.base.append(self.cache)
        print(json.dumps(self.cache, indent=4, sort_keys=True))

    def set_title(self, title):
        self.cache['title'] = title

    def set_date(self, date):
        self.cache['date'] = date

    def set_category(self, category):
        self.cache['category'] = category

    def set_url(self, url):
        self.cache['url'] = url

    def set_price(self, price):
        self.cache['price'] = price

    def set_contact(self, contact):
        self.cache['contacts'].append(contact)

    def set_description(self, description):
        self.cache['details']['description'] = description

    def set_image(self, image):
        self.cache['details']['image_urls'].append(image)

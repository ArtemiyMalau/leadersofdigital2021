import itertools

from bs4 import BeautifulSoup

from ..db.models import ContactType
from .parserBase import Parser


class OptunionParser(Parser):
    def __init__(self):
        super().__init__()

        self.SITE_ROOT = "https://www.opt-union.ru"


    def parse_listing(self, url):
        companies = set()

        for page in itertools.count(start=1):
            previous_len = len(companies)

            resp = self.sess.get(url, params={"page": page})
            with open("result.html", "w", encoding="utf8") as file:
                file.write(resp.text)

            soup = BeautifulSoup(resp.text, "lxml")

            divs = soup.find_all("div", attrs={"class": "data-block bordered"})

            try:
                companies.update([div.find_all("a")[0].get("href") for div in divs[1:]])

            # Page change layout
            except AttributeError:
                print("Change layout")
                break

            if previous_len == len(companies):
                break

        return list(map(lambda company: self.SITE_ROOT + company, companies))


    def parse_vendor(self, url):
        resp = self.sess.get(url)

        soup = BeautifulSoup(resp.text, "lxml")

        try:
            # Getting name and drop extra substrings
            name = soup.find("h1").text.removesuffix(" - о компании").removesuffix(" - список товаров")

            # Getting company's description
            description = soup.find("div", attrs={"class": "data-block"}).text.strip()

            # Trying to get multiply phone numbers
            country = self.__find_by_property_name(soup, "Страна")
            city = self.__find_by_property_name(soup, "Город")
            address = self.__find_by_property_name(soup, "Адрес")

            contacts = {}
            phones = self.__find_by_property_name(soup, "Телефон")
            if phones: 
                contacts[ContactType.PHONE] = phones.split(",")
            website = self.__find_by_property_name(soup, "Интернет")
            if website: 
                contacts[ContactType.WEBSITE] = [website]

            return {
                "url": url,
                "name": name,
                "description": description,
                "country": country,
                "city": city,
                "address": address,
                "contacts": contacts,
            }
        except AttributeError as e:
            return None


    def parse_vendors(self, url):
        vendor_urls = self.parse_listing(url)
        vendors = list(map(self.parse_vendor, vendor_urls))

        return vendors


    @staticmethod
    def __find_by_property_name(soup, property_name):
        property_tag = soup.find("div", attrs={"class": "itemLeft"}, string=property_name)
        if property_tag:
            value = property_tag.findNext("div", attrs={"class": "itemRight"}).text

            return value
        else:
            return None
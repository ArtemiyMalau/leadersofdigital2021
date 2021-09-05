import re
import time
from pprint import pprint

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .parserBase import Parser


class MinpromtorgParser(Parser):
    def __init__(self):
        self.LISTING_URL = "https://gisp.gov.ru/pp719v2/pub/prod/"
        self.LONG_TIMEOUT = 5

        self.TITLED_FIELD_FORMATTERS = {
            "Полное наименование предприятия": ("name", None),
            "ФИО ответственного лица": ("responsible_person", None),
            "ОГРН": ("ogrn", None),
            "ИНН": ("inn", None),
            "КПП": ("kpp", None),
            "Страна": ("country", None),
            "Регион": ("region", None),
            "Город": ("city", None),
            "Адрес": ("address", None),
            "Телефон": ("phone", None),
            "E-mail": ("email", None),
            "www": ("website", None),
            "ОКВЭД": ("okveds", lambda okved_str: list(map(str.strip, okved_str.split(",")))),
            "ОКВЭД 2": ("okveds_2", lambda okved_str: list(map(str.strip, okved_str.split(",")))),
            "Отрасль из справочника отраслей ГИСП:": ("gisp", None),
        }

        super().__init__()

    def parse_listing(self, start_page, end_page):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(2)

        driver.get(self.LISTING_URL)
        WebDriverWait(driver, self.LONG_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='dx-pages']")))

        vendors = set()

        try:
            if start_page > 1:
                for page in range(1, start_page):
                    new_page = driver.find_element_by_xpath(f"//div[@class='dx-pages']/div[text()='{page + 1}']")
                    new_page.click()
                    time.sleep(1)

            for page in range(start_page, end_page):
                html = driver.page_source.encode("utf8")

                soup = BeautifulSoup(html, "lxml")
                trs = soup.find("body").find_all("tr", attrs={"class": "dx-row dx-data-row dx-column-lines"})
                for tr in trs:
                    td = tr.find_all("td")[-1]
                    a = td.find_all("a")[0]

                    vendor_url = a.get("href")
                    if vendor_url is not None:
                        vendors.add(vendor_url)

                for _ in range(5):
                    try:
                        new_page = driver.find_element_by_xpath(f"//div[@class='dx-pages']/div[text()='{page + 1}']")
                        new_page.click()
                    except Exception as e:
                        time.sleep(1)
                    else:
                        break
                time.sleep(1)


        except Exception as e:
            with open("html.html", "w", encoding="utf8") as file:
                file.write(html.decode("utf8"))
            raise Exception from e
        finally:
            pass
        # driver.quit()

        return list(vendors)

    def parse_vendor(self, url):
        resp = self.sess.get(url)

        soup = BeautifulSoup(resp.text, "lxml")

        vendor = dict()

        main_tag, specialization_tag, contact_tag = soup.find("div", attrs={"class": "content__main_1"}).find_all(
            "fieldset")

        for fieldset_tag in [main_tag, specialization_tag, contact_tag]:
            for field_tag in fieldset_tag.find("div").find_all("p"):
                title, value = field_tag.text.split(":", 1)

                if title in self.TITLED_FIELD_FORMATTERS:
                    key, func = self.TITLED_FIELD_FORMATTERS[title]

                    value = re.sub(r'\s+', ' ', value).strip()
                    value = func(value) if func else value

                    vendor[key] = value

        vendor["rate"] = main_tag.select("span.raitig.text,span.value")[-1].text
        pprint(vendor)
        return vendor

    def parse_vendors(self, start_page, end_page):
        vendor_urls = self.parse_listing(start_page, end_page)
        print(vendor_urls)
        vendors = list(map(self.parse_vendor, vendor_urls))

        return vendors

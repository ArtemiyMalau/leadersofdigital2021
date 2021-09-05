import itertools

from .parserBase import Parser
from ..db.models import ContactType


class YandexParser(Parser):
    def __init__(self, API_KEY):
        super().__init__()

        self.API_URL = "https://search-maps.yandex.ru/v1"
        self.RESULTS_PER_REQUEST = 100

        self.API_KEY = API_KEY

        self.params = {
            "apikey": self.API_KEY,

            "text": None,

            "lang": "ru_RU",
            "type": "biz",

            "results": self.RESULTS_PER_REQUEST
        }

    def parse_vendors(self, vendor_name):
        self.params["text"] = vendor_name

        vendors = []
        for skip in itertools.count(start=0, step=self.RESULTS_PER_REQUEST):
            self.params["skip"] = skip

            resp = self.sess.get(self.API_URL, params=self.params)

            vendors_resp = resp.json()

            for vendor in vendors_resp["features"]:
                contacts = {}
                if "url" in vendor["properties"]["CompanyMetaData"]:
                    contacts[ContactType.WEBSITE] = [vendor["properties"]["CompanyMetaData"]["url"]]
                if "Phones" in vendor["properties"]["CompanyMetaData"]:
                    contacts[ContactType.PHONE] = list(
                        map(
                            lambda phone_item: phone_item["formatted"],
                            filter(lambda phone_item: phone_item["type"] == "phone",
                                   vendor["properties"]["CompanyMetaData"]["Phones"])
                        )
                    )

                category = next(
                    filter(
                        lambda category: category["class"] == "office service",
                        vendor["properties"]["CompanyMetaData"]["Categories"]
                    )
                )["name"]

                country, city, _ = vendor["properties"]["CompanyMetaData"]["address"].split(",", maxsplit=2)

                vendors.append({
                    "name": vendor["properties"]["name"],
                    "country": country.strip(),
                    "city": city.strip(),
                    "address": vendor["properties"]["CompanyMetaData"]["address"],
                    "category": category,
                    "contacts": contacts,
                })

            if vendors_resp["properties"]["ResponseMetaData"]["SearchResponse"][
                "found"] <= skip + self.RESULTS_PER_REQUEST:
                break

        return vendors

from datetime import datetime

from .parserBase import Parser


class CheckoParser(Parser):
    def __init__(self, API_KEY):
        super().__init__()

        self.API_URL = "https://api.checko.ru/json"

        self.API_KEY = API_KEY

    def parse_organization(self, *, ogrn=None, inn=None, kpp=None):
        resp = self.sess.get(self.API_URL, params={
            "object": "organization",
            "key": self.API_KEY,
            "ogrn": ogrn,
            "inn": inn,
            "kpp": kpp,
        }).json()

        self.__check_valid_key(resp)

        organization = resp["data"]

        vendor = dict()

        vendor["is_unfair_supplier"] = organization.get("is_unfair_supplier", None)

        try:
            if organization["capital"]["type"] == "УСТАВНЫЙ КАПИТАЛ":
                vendor["authorized_capital"] = organization["capital"]["amount"]
            else:
                vendor["authorized_capital"] = None
        except KeyError:
            vendor["authorized_capital"] = None

        vendor["licenses"] = organization.get("licenses", [])
        vendor["reg_data"] = datetime.strptime(organization["reg_date"], "%Y-%m-%d").timestamp()

        if "okved_extra" in organization:
            vendor["okveds"] = [okved["code"] for okved in organization["okved_extra"] if okved["version"] == 2001]
            vendor["okveds_2"] = [okved["code"] for okved in organization["okved_extra"] if okved["version"] == 2014]

        if organization["okved"]["version"] == 2001:
            vendor["okveds"].append(organization["okved"]["code"])
        elif organization["okved"]["version"] == 2014:
            vendor["okveds_2"].append(organization["okved"]["code"])

        return vendor

    def parse_finances(self, *, ogrn=None, inn=None, kpp=None):
        # http://www.consultant.ru/document/cons_doc_LAW_103394/b990bf4a13bd23fda86e0bba50c462a174c0d123/
        resp = self.sess.get(self.API_URL, params={
            "object": "finances",
            "key": self.API_KEY,
            "ogrn": ogrn,
            "inn": inn,
            "kpp": kpp,
        }).json()

        self.__check_valid_key(resp)

        vendor = list()

        finances = resp["data"]["accounting"]

        for year, fields in finances.items():
            year_finances = {
                "year": year,
                # 2110 - Выручка
                "f_2110": fields.get("2110", None),
                # 2200 - Прибыль (убыток) от продаж
                "f_2200": fields.get("2200", None),
                # 2100 - Валовая прибыль (убыток)
                "f_2100": fields.get("2100", None),
                # 2300 - Прибыль (убыток) до налогообложения
                "f_2300": fields.get("2300", None),
                # 2400 - Чистая прибыль (убыток)
                "f_2400": fields.get("2400", None),
            }

            vendor.append(year_finances)

        return vendor

    def __check_valid_key(self, resp):
        if resp["meta"]["status"] == "ok":
            return
        elif resp["meta"]["status"] == "error":
            raise ValueError(F"Error with {self.API_KEY} API key\nReason: {resp['meta']['message']}")

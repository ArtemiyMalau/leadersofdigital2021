import csv
import re
import requests

from bs4 import BeautifulSoup
from io import StringIO
from sqlalchemy import func

from ..db.models import Country, City, Okved, OkvedSection


def import_countries(session):
	URL = "https://www.artlebedev.ru/country-list/tab/"

	resp = requests.get(URL)

	countries = csv.DictReader(StringIO(resp.text), delimiter="\t")

	for country in countries:
		session.add(Country(name=country["name"], alpha2=country["alpha2"], alpha3=country["alpha3"]))
	session.commit()


# dummy, works only with city.csv file and Russia's cities
def import_cities(session, country_name):
	country = session.query(Country).filter(func.lower(Country.name) == func.lower(country_name)).first()

	with open("./py/helpers/city.csv", "r", encoding="utf8") as file:
		cities = csv.DictReader(file, delimiter=";")

		for city in filter(lambda city: int(city["country_id"]) == 3159, cities):
			session.add(City(country_id=country.id, name=city["name"]))
	session.commit()


def formatting_okved(session):
	for okved in session.query(Okved).all():
		if okved.name.startswith("Код ОКВЭД "):
			okved.name = okved.name.removeprefix("Код ОКВЭД ")

		format_name = None

		if okved.level == 1:
			format_code = re.search(r"^(\d{2})", okved.name)
			okved.code = format_code.group(1)

			format_name = re.search(r"^(\d{2})(\s*[-—-]\s*)(.*)", okved.name)

		elif okved.level == 2:
			format_code = re.search(r"^(\d{2}\.\d)", okved.name)
			okved.code = format_code.group(1)

			format_name = re.search(r"^(\d{2}\.\d)(\s*[-—-]\s*)(.*)", okved.name)

		elif okved.level == 3:
			format_code = re.search(r"^(\d{2}\.\d{2})", okved.name)
			okved.code = format_code.group(1)

			format_name = re.search(r"^(\d{2}\.\d{2})(\s*[-—-]\s*)(.*)", okved.name)

		elif okved.level == 4:
			format_code = re.search(r"^(\d{2}\.\d{2}\.\d{1,2})", okved.name)
			okved.code = format_code.group(1)

			format_name = re.search(r"^(\d{2}\.\d{2}\.\d{1,2})(\s*[-—-]\s*)(.*)", okved.name)

		if format_name:
			okved.name = f"{format_name.group(1)} {format_name.group(3)}"
			
	session.commit()


def import_okved(session):
	URL = "https://okved.online/"

	resp = requests.get(URL)
	soup = BeautifulSoup(resp.text, "lxml")

	# Inserting okved sections
	okved_sections = []
	for section_tag in soup.find_all("a", attrs={"class": "rank-math-link"}):
		result = re.search(r"Раздел (.+): (.+)", section_tag.text)

		okved_section = OkvedSection(code=result.group(1), name=result.group(2))
		okved_sections.append((okved_section, section_tag.get("href")))
		session.add(okved_section)

	session.flush()

	# Inserting first level okveds
	okveds_1 = []
	for okved_section, url in okved_sections:
		resp = requests.get(url)
		soup = BeautifulSoup(resp.text, "lxml")

		for okved_tag in soup.select("article.post-page a"):
			spans = okved_tag.find_all("span")

			okved_1 = Okved(
				okved_section_id=okved_section.id,
				level=1,
				name=f"{spans[0].text.strip()} {spans[1].text.strip()}"
				)
			okveds_1.append((okved_1, okved_tag.get("href")))
			print(okved_1)
			session.add(okved_1)

	session.flush()

	# Inserting second, third, fourth levels okveds
	for okved_1, url in okveds_1:
		resp = requests.get(url)
		soup = BeautifulSoup(resp.text, "lxml")

		for okved_2_tag in soup.find_all("div", attrs={"class": "okved-listg"}):
			okved_2_name = okved_2_tag.find_next("span", attrs={"class": "name"}).text.strip()

			okved_2 = Okved(
				okved_section_id=okved_1.okved_section_id,
				parent_okved_id=okved_1.id,
				level=2,
				name=okved_2_name
				)
			print(okved_2)
			session.add(okved_2)
			session.flush()


			okved_3 = None
			for okved_34_tag in okved_2_tag.find_all("div", attrs={"class": ["okved-row"]}):
				code = okved_34_tag.find("div", attrs={"class": "number"}).text.strip()
				name = okved_34_tag.find("div", attrs={"class": "after-number flex"}).find_next("span").text.strip()

				if code.count(".") == 1 or code.endswith("."):
					okved_3 = Okved(
						okved_section_id=okved_1.okved_section_id,
						parent_okved_id=okved_2.id,
						level=3,
						name=f"{code} - {name}"
						)
					print(okved_3)
					session.add(okved_3)
					session.flush()
				else:
					okved_4 = Okved(
						okved_section_id=okved_1.okved_section_id,
						parent_okved_id=okved_3.id,
						level=4,
						name=f"{code} - {name}"
						)
					print(okved_4)
					session.add(okved_4)
			session.flush()

	session.commit()

	formatting_okved(session)
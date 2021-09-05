from .models import City, Country, Contact, Vendor, Gisp, ContactType, Okved2, Okved2Vendor, VendorFinances

__all__ = [
    "export_minpromtorg_vendor_to_db",
    "export_checko_vendor_finances_to_db",
    "export_checko_vendor_to_db",
]


def export_minpromtorg_vendor_to_db(session, vendor_data):
    vendor_dict = {
        "ogrn": vendor_data.get("ogrn", None),
        "inn": vendor_data.get("inn", None),
        "kpp": vendor_data.get("kpp", None),
        "name": vendor_data.get("name", None),
        "responsible_person": vendor_data.get("responsible_person", None),
        "address": vendor_data.get("address", None),
        "email": vendor_data.get("email", None),
        "website": vendor_data.get("website", None),
        "phone": vendor_data.get("phone", None),
        "rate_minpromtorg": vendor_data.get("rate", None),
    }

    if all(data in vendor_data for data in ["city", "country"]):
        city = session.query(City).filter(
            City.name == vendor_data["city"],
            Country.name == vendor_data["country"],
            City.country_id == Country.id
        ).first()
    else:
        city = None
    vendor_dict["city_id"] = city.id if city else None

    if "gisp" in vendor_data:
        gisp = Gisp.get_or_create(session, vendor_data["gisp"])
    else:
        gisp = None
    vendor_dict["gisp_id"] = gisp.id if gisp else None

    vendor = Vendor(**vendor_dict)
    session.add(vendor)
    session.flush()

    if "okveds_2" in vendor_data:
        for okved_name in vendor_data["okveds_2"]:
            okved2 = session.query(Okved2).filter(Okved2.name == okved_name).first()
            if okved2:
                session.add(Okved2Vendor(vendor_id=vendor.id, okved_id=okved2.id))

    if vendor_dict["email"]:
        session.add(Contact(vendor_id=vendor.id, type=ContactType.EMAIL, value=vendor_dict["email"]))
    if vendor_dict["website"]:
        session.add(Contact(vendor_id=vendor.id, type=ContactType.WEBSITE, value=vendor_dict["website"]))
    if vendor_dict["phone"]:
        session.add(Contact(vendor_id=vendor.id, type=ContactType.PHONE, value=vendor_dict["phone"]))


def export_checko_vendor_finances_to_db(session, vendor_id, vendor_finances):
    vendor = session.query(VendorFinances).filter(VendorFinances.vendor_id == vendor_id).first()


    for finance in vendor_finances:
        session.add(VendorFinances(vendor_id=vendor_id, **finance))

    session.commit()


def export_checko_vendor_to_db(session, vendor_id, vendor_data):
    vendor = session.query(Vendor).filter(Vendor.id == vendor_id).first()

    vendor.is_unfair_supplier = vendor_data["is_unfair_supplier"]
    vendor.authorized_capital = vendor_data["authorized_capital"]
    vendor.reg_data = vendor_data["reg_data"]

    if "okveds_2" in vendor_data:
        for okved_name in vendor_data["okveds_2"]:
            okved2 = session.query(Okved2).filter(Okved2.name == okved_name).first()
            if okved2:
                session.add(Okved2Vendor(vendor_id=vendor.id, okved_id=okved2.id))

    session.commit()


def parse_vendors_from_minpromtorg_checko(minpromtorg_diapason):
	parser = MinpromtorgParser()

	vendors = parser.parse_vendors(*minpromtorg_diapason)

	for vendor in vendors:
		export_minpromtorg_vendor_to_db(session, vendor)
	session.commit()

	checko_parser = CheckoParser(config["checko_api_key"])
	for vendor in session.query(Vendor).all():

		export_checko_vendor_finances_to_db(
			session,
			vendor.id,
			checko_parser.parse_finances(ogrn=vendor.ogrn)
			)
		export_checko_vendor_to_db(
			session,
			vendor.id,
			checko_parser.parse_organization(ogrn=vendor.ogrn)
			)
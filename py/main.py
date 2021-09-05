import json
import re

from pprint import pprint
from sqlalchemy import func, or_, delete

from .config import *
from .helpers import dbFilling
from .database import session, engine
from .db import methods
from .parsers import OptunionParser, YandexParser, MinpromtorgParser, CheckoParser
from .db.models import Vendor
from .ranking import methods as rank_methods


if __name__ == '__main__':
	# parse_vendors_from_minpromtorg_checko((50, 70))
	rank_methods.update_backend_ratings(session)

	# extra_finances = dict()
	# for vendor_finances in session.execute("SELECT * FROM vendor_finances").all():
	# 	# print(vendor_finances)
	# 	finances_keys = (vendor_finances[1], vendor_finances[2])
	# 	if finances_keys not in extra_finances:
	# 		extra_finances[finances_keys] = 0
	# 	extra_finances[finances_keys] += 1

	# pprint(extra_finances)
	# for extra, count in extra_finances.items():
	# 	if count > 1:
	# 		session.execute("DELETE FROM vendor_finances WHERE vendor_id = %s AND year = %s LIMIT %s", (extra[0], extra[1], count - 1))
	# session.commit()		

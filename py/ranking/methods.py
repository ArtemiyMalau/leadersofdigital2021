from datetime import datetime
from dateutil.relativedelta import relativedelta

from . import COMPANY_AGE_DIAPASON, TIME_KOEFFS
from ..db.models import Vendor, VendorFinances
from sqlalchemy import func, and_


def update_backend_ratings(session):
	"""
		SELECT vendor_id, MAX(`year`) `year` FROM vendor_finances GROUP BY vendor_id
	"""
	subquery = session.query(VendorFinances.vendor_id, func.max(VendorFinances.year).label("year")).group_by(
		VendorFinances.vendor_id).subquery()

	"""
		SELECT vendor_finances.id, vendor_finances.year FROM vendor_finances 
		INNER JOIN ( 
			SELECT vendor_id, MAX(`year`) `year` FROM vendor_finances GROUP BY vendor_id 
		) sub_q ON vendor_finances.vendor_id = sub_q.vendor_id AND vendor_finances.year = sub_q.year
		INNER JOIN vendor ON vendor_finances.vendor_id = vendor.id
	"""
	vendors = session.query(VendorFinances, Vendor). \
		join(
		subquery,
		and_(VendorFinances.vendor_id == subquery.c.vendor_id, VendorFinances.year == subquery.c.year)
	). \
		join(
		Vendor,
		VendorFinances.vendor_id == Vendor.id
	). \
		all()

	vendor_rates = []
	for vendor in vendors:
		if all([field is not None for field in [
			vendor.Vendor.reg_data, 
			vendor.VendorFinances.f_2110, 
			vendor.VendorFinances.f_2200, 
			vendor.VendorFinances.f_2400,
			vendor.Vendor.authorized_capital,
			]]):

			reg_date = datetime.fromtimestamp(vendor.Vendor.reg_data)
			now = datetime.now()

			company_age = relativedelta(now, reg_date).years

			vendor_rates.append((
					vendor,
					calculate_rate_backend_on_profit_margin_sales_own(
						calculate_time_koeff(company_age), 
						vendor.VendorFinances.f_2110, 
						vendor.VendorFinances.f_2200, 
						vendor.VendorFinances.f_2400,
						vendor.Vendor.authorized_capital,
					),
					calculate_rate_backend_on_profit_margin(
						calculate_time_koeff(company_age), 
						vendor.VendorFinances.f_2110,
						vendor.VendorFinances.f_2400,
						vendor.Vendor.authorized_capital,
					),
				))

	rates_profit_margin_sales_own = [rate[1] for rate in vendor_rates]
	profit_margin_sales_own_diapason = (min(rates_profit_margin_sales_own), max(rates_profit_margin_sales_own))

	rates_profit_margin = [rate[2] for rate in vendor_rates]
	profit_margin_diapason = (min(rates_profit_margin), max(rates_profit_margin))

	for rate in vendor_rates:
		rate_backend_1 = calcalate_value_in_range_based_on_value_in_other_range(profit_margin_sales_own_diapason, (0, 100), rate[1])
		rate_backend_2 = calcalate_value_in_range_based_on_value_in_other_range(profit_margin_diapason, (0, 100), rate[2])
		average_rate = int((rate_backend_1 + rate_backend_2) / 2)
		print(rate_backend_1, rate_backend_2, average_rate)

		vendor = session.query(Vendor).filter(Vendor.id == rate[0][1].id).first()
		vendor.rate_backend = average_rate

	session.commit()


def calcalate_value_in_range_based_on_value_in_other_range(first_range, second_range, first_range_value):
	assert first_range[0] <= first_range_value <= first_range[1]

	second_range_value = (first_range_value - first_range[0]) \
						/ (first_range[1] - first_range[0]) \
						* (second_range[1] - second_range[0]) + second_range[0]

	return second_range_value


def calculate_time_koeff(company_age):
	if company_age < COMPANY_AGE_DIAPASON[0]:
		time_koeff = TIME_KOEFFS[0]
	elif company_age > COMPANY_AGE_DIAPASON[1]:
		time_koeff = TIME_KOEFFS[1]
	else:
		time_koeff = calcalate_value_in_range_based_on_value_in_other_range(COMPANY_AGE_DIAPASON, TIME_KOEFFS, company_age)

	return time_koeff


def calculate_rate_backend_on_profit_margin(time_koeff, f_2110, f_2400, authorized_capital):
	# f_2110 - Выручка
	# f_2400 - Чистая прибыль (убыток)

	profit_margin = f_2400 / f_2110 * 100

	# rate = (time_koeff * profit_margin * f_2400 * authorized_capital) / (f_2400 * authorized_capital)
	rate = (time_koeff * profit_margin)

	return rate


def calculate_rate_backend_on_profit_margin_sales_own(time_koeff, f_2110, f_2200, f_2400, authorized_capital):
	# f_2110 - Выручка
	# f_2400 - Чистая прибыль (убыток)
	# f_2200 - Прибыль (убыток) от продаж

	profit_margin = f_2400 / f_2110 * 100
	profit_sales = f_2200 / f_2110 * 100

	average_cost_capital = authorized_capital + f_2110  # замена средней стоимости собственного капитала

	profit_own = f_2400 / average_cost_capital * 100

	rate = time_koeff * (profit_margin + profit_own + profit_sales) / 3

	return rate
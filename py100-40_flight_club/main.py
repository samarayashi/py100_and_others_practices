from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "TPE"

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# get iata code, if there is empty column.
for row in sheet_data:
    if not row["iataCode"]:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

# to check if there is eligible flight in next six months
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
for destination in sheet_data:
    flight = flight_search.flight_check(origin_city_code=ORIGIN_CITY_IATA,
                                        destination_city_code=destination["iataCode"],
                                        from_time=tomorrow,
                                        to_time=six_month_from_today)
    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
        users = data_manager.get_customer_emails()
        emails = [user["email"] for user in users]
        names = [user["firstName"] for user in users]
        message = f"Low price alert! Only NT{flight.price} to fly from {flight.origin_city}-{flight.origin_airport}" \
                  f"to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
        # get google flight link, and send email
        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
        notification_manager.send_emails(emails, message, link)

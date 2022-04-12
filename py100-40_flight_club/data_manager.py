import requests

SHEETY_PRICES_ENDPOINT = "SHEETY END POINT FOR PRICE PAGE"
SHEETY_CUSTOMERS_ENDPOINT = "SHEETY END POINT FOR USER PAGE"


class DataManager:

    def __init__(self):
        self.destination_data = None
        self.customer_data = None

    def get_destination_data(self):
        """get destination data from the google sheet"""
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        """update iata code of destination to the google sheet"""
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", json=new_data)
            print("iataCode: "+response.json()["price"]["iataCode"])

    def get_customer_emails(self):
        """get customer data from the google sheet"""
        response = requests.get(url=SHEETY_CUSTOMERS_ENDPOINT)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data


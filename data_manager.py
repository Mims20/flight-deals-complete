import requests
import os

# This class is responsible for talking to the Google Sheet.

SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]


class DataManager:

    def __init__(self):
        self.sheet_data = {}
        self.customers_data = {}

    # Get sheet data
    def get_sheet(self):
        response = requests.get(url=SHEET_ENDPOINT)
        # auth={USERNAME, PASSWORD})
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data

    # Update spreadsheet with iatacode found for each city
    def update_sheet(self, iatacode, row_id):
        update_endpoint = f"{SHEET_ENDPOINT}/{row_id}"
        # print(update_endpoint, iatacode)
        new_data = {
            "price": {
                "iataCode": iatacode
            }
        }

        response = requests.put(url=update_endpoint,
                                json=new_data)

    # Get users email from spreadsheet through sheety api
    def customers(self):
        customers_endpoint = "https://api.sheety.co/224e8a5ae110a970aff3b3b8710faed9/flightDeals/users"
        response = requests.get(url=customers_endpoint)
        data = response.json()
        self.customers_data = data["users"]
        return self.customers_data

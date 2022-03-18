from pprint import pprint

import requests
from datetime import datetime, timedelta
from flight_data import FlightData
import os

TEQUILA_API_KEY = os.environ["TEQUILA_API_KEY"]


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    # Search for iatacode for each city in the spreadsheet
    def get_iatacode(self, city):
        parameters = {
            "term": city,
            "location_types": "city",
        }
        headers = {
            "apikey": TEQUILA_API_KEY,
        }
        response = requests.get(url="https://tequila-api.kiwi.com/locations/query",
                                params=parameters,
                                headers=headers)
        data = response.json()
        data = data["locations"]
        return data[0]["code"]

    # Search for direct flights between tomorrow and the next 6 months
    # If no direct flights search for flights with 1 stopover
    # Use data to update FlightData class
    def search_flight(self, iatacode):
        tomorrow = datetime.now() + timedelta(days=1)
        six_months = tomorrow + timedelta(days=180)
        tequila_search_endpoint = "https://tequila-api.kiwi.com/v2/search"

        headers = {
            "apikey": TEQUILA_API_KEY
        }

        parameters = {
            "fly_from": "LON",
            "fly_to": iatacode,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": six_months.strftime("%d/%m/%Y"),
            "curr": "GBP",
            "flight_type": "round",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "max_stopovers": 0,
            "one_for_city": 1,
            "limit": 1

        }

        response = requests.get(url=tequila_search_endpoint,
                                params=parameters, headers=headers)
        try:
            data = response.json()["data"][0]
            # print(f"{iatacode} {data['price']}")
            # print(data["price"])
        except IndexError:
            # If there are no direct flights, search for flights with 1 stop overs
            parameters["max_stopovers"] = 1
            response = requests.get(url=tequila_search_endpoint,
                                    params=parameters, headers=headers)
            try:
                data = response.json()["data"][0]
            except IndexError:
                print(f"No flights found for {iatacode} with 1 or 0 stopover.")
            else:
                flight_data = FlightData(price=data["price"],
                                         origin_city=data["cityFrom"],
                                         origin_airport=data["flyFrom"],
                                         destination_city=data["cityTo"],
                                         destination_airport=data["flyTo"],
                                         departure_date=data["route"][0]["local_departure"].split("T")[0],
                                         return_date=data["route"][1]["local_departure"].split("T")[0],
                                         stop_over=1,
                                         via_city=data["route"][0]["cityTo"]
                                         )
                return flight_data
        else:
            flight_data = FlightData(price=data["price"],
                                     origin_city=data["cityFrom"],
                                     origin_airport=data["flyFrom"],
                                     destination_city=data["cityTo"],
                                     destination_airport=data["flyTo"],
                                     departure_date=data["route"][0]["local_departure"].split("T")[0],
                                     return_date=data["route"][1]["local_departure"].split("T")[0],
                                     )

            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data

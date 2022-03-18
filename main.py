from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.

data_manager = DataManager()
sheet_data = data_manager.get_sheet()


flight_search = FlightSearch()
notification_manager = NotificationManager()

# Search for iatacode for each city in the spreadsheet and update spreadsheet with codes
# Search for flights from LON to each iatacode. Compare lowest price to what's in the spreadsheet
# If price is lower, send email to customer or sms using twilio. Include link to book flight
for data in sheet_data:
    if data["iataCode"] == "":
        iatacode = flight_search.get_iatacode(city=data["city"])
        update_sheet = data_manager.update_sheet(iatacode=iatacode, row_id=data["id"])
    else:
        # print(data["iataCode"])
        flight = flight_search.search_flight(iatacode=data["iataCode"])
        if flight is None:
            continue

        if flight.price < data["lowestPrice"]:

            # get emails of customers from spreadsheet
            users = data_manager.customers()
            emails = [row["email"] for row in users]
            first_name = [row["firstName"] for row in users]

            print(f"£{flight.price} is the new low price compared to £{data['lowestPrice']} in the spreadsheet")
            message = f"Low price alert! It's only {flight.price} to fly from{flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.departure_date} to {flight.return_date}"
            google_flight_link = f"https://www.google.com/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.departure_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date} "

            if flight.stop_over > 0:
                print(flight.price, data["lowestPrice"], flight.stop_over, flight.via_city)
                message += f"\nFlight has {flight.stop_over} stop over, via {flight.via_city}"

            # text using twilio or email using smtplib
            notification_manager.text_notification(text_message=message)
            notification_manager.send_emails(emails, message, google_flight_link)


from twilio.rest import Client
import os
import smtplib

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

twilio_number = os.environ["TWILIO_PHONE_NUMBER"]
twilio_verified_number = os.environ["MY_VERIFIED_TWILIO_NUMBER"]

EMAIL = os.environ["email"]
PASSWORD = os.environ["password"]


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    # Send sms using twilio
    def text_notification(self, text_message):
        message = client.messages \
            .create(
            body=text_message,
            from_=twilio_number,
            to=twilio_verified_number,
        )

        print(message.status)

    # Send emails to customers about low price
    def send_emails(self, emails, message, google_flight_link):
        for email in emails:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(EMAIL, PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=email,
                    msg=f"SUBJECT:New low price alert!\n\n{message}\n{google_flight_link}".encode("utf-8")
                )

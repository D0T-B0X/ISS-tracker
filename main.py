import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 26.449923
MY_LONG = 80.331871


def is_above():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if 21 <= iss_latitude <= 31 and 75 <= iss_longitude <= 85:
        return True


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzid": "Asia/Calcutta",
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hours = time_now.hour

    if sunset <= hours or sunrise >= hours:
        return True


while True:

    time.sleep(60)
    if is_above() and is_night():

        with smtplib.SMTP("smpt-mail.outlook.com", 587) as connection:
            connection.starttls()
            connection.login(user="pythontest122@outlook.com", password="knsp2793")
            connection.sendmail(
                from_addr="pythontest122@outlook.com",
                to_addrs="aadikeshu2305@gmail.com",
                msg="Subject:The ISS is right above you"
                    "\n\nLook out! The ISS is currently right above you! See if you can spot it"
            )

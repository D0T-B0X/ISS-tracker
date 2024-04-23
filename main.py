import requests
from datetime import datetime
import smtplib
import time

MY_LAT = #<your latitude>  #you can find your lat and long from www.latlong.com
MY_LONG = #<your longitude>


def is_above():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzid": #<Your timezone>,  #you can find your timezone from "https://www.php.net/manual/en/timezones.php"
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
            connection.login(user=#<dummy email account from where you can send yourself an email>, password= <password for account>)
            connection.sendmail(
                from_addr=#<same as "user">,
                to_addrs=#<your main email address>,
                msg="Subject:The ISS is right above you"
                    "\n\nLook out! The ISS is currently right above you! See if you can spot it"
            )

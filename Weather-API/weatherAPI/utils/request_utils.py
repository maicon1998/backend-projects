from datetime import datetime
import requests
from requests.exceptions import ConnectionError, HTTPError, JSONDecodeError


def request_api(location):
    try:
        geocoding = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=10&language=en&format=json"
        )
        geocoding.raise_for_status()

    except ConnectionError:
        return {"error": "Network error"}
    except HTTPError as error:
        return {"error": error}
    except JSONDecodeError:
        return {"error": "Couldn't decode the text into json"}

    else:
        geocoding_json = geocoding.json()
        if "results" not in geocoding_json:
            return {"error": "Location not found"}

        else:
            latitude = geocoding_json["results"][0]["latitude"]
            longitude = geocoding_json["results"][0]["longitude"]

            try:
                weather = requests.get(
                    f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&hourly=temperature_2m,precipitation_probability&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,precipitation,pressure_msl&forecast_hours=24&past_hours=24"
                )
                weather.raise_for_status()

            except ConnectionError:
                return {"error": "Network error"}
            except HTTPError as error:
                return {"error": error}
            except JSONDecodeError:
                return {"error": "Couldn't decode the text into json"}

            else:
                data = weather.json()
                now = datetime.now()

                # change the datetime for Month, day hour:minute e.g. Jun, 16 00:00
                data["hourly"]["time"] = [
                    dt.strftime("%b, %d %H:%M")
                    for dt in (
                        datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
                        for date_str in data["hourly"]["time"]
                    )
                    if dt >= now
                ]

                # change the date for "month, day" e.g. Jun, 16
                data["daily"]["time"] = [
                    datetime.strptime(date_str, "%Y-%m-%d").strftime("%b, %d")
                    for date_str in data["daily"]["time"]
                ]

                return data

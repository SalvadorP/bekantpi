import requests
import json
from pprint import pprint

# Read the config file.
def getConfig():
    with open("owm_config.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
    return data

# Retrieve weather data.
def getWeatherData(data):
    # API KEY
    API_key = data['api_key']

    # This stores the url
    base_url = data['owm_url']

    # This will ask the user to enter city ID
    city_id = data['city_id']

    # This is final url. This is concatenation of base_url, API_key and city_id
    Final_url = base_url + "appid=" + API_key + "&id=" + city_id + "&units=metric"

    # this variable contain the JSON data which the API returns
    return  requests.get(Final_url).json()


weather_data = getWeatherData(getConfig())
# JSON data is difficult to visualize, so you need to pretty print
pprint(weather_data)

print("City = " + weather_data['name'])
print('Weather = ' + weather_data['weather'][0]['description'])
print("Temp = " + format(weather_data['main']['temp'], '.2f'))
print("Humidity = " + format(weather_data['main']['humidity']))
print('Feels Like = ' + format(weather_data['main']['feels_like'], '.2f'))
print('Wind = ' + format(weather_data['wind']['speed'], '.2f'))

import requests
import json
from pprint import pprint

def getWeatherData(city_id):
    # API KEY
    API_key = "api_key"
 
    # This stores the url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
    # This will ask the user to enter city ID
    # city_id = input("Enter a city ID : ")
    city_id = "2521978"
 
    # This is final url. This is concatenation of base_url, API_key and city_id
    Final_url = base_url + "appid=" + API_key + "&id=" + city_id + "&units=metric"
 
    # this variable contain the JSON data which the API returns
    return  requests.get(Final_url).json()
 

city_id = "city_id"
weather_data = getWeatherData(city_id)
# JSON data is difficult to visualize, so you need to pretty print 
pprint(weather_data)

print("City = " + weather_data['name'])
print("Temp = " + format(weather_data['main']['temp'], '.2f'))
print("Humidity = " + format(weather_data['main']['humidity']))

# Parse the JSON data
# data = json.loads(weather_data)

# pprint(data)

import csv
import re
import json
import requests


DEFAULT_LOCATION_NAME = 'Johnson City'
DEFUALT_LOCATION_COORDS = ['36.3406', '-82.3804']
LOCATION_DATA = []

# Read in location data from worldcities.csv.
# In LOCATION_DATA row[0], is city name;  row[1] and [2] are lat. & long.;  row[6] is state/providence.
# "worldcities.csv" https://simplemaps.com/data/world-cities by Pareto Software, LLC is licensed under CC BY 4.0
def parse_location_data():
    with open('pops_utils/weather_data/worldcities.csv', 'r') as file_data:
        csv_reader = csv.reader(file_data)

        for row in csv_reader:
            LOCATION_DATA.append(row)
    file_data.close()


# Called on by send_forecast_in() or send_forecast_here() to create and return a formatted forecast message.
def create_forecast_message(weather_response):
    temp_strings = []
    for i in range(0, 6):
        temp_strings.append((str)(weather_response['properties']['periods'][i]['temperature']) + ' degrees. ')

    return (
            '\n\n' + weather_response['properties']['periods'][0]['name'] + ': '
            + temp_strings[0] + weather_response['properties']['periods'][0]['detailedForecast'] # Current day temp + forecast.

            + '\n\n' + weather_response['properties']['periods'][1]['name'] + ': '
            + temp_strings[1] + weather_response['properties']['periods'][1]['detailedForecast'] # Next day temp + forecast.

            + '\n\n' + weather_response['properties']['periods'][3]['name'] + ': '
            + temp_strings[2] + weather_response['properties']['periods'][3]['detailedForecast'] # Next day temp + forecast.

            + '\n\n' + weather_response['properties']['periods'][5]['name'] + ': '
            + temp_strings[3] + weather_response['properties']['periods'][5]['detailedForecast'] # Next day temp + forecast.

            + '\n\n' + weather_response['properties']['periods'][7]['name'] + ': '
            + temp_strings[4] + weather_response['properties']['periods'][7]['detailedForecast'] # Next day temp + forecast.

            + '\n\n' + weather_response['properties']['periods'][9]['name'] + ': '
            + temp_strings[5] + weather_response['properties']['periods'][9]['detailedForecast'] # Next day temp + forecast.
            )

# Create and return the current weather info for the default location.
def send_weather_here():
    weather_response = (requests.get('https://api.weather.gov/points/' + DEFUALT_LOCATION_COORDS[0] 
                    + ',' + DEFUALT_LOCATION_COORDS[1] + '/forecast').json())

    temp_string = (str)(weather_response['properties']['periods'][0]['temperature']) + ' degrees. '
    
    current_weather = (weather_response['properties']['periods'][0]['name'] + ': ' + temp_string
                    + weather_response['properties']['periods'][0]['detailedForecast'])

    return 'Weather for ' + DEFAULT_LOCATION_NAME + ': ' + current_weather


# Create and return the current weather info for a location other than the default location.
def send_weather_in(message):
    # Default reply if the territory is not in LOCATION_DATA:
    weather_msg = 'Weather data could not be found for that location.'

    # Split string in 2 and store 2nd string as place name to search.
    msg_split = message.split('weather in ', 1)
    place = msg_split[1]

    row_found = False
    str_search = re.match('.*,.*', place)
    # '.*,.*' means 'city, state/providence' so both of these will be searched for in the for-loop.
    if (str_search):
        split_str = place.split(',', 1)
        for row in LOCATION_DATA:
            if (row[0].lower() in split_str[0]) and (row[3].lower() in split_str[1]):
                row_found = True
                break 
            elif (row[0].lower() in split_str[0]) and (row[6].lower in split_str):
                row_found = True

    # else, only the city was specified. If two of the same cities, it will return forecast
    # of the first one it came accross in LOCATION_DATA.
    else:
         for row in LOCATION_DATA:
            if (row[0].lower() in place):
                row_found = True
                break
    
    if (row_found):

        weather_response = (requests.get('https://api.weather.gov/points/' + row[1] 
                        + ',' + row[2] + '/forecast').json())

        if not('status' in weather_response.keys()):
            current_weather = (weather_response['properties']['periods'][0]['name'] 
                + ' ' + weather_response['properties']['periods'][0]['detailedForecast'])

            weather_msg = 'Weather for ' + row[0] + ', ' + row[6] + ': ' + current_weather

    return weather_msg


# Create and return a 6-day weather forecast message for the default location.
def send_forecast_here():
    weather_response = (requests.get('https://api.weather.gov/points/' + DEFUALT_LOCATION_COORDS[0] 
                    + ',' + DEFUALT_LOCATION_COORDS[1] + '/forecast').json())

    current_weather = create_forecast_message(weather_response)

    return 'Weather for ' + DEFAULT_LOCATION_NAME + ': ' + current_weather


# Create and return a 6-day weather forecast message for a location other than the default location.
def send_forecast_in(message):
    # Default reply if the territory is not in LOCATION_DATA:
    weather_msg = 'Weather data could not be found for that location.'

    # Split string in 2 and store 2nd string as place name to search.
    msg_split = message.split('forecast in ', 1)
    place = msg_split[1]

    row_found = False
    str_search = re.match('.*,.*', place)
    # '.*,.*' means 'city, state/providence' so both of these will be searched for in the for-loop.
    if (str_search):
        split_str = place.split(',', 1)
        for row in LOCATION_DATA:
            if (row[0].lower() in split_str[0]) and (row[3].lower() in split_str[1]):
                row_found = True
                break 
            elif (row[0].lower() in split_str[0]) and (row[6].lower in split_str):
                row_found = True
    # else, only the city was specified. If two of the same cities, it will return forecast
    # of the first one it came accross in LOCATION_DATA.
    else:
         for row in LOCATION_DATA:
            if (row[0].lower() in place):
                row_found = True
                break
    
    
    if (row_found):

        weather_response = (requests.get('https://api.weather.gov/points/' + row[1] 
                        + ',' + row[2] + '/forecast').json())
        
        # When the response contains a 'status' this means an error occurred (such as not
        # having info about the coordinates specified), therefore, we wouldn't be able
        # to create a forecast message; code would throw exception.
        if not ('status' in weather_response.keys()):
            current_weather = create_forecast_message(weather_response)
            weather_msg = 'Weather for ' + row[0] + ', ' + row[6] + ': ' + current_weather

    return weather_msg


# Search strings about weather to determine whether to send
# default weather or weather in specified location.
def get_weather(msg):
    msg_text = msg.lower()

    while True:
        str_search = re.search('tell.*weather in.*', msg_text)
        if (str_search):
            reply = send_weather_in(msg_text)
            break
        else:
            str_search = re.search('tell.*weather', msg_text)
            if (str_search):
                reply = send_weather_here()
                break

        str_search = re.search('what.*s.*weather in.*', msg_text)
        if (str_search):
            reply = send_weather_in(msg_text)
            break
        else:
            str_search = re.search('what.*s.*weather', msg_text)
            if (str_search):
                reply = send_weather_here()
                break

    return reply


# Search strings about forecast to determine whether to send
# default forecast or forecast in specified location.
def get_forecast(msg):
    msg_text = msg.lower()

    while True:
        str_search = re.search('tell.*forecast in.*', msg_text)
        if (str_search):
            reply = send_forecast_in(msg_text)
            break
        else:
            str_search = re.search('tell.*forecast', msg_text)
            if (str_search):
                reply = send_forecast_here()
                break

        str_search = re.search('what.*s.*forecast in.*', msg_text)
        if (str_search):
            reply = send_forecast_in(msg_text)
            break
        else:
            str_search = re.search('what.*s.*forecast', msg_text)
            if (str_search):
                reply = send_forecast_here()
                break

    return reply

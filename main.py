# main.py

import os
import random
import re
import requests
import time
import pops_calls
from multiprocessing import Process
from pops_utils import weather_util

BOT_ID = 'INSERT BOT ID HERE'
GROUP_ID = 'INSERT GROUP ID HERE'
ACCESS_TOKEN = 'INSERT ACCESS TOKEN HERE'
POST_URL = 'https://api.groupme.com/v3/bots/post'
UPLOADS_URL = 'INSERT DROPBOX OR DRIVE URL TO UPLOADS HERE'
MOTIONEYE_IP = 'INSERT IP ADDRESS OF MOTIONEYE CAM HERE'
THIS_DEVICE_IP = 'INSERT IP ADDRESS OF THIS DEVICE' # Should be your public IP address.
INDEX_LOCATION = 'INSERT PATH WHERE SERVER INDEX PAGE IS STORED' # Must be on the machine you plan to run this program.
# I run Apache server on my Pi. The index is in '/var/www/html'. You may need to modify the directory
# to give you write permission if you don't already have it. 

request_params = { 'token': ACCESS_TOKEN }

def send_reply(reply, message):
    post_params = { 'bot_id': BOT_ID, 'text': reply }
    req = requests.post(POST_URL, params = post_params)

    request_params['since_id'] = message['id']
    print('Sent reply: ' + reply)
    print(req) # Print http response.


def send_snap_reply(message):

    # Location of web server's index page and dir where images are stored
    # so they can be accessed by url 'public_ip_address/image_name.jpeg'
    # for example (XX.XXX.XX.XX/0002021312312312.jpeg)
    test = os.listdir(INDEX_LOCATION)

    i = 0
    for item in test:
        i += 1

    if (i > 49): # Clear out folder every 50 images.
        for item in test:
            # Remove all old jpegs from previous downloads.
            if (item.endswith('.jpeg')): 
                os.remove(os.path.join(INDEX_LOCATION, item))

    # Goal here is basically to create an image name that will never be used again.
    # Workaround for groupme api caching first image from url and never sending
    # new image even after content in 'current.jpeg', for example, had changed.
    filename = str(random.randint(0, 90000000)) + str(random.randint(0, 90000000)) + '.jpeg'
    f = open('/var/www/html/' + filename, 'wb')
    f.write(requests.get('http://' + MOTIONEYE_IP + '/picture/1/current/').content)
    f.close()

    post_params = { 'bot_id': BOT_ID, 'text': '' }
    post_data = {'text': 'current.jpeg', 'picture_url': ('http://' + THIS_DEVICE_IP + '/' + filename)}
    req = requests.post(POST_URL, params = post_params, data = post_data)

    request_params['since_id'] = message['id']
    print('Sent most recent image snap')
    print(req) # Print http response.


def main():
    # Parse in all the location data from file.
    # "worldcities.csv" https://simplemaps.com/data/world-cities by Pareto Software, LLC is licensed under CC BY 4.0
    # File is in "./pops_utils/weather_data".
    weather_util.parse_location_data()

    while True:
        try:
            response = requests.get('https://api.groupme.com/v3/groups/' + GROUP_ID 
                    + '/messages', params = request_params)

            if (response.status_code == 200):
                response_messages = response.json()['response']['messages']

                print('\n####################\n# Bot: Pops \n# Group: Pops Alerts'
                    + '\n# Status: Listening\n ###################')

                # Iterate through each message, checking its text
                for message in response_messages:
                    if not (message['text'] == None):
                        # Test for Weather query first
                        # Forecast searches before weather because ppl may say "Whats the weather forecast"
                        str_search = re.search('what.*s.*forecast', message['text'].lower())
                        if (str_search):
                            reply = weather_util.get_forecast(message['text'])
                            send_reply(reply, message)
                            break

                        str_search = re.search('tell.*forecast', message['text'].lower())
                        if (str_search):
                            reply = weather_util.get_forecast(message['text'])
                            send_reply(reply, message)
                            break

                        str_search = re.search('what.*s.*weather', message['text'].lower())
                        if (str_search):
                            reply = weather_util.get_weather(message['text'])
                            send_reply(reply, message)
                            break

                        str_search = re.search('tell.*weather', message['text'].lower())
                        if (str_search):
                            reply = weather_util.get_weather(message['text'])
                            send_reply(reply, message)
                            break

                        # If someone tags Pops (and not to ask weather), pops_calls handles the reply.
                        if ('@pops' in message['text'].lower()):
                            reply = pops_calls.get_reply(message)
                            send_reply(reply, message)
                            break

                        # Key words to get info from MotionEye camera; popcam_calls handles these. 

                        # I have an IFTTT webhook which when called by MotionEye, posts 'ALERT!!...'
                        # when motion is detected. Then my bot knows to post a current snapshot.
                        elif ('ALERT!!' in message['text']) or (message['text'] == 'SNAP'):
                            attempt_send = Process(target = send_snap_reply(message))
                            attempt_send.start()
                            attempt_send.join(timeout = 45) # Max time function can run is 45 secs.
                            attempt_send.terminate()        # Terminate if still running after 45.
                            break

                        elif (message['text'] == 'STREAM'):
                            send_reply(MOTIONEYE_IP, message)
                            break

                        elif (message['text'] == 'UPLOADS'):
                            send_reply(UPLOADS_URL, message)
                            break

        except requests.exceptions.ConnectionError as e:
            print('No connection')
            print(e)

        except requests.exceptions.Timeout as e:
            print('Connection timed out')
            print(e)

        except requests.exceptions.RequestException as e:
            print('A request error ocurred')
            print(e)

        except:
            print('An error occurred')
            
main()


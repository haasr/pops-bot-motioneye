# main.py

# Rudimentary program which interfaces with the GroupMe API to scan through given 
# GroupMe group and look for key words which indicate queries to the GroupMe bot. 
# The program will then use post requests to post a response. Provides some useful
# data from MotionEye cam on LAN and makes basic conversation using the pops_calls
# module. 

# My code resembles the code from http://sweb.uky.edu/~jtba252/index.php/2017/09/13/how-to-write-a-groupme-bot-using-python/
# which I read and followed to learn how to interface with the GroupMe API in Python. Thanks for a great tutorial.


import re
import requests
import time
import pops_calls

BOT_ID = 'INSERT BOT ID HERE'
GROUP_ID = 'INSERT GROUP ID HERE'
ACCESS_TOKEN = 'INSERT ACCESS TOKEN HERE'
POST_URL = 'https://api.groupme.com/v3/bots/post'
UPLOADS_URL = 'INSERT DROPBOX OR DRIVE URL TO UPLOADS HERE'
MOTIONEYE_IP = '192.168.1.104'

request_params = { 'token': ACCESS_TOKEN }

def send_reply(reply, message):
    post_params = { 'bot_id': BOT_ID, 'text': reply } 
    req = requests.post(POST_URL, params = post_params)
    
    request_params['since_id'] = message['id']
    print('Sent reply: ' + reply)
    print(req) # Print http response.


def send_snap_reply(message):
    # I couldn't figure out how to send an image following Groupme's API documentation.
    # Kept getting http response 400. The solution was not to use 'attachments' in the
    # post parameters but 'picture_url' as shown here:
    # https://stackoverflow.com/questions/53807009/groupme-bot-is-not-sending-images-along-with-its-text
     
    post_params = { 'bot_id': BOT_ID, 'text': '' } 
    # Pass URL to current snapshot from MotionEye camera to the data field.
    post_data = {'text': 'current.jpeg', 'picture_url': 'http://' + MOTIONEYE_IP + '/picture/1/current/'}
    req = requests.post(POST_URL, params = post_params, data = post_data)
    
    request_params['since_id'] = message['id']
    print('Sent most recent image snap')
    print(req) # Print http response.


def main():

    while True:

        print('\n####################\n# Bot: Pops \n# Group: Dev Testing'
                + '\n# Status: Listening\n ###################')
    
        response = requests.get('https://api.groupme.com/v3/groups/' + GROUP_ID 
                + '/messages', params = request_params)

        if (response.status_code == 200):
            response_messages = response.json()['response']['messages']

            # Iterate through each message, checking its text
            for message in response_messages:
                if not (message['text'] == None):

                    # If someone tags Pops, pops_calls handles the reply.
                    if ('@pops' in message['text'].lower()):
                        reply = pops_calls.get_reply(message)
                        send_reply(reply, message)
                        break

                    # Key words to get info from MotionEye camera. 
                    elif ('ALERT!!' in message['text']):
                        send_snap_reply(message)
                        break
                        
                    elif (message['text'] == 'SNAP'):
                        send_snap_reply(message)
                        break

                    elif (message['text'] == 'STREAM'):
                        send_reply(reply, MOTIONEYE_IP)
                        break

                    elif (message['text'] == 'UPLOADS'):
                        reply = UPLOADS_URL
                        send_reply(reply, message)
                        break
                    else:
                        pass   
                
        time.sleep(5)
main()

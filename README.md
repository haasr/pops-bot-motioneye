# pops-bot-motioneye
A rudimentary Python program which utilizes a GroupMe bot to make basic conversation and provide functionality from a MotionEyeOS camera on LAN by communicating with the GroupMe API and MotionEye host through GET and POST requests using the Python requests library. My cam is set up to monitor my pet chicken --Popcorn-- and the responses returned from the GroupMe bot are meant to immitate her personality.

My code is based off of a tutorial from http://sweb.uky.edu/~jtba252/index.php/2017/09/13/how-to-write-a-groupme-bot-using-python/ which I greatly appreciate.

Updates:

  - Added recognition to phrases such as "what is the weather" or "tell me the forecast in Brooklyn, New York" and a weather utility module to handle queries for weather information and return appropriate weather data.
  
  - Added functionality to provide proverbs/wisdom when requested to the bot.
  
  - Added exception handling for requests.
  
  - Changed the way images are uploaded. The original method was to upload a current snapshot from the MotionEye camera by using the URL [MotionEye IP address]/picture/1/current provided by the MotionEye camera. Now an Apache server has been set up to host an index page in the directory "/var/www/html" on my Raspberry Pi; the image provided by the "[MotionEye IP address]/picture/1/current" URL is downloaded to this directory to a random image name. This creates a unique URL which consists of my Raspberry Pi's IP address plus the name of the image (i.e. "192.168.1.149/00023121000101.jpeg"). This was a workaround to an issue I discovered in which the GroupMe bot would not post any new images when the same URL was passed in the POST request (the first time the URL, "[MotionEye IP address]/picture/1/current" was used, the correct image posted, every time thereafter, the same image posted even though "[MotionEye IP address]/picture/1/current" would contain a new image).

Requirements:

  - Python 3.x.
  
  - Python requests library.
  
  - A GroupMe bot in your selected GroupMe group. You can create bots by registering an account on "https://dev.groupme.com/".
    This is also where you access your access token, bot ID, and group ID needed in "main.py" after you have created a bot.
  
  - A MotionEyeOS camera connected on the same LAN as the machine running the program.
  
  - A web server needs to be running on the same machine that you are running the program to make use of the "send_snap_reply" function in "main.py". I use an Apache server on my Raspberry Pi. If you don't want to set up a web server, simply comment or delete out lines 33-66 and lines 125-131 in "main.py".

Setup: 

After creating a GroupMe bot, open the "main.py" file in a text editor and insert your bot ID, group ID, access token, 
** *uploads URL*, the IP address of your machine which will run the program (you need to use a static IP if using the web server), the directory on your machine where the index page of your web server is located (again, if you are using the web server), and the IP address to the MotionEye camera. Then the program is ready to run by executing "main.py".

** *There is an option in the MotionEyeOS admin settings to have footage uploaded to a Google Drive or Dropbox location. The purose of the uploads URL is so when a user says "UPLOADS" in the group, the bot returns a hyperlink to this Drive or Dropbox location. If you don't want this feature, you can simply delete it out of "main.py" by removing lines 15, 137, 138, and 139.*
  
Messaging the Pops Bot in your GroupMe group:

  * PopCam Utilities
  
    SNAP
      - Sends a recent snapshot from the PopCam.
    STREAM
      - Sends URL to live stream (works on local connection only).
    UPLOADS
      - Sends URL to view all photos and videos captured.
      
 * Pops Weather Utility
  
    “What’s the weather”
      - Sends weather at Pops’ coop.”

    “What’s the forecast”
      - Sends 5-day forecast of weather at Pops’ coop.
      “What’s the weather in [city]” / “What’s the weather in [city, territory]”
      - Attempts to get weather data for the city specified and replies with weather or notifies that
      the location was not found. Limited right now due to the small size of my data file that it searches
      from.
      - "What’s the weather in [city, territory]” is a better format. (If Morristown, New Jersey were first in
      list and you asked for weather in Morristown expecting Morristown, TN, you would get the weather
      for Morristown, NJ instead.

    “What’s the forecast in [city]” / “What’s the forecast in [city, territory]”
      - Attempts to get 5-day weather forecast data for the city specified and replies with forecast or
      notifies that the location was not found. Limited right now due to the small size of my data file
      that it searches from.
      - Again, specifying [city, territory] will be more accurate.

 * Talk to Popcorn. A few things to try:
  - ”@pops What is the meaning of life?”
  - ”@pops How are you?”
  - ”@pops What’s up”
  - ”@pops What are you doing?”
  - ”@pops Where are you?”
  - ”@pops How’s the weather?”
  - ”@pops Tell me about your business”
  - ”@pops Where are you from?”
  - ”@pops Should I ___ or ___?”
  - ”@pops Tell me a joke”
  - ”@pops Tell me a proverb.”
  - ”@pops Give me wisdom.”

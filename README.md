# pops-bot-motioneye
A rudimentary Python program which utilizes a GroupMe bot to make basic conversation and provide functionality from a MotionEyeOS camera on LAN by communicating with the GroupMe API and MotionEye host through GET and POST requests using the Python requests library. My cam is set up to monitor my pet chicken --Popcorn-- and the responses returned from the GroupMe bot are meant to immitate her personality.

My code is based off of a tutorial from http://sweb.uky.edu/~jtba252/index.php/2017/09/13/how-to-write-a-groupme-bot-using-python/ which I greatly appreciate.

The CSV file which my weather_util module uses to get the coordinates of a city can be found at https://simplemaps.com/data/world-cities and is licensed under CC BY 4.0. View the license in "./pops_utils/weather_data/license.html"

Updates:

  - Fixed the function "create_forecast_message" in "pops_utils/weather_util.py" which was returning a string with the wrong weather data from 6:00 to 17:00 due to the way the indices of forecast periods changed in the json data returned from the weather API.
  
  - Added recognition to queries such as "@pops how's the weather" wherein the bot will base it's response off of the current temperature returned from the get_default_temperature() method in "pops_utils/weather_util.py".


Requirements:

  - Python 3.x.
  
  - Python requests library.
  
  - A GroupMe bot in your selected GroupMe group. You can create bots by registering an account on "https://dev.groupme.com/".
    This is also where you access your access token, bot ID, and group ID needed in "main.py" after you have created a bot.
  
  - A MotionEyeOS camera connected on the same LAN as the machine running the program.
  
  - A web server needs to be running on the same machine that you are running the program to make use of the "send_snap_reply" function in "main.py". I use an Apache server on my Raspberry Pi. Of course, the device running the server must have a static IP address so you can forward the HTTP/tcp port to the server (in my experience, https did not work). The server is only for the functionality of posting images in the group; if you don't want to set up a web server, simply comment or delete out lines 33-66 and lines 125-131 in "main.py". 

Setup: 

After creating a GroupMe bot, open the "main.py" file in a text editor and insert your bot ID, group ID, access token, 
** *uploads URL*, MotionEye camera stream address, the IP address of your machine which will run the program (you need to use your public IP if using the web server), the directory on your machine where the index page of your web server is located (again, if you are using the web server), and the IP address to the MotionEye camera. Then the program is ready to run by executing "main.py".

** *There is an option in the MotionEyeOS admin settings to have footage uploaded to a Google Drive or Dropbox location. The purose of the uploads URL is so when a user says "UPLOADS" in the group, the bot returns a hyperlink to this Drive or Dropbox location. If you don't want this feature, you can simply delete it out of "main.py" by removing lines 15 and 137-139.*
  
Messaging the Pops Bot in your GroupMe group:

  * PopCam Utilities
  
    - SNAP
      - Sends a recent snapshot from the PopCam.
    
    - STREAM
      - Sends URL to live stream (works on local connection only).
    
    - UPLOADS
      - Sends URL to view all photos and videos captured.
      
 * Pops Weather Utility
  
    - “What’s the weather”
      - Sends weather at Pops’ coop.”

    - “What’s the forecast”
      - Sends 5-day forecast of weather at Pops’ coop.
    - “What’s the weather in [city]” / “What’s the weather in [city, territory]”
      - Attempts to get weather data for the city specified and replies with weather or notifies that
        the location was not found. Limited right now due to the small size of my data file that it searches
        from.
      - "What’s the weather in [city, territory]” is a better format. (If Morristown, New Jersey were first in
        list and you asked for weather in Morristown expecting Morristown, TN, you would get the weather
        for Morristown, NJ instead.

    - “What’s the forecast in [city]” / “What’s the forecast in [city, territory]”
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

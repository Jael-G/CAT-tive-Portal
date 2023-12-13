![CAT-tive Portal](https://github.com/Jael-G/CAT-tive-Portal/blob/main/images/CAT-tivePortalBanner.png)

# CAT-tive Portal
CAT-tive Portal is an ESP32 Micropython project made using the [Phew](https://github.com/pimoroni/phew) library. It hosts a basic captive portal that asks most devices to log in to be able to use the network and captures any log in credentials. It displays capture data on an SSD1306 Display, and stores the information in `.csv` files.
- [CAT-tive Portal](#cat-tive-portal)
    - [Features](#features)
    - [Installation and Requirements](#installation-and-requirements)
    - [Execution](#execution)
    - [Display](#display)
    - [Captive Portal](#captive-portal)
    - [Data](#data)
    - [Notes](#notes)

## Features
1. Creates access point with captive portal to obtain credentials
2. Stores every credential captured into `.csv` files
3. Displays the information in a (cute) interface
## Installation and Requirements
To make the project work you will need to have the following:

1. Install [Phew](https://github.com/pimoroni/phew/tree/main/phew) and add it to a directory with the name `phew` on the ESP32 device
2. Download the [SSD1306 display Library](https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display/ssd1306) and add it as a `ssd1306.py` file in the main (flash) directory of the ESP32
3. Add an empty directory called `captures` to the main directory of the ESP32 (the `capture_#.csv` files will be saved here)
4. Add this reposity to your ESP32 device

Your device's file should look like:
```
├── animations/
│   ├── cat_captures.json
│   └── cat_sleeping.json
│
├── captures/
│
├── phew/
│   ├── dns.py
│   ├── logging.py
│   ├── server.py
│   ├── template.py
│   └── __init__.py
│
├── templates/
│   └── goog.html
|
├── cat-tive_portal.py
└── ssd1306.py
```

## Execution
Once the installation and requirements are completed, and the ESP32 is connected properly to the SSD1306 display (remember to set up the pins properly in the code) the code is ready to run. 

* To make the code run automatically on poweron, create `main.py` and move the code there or add a command like `exec(open("cat-tive_portal.py").read())`

The display should instantly light up and show the cat sleeping animation. The access point will have been created, and the DNS server that catches all requests will be up and running, waiting for people to connect. The DNS server will redirect any user that connects to the captive portal webpage.  

## Display
The display is used to demonstrate valuable information in a fun and cute way. Here is what every part of the display indicates:
1. Waiting Mode

![Waiting Mode Display](https://github.com/Jael-G/CAT-tive-Portal/blob/main/images/WaitingDisplay.png)

UPDATE: The waiting mode no longer displays "Waiting...". Now, in its place it indicates the ESSID of the access point, under the ESSID it indicates the channel and under that the authmode being used. The display image for this mode will be updated when I have more time. 

In this mode, the most important data present is the amount of captures so far in the upper left corner, and to the right, the amount of time the device has been on (Uptime). The device will be in this mode while the servers and access point are running. 

2. Capture Mode

![Capture Mode Display](https://github.com/Jael-G/CAT-tive-Portal/blob/main/images/CaptureDisplay.png)

This mode appears for 5 seconds whenever a capture of credentials has been made in the captive portal. It shows some vital information about the capture. In the top left corner, it shows the amount of captures so far (which should be updated by 1). To the right of that, the website the credentials are from (based on the form sent by the captive portal). Under the upper bar to the left, the username and password submitted. Finally, on the lower right, it shows the number of the file where it will be stored, in this example 12 indicates the credentials are saved in `capture_12.csv`. A new `.csv` is created everytime the code is executed, increase the number of the capture file each time. 

## Access Point
The access point settings can be modified in the code. The essid, channel and authmode are shown in the display. The settings are:
1. ESSID: The name the access point will have

2. Password: The password to access, only works if authmode is changed from network.AUTH_OPEN

3. Channel: The channel the access point will be on

4. Authmode: The authentication method to be used. The authmode can be set using the network constant or the int value. The options are shown in the code, they are:

```
    * 0 || network.AUTH_OPEN         -- OPEN 
    * 1 || network.AUTH_WEP          -- WEP
    * 2 || network.AUTH_WPA-PSK      -- WPA-PSK
    * 3 || network.AUTH_WPA2_PSK     -- WPA2-PSK
    * 4 || network.AUTH_WPA_WPA2_PSK -- WPA/WPA2-PSK
```

## Captive Portal
What makes the captive portal so effective and useful is that many devices get a pop-up indicating that they need to log in to the network. In fact, in many instances it evens instantly redirects to the captive portal as soon as the person attempts to connect to the access point. After that, any credential sent is displayed and stored.

The project comes with an example of a captive portal. `Goog` is a clone of Google's Gmail login page.

![Goog Captive Portal](https://github.com/Jael-G/CAT-tive-Portal/blob/main/images/captiveportal.png)


 In the template, it showcases one of the most important features to keep in mind when creating a webpage for this project, the form. The form HAS to contain 3 items, the username, the password, and finally the website. 

`Why the 'website' item?`

The website item was implemented for two main reasons.
1. In a read team scenario, different clones of popular login portals (i.e. Gmail, Microsoft, Apple) might be used at different times, and therefore, it is important to keep track of to what website each credential belongs to.

2. Secondly, the initial version of this project had a captive portal which was a landing page that allowed different forms of login (think of the pages that let you use Gmail, Microsoft or Apple as login options). This meant a single session could receive multiple credentials of different websites, and thus, an even bigger reason to keep track of each website. Why this portal was discarded is explained more in the [Notes](#Notes) section.

## Data
* The credentials are stored in a `.csv` file and are stored as:

    | Username | Password | Website |
    | :---:   | :---: | :---: |
    | Catuser | Pass123   | Goog   |

## Notes
* Previously, this project used a landing page that allowed different forms of logins. This were:
    - Goog (current one used in the captive portal page example, a clone of Gmail)
    - Macrohard (Microsoft clone)
    - Pear (Apple clone)

    However, employing a landing page that redirected to another template led to a crash of the DNS server after minimal usage. Thus, switching to a single-page setup allowed the device to continue operating without any hiccups, enduring many credential captures and extended durations without encountering any issues. Testing of up to 60 captures over 12 hours showed no signs of past problems or indications of potential future ones.

    `Were there possible fixes or workarounds?` 

    Possibly. The thought of implementing a dynamic page that loads EVERYTHING via JavaScript was worked on. The page would have 3 options (the ones previously mentioned), and when one was selected the new page would load entirely via JavaScript, thus functioning as a redirect. However, the implementation was abandoned for simplicities sake. 

    There's also the consideration that when this problem was encountered the pages were being served using the `server.render_template('path')` function, the initial landing page was never tested with the new method of preloading every html file as a response when the code starts execution. 

* The animation was made possibly using my very own method of 'encoding'. It worked the following way:
    1. Store all the frames of an animation in a directory

    2. Run a python code (most important part) that did the following to each frame:

        a. Grab the frame, resize it to 128x64 (resolution fo the SSD1306 display)

        b. Turn it into grayscale, and turn each pixel into either black or white based on a treshold

        C. Scan every single pixel of the new image, and recording every white or black pixel. This was set up depending on each image. If the background is white and the lines black, only record the black pixels, if it's the reverse, record only the white ones.

        D. Store the data in a 2D Array. The array was made up of each row, and inside each row there's int representing the X value of each pixel that should be drawn in the display.

        E. Once every frame is recorded, store it into a json. The json files were incredibly small, most being slightly less than 1Kb. 
        

       The content inside the json is basically a huge list, inside that list there was every frame represented as a 2D Array, and inside that 2D array, every row was a list containing the int values for X. For example, if in the first frame the first row indicated [1,10,20] this meant the pixels (1,0), (10,0) and (20,0) should be drawn. 

        Maybe one day I'll upload the "encoder" as a seperate project. However, this means that any animation that goes through the process of said encoding can be implemented into the device for customizing purposes. It is important to remember that if different animations have different amount of frames, the code has to be changed so that each animation has its own `FRAMES_NUM` variable.

* Previously, it was attempted to implement into the project the option to send the capture file genereated whenever a certain amount of captures is met. However, the device would fail to read the file and send it's data. Could never figure out the reason. Sending the same data as a hard-coded string was no problem. Althought the device indicated it was a memory error, the memory was monitored and never reached a point close to being full. 

* This project was in part inspired by [pwnagotchi](https://github.com/evilsocket/pwnagotchi). The idea of having a cybersecurity red-team project with a cute interface seemed like a nice and fun combo. 

## To-Do
* Revisit the idea of having a lading page as default, and said landing page can redirect to multiple log in portal clones.
* Possibly implement more useful data that can be displayed into the SSD1306 display

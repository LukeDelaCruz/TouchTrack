# Member 1: Onimisi Ayira with ID: 1548437
# Member 2: Luke Patrick Dela Cruz with ID: 1504816
# Cmput 275 Wi18, Project

from flask import Flask, render_template
from flask_sockets import Sockets
import pyautogui
import socket
import os

# initialize network objects
app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/move_mouse')
def echo_socket(ws):
    received_coords = [[[-1, -1], False], [[-1, -1], False]]
    if not ws.closed:
        print("Android device acknowledged!")
    while not ws.closed:
        message = ws.receive()
        if message:
            if message == "Clicked!":
                pyautogui.click()
            else:
                coords = message.split(",")
                pyautogui.PAUSE = 0.01  # remove lag!
                new_x = int(coords[0].strip())
                new_y = int(coords[1].strip())
                if not received_coords[0][1]:
                    received_coords[0][0][0] = new_x
                    received_coords[0][0][1] = new_y
                    received_coords[0][1] = True
                elif received_coords[0][1] and not received_coords[1][1]:
                    received_coords[1][0][0] = new_x
                    received_coords[1][0][1] = new_y
                    received_coords[1][1] = True
                elif received_coords[0][1] and received_coords[1][1]:
                    curr_x, curr_y = pyautogui.position()
                    trans_x = received_coords[1][0][0] - received_coords[0][0][0]
                    trans_y = received_coords[1][0][1] - received_coords[0][0][1]
                    pyautogui.moveTo(curr_x+trans_x, curr_y+trans_y)
                    received_coords = [((-1, -1), False), ((-1, -1), False)]
                # print("current x and y of screen,",curr_x, curr_y)
                # print("coordinates sent from phone,", new_x, new_y)
                # if new_x>curr_x and new_y<curr_y:
                #     pyautogui.moveTo(new_x-curr_x, curr_y-new_y)
                # elif new_x<curr_x and new_y>curr_y:
                #     pyautogui.moveTo(curr_x-new_x, new_y-curr_y)
                # elif new_x>curr_x and new_y>curr_y:
                #     pyautogui.moveTo(new_x-curr_x, new_y-curr_y)
                # elif new_x<curr_x and new_y<curr_y:
                #     pyautogui.moveTo(curr_x-new_x, curr_y-new_y)
                # print("Old:", pyautogui.position())
                # print("Received:", new_x, new_y)
                # pyautogui.moveTo(new_x, new_y)
                # print("New:", pyautogui.position())
# @app.route('/')
# def hello():
#     return 'Hello World!'

if __name__ == "__main__":

    # # set up command line
    # clear = lambda: os.system('cls')
    # window_resize = lambda: os.system('mode con: cols=174 lines=43')
    # clear()
    # window_resize()
    # serverIP = socket.gethostbyname(socket.gethostname())
    # print("Use this as the server IP in the app:", serverIP)
    #
    # # run server
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    # server.serve_forever()
    received_coords = [[[-1, -2], False], [[-1, -1], False]]
    received_coords[0][0][0] = -3
    print(received_coords[0][0][0])

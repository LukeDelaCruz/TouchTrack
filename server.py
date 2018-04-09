from flask import Flask, render_template
from flask_sockets import Sockets
from codegen import gen_password
from trackprocessor import*
import pyautogui
import socket
import os

# initialize network objects
app = Flask(__name__)
sockets = Sockets(app)

# set up environment
received_coords = [[[-1, -1], False], False]
security_code = ""
pyautogui.PAUSE = 0.01  # remove delay! can't be zero from hardware limitations
pyautogui.FAILSAFE = False  # allow for the corners to be reached by the cursor


@sockets.route('/move_mouse')
def echo_socket(ws):
    if not ws.closed:
        # allows us to keep track of environment variables statuses in between
        # calls to echo_socket function
        global security_code
        global received_coords

        print("Android device acknowledged! Server IP accepted!")

        if ws.receive() != security_code:  # now we are ready to receive the security code
            print("Invalid security code! Please try again by hitting the >terminate< button.")
            security_code = gen_password(1)
            print("New security code generated:", security_code)
            return  # prevents potential server timeouts in between echo_socket calls
        else:
            print("Security code accepted!")

    while not ws.closed:
        message = ws.receive()
        if not message:
            break
        received_coords = oneTouchTracker(message, received_coords)

    print("Android device terminated!")
    security_code = gen_password(1)
    print("New security code generated:", security_code)
    return  # prevents potential server timeouts in between echo_socket calls


if __name__ == "__main__":

    # set up command line and authentication
    security_code = gen_password(1)
    print("Enter this 5-character-case-sensitive security code:", security_code)
    serverIP = socket.gethostbyname(socket.gethostname())  # retrieve machine's (server) IP
    print("Use this as the server IP in the app:", serverIP)
    print("Use Ctrl + c to exit.")

    # run server from the random port of 5000
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

from flask import Flask, render_template
from flask_sockets import Sockets
import pyautogui

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/move_mouse')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message:
            if message == "Clicked!":
                pyautogui.click()
            else:
                coords = message.split(",")
                pyautogui.click(int(coords[0].strip()), int(coords[1].strip()))

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

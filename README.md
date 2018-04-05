# touchtrack
Server instructions:
1. Connect and authenticate within openUWS on laptop and mobile. (Alternately, you can connect to a LAN that places the devices in the same subnet, e.g., UWS will not work for these purposes).
2. Install pyautogui as such:
> On Windows, no need to do anything!
> On OS X, run sudo pip3 install pyobjc-framework-Quartz, sudo pip3 install pyobjc-core, and then sudo pip3 install pyobjc.
> On Linux, run sudo pip3 install python3-xlib, sudo apt-get install scrot, sudo apt-get install python3-tk, and sudo apt-get install python3-dev. (Scrot is a screenshot program that PyAutoGUI uses.)
3. Run the python server.
4. Then open the app (AFTER running the server).
5. Type in the IP address given by the server to the app.

Todo:
3. Have authentication and proper termination when connections are lost.
4. Have enum states using graph nodes that implement a finite state machine to check for valid IPs
5. Proper left click and right click.

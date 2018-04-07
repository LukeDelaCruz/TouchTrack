package com.example.lukepatrick.touchtrack2;

import android.view.MotionEvent;
import android.view.View;

import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;

// class based on WebSocket from the previous activity
public class TouchCoordsDispatcher extends WebSocketListener {
    // get the environment that will be used to motion events
    private View view;
    public TouchCoordsDispatcher(View view) {
        this.view = view;
    }

    // function that runs when an object of this class is instantiated
    // that be called when a WebSocket request connection is made.
    @Override
    public void onOpen(final WebSocket webSocket, Response response) {

        view.setOnTouchListener(new View.OnTouchListener() {

            // time allocated for a proper click is 200 ms from the down action to up action
            private static final int MAX_CLICK_DURATION = 200;
            // timer used to count time intervals
            private long startClickTime;
            // flags right clicks
            private boolean tap2 = false;

            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
               // Log.i("TOUCH", motionEvent.toString());
                if (view == null) {
                    return false;
                }

                switch (motionEvent.getActionMasked()) {
                    case MotionEvent.ACTION_DOWN:  // display has been touched
                        startClickTime = System.currentTimeMillis();  // start timer
                        break;

                    case MotionEvent.ACTION_POINTER_DOWN: // touched by another finger or object
                        webSocket.send("RC");  // this is a right click
                        tap2 = true; // set right click flag
                        break;

                    case MotionEvent.ACTION_UP:
                        // if the timing was short enough between a press and release and that
                        // there was no right click (i.e., tap2 = false) we register a click and
                        // send that click ("C") signal to the server
                        long clickDuration = System.currentTimeMillis() - startClickTime;
                        if (clickDuration < MAX_CLICK_DURATION && !tap2){
                            webSocket.send("C");
                        }
                        tap2 = false;  // since a right just happened we can set this flag again
                        break;

                    case MotionEvent.ACTION_MOVE:  // general movement
                        // absolute coordinates are send to the server which will process that data
                        // and move the move accordingly
                        String coordMessage = String.format("%d, %d", (int) motionEvent.getRawX(), (int) motionEvent.getRawY());
                        webSocket.send(coordMessage);  // transmit the absolute coordinates
                        break;
                }
                return true;
            }
        });
    }
}



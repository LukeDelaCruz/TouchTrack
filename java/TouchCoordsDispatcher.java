package com.example.lukepatrick.touchtrack2;

import android.util.Log;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;


public class TouchCoordsDispatcher extends WebSocketListener {
    private View view;


    public TouchCoordsDispatcher(View view) {
        this.view = view;
    }


    @Override
    public void onOpen(final WebSocket webSocket, Response response) {


        view.setOnTouchListener(new View.OnTouchListener() {
            private static final int MAX_CLICK_DURATION = 150;
            private long startClickTime;
            private int tap_count = 0;
            private boolean tap2 = false;


            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
               // Log.i("TOUCH", motionEvent.toString());
                if (view == null) {
                    return false;
                }

                switch (motionEvent.getActionMasked()) {
                    case MotionEvent.ACTION_DOWN:
                        ++tap_count;
                        startClickTime = System.currentTimeMillis();
                        break;

                    case MotionEvent.ACTION_POINTER_DOWN : {
                        ++tap_count;
                        webSocket.send("2C");
                        tap2 = true;
                        break;
                    }

//                    case MotionEvent.ACTION_POINTER_UP : {
//                        --tap_count;
//                        break;
//                    }

                    case MotionEvent.ACTION_UP:
                        --tap_count;
                        long clickDuration = System.currentTimeMillis() - startClickTime;
                        if (clickDuration < MAX_CLICK_DURATION && !tap2){
                            webSocket.send("C");
                        }
                        tap2 = false;
//                        if (tap_count == 2) {
//                            tap_count = 0;
//                            webSocket.send("2C");
//                        }
                        break;

                    case MotionEvent.ACTION_MOVE:
                        String coordMessage = String.format("%d, %d", (int) motionEvent.getRawX(), (int) motionEvent.getRawY());
                        webSocket.send(coordMessage);
                        break;

                }


                return true;
            }

        });

    }
}



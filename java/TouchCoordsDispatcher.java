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


            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
               // Log.i("TOUCH", motionEvent.toString());
                if (view == null) {
                    return false;
                }

                switch (motionEvent.getActionMasked()) {
                    case MotionEvent.ACTION_DOWN:
                        startClickTime = System.currentTimeMillis();
                        break;

                    case MotionEvent.ACTION_UP:
                        long clickDuration = System.currentTimeMillis() - startClickTime;
                        if (clickDuration < MAX_CLICK_DURATION){
                            webSocket.send("C");
                        }
                        break;

                    case MotionEvent.ACTION_MOVE:
                        String coordMessage = String.format("%d, %d", (int) motionEvent.getRawX(), (int) motionEvent.getRawY());
                        webSocket.send(coordMessage);
                        break;
                    case MotionEvent.ACTION_CANCEL:
                        webSocket.send("hi2");
                }


                return true;
            }

        });

    }
}



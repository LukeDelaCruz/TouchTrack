package com.example.lukepatrick.touchtrack2;

import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Toast;

import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;


public class TouchCoordsDispatcher extends WebSocketListener {
    private View view;
    public TouchCoordsDispatcher(View view) {
        this.view = view;
    }

    boolean moved = false;
    long startTime = 0;
    @Override
    public void onOpen(final WebSocket webSocket, Response response) {

        view.setOnTouchListener(new View.OnTouchListener() {

            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
               // Log.i("TOUCH", motionEvent.toString());
                if (view == null) {
                    return false;
                }
                switch (motionEvent.getActionMasked()) {
                    case MotionEvent.ACTION_MOVE:
                        String coordMessage = String.format("%d, %d", (int) motionEvent.getRawX(), (int) motionEvent.getRawY());
                        webSocket.send(coordMessage);
                        moved = true;
                        startTime = System.currentTimeMillis();

//                    case MotionEvent.ACTION_DOWN:
//                        return true;

//                    case MotionEvent.ACTION_UP:
//                        if (System.currentTimeMillis() - startTime > 700){
//                            moved = false;
//                        }
//                        else {
//                            webSocket.send("Clicked!");
//                        }
//                    case MotionEvent.ACTION_CANCEL:

                }
                return true;
            }
        });
    }
}


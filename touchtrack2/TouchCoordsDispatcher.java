package com.example.lukepatrick.touchtrack2;

import android.util.Log;
import android.view.MotionEvent;
import android.view.View;

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
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                Log.i("TOUCH", motionEvent.toString());
                if (motionEvent.getAction() == MotionEvent.ACTION_MOVE) {
                    String coordMessage = String.format("%d, %d", (int) motionEvent.getX(), (int) motionEvent.getY());
                    webSocket.send(coordMessage);
                    return true;
                }
                else if (motionEvent.getAction() == MotionEvent.ACTION_DOWN) {
                    webSocket.send("Clicked!");
                    return true;
                }

                return false;
            }
        });
    }
}

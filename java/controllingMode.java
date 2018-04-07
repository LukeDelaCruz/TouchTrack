package com.example.lukepatrick.touchtrack2;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.WebSocket;

public class controllingMode extends AppCompatActivity {

    // create new activity of environment
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controlling_mode);
        View touchPadView = findViewById(R.id.Control);
        Intent intentExtras = getIntent();  // holds IP data from previous activity
        Bundle extrasBundle = intentExtras.getExtras();  // get the extras from previous activity

        // using the IP from user that was from server, we can request a connection establishment
        String url = "ws://" + extrasBundle.getString("serverIP") + ":5000/move_mouse";
        // unpack the security code from last activity as in IP
        String security_code =  extrasBundle.getString("serverPasswd");
        Request request = new Request.Builder().url(url).build();
        // instantiating network objects
        TouchCoordsDispatcher TCD = new TouchCoordsDispatcher(touchPadView);
        OkHttpClient client = new OkHttpClient();
        WebSocket ws = client.newWebSocket(request, TCD);
        ws.send(security_code);  // establish semi-secure connection with the server
        client.dispatcher().executorService().shutdown();
    }

    // called when the terminate button is clicked
    public void finishActivity(View v){
        finish();
        System.exit(0);
    }
}



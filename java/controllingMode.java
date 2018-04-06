package com.example.lukepatrick.touchtrack2;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.WebSocket;

public class controllingMode extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controlling_mode);
        View touchPadView = findViewById(R.id.Control);
        Intent intentExtras = getIntent();
        Bundle extrasBundle = intentExtras.getExtras();

        Request request = new Request.Builder().url("ws://" + extrasBundle.getString("serverIP") + ":5000/move_mouse").build();
        TouchCoordsDispatcher TCD = new TouchCoordsDispatcher(touchPadView);
        OkHttpClient client = new OkHttpClient();
        WebSocket ws = client.newWebSocket(request, TCD);
        client.dispatcher().executorService().shutdown();
    }

    public void finishActivity(View v){
        finish();
    }

    private void showToast(String text) {
        Toast.makeText(controllingMode.this, text, Toast.LENGTH_SHORT).show();
    }
}



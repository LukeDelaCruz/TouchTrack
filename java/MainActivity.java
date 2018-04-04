package com.example.lukepatrick.touchtrack2;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.net.Socket;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.WebSocket;

public class MainActivity extends AppCompatActivity {

    String serverIP;
    Matcher matcher;
    EditText IPinput;
    Button submitIP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getSupportActionBar().setTitle("Network Configuration Mode");
        IPinput = (EditText) findViewById(R.id.IPinput);
        submitIP = (Button) findViewById(R.id.submitIP);
        submitIP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                serverIP = IPinput.getText().toString();
                matcher = IP_ADDRESS.matcher(serverIP);
                if (matcher.matches()) {
                    showToast(serverIP + " Accepted!");
                    launchActivity();
                }
                else {
                    showToast("Please enter a valid IP address.");
                }
            }
        });
    }

    private void showToast(String text) {
        Toast.makeText(MainActivity.this, text, Toast.LENGTH_SHORT).show();
    }

    // convert to a finite state machine
    public final Pattern IP_ADDRESS
            = Pattern.compile(
            "((25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9])\\.(25[0-5]|2[0-4]"
                    + "[0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1]"
                    + "[0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}"
                    + "|[1-9][0-9]|[0-9]))");

    private void launchActivity() {
        Intent intent = new Intent(this, controllingMode.class);
        Bundle bundle = new Bundle();
        bundle.putString("serverIP", serverIP);  // pass the server IP to the next activity
        intent.putExtras(bundle);
        startActivity(intent);
    }
}

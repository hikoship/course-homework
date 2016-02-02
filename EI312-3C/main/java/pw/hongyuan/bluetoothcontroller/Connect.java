package pw.hongyuan.bluetoothcontroller;


import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.ColorFilter;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.IBinder;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Connect extends ActionBarActivity {

    Button button, button2;
    MyReceiver receiver;
    IBinder serviceBinder;
    MyService mService;
    Intent intent;
    int value = 0;
    private boolean isConnected=false;
    private ListView listView;
    private BluetoothAdapter mBluetoothAdapter = null;
    private TextView textview;
    /**************service 命令*********/
    static final int CMD_STOP_SERVICE = 0x01;
    static final int CMD_SEND_DATA = 0x02;
    static final int CMD_SYSTEM_EXIT =0x03;
    static final int CMD_SHOW_TOAST =0x04;
    static final int CMD_IS_CONNECTED =0x05;
    static final int CMD_ENABLE_BLUETOOTH =0x06;
    static final int CMD_BLUETOOTH_ENABLED =0x07;

    private static final int REQUEST_ENABLE_BT = 2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connect);
        button = (Button) findViewById(R.id.button);
        button2 = (Button) findViewById(R.id.button5);
        textview = (TextView) findViewById(R.id.textView6);
    }



    public void connect(View view){
        if(!isConnected) {
            intent = new Intent(Connect.this,MyService.class);
            startService(intent);

            textview.setText("\nSTATUS: CONNECTING");
            button.setText("  CONNECTING  ");
            button.setEnabled(false);
            button.setTextColor(0xff37474f);
        }
        else{
            stop();
            isConnected=false;
            textview.setText("\nSTATUS: DISCONNECTED");
            button.setText("  CONNECT  ");
            button2.setTextColor(0xff37474f);
        }
    }

    public void buttonEnable(){
        button.setEnabled(true);
        textview.setText("\nSTATUS: CONNECTED");
        button.setTextColor(0xffffffff);
        button.setText("  DISCONNECT  ");
        button2.setTextColor(0xffffffff);
        isConnected=true;
    }

    public void control(View view){
        if(isConnected) {
            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
        }
        else showToast("Connect first.");

    }


    @Override
    protected void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();

        if(receiver!=null){
            Connect.this.unregisterReceiver(receiver);
        }
    }




    @Override
    protected void onResume() {
        // TODO Auto-generated method stub
        super.onResume();
        receiver = new MyReceiver();
        IntentFilter filter=new IntentFilter();
        filter.addAction("android.intent.action.lxx");
        Connect.this.registerReceiver(receiver,filter);
    }

    public void showToast(String str){//显示提示信息
        Toast.makeText(getApplicationContext(), str, Toast.LENGTH_SHORT).show();
    }


    public class MyReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            // TODO Auto-generated method stub
            if(intent.getAction().equals("android.intent.action.lxx")){
                Bundle bundle = intent.getExtras();
                int cmd = bundle.getInt("cmd");

                if(cmd == CMD_SHOW_TOAST){
                    String str = bundle.getString("str");
                    showToast(str);
                }

                else if(cmd == CMD_ENABLE_BLUETOOTH){
                    showToast("enable bt");
                    Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                    startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);


                }
                else if(cmd == CMD_IS_CONNECTED){
                    buttonEnable();
                }

                else if(cmd == CMD_SYSTEM_EXIT){
                    System.exit(0);
                }

            }
        }
    }

    public void stop(){
        Intent intent = new Intent();//创建Intent对象
        intent.setAction("android.intent.action.cmd");
        intent.putExtra("cmd", CMD_STOP_SERVICE);
        sendBroadcast(intent);//发送广播
    }


}

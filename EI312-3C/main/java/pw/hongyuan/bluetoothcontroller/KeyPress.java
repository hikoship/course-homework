package pw.hongyuan.bluetoothcontroller;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.IBinder;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class KeyPress extends ActionBarActivity {

    TextView textview;
    KeyPress.MyReceiver receiver;
    IBinder serviceBinder;
    MyService mService;
    Intent intent;
    int value = 0;
    /**************service 命令*********/
    static final int CMD_STOP_SERVICE = 0x01;
    static final int CMD_SEND_DATA = 0x02;
    static final int CMD_SYSTEM_EXIT =0x03;
    static final int CMD_SHOW_TOAST =0x04;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_key_press);
        textview=(TextView) findViewById(R.id.textView2);
    }

    public void stop(View view){
        byte command = 0x00;
        sendCmd(command);

        textview.setText("STOP");
    }

    public void drive(View view){
        byte command = 0x01;
        sendCmd(command);

        textview.setText("↑");
    }

    public void reverse(View view){
        byte command = 0x02;
        sendCmd(command);
        textview.setText("↓");
    }

    public void left(View view){
        byte command = 0x03;
        sendCmd(command);
        textview.setText("←");
    }

    public void right(View view){
        byte command = 0x04;
        sendCmd(command);
        textview.setText("→");
    }

    @Override
    protected void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();

        if(receiver!=null){
            KeyPress.this.unregisterReceiver(receiver);
        }
    }




    @Override
    protected void onResume() {
        // TODO Auto-generated method stub
        super.onResume();
        receiver = new MyReceiver();
        IntentFilter filter=new IntentFilter();
        filter.addAction("android.intent.action.lxx");
        KeyPress.this.registerReceiver(receiver,filter);
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

                else if(cmd == CMD_SYSTEM_EXIT){
                    System.exit(0);
                }

            }
        }
    }
    @Override
    protected void onPause() {
        super.onPause();
        byte command = 0x00;
        sendCmd(command);
    }
    public void sendCmd(byte command){
        Intent intent = new Intent();//创建Intent对象
        intent.setAction("android.intent.action.cmd");
        intent.putExtra("cmd", CMD_SEND_DATA);
        intent.putExtra("command", command);
        sendBroadcast(intent);//发送广播
    }

}

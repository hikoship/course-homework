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


public class MainActivity extends ActionBarActivity {

    TextView myTextView;
    MainActivity.MyReceiver receiver;
    IBinder serviceBinder;
    MyService mService;
    Intent intent;
    int value = 0;
    /**************service 命令*********/
    static final int CMD_STOP_SERVICE = 0x01;
    static final int CMD_SEND_DATA = 0x02;
    static final int CMD_SYSTEM_EXIT =0x03;
    static final int CMD_SHOW_TOAST =0x04;

    public void keyPress(View view){
        Intent intent = new Intent(this, KeyPress.class);
        startActivity(intent);
    }

    public void joystick(View view){
        Intent intent = new Intent(this, Joystick.class);
        startActivity(intent);
    }
    public void gravity(View view){
        Intent intent = new Intent(this, Gravity.class);
        startActivity(intent);
    }

    public void voice(View view){
        Intent intent = new Intent(this, Voice.class);
        startActivity(intent);
    }

    public void gesture(View view){
        Intent intent = new Intent(this, Gesture.class);
        startActivity(intent);
    }

    public void webcam(View view){
        Intent intent = new Intent(this, WebCam.class);
        startActivity(intent);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }



    @Override
    protected void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();

        if(receiver!=null){
            MainActivity.this.unregisterReceiver(receiver);
        }
    }




    @Override
    protected void onResume() {
        // TODO Auto-generated method stub
        super.onResume();
        receiver = new MyReceiver();
        IntentFilter filter=new IntentFilter();
        filter.addAction("android.intent.action.lxx");
        MainActivity.this.registerReceiver(receiver,filter);
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

}

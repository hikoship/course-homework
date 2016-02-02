package pw.hongyuan.bluetoothcontroller;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.IBinder;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.WindowManager;
import android.widget.CheckBox;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

public class Gravity extends ActionBarActivity {

    private SensorManager mSensorManager;
    private Sensor mSensor;
    private SensorEventListener mListener;
    private TextView textview;
    private TextView textviewD;

    private ImageView stop;
    private ImageView leftBox1;
    private ImageView leftBox2;
    private ImageView leftArrow;
    private ImageView upBox1;
    private ImageView upBox2;
    private ImageView upArrow;
    private ImageView rightBox1;
    private ImageView rightBox2;
    private ImageView rightArrow;
    private ImageView downBox1;
    private ImageView downBox2;
    private ImageView downArrow;


    private byte status=0x00;

    Gravity.MyReceiver receiver;
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
        setContentView(R.layout.activity_gravity);

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);   //应用运行时，保持屏幕高亮，不锁屏

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        mSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION);

        textview = (TextView) findViewById(R.id.textView);
        stop = (ImageView) findViewById(R.id.imageView4);
        leftBox1 = (ImageView) findViewById(R.id.imageView5);
        leftBox2 = (ImageView) findViewById(R.id.imageView6);
        leftArrow = (ImageView) findViewById(R.id.imageView7);
        upBox1 = (ImageView) findViewById(R.id.imageView8);
        upBox2 = (ImageView) findViewById(R.id.imageView9);
        upArrow = (ImageView) findViewById(R.id.imageView10);
        rightBox1 = (ImageView) findViewById(R.id.imageView11);
        rightBox2 = (ImageView) findViewById(R.id.imageView12);
        rightArrow = (ImageView) findViewById(R.id.imageView13);
        downBox1 = (ImageView) findViewById(R.id.imageView14);
        downBox2 = (ImageView) findViewById(R.id.imageView15);
        downArrow = (ImageView) findViewById(R.id.imageView16);



        mListener = new SensorEventListener() {
            public void onAccuracyChanged(Sensor sensor, int accuracy) {

            }
            public void onSensorChanged(SensorEvent event) {
                float x = event.values[1];
                float y = event.values[2];


                textview.setText("X: "+String.valueOf(x)+"\nY: "+String.valueOf(y));

                //DRIVE
                if(x>-40&&x<=-20&&y>-20&&y<20){
                    if(status!=0x11){
                        status=0x11;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.VISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }
                else if(x>-20&&x<=0&&y>-20&&y<20){
                    if(status!=0x12){
                        status=0x12;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.VISIBLE);
                        upBox2.setVisibility(View.VISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }
                else if(x>0&&y>-20&&y<20){
                    if(status!=0x01){
                        status=0x01;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.VISIBLE);
                        upBox2.setVisibility(View.VISIBLE);
                        upArrow.setVisibility(View.VISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);

                    }
                }

                //REVERSE
                else if(x<=-60&&x>-80&&y>-20&&y<20){
                    if(status!=0x21){
                        status=0x21;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.VISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }
                else if(x<=-80&&x>-100&&y>-20&&y<20){
                    if(status!=0x22){
                        status=0x22;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.VISIBLE);
                        downBox2.setVisibility(View.VISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }
                else if(x<=-100&&y>-20&&y<20){
                    if(status!=0x02){
                        status=0x02;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.VISIBLE);
                        downBox2.setVisibility(View.VISIBLE);
                        downArrow.setVisibility(View.VISIBLE);
                        sendCmd(command);
                    }
                }

                //LEFT
                else if(y>=20&&y<40){
                    if(status!=0x31){
                        status=0x31;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.VISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }
                else if(y>=40&&y<60){
                    if(status!=0x32){
                        status=0x32;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.VISIBLE);
                        leftBox2.setVisibility(View.VISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }
                else if(y>=60){
                    if(status!=0x03){
                        status=0x03;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.VISIBLE);
                        leftBox2.setVisibility(View.VISIBLE);
                        leftArrow.setVisibility(View.VISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }

                //RIGHT
                else if(y<=-20&&y>-40){
                    if(status!=0x41){
                        status=0x41;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.VISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }
                else if(y<=-40&&y>-60){
                    if(status!=0x42){
                        status=0x42;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.VISIBLE);
                        rightBox2.setVisibility(View.VISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }
                else if(y<=-60){
                    if(status!=0x04){
                        status=0x04;
                        byte command=status;
                        stop.setVisibility(View.INVISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.VISIBLE);
                        rightBox2.setVisibility(View.VISIBLE);
                        rightArrow.setVisibility(View.VISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }

                //STOP
                else{
                    if(status!=0x00){
                        status=0x00;
                        byte command=status;
                        stop.setVisibility(View.VISIBLE);
                        leftBox1.setVisibility(View.INVISIBLE);
                        leftBox2.setVisibility(View.INVISIBLE);
                        leftArrow.setVisibility(View.INVISIBLE);
                        upBox1.setVisibility(View.INVISIBLE);
                        upBox2.setVisibility(View.INVISIBLE);
                        upArrow.setVisibility(View.INVISIBLE);
                        rightBox1.setVisibility(View.INVISIBLE);
                        rightBox2.setVisibility(View.INVISIBLE);
                        rightArrow.setVisibility(View.INVISIBLE);
                        downBox1.setVisibility(View.INVISIBLE);
                        downBox2.setVisibility(View.INVISIBLE);
                        downArrow.setVisibility(View.INVISIBLE);
                        sendCmd(command);
                    }
                }

            }
        };
        mSensorManager.registerListener(mListener, mSensor, mSensorManager.SENSOR_DELAY_GAME);
    }


    @Override
    protected void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();

        if(receiver!=null){
            Gravity.this.unregisterReceiver(receiver);
        }
    }



    @Override
    protected void onPause() {
        super.onPause();
        byte command = 0x00;
        sendCmd(command);
        mSensorManager.unregisterListener( mListener);
    }

    @Override
    protected void onResume() {
        // TODO Auto-generated method stub
        super.onResume();
        receiver = new MyReceiver();
        IntentFilter filter=new IntentFilter();
        filter.addAction("android.intent.action.lxx");
        Gravity.this.registerReceiver(receiver,filter);
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

    public void sendCmd(byte command){
        Intent intent = new Intent();//创建Intent对象
        intent.setAction("android.intent.action.cmd");
        intent.putExtra("cmd", CMD_SEND_DATA);
        intent.putExtra("command", command);
        sendBroadcast(intent);//发送广播
    }

}

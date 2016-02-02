package pw.hongyuan.bluetoothcontroller;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.GestureDetector;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.widget.TextView;


public class Gesture extends ActionBarActivity implements GestureDetector.OnGestureListener,GestureDetector.OnDoubleTapListener {

    private int verticalMinDistance = 180;
    private int minVelocity         = 0;
    private TextView textview;
    private GestureDetector gd;
    /**************service 命令*********/
    static final int CMD_STOP_SERVICE = 0x01;
    static final int CMD_SEND_DATA = 0x02;
    static final int CMD_SYSTEM_EXIT =0x03;
    static final int CMD_SHOW_TOAST =0x04;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gesture);
        textview = (TextView)findViewById(R.id.textView3);
        gd = new GestureDetector(this,this);
        gd.setOnDoubleTapListener(this);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event){
        this.gd.onTouchEvent(event);
        // Be sure to call the superclass implementation
        return super.onTouchEvent(event);
    }

    @Override
    public boolean onDown(MotionEvent e) {
        return false;
    }

    @Override
    public void onShowPress(MotionEvent e) {

    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        return false;
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {
        return false;
    }

    @Override
    public void onLongPress(MotionEvent e) {

    }

    public boolean onFling(MotionEvent event1, MotionEvent event2,
                           float velocityX, float velocityY) {

        if (event1.getX() - event2.getX() > verticalMinDistance && event1.getX() - event2.getX() > Math.abs(event1.getY()-event2.getY()) && Math.abs(velocityX) > minVelocity) {
            byte command = 0x03;
            sendCmd(command);
            textview.setText("←");
        } else if (event2.getX() - event1.getX() > verticalMinDistance && event2.getX() - event1.getX() > Math.abs(event1.getY()-event2.getY()) && Math.abs(velocityX) > minVelocity) {
            byte command = 0x04;
            sendCmd(command);
            textview.setText("→");
        }

        if (event1.getY() - event2.getY() > verticalMinDistance && event1.getY() - event2.getY() > Math.abs(event1.getX()-event2.getX()) && Math.abs(velocityY) > minVelocity) {
            byte command = 0x01;
            sendCmd(command);
            textview.setText("↑");
        } else if (event2.getY() - event1.getY() > verticalMinDistance && event2.getY() - event1.getY() > Math.abs(event1.getX()-event2.getX()) && Math.abs(velocityY) > minVelocity) {
            byte command = 0x02;
            sendCmd(command);
            textview.setText("↓");
        }

        return true;

    }

    @Override
    public boolean onDoubleTap(MotionEvent event) {
        byte command = 0x00;
        sendCmd(command);
        textview.setText("STOP");
        return true;
    }

    @Override
    public boolean onDoubleTapEvent(MotionEvent event) {
        return false;
    }

    @Override
    public boolean onSingleTapConfirmed(MotionEvent event) {
        return false;
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

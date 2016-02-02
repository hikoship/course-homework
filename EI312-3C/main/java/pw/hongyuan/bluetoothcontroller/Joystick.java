package pw.hongyuan.bluetoothcontroller;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.GestureDetector;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.RelativeLayout;
import android.widget.TextView;


public class Joystick extends ActionBarActivity implements GestureDetector.OnGestureListener,GestureDetector.OnDoubleTapListener  {

    ImageButton point;
    TextView textview;
    private GestureDetector gd;
    /**************service 命令*********/
    static final int CMD_STOP_SERVICE = 0x01;
    static final int CMD_SEND_DATA = 0x02;
    static final int CMD_SYSTEM_EXIT =0x03;
    static final int CMD_SHOW_TOAST =0x04;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_joystick);
        textview = (TextView)findViewById(R.id.textView5);
        point = (ImageButton)findViewById(R.id.imageButton6);
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
        textview.setText("X: "+String.valueOf(e.getX())+"\nY: "+String.valueOf(e.getY()));
        return true;
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

        textview.setText("X: "+String.valueOf(e2.getX())+"\nY: "+String.valueOf(e2.getY()));

        ViewGroup.MarginLayoutParams margin=new ViewGroup.MarginLayoutParams(point.getLayoutParams());
        margin.setMargins((int)e2.getX()-margin.width,margin.topMargin, (int)e2.getX(), margin.bottomMargin);
        RelativeLayout.LayoutParams layoutParams = new RelativeLayout.LayoutParams(margin);
        point.setLayoutParams(layoutParams);
        return true;
    }

    @Override
    public void onLongPress(MotionEvent e) {

    }

    public boolean onFling(MotionEvent event1, MotionEvent event2,
                           float velocityX, float velocityY) {return false;    }

    @Override
    public boolean onDoubleTap(MotionEvent event) {return false;    }

    @Override
    public boolean onDoubleTapEvent(MotionEvent event) {
        return false;
    }

    @Override
    public boolean onSingleTapConfirmed(MotionEvent event) {
        return false;
    }

    public void sendCmd(byte command){
        Intent intent = new Intent();//创建Intent对象
        intent.setAction("android.intent.action.cmd");
        intent.putExtra("cmd", CMD_SEND_DATA);
        intent.putExtra("command", command);
        sendBroadcast(intent);//发送广播
    }
}

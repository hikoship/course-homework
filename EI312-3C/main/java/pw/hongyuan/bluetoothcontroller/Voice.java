package pw.hongyuan.bluetoothcontroller;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.IBinder;
import android.speech.RecognizerIntent;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;


public class Voice extends ActionBarActivity {

    TextView myTextView;
    Voice.MyReceiver receiver;
    IBinder serviceBinder;
    MyService mService;
    Intent intent;
    int value = 0;
    /**************service 命令*********/
    static final int CMD_STOP_SERVICE = 0x01;
    static final int CMD_SEND_DATA = 0x02;
    static final int CMD_SYSTEM_EXIT =0x03;
    static final int CMD_SHOW_TOAST =0x04;

    protected static final int RESULT_SPEECH = 1;

    private Spinner spinner;
    private ImageButton btnSpeak;
    private TextView txtText;
    public String string="";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_voice);
        spinner = (Spinner) findViewById(R.id.spinner);

        txtText = (TextView) findViewById(R.id.textView);

        btnSpeak = (ImageButton) findViewById(R.id.imageButton7);

        btnSpeak.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {

                String language="";


                Intent intent = new Intent(
                        RecognizerIntent.ACTION_RECOGNIZE_SPEECH);


                switch(spinner.getSelectedItemPosition()){
                    case 0:{
                        language="en-US";
                        break;
                    }

                    case 1:{
                        language="zh-CN";
                        break;
                    }

                    case 2:{
                        language="ja-JP";
                        break;
                    }
                }
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,language);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, language);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, language);
                //intent.putExtra(RecognizerIntent.EXTRA_ONLY_RETURN_LANGUAGE_PREFERENCE, language);


                try {
                    startActivityForResult(intent, RESULT_SPEECH);
                    txtText.setText("");
                } catch (ActivityNotFoundException a) {
                    Toast t = Toast.makeText(getApplicationContext(),
                            "Opps! Your device doesn't support Speech to Text",
                            Toast.LENGTH_SHORT);
                    t.show();
                }
            }
        });

    }


    @Override
    protected void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();

        if(receiver!=null){
            Voice.this.unregisterReceiver(receiver);
        }
    }




    @Override
    protected void onResume() {
        // TODO Auto-generated method stub
        super.onResume();
        receiver = new MyReceiver();
        IntentFilter filter=new IntentFilter();
        filter.addAction("android.intent.action.lxx");
        Voice.this.registerReceiver(receiver,filter);
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

    @Override
    protected void onPause() {
        super.onPause();
        byte command = 0x00;
        sendCmd(command);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode) {
            case RESULT_SPEECH: {
                if (resultCode == RESULT_OK && null != data) {

                    ArrayList<String> text = data
                            .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);

                    txtText.setText(text.get(0));


                    String string;
                    string=txtText.getText().toString();
                    if(string.equals("stop")){
                        byte command=0x00;
                        sendCmd(command);
                    }
                    if(string.equals("forward")||string.equals("drive")||string.equals("go")){
                        byte command=0x01;
                        sendCmd(command);
                    }
                    if(string.equals("reverse")||string.equals("go back")||string.equals("back")||string.equals("backward")){
                        byte command=0x02;
                        sendCmd(command);
                    }
                    if(string.equals("left")||string.equals("turn left")){
                        byte command=0x03;
                        sendCmd(command);
                    }
                    if(string.equals("right")||string.equals("turn right")){
                        byte command=0x04;
                        sendCmd(command);
                    }
                }
                break;
            }

        }
    }

}

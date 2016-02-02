package pw.hongyuan.bluetoothcontroller;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;


public class WebCam extends Activity {

    private WebView webHolder;
    private WebSettings settings;
    private WebViewClient client;
    static final int CMD_STOP_SERVICE = 0x01;
    static final int CMD_SEND_DATA = 0x02;
    static final int CMD_SYSTEM_EXIT =0x03;
    static final int CMD_SHOW_TOAST =0x04;
    WebCam.MyReceiver receiver;

    public void stop(View view){
        byte command = 0x00;
        sendCmd(command);

    }

    public void drive(View view){
        byte command = 0x01;
        sendCmd(command);

    }

    public void reverse(View view){
        byte command = 0x02;
        sendCmd(command);

    }

    public void left(View view){
        byte command = 0x03;
        sendCmd(command);
    }

    public void right(View view){
        byte command = 0x04;
        sendCmd(command);

    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_web_cam);
        webHolder = (WebView) findViewById(R.id.webview);
        settings = webHolder.getSettings();
        client = new OwnerWebView();

        settings.setDefaultTextEncodingName("UTF-8");
        settings.setJavaScriptEnabled(true);
        webHolder.setWebViewClient(client);

        webHolder.loadUrl("http://192.168.43.1:8080/browserfs.html");
    }

    private class OwnerWebView extends WebViewClient{

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            view.loadUrl(url);
            return true;
        }

    }

    @Override
    protected void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();

        if(receiver!=null){
            WebCam.this.unregisterReceiver(receiver);
        }
    }


    @Override
    protected void onResume() {
        // TODO Auto-generated method stub
        super.onResume();
        receiver = new MyReceiver();
        IntentFilter filter=new IntentFilter();
        filter.addAction("android.intent.action.lxx");
        WebCam.this.registerReceiver(receiver,filter);
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
    public void showToast(String str){//显示提示信息
        Toast.makeText(getApplicationContext(), str, Toast.LENGTH_SHORT).show();
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

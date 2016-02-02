package pw.hongyuan.bluetoothcontroller;



import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.UUID;

import android.app.Activity;
import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;

public class MyService extends Service {

    public boolean threadFlag = true;
    MyThread myThread;
    CommandReceiver cmdReceiver;//继承自BroadcastReceiver对象，用于得到Activity发送过来的命令

    /**************service 命令*********/
    static final int CMD_STOP_SERVICE = 0x01;
    static final int CMD_SEND_DATA = 0x02;
    static final int CMD_SYSTEM_EXIT =0x03;
    static final int CMD_SHOW_TOAST =0x04;
    static final int CMD_IS_CONNECTED =0x05;
    static final int CMD_ENABLE_BLUETOOTH =0x06;
    static final int CMD_BLUETOOTH_ENABLED =0x07;

    private BluetoothAdapter mBluetoothAdapter = null;
    private BluetoothSocket btSocket = null;
    private OutputStream outStream = null;
    private InputStream inStream = null;
    public  boolean bluetoothFlag  = true;
    private static final UUID MY_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    private static String address = "98:D3:31:40:0A:0A"; // <==要连接的蓝牙设备MAC地址

    private static final int REQUEST_ENABLE_BT = 2;

    @Override
    public IBinder onBind(Intent intent) {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public void onCreate() {
        // TODO Auto-generated method stub
        super.onCreate();

    }



    //前台Activity调用startService时，该方法自动执行
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // TODO Auto-generated method stub
        cmdReceiver = new CommandReceiver();
        IntentFilter filter = new IntentFilter();//创建IntentFilter对象
        //注册一个广播，用于接收Activity传送过来的命令，控制Service的行为，如：发送数据，停止服务等
        filter.addAction("android.intent.action.cmd");
        //注册Broadcast Receiver
        registerReceiver(cmdReceiver, filter);
        doJob();//调用方法启动线程
        return super.onStartCommand(intent, flags, startId);

    }



    @Override
    public void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();
        this.unregisterReceiver(cmdReceiver);//取消注册的CommandReceiver
        threadFlag = false;
        boolean retry = true;
        while(retry){
            try{
                myThread.join();
                retry = false;
            }catch(Exception e){
                e.printStackTrace();
            }

        }
    }

    public class MyThread extends Thread{
        @Override
        public void run() {
            // TODO Auto-generated method stub
            super.run();
            while(!mBluetoothAdapter.isEnabled()){
                try{
                    myThread.sleep(100);
                } catch(InterruptedException e){
                    DisplayToast("Sleep failed");
                }
            }
            connectDevice();//连接蓝牙设备

            Intent intent = new Intent();//创建Intent对象
            intent.putExtra("cmd", CMD_IS_CONNECTED);
            intent.setAction("android.intent.action.lxx");
            sendBroadcast(intent);
        }
    }

    public void doJob(){
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (mBluetoothAdapter == null) {
            bluetoothFlag  = false;
            return;
        }

        if (!mBluetoothAdapter.isEnabled()) {
            Intent intent = new Intent();//创建Intent对象
            intent.putExtra("cmd", CMD_ENABLE_BLUETOOTH);
            intent.setAction("android.intent.action.lxx");
            sendBroadcast(intent);
        }
        threadFlag = true;
        myThread = new MyThread();
        myThread.start();

    }
    public  void connectDevice(){
        BluetoothDevice device = mBluetoothAdapter.getRemoteDevice(address);
        try {
            btSocket = device.createRfcommSocketToServiceRecord(MY_UUID);
        } catch (IOException e) {
            bluetoothFlag = false;
        }
        if(btSocket==null) DisplayToast("no socket");
        mBluetoothAdapter.cancelDiscovery();
        try {
            btSocket.connect();
            bluetoothFlag = true;
        } catch (IOException e) {
            try {
                btSocket.close();
                bluetoothFlag = false;
            } catch (IOException e2) {
            }
        }

        if(bluetoothFlag){
            try {
                inStream = btSocket.getInputStream();
            } catch (IOException e) {
                e.printStackTrace();
            } //绑定读接口

            try {
                outStream = btSocket.getOutputStream();
            } catch (IOException e) {
                e.printStackTrace();
            } //绑定写接口

        }
    }

    public void sendCmd(byte cmd)//串口发送数据
    {
        if(!bluetoothFlag){
            return;
        }
        byte[] msgBuffer = new byte[1];
        msgBuffer[0] = cmd;

        try {
            outStream.write(msgBuffer);
            outStream.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }



    public void stopService(){//停止服务
        threadFlag = false;//停止线程
        showToast("关闭service");

        try {
            btSocket.close();
        } catch (IOException e){
            showToast("关闭service失败");
        }
        stopSelf();//停止服务
    }

    public void showToast(String str){//显示提示信息
        Intent intent = new Intent();
        intent.putExtra("cmd", CMD_SHOW_TOAST);
        intent.putExtra("str", str);
        intent.setAction("android.intent.action.lxx");
        sendBroadcast(intent);
    }

    public void DisplayToast(String str)
    {
        Log.d("Season", str);
    }

    //接收Activity传送过来的命令
    private class CommandReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            if(intent.getAction().equals("android.intent.action.cmd")){
                int cmd = intent.getIntExtra("cmd", -1);//获取Extra信息
                if(cmd == CMD_STOP_SERVICE){
                    stopService();
                }

                if(cmd == CMD_SEND_DATA)
                {
                    byte command = intent.getByteExtra("command", (byte) 0);
                    sendCmd(command);
                }

            }
        }
    }



}
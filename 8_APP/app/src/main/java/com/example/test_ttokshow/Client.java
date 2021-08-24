package com.example.test_ttokshow;

import android.app.Application;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
    public class Client extends AppCompatActivity {
        private static String[] output;
        static String send;
        static Boolean cam = false;
        public static void main(String... args) {
            try (Socket client = new Socket()) {
                InetSocketAddress ipep = new InetSocketAddress("13.59.29.176", 9999);
                //3.144.33.17
                //13.59.29.176
                client.connect(ipep);
                try (OutputStream sender = client.getOutputStream(); InputStream receiver = client.getInputStream()) {

                    for (int i = 0; i < 1; i++) {

                        if (cam){
                            byte[] data = send.getBytes();
                            ByteBuffer b = ByteBuffer.allocate(4);
                            b.order(ByteOrder.LITTLE_ENDIAN);
                            b.putInt(data.length);
                            sender.write(b.array(),0,4);
                            sender.write(data);
                            cam = false;
                        }

                        byte[] data = new byte[4];
                        sender.write(data,0,4);
                        receiver.read(data, 0, 4);
                        ByteBuffer bu = ByteBuffer.wrap(data);
                        bu.order(ByteOrder.LITTLE_ENDIAN);

                        int length = bu.getInt();
                        data = new byte[length];
                        receiver.read(data, 0, length);

                        String msg = new String(data, "UTF-8");
                        output = msg.split("#");
                    }

                }
            } catch (Throwable e) {
                e.printStackTrace();
            }
        }
        static String[] getOutput(){
            return output;
        }

    }


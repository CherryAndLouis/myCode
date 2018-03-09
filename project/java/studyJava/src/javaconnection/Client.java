package javaconnection;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.channels.ServerSocketChannel;

public class Client {
	public static final String ip_addr = "localhost";
	public static final int port = 23456;

	public static void main(String[] args) {
		System.out.println("客户端启动中。。。");
		while (true) {
			Socket socket = null;
			try {
				socket = new Socket(ip_addr, port);
				DataInputStream dataInputStream = new DataInputStream(socket.getInputStream());
				DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
				System.out.println("请输入要向服务端发送的内容：");
				String data = new BufferedReader(new InputStreamReader(System.in)).readLine();
				dataOutputStream.writeUTF(data);
				String outdata = dataInputStream.readUTF();
				System.out.println("服务器端返回过来的是: " + outdata);
				dataInputStream.close();
				dataOutputStream.close();
			} catch (UnknownHostException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} finally {
				if (socket != null) {
					try {
						socket.close();
					} catch (IOException e) {
						socket = null;
						System.out.println("客户端 finally 异常:" + e.getMessage());
					}
				}
			}
		}
	}
}

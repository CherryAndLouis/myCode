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
		System.out.println("�ͻ��������С�����");
		while (true) {
			Socket socket = null;
			try {
				socket = new Socket(ip_addr, port);
				DataInputStream dataInputStream = new DataInputStream(socket.getInputStream());
				DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
				System.out.println("������Ҫ�����˷��͵����ݣ�");
				String data = new BufferedReader(new InputStreamReader(System.in)).readLine();
				dataOutputStream.writeUTF(data);
				String outdata = dataInputStream.readUTF();
				System.out.println("�������˷��ع�������: " + outdata);
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
						System.out.println("�ͻ��� finally �쳣:" + e.getMessage());
					}
				}
			}
		}
	}
}

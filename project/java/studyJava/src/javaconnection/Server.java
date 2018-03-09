package javaconnection;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

import javax.xml.stream.events.StartDocument;
import javax.xml.ws.handler.MessageContext.Scope;



public class Server {
	private static final int port = 23456;
	
	public static void main(String[] args) {
		System.out.println("服务器启动...");
		Server server = new Server();
		server.init();
	}
	public void init() {
		try {
			ServerSocket serverSocket = new ServerSocket(port);
			while(true) {
				Socket client = serverSocket.accept();
				new HanderThread(client);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	public class HanderThread implements Runnable {
		private Socket socket ;
		public HanderThread(Socket client) {
			socket=client;
			new Thread(this).start();
		}
			public void run() {
				try {
					DataInputStream dataInputStream = new DataInputStream(socket.getInputStream());
					String data = dataInputStream.readUTF();
					System.out.println("客户端的信息为"+data);
					DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
					System.out.println("请输入：");
					String input = new BufferedReader(new InputStreamReader(System.in)).readLine();
					dataOutputStream.writeUTF(input);
					dataInputStream.close();
					dataOutputStream.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				finally{
					if (socket != null) {    
	                    try {    
	                        socket.close();    
	                    } catch (Exception e) {    
	                        socket = null;    
	                        System.out.println("服务端 finally 异常:" + e.getMessage());    
	                    }
				}
			}
		}
	}
}

package BytesIO;

import java.io.UnsupportedEncodingException;

public class EncodeTest {

	public static void main(String[] args) throws UnsupportedEncodingException {
		// TODO Auto-generated method stub
		String name ="刘新宇louis";
		//以项目默认的编码格式转化成字节
		byte[] bytes = name.getBytes();
		for (byte b : bytes) {
			//GBK编码格式中文是占用两个字节，英文是占用一个字节
			System.out.print(Integer.toHexString(b & 0xff) + " ");
		}
		System.out.println();
		//以UF-8编码格式转换成字节
		byte[] bytes1 = name.getBytes("utf-8");
		//以什么编码格式转换的字节就要以什么编码格式转换成字符串，不然会出现乱码
		String name1  = new String(bytes1,"utf-8");
		System.out.println(name1);
		for (byte b : bytes1) {
			//utf-8编码格式中文占用三个字节，英文占用一个字节
			System.out.print(Integer.toHexString(b & 0xff) + " ");
		}
		System.out.println();
		//java 是双字节编码，是utf-16be编码格式
		byte[] bytes2=name.getBytes("utf-16be");
		for (byte b : bytes2) {
			//utf-16be编码格式中文占用两个字节，英文占用两个字节
			System.out.print(Integer.toHexString(b & 0xff) + " ");
		}
	}

}

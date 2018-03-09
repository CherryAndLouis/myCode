package BytesIO;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.Arrays;

public class RafDemo {

	public static void main(String[] args) throws IOException{
		// TODO Auto-generated method stub
		File demo =  new File("Demo");
		File file = new File(demo,"test.dat");
		if (!demo.exists()) {
			demo.mkdir();
		}
		if (!file.exists()) {
			file.createNewFile();
		}
		RandomAccessFile raf = new RandomAccessFile(file, "rw");
		System.out.println(raf.getFilePointer());
		raf.write('A');
		System.out.println(raf.getFilePointer());
		raf.write('B');
		int i = 0x7fffffff;
		//��write����ÿ��ֻ��дһ���ֽڣ����Ҫ��iд��ȥ�͵�д4��
		raf.write(i >>> 24);//��8λ
		raf.write(i >>> 16);
		raf.write(i >>> 8);
		raf.write(i);
		System.out.println(raf.getFilePointer());
		raf.writeInt(i);
		System.out.println(raf.getFilePointer());
		
		String s = "��";
		byte[] gbk = s.getBytes("gbk");
		raf.write(gbk);
		System.out.println(raf.getFilePointer());
		System.out.println(raf.length());
		
		raf.seek(0);
		byte[] buf = new byte[(int)raf.length()];
		raf.read(buf);
		System.out.println(Arrays.toString(buf));
		for (byte b : buf) {
			System.out.println(Integer.toHexString(b & 0xff)+" ");
		}
	    raf.close();
	}

}

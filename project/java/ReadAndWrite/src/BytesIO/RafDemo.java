package BytesIO;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;

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
		
	}

}

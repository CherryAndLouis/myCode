package BytesIO;

import java.io.File;
import java.io.IOException;

public class FileUiltsTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		File file = new File("E:\\ДњТы\\git\\myCode");
		FileUtils test = new FileUtils();
		try {
			test.listDiretory(file);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}

package BytesIO;

import java.io.File;
import java.io.IOException;

//�г�file��һЩ�����ò�����������ˣ������ȵ�
public class FileUtils {
	public static void listDiretory(File dir) throws IOException {
		if (!dir.exists()) {
			throw new IllegalArgumentException("Ŀ¼"+dir + "������");
		}
		if(!dir.isDirectory()) {
			throw new IllegalArgumentException(dir + "����һ��Ŀ¼");
		}
		File[] files = dir.listFiles();
		if (files!=null && files.length>0) {
			for (File file : files) {
				if (file.isDirectory()) {
					listDiretory(file);
				}
				System.out.println(file);
			}
		}
	}
}

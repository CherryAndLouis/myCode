package BytesIO;

import java.io.File;
import java.io.IOException;

//列出file的一些厂常用操作，比如过滤，遍历等等
public class FileUtils {
	public static void listDiretory(File dir) throws IOException {
		if (!dir.exists()) {
			throw new IllegalArgumentException("目录"+dir + "不存在");
		}
		if(!dir.isDirectory()) {
			throw new IllegalArgumentException(dir + "不是一个目录");
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

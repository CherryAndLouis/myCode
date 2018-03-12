package BytesIO;

import java.io.File;
import java.io.IOException;

public class FileDemo {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		File file = new File("E:\\代码\\git\\myCode\\project\\java\\test");
		//判断是文件或者目录是否存在
		System.out.println(file.exists());
		//判断file对象是否是一个目录
		System.out.println(file.isDirectory());
		//判断file对象是否是一个文件
		System.out.println(file.isFile());
		if (!file.exists()) {
			//如果对象不存在的话，创建目录
			file.mkdir();//mkdirs()创建多级目录
		}
		else {
			//删除目录
			file.delete();
		}
		
		//file对象表示的是一个文件
		//File file2 = new File("e:\\javaio\\日记1.txt");
		File file2 = new File("E:\\代码\\git\\myCode\\project\\java\\test","日记1.txt");
		if (!file2.exists()) {
			try {
				//如果文件不存在，创建一个新的文件
				file2.createNewFile();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		else {
			file2.delete();
		}
		
		
		 //常用的File对象的API
		System.out.println(file);//file.toString()的内容
		System.out.println(file.getAbsolutePath());
		System.out.println(file.getName());
		System.out.println(file2.getName());
		System.out.println(file.getParent());
		System.out.println(file2.getParent());
		System.out.println(file.getParentFile().getAbsolutePath());
	}

}

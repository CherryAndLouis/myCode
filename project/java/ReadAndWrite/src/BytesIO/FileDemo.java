package BytesIO;

import java.io.File;
import java.io.IOException;

public class FileDemo {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		File file = new File("E:\\����\\git\\myCode\\project\\java\\test");
		//�ж����ļ�����Ŀ¼�Ƿ����
		System.out.println(file.exists());
		//�ж�file�����Ƿ���һ��Ŀ¼
		System.out.println(file.isDirectory());
		//�ж�file�����Ƿ���һ���ļ�
		System.out.println(file.isFile());
		if (!file.exists()) {
			//������󲻴��ڵĻ�������Ŀ¼
			file.mkdir();//mkdirs()�����༶Ŀ¼
		}
		else {
			//ɾ��Ŀ¼
			file.delete();
		}
		
		//file�����ʾ����һ���ļ�
		//File file2 = new File("e:\\javaio\\�ռ�1.txt");
		File file2 = new File("E:\\����\\git\\myCode\\project\\java\\test","�ռ�1.txt");
		if (!file2.exists()) {
			try {
				//����ļ������ڣ�����һ���µ��ļ�
				file2.createNewFile();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		else {
			file2.delete();
		}
		
		
		 //���õ�File�����API
		System.out.println(file);//file.toString()������
		System.out.println(file.getAbsolutePath());
		System.out.println(file.getName());
		System.out.println(file2.getName());
		System.out.println(file.getParent());
		System.out.println(file2.getParent());
		System.out.println(file.getParentFile().getAbsolutePath());
	}

}

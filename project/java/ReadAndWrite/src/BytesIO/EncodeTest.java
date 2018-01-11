package BytesIO;

import java.io.UnsupportedEncodingException;

public class EncodeTest {

	public static void main(String[] args) throws UnsupportedEncodingException {
		// TODO Auto-generated method stub
		String name ="������louis";
		//����ĿĬ�ϵı����ʽת�����ֽ�
		byte[] bytes = name.getBytes();
		for (byte b : bytes) {
			//GBK�����ʽ������ռ�������ֽڣ�Ӣ����ռ��һ���ֽ�
			System.out.print(Integer.toHexString(b & 0xff) + " ");
		}
		System.out.println();
		//��UF-8�����ʽת�����ֽ�
		byte[] bytes1 = name.getBytes("utf-8");
		//��ʲô�����ʽת�����ֽھ�Ҫ��ʲô�����ʽת�����ַ�������Ȼ���������
		String name1  = new String(bytes1,"utf-8");
		System.out.println(name1);
		for (byte b : bytes1) {
			//utf-8�����ʽ����ռ�������ֽڣ�Ӣ��ռ��һ���ֽ�
			System.out.print(Integer.toHexString(b & 0xff) + " ");
		}
		System.out.println();
		//java ��˫�ֽڱ��룬��utf-16be�����ʽ
		byte[] bytes2=name.getBytes("utf-16be");
		for (byte b : bytes2) {
			//utf-16be�����ʽ����ռ�������ֽڣ�Ӣ��ռ�������ֽ�
			System.out.print(Integer.toHexString(b & 0xff) + " ");
		}
	}

}

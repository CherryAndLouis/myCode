package PokeGame;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

import javax.print.DocFlavor.INPUT_STREAM;
import javax.sql.rowset.FilteredRowSet;

import org.omg.CosNaming.NamingContextExtPackage.AddressHelper;


public class PlayGame {
	Scanner input= new Scanner(System.in);
	/**
	 * ���ڴ���˿���
	 * @param args
	 */
	public Set<Poke> pokes; 
	public PlayGame() {
		this.pokes = new HashSet<Poke>();
	}
	/**
	 * ϴ��
	 * @param args
	 */
	public void cleanPoke() {
		System.out.println("��ʼϴ�ơ�����");
		for (int i=0;i<4;i++) {
			for (int j=1;j<14;j++) {
				if (i==0) {
					if (j==1) {
						Poke poke= new Poke("÷��", "A");
						pokes.add(poke);
					}
					else if (j==11) {
						Poke poke= new Poke("÷��", "J");
						pokes.add(poke);
					}
					else if (j==12) {
						Poke poke= new Poke("÷��", "Q");
						pokes.add(poke);
					}
					else if (j==13) {
						Poke poke= new Poke("÷��", "K");
						pokes.add(poke);
					}
					else {
						Poke poke= new Poke("÷��", j+"");
						pokes.add(poke);
					}
				}
				if (i==1) {
					if (j==1) {
						Poke poke= new Poke("����", "A");
						pokes.add(poke);
					}
					else if (j==11) {
						Poke poke= new Poke("����", "J");
						pokes.add(poke);
					}
					else if (j==12) {
						Poke poke= new Poke("����", "Q");
						pokes.add(poke);
					}
					else if (j==13) {
						Poke poke= new Poke("����", "K");
						pokes.add(poke);
					}
					else {
						Poke poke= new Poke("����", j+"");
						pokes.add(poke);
					}
				}
				if (i==2) {
					if (j==1) {
						Poke poke= new Poke("����", "A");
						pokes.add(poke);
					}
					else if (j==11) {
						Poke poke= new Poke("����", "J");
						pokes.add(poke);
					}
					else if (j==12) {
						Poke poke= new Poke("����", "Q");
						pokes.add(poke);
					}
					else if (j==13) {
						Poke poke= new Poke("����", "K");
						pokes.add(poke);
					}
					else {
						Poke poke= new Poke("����", j+"");
						pokes.add(poke);
					}
				}
				if (i==3) {
					if (j==1) {
						Poke poke= new Poke("����", "A");
						pokes.add(poke);
					}
					else if (j==11) {
						Poke poke= new Poke("����", "J");
						pokes.add(poke);
					}
					else if (j==12) {
						Poke poke= new Poke("����", "Q");
						pokes.add(poke);
					}
					else if (j==13) {
						Poke poke= new Poke("����", "K");
						pokes.add(poke);
					}
					else {
						Poke poke= new Poke("����", j+"");
						pokes.add(poke);
					}
				}
			}
		}
		System.out.println("ϴ�ƽ���������������");
	}
	

	
	/**
	 * �����û�
	 * @param args
	 */
	public Player[] createPlayer() {
		System.out.println("���������1������");
		String name1 = input.next();
		Player player1=new Player(1, name1);
		System.out.println("���1�����ɹ���");
		System.out.println("���������2������");
		String name2 = input.next();
		Player player2=new Player(1, name2);
		System.out.println("���2�����ɹ���");
		Player[] users= {player1,player2};
		return users;
	}
	
	/**
	 *����
	 * @param args
	 */
	
	public void getPoke(Player[] a) {
		Player player1=a[0];
		Player player2=a[1];
		System.out.println("��ʼ���ơ�����������");
		System.out.println("���1���ơ�����");
		Iterator<Poke> poke=pokes.iterator();
		if(poke.hasNext()) {
			player1.myPoke.add(poke.next());
		}

		System.out.println("���2���ơ�����");
		if(poke.hasNext()) {
			player2.myPoke.add(poke.next());
		}

		System.out.println("���1���ơ�����");
		if(poke.hasNext()) {
			player1.myPoke.add(poke.next());
		}
		
		System.out.println("���2���ơ�����");

		if(poke.hasNext()) {
			player2.myPoke.add(poke.next());
		}
		System.out.println("��Ʊ��������������");
	}
	
	/**
	 * �Ƚ�
	 * @param args
	 */
	public void compare(Player[] a) {
		Player player1=a[0];
		Player player2=a[1];
		int X=player1.myPoke.get(0).compareTo(player1.myPoke.get(1));
		int Y=player2.myPoke.get(0).compareTo(player2.myPoke.get(1));
		if (X>=0) {
			if(Y>=0) {
				int q=player1.myPoke.get(0).compareTo(player2.myPoke.get(0));
				switch (q) {
				case 1:
					System.out.println("���1��ʤ");
					break;

				case -1:
					System.out.println("���2��ʤ");
					break;
				case 0:
					System.out.println("������");
					break;
				}
			}
			else {
				int w=player1.myPoke.get(0).compareTo(player2.myPoke.get(1));
				switch (w) {
				case 1:
					System.out.println("���1��ʤ");
					break;

				case -1:
					System.out.println("���2��ʤ");
					break;
				case 0:
					System.out.println("������");
					break;
				}
			}
		}
		
		else if (X<0) {
			if(Y>=0) {
				int w=player1.myPoke.get(1).compareTo(player2.myPoke.get(0));
				switch (w) {
				case 1:
					System.out.println("���1��ʤ");
					break;

				case -1:
					System.out.println("���2��ʤ");
					break;
				case 0:
					System.out.println("������");
					break;
				}
			}
			else {
				int w=player1.myPoke.get(1).compareTo(player2.myPoke.get(1));
				switch (w) {
				case 1:
					System.out.println("���1��ʤ");
					break;

				case -1:
					System.out.println("���2��ʤ");
					break;
				case 0:
					System.out.println("������");
					break;
				}
			}
		}
	}
	/**
	 * ���������
	 * @param args
	 */
	
	private void forech(Player[] a) {
		// TODO Auto-generated method stub
		for(int i=0;i<a.length;i++) {
			System.out.println("���"+(i+1)+"������Ϊ��");
			for (int j=0;j<a[i].myPoke.size();j++) {
				Poke test=(Poke)a[i].myPoke.get(j);
				System.out.println(test.getColor() +test.getNum());
			}
		}
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		PlayGame play = new PlayGame();
		Player[] user=play.createPlayer();
		play.cleanPoke();
		play.getPoke(user);
		play.compare(user);
		play.forech(user);
	}

}

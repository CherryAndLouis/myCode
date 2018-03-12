package PokeGame;

public class Poke implements Comparable<Poke> {
	public String getColor() {
		return color;
	}
	public void setColor(String color) {
		this.color = color;
	}
	public String getNum() {
		return num;
	}
	public void setNum(String num) {
		this.num = num;
	}
	private String color;
	private String num;
	public Poke(String color,String num) {
		this.color=color;
		this.num=num;
	}
	@Override
	public int compareTo(Poke o) {
		// TODO Auto-generated method stub
		if (this.num.compareTo(o.num)>0) {
			return 1;
		}
		if (this.num.compareTo(o.num)<0) {
			return -1;
		}
		if (this.color.compareTo(o.color)>0) {
			return 1;
		}
		if (this.color.compareTo(o.color)<0) {
			return -1;
		}
		return 0;
	}
}

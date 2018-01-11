package PokeGame;

import java.awt.List;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class Player {
	private int id;
	private String name;
	public ArrayList<Poke> myPoke;
	
	public Player(int id,String name) {
		this.id=id;
		this.name=name;
		this.myPoke = new ArrayList<Poke>();
	}
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}

}

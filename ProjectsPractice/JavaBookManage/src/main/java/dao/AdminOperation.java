package main.java.dao;

public interface AdminOperation {
    public boolean setPrice(String Name,float price);
    public boolean changeName(String originalName,String name);
}

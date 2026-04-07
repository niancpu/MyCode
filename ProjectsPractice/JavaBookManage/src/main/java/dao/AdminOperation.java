package main.java.dao;

import java.io.IOException;

public interface AdminOperation {
    public boolean setPrice(String Name,float price);
    public boolean changeName(String originalName,String name);
    public boolean addBook(String name,float price) throws IOException;
}

package main.java.dao;

import java.io.IOException;

 public interface AdminOperation {
     boolean setPrice(String Name,float price);
     boolean changeName(String originalName,String name);
     boolean addBook(String name,float price) throws IOException;
     boolean delbook(String name);
//     void libraryOverview();
}

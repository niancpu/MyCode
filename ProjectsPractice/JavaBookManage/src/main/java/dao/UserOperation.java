package main.java.dao;

import Entity.BookEntity;

 public interface UserOperation {
     boolean ask(String bookName);
     BookEntity find(String bookName);
     BookEntity find(int id);
     boolean borrow(String name);
     boolean giveBack(String name);
}

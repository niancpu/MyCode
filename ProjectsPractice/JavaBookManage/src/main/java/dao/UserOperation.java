package main.java.dao;

import Entity.BookEntity;

 public interface UserOperation {
     boolean ask(String bookName);
     BookEntity find(String bookName);
     boolean borrow(String name);
     boolean giveBack(String name);
}

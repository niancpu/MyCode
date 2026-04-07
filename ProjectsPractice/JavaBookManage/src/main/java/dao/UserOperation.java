package main.java.dao;

import Entity.BookEntity;

public interface UserOperation {
    public boolean ask(String bookName);
    public BookEntity find(String bookName);
    public boolean borrow(String name);
    public void giveBack(String name);
}

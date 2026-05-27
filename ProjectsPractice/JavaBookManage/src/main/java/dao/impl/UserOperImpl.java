package main.java.dao.impl;
import Entity.BookDomain;
import Entity.BookEntity;
import main.java.dao.AdminOperation;
import main.java.dao.DatabaseOperation;
import main.java.dao.UserOperation;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;


public class UserOperImpl implements UserOperation {
    private final DatabaseOperation oper = new DbOperFileImpl();

    @Override
    public boolean ask(String name) {
        int bookNum= oper.getBookNum();
        for (int i = 1; i < bookNum; i++) {
            BookEntity book;
            book = oper.get(i);
            if (book.getBookName().equals(name)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public BookEntity find(String name) {
        int bookNum= oper.getBookNum();
        for (int i = 1; i <= bookNum; i++) {
            BookEntity book;
            book = oper.get(i);
            if (book.getBookName().equals(name)&&book.getState()) {
                return book;
            }
        }
        return null;
    }
    @Override
    public  BookEntity find(int id){
        return oper.get(id);
    }

    @Override
    public boolean borrow(String name){
        BookEntity book;
        if((book=find(name))!=null){
            book.setState(false);
            oper.updata(book);
            return !find(name).getState();
        }
        else{
            return false;
        }
    }
    @Override
    public boolean giveBack(String name){
        BookEntity book;
        if((book=find(name))!=null){
            book.setState(true);
            oper.updata(book);
            return (find(name)).getState();
        }
        else{
            return false;
        }
    }
}

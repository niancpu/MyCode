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
    private final Path dbpath = Paths.get("db.dat");


    @Override
    public boolean ask(String name) {
        long dbsize;
        try {
            dbsize = Files.size(dbpath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        for (int i = 1; i < dbsize / BookEntity.TOTAL_LENGTH; i++) {
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
        long dbsize;
        try {
            dbsize = Files.size(dbpath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        for (int i = 1; i < dbsize / BookEntity.TOTAL_LENGTH; i++) {
            BookEntity book;
            book = oper.get(i);
            if (book.getBookName().equals(name)&&book.getState()) {
                return book;
            }
        }
        return null;
    }
    @Override
    public boolean borrow(String name){
        BookEntity book;
        if((book=find(name))!=null){
            book.setState(false);
            return true;
        }
        else{
            return false;
        }
    }
    @Override
    public void giveBack(String name){
        BookEntity book;
        book=find(name);
        book.setState(true);
    }
}

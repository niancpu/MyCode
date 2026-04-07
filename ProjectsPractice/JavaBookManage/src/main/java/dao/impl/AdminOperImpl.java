package main.java.dao.impl;

import Entity.BookEntity;
import main.java.dao.AdminOperation;
import main.java.dao.DatabaseOperation;
import main.java.dao.UserOperation;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class AdminOperImpl implements AdminOperation {
    private final UserOperation Uoper=new UserOperImpl();
    private final DatabaseOperation oper=new DbOperFileImpl();
    private final Path dbpath = Paths.get("db.dat");

    @Override
    public boolean changeName (String originalName,String name){
        BookEntity book;
        if((book=Uoper.find(originalName))!=null){
            book.setBookName(name);
            oper.updata(book);
            return true;
        }
        else{
            return false;
        }
    }
    @Override
    public boolean setPrice(String name,float price){
        BookEntity book;
        if((book=Uoper.find(name))!=null){
            book.setPrice(price);
            oper.updata(book);
            return true;
        }
        else{
            return false;
        }
    }
    @Override
    public boolean addBook(String name,float price) throws IOException {
        try {
            long dbsize= Files.size(dbpath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        BookEntity book=new BookEntity();
        book.setBookName(name);
        book.setPrice(price);
        int id=
        }
    }
}

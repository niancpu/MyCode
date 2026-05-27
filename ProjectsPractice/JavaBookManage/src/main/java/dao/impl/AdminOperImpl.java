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
    private final static UserOperation Uoper=new UserOperImpl();
    private final static DatabaseOperation oper=new DbOperFileImpl();
    private final static Path dbpath = Paths.get("db.dat");

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
    public boolean addBook(String name,float price) {
        long dbsize;
        try {
            dbsize= Files.size(dbpath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        BookEntity book=new BookEntity();
        book.setBookName(name);
        book.setPrice(price);
        int id=(int)dbsize / BookEntity.TOTAL_LENGTH+1;
        book.setId(id);
        oper.add(book);
        return Uoper.ask(book.getBookName());

        }

    @Override
    public boolean delbook(String name) {
        BookEntity book;
        if ((book = Uoper.find(name)) != null) {
            oper.delete(book.getId());
            return true;
        }
        else {
            return false;
        }
    }
    public static void libraryOverview(){
        long dbsize;
        try {
            dbsize=Files.size(dbpath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        var book=new BookEntity();
        int normalBook=0;
        int onLoan=0;
        int blank=0;
        for(int i = 1; i<=dbsize / BookEntity.TOTAL_LENGTH; i++){
            book=oper.get(i);
            if(book.getId()!=0){
                if(book.getState()){
                normalBook++;}
                else{
                    onLoan++;
                }
            }
            else{
                blank++;
            }
        }
        System.out.printf("""
                图书馆共有书%d;
                其中被借出去%d;
                现有%d;
                另外有空白书位%d;""",
                normalBook+onLoan,
                onLoan,
                normalBook,
                blank);
    }
}

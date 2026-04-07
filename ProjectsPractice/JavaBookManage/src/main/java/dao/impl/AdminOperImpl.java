package main.java.dao.impl;

import Entity.BookEntity;
import main.java.dao.AdminOperation;
import main.java.dao.DatabaseOperation;
import main.java.dao.UserOperation;

public class AdminOperImpl implements AdminOperation {
    UserOperation Uoper=new UserOperImpl();
    DatabaseOperation oper=new DbOperFileImpl();
    BookEntity book=new BookEntity();
    @Override
    public boolean changeName (String originalName,String name){
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
        if((book=Uoper.find(name))!=null){
            book.setPrice(price);
            oper.updata(book);
            return true;
        }
        else{
            return false;
        }
    }
}

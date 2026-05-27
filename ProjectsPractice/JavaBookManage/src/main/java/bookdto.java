package main.java;
import Entity.BookEntity;
public class bookdto {
    public bookdto(BookEntity entity){
        String bookName=entity.getBookName();
        int id=entity.getId();
        double price=entity.getPrice();
    }
}

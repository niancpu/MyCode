package main.java.dao;
import Entity.BookEntity;

public interface DatabaseOperation {
    void updata(BookEntity book);
    void delete(int id);
    void add(BookEntity book);
    BookEntity get(int id);
}

package dao;
import Entity.BookEntity;

public interface DatabaseOperation {
    void add(String bookName);
    void delete(String bookName);
    void search(String bookName);
    void change(String bookName);
}

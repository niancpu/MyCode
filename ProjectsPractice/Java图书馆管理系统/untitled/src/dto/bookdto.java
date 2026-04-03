package dto;
import Entity.BookEntity;
public class bookdto {
    public bookdto(BookEntity entity){
        String bookName=entity.getBookName();
        String uuid=entity.getuuid();
        double price=entity.getPrice();
    }
}

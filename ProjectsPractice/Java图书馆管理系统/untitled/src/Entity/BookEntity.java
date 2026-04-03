package Entity;

public class BookEntity {
    private String uuid;
    private String bookName;
    private double price;

    public BookEntity(){};

    public String getuuid(){ return uuid; }
    public void setuuid(String uuid){ this.uuid=uuid; }
    public String getBookName(){ return bookName; }
    public void setBookName(String bookName){ this.bookName=bookName; }
    public double getPrice(){ return price; }
    public void setPrice(double price){ this.price=price; }
}

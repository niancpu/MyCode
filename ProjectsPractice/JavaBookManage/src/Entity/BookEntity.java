package Entity;

public class BookEntity {
    private int id;
    private String bookName;
    private float price;
    private boolean state=true;
    public static final int NAME_LENGTH=90;
    public static final int TOTAL_LENGTH=NAME_LENGTH+8+1;

    public BookEntity(){};
    public BookEntity(int id,String bookName,float price){
        this.id= id;
        this.bookName=bookName;
        this.price=price;
    }

    public int getId(){ return id; }
    public void setId(int  id){ this.id=id; }
    public String getBookName(){ return bookName; }
    public void setBookName(String bookName){ this.bookName=bookName; }
    public float getPrice(){ return price; }
    public void setPrice(float price){ this.price=price; }
    public boolean getState(){return state;}
    public void setState(boolean state){this.state=state;}
}

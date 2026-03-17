class Main{
    public static void main(String[] args) {
        var book=new Book("java入门",2333);
        book.printInfo();

    }
}

class Book {
    private String name;
    private double price;
    public Book(String name,double price){
        this.name=name;
        this.price=price;
    }
    public String getName (){
        return name;
    }
    public void setName(String name){
        this.name=name;
    }
    public double getPrice(){
        return price;
    }
    public void setPrice(double price){
        if (price<0){
            throw new IllegalArgumentException("Invalid Price！");
        }
        else{
            this.price=price;
        }

    }
    public void printInfo(){
        System.out.printf("书名：%s,价格：%.0f",this.name,this.price);
    }

}
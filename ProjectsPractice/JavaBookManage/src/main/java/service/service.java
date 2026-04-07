package main.java.service;

import Entity.BookEntity;
import main.java.dao.AdminOperation;
import main.java.dao.UserOperation;

import java.util.Scanner;

public class service {
    private UserOperation Uoper;
    private AdminOperation Aoper;

    public service(UserOperation Uoper, AdminOperation Aoper) {
        this.Uoper = Uoper;
        this.Aoper = Aoper;
    }

    public String state(boolean bookstate) {
        return bookstate ? "未借出" : "已借出";
    }

    public void start() {
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("再见");
        }));

        var sc = new Scanner(System.in);
        System.out.println("""
                =====欢迎来到图书馆=====
                您是管理员还是用户？
                1.管理员
                2，用户
                """);
        String choice = sc.nextLine();
        switch (choice) {

            case "1" -> {
                System.out.println("""
                        =====欢迎您！管理员=====
                        请选择您需要的操作：
                        1.查找图书
                        2.存放图书
                        3.删除图书
                        4.更改图书名字
                        5.更改图书状态
                        6.更改图书价格
                        7.总览图书馆状态
                        8.查询图书借阅状态
                        
                        """);
                choice = sc.nextLine();
                switch (choice) {
                    case "1" -> {
                        System.out.println("请输入您要查找的图书的名字：\n");
                        BookEntity book = Uoper.find(sc.nextLine());
                        if (book != null) {
                            System.out.printf("""
                                            图书馆存在您要查询的这本书，它的信息是:
                                            ID:%d;
                                            书名:%s;
                                            书籍价格:%f;
                                            书籍状态:%s
                                            """,
                                    book.getId(),
                                    book.getBookName(),
                                    book.getPrice(),
                                    state(book.getState())
                            );
                        }
                    }
                    case "2" -> {
                        System.out.print("""
                                输入您要存放的图书的信息：
                                书名: 
                                """);
                        String name = sc.next();
                        System.out.print("价格: ");
                        float price = sc.nextFloat();
                    }

                }
            }
            case "2" -> {
                System.out.println("""
                        =====欢迎您！用户=====
                        请选择您需要的操作：
                        1.借阅图书
                        2.归还图书
                        3.查询图书
                        4.查找图书
                        
                        """);
            }
            default -> {
                System.out.println("请输入合法字符\n");
            }

        }
    }
}

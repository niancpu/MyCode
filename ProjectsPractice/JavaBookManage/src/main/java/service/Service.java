package main.java.service;

import Entity.BookEntity;
import main.java.dao.AdminOperation;
import main.java.dao.UserOperation;
import main.java.dao.impl.AdminOperImpl;

import java.io.IOException;
import java.util.Scanner;
import java.util.concurrent.CompletableFuture;

public class Service {
    private final UserOperation Uoper;
    private final AdminOperation Aoper;

    public Service(UserOperation Uoper, AdminOperation Aoper) {
        this.Uoper = Uoper;
        this.Aoper = Aoper;
    }

    public String state(boolean bookstate) {
        return bookstate ? "未借出" : "已借出";
    }

    public void start() {
        Runtime.getRuntime().addShutdownHook(new Thread(() ->
                System.out.println("再见")));

            var sc = new Scanner(System.in);
            System.out.println("""
                    =====欢迎来到图书馆=====
                    您是管理员还是用户？
                    1.管理员
                    2，用户
                    """);
            String choice = sc.nextLine();
        while (true) {
            switch (choice) {
                case "1" -> {
                    System.out.println("""
                            =====欢迎您！管理员=====
                            请选择您需要的操作：
                            1.查找图书
                            2.存放图书
                            3.删除图书
                            4.更改图书名字
                            5.更改图书价格
                            6.总览图书馆状态 
                            """);
                    choice = sc.nextLine().trim();
                    BookEntity book = new BookEntity();
                    switch (choice) {
                        case "1" -> {
                            System.out.println("请输入您要查找的图书的名字：\n");
                            book = Uoper.find(sc.nextLine());
                            if (book != null) {
                                System.out.printf("""
                                                图书馆存在您要查询的这本书，它的信息是:
                                                ID:%d;
                                                书名:%s;
                                                书籍价格:%.2f;
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
                            String name = sc.next().trim();
                            System.out.print("价格: ");
                            float price = sc.nextFloat();
                            try {
                                Aoper.addBook(name, price);
                            } catch (IOException e) {
                                throw new RuntimeException(e);
                            }
                        }
                        case "3" -> {
                            System.out.println("""
                                    输入您要删除的图书的名字：
                                    """);
                            if (Aoper.delbook(sc.nextLine().trim())) {
                                System.out.println("删除成功！");
                            } else {
                                System.out.println("请确认这本书是否存在！");
                            }

                        }
                        case "4" -> {
                            System.out.println("""
                                    请输入您要更改名字的图书的书名：
                                    """);
                            String orginalName = sc.nextLine().trim();
                            System.out.println("请输入您想要改的名字：");
                            String name = sc.nextLine().trim();
                            if (Aoper.changeName(orginalName, name)) {
                                System.out.println("改名成功！");
                            } else {
                                System.out.println("改名失败！请检查这本书是否存在！");
                            }
                        }
                        case "5" -> {
                            System.out.println("""
                                    您可以将这本书的价格修改，
                                    请输入您要修改的书的名字：""");
                            String name = sc.nextLine().trim();
                            System.out.println("请输入您想要修改的价格：");
                            if (Aoper.setPrice(name, sc.nextFloat())) {
                                System.out.println("修改价格成功！");
                            } else {
                                System.out.println("修改价格失败，请检查这本书是否存在！");
                            }
                        }
                        case "6" -> {
                            CompletableFuture.runAsync(AdminOperImpl::libraryOverview)
                                    .thenRun(() -> System.out.println("输出完毕！"));
                            System.out.println("正在大调查...");
                        }
                        default -> System.out.println("请输入合法字符");
                    }
                }
                case "2" -> {
                    System.out.println("""
                            =====欢迎您！用户=====
                            请选择您需要的操作：
                            1.借阅图书
                            2.归还图书
                            3.查找图书
                            """);
                    choice = sc.nextLine();
                    var book = new BookEntity();
                    switch (choice) {
                        case "1" -> {
                            System.out.println("请输入您要借阅的图书：");
                            String name = sc.nextLine().trim();
                            if (Uoper.borrow(name)) {
                                System.out.println("借阅成功！");
                            } else {
                                System.out.println("借阅失败！");
                            }

                        }
                        case "2" -> {
                            System.out.println("请输入您要归还的图书：");
                            String name = sc.nextLine().trim();
                            if (Uoper.giveBack(name)) {
                                System.out.println("归还成功！");
                            } else {
                                System.out.println("归还失败！");
                            }
                        }
                        case "3" -> {
                            System.out.println("请输入您要查找的图书的名字：\n");
                            book = Uoper.find(sc.nextLine());
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
                    }
                }
                default -> System.out.println("请输入合法字符\n");
            }
        }
    }
}

package main.java.service;

import Entity.BookEntity;
import main.java.dao.AdminOperation;
import main.java.dao.UserOperation;

import java.util.Scanner;

public class service{
    private UserOperation Uoper;
    private AdminOperation Aoper;

    public service(UserOperation Uoper,AdminOperation Aoper){
        this.Uoper=Uoper;
        this.Aoper=Aoper;
    }


    public void start(){
        Runtime.getRuntime().addShutdownHook(new Thread(()->{
            System.out.println("再见");
        }));

        var sc=new Scanner(System.in);
        System.out.println("""
                =====欢迎来到图书馆=====
                您是管理员还是用户？
                1.管理员
                2，用户
                """);
        if(sc.nextInt()==1){
            System.out.println("""
                    =====欢迎您！管理员=====
                    请选择您需要的操作：
                    1.查找图书
                    2.查询图书信息
                    3.更改图书名字
                    4.更改图书状态
                    5.总览图书馆状态
                    6.查询图书借阅状态
                    
                    """);
            if (sc.nextInt()==1){
                System.out.println("请输入您要查找的图书的名字：\n");
                BookEntity book=Uoper.find(sc.nextLine());
                if (book!=null){
                    System.out.printf("""
                            您要查询的图书存在:
                            ID:%d;
                            书名:%s;
                            书籍价格:%f;
                            书籍状态:%s
                            """);
                }

            }
        }
        else if(sc.nextInt()==2){
            System.out.println("""
                    =====欢迎您！用户=====
                    请选择您需要的操作：
                    1.借阅图书
                    2.归还图书
                    3.查询图书
                    4.查找图书
                    
                    """);
        }
        else{
            System.out.println("请输入合法字符\n");
        }

    }
}

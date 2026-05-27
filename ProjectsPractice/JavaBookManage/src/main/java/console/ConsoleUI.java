package main.java.console;

import main.java.dao.AdminOperation;
import main.java.dao.UserOperation;
import main.java.dao.impl.AdminOperImpl;
import main.java.dao.impl.UserOperImpl;
import main.java.service.Service;

public class ConsoleUI {
    public static void main(String[] args){
        UserOperation Uoper=new UserOperImpl();
        AdminOperation Aoper=new AdminOperImpl();
        var service=new Service(Uoper,Aoper);
        service.start();
    }

}

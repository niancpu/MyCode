package src;
import java.io.IOException;


public class FileReaderDemo {
    public static void main(String[] args){
        String regex=".*src";
        String pwd=System.getProperty("user.dir");

        try {
            java.io.FileReader fr = new java.io.FileReader(pwd + "\\demo.txt");
            int data;
            while ((data = fr.read()) != -1) {
                System.out.print((char) data);
            }

            fr.close();
        }catch(IOException e){
            e.printStackTrace();
        }
    }
}


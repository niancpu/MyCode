package src;

import java.io.IOException;
import java.io.RandomAccessFile;

public class RandomAccessFileDemo {
    public static void main(String[] args){
        //try-with-resource
        String pwd=System.getProperty("user.dir");
        try(RandomAccessFile raf = new RandomAccessFile(pwd+"//demo.txt","r")){
            //定义缓冲字节数组
            byte[] bs = new byte[1024];
            int byteRead = 0;
            //read(bs)  读取bs.length个字节的数据到一个字节数组中
            while((byteRead = raf.read(bs))!=-1){
                System.out.println("读取的内容："+new String(bs,0,byteRead));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}

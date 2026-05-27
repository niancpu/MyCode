package test;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

import Entity.BookEntity;

public class Write {
    public static void main(String[] args){
        var aBook=new BookEntity(
                1,
                "AAA代码批发商养成指南",
                100.0f
        );

        String pwd=System.getProperty("user.dir");
//        System.out.println(pwd);
        try(RandomAccessFile raf = new RandomAccessFile(pwd+"//db.dat","rws")){
            //定义缓冲字节数组
            byte[] bs = new byte[256];
            int byteRead = 0;
            //read(bs)  读取bs.length个字节的数据到一个字节数组中
            while((byteRead = raf.read(bs))!=-1){
                System.out.println("\n"+raf.getFilePointer());
                raf.seek(0);
                System.out.println(raf.getFilePointer());
                raf.writeInt(aBook.getId());
                raf.seek(72);
                raf.writeChars(aBook.getBookName());
                raf.seek(252);
                raf.writeFloat(aBook.getPrice());
                raf.seek(252);
                System.out.printf("%.2f",raf.readFloat());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}

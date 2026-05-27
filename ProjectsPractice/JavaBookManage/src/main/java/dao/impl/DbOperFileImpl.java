package main.java.dao.impl;
import Entity.BookEntity;
import main.java.dao.DatabaseOperation;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;

public class DbOperFileImpl implements DatabaseOperation {
    {
        Path path= Paths.get("db.dat");
        if(Files.notExists(path)){
            try {
                Files.createFile(path);
                System.out.println("正在创建数据库文件...");
            } catch (IOException e) {
                throw new RuntimeException(e);  
            }
        }
        else {
            System.out.println("数据库文件已存在，正在读取...");
        }
    }
    byte[] bs=new byte[BookEntity.TOTAL_LENGTH];
    byte[] setBlank=new byte[BookEntity.TOTAL_LENGTH];
    static final Path dbPath=Paths.get("db.dat");

    int byteRead=0;

    @Override
    public void add(BookEntity book){
        Arrays.fill(setBlank,(byte)0);
        try(var raf=new RandomAccessFile(dbPath.toString(),"rw")){
            book.setId(getBookNum()+1);
            raf.seek(raf.length());
            raf.writeInt(book.getId());
            raf.writeChars(book.getBookName());
            raf.write(setBlank,0,BookEntity.NAME_LENGTH-book.getBookName()
                                                .getBytes(StandardCharsets.UTF_16BE)
                                                .length);
            raf.writeFloat(book.getPrice());
            raf.writeBoolean(book.getState());
        }catch(IOException e){
            e.printStackTrace();
        }
    }

    @Override
    public void updata(BookEntity book){
        Arrays.fill(setBlank,(byte)0);
        try(var raf=new RandomAccessFile(dbPath.toString(),"rw")){
            raf.seek((long)(book.getId()-1)* BookEntity.TOTAL_LENGTH+4);
            raf.writeChars(book.getBookName());
            raf.write(setBlank,0,BookEntity.NAME_LENGTH-book
                    .getBookName().getBytes(StandardCharsets.UTF_16BE)
                    .length);
            raf.writeFloat(book.getPrice());
            raf.writeBoolean(book.getState());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public BookEntity get(int id) {
        var book = new BookEntity();
        int bookNum=getBookNum();
        if (id>bookNum) return null;
        long pos=(id - 1L) * BookEntity.TOTAL_LENGTH;
        try (var raf = new RandomAccessFile(dbPath.toString(), "r")) {
            raf.seek(pos);
            if ((byteRead = raf.read(bs)) != -1) {
//                book.setId(
//                        ByteBuffer.wrap(bs,0,4)
//                                .order(ByteOrder.BIG_ENDIAN)
//                                .getInt()
//                );
                book.setId(
                        ((bs[0]&0xFF)<<24)|
                        ((bs[1]&0xFF)<<16)|
                        ((bs[2]&0xFF)<<8)|
                        (bs[3]&0xFF)
                );
                book.setBookName(new String(bs,4,BookEntity.NAME_LENGTH,StandardCharsets.UTF_16BE).trim());
                book.setPrice(
                        ByteBuffer.wrap(bs,94,4)
                                .order(ByteOrder.BIG_ENDIAN)
                                .getFloat()
                );
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return book;
    }

    @Override
    public void delete(int id){
        try(var raf= new RandomAccessFile(dbPath.toString(),"rw")){
            Arrays.fill(setBlank,(byte)0);
            raf.seek((id-1L)*BookEntity.TOTAL_LENGTH);
            raf.write(setBlank);
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public int getBookNum(){
        long dbsize;
        try {
            dbsize= Files.size(dbPath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return (int)dbsize/BookEntity.TOTAL_LENGTH;
    }
}

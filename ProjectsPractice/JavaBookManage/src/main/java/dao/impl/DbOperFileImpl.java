package main.java.dao.impl;
import Entity.BookEntity;
import main.java.dao.DatabaseOperation;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

public class DbOperFileImpl implements DatabaseOperation {
    byte[] bs=new byte[BookEntity.TOTAL_LENGTH];
    byte[] setBlank=new byte[BookEntity.TOTAL_LENGTH];
    String pwd=System.getProperty("user.dir")+"\\db.dat";
    int byteRead=0;

//测试用例
//    public static void main(String[] args){
//        var book=new BookEntity(
//                1,
//                "AAA代码批发商养成指南",
//                100.0f
//        );
//        DatabaseOperation oper=new DbOperFileImpl();
//        oper.add(book);
//        oper.get(1);
//    }

    @Override
    public void add(BookEntity book){
        Arrays.fill(setBlank,(byte)0);
        try(var raf=new RandomAccessFile(pwd,"rw")){
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
        try(var raf=new RandomAccessFile(pwd,"rw")){
            raf.seek((long)(book.getId()-1)* BookEntity.TOTAL_LENGTH);
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
        try (var raf = new RandomAccessFile(pwd, "r")) {
            raf.seek((id - 1L) * BookEntity.TOTAL_LENGTH);
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
    public void delete(int id){
        try(var raf= new RandomAccessFile(pwd,"rw")){
            Arrays.fill(setBlank,(byte)0);
            raf.seek((id-1L)*BookEntity.TOTAL_LENGTH);
            raf.write(setBlank);
        }catch(Exception e){
            e.printStackTrace();
        }

    }

}

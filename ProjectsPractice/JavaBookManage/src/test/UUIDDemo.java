package test;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

public class UUIDDemo{
    public static void main(String[] args){
        var uuid= UUID.nameUUIDFromBytes("AAA代码批发商".getBytes(StandardCharsets.UTF_8));
        System.out.println(uuid.toString().getBytes(StandardCharsets.UTF_8).length);

    }
}
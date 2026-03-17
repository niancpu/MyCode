
public class D0000practice{

    public static void main(String[] args) {
        CCC ddd = new DDD();
    System.out.println(ddd.sum());
    }}
    class CCC{

        int i=10;

        public int sum(){
            return i+10;
        }
    }

    class DDD extends CCC{

        int i=20;
//
//        public int sum(){
//            return i + 20;
//        }
    }

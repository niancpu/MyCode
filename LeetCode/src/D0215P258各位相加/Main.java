package D0215P258各位相加;

public class Main {
    public static void main(String[] args){
           var s=new Solution();
           int a=38;
           System.out.println(s.addDigits(a));
    }
}
class Solution {
    public int addDigits(int num) {
        int a=0;
        while(!(num==0)){
            a+=num%10;
            num/=10;
            if(a>=10&&num==0){

                num=a;a=0;
            }
        }
        return a;
    }
}
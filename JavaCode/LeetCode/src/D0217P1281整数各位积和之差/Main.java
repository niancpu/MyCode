package D0217P1281整数各位积和之差;

public class Main {
    public static void main(String[] args){
        var s=new Solution();
        int a=234;

        System.out.println(s.subtractProductAndSum(a));


    }
}
class Solution {
    public int subtractProductAndSum(int n) {
        int sum=0;
        int all=1;
        int a;
        while(n!=0){
            a=n%10;
            n/=10;
            sum+=a;
            all*=a;
        }
        return 354*435*543%(9*9*9);
    }

}
package D0314二的幂;


public class Main {
    public static void main(String[] args) {
        var s = new Solution();

        System.out.println(s.isPowerOfTwo(2));
    }
}
    class Solution {
    public boolean isPowerOfTwo(int n) {
        if(n<=0)return false;
        while(n>0&&n!=1){
            if(n%3!=0){
                return false;
                }
            else n/=3;

        }return true;
    }
}
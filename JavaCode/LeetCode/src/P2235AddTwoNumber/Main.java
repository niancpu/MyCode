package P2235AddTwoNumber;

public class Main {
    public static void  main (String[] args) {
        int a = 1;
        int b = 2;
        var s = new Solution();
        int result=s.sum(a,b);
        System.out.println(result);
    }
}

class Solution {
    public int sum(int num1, int num2) {

        return num1+num2;
    }
}

package p2413MInimumEvenMultiple;

public class Main
{
    public static void main(String[] args){
        int a=5;
        var s=new Solution();
        System.out.println(s.smallestEvenMultiple(a));

    }
}
class Solution {
    public int smallestEvenMultiple(int n) {
        if ((n/2)==0){
            return n;

        }
        else {
            return n*2;
        }
    }
}

package D0209P1486数组异或;

public class Main {
    public static void main(String[] args){
        int n=5;
        int start=0;
        var s=new Solution();
        System.out.println(s.xorOperation(n,start));
    }
}

class Solution {
    public int xorOperation(int n, int start) {
        int xor=start;
        for(int i=1;i<n;i++){
            int current=i*2+start;
            xor=xor^current;
        }
        return xor;
    }
}


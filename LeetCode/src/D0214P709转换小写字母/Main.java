package D0214P709转换小写字母;




public class Main {
    public static void main(String[] args) {
        var s = new Solution();
        String a="HelKKKo";
        System.out.println(s.toLowerCase(a));

    }
}

class Solution {
    public String toLowerCase(String s) {
        s = s.toLowerCase();
        return s;
    }
}
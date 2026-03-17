package P263丑数;

class Solution {
    public boolean isUgly(int n) {
        while((n&1)==0){
            n/=2;
        }
        while(n%3==0){
            n/=3;
        }
        while(n%5==0){
            n/=5;
        }
        if (n==1){
            return true;
        }
        else{
            return false;
        }
    }
}
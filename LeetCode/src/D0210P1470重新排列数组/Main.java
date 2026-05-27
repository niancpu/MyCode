package D0210P1470重新排列数组;
import java.util.ArrayList;
import java.util.Arrays;

public class Main {
    public static void main(String[] args){
        var s=new Solution();
        var arr= new int[]{5,5,4,3,1,3};
        System.out.println(Arrays.toString(s.shuffle(arr,3)));

    }
}
class Solution {
    public int[] shuffle(int[] nums, int n) {
        var arr=new int[2*n];
        for(int i=0;i<n;i++){
            arr[2*i]=nums[i];
            arr[i*2+1]=nums[i+n];
        }
        return arr;
    }
}
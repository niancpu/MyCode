package D0211P1534统计好三元组;

import java.util.ArrayList;
import java.util.HashMap;

class Main
{
    public static void main(String[] args){
        var s=new Solution();
        var arr= new int[]{3,0,1,1,9,7};
        int a=7,b=2,c=3;
        System.out.println(s.countGoodTriplets(arr,a,b,c));

    }}

class Solution {
    public int countGoodTriplets(int[] arr, int a, int b, int c) {
        int sum=0;
        for(int i=0;i<arr.length;i++){
            for(int j=i+1;j<arr.length;j++){
                for(int k=j+1;k<arr.length;k++){
                    if(arr[i]-arr[j]<=a&&arr[j]-arr[k]<=b&&arr[i]-arr[k]<=c&&arr[i]-arr[j]>=~a+1&&arr[j]-arr[k]>=~b+1&&arr[i]-arr[k]>=~c+1){
                        sum++;
                    }
                }
            }
        }


        return sum;
    }
}
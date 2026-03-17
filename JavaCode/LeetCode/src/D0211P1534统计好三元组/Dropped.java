//package D0211P1534统计好三元组;
//
//import java.util.ArrayList;
//import java.util.HashMap;
//
//class Main
//{
//    public static void main(String[] args){
//        var s=new Solution();
//        var arr= new int[]{3,0,1,1,9,7};
//        int a=7,b=2,c=3;
//        System.out.println(s.countGoodTriplets(arr,a,b,c));
//
//    }}
//
//class Solution {
//    public int countGoodTriplets(int[] arr, int a, int b, int c) {
//        var asite=new HashMap<Integer, ArrayList<Integer>>();
//        var bsite=new HashMap<Integer, ArrayList<Integer>>();
//        var csite=new if(asite.get(i)==null){
//            asite.put(i,new ArrayList<>());
//        }
//        asite.get(i).add(j);
//        int n=arr.length;
//        int sum=0;
//        for (int i=0;i<n;i++){
//            for(int j=i+1;j<n;j++){
//                if(arr[i]-arr[j]<=a&&arr[i]-arr[j]>=~a+1){
//                    if(asite.get(i)==null){
//                        asite.put(i,new ArrayList<>());
//                    }
//                    asite.get(i).add(j);
//                }
//                if(arr[i]-arr[j]<=b&&arr[i]-arr[j]>=~b+1){
//                    if(bsite.get(i)==null){
//                        bsite.put(i,new ArrayList<>());
//                    }
//                    bsite.get(i).add(j);
//                }
//                if(arr[i]-arr[j]<=c&&arr[i]-arr[j]>=~c+1){
//                    if(csite.get(i)==null){
//                        csite.put(i,new ArrayList<>());
//                    }
//                    csite.get(i).add(j);
//                }
//            }
//        }
//        for(Integer i:asite.keySet()){
//
//
//            if(bsite.containsKey(asite.get(i))&&bsite.get(asite.get(i)).equals(csite.get(i))){
//                sum++;
//
//            }
//
//        }
//        return sum;
//    }
//}
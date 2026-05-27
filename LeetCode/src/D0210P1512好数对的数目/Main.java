package D0210P1512好数对的数目;
import java.util.ArrayList;
import java.util.HashMap;
public class Main
{
    public static void main(String[] args){
        var s=new Solution();
        var arr= new int[]{5,5,5,6,3};
        System.out.println(s.numIdenticalPairs(arr));

    }
}
class Solution {
    public int numIdenticalPairs(int[] nums) {
        var map=new HashMap<Integer,Integer>();
        for (int i : nums){
                map.put(i,map.getOrDefault(i,0)+1);
        }
        int sum=0;
//        for(int value:map.values()){
//            sum+=value*(value-1)/2;
//        }
        sum+=map.values()
                .stream()
                .mapToInt(v->v*(v-1)/2)
                .sum();
        return sum;
    }
}

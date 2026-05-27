/*
 * @lc app=leetcode.cn id=1422 lang=java
 *
 * [1422] 分割字符串的最大得分
 */

// @lc code=start
class Solution {
    public int maxScore(String s) {
        int left=0,right=0,sum=0;
        for(int i=1;i<s.length()-1;i++){
            for(int l=0;l<i;l++){
                if(s.charAt(l)=='0'){
                    left++;
                }
            }
            for(int r=1;r<s.length()-i;r++){
                if(s.charAt(i+r)=='1'){
                    right++;
                }
            }
            if(left+right>sum){
                sum=left+right;
            }
            right=left=0;

        }
        return sum;
        
    }
}
// @lc code=end


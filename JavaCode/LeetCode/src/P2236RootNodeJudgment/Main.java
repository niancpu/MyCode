package P2236RootNodeJudgment;
class Main{
    public static void main(String[] args){
        var s=new Solution();
        var c=new TreeNode(4);
        var b=new TreeNode(5);
        var a=new TreeNode(2,c,b);
        System.out.println(s.checkTree(a));
    }
}

class TreeNode {
      int val;
      TreeNode left;
      TreeNode right;
      TreeNode() {}
      TreeNode(int val) { this.val = val; }
      TreeNode(int val, TreeNode left, TreeNode right) {
          this.val = val;
          this.left = left;
         this.right = right;
      }
}
class Solution {
    public boolean checkTree(TreeNode root) {
        return (root.left.val+root.right.val==root.val);
    }
}
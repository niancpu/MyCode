package P1768AlternateMergeString;

class Main
{
    public static void main (String[] args){
        Solution solution=new Solution();

        String word1="ab";
        String word2="efsd";

        String result =solution.mergeAlternately(word1,word2);
        System.out.println(result);
    }
}
class Solution{
    public String mergeAlternately(String word1,String word2){
        char[] a=word1.toCharArray();
        char[] b=word2.toCharArray();

        char[] c=new char[word1.length()+word2.length()];
        for(int i=0;;i++){
            if(i>=word1.length()&&i>=word2.length()){
                break;
            }
            else if(i<word1.length()&&i>=word2.length()){
                int temp=i;
                for(int j=temp*2;j<word2.length()+word1.length();j++){
                    c[j]=a[i];
                    i++;
                }
                continue;
            }
            else if (i<word2.length()&&i>=word1.length()){
                int temp=i;
                for(int j=temp*2;j<word2.length()+word1.length();j++){
                    c[j]=b[i];
                    i++;
                }
                continue;
            }
            c[2*i]=a[i];
            c[2*i+1]=b[i];

        }
        return new String(c);
    }
}
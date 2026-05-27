/*
 * @lc app=leetcode.cn id=1456 lang=c
 *
 * [1456] Maximum Number of Vowels in a Substring of Given Length
 */

#include <stdio.h>
#include <string.h>
    int maxVowels(char *s, int k)
    {
        int start = 0,count = 0,sum=0,init=1;
        int end = strlen(s);
        char *charSet = "aeiou";
        for (; start < end; start += 1)
        {


                if(start>=k&&strchr(charSet,s[start-k])){
                    count--;
                }
                if(strchr(charSet,s[start])){        
                    count++;
                
            }
            sum = (count > sum) ? count : sum;
        }

        return sum;
    }
// @lc code=end
int main()
{
    char *s = "tryhard";

    printf("%d", maxVowels(s, 3));
}

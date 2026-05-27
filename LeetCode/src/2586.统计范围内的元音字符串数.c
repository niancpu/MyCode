/*
 * @lc app=leetcode.cn id=2586 lang=c
 *
 * [2586] 统计范围内的元音字符串数
 */

// @lc code=start
#include <string.h>
#include <stdio.h>

int vowelStrings(char** words, int wordsSize, int left, int right) {
    char charSet[]="aeiou";
    int sum=0;
    for(int i=left;i<=right;i++){
        int length=strlen(words[i]);
        if(strchr(charSet,*words[i])){
            if(strchr(charSet,words[i][length-1])){
                sum++;
            }
        }


    }
    return sum;
}
// @lc code=end
int main(){
    char* words[]={"hey","aeo","mu","ooo","artro"};
    int result=vowelStrings(words,5,1,4);
    printf("%d\n", result);
}

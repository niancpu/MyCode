/*
 * @lc app=leetcode.cn id=852 lang=c
 *
 * [852] 山脉数组的峰顶索引
 */

// @lc code=start
#include <string.h>
#include <stdio.h>

int loop(int start, int end, int *arr); // 前向声明

int peakIndexInMountainArray(int *arr, int arrSize)
{
    int start = 0, end = arrSize - 1;
    return loop(start, end, arr);
}
int loop(int start, int end, int *arr)
{
    int a, b, c;
    int arrSize = end - start + 1;
    if (arrSize & 1)
    {
        b = start + (arrSize - 1) / 2;
        a = b - 1;
        c = b + 1;
        if (arr[b] > arr[a] && arr[b] > arr[c])
        {
            return b;
        }
        else if (arr[b] >= arr[a] && arr[b] <= arr[c])
        {
            return loop(b, end, arr);
        }
        else if (arr[b] <= arr[a] && arr[b] >= arr[c])
        {
            return loop(start, b, arr);
        }
    }
    else
    {
        c = start + arrSize / 2;
        b = c - 1;
        a = b - 1;

        if (arr[b] > arr[a] && arr[b] > arr[c])
        {
            return b;
        }
        else if (arr[b] >= arr[a] && arr[b] <= arr[c])
        {
            return loop(b, end, arr);
        }
        else if (arr[b] <= arr[a] && arr[b] >= arr[c])
        {
            return loop(start, b, arr);
        }
    }
    return -1; // 兜底返回
}
// @lc code=end

int main()
{
    int arr[] = {3,5,3,2,0};
    printf("%d", peakIndexInMountainArray(arr, 5));
}
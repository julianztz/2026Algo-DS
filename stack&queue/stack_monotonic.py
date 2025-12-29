'''
单调栈

使得每次新元素入栈后，栈内的元素都保持有序（单调递增或单调递减）

处理问题：
找下个更大 或 上个更小
'''

'''
例题
输入一个数组 nums，要求返回一个等长的结果数组，
结果数组中对应索引存储着下一个更大元素，如果没有更大的元素，就存 -1

思路: s[] 从右往左push大元素 -- 保持单调递减，移除小元素，栈顶永远是最大
'''
from typing import List


def calculateGreaterElement(nums):
    n = len(nums)
    # 存放答案的数组
    res = [0]*n
    s = []              # 从右往左记录大元素
    # 倒着往栈里放，此时栈包含右边（大）元素
    for i in range(n-1, -1, -1):
        # 移除被挡住的元素
        while s and s[-1] <= nums[i]:
            s.pop()
        # nums[i] 身后的更大元素
        res[i] = -1 if not s else s[-1]
        s.append(nums[i])
    return res


# lc 496
'''
nums1 中数字 x 的 下一个更大元素 是指 x 在 nums2 中对应位置 右侧 的 第一个 比 x 大的元素。
给你两个 没有重复元素 的数组 nums1 和 nums2 ，下标从 0 开始计数，其中nums1 是 nums2 的子集。

'''
def nextGreaterElement(nums1: List[int], nums2: List[int]) -> List[int]:
    n = len(nums2)    # 原list
    s = []            # stack 用作记录大数字

    temp = {}
    res = [0] * len(nums1)


    ind_nums1 = 0

    # 倒着读原数组 nums2
    for i in range(n-1, -1, -1):
        cur = nums2[i]
        # 移除stack顶端小元素
        while s and s[-1] <= cur:
            s.pop()
        
        temp[cur] = -1 if not s else s[-1]
        s.append(nums2[i])

    for n in nums1:
        res[ind_nums1] = temp[n]
        ind_nums1 += 1

    print(res)

# todo 739 daily temperature
'''
Given an array of integers temperatures represents the daily temperatures, 
return an array answer such that answer[i] is the number of days you have to wait 
after the ith day to get a warmer temperature. 
If there is no future day for which this is possible, keep answer[i] == 0 instead.
'''






if __name__ == '__main__':
    nextGreaterElement([4,1,2],[1,3,4,2])



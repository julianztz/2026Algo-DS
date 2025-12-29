from typing import List

#lc 645 Set Mismatch
'''
数组当作hash；当前数字*-1无损标记是否visited
'''
def findErrorNums(nums: List[int]) -> List[int]:
    if not nums:
        return []

    res = []
    for n in nums:
        n_idx = abs(n)-1           # index 对应num-1
        if nums[n_idx] > 0:        # 没有visited
            nums[n_idx] *= -1
        else:                      # visited！ 找到重复！
            res.append(abs(n))     # dup
    
    for i in range(len(nums)):
        if nums[i] > 0:            # visited过的位置 -> 缺失
            res.append(i+1)       # missing
    return res


# lc 1365 How Many Numbers Are Smaller Than the Current Number
'''
前缀和 -- how many are smaller than ... ? 
prefixSum -- 记录排名
'''
def smallerNumbersThanCurrent(nums: List[int]) -> List[int]:
    preSum = [0] * 101
    for i in range(len(nums)):
        preSum[nums[i]] += 1

    for i in range(1, len(preSum)):
        preSum[i] += preSum[i-1]

    print(preSum) 

    res = [0] * len(nums)

    for i in range(len(nums)):
        if nums[i] == 0:
            res[i] = 0
        else:
            res[i] = preSum[nums[i]-1]

    print(res)
    return res


smallerNumbersThanCurrent([5,0,10,0,10,6])


# lc 41 First Missing Positive
'''
❌ 这不是前缀和！这是"原地哈希"（In-place Hashing）

前缀和 vs 原地哈希的区别：
- 前缀和：计算累积和 preSum[i] = sum(nums[0...i-1])，用于快速查询区间和
- 原地哈希：使用数组索引作为哈希表，通过标记（如负数）记录信息

O(1) space 解法：使用数组本身作为哈希表
关键观察：答案只可能在 [1, n+1] 范围内
- 如果 [1, n] 都存在，答案是 n+1
- 否则答案是第一个缺失的正整数

方法：用数组索引作为哈希表（类似 findErrorNums）
- 对于数字 x (1 <= x <= n)，标记位置 x-1
- 通过将 nums[x-1] 变为负数来标记（表示 x 存在）
- 但需要先处理非正数和大于 n 的数
'''
def firstMissingPositive(nums: List[int]) -> int:
    n = len(nums)
    
    # 第一步：将所有非正数和大于 n 的数替换为 n+1（不影响结果）
    # 这样数组中只剩下 [1, n] 范围内的数
    for i in range(n):
        if nums[i] <= 0 or nums[i] > n:
            nums[i] = n + 1
    
    # 第二步：使用数组本身作为哈希表
    # 对于数字 x，将 nums[x-1] 标记为负数（表示 x 存在）
    for i in range(n):
        num = abs(nums[i])  # 取绝对值，因为可能已经被标记为负数
        if num <= n:
            nums[num - 1] = -abs(nums[num - 1])  # 标记为负数
    
    # 第三步：找到第一个正数的位置，其索引+1 就是答案
    for i in range(n):
        if nums[i] > 0:
            return i + 1
    
    # 如果所有位置都被标记（即 [1, n] 都存在），答案是 n+1
    return n + 1
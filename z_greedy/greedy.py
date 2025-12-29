from logging import fatal
from typing import List

'''
DP vs Greedy
动态规划 -- 算法问题必须要有「最优子结构」性质，才能通过子问题的最优解推导出全局最优解
            所有子问题的最优解都求出来了，然后我可以基于这些子问题的最优解推导出原问题的最优解。

贪心选择 -- 我只需要进行一些局部最优的选择策略，就能直接知道哪个子问题的解是最优的了，
            且这个局部最优解可以推导出原问题的最优解。此时此刻我就能知道，不需要等到所有子问题的解算出来才知道。
'''


# lc55 Jump Game
'''
You are given an integer array nums. 
You are initially positioned at the array's first index, 
and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.

思路1：backward 找上一个能到末尾的 index
从末尾index开始向前遍历，p不断更新上一个可以到达末尾的index，如果最后能到0，true
'''
def canJump(nums: List[int]) -> bool:
    sz = len(nums)
    pers = sz-1           # 从后往前，记录能到达的位置
    for i in range(sz-2, -1, -1):
        if nums[i] >= pers - i:     # 当前index可以到头
            pers = i

    if pers == 0:
        return True
    return False

'''
思路1.1：加油  
一次走一步（i），gas用一格，如果此处油多于现有则加油继续走
'''

'''
思路2：贪心
子问题 -- recursively下一步谁能走的更远
'''
def canJumpGreedy(nums: List[int]) -> bool:
    n = len(nums)
    farthest = 0
    for i in range(n - 1):
        # 不断计算能跳到的最远距离
        farthest = max(farthest, i + nums[i])
        # 可能碰到了 0，卡住跳不动了
        if farthest <= i:
            return False
    return farthest >= n - 1

'''
思路3：DP + 剪枝（方法1：返回布尔值）
子问题 -- 从当前index能否到达末尾

- dp(i) = 从位置i能否到达末尾（布尔值）
- 枚举所有可能的下一步，只要有一条路径能到达，返回True
'''
def canJumpDP(nums: List[int]) -> bool:
    memo = {}     # index: 能否到达末尾 (True/False)

    # 状态转移方程
    # input：from index
    # return：能否到达末尾
    def canReachEnd(from_ind: int) -> bool:
        # base case: 已经到达或超过末尾
        if from_ind >= len(nums) - 1:
            return True
        
        # 剪枝：查memo
        if from_ind in memo:
            return memo[from_ind]
        
        # 枚举所有可能的下一步
        max_jump = nums[from_ind]
        for step in range(1, max_jump + 1):
            next_pos = from_ind + step
            if canReachEnd(next_pos):
                memo[from_ind] = True
                return True
        
        # 所有路径都走不通
        memo[from_ind] = False
        return False
    
    return canReachEnd(0)



# lc45 jump game II
'''
You are given a 0-indexed array of integers nums of length n. You are initially positioned at index 0.

Each element nums[i] represents the maximum length of a forward jump from index i.
In other words, if you are at index i, you can jump to any index (i + j) where:

思路： 与lc55 主要区别 -- 需要计算最短路径
DP -- 剪枝 + 跟新状态 （可行）
Greedy -- 
'''


## DP wrong review!!!
def canJumpIIDP(nums: List[int]) -> bool:

    memo = {}     # index: 从该index能到达的最远位置

    # 状态转移方程
    # input：from index
    # return：from index 到list[-1]需要的步数
    def farthestReachable(from_ind: int) -> int:
        # base case: 已经到达末尾
        if from_ind >= len(nums) - 1:
            return len(nums) - 1
        
        # 剪枝：查memo
        if from_ind in memo:
            return memo[from_ind]
        
        # 当前能跳的最远距离
        max_jump = nums[from_ind]
        # if max_jump == 0:
        #     # 当前位置无法移动
        #     memo[from_ind] = from_ind
        #     return from_ind
        
        # 枚举所有可能的下一步，找最远的
        for step in range(1, max_jump + 1):
            
            subProblem = farthestReachable(from_ind+step)

            memo[from_ind] = min(memo[from_ind], subProblem+1)
        return memo[from_ind]
    
    return farthestReachable(0)



# 贪婪： 每一次jump落在的区间里面选最远的
def canJumpII_greedy(nums: List[int]) -> bool:
    if len(nums) <= 1:
        return 0

    fartherest = 0         # 记录每格子能reach的最远地方
    end = 0                # 区间末尾
    jump_time = 0
    for i in range(len(nums)):
        fartherest = max(fartherest, i + nums[i])   # 从i可以到达的最大index -- 绝对位置

        if i == end:
            jump_time += 1
            end = fartherest
            if fartherest >= len(nums)-1:
                return jump_time

    return -1



    



if __name__ == '__main__':
    # 测试用例
    n1 = [2,3,1,1,4]      # True
    n2 = [3,2,1,0,6]      # False - 卡在0
    n3 = [3,2,2,0,0]      # True
    n4 = [0]              # True - 只有一个元素
    n5 = [2,0,0]          # True
    
    test_cases = [n1, n2, n3, n4, n5]
    
    for i, nums in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {nums}")
        print(f"  倒推法:     {canJump(nums)}")
        print(f"  贪心法:     {canJumpGreedy(nums)}")
        print(f"  DP布尔值:   {canJumpDP(nums)}")


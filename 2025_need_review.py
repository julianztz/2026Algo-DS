from collections import defaultdict
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


# smallerNumbersThanCurrent([5,0,10,0,10,6])


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


# lc1679 Max Number of K-Sum Pairs
'''
思路1: 排序 + 左右指针 n log n
'''
def maxOperations(nums: List[int], k: int) -> int:
    max_op = 0
    nums.sort()
    left = 0
    right = len(nums) - 1
    while left < right:
        if nums[left] + nums[right] < k:
            left += 1
        elif nums[left] + nums[right] > k:
            right -= 1
        else:
            max_op += 1
            left += 1
            right -= 1

    print(max_op)
    return max_op

maxOperations([1,2,3,4],5)

'''
思路2: 类似 twoSum， num：freq
'''
def maxOperations2(nums: List[int], k: int) -> int:
    checked = defaultdict(int)

    pair_counter = 0

    for idx in range(len(nums)):
        if k - nums[idx] in checked:
            pair_counter += 1
            
            checked[k - nums[idx]] -= 1
            if checked[k - nums[idx]] <= 0:
                del checked[k - nums[idx]]

        else:
            checked[nums[idx]] += 1
    
    print(pair_counter)
    return pair_counter

maxOperations2([2,2,1,1],3)  



def findMaxAverage(nums: List[int], k: int) -> float:
    n = len(nums)

    # 初始状态
    win = nums[:k]     # 0, k-1
    win_sum = sum(win)
    max_sum = win_sum

    left = 0
    while left+k < n:
        win_sum -= nums[left]
        win_sum += nums[left+k]
        max_sum = max(max_sum, win_sum)
        left += 1
    return max_sum/k
    
# findMaxAverage([3,3,4,3,0],3)
findMaxAverage([9,7,3,5,6,2,0,8,1,9],6)


# 1071 Greatest Common Divisor of Strings
'''
正确思路：
1. 如果 str1 + str2 != str2 + str1，说明没有公共因子，返回 ""
2. 找到两个字符串长度的最大公约数（GCD）
3. 返回 str1[:gcd_length]（或 str2[:gcd_length]）

关键观察：
- 如果两个字符串有公共因子，那么 str1 + str2 == str2 + str1
- GCD 的长度就是两个字符串长度的最大公约数
'''
def gcdOfStrings(str1: str, str2: str) -> str:
    # 关键检查：如果 str1 + str2 != str2 + str1，说明没有公共因子
    if str1 + str2 != str2 + str1:
        return ''
    
    # 计算两个字符串长度的最大公约数
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a
    
    gcd_length = gcd(len(str1), len(str2))
    return str1[:gcd_length]


# 345. Reverse Vowels of a String
def reverseVowels(s: str) -> str:
    res = ""

    vowels = ['a','e','i','o','u']

    p = len(s) - 1 
    for c in s:
        if c.lower() not in vowels:
            res += c
        else:
            while s[p].lower() not in vowels:
                p -= 1
            res += s[p]
            p -= 1

    print(res)
    return res   
     
# reverseVowels("IceCream")


# 238 product of array except for self
'''
suffix * prefix
'''
def productExceptSelf(nums: List[int]) -> List[int]:
    res = [1] * (len(nums))
    for i in range(1,len(nums)):
        res[i] = nums[i-1] * res[i-1]

    suffix = 1
    for i in range(len(nums)-2,-1,-1):
        suffix = nums[i+1] * suffix
        res[i] *= suffix

    return res

productExceptSelf([1,2,3,4])


# 334. Increasing Triplet Subsequence
'''
找三个递增元素
'''
def increasingTriplet(nums: List[int]) -> bool:
    res = []
    first = float("inf")
    second = float("inf")
    for n in nums:
        if n <= first:
            first = n
        elif n <= second:
            second = n
            mark_first = first
            
        else:
            res = [mark_first, second, n]
            print(res)
            return True        # 存在一个比前两个数字大

    return False

# increasingTriplet([4,5,0,6])
# increasingTriplet([40,50,3,2,3,60])


# 443. string compression
'''
双(三)指针 -- 快慢指针

slow/start -- group起点的位置
write - 写入相同char长度位置
fast -- 新char/group终点+1的位置
'''
def compress(chars: List[str]) -> int:
    fast = 0
    slow = 0  # group 起点
    write = 0  # 写入位置

    n = len(chars)
    while fast <= n:
        if fast==n or chars[fast] != chars[slow]:
            
            chars[write] = chars[slow]
            write += 1

            group_len = fast - slow
            if group_len > 1:
                for c in str(group_len):
                    chars[write] = c
                    write += 1
            slow = fast
        
        fast += 1
    return write

c = ["a","a","b","b","c","c","c"]
c2 = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
c3 = ["a","b","b","b","b","b","b","b","b","b","b","b","b","a","a","a","a"]
c4 = ['a','a']
c5 = ['a','b','c']
c6 = ['a','a','a','b']
# compress(c)


# 283. Move Zeroes 
'''
指针职责要单一
所有non-zero前移，最后剩下的都是0

'''
def moveZeroes(nums: List[int]) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    zero_seperator = 0           # 分界线 123 | 000  
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[i], nums[zero_seperator] = nums[zero_seperator], nums[i]
            zero_seperator += 1

nums = [0,1,0,3,12]          
nums2 = [1,2]
nums3 = [1,0,1]
moveZeroes(nums3)
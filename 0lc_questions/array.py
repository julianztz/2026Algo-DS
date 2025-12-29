from typing import Any, Optional, List
from collections import Counter

"""
Counter 使用说明：
Counter 本质上是 dict 的子类，专门用于计数（记录频率）

主要特性：
1. 自动处理不存在的键：访问不存在的键返回 0（不会报 KeyError）
2. 可以直接从可迭代对象创建：Counter("hello") -> Counter({'h': 1, 'e': 1, 'l': 2, 'o': 1})
3. 支持数学运算：+ - & | （并集、交集等）
4. 常用方法：most_common(n) 返回最常见的 n 个元素

示例：
    # 创建 Counter
    c1 = Counter("hello")           # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    c2 = Counter([1, 1, 2, 3, 3, 3]) # {1: 2, 2: 1, 3: 3}
    
    # 访问不存在的键返回 0（普通 dict 会报 KeyError）
    print(c1['x'])  # 0
    
    # 可以直接比较
    Counter("hello") == Counter("olleh")  # True（顺序无关）
    
    # 更新计数
    c1['l'] += 1    # {'l': 3}
    c1['l'] -= 2    # {'l': 1}
    
    # 删除元素（计数为 0 时不会自动删除，需要手动 del）
    del c1['l']
    
    # most_common() 返回最常见的元素
    Counter("aabbcc").most_common(2)  # [('a', 2), ('b', 2)]
    
与普通 dict 的区别：
    - Counter 访问不存在的键返回 0，不会报错
    - Counter 可以直接从可迭代对象创建并自动计数
    - Counter 支持 + - & | 等数学运算
    - Counter 提供 most_common() 等方法
"""


# 26 remove duplicate from sorted array
'''
Given an integer array nums sorted in non-decreasing order, 
remove the duplicates in-place such that each unique element appears only once. 
The relative order of the elements should be kept the same.

思路： 快慢指针
slow -- keep track of 无重复array -> result
fast -- loop 找不重复元素
'''
def removeDuplicatesBetter(nums: List[int]) -> int:
    if not nums:
        return 0
    
    # 双指针：slow指向下一个唯一元素应该放置的位置
    # fast遍历数组找到唯一的元素
    slow = 0
    
    for fast in range(1, len(nums)):
        # 如果fast指向的元素和slow不同，说明是新的唯一元素
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]  # 关键：原地修改数组
    
    return slow + 1  # 返回唯一元素的个数

'''
same for 实现
'''
def removeDuplicates(nums: List[int]) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return 1
    
    p1 = 0
    p2 = 1
    while p2 < len(nums):
        if nums[p2] != nums[p1]:
            p1 += 1
            nums[p1] = nums[p2]
        p2 += 1

    return p1+1


# 27 remove element
'''
remove all val from nums
The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.

思路：快慢指针
slow -- keep track of 无重复array -> result
fast -- loop 找不重复元素
'''
def removeElement(nums: List[int], val: int) -> int:
    slow = 0

    for fast in range(len(nums)):
        # 一步步移动，覆盖所有 ； skip需要删除的value
        if nums[fast] != val:
            # 2. slow 指针一步步走 储存（覆盖式）所有非target value
            nums[slow] = nums[fast]
            slow += 1

    # 如果要真正缩短数组，使用以下方法之一：
    # 方法1：使用切片赋值（推荐）
    nums[:] = nums[:slow]
    # 方法2：使用del删除后面的元素
    # del nums[slow:]
    
    return slow  # slow 已经是有效元素个数，不需要 +1

# removeElement([3,2,2,3],3)




# 283 move zeros
'''
Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

两种思路对比：

思路1 (moveZeroes): 
- slow 指向下一个非零元素应该放置的位置（类似 removeDuplicates 的思路）
- fast 遍历数组
- 当 fast 遇到非零元素时：交换并 slow += 1
- 核心：slow 维护"非零元素区"的末尾

思路2 (moveZeroes2):
- slow 指向第一个0的位置（维护"零区"的起始位置）
- fast 遍历数组
- 当 fast 遇到0时：如果 slow 不是0，则 slow = fast（记录第一个0的位置）
- 当 fast 遇到非0时：如果 slow 是0，则交换并 slow += 1
- 核心：slow 维护"零区"的起始位置

两种方法对比：
1. 时间复杂度：都是 O(n)
2. 空间复杂度：都是 O(1)
3. 交换次数：思路1 可能交换更多次（即使 slow==fast 也会交换），思路2 只在需要时交换
4. 代码简洁度：思路1 更简洁（条件判断更少）
5. 理解难度：思路1 更直观（类似 removeDuplicates），思路2 需要理解"维护零区起始位置"的概念

示例：[0, 1, 0, 3, 12]
思路1执行过程：
  fast=0: nums[0]=0, 跳过
  fast=1: nums[1]=1≠0, 交换 nums[0]↔nums[1], slow=1 → [1,0,0,3,12]
  fast=2: nums[2]=0, 跳过
  fast=3: nums[3]=3≠0, 交换 nums[1]↔nums[3], slow=2 → [1,3,0,0,12]
  fast=4: nums[4]=12≠0, 交换 nums[2]↔nums[4], slow=3 → [1,3,12,0,0]

思路2执行过程：
  fast=0: nums[0]=0, slow=0且nums[0]=0, slow不变
  fast=1: nums[1]=1≠0, slow=0且nums[0]=0, 交换 nums[0]↔nums[1], slow=1 → [1,0,0,3,12]
  fast=2: nums[2]=0, slow=1且nums[1]=0, slow不变
  fast=3: nums[3]=3≠0, slow=1且nums[1]=0, 交换 nums[1]↔nums[3], slow=2 → [1,3,0,0,12]
  fast=4: nums[4]=12≠0, slow=2且nums[2]=0, 交换 nums[2]↔nums[4], slow=3 → [1,3,12,0,0]
'''
def moveZeroes(nums) -> None:
    """
    思路1: slow 指向下一个非零元素应该放置的位置
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
    print(nums)

# moveZeroes([0,1,0,3,12])

def moveZeroes2(nums) -> None:
    """
    思路2: slow 记录第一个0的位置，fast 遍历数组
    - 当 fast 遇到0时：如果 slow 不是0，则 slow = fast（记录第一个0的位置）
    - 当 fast 遇到非0时：如果 slow 是0，则交换并 slow += 1
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] == 0:
            if nums[slow] != 0:
                slow = fast         # slow 记住第一个0位置
        else:
            if nums[slow] == 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1

    print(nums)



# 344 reverse string
'''
Write a function that reverses a string. The input string is given as an array of characters s.

You must do this by modifying the input array in-place with O(1) extra memory.

思路：左右指针，交换位置
'''
def reverseString(s: List[str]) -> None:
    left = 0
    right = len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1

def reverseStringPythonic(s: List[str]) -> None:
    s[:] = s[::-1]

def reverseStringFast(s) -> None:
    s.reverse()


# reverseStringPythonic(["h","e","l","l","o"])


# 167 two sum 2 -- sorted input array
'''
Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, 
find two numbers such that they add up to a specific target number. 
Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers, index1 and index2, 
added by one as an integer array [index1, index2] of length 2.

思路： 左右指针 -- 因为array is sorted！好办
left + right > tar --> right - 1
left + right < tar --> left + 1

思路2：借助dictionary -- 更适合未排序的list
'''
def twoSumSorted(numbers: List[int], target: int) -> List[int]:
    left = 0
    right = len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s > target:
            right -= 1
        elif s < target:
            left += 1
        else:
            return [left+1, right+1]
    return []


# 5 longest palindrome substring
'''
思路： 左右指针
遍历整个 string 以每一个char为中心，找到其最大palindrome substring
'''
# "b a b a d"
def longestPalindrome(s: str) -> str:
    longestStr = ""
    for i in range(len(s)):
        s1 = findPalindrome(s, i, i)  # 单个i中心 找palindrome str
        s2 = findPalindrome(s, i, i+1)  # 两个i，i+1中心 找palindrome str
        # print(s1)
        longestStr = s1 if len(s1) > len(longestStr) else longestStr
        longestStr = s2 if len(s2) > len(longestStr) else longestStr

    print(longestStr)


def findPalindrome(s, l, r):

    while l>=0 and r<len(s) and s[l] == s[r]:
        l = l-1
        r = r+1

    return s[l+1: r]


# longestPalindrome("babad")
# longestPalindrome("aab")



# 151 reverse words in string
'''
A word is defined as a sequence of non-space characters. 
The words in s will be separated by at least one space.
Return a string of the words in reverse order concatenated by a single space.

思路1：split by “ ” save in list, then reverse list
    转化成list 之后双指针原地反转 O1 space
'''
def reverseWords(s: str) -> str:
    arr = s.split()
    l = 0
    r = len(arr) - 1
    while l < r:
        arr[l], arr[r] = arr[r], arr[l]
        l += 1
        r -= 1

    s = " ".join(arr)
    # print(s)
    return s
print(reverseWords("hi hello    world   "))

def reverseWords2(s: str) -> str:
    word_list = s.split()
    res = ''
    for word in reversed(word_list):
        res+=word+" "
    return res.strip()

# pythonic
# " ".join(reversed(s.split()))


# 48 rotate image
'''
You are given an n x n 2D matrix representing an image, 
rotate the image by 90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. 
DO NOT allocate another 2D matrix and do the rotation.

思路： None
提示--diagonal交换matrix[i][j]位置再进行每行反转
'''
def rotateClockwise(matrix: List[List[int]]) -> None:
    """
    Do not return anything, modify matrix in-place instead.
    """
    n = len(matrix)
    for row in range(n):
        for col in range(row, n):
            matrix[row][col], matrix[col][row] = matrix[col][row], matrix[row][col]

    for row in matrix:
        row.reverse()

def rotateCounterClockwise(matrix: List[List[int]]) -> None:
    """
    Do not return anything, modify matrix in-place instead.
    """
    n = len(matrix)
    for row in matrix:
        row.reverse()

    for row in range(n):
        for col in range(row, n):
            matrix[row][col], matrix[col][row] = matrix[col][row], matrix[row][col]

# 54 spiral order
'''
Given an m x n matrix, return all elements of the matrix in spiral order.
input：
1 2 3
4 5 6
7 8 9
output:
123698745

思路：递归/DP？？？ 
base case: 到头 -- element已经在res list中

'''
def spiralOrder(matrix: List[List[int]]) -> List[int]:

    row = len(matrix)
    col = len(matrix[0])

    def traverse(matrix, row, ):
        pass





# 15 3 Sum
'''
找到三个elements sum up to 0

方法1：依赖twoSum（复杂，需要处理索引映射和去重）
方法2：排序+双指针（推荐，更简洁高效）
思路：
1. 先排序数组（方便去重和双指针）
2. 固定第一个元素nums[i]
3. 在剩余部分用双指针找twoSum（left从i+1开始，right从末尾开始）
4. 通过跳过重复元素来去重，不需要set

时间复杂度：O(n²) - 排序O(nlogn) + 双重循环O(n²)
空间复杂度：O(1) - 除了结果数组，只用常量空间
'''
def threeSum(nums: List[int]) -> List[List[int]]:
    res = []
    nums.sort()  # 排序，方便去重和双指针
    
    for i in range(len(nums) - 2):  # 至少需要3个元素
        # 跳过重复的第一个元素
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        left = i + 1
        right = len(nums) - 1
        target = -nums[i]  # 需要在剩余部分找和为-nums[i]的两个数
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                # 找到三元组
                res.append([nums[i], nums[left], nums[right]])
                
                # 跳过重复的left和right
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1  # 和太小，左指针右移
            else:
                right -= 1  # 和太大，右指针左移
    
    return res


# $$$ todo 18 4 Sum -- recursive
def fourSum(nums: List[int], target: int) -> List[List[int]]:
    pass



# 88 merge two sorted arrays 
'''
You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, 
and two integers m and n, representing num1 & num2 中交换的有效元素

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside the array nums1.
To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, 
and the last n elements are set to 0 and should be ignored. nums2 has a length of n.

思路 WRONG！！！ swap num1和num2，把小数换到num1，剩下的num2 接到num1后面   
     [1,2,3,4] 
     [2,2,3]     导致错误！！！

思路 right： backward遍历，双指针--先将大的数字存到nums1最后--尾部安全space，依次向前
    利用尾部空间避免覆盖values
    
    关键理解：nums1末尾必须有n个0作为"安全空间"
    - nums1总长度 = m + n
    - 前m个元素：有效元素（参与合并）
    - 后n个元素：占位符0（安全空间，用于存放合并结果）
    
    例子：
    - 如果n=3：nums1末尾需要3个0 → [1,2,3,0,0,0]
    - 如果n=6：nums1末尾需要6个0 → [1,2,3,0,0,0,0,0,0]
    为什么？因为最多可能需要n个位置来存放nums2的元素！

'''

def merge(nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    """
    Do not return anything, modify nums1 in-place instead.
    
    为什么从后往前合并能避免覆盖？
    
    关键理解：
    1. nums1末尾的0是"安全空间"：这些位置本身就是为结果预留的
    2. 从后往前填充：每次填充的是"已确定不会再需要"的位置
    3. 覆盖顺序保证：即使覆盖nums1的有效元素，那也是"已经用过"的
    
    例子：nums1=[1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3
    初始：[1,2,3,0,0,0]  ← 末尾3个0是安全空间
          ↑     ↑  ↑  ↑
        nums1有效  0占位符
    
    步骤：
    - p=5: 比较nums1[2]=3和nums2[2]=6 → 6更大 → nums1[5]=6
      [1,2,3,0,0,6]  ← 覆盖了0（安全），nums1[2]=3已用，不会再需要
      
    - p=4: 比较nums1[2]=3和nums2[1]=5 → 5更大 → nums1[4]=5
      [1,2,3,0,5,6]  ← 覆盖了0（安全），nums1[2]=3已用
      
    - p=3: 比较nums1[2]=3和nums2[0]=2 → 3更大 → nums1[3]=3
      [1,2,3,3,5,6]  ← nums1[2]=3被覆盖，但它已经"用过"了（复制到了p=3）
      
    为什么不会覆盖未处理的值？
    - nums1[i]被覆盖时，它的值已经被复制到后面的位置了
    - 我们从后往前填充，确保覆盖的都是"已使用"的值
    - 前面的值还没处理，所以不会被覆盖
    
    关键观察：当第一个循环结束时（i < 0 且 j >= 0），
    j的值恰好等于nums1中未被覆盖的目标位置索引！
    因此可以直接用 nums1[j] = nums2[j]，而不需要额外的p指针。
    """
    i = m - 1  # nums1有效元素的末尾
    j = n - 1  # nums2的末尾
    p = len(nums1) - 1  # nums1总末尾（目标位置）

    while i >= 0 and j >= 0:
        if nums1[i] >= nums2[j]:
            nums1[p] = nums1[i]  # 从nums1取较大值，nums1[i]已用，可以覆盖
            i -= 1
        else:
            nums1[p] = nums2[j]  # 从nums2取较大值
            j -= 1
        p -= 1  # 从后往前填充

    # 如果nums2还有剩余，j的位置正好对应nums1中未被覆盖的位置
    while j >= 0:
        nums1[j] = nums2[j]
        j -= 1
    
    # nums1的剩余元素（如果有）已经在正确位置，不需要处理

    print(nums1)

# merge([1,2,3,4,0,0,0],4,[2,2,3],3)
# merge([2,2,3,0,0,0,0],3,[1,2,3,4],4)



# 前缀问题
# 303 range sum query - Immutable
'''
Given an integer array nums, handle multiple queries of the following type:
Calculate the sum of the elements of nums between indices left and right inclusive.

思路：前缀和（Prefix Sum）
- 初始化时计算前缀和数组：preSum[i] = sum(nums[0...i-1])
- 查询sumRange(left, right) = preSum[right+1] - preSum[left]

时间复杂度：
- __init__: O(n) - 需要遍历数组一次
- sumRange: O(1) - 只需要一次减法操作

空间复杂度：
- O(n) - 存储前缀和数组

优化：
1. 如果数组是不可变的，可以删除self.nums节省空间
2. 使用列表推导式可以让代码更简洁（但不一定更快）
3. 空间复杂度已经是最优（O(n)），无法再优化
'''
class NumArray:

    def __init__(self, nums: List[int]):
        # 初始化前缀和数组，preSum[0] = 0
        # preSum[i] = sum(nums[0...i-1])
        self.preSum = [0]
        for num in nums:
            self.preSum.append(self.preSum[-1] + num)
        
        # 优化：如果数组不可变，可以删除self.nums节省空间
        # 但对于可变数组，需要保留原数组用于更新
        # self.nums = nums  # 可选：根据需要决定是否保留
        
    def sumRange(self, left: int, right: int) -> int:
        """
        返回nums[left...right]的和（包含两端）
        
        时间复杂度：O(1)
        使用前缀和：sumRange(left, right) = preSum[right+1] - preSum[left]
        
        为什么是right+1？
        - preSum[i] = sum(nums[0...i-1])
        - 所以preSum[right+1] = sum(nums[0...right])
        - preSum[left] = sum(nums[0...left-1])
        - 相减得到：sum(nums[left...right])
        """
        return self.preSum[right + 1] - self.preSum[left]


# 304 range sum 2D matrix
class NumMatrix:
    # preSum[i][j] 记录矩阵 [0, 0, i-1, j-1] 的元素和
    def __init__(self, matrix: List[List[int]]):
        m = len(matrix)
        n = len(matrix[0])
        if m == 0 or n == 0:
            return
        # 构造前缀和矩阵
        self.preSum = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # 计算每个矩阵 [0, 0, i, j] 的元素和
                self.preSum[i][j] = (self.preSum[i - 1][j] + self.preSum[i][j - 1] +
                                     matrix[i - 1][j - 1] - self.preSum[i - 1][j - 1])

    # 计算子矩阵 [x1, y1, x2, y2] 的元素和
    def sumRegion(self, x1: int, y1: int, x2: int, y2: int) -> int:
        # 目标矩阵之和由四个相邻矩阵运算获得
        return (self.preSum[x2 + 1][y2 + 1] - self.preSum[x1][y2 + 1] -
                self.preSum[x2 + 1][y1] + self.preSum[x1][y1])

# 724 Find Pivot Index -- 前缀问题
'''
问题定义：找到索引 i，使得 nums[0...i-1] 的和 = nums[i+1...n-1] 的和

❌ 双指针方法的问题（即使单独处理 index 0 也不行）：
1. **核心问题：概念不匹配**
   - 双指针比较的是"从左边累加的和" vs "从右边累加的和"
   - 但 pivot 需要的是"索引左边所有元素之和" vs "索引右边所有元素之和"
   - 这两个概念完全不同！

2. **具体失败案例：**
   
   案例1: [1, 1, 1, 1, 1]
   - 双指针：left=0(sum=1), right=4(sum=1) → 返回 1
   - 但索引 1 不是 pivot（左边 [1]=1，右边 [1,1,1]=3，不相等）
   - 真正的 pivot 是索引 2（左边 [1,1]=2，右边 [1,1]=2）
   - 问题：双指针在第一步就误判了
   
   案例2: [-1, -1, -1, -1, 0, 1]
   - 真正的 pivot 是索引 1（左边 [-1]=-1，右边 [-1,-1,0,1]=-1）
   - 但双指针一直移动 left，直到结束，返回 -1
   - 问题：双指针无法找到中间的 pivot

3. **为什么单独处理 index 0 不够：**
   - 虽然能解决 [1, -1, 1] 和 [2, 1, -1] 这类边界情况
   - 但无法解决上述两个案例中的根本性问题
   - 双指针的逻辑本身就不适用于这个问题

✅ 正确思路：前缀和（Prefix Sum）
- 对于索引 i，左边和 = preSum[i]，右边和 = total - preSum[i] - nums[i]
- 遍历每个索引，检查 leftSum == rightSum

时间复杂度：O(n)
空间复杂度：O(1) - 只需要常量空间
'''
def pivotIndex(nums: List[int]) -> int:
    # left = 0
    # right = len(nums) - 1
    # leftSum = nums[left]
    # rightSum = nums[right]
    # while left < right:     # <=??

    #     if leftSum < rightSum:
    #         left += 1
    #         leftSum += nums[left]
    #     elif leftSum > rightSum:
    #         right -= 1
    #         rightSum += nums[right]
    #     elif leftSum == rightSum:
    #         if left+1 == right:
    #             return -1
    #         return left+1

    # if sum(nums) == 0:
    #     return 0
    """
    使用前缀和思想，但优化为 O(1) 空间复杂度
    
    核心思路：
    - 对于索引 i，左边和 = sum(nums[0...i-1])
    - 右边和 = sum(nums[i+1...n-1]) = total - leftSum - nums[i]
    - 当 leftSum == rightSum 时，即 leftSum == total - leftSum - nums[i]
    - 化简：2 * leftSum == total - nums[i]
    """
    total = sum(nums)
    leftSum = 0
    
    for i in range(len(nums)):
        # 左边和 = 右边和 （总和 - 左边和 - 当前元素）
        # 如果左边和 == 右边和，则找到 pivot
        if leftSum == total - leftSum - nums[i]:
            return i
        leftSum += nums[i]
    
    return -1

# 238 前缀*后缀
'''
Given an integer array nums, return an array answer such that answer[i] 
is equal to the product of all the elements of nums except nums[i].
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
You must write an algorithm that runs in O(n) time and without using the division operation.
思路1：nested loop                     n^2    -- Tc不符合
思路2：prefix 总乘积/nums[i];           n     -- 需要除法
       特别处理0：1个0，该位置为其他num乘积 ；两个以上0，全部为0
思路3： prefix * suffix
'''

# O n O n
def productExceptSelf(nums: List[int]) -> List[int]:
    prefix = [1] * (len(nums))
    suffix = [1] * (len(nums))
    for i in range(1,len(nums)):
        prefix[i] = nums[i-1] * prefix[i-1]

    for i in range(len(nums)-2,-1,-1):
        suffix[i] = nums[i+1] * suffix[i+1]

    print(prefix)
    print(suffix)

    res = []
    for i in range(len(nums)):
        res.append(prefix[i]*suffix[i])
    print(res)
    return res

# O n  O 1
def productExceptSelf_O1Space(nums: List[int]) -> List[int]:
    res = [1] * (len(nums))
    for i in range(1,len(nums)):
        res[i] = nums[i-1] * res[i-1]

    suffix = 1
    for i in range(len(nums)-2,-1,-1):
        suffix = nums[i+1] * suffix
        res[i] *= suffix

    print(res)
    return res

# 525 前缀
'''
Given a binary array nums, return the maximum length 
of a contiguous subarray with an equal number of 0 and 1.
Input: nums = [0,1,1,1,1,1,0,0,0]
Output: 6
Explanation: [1,1,1,0,0,0] is the longest contiguous subarray with equal number of 0 and 1.
'''
def findMaxLength(nums: List[int]) -> int:
    n = len(nums)
    preSum = [0] * (n + 1)
    # 计算 nums 的前缀和
    for i in range(n):
        preSum[i + 1] = preSum[i] + (-1 if nums[i] == 0 else 1)

    print(preSum)

    val_to_index = {}
    res = 0
    for i in range(len(preSum)):
        # 如果这个前缀和还没有对应的索引，说明这个前缀和第一次出现，记录下来
        if preSum[i] not in val_to_index:
            val_to_index[preSum[i]] = i
        else:
            # 这个前缀和已经出现过了，则找到一个和为 0 的子数组
            res = max(res, i - val_to_index[preSum[i]])
        # 因为题目想找长度最大的子数组，所以前缀和索引应尽可能小
    return res




# 76 minimum window substring HARD
'''
Given two strings s and t of lengths m and n respectively,
return the minimum window substring of s such that 
every character in t (including duplicates) is included in the window. 
If there is no such substring, return the empty string "".

Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"

思路：快慢指针 + 滑动窗口
'''
def minWindow(s: str, t: str) -> str:
    res = ""
    min_len = len(s)

    need = {}           # 记录t中出现过的char数量
    window = {}         # 每个字符出现过的次数
    for char in t:
        need[char] = need.get(char, 0) + 1

    for char in t:
        window[char] = 0

    
    l = 0
    r = 0

    # 0. 初始状态： 存入s[0]
    if s[0] in window:
        window[s[0]] += 1

    while r < len(s):   # chk logic

        # 1. 右移r扩大：if need中没有记录全部
        if not validWindow(window, need):    
            r += 1

            # right 指针 存入window
            if r!=l and r < len(s) and s[r] in window:
                window[s[r]] += 1

        # 2. 左移l缩小：window 包含了所有需要元素（个数）
        else:
            #  3. 更新最小string
            if r-l+1 <= min_len: 
                min_len = r-l+1
                res = s[l:r+1]

            if s[l] in window:
                window[s[l]] -= 1

            l += 1
        
    print(res)
    return res


# window contains all letters from need 数量也一致！
def validWindow(win, need) -> bool:
    for k in need.keys():
        if win[k] < need[k]:
            return False
    return True


# minWindow("ADOBECODEBANCB", "ABCB")
# minWindow("a","a")


def minWindowFast(s: str, t: str) -> str:
    need, window = {}, {}
    for c in t:
        need[c] = need.get(c, 0) + 1

    left = 0
    right = 0
    valid = 0
    # 记录最小覆盖子串的起始索引及长度
    start = 0
    length = float('inf')
    while right < len(s):
        # c 是将移入窗口的字符
        c = s[right]
        # 扩大窗口
        right += 1
        # 进行窗口内数据的一系列更新
        if c in need:
            window[c] = window.get(c, 0) + 1
            if window[c] == need[c]:
                valid += 1

        # 判断左侧窗口是否要收缩
        while valid == len(need): 

            # 在这里更新最小覆盖子串
            if right - left < length:
                start = left
                length = right - left
            # d 是将移出窗口的字符
            d = s[left]
            # 缩小窗口
            left += 1
            # 进行窗口内数据的一系列更新
            if d in need:
                if window[d] == need[d]:
                    valid -= 1
                window[d] -= 1


    # 返回最小覆盖子串
    return "" if length == float('inf') else s[start: start + length]


# 567. Permutation in String MED
'''
Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.
In other words, return true if one of s1's permutations is the substring of s2.

Input: s1 = "ab", s2 = "eidbaooo"
Output: true

思路：与76 minWindow 类似，快慢指针+滑动窗口；（需要连续）定长窗口
'''

# counter 记录freq
def checkInclusionSet(s1: str, s2: str) -> bool:
    """
    方案1: 使用 Counter 快速修复（简单但稍慢）
    问题：set 无法区分频率，必须用 Counter 或字典记录频率
    """
    targetLen = len(s1)
    targetCount = Counter(s1)   # 用 Counter 记录 s1 的字符频率
    
    for i in range(len(s2) - targetLen + 1):
        frag = s2[i:i+targetLen]
        fragCount = Counter(frag)  # 检查每个窗口的频率
        
        if fragCount == targetCount:  # Counter 可以直接比较
            print("FOUND!", targetCount, " -- ", fragCount)
            return True
    
    return False

# sliding window 
def checkInclusionSetOptimized(s1: str, s2: str) -> bool:
    """
    方案2: 滑动窗口 + Counter（最优解 O(n)）
    固定窗口大小滑动，只更新窗口两端的变化，避免重复创建 Counter
    """
    if len(s1) > len(s2):
        return False
    
    targetLen = len(s1)
    targetCount = Counter(s1)
    windowCount = Counter(s2[:targetLen])  # 初始窗口
    
    if windowCount == targetCount:
        return True
    
    # 滑动窗口：每次移除左边一个字符，添加右边一个字符
    for i in range(targetLen, len(s2)):
        # 移除左边字符
        left_char = s2[i - targetLen]
        windowCount[left_char] -= 1
        if windowCount[left_char] == 0:
            del windowCount[left_char]
        
        # 添加右边字符
        right_char = s2[i]
        windowCount[right_char] += 1
        
        # 检查是否匹配
        if windowCount == targetCount:
            return True
    
    return False

# checkInclusionSet("ab","eidbaooo")
# checkInclusionSet("ab","eidboaooo")
# checkInclusionSet("hello", "ooolleoooleh")
            

# 438 find all anagrams in string
'''
Given two strings s and p, return an array of all the start indices of p's anagrams in s.
You may return the answer in any order.

Input: s = "cbaebabacd", p = "abc"
Output: [0,6]

思路：双指针，定长滑动窗口
'''
def findAnagrams(s: str, p: str) -> List[int]:
    need = {}
    window = {}
    need = Counter(p)    # dictionary 子类，快速记录element以及freq
    print(need)

    res = []
    valid = 0    # 记录符合要求char数量
    left = 0
    right = 0
    while right < len(s):
        r = s[right]
        # 判断eight -- 加入window
        if r in need:
            window[r] = window.get(r,0) + 1
            if window[r] == need[r]:
                valid += 1
        right += 1

        # 判断左边 -- 移出 window
        if right - left >= len(p):         # while??
            # 找到符合！
            if valid == len(need):
                res.append(left)

            l = s[left]
            if l in need:
                # 同个char出现多次，valid只需要记录一次
                if window[l] == need[l]:
                    valid -= 1
                window[l] -= 1
            left += 1
    print(res)
    return res



# findAnagrams("cbaebabacd", "abc")
# findAnagrams("paa","aa")



# 3. Longest Substring Without Repeating Characters
'''
Given a string s, find the length of the longest substring without duplicate characters.

Input: s = "abcabcbb"
Output: 3

'''
def lengthOfLongestSubstring(s: str) -> int:
    res = 0
    left = 0
    right = 0
    map = {}

    # 1. when移动right指针：目前没有重复
    # 2. when移动left指针：新char造成重复
    # 3. when更新res： 移动left直至没重复
    while right < len(s):
        right_char = s[right]
        right += 1

        # 无重复 -- add right
        map[right_char] = map.get(right_char,0) + 1

        # 新char造成重复 -- 一直remove left，直到新char无重复
        while map[right_char] > 1:
            map[s[left]] -= 1
            left += 1
        
        # left-right无重复 更新result！
        res = max(right-left, res)
    
    print(res)



# lengthOfLongestSubstring("abcabcbb")
# lengthOfLongestSubstring("abcc")



# 704 binary search
'''
思路1：左右两边找到middle point 不断更新left和right return 结果
思路2：左右recursive， return 结果
'''
def search(nums: List[int], target: int) -> int:
    left, right = 0, len(nums)-1
    while left <= right: 
        mid = (left + right) // 2        # floor divide 5//2 = 2
        if nums[mid] < target:
            left = mid + 1              # 移除mid 缩小窗口至右半边
        elif nums[mid] > target:
            right = mid - 1             # 移除mid 缩小窗口至左半边
        elif nums[mid] == target:
            print(mid)
            return mid
    return -1

def searchRecursive(nums: List[int], target: int) -> int:
    def helper(left, right):
        # target not found
        if left > right: 
            return -1

        mid = (left + right) // 2

        # search(right half)
        if nums[mid] < target:
            return helper(mid+1, right)

        # search(left half)
        elif nums[mid] > target:
            return helper(left, mid-1)
        
        # target found
        elif nums[mid] == target:
            return mid

    return helper(0, len(nums)-1)
    

# 875 koko eating banana
'''
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. 
The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. 
If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.
思路：提炼speed(x)与时间(h) 之间的关系 f(x) = h
      二分法选择x ；right_bounded
'''
def minEatingSpeed(piles: List[int], h: int) -> int:
    piles.sort()
    # 二分法选择 x 区间，传递给speedFunc得到时间与 h 比较

    left = 1
    right = piles[-1]
    speed = -1
    while left <= right:
        mid = (left + right) // 2

        timeToFinish = speedFunc(piles, mid)
        if timeToFinish <= h:    # 吃的太快，减速 （速度ok，与==h 归为一类）
            speed = mid           # 记录valid speed
            right = mid - 1
        elif timeToFinish > h:  # 吃的太慢，加速
            left = mid + 1

        # elif timeToFinish == h:    # 时间充裕，一点点放慢速度
        #     left += 1
        #     speed = mid
    print(speed)
    return speed

    

# koko 以速度x 吃完piles所有香蕉的用时
def speedFunc(piles, x) -> int:
    hours = 0
    for b in piles:
        hours += b // x
        if b % x > 0:
            hours += 1
    # print(hours)
    return hours



'''
1011 Capacity To Ship Packages Within D Days

A conveyor belt has packages that must be shipped from one port to another within days days.

The ith package on the conveyor belt has a weight of weights[i].
Each day, we load the ship with packages on the conveyor belt (in the order given by weights). 
We may not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.

思路：binary search + daysTake function
'''

# 船的运载能力为goods时，运送weights[] 货物花费的时间
def daysTake(weights, goods):
    days = 1
    capacity = goods
    i = 0
    while i < len(weights):
        if capacity < weights[i]:             # 空间不够
            capacity = goods
            days += 1
        # else:                                 # 空间够，继续装货
        capacity -= weights[i] 

        i += 1
    print(days)
    return days

# better logic
def f(weights: List[int], x: int) -> int:
    days = 0
    # 尽可能多的装货
    i = 0
    while i < len(weights):
        cap = x
        while i < len(weights):
            if cap < weights[i]:
                break
            else:
                cap -= weights[i]
                i += 1
        days += 1
    print(days)
    return days
    

def shipWithinDays(weights: List[int], days: int) -> int:
    left = 0            # 最小capacity
    right = 1           # 最大capacity

    for w in weights:
        left = max(left, w)
        right += w
    print(left, right)

    while left < right:
        mid = (left+right)//2     # capacity
        if daysTake(weights, mid) <= days:
            right = mid
        else:
            left = mid + 1
    
    return left
        



if __name__ == '__main__':
    # search([-1,0,3,5,9,12], 2)


    ### koko eat banana
    # speedFunc([30,11,23,4,20], 10)
    # speedFunc([3, 6, 7, 11], 8)
    # minEatingSpeed([3, 6, 7, 11], 8)
    # minEatingSpeed([30,11,23,4,20], 5)


    ### ship capacity
    # daysTake([1,2,3,1,1],3)
    # f([1,2,3,1,1],3)
    # shipWithinDays([1,2,3,1,1],3)

    # pivotIndex([1,7,3,6,5,6])
    # pivotIndex([1,2,3])

    # productExceptSelf_O1Space([1,2,3,4])
    # productExceptSelf_O1Space([-1,1,0,3,-3])

    # findMaxLength([0,1,0])
    
    # 比较 moveZeroes 和 moveZeroes2
    print("=== 比较 moveZeroes 和 moveZeroes2 ===\n")
    test_cases = [
        [0, 1, 0, 3, 12],
        [0, 0, 1],
        [1, 0, 0, 3, 12],
        [1, 2, 3, 4, 5],
        [0, 0, 0],
        [1, 0, 2, 0, 3, 0],
    ]
    
    for test in test_cases:
        print(f"输入: {test}")
        nums1 = test.copy()
        nums2 = test.copy()
        
        moveZeroes(nums1)
        moveZeroes2(nums2)
        
        print(f"moveZeroes:   {nums1}")
        print(f"moveZeroes2:  {nums2}")
        print(f"结果相同: {nums1 == nums2}\n")


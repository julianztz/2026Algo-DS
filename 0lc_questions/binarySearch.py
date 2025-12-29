
from typing import List

# lc35 search insert position
'''
         ind   0 1 2 3   
Input: nums = [1,3,5,6], target = 5
Output: 2

思路： binarySearch
'''
def searchInsert(nums: List[int], target: int) -> int:
    left = 0
    right = len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if target < nums[mid]:
            right = mid - 1            # !!! 跳过mid
        elif target > nums[mid]:
            left = mid + 1               # !!! 跳过mid
        elif target == nums[mid]:
            return mid

    return left


# lc392 Is Subsequence
'''
Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) 
of the characters without disturbing the relative positions of the remaining characters. 
(i.e., "ace" is a subsequence of "abcde" while "aec" is not).

ie.
Input: s = "abc", t = "ahbgdc"
Output: true
Input: s = "axc", t = "ahbgdc"
Output: false

Follow up: Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 10^9, 
and you want to check one by one to see if t has its subsequence. In this scenario, how would you change your code?

═══════════════════════════════════════════════════════════════
方法1：双指针（推荐用于单次查询）
═══════════════════════════════════════════════════════════════
时间复杂度：O(n)，其中 n = len(t)
空间复杂度：O(1)

优点：
- 简单直观
- 时间复杂度最优（单次查询）
- 空间复杂度最优

缺点：
- 对于多次查询，每次都要遍历 t


'''
def isSubsequence(s: str, t: str) -> bool:
    """
    双指针方法：时间复杂度 O(n)，其中 n = len(t)
    
    思路：
    - pt 指向 s 的当前位置
    - 遍历 t，如果 t[i] == s[pt]，则 pt 前进
    - 如果 pt 到达 s 的末尾，说明 s 是 t 的子序列

    """
    if len(s) > len(t):
        return False
    if s == '':
        return True

    pt = 0
    for i in range(len(t)):
        if pt == len(s):
            break

        if t[i] == s[pt]:
            pt += 1

    return pt == len(s)


'''
TODO
═══════════════════════════════════════════════════════════════
方法2：二分查找（推荐用于多次查询）
═══════════════════════════════════════════════════════════════
时间复杂度：
- 预处理：O(n)
- 每次查询：O(m * log(n))，其中 m = len(s)
- k 次查询：O(n + k * m * log(n))

空间复杂度：O(n) - 存储每个字符的位置列表

优点：
- 预处理一次 t，可以快速查询多个 s
- 对于大量查询，比双指针更高效

缺点：
- 需要额外空间存储位置信息
- 单次查询比双指针慢（因为需要二分查找）

适用场景：
- Follow-up 问题：有很多 s 需要检查
- t 很大，但需要查询很多次
'''

class IsSubsequenceOptimized:
    """
    进一步优化：如果有很多 s 需要检查，可以预处理一次 t，然后快速查询多个 s
    """
    def __init__(self, t: str):
        """
        预处理 t，记录每个字符的位置
        时间复杂度：O(n)
        """
        from collections import defaultdict
        self.char_positions = defaultdict(list)
        for i, char in enumerate(t):
            self.char_positions[char].append(i)
    
    def check(self, s: str) -> bool:
        """
        检查 s 是否是 t 的子序列
        时间复杂度：O(m * log(n))，其中 m = len(s), n = len(t)
        """
        import bisect
        prev_pos = -1
        
        for char in s:
            if char not in self.char_positions:
                return False
            
            positions = self.char_positions[char]
            idx = bisect.bisect_right(positions, prev_pos)
            
            if idx >= len(positions):
                return False
            
            prev_pos = positions[idx]
        
        return True

# 566 reshape the matrix
'''
思路：把mat变成linear，然后按照r，c构造新matrix
'''
def matrixReshape(mat: List[List[int]], r: int, c: int) -> List[List[int]]:
    row = len(mat)
    col = len(mat[0])

    if row * col != r * c:
        # print(mat)
        return mat

    linear_mat = []
    for r_mat in range(row):
        for c_mat in range(col):
            linear_mat.append(mat[r_mat][c_mat])

    # print(linear_mat)

    res = []
    idx = 0
    for i in range(r):
        r_mat = []
        for j in range(c):
            r_mat.append(linear_mat[idx])
            idx += 1
        res.append(r_mat)

    print(res)
    return res


# 74 (binary) search 2D matrix
'''
2D matrix 从上到下，从左到右递增
判断target是否在matrix中，要求时间复杂度 O(log(m*n))

你的思路：
2D -> linear array，然后 binarySearch
- 优点：思路清晰，代码易懂
- 缺点：需要 O(m*n) 时间和空间来展平矩阵

优化思路：
直接计算索引映射，不需要展平
- linear_idx -> (row, col): row = linear_idx // col, col = linear_idx % col
- 优点：O(log(m*n)) 时间，O(1) 空间
- 缺点：需要计算索引映射，代码稍复杂

两种方法对比：
- 你的方法：O(m*n) 时间，O(m*n) 空间，但代码清晰
- 优化方法：O(log(m*n)) 时间，O(1) 空间，但需要索引计算

如果数据量不大，你的方法完全可以接受！
'''
def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    """
    你的实现：展平后二分搜索
    
    时间复杂度：O(m*n) - 展平矩阵需要 O(m*n)
    空间复杂度：O(m*n) - 需要存储展平后的数组
    
    逻辑正确，但效率可以优化
    """
    row = len(matrix)
    col = len(matrix[0])

    linear_mat = []
    for r_mat in range(row):
        for c_mat in range(col):
            linear_mat.append(matrix[r_mat][c_mat])

    left = 0
    right = len(linear_mat)-1
    while left <= right:
        mid = (left + right) // 2
        if linear_mat[mid] == target:
            return True
        elif linear_mat[mid] > target:
            right = mid - 1
        elif linear_mat[mid] < target:
            left = mid + 1
    return False


def searchMatrixOptimized(matrix: List[List[int]], target: int) -> bool:
    """
    优化版本：直接计算索引映射，不需要展平
    
    时间复杂度：O(log(m*n))
    空间复杂度：O(1)
    
    核心思想：
    - 将 2D 矩阵视为一维数组
    - 对于线性索引 mid，计算对应的 2D 位置：
      - row = mid // col
      - col = mid % col
    """
    if not matrix or not matrix[0]:
        return False
    
    row = len(matrix)
    col = len(matrix[0])
    
    left = 0
    right = row * col - 1
    
    while left <= right:
        mid = (left + right) // 2
        # 计算 mid 对应的 2D 位置
        mid_row = mid // col
        mid_col = mid % col
        mid_val = matrix[mid_row][mid_col]
        
        if mid_val == target:
            return True
        elif mid_val > target:
            right = mid - 1
        else:
            left = mid + 1
    
    return False
        



if __name__ == '__main__':
    # 测试 isSubsequence
    # print("=== 测试 isSubsequence（双指针）===")
    # test_cases = [
    #     ('abc', 'ahbgdc', True),
    #     ('axc', 'ahbgdc', False),
    #     ('ace', 'abcde', True),
    #     ('aec', 'abcde', False),
    #     ('', 'abc', True),
    #     ('a', '', False),
    #     ('b', 'abc', True),
    # ]
    
    # for s, t, expected in test_cases:
    #     result = isSubsequence(s, t)
    #     status = '✓' if result == expected else '✗'
    #     print(f"{status} s='{s}', t='{t}' => {result} (期望: {expected})")
    
    
    # print("\n=== 测试 IsSubsequenceOptimized（多次查询优化）===")
    # t = "ahbgdc"
    # checker = IsSubsequenceOptimized(t)
    # queries = ['abc', 'axc', 'ace', 'aec', 'b', 'c']
    # for s in queries:
    #     result1 = isSubsequence(s, t)
    #     result2 = checker.check(s)
    #     status = '✓' if result1 == result2 else '✗'
    #     print(f"{status} s='{s}' => 双指针:{result1}, 二分查找:{result2}")

    # 测试 searchMatrix
    print("=== 测试 searchMatrix ===")
    test_cases = [
        ([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3, True),
        ([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 13, False),
        ([[1]], 1, True),
        ([[1]], 2, False),
        ([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 60, True),
        ([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 0, False),
    ]
    
    for matrix, target, expected in test_cases:
        result1 = searchMatrix([row[:] for row in matrix], target)
        result2 = searchMatrixOptimized([row[:] for row in matrix], target)
        status1 = '✓' if result1 == expected else '✗'
        status2 = '✓' if result2 == expected else '✗'
        print(f"{status1} 你的方法: matrix={matrix}, target={target} => {result1} (期望: {expected})")
        print(f"{status2} 优化方法: => {result2} (期望: {expected})")
        print()
    
    print("="*60)
    print("两种方法对比：")
    print("="*60)
    print("""
你的方法（展平后搜索）：
  ✓ 优点：思路清晰，代码易懂，逻辑直观
  ✗ 缺点：时间复杂度 O(m*n)，空间复杂度 O(m*n)
  ✓ 适用：数据量不大时，完全可以使用

优化方法（直接索引映射）：
  ✓ 优点：时间复杂度 O(log(m*n))，空间复杂度 O(1)
  ✗ 缺点：需要计算索引映射，代码稍复杂
  ✓ 适用：数据量很大时，或者对性能要求高时

建议：
  - 如果数据量不大（m*n < 10^4），你的方法完全可以接受
  - 如果数据量很大或对性能要求高，使用优化方法
  - 在面试中，可以先说你的方法，然后提到可以优化
    """)
'''
滑动窗口 

本质：快慢双指针前后跟随，向后移动，维护窗口
用途：子数组问题 -- 找符合条件的最长/最短子数组
用法(3个问题)：
1.何时右移right 扩大窗口？
2.何时右移left 缩小窗口？
3.何时更新（最大/小）结果？
'''

## 滑动窗口 - 模板
from collections import Counter


def sliding_win_template(nums):
    # 左右窗口指针index
    left, right = 0

    res = []
    while (right < len(nums)):
        # 1.右移right - 扩大窗口
        res.append(nums[right])
        right += 1

        need_shrink = True
        # 2.需要右移left 缩小窗口
        while (need_shrink):
            res.pop(left)
            left += 1

    return res



# lc76 minimum window substring HARD
'''
Given two strings s and t of lengths m and n respectively,
return the minimum window substring of s such that 
every character in t (including duplicates) is included in the window. 
If there is no such substring, return the empty string "".

Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"

思路：快慢指针 + 滑动窗口

⚠️ 当前实现的问题：
1. 时间复杂度：O(n² * k)，其中 n=len(s), k=len(t)
   - 每次循环都调用 validStr(s[left:right+1], t)
   - 创建子串 s[left:right+1]：O(窗口大小)
   - Counter(win)：O(窗口大小)
   - Counter(t)：O(k)（虽然可以优化，但每次都创建）
   - 最坏情况：窗口大小可能达到 n，所以是 O(n² * k)

2. 空间复杂度：O(n + k)
   - 每次 validStr 调用需要 O(窗口大小 + k) 的空间

3. 优化建议：
   - 使用哈希表维护窗口状态，而不是每次都重新计算
   - 只在窗口变化时更新状态（添加/删除一个字符）
   - 时间复杂度可以优化到 O(n)
'''
def minWindow(s: str, t: str) -> str:
    res = ''
    left, right = 0, 0
    min_win_size = float('inf')

    map_target = Counter(t)   # a:1 b:1 c:1

    if len(t) > len(s):
        return ''

    while right < len(s):
        
        # ⚠️ 问题：每次都要创建子串并重新计算 Counter
        window = s[left:right+1]

        # 1. window 不包含整个 t -- 右移r扩大
        if not validStr(window, t):
            right += 1
        # 2. window 包含了整个 t -- 左移l缩小
        else: 
            # 更新最小窗口 当找到更小窗口
            if right - left + 1 < min_win_size:
                min_win_size = right - left + 1
                res = window
            left += 1

    print(res)
    return res


# 检查目前窗口包含t中所有char -- Counter！！！
def validStr(win, t):
    """
    ⚠️ 低效方法：每次都要重新计算整个窗口的 Counter
    时间复杂度：O(窗口大小 + len(t))
    """
    c1 = Counter(win)
    c2 = Counter(t)
    return all(c1[ch] >= c2[ch] for ch in c2)




def minWindowFast(s: str, t: str) -> str:
    """
    优化版本：使用哈希表维护窗口状态
    
    时间复杂度：O(n)
    - 外层循环：O(n)
    - 内层 while 循环：每个字符最多被访问两次（进入和离开窗口），所以是 O(n)
    - 总时间复杂度：O(n)
    
    空间复杂度：O(k)，其中 k = len(t)
    - need 字典：O(k)
    - window 字典：O(k)（只存储 t 中的字符）
    
    优化点：
    1. 使用哈希表维护窗口状态，而不是每次都重新计算
    2. 只在窗口变化时更新状态（添加/删除一个字符）
    3. 使用 valid 计数器快速判断窗口是否有效
    """
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


# lc1658 Minimum Operations to Reduce X to Zero
'''
You are given an integer array nums and an integer x. In one operation, 
you can either remove the leftmost or the rightmost element from the array nums and subtract its value from x.
Note that this modifies the array for future operations.

Return the minimum number of operations to reduce x to exactly 0 if it is possible, otherwise, return -1.

思路： 
反窗口 -- 找到中间窗口使得 win_sum == sum(nums) - x
return len(nums) - len(win)

原实现的问题：
1. ❌ 索引越界：当 left >= right 时，尝试访问 nums[left] 会导致 IndexError
2. ❌ 逻辑错误：当 window_sum + nums[right] > target 且 left >= right 时，应该先移动 right，而不是缩小窗口
3. ❌ 边界情况：没有处理 target < 0 和 target == 0 的情况
4. ❌ 窗口更新顺序：应该先更新 window_sum，再移动指针

修复方案：
1. ✅ 使用 for right in range(len(nums)) 避免索引越界
2. ✅ 使用 while left <= right and window_sum > target 确保 left 不会超过 right
3. ✅ 添加边界情况处理：target < 0 返回 -1，target == 0 返回 len(nums)
4. ✅ 简化逻辑：先扩大窗口，再缩小窗口，最后检查是否找到解
'''
def minOperations(nums, x: int) -> int:
    """
    滑动窗口思路：找到中间窗口使得 sum == target，返回 len(nums) - len(window)
    
    时间复杂度：O(n)
    空间复杂度：O(1)
    
    关键点：
    1. target = sum(nums) - x（中间窗口的目标和）
    2. 如果 target < 0，无法达到，返回 -1
    3. 如果 target == 0，说明需要移除所有元素，返回 len(nums)
    4. 使用滑动窗口找到和为 target 的最长连续子数组
    """
    s = sum(nums)
    target = s - x
    
    # 边界情况
    if target < 0:
        return -1
    if target == 0:
        return len(nums)
    
    res = float('inf')
    window_sum = 0
    left = 0
    
    # 滑动窗口：找到和为 target 的最长连续子数组
    for right in range(len(nums)):
        # 扩大窗口：加入 nums[right]
        window_sum += nums[right]
        
        # 缩小窗口：当 window_sum > target 时，从左边移除元素
        while left <= right and window_sum > target:
            window_sum -= nums[left]
            left += 1
        
        # 找到解：window_sum == target
        if window_sum == target:
            # 窗口长度：right - left + 1
            # 需要移除的元素数：len(nums) - (right - left + 1)
            window_len = right - left + 1
            res = min(res, len(nums) - window_len)
    
    return res if res != float('inf') else -1

# 713 Subarray Product Less Than K
'''
Given an array of integers nums and an integer k,
return the number of contiguous subarrays where the 
product of all the elements in the subarray is strictly less than k.
constraints
1 <= nums.length <= 3 * 104
1 <= nums[i] <= 1000
0 <= k <= 106
'''
# def numSubarrayProductLessThanK(nums, k: int) -> int: # 边界错误！！！！！
#     sub_arr_prod = []
#     left = 0
#     prod = 1

#     # left 闭合 right 开放
#     for right, n in enumerate(nums):
#         prod *= n
#         # 扩大窗口 右移right 
#         if prod < k:
#             sub_arr_prod.append(prod)

#         # 缩小窗口 右移left
#         while left < right:

#             prod /= nums[left]
#             if prod < k:
#                 sub_arr_prod.append(prod)
#             left += 1
#     return len(sub_arr_prod)

def numSubarrayProductLessThanK(nums, k: int) -> int:
    """
    为什么可以用 right - left + 1 计算？
    
    ════════════════════════════════════════════════════════════
    核心理解：固定右端点，枚举所有左端点
    ════════════════════════════════════════════════════════════
    
    当窗口 [left, right] 的乘积 < k 时，
    以 right 为右端点的所有满足条件的子数组是：
    
    索引：  left    left+1  left+2  ...  right-1  right
    数组：  [  ?  ,   ?   ,   ?   , ... ,   ?   ,  ?  ]
            └─────────────────────────────────────┘
                    窗口 [left, right]
    
    以 right 为右端点的子数组（从不同位置开始）：
    1. [left, right]      ← 从 left 开始
    2. [left+1, right]    ← 从 left+1 开始
    3. [left+2, right]    ← 从 left+2 开始
    4. ...
    5. [right, right]     ← 从 right 开始（单个元素）
    
    这些子数组的数量 = right - left + 1
    
    ════════════════════════════════════════════════════════════
    为什么这些子数组都满足条件？
    ════════════════════════════════════════════════════════════
    
    因为窗口 [left, right] 的乘积 < k，而所有子数组都是它的子集，
    所以它们的乘积也一定 < k（因为所有元素都是正整数，子集的乘积更小）
    
    ════════════════════════════════════════════════════════════
    具体示例：nums=[10,5,2,6], k=100
    ════════════════════════════════════════════════════════════
    
    right=0, left=0:
      窗口：[10], 乘积=10 < 100
      以0为右端点的子数组：[10] (1个)
      计算：0-0+1 = 1 ✓
    
    right=1, left=0:
      窗口：[10,5], 乘积=50 < 100
      以1为右端点的子数组：[10,5], [5] (2个)
      计算：1-0+1 = 2 ✓
    
    right=2, left=1:
      窗口：[5,2], 乘积=10 < 100 (因为 [10,5,2] 乘积=100 >= 100，所以缩小窗口)
      以2为右端点的子数组：[5,2], [2] (2个)
      计算：2-1+1 = 2 ✓
    
    right=3, left=1:
      窗口：[5,2,6], 乘积=60 < 100
      以3为右端点的子数组：[5,2,6], [2,6], [6] (3个)
      计算：3-1+1 = 3 ✓
    
    总计：1+2+2+3 = 8
    """
    res = 0
    left = 0
    prod = 1
    for right in range(len(nums)):
        prod *= nums[right]  # 扩大窗口
        
        # 只在 prod >= k 时缩小窗口
        while left <= right and prod >= k:
            prod //= nums[left]  # 使用整数除法
            left += 1
        
        # 以 right 为右端点的满足条件的子数组数量
        # 这些子数组是：nums[left...right], nums[left+1...right], ..., nums[right...right]
        # 共 right - left + 1 个
        res += right - left + 1

    return res

if __name__ == '__main__':
    # 测试用例
    test_cases = [
        ('ADOBECODEBANC', 'ABC', 'BANC'),
        ('a', 'a', 'a'),
        ('a', 'aa', ''),
        ('AAA', 'AAA', 'AAA'),
    ]
    
    # print("=== 测试 minWindow ===")
    # for s, t, expected in test_cases:
    #     result = minWindow(s, t)
    #     print(f"s='{s}', t='{t}'")
    #     print(f"  期望: '{expected}', 实际: '{result}', 正确: {result == expected}\n")
    
    # # 性能测试
    # import time
    # print("=== 性能对比 ===")
    # s_large = 'A' * 1000 + 'B' * 1000 + 'C' * 1000 + 'ADOBECODEBANC'
    # t_large = 'ABC'
    
    # # 测试 minWindow
    # start = time.time()
    # result1 = minWindow(s_large, t_large)
    # time1 = time.time() - start
    # print(f"minWindow:     结果='{result1}', 耗时={time1:.4f}秒")
    
    # # 测试 minWindowFast
    # start = time.time()
    # result2 = minWindowFast(s_large, t_large)
    # time2 = time.time() - start
    # print(f"minWindowFast: 结果='{result2}', 耗时={time2:.4f}秒")
    # print(f"性能提升: {time1/time2:.2f}x")

    # 测试 minOperations
    print("=== 测试 minOperations ===")
    test_cases = [
        ([1,1,4,2,3], 5, 2),      # 移除 [1,1,4] = 6，剩余 [2,3] = 5
        ([3,2,20,1,1,3], 10, 5),  # 移除 [3,2,20,1,1,3] = 30，剩余 [] = 0
        ([5,6,7,8,9], 4, -1),     # 无法达到
        ([1,1], 3, -1),           # 无法达到
        ([1,1,1,1,1], 3, 3),      # 移除两端
    ]
    
    # for nums, x, expected in test_cases:
    #     result = minOperations(nums.copy(), x)
    #     print(f"nums={nums}, x={x}")
    #     print(f"  期望: {expected}, 实际: {result}, 正确: {result == expected}\n")


    # 测试并可视化 numSubarrayProductLessThanK
    print("=== 可视化 numSubarrayProductLessThanK ===")
    nums = [10, 5, 2, 6]
    k = 100
    
    print(f"nums = {nums}, k = {k}")
    print("⚠️ 关键：题目要求的是'连续子数组'（contiguous subarray），不是'子序列'（subsequence）")
    print("   连续子数组必须是原数组中连续的元素，不能跳过任何元素！\n")
    
    # 手动计算每个 right 的情况
    left = 0
    prod = 1
    
    for right in range(len(nums)):
        prod *= nums[right]
        
        # 缩小窗口
        while left <= right and prod >= k:
            prod //= nums[left]
            left += 1
        
        # 计算以 right 为右端点的所有子数组
        print(f"right={right}, left={left}, 窗口={nums[left:right+1]}, 乘积={prod}")
        print(f"  以 {right} 为右端点的连续子数组：")
        
        count = 0
        for start in range(left, right + 1):
            subarray = nums[start:right+1]
            sub_prod = 1
            for num in subarray:
                sub_prod *= num
            print(f"    {subarray} (乘积={sub_prod})")
            count += 1
        
        # 特别说明为什么 [5,6] 不包含
        if right == 3 and left == 1:
            print(f"\n  ❓ 为什么 [5,6] 不包含？")
            print(f"     原数组：{nums}")
            print(f"     索引：  0    1    2    3")
            print(f"     要取 [5,6]，需要索引 1 和 3，但跳过了索引 2 的元素 2")
            print(f"     这不是连续子数组！连续子数组必须是原数组中连续的元素。")
            print(f"     如果要取 [5,6]，必须跳过中间的 2，这就不是连续的了。")
            print(f"     所以 [5,6] 不是连续子数组，而是子序列（subsequence）。")
        
        calculated = right - left + 1
        print(f"\n  计算值：right - left + 1 = {right} - {left} + 1 = {calculated}")
        print(f"  实际数量：{count}")
        print(f"  {'✓ 正确' if calculated == count else '✗ 错误'}\n")
    
    result = numSubarrayProductLessThanK(nums, k)
    print(f"最终结果：{result}")
    
    # 额外说明：连续子数组 vs 子序列
    print("\n" + "="*60)
    print("连续子数组（Contiguous Subarray）vs 子序列（Subsequence）")
    print("="*60)
    print(f"原数组：{nums}")
    print(f"索引：  {list(range(len(nums)))}")
    print()
    print("连续子数组（必须连续，不能跳过元素）：")
    print("  [10], [5], [2], [6]")
    print("  [10,5], [5,2], [2,6]")
    print("  [10,5,2], [5,2,6]")
    print("  [10,5,2,6]")
    print()
    print("子序列（可以跳过元素，不要求连续）：")
    print("  [10,2], [10,6], [5,6], [10,2,6] 等")
    print("  注意：[5,6] 是子序列，但不是连续子数组！")
    print("  因为要取 [5,6]，必须跳过中间的 2，所以不是连续的。")
    
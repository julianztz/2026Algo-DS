# -*- coding: utf-8 -*-
'''
递归两种思路

1. 遍历一遍树（回溯）-- backtrack, 关注节点间移动
2. 分解问题（DP分治）-- DP思路，关注整颗子树 left+1 / right+1
        递归函数一定有return；结果需要返还给上层计算
'''


# eg1 fib()   f(n) = f(n-1) + f(n-2)
# 分解问题思路 top-down （二叉树后序遍历相同）
# ⚠️ 时间复杂度：O(2^n) - 指数级！
# ⚠️ 空间复杂度：O(n) - 递归调用栈深度
# 
# 为什么慢？因为存在大量重复计算！
# 例如：计算 fib(5) 时：
#   - fib(5) 需要 fib(4) + fib(3)
#   - fib(4) 需要 fib(3) + fib(2)
#   - fib(3) 需要 fib(2) + fib(1)
#   可以看到 fib(3) 被计算了多次，fib(2) 被计算了更多次
# 
# 递归树展开：
#                    fib(5)
#                   /      \
#              fib(4)      fib(3)
#             /     \      /     \
#        fib(3)  fib(2) fib(2) fib(1)
#        /   \
#   fib(2) fib(1)
# 
# 每个节点都会分裂成两个子节点，总节点数约为 2^n
from typing import List


def fib_dp(n):
    if n == 1 or n == 2:
        return 1

    left1 = fib_dp(n-1)      
    left2 = fib_dp(n-2)
    return left1 + left2

# 优化版本1
'''
#  ！！！动态规划 (top-down)！！！ 带记忆化的递归（Memoization）
# ✅ 时间复杂度：O(n) - 每个子问题只计算一次
# ✅ 空间复杂度：O(n) - 存储结果 + 递归栈
'''
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 1 or n == 2:
        return 1
    
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# 优化版本2
'''
#  ！！！动态规划 (btm-up)！！！）普通遍历算法 
# ✅ 时间复杂度：O(n) - 线性时间
# ✅ 空间复杂度：O(n) - 存储结果数组（可优化到O(1)）
# 
# 为什么快？每个值只计算一次，没有重复计算 
# 从 fib(1), fib(2) 开始，逐步计算到 fib(n)
'''
def fib_iter(n):
    res = [1,1]
    for i in range(2, n+1):
        res.append(res[i-1]+res[i-2])
    print(res)



# review !! lc322 coin change 
'''
way1 递归 从上到下

思路： 
0.子问题/递归公式：凑n需要最少硬币
1.暴力求解 -- 记录所有amt的最少coin需求
2.剪枝 -- memo 记录算过的 {amt：min_coin}

状态转移方程：
f(amt):
f(0) return 0    # valid 解    
f(<0) return -1  # invalid 解
f(>0) --> f(amount-x)

''' 
def coinChange(coins: List[int], amount: int) -> int:
    memo = {}                # 记录过程 amt: coin个数

    # return 凑齐amt 需要最少的coin# 
    def dp(coins, amt) -> int:
        min_coin = float('inf')
        # base case
        if amt < 0:          # invalid
            return -1
        elif amt == 0:       # valid
            return 0

        # 备忘录剪枝 -- return已经算过的amt
        if amt in memo:
            return memo[amt]

        # 递归公式
        for c in coins:
            subProblem = dp(coins, amt-c)
            if subProblem == -1:         # 最底层 invalid 解 -- skip
                continue
            min_coin = min(min_coin, subProblem+1)   # valid解，coin#+1
        
        # 加入memo
        memo[amt] = min_coin

        if min_coin != float('inf'):
            return min_coin
        return -1

    return dp(coins, amount)

'''
way2 迭代 bottom-up

思路： 
1.暴力枚举：凑出所有amt的所有可能
dp 数组的定义：当目标金额为 i 时，至少需要 dp[i] 枚硬币凑出。
'''
# review ！！！！！
def coinChangeIterative(coins: List[int], amount:int) -> int:

    # 数组大小为 amount + 1，初始值也为 amount + 1
    dp = [amount + 1] * (amount + 1)

    dp[0] = 0
    # base case
    # 外层 for 循环在遍历所有状态的所有取值
    for i in range(len(dp)):
        # 内层 for 循环在求所有选择的最小值
        for coin in coins:
            # 子问题无解，跳过
            if i - coin < 0:
                continue
            dp[i] = min(dp[i], 1 + dp[i - coin]) 

    return -1 if dp[amount] == amount + 1 else dp[amount]



# 23. Merge k Sorted Lists
'''
You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]

思路：分治 merge (merge(1,2), merge(3,4))  binarySearch + merge2SortedLists


子问题 -- merge two sorted lists 双指针
'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 子问题 -- merge two lists
def mergeTwoList(l1, l2) -> ListNode:
    pers = l1
    poes = l2
    head = ListNode(0)
    p = head

    while pers and poes:
        if pers.val < poes.val:
            p.next = pers
            pers = pers.next
        else:
            p.next = poes
            poes = poes.next
        p = p.next

    # connect the rest
    if pers:
        p.next = pers
    if poes:
        p.next = poes
    return head.next


def mergeKLists(lists: List[ListNode]) -> ListNode:
    if len(lists) == 0:
        return None
    
    def merge(sorted_list, left, right):
        # base case
        if left == right:
            return sorted_list[left]

        mid = (left + right) // 2
        
        # 递归分解：左右分别合并，注意用不同变量名避免覆盖参数
        left_list = merge(sorted_list, left, mid)
        right_list = merge(sorted_list, mid+1, right)
        
        # 合并两个已排序的链表
        return mergeTwoList(left_list, right_list)
    
    return merge(lists, 0, len(lists)-1)

# $$$ review
def mergeKListsGreedy(lists: List[ListNode]) -> ListNode:
    if not lists:
        return None

    dummy = ListNode(0)
    p = dummy

    while True:    # 遍历所有node

        min_val = float('inf')
        min_idx = -1           # min所在的linkedlist
        p_min = None

        for i in range(len(lists)):
            if lists[i] and lists[i].val < min_val:
                min_val = lists[i].val
                min_idx = i
                p_min = lists[i]

        if min_idx == -1:
            break
        # 更新结果链表
        p.next = p_min
        p = p.next

        lists[min_idx] = lists[min_idx].next

    return dummy.next


'''
================================================================================
mergeKLists 两种实现方法对比
================================================================================

【方法1：分治（Divide & Conquer） - mergeKLists】

核心思路：
- 递归地将k个链表分成两部分，分别合并，最后合并两个结果
- 类似归并排序的merge过程

实现步骤：
1. Base case: 如果left == right，返回单个链表
2. 分解：找到中点mid，分别递归合并[left, mid]和[mid+1, right]
3. 合并：用mergeTwoList合并两个已排序的链表

时间复杂度：O(n log k)
- n: 所有链表的总节点数
- k: 链表数量
- 分析：合并过程O(n)，递归深度O(log k)，所以总时间O(n log k)

空间复杂度：O(log k)
- 递归调用栈的深度为O(log k)

优点：
✅ 时间复杂度最优（O(n log k)）
✅ 递归思路清晰，易于理解
✅ 适合链表数量较多的情况

缺点：
❌ 有递归栈开销
❌ 代码相对复杂


【方法2：暴力/贪心（Brute Force/Greedy） - mergeKLists2】

核心思路：
- 每次遍历所有链表的头节点，找到最小值，加入到结果链表
- 重复这个过程直到所有链表都为空

实现步骤：
1. 创建dummy节点作为结果链表的头
2. 循环直到所有链表都为空：
   a. 遍历所有链表的当前头节点
   b. 找到值最小的节点
   c. 将该节点加入结果链表
   d. 移动对应链表的指针
3. 返回dummy.next

时间复杂度：O(nk)
- n: 所有链表的总节点数
- k: 链表数量
- 分析：需要处理n个节点，每个节点需要比较k次（遍历所有链表头）

空间复杂度：O(1)
- 只使用了常数额外空间（dummy节点等）

优点：
✅ 空间复杂度最优（O(1)）
✅ 代码简单直观
✅ 无递归开销

缺点：
❌ 时间复杂度较高（O(nk)）
❌ 当k很大时效率低

【方法对比表】

| 特性 | 方法1：分治 | 方法2：暴力 |
|------|------------|------------|
| 时间复杂度 | O(n log k) ✅ | O(nk) ❌ |
| 空间复杂度 | O(log k) | O(1) ✅ |
| 代码复杂度 | 中等 | 简单 ✅ |
| k小时 | 较好 | 很好 ✅ |
| k大时 | 很好 ✅ | 较差 |
| 递归开销 | 有 | 无 ✅ |

【选择建议】

1. k较小（k < 10）：使用方法2，代码简单，实际性能差异不大
2. k较大（k >= 10）：使用方法1，时间复杂度优势明显
3. 空间受限：使用方法2，O(1)空间
4. 时间受限：使用方法1，O(n log k)时间

【优化方向】

方法2可以优化为O(n log k)：
- 使用优先队列（堆）存储所有链表的头节点
- 每次取出最小值，时间复杂度降为O(log k)
- 总体时间复杂度：O(n log k)
- 空间复杂度：O(k)

示例（使用heapq）：
```python
import heapq

def mergeKLists3(lists):
    heap = []
    for i, l in enumerate(lists):
        if l:
            heapq.heappush(heap, (l.val, i, l))
    
    dummy = ListNode(0)
    p = dummy
    
    while heap:
        val, idx, node = heapq.heappop(heap)
        p.next = node
        p = p.next
        if node.next:
            heapq.heappush(heap, (node.next.val, idx, node.next))
    
    return dummy.next
```

================================================================================
'''



'''
mergeSort 分治思想: 本质--b tree后序遍历

base case: split成单个元素list
子问题：左右半边分别sort；相互独立，不重叠
    递归公式：左不包[:mid]  右包[mid:] 

'''
# 区分左右两边
def mergeSort(nums) -> List:
    # base： 分到底
    if len(nums) <= 1:
        return nums

    mid = len(nums) // 2              # 更新中点给下一层

    # 递归公式：左右split + merge(排序)
    left = mergeSort(nums[:mid])            
    right = mergeSort(nums[mid:])     # 中间点归右边
    return merge(left, right)



# 后序位置：merging two (sorted) lists
def merge(left, right) -> List:
    l = 0
    r = 0
    res = []

    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            res.append(left[l])
            l += 1
        else:
            res.append(right[r])
            r += 1

    res.extend(right[r:])   # 原地修改列表; 
    # res += res[r:]        # 会创建新列表 more space needed
    res.extend(left[l:])

    print(res)
    return res


if __name__ == '__main__':

    
    print("fib简单测试:")
    # print(f"fib_dp(10) = {fib_dp(10)}")
    # print(f"fib_memo(10) = {fib_memo(10)}")
    fib_iter(40)
    print("\n")

    coins = [1,2,5]
    print(coinChange(coins, 11))




'''
================================================================================
动态规划（Top-Down记忆化递归）标准模板
================================================================================

【200字核心思路总结】
DP核心：将问题分解为重叠子问题，通过记忆化避免重复计算。
解题四步：
1)定义状态和递归函数(input和return)，明确子问题是什么；
2)确定base case，处理边界和最小子问题；
3)写出递归公式，遍历所有可能的子问题选择，用min/max/sum等更新结果；
4)用memo存储已计算状态，递归前先查memo剪枝。

剪枝三处：memo剪枝在递归公式前(必须)，
遍历前剪枝跳过无效选择(可选)，
遍历中剪枝过滤无效子问题解(常用)。
核心不变：base case → memo查表 → 递归分解 → 更新结果 → 存入memo。

【你的总结 ✅ 基本正确！】

标准流程：
1. 找到子问题求解，需要构造函数（必须找到input和return分别是什么）
2. base case：迭代到最底层的处理
3. 递归公式：多叉树遍历所有子node，更新最终需要的最值
4. 本层处理完得到最值加入memo

【标准模板代码框架】

def dp_problem(params):
    memo = {}  # 或 memo = defaultdict(lambda: None)
    
    def dp(state):
        # ========== 第1步：Base Case ==========
        # 终止条件：最小子问题的解
        if 到达最小子问题:
            return 基础解  # 如：0, 1, True, False等
        
        if 无效状态:
            return 无效标记  # 如：-1, float('inf'), None等
        
        # ========== 第2步：Memo剪枝（遍历子节点之前）==========
        # 位置：在base case之后，递归公式之前
        # 作用：避免重复计算已解决的子问题
        if state in memo:
            return memo[state]
        
        # ========== 第3步：初始化结果变量 ==========
        result = 初始值  # 如：0, float('inf'), float('-inf')等
        
        # ========== 第4步：递归公式（遍历所有子节点）==========
        for choice in choices:  # 或 for subproblem in subproblems
            # ========== 剪枝位置A：遍历前剪枝（可选）==========
            # 提前跳过明显无效的选择
            if 明显无效的选择:
                continue
            
            # ========== 递归调用子问题 ==========
            sub_result = dp(新的state)
            
            # ========== 剪枝位置B：遍历中剪枝（过滤无效子问题解）==========
            # 过滤掉无效的子问题解（如coinChange中的-1）
            if sub_result == 无效标记:
                continue
            
            # ========== 更新结果（根据问题类型）==========
            # 最值问题：取min/max
            result = min/max(result, sub_result + cost)
            # 计数问题：累加
            result += sub_result
            # 布尔问题：或/与操作
            result = result or/and sub_result
        
        # ========== 第5步：处理所有子问题都无效的情况 ==========
        if result == 初始值且没有有效解:
            memo[state] = 无效标记
            return 无效标记
        
        # ========== 第6步：加入memo并返回 ==========
        memo[state] = result
        return result
    
    return dp(初始状态)

【剪枝的三种位置和时机】

1. Memo剪枝（必须，位置：递归公式之前）
   - 时机：检查当前状态是否已计算过
   - 位置：base case之后，递归公式之前
   - 作用：避免重复计算，这是DP的核心优化
   - 示例：if amt in memo: return memo[amt]

2. 遍历前剪枝（可选，位置：进入递归前）
   - 时机：在选择循环中，调用递归前
   - 位置：for循环内部，dp()调用前
   - 作用：提前跳过明显无效的选择，减少递归调用
   - 示例：
     if i - coin < 0:  # 索引越界
         continue
     if grid[i][j] == 障碍物:  # 不可达
         continue

3. 遍历中剪枝（可选，位置：得到子问题结果后）
   - 时机：递归返回后，使用结果前
   - 位置：for循环内部，dp()调用后
   - 作用：过滤无效的子问题解，不参与最终计算
   - 示例：
     sub_result = dp(new_state)
     if sub_result == -1:  # 无效解
         continue
     result = min(result, sub_result + 1)

【适用性问题】

✅ 这个模板适用于大多数DP问题，但需要注意：

1. 基础计数/最值问题（如fib, coinChange, climbStairs）
   - ✅ 完全适用
   - 标准流程：base case → memo → 遍历子问题 → 更新结果 → memo

2. 二维DP问题（如uniquePaths, minPathSum）
   - ✅ 适用，但state是二维的 (i, j)
   - memo用元组：memo[(i, j)] = result

3. 背包问题（如0-1背包，完全背包）
   - ✅ 适用
   - state通常包含：剩余容量 + 可选物品索引
   - 剪枝：容量不足时跳过

4. 字符串DP问题（如editDistance, longestCommonSubsequence）
   - ✅ 适用
   - state通常是两个字符串的索引位置
   - 剪枝：索引越界时返回基础解

5. 区间DP问题（如matrixChainMultiplication, palindromePartitioning）
   - ⚠️ 部分适用，但可能需要调整
   - state通常是区间 (start, end)
   - 递归公式可能需要三层循环

6. 树形DP问题（如houseRobberIII, binaryTreeMaximumPathSum）
   - ⚠️ 需要调整
   - state通常是节点
   - 递归公式需要遍历子树

【关键点总结】

1. ✅ Memo剪枝必须在递归公式之前（这是DP优化的核心）
2. ✅ 遍历前剪枝可以减少不必要的递归调用
3. ✅ 遍历中剪枝可以过滤无效解，保证结果正确性
4. ✅ 大多数DP问题遵循这个模板，细节根据问题调整
5. ⚠️ 某些复杂问题（如区间DP、树形DP）需要根据特点调整

【模板vs实际应用】

- 基础DP问题：90%+符合模板
- 中等DP问题：70-80%符合模板，需要调整细节
- 困难DP问题：50-60%符合模板，需要更多变通

但核心思想不变：base case → memo剪枝 → 递归公式 → 更新结果 → 存入memo

================================================================================
'''

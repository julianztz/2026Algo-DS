"""
贪心算法解题模板集合
包含4种常见模板的实际应用
"""
from typing import List
import heapq

# ============================================================================
# 模板1：区间/范围类问题
# ============================================================================

def activitySelection(activities: List[tuple]) -> List[tuple]:
    """
    活动选择问题：选择最多的不冲突活动
    模板：排序 + 贪心选择
    """
    # 1. 按结束时间排序
    activities.sort(key=lambda x: x[1])
    
    # 2. 贪心选择
    selected = [activities[0]]
    last_end = activities[0][1]
    
    for start, end in activities[1:]:
        if start >= last_end:  # 不冲突
            selected.append((start, end))
            last_end = end
    
    return selected


def eraseOverlapIntervals(intervals: List[List[int]]) -> int:
    """
    LC435: 无重叠区间
    模板：排序 + 贪心选择（保留结束时间最早的）
    """
    if not intervals:
        return 0
    
    # 按结束时间排序
    intervals.sort(key=lambda x: x[1])
    
    count = 0
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:  # 重叠
            count += 1
        else:
            end = intervals[i][1]
    
    return count


# ============================================================================
# 模板2：最值选择类问题（堆/优先队列）
# ============================================================================

# 注意：mergeKLists需要ListNode类，这里仅展示思路
# def mergeKLists(lists: List) -> List:
#     """
#     合并K个有序链表
#     模板：堆 + 贪心选择最小/最大值
#     """
#     heap = []
#     
#     # 初始化：每个链表的第一个节点
#     for i, node in enumerate(lists):
#         if node:
#             heapq.heappush(heap, (node.val, i, node))
#     
#     dummy = ListNode(0)
#     current = dummy
#     
#     while heap:
#         val, idx, node = heapq.heappop(heap)
#         current.next = node
#         current = current.next
#         
#         # 添加下一个节点
#         if node.next:
#             heapq.heappush(heap, (node.next.val, idx, node.next))
#     
#     return dummy.next


def findKthLargest(nums: List[int], k: int) -> int:
    """
    LC215: 数组中的第K个最大元素
    模板：堆 + 贪心选择
    """
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # 保持堆大小为k
    
    return heap[0]


# ============================================================================
# 模板3：累积/更新类问题
# ============================================================================

def jump(nums: List[int]) -> int:
    """
    LC45: 跳跃游戏II - 最少跳跃次数
    模板：累积更新 + 边界判断
    """
    if len(nums) <= 1:
        return 0
    
    jumps = 0
    farthest = 0  # 当前能到达的最远位置
    end = 0  # 上一次跳跃的边界
    
    for i in range(len(nums) - 1):
        # 更新能到达的最远位置
        farthest = max(farthest, i + nums[i])
        
        # 到达边界，需要跳跃
        if i == end:
            jumps += 1
            end = farthest
            
            # 提前终止
            if farthest >= len(nums) - 1:
                break
    
    return jumps


def canCompleteCircuit(gas: List[int], cost: List[int]) -> int:
    """
    LC134: 加油站
    模板：累积更新 + 贪心选择起始点
    """
    total_gas = 0
    current_gas = 0
    start = 0
    
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total_gas += diff
        current_gas += diff
        
        # 如果当前累积油量不够，从下一个位置重新开始
        if current_gas < 0:
            start = i + 1
            current_gas = 0
    
    return start if total_gas >= 0 else -1


def maxProfit(prices: List[int]) -> int:
    """
    LC121: 买卖股票的最佳时机
    模板：累积更新 + 维护最值
    """
    if not prices:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices[1:]:
        # 更新最低价格
        min_price = min(min_price, price)
        # 更新最大利润
        max_profit = max(max_profit, price - min_price)
    
    return max_profit


# ============================================================================
# 模板4：排序+选择类问题
# ============================================================================

def findContentChildren(g: List[int], s: List[int]) -> int:
    """
    LC455: 分发饼干
    模板：排序 + 贪心匹配
    """
    g.sort()  # 孩子胃口
    s.sort()  # 饼干大小
    
    i = j = 0
    count = 0
    
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:  # 能满足
            count += 1
            i += 1
        j += 1
    
    return count


def largestNumber(nums: List[int]) -> str:
    """
    LC179: 最大数
    模板：自定义排序 + 贪心选择
    """
    from functools import cmp_to_key
    
    # 自定义排序：比较两个数字拼接后的大小
    def compare(x, y):
        s1 = str(x) + str(y)
        s2 = str(y) + str(x)
        return -1 if s1 > s2 else 1
    
    nums.sort(key=cmp_to_key(compare))
    result = ''.join(map(str, nums))
    return result if result[0] != '0' else '0'


# ============================================================================
# 对比：Greedy vs DP
# ============================================================================

def coinChange_greedy(coins: List[int], amount: int) -> int:
    """
    ❌ 错误示例：Coin Change不能用Greedy
    反例：[1, 3, 4], amount = 6
    Greedy: 4+1+1 = 3个硬币 ❌
    正确: 3+3 = 2个硬币 ✅
    """
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1


def coinChange_dp(coins: List[int], amount: int) -> int:
    """
    ✅ 正确示例：Coin Change用DP
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


# ============================================================================
# 测试
# ============================================================================

if __name__ == '__main__':
    # 测试1：活动选择
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]
    print("活动选择:", activitySelection(activities))
    
    # 测试2：跳跃游戏
    nums = [2, 3, 1, 1, 4]
    print("最少跳跃次数:", jump(nums))
    
    # 测试3：分发饼干
    g = [1, 2, 3]
    s = [1, 1]
    print("能满足的孩子数:", findContentChildren(g, s))
    
    # 测试4：Coin Change对比
    coins = [1, 3, 4]
    amount = 6
    print(f"\nCoin Change (amount={amount}, coins={coins}):")
    print(f"  Greedy (错误): {coinChange_greedy(coins, amount)} 个硬币")
    print(f"  DP (正确): {coinChange_dp(coins, amount)} 个硬币")


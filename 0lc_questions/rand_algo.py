import random
from typing import List, Optional
from collections import Counter

# 384 shuffle an array
'''
Given an integer array nums, design an algorithm to randomly shuffle the array. 
All permutations of the array should be equally likely as a result of the shuffling.
随机打乱数组

思路：Fisher-Yates 洗牌算法
- [i] 与 [i] 之后的随机位置交换
- 确保每个排列的概率相等

你的实现分析：
1. ✅ 算法思路正确：Fisher-Yates 洗牌算法
2. ✅ 循环范围正确：range(len(self.nums)-1)
3. ❌ 随机范围错误：原实现是 random.randint(i+1, len(self.nums)-1)
   - 问题：如果只从 [i+1, n-1] 选择，位置 i 的元素永远不会留在原位置
   - 这会导致某些排列永远不会出现，不符合"所有排列等概率"的要求
   - 修正：应该是 random.randint(i, len(self.nums)-1)，包括 i 本身
4. ✅ reset 方法：需要重新复制 original，避免修改原始数组
'''
class ArrayShuffle:
    def __init__(self, nums: List[int]):
        self.nums = nums
        self.original = nums.copy()  # 保存原始数组

    def reset(self) -> List[int]:
        """重置为原始数组"""
        self.nums = self.original.copy()  # ⚠️ 注意：需要重新复制，否则会修改 original
        return self.nums

    def shuffle(self) -> List[int]:
        """
        Fisher-Yates 洗牌算法
        
        时间复杂度：O(n)
        空间复杂度：O(1)
        
        算法正确性：
        - 对于位置 i，从 [i, n-1] 中随机选择一个位置交换（包括 i 本身）
        - 每个元素出现在每个位置的概率都是 1/n
        - 每个排列的概率都是 1/n!
        
        ⚠️ 关键：随机范围必须是 [i, n-1]，不是 [i+1, n-1]
        - 如果只从 [i+1, n-1] 选择，位置 i 的元素永远不会留在原位置
        - 这会导致某些排列永远不会出现，不符合"所有排列等概率"的要求
        """
        for i in range(len(self.nums) - 1):
            # ⚠️ 修正：从 [i, len(self.nums)-1] 中随机选择，包括 i 本身
            r = random.randint(i, len(self.nums) - 1)
            self.nums[i], self.nums[r] = self.nums[r], self.nums[i]
        
        return self.nums 



# 382 linked list random node
'''
Given a singly linked list, return a random node's value from the linked list.
Each node must have the same probability of being chosen.

follow-up
What if the linked list is extremely large and its length is unknown to you?
Could you solve this efficiently without using extra space?

思路： 
wrong❌❌❌ 不停读linkedlist （首尾相接），randomly stop
correct✅ 
动态变化概率，第i个node的概率应该是 1/i
当你遇到第 i 个元素时，应该有 1/i 的概率选择该元素，1 - 1/i 的概率保持原有的选择
'''

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Linkedlist_shuffle:

    def __init__(self, head: Optional[ListNode]):
        self.head = head

    def getRandom(self) -> int:
        """
        Reservoir Sampling（蓄水池抽样）算法
        
        时间复杂度：O(n)，其中 n 是链表长度
        空间复杂度：O(1)
        
        算法正确性：
        - 对于第 i 个节点，以 1/i 的概率选择它
        - 每个节点最终被选中的概率都是 1/n（n 是链表长度）
        
        数学证明：每个元素备选概率相同
        第i个元素被选择 且 后面元素没有被选择
          1/i * [1-1/(i+1)] * [1-1/(i+2)] * ... * [1 - 1/n]
        = 1/i * [i/(i+1)] * [i+1/(i+1)] * ... * (n-1)/n
        = 1/n
        """
        res = 0

        i = 0    # 当前node是第几个
        p = self.head    # 当前位置pointer

        while p != None:
            i += 1
            # 生成 [0, i-1] 之间的整数（包括两端）
            rand_num = random.randint(0, i-1)
            # 如果 rand_num == 0，选择当前节点，概率是 1/i
            if rand_num == 0:
                res = p.val
            p = p.next

        return res


# 528 random pick with weight
'''
求前缀和 -- 累计区间进行random
二分法找左区间
'''
class RandomPickWithWeight:

    def __init__(self, w: List[int]):
        # self.w = w
        self.preSum = [w[0]]
        for i in range(1, len(w)):
            self.preSum.append(self.preSum[i-1] + w[i])


    def pickIndex(self) -> int:
        target = random.randint(1, self.preSum[-1])

        # res = -1
        # 找target所在的preSum中的leftBound所对应的原位置 -- binarySearch
        left = 0
        right = len(self.preSum) - 1
        while left < right:                 # 注意边界
            mid = (left + right) // 2
            if target == self.preSum[mid]:
                right = mid
            elif target < self.preSum[mid]:
                right = mid
            elif target > self.preSum[mid]:
                left = mid + 1
        
        return left
            
        




if __name__ == '__main__':
    # 测试 RandomPickWithWeight
    print("=== 测试 RandomPickWithWeight ===")
    
    # 测试用例1：w = [1, 3]
    print("\n测试用例1: w = [1, 3]")
    w1 = [1, 3]
    picker1 = RandomPickWithWeight(w1)
    print(f"  权重数组: {w1}")
    print(f"  前缀和（你的计算）: {picker1.preSum}")
    print(f"  正确的前缀和应该是: [1, 4]")
    print(f"  ⚠️ 问题：如果 w = [1, 2, 3]，你的前缀和计算会出错")
    
    # 测试用例2：w = [1, 2, 3] - 这个会暴露前缀和计算错误
    print("\n测试用例2: w = [1, 2, 3]")
    w2 = [1, 2, 3]
    picker2 = RandomPickWithWeight(w2)
    print(f"  权重数组: {w2}")
    print(f"  前缀和（你的计算）: {picker2.preSum}")
    print(f"  正确的前缀和应该是: [1, 3, 6]")
    if picker2.preSum != [1, 3, 6]:
        print(f"  ❌ 前缀和计算错误！")
        print(f"     你的: {picker2.preSum}")
        print(f"     正确: [1, 3, 6]")
    
    # 测试 pickIndex 的逻辑问题
    print("\n测试 pickIndex 逻辑:")
    print("  问题1: res = -1 初始化，如果 target 不等于任何 preSum[mid]，res 仍然是 -1")
    print("  问题2: left = mid 可能导致死循环（如果 left == mid 且 target > preSum[mid]）")
    print("  问题3: return res - 1 返回值错误")
    
    # 尝试运行几次看看
    print("\n尝试运行 pickIndex（可能出错）:")
    try:
        for _ in range(5):
            idx = picker1.pickIndex()
            print(f"  返回索引: {idx}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

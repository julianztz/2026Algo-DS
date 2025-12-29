from collections import Counter
import heapq
from typing import List

# lc 347. Top K Frequent Elements
'''
正确思路：
1. 用Counter统计频率 ✅
2. 把(频率, 元素)放入heap，用频率作为优先级 ✅
3. 维护大小为k的堆，始终保持前k个频率最大的元素 ✅
4. 不需要最后sort，heap已经按优先级排序 ✅

关键：用频率作为堆的优先级，而不是把元素本身放入堆
时间复杂度：O(n log k)，比O(n log n)更好
'''

def topKFrequent(nums: List[int], k: int) -> List[int]:
    """方法1：维护大小为k的最小堆（推荐）"""
    counter = Counter(nums)
    heap = []
    
    # 把(频率, 元素)放入堆，频率作为优先级
    for num, freq in counter.items():
        heapq.heappush(heap, (freq, num))  # (频率, 元素)
        if len(heap) > k:
            heapq.heappop(heap)  # 弹出频率最小的
    
    # 堆中保留的是频率最大的k个元素，但顺序是频率小的在前
    # 需要reverse
    return [num for freq, num in reversed(heap)]


def topKFrequent_v2(nums: List[int], k: int) -> List[int]:
    """方法2：用负频率实现最大堆（更直观）"""
    counter = Counter(nums)
    heap = []
    
    for num, freq in counter.items():
        heapq.heappush(heap, (-freq, num))  # 负频率，实现最大堆效果
        if len(heap) > k:
            heapq.heappop(heap)  # 弹出负频率最大的（即频率最小的）
    
    # 堆中的元素按负频率排序（-3 < -2），但我们需要频率大的在前
    # 所以需要reverse或按频率排序
    return [num for neg_freq, num in reversed(heap)]


def topKFrequent_v3(nums: List[int], k: int) -> List[int]:
    """方法3：全部入堆再弹出k个（效率较低，但思路清晰）"""
    counter = Counter(nums)
    heap = []
    
    # 全部入堆
    for num, freq in counter.items():
        heapq.heappush(heap, (-freq, num))
    
    # 弹出k个最大的
    result = []
    for _ in range(k):
        neg_freq, num = heapq.heappop(heap)
        result.append(num)
    
    return result


if __name__ == '__main__':
    # 测试用例
    nums1 = [1, 1, 1, 2, 2, 3]
    nums2 = [4, 1, -1, 2, -1, 2, 3]
    
    print(f'测试1: {nums1}, k=2')
    print(f'方法1: {topKFrequent(nums1, 2)}')        # [1, 2]
    print(f'方法2: {topKFrequent_v2(nums1, 2)}')     # [1, 2]
    print(f'方法3: {topKFrequent_v3(nums1, 2)}')     # [1, 2]
    
    print(f'\n测试2: {nums2}, k=2')
    print(f'方法1: {topKFrequent(nums2, 2)}')        # [2, -1] (频率都是2)
    print(f'方法2: {topKFrequent_v2(nums2, 2)}')     # [2, -1]
    print(f'方法3: {topKFrequent_v3(nums2, 2)}')     # [-1, 2]



















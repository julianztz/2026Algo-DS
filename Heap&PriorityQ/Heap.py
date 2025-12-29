import heapq

from typing import List
from collections import Counter

'''
binary heap: 二叉堆就是一种能够动态排序的数据结构
        Binary Heap 会在 insert / delete 后
        自动恢复 parent ≥ children（max-heap）或 ≤（min-heap） 的局部顺序
        （并不保证左右子树大小关系）

应用： Priority Q & Heap sort
      （按照优先级顺序--最大/最小--提取（类似Queue），但是底层原理和二叉树有关，和队列没啥关系）
      总结：逻辑像是queue，实现利用binary tree

操作： sink & swim

maxHeap - root最大
minHeap - root最小

增删： O(logN)
space： O(1)
'''


# lc 215 Kth element in an array
'''
Given an integer array nums and an integer k, return the kth largest element in the array.
Note that it is the kth largest element in the sorted order, not the kth distinct element.
Can you solve it without sorting?
'''
def findKthLargest(nums: List[int], k: int) -> int:
    
    pq = []
    for e in nums:
        heapq.heappush(pq,e)

    for _ in range(len(pq)-k):
        heapq.heappop(pq)

    print(pq)
    return pq[0]



# lc 347. Top K Frequent Elements
'''
Given an integer array nums and an integer k, 
return the k most frequent elements. You may return the answer in any order.

Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
'''

# wrong❌❌❌-- 找了前k个不同的元素
def topKFrequentDiff(nums: List[int], k: int) -> List[int]:
    res = []
    pq = []
    for e in nums:
        heapq.heappush(pq, e)

    next_diff = None
    while k > 0:
        pop_num = heapq.heappop(pq)

        if next_diff != pop_num:
            res.append(pop_num)
            next_diff = pop_num
            k -= 1
    return res
    

# 目标-找前k个最多元素
'''
思路：
heap 存储 tuple(freq, num)
(freq, num)：freq 是优先级，num 是数据
按照频率高低进行pop保留前k个
'''
def topKFrequent(nums: List[int], k: int) -> List[int]:
    pq = []

    val_to_freq = Counter(nums)

    # 利用数字的频率作为priority存入heap，每个freq还match到对应的num
    for num, freq in val_to_freq.items():
        heapq.heappush(pq, (freq, num))
        
    while len(pq) > k:
        heapq.heappop(pq)

    res = [n for freq, n in pq]
    print(res)
    return res

    

    




if __name__ == '__main__':
    n1 = [3,2,1,5,6,4]
    findKthLargest(n1, 2)


    n2 = [1,1,1,2,2,3]
    n3 = [4,1,-1,2,-1,2,3]

    topKFrequent(n3, 2)
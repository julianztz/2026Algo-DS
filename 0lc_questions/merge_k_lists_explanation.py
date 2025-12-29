# -*- coding: utf-8 -*-
"""
合并 k 个排序链表 - 思路解析和实现
"""

from typing import Optional, List

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

print("=" * 70)
print("合并 k 个排序链表 - 思路解析")
print("=" * 70)

print("\n【你的思路分析】")
print("""
你的思路：
  - 用 p_min 追踪最小元素 ✅
  - 用 cur 追踪每个链表的首元素 ⚠️

问题：
  1. cur 只追踪一个链表，需要追踪所有链表的当前节点
  2. 循环逻辑有问题，会越界（i 会超出范围）
  3. 没有正确维护每个链表的当前指针
  4. 当链表结束时，不知道如何切换到下一个链表
""")

print("\n" + "=" * 70)
print("正确的思路")
print("=" * 70)

print("""
【核心思路】

1. 维护每个链表的当前指针
   - 用 lists[i] 直接存储第 i 个链表的当前节点
   - 初始时，lists[i] 就是每个链表的头节点
   - 每次选择最小节点后，将该链表的指针后移

2. 每次循环：
   - 遍历所有链表的当前节点（lists[0], lists[1], ..., lists[k-1]）
   - 找到值最小的节点（p_min）
   - 记录该节点所在的链表索引（min_idx）

3. 将最小节点加入结果链表
   - p.next = p_min
   - p = p.next

4. 移动该链表的指针
   - lists[min_idx] = lists[min_idx].next

5. 如果某个链表结束（lists[i] == None），跳过它

6. 重复步骤2-5，直到所有链表都结束（min_idx == -1）
""")

print("\n" + "=" * 70)
print("正确实现")
print("=" * 70)

def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    合并 k 个排序链表
    
    思路：
    1. 维护每个链表的当前指针（用 lists 数组直接存储）
    2. 每次遍历所有链表的当前节点，找到最小的
    3. 将最小节点加入结果链表
    4. 移动该链表的指针
    5. 重复直到所有链表都结束
    """
    if not lists:
        return None
    
    dummy = ListNode(0)
    p = dummy
    
    # 循环直到所有链表都处理完
    while True:
        # 找到当前所有链表头节点中的最小值
        min_val = float('inf')
        min_idx = -1  # 记录最小节点所在的链表索引
        p_min = None  # p_min 指向最小节点
        
        # 遍历所有链表，找到当前最小的节点
        for i in range(len(lists)):
            # 如果该链表还没结束，且值更小
            if lists[i] and lists[i].val < min_val:
                min_val = lists[i].val
                min_idx = i
                p_min = lists[i]  # p_min 指向最小节点
        
        # 如果所有链表都结束了（min_idx == -1），退出循环
        if min_idx == -1:
            break
        
        # 将最小节点加入结果链表
        p.next = p_min
        p = p.next
        
        # 移动该链表的指针到下一个节点
        lists[min_idx] = lists[min_idx].next
    
    return dummy.next

print("""
def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    if not lists:
        return None
    
    dummy = ListNode(0)
    p = dummy
    
    # 循环直到所有链表都处理完
    while True:
        # 找到当前所有链表头节点中的最小值
        min_val = float('inf')
        min_idx = -1  # 记录最小节点所在的链表索引
        p_min = None  # p_min 指向最小节点
        
        # 遍历所有链表，找到当前最小的节点
        for i in range(len(lists)):
            # 如果该链表还没结束，且值更小
            if lists[i] and lists[i].val < min_val:
                min_val = lists[i].val
                min_idx = i
                p_min = lists[i]  # p_min 指向最小节点
        
        # 如果所有链表都结束了（min_idx == -1），退出循环
        if min_idx == -1:
            break
        
        # 将最小节点加入结果链表
        p.next = p_min
        p = p.next
        
        # 移动该链表的指针到下一个节点
        lists[min_idx] = lists[min_idx].next
    
    return dummy.next
""")

print("\n" + "=" * 70)
print("关键理解")
print("=" * 70)

print("""
【关键点1：lists[i] 的含义】
  - 初始时：lists[i] 是第 i 个链表的头节点
  - 过程中：lists[i] 是第 i 个链表的当前节点
  - 结束时：lists[i] 是 None（该链表已处理完）

【关键点2：如何追踪所有链表的当前节点】
  - 不需要额外的数组
  - 直接用 lists 数组存储每个链表的当前节点
  - 每次选择最小节点后，更新 lists[min_idx] = lists[min_idx].next

【关键点3：如何判断所有链表都结束】
  - 如果遍历完所有链表，min_idx 仍然是 -1
  - 说明所有链表都是 None，可以退出循环

【关键点4：为什么不需要 cur 数组？】
  - 因为 lists[i] 本身就存储了当前节点
  - 不需要额外的 cur 数组来追踪
""")

print("\n" + "=" * 70)
print("你的代码问题分析")
print("=" * 70)

print("""
【问题1：cur 只追踪一个链表】
  你的代码：
    cur = lists[0]  # 只追踪第一个链表
  
  正确做法：
    遍历所有链表：for i in range(len(lists))
    用 lists[i] 访问每个链表的当前节点

【问题2：循环会越界】
  你的代码：
    while i < len(lists):
        i += 1
        cur = lists[i]  # 当 i == len(lists) 时会越界
  
  正确做法：
    for i in range(len(lists)):
        if lists[i]:  # 检查是否为空
            ...

【问题3：没有维护每个链表的指针】
  你的代码：
    只更新了 cur，没有更新 lists[i]
  
  正确做法：
    lists[min_idx] = lists[min_idx].next  # 移动该链表的指针

【问题4：不知道如何切换到下一个链表】
  你的代码：
    if p_min.next:
        cur = p_min.next
    else:
        # 不知道如何处理
  
  正确做法：
    不需要手动切换，循环会自动遍历所有链表
    如果某个链表结束（lists[i] == None），循环会跳过它
""")

print("\n" + "=" * 70)
print("执行流程示例")
print("=" * 70)

print("""
假设有 3 个链表：
  lists[0]: 1 -> 4 -> 5
  lists[1]: 1 -> 3 -> 4
  lists[2]: 2 -> 6

初始状态：
  lists[0] = 1 (节点)
  lists[1] = 1 (节点)
  lists[2] = 2 (节点)

第1次循环：
  - 遍历所有链表：lists[0].val=1, lists[1].val=1, lists[2].val=2
  - 找到最小：min_val=1, min_idx=0 (或1，都可以)
  - 假设选择 lists[0]
  - p.next = lists[0] (节点1)
  - lists[0] = lists[0].next (节点4)

第2次循环：
  - 遍历所有链表：lists[0].val=4, lists[1].val=1, lists[2].val=2
  - 找到最小：min_val=1, min_idx=1
  - p.next = lists[1] (节点1)
  - lists[1] = lists[1].next (节点3)

第3次循环：
  - 遍历所有链表：lists[0].val=4, lists[1].val=3, lists[2].val=2
  - 找到最小：min_val=2, min_idx=2
  - p.next = lists[2] (节点2)
  - lists[2] = lists[2].next (节点6)

... 继续直到所有链表都结束
""")

print("\n" + "=" * 70)
print("时间复杂度分析")
print("=" * 70)

print("""
【时间复杂度】
  - 每次循环：O(k) 找到最小节点（k 是链表数量）
  - 总循环次数：O(n)（n 是所有节点的总数）
  - 总时间复杂度：O(k * n)

【空间复杂度】
  - O(1) 额外空间（不包括结果链表）
  - 直接修改 lists 数组，不需要额外空间

【优化方法】
  如果 k 很大，可以用优先队列（堆）优化到 O(n log k)
  但你的思路（直接遍历）对于 k 较小的情况已经足够好了
""")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)

print("""
✅ 你的思路方向正确：
  - 用 p_min 追踪最小元素 ✅
  - 需要找到所有链表中当前最小的节点 ✅

⚠️ 需要改进的地方：
  1. 不要用单个 cur，要遍历所有链表的当前节点
  2. 用 lists[i] 直接存储每个链表的当前节点
  3. 每次选择最小节点后，更新 lists[min_idx] = lists[min_idx].next
  4. 当所有链表都结束时（min_idx == -1），退出循环

【核心改进】
  - 不需要 cur 数组
  - 直接用 lists[i] 追踪每个链表的当前节点
  - 循环遍历所有链表，找到最小的
  - 更新该链表的指针，继续循环
""")




























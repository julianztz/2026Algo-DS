# -*- coding: utf-8 -*-
"""
循环队列实现指南
解答：deque 如何处理 size/full，以及循环逻辑的实现
"""

import sys
import io
from collections import deque

# 设置输出编码为 UTF-8（解决 Windows 控制台编码问题）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ========== 1. deque 的 maxlen 参数 ==========
print("=" * 60)
print("1. deque 的 maxlen 参数 - 如何处理 size/full")
print("=" * 60)

# deque 可以通过 maxlen 参数限制最大长度
dq = deque(maxlen=3)
print(f"创建 deque(maxlen=3): {dq}")

# 当达到 maxlen 时，添加新元素会自动删除最旧的元素
for i in range(1, 6):
    dq.append(i)
    print(f"  添加 {i}: {dq} (len={len(dq)})")

print("\n关键点：")
print("  - deque 的 maxlen 是自动丢弃旧元素，不是循环队列")
print("  - 当满时，append() 会自动 popleft() 最旧的元素")
print("  - 这不符合循环队列的定义（应该拒绝添加，而不是丢弃）")

# 检查是否满
print(f"\n检查是否满：")
print(f"  len(dq) == dq.maxlen: {len(dq) == dq.maxlen}")
print(f"  dq.maxlen: {dq.maxlen}")


# ========== 2. 使用 deque 实现循环队列（需要手动管理） ==========
print("\n" + "=" * 60)
print("2. 使用 deque 实现循环队列（手动管理 size）")
print("=" * 60)

class CircularQueueWithDeque:
    """
    使用 deque 实现循环队列
    注意：deque 本身不需要 mod，但我们需要手动管理 size
    """
    
    def __init__(self, k: int):
        self.capacity = k
        self.queue = deque()  # 不使用 maxlen，手动管理
        # 或者：self.queue = deque(maxlen=k) 但这样会自动丢弃，不符合要求
    
    def enQueue(self, value: int) -> bool:
        """入队：如果队列未满，返回 True；否则返回 False"""
        if len(self.queue) == self.capacity:
            return False  # 队列已满，拒绝添加
        self.queue.append(value)
        return True
    
    def deQueue(self) -> bool:
        """出队：如果队列非空，返回 True；否则返回 False"""
        if len(self.queue) == 0:
            return False
        self.queue.popleft()
        return True
    
    def Front(self) -> int:
        """返回队首元素，如果队列为空返回 -1"""
        if len(self.queue) == 0:
            return -1
        return self.queue[0]
    
    def Rear(self) -> int:
        """返回队尾元素，如果队列为空返回 -1"""
        if len(self.queue) == 0:
            return -1
        return self.queue[-1]
    
    def isEmpty(self) -> bool:
        return len(self.queue) == 0
    
    def isFull(self) -> bool:
        return len(self.queue) == self.capacity


# 测试
print("使用 deque 实现（不需要 mod）：")
cq_deque = CircularQueueWithDeque(3)
print(f"  初始: {cq_deque.queue}, isEmpty={cq_deque.isEmpty()}, isFull={cq_deque.isFull()}")

for i in range(1, 5):
    result = cq_deque.enQueue(i)
    print(f"  enQueue({i}): {result}, queue={list(cq_deque.queue)}, isFull={cq_deque.isFull()}")

print(f"  Front: {cq_deque.Front()}, Rear: {cq_deque.Rear()}")
cq_deque.deQueue()
print(f"  deQueue 后: {list(cq_deque.queue)}")
cq_deque.enQueue(4)
print(f"  enQueue(4) 后: {list(cq_deque.queue)}")


# ========== 3. 使用 list 实现循环队列（需要 mod） ==========
print("\n" + "=" * 60)
print("3. 使用 list 实现循环队列（需要 mod 运算）")
print("=" * 60)

class CircularQueueWithList:
    """
    使用 list 实现循环队列
    关键：需要使用 mod 运算来处理循环逻辑
    """
    
    def __init__(self, k: int):
        self.capacity = k
        self.queue = [None] * k  # 固定大小的 list
        self.front = 0  # 队首指针
        self.rear = 0   # 队尾指针（指向下一个插入位置）
        self.size = 0   # 当前元素数量
    
    def enQueue(self, value: int) -> bool:
        """入队：如果队列未满，返回 True；否则返回 False"""
        if self.size == self.capacity:
            return False  # 队列已满
        
        self.queue[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity  # 关键：mod 运算实现循环
        self.size += 1
        return True
    
    def deQueue(self) -> bool:
        """出队：如果队列非空，返回 True；否则返回 False"""
        if self.size == 0:
            return False
        
        self.queue[self.front] = None  # 清理引用
        self.front = (self.front + 1) % self.capacity  # 关键：mod 运算实现循环
        self.size -= 1
        return True
    
    def Front(self) -> int:
        """返回队首元素，如果队列为空返回 -1"""
        if self.size == 0:
            return -1
        return self.queue[self.front]
    
    def Rear(self) -> int:
        """返回队尾元素，如果队列为空返回 -1"""
        if self.size == 0:
            return -1
        # rear 指向下一个插入位置，所以队尾是 (rear - 1) % capacity
        rear_index = (self.rear - 1 + self.capacity) % self.capacity
        return self.queue[rear_index]
    
    def isEmpty(self) -> bool:
        return self.size == 0
    
    def isFull(self) -> bool:
        return self.size == self.capacity
    
    def __str__(self):
        """可视化"""
        elements = []
        for i in range(self.size):
            idx = (self.front + i) % self.capacity
            elements.append(str(self.queue[idx]))
        return f"CircularQueue: [{', '.join(elements)}] (底层: {self.queue}, front={self.front}, rear={self.rear}, size={self.size})"


# 测试
print("使用 list 实现（需要 mod）：")
cq_list = CircularQueueWithList(3)
print(f"  初始: {cq_list}")

for i in range(1, 5):
    result = cq_list.enQueue(i)
    print(f"  enQueue({i}): {result}, {cq_list}")

print(f"  Front: {cq_list.Front()}, Rear: {cq_list.Rear()}")
cq_list.deQueue()
print(f"  deQueue 后: {cq_list}")
cq_list.enQueue(4)
print(f"  enQueue(4) 后: {cq_list}")


# ========== 4. 关键问题解答 ==========
print("\n" + "=" * 60)
print("4. 关键问题解答")
print("=" * 60)

print("""
Q1: deque 是如何处理 size full 的？

A1: deque 有两种方式处理 size：
    
    方式1: 使用 maxlen 参数
        dq = deque(maxlen=3)
        - 当达到 maxlen 时，append() 会自动删除最旧的元素
        - 这不是循环队列，而是自动丢弃旧元素
        - 检查是否满：len(dq) == dq.maxlen
    
    方式2: 不使用 maxlen，手动管理
        dq = deque()
        - 需要自己维护 capacity 和检查 len(dq) == capacity
        - 符合循环队列的定义（满时拒绝添加）


Q2: 无论用哪种结构，都需要用 mod 来处理循环逻辑对吗？

A2: 不完全对！这取决于使用哪种结构：

    ✅ 使用 list 实现：需要 mod 运算
        - list 是固定大小的数组
        - 需要通过 front/rear 指针 + mod 运算实现循环
        - 例如：rear = (rear + 1) % capacity
    
    ❌ 使用 deque 实现：不需要 mod 运算
        - deque 本身就是动态的，会自动管理内存
        - 不需要手动计算索引的循环
        - 只需要检查 len(deque) == capacity 来判断是否满
    
    总结：
    - list 实现：需要 mod（因为使用固定大小数组 + 指针）
    - deque 实现：不需要 mod（因为 deque 本身就是动态的）


Q3: 两种实现的对比

    使用 list：
        ✅ 更接近底层实现，理解循环数组的本质
        ✅ 内存固定，不会动态扩容
        ❌ 需要手动管理指针和 mod 运算
        ❌ 代码更复杂
    
    使用 deque：
        ✅ 代码更简洁，不需要 mod 运算
        ✅ deque 的 popleft() 和 append() 都是 O(1)
        ❌ 需要手动检查 size（不能直接用 maxlen）
        ❌ 可能不如 list 实现直观理解循环数组概念
""")


# ========== 5. LeetCode 622 循环队列的标准实现 ==========
print("\n" + "=" * 60)
print("5. LeetCode 622 循环队列 - 两种实现方式对比")
print("=" * 60)

print("""
方式1: 使用 list + mod（推荐用于理解）
- 需要 mod 运算处理循环
- 需要维护 front, rear, size

方式2: 使用 deque（代码更简洁）
- 不需要 mod 运算
- 只需要检查 len(deque) == capacity

两种方式都可以，选择哪种取决于：
- 学习目的：用 list 更好理解循环数组的本质
- 实际应用：用 deque 代码更简洁
""")


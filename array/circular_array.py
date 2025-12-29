'''
环形数组（循环数组）-- 求模mod

【Python 中的数组结构】
1. list - Python 内置的动态数组（最常用）
2. array.array - 标准库的同类型数组（需要 import array）
3. numpy.array - NumPy 数组（第三方库，科学计算）

【循环数组的本质】
- 循环数组不是 Python 的内置类型
- 循环数组是使用 list 实现的一种数据结构模式/设计技巧
- 通过指针 + mod 运算实现循环逻辑
- 底层存储：使用 Python list（如 [None] * capacity）

【核心目的】
主要用于实现队列（Queue）等数据结构，优化两端操作的效率
- 普通数组队列：dequeue() 需要 pop(0)，时间复杂度 O(n)（需移动所有元素）
- 环形数组队列：dequeue() 只需移动指针，时间复杂度 O(1)

【注意】
❌ 不是为了提高普通数组在任意位置的 insert/remove 效率
✅ 只优化队列的两端操作（头部删除、尾部插入）
✅ 适用于 FIFO 数据结构（队列、双端队列）

0.原理 双指针维护
start/front: 指向第一个有效元素的索引
end/rear: 指向最后一个有效元素的下一个位置索引
区间 -- 左闭右开

1.实现示例   # 利用 mod 不停遍历arr
while i < len(ls):
    print(ls[i])
    i = (i+1) % len(ls)

2.队列应用
参考：linkedList/circularArrayQueue.py
- enqueue: O(1) - 尾部插入
- dequeue: O(1) - 头部删除（关键优势！）

3.详细说明
参考：array/python_array_types.md
'''


ls = [1,2,3,4,5]
i = 0
while i < len(ls):
    # print(ls[i])
    i = (i+1) % len(ls)


from collections import deque

# 622 循环队列 - deque实现
'''
动态，无需手动管理index和循环
'''
class MyCircularQueue_deque:

    def __init__(self, k: int):
        self.q = deque()
        self.capacity = k

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.q.append(value)
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.q.popleft()          # FIFO
        return True
        
    def Front(self) -> int:
        if self.isEmpty():
            return -1
        return self.q[0]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self.q[-1]

    def isEmpty(self) -> bool:
        return len(self.q) == 0

    def isFull(self) -> bool:
        return len(self.q) == self.capacity


# 622 循环队列 - list实现
'''
需要用指针+mod手动计算循环
'''
class MyCircularQueue_list:

    def __init__(self, k: int):
        self.q = [None] * k
        self.capacity = k
                                    #  先   ----------->  后
        self.front = 0              #   1,   2,  3,  4,   5  --> append 顺序 
        self.rear = 0               # front             rear             
        self.size = 0

    # enqueue 以后 rear指向下一个空位置
    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.q[self.rear] = value
        # self.rear += 1
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1 
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.q[self.front] = None
        # self.q.pop(self.front)          #  pop 会自动shift后续所有elements,破坏了循环数组O(1)优势
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def Front(self) -> int:
        if self.isEmpty():
            return -1
        return self.q[self.front]
       
    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        # return self.q[self.rear]       # rear指向下个空位置
        last = (self.rear - 1 + self.capacity) % self.capacity
        return self.q[last]
      
    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity


# 641 双端循环队列 - list实现  左闭右开？？
'''
0.原理 双指针维护
start/front: 指向第一个有效元素的索引
end/rear: 指向最后一个有效元素的下一个位置索引
'''
class MyDoubleCircularDeque_list:
    def __init__(self, k: int):
        self.q = [None] * k
        self.capacity = k
                                    #  先   ----------->  后
        self.front = 0              #   1,   2,  3,  4,   5  --> append 顺序 
        self.rear = 0               # front             rear             
        self.size = 0

    def insertFront(self, value: int) -> bool:    # front端 插入前移
        if self.isFull():
            return False

        self.front = (self.front - 1 + self.capacity) % self.capacity               # front： 第一个有元素位置 需要前移跳过
        self.q[self.front] = value                                                  
        self.size += 1
        return True

    def insertLast(self, value: int) -> bool:     # 插入后移
        if self.isFull():
            return False
        self.q[self.rear] = value                                                    # rear： 最后一个元素的下个空位 直接insert
        self.rear = (self.rear + 1) % self.capacity

        self.size += 1
        return True

    def deleteFront(self) -> bool:               # front端 删除后移
        if self.isEmpty():
            return False
        self.q[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def deleteLast(self) -> bool:                # 删除前移
        if self.isEmpty():
            return False
        self.rear = (self.rear -1 + self.capacity) % self.capacity
        self.q[self.rear] = None
        self.size -= 1
        return True

    def getFront(self) -> int:
        if self.isEmpty():
            return -1
        return self.q[self.front]

    def getRear(self) -> int:
        if self.isEmpty():
            return -1
        last = (self.rear - 1 + self.capacity) % self.capacity
        return self.q[last]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
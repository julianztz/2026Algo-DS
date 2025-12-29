class CircularArrayQueue:
    """
    使用循环数组实现的队列，dequeue操作O(1)时间复杂度
    """
    
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0  # 队首指针
        self.rear = 0   # 队尾指针
        self.size = 0   # 当前元素数量
    
    def enqueue(self, e):
        """入队操作 O(1)"""
        if self.is_full():
            self._resize()  # 动态扩容
        
        self.queue[self.rear] = e
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
    
    def dequeue(self):
        """出队操作 O(1) - 关键优势！"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        
        element = self.queue[self.front]
        self.queue[self.front] = None  # 清理引用
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return element
    
    def peek(self):
        """查看队首元素 O(1)"""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.queue[self.front]
    
    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size == self.capacity
    
    def get_size(self):
        return self.size
    
    def _resize(self):
        """动态扩容 O(n) - 但摊还分析后为O(1)"""
        old_capacity = self.capacity
        self.capacity *= 2
        new_queue = [None] * self.capacity
        
        # 将元素从旧数组复制到新数组
        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % old_capacity]
        
        self.queue = new_queue
        self.front = 0
        self.rear = self.size
    
    def __str__(self):
        """可视化队列状态"""
        if self.is_empty():
            return "Queue: []"
        
        elements = []
        for i in range(self.size):
            idx = (self.front + i) % self.capacity
            elements.append(str(self.queue[idx]))
        
        return f"Queue: [{', '.join(elements)}] (front={self.front}, rear={self.rear}, size={self.size})"


# 测试代码
if __name__ == "__main__":
    # 创建循环队列
    cq = CircularArrayQueue(5)
    
    print("=== 循环数组队列测试 ===")
    
    # 入队测试
    for i in range(1, 6):
        cq.enqueue(i)
        print(f"入队 {i}: {cq}")
    
    # 出队测试
    print(f"\n出队: {cq.dequeue()}")
    print(f"出队后: {cq}")
    
    # 继续入队测试循环特性
    cq.enqueue(6)
    print(f"入队 6: {cq}")
    
    # 性能对比测试
    import time
    
    print("\n=== 性能对比测试 ===")
    n = 10000
    
    # 测试1: 普通list实现
    start = time.time()
    list_queue = []
    for i in range(n):
        list_queue.append(i)
    for i in range(n):
        list_queue.pop(0)  # O(n) 操作
    list_time = time.time() - start
    print(f"List实现 (pop(0)): {list_time:.4f}秒")
    
    # 测试2: 循环数组实现
    start = time.time()
    circular_queue = CircularArrayQueue()
    for i in range(n):
        circular_queue.enqueue(i)
    for i in range(n):
        circular_queue.dequeue()  # O(1) 操作
    circular_time = time.time() - start
    print(f"循环数组实现: {circular_time:.4f}秒")
    
    print(f"性能提升: {list_time/circular_time:.1f}倍")

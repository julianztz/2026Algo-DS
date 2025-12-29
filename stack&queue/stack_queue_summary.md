# Stack 和 Queue 应用情景与用法总结

## 一、基本概念

### Stack（栈）- LIFO（后进先出）

**特性：**
- 同一端进行插入和删除操作
- 后进入的元素先出来
- 就像叠盘子：最后放上去的盘子最先拿下来

**操作：**
- `push()` / `append()` - 入栈（O(1)）
- `pop()` - 出栈（O(1)）
- `peek()` / `top()` - 查看栈顶（O(1)）

### Queue（队列）- FIFO（先进先出）

**特性：**
- 一端插入，另一端删除
- 先进入的元素先出来
- 就像排队：先来的人先买到票

**操作：**
- `enqueue()` / `append()` - 入队（O(1)）
- `dequeue()` / `popleft()` - 出队（O(1)）
- `front()` / `peek()` - 查看队首（O(1)）

---

## 二、Python 实现方式

### 1. 使用 list 实现 Stack

```python
# Stack 实现
stack = []

# 入栈
stack.append(item)  # O(1)

# 出栈
item = stack.pop()  # O(1)

# 查看栈顶
top = stack[-1]  # O(1)

# 检查是否为空
is_empty = len(stack) == 0  # 或 not stack
```

### 2. 使用 list 实现 Queue（不推荐）

```python
# Queue 实现（低效）
queue = []

# 入队
queue.append(item)  # O(1)

# 出队
item = queue.pop(0)  # ❌ O(n) - 需要移动所有元素！
```

### 3. 使用 deque 实现 Queue（推荐）

```python
from collections import deque

# Queue 实现（高效）
queue = deque()

# 入队
queue.append(item)  # O(1)

# 出队
item = queue.popleft()  # ✅ O(1)

# 查看队首
front = queue[0]  # O(1)
```

### 4. 使用 list 实现循环队列（固定大小）

```python
class CircularQueue:
    def __init__(self, k: int):
        self.q = [None] * k
        self.capacity = k
        self.front = 0  # 指向第一个有效元素
        self.rear = 0   # 指向最后一个有效元素的下一个位置
        self.size = 0
    
    def enqueue(self, value: int) -> bool:
        if self.size == self.capacity:
            return False
        self.q[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
        return True
    
    def dequeue(self) -> bool:
        if self.size == 0:
            return False
        self.q[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True
```

---

## 三、Stack 应用场景

### 1. 括号匹配问题

**LeetCode 20: Valid Parentheses**

```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # 右括号
            if not stack or stack.pop() != mapping[char]:
                return False
        else:  # 左括号
            stack.append(char)
    
    return not stack
```

**应用场景：**
- XML/HTML 标签匹配
- 代码语法检查
- 表达式求值

### 2. 路径简化问题

**LeetCode 71: Simplify Path**

```python
def simplifyPath(path: str) -> str:
    stack = []
    parts = path.split("/")
    
    for part in parts:
        if part == "..":
            if stack:
                stack.pop()  # 返回上一级目录
        elif part and part != ".":
            stack.append(part)  # 进入目录
    
    return "/" + "/".join(stack)
```

**应用场景：**
- 文件系统路径处理
- URL 规范化

### 3. 表达式求值

**中缀表达式转后缀表达式（逆波兰表达式）**

```python
def evaluateExpression(expression: str) -> int:
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in expression.split():
        if token not in operators:
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a // b)
    
    return stack[0]
```

**应用场景：**
- 计算器实现
- 编译器表达式解析

### 4. 单调栈问题

**LeetCode 739: Daily Temperatures**

```python
def dailyTemperatures(temperatures: list) -> list:
    stack = []  # 存储索引
    result = [0] * len(temperatures)
    
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_index = stack.pop()
            result[prev_index] = i - prev_index
        stack.append(i)
    
    return result
```

**应用场景：**
- 寻找下一个更大/更小元素
- 柱状图最大矩形面积
- 接雨水问题

### 5. 函数调用栈

**递归转迭代**

```python
# 递归版本
def dfs_recursive(node):
    if not node:
        return
    print(node.val)
    dfs_recursive(node.left)
    dfs_recursive(node.right)

# 迭代版本（使用栈）
def dfs_iterative(root):
    stack = [root]
    while stack:
        node = stack.pop()
        if node:
            print(node.val)
            stack.append(node.right)  # 先右后左，保证左先处理
            stack.append(node.left)
```

**应用场景：**
- 深度优先搜索（DFS）
- 树的前序/中序/后序遍历
- 回溯算法

### 6. 撤销操作（Undo）

```python
class TextEditor:
    def __init__(self):
        self.text = ""
        self.undo_stack = []
    
    def type(self, char):
        self.undo_stack.append(self.text)  # 保存状态
        self.text += char
    
    def undo(self):
        if self.undo_stack:
            self.text = self.undo_stack.pop()
```

**应用场景：**
- 文本编辑器撤销功能
- 浏览器前进后退
- 游戏状态保存

---

## 四、Queue 应用场景

### 1. 广度优先搜索（BFS）

**LeetCode 102: Binary Tree Level Order Traversal**

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    
    queue = deque([root])
    result = []
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

**应用场景：**
- 树的层序遍历
- 图的最短路径（无权图）
- 社交网络中的"六度分隔"问题

### 2. 滑动窗口问题

**LeetCode 239: Sliding Window Maximum**

```python
from collections import deque

def maxSlidingWindow(nums, k):
    queue = deque()  # 存储索引，保持单调递减
    result = []
    
    for i, num in enumerate(nums):
        # 移除窗口外的元素
        while queue and queue[0] <= i - k:
            queue.popleft()
        
        # 保持单调递减
        while queue and nums[queue[-1]] < num:
            queue.pop()
        
        queue.append(i)
        
        # 窗口形成后，记录最大值
        if i >= k - 1:
            result.append(nums[queue[0]])
    
    return result
```

**应用场景：**
- 滑动窗口最大值/最小值
- 数据流中的中位数
- 实时数据统计

### 3. 任务调度

```python
from collections import deque
import time

class TaskScheduler:
    def __init__(self):
        self.task_queue = deque()
    
    def add_task(self, task):
        self.task_queue.append(task)
    
    def process_tasks(self):
        while self.task_queue:
            task = self.task_queue.popleft()
            task.execute()
            time.sleep(0.1)  # 模拟处理时间
```

**应用场景：**
- 操作系统进程调度
- 消息队列
- 打印队列
- 网络请求队列

### 4. 缓存实现（LRU Cache）

```python
from collections import deque

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.access_order = deque()  # 记录访问顺序
    
    def get(self, key):
        if key in self.cache:
            # 更新访问顺序
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            self.access_order.remove(key)
            self.access_order.append(key)
        else:
            if len(self.cache) >= self.capacity:
                # 移除最久未使用的
                lru_key = self.access_order.popleft()
                del self.cache[lru_key]
            self.cache[key] = value
            self.access_order.append(key)
```

**应用场景：**
- 缓存系统
- 内存管理
- 数据库查询优化

### 5. 最短路径问题（BFS）

**LeetCode 127: Word Ladder**

```python
from collections import deque

def ladderLength(beginWord, endWord, wordList):
    wordSet = set(wordList)
    if endWord not in wordSet:
        return 0
    
    queue = deque([(beginWord, 1)])
    visited = {beginWord}
    
    while queue:
        word, length = queue.popleft()
        
        if word == endWord:
            return length
        
        # 尝试改变每个字符
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word in wordSet and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))
    
    return 0
```

**应用场景：**
- 无权图最短路径
- 迷宫问题
- 单词变换问题

### 6. 生产者-消费者模式

```python
from collections import deque
import threading
import time

class ProducerConsumer:
    def __init__(self):
        self.queue = deque()
        self.max_size = 10
    
    def producer(self):
        for i in range(20):
            while len(self.queue) >= self.max_size:
                time.sleep(0.1)  # 队列满，等待
            self.queue.append(f"item_{i}")
            print(f"Produced: item_{i}")
            time.sleep(0.5)
    
    def consumer(self):
        while True:
            if self.queue:
                item = self.queue.popleft()
                print(f"Consumed: {item}")
                time.sleep(0.3)
            else:
                time.sleep(0.1)  # 队列空，等待
```

**应用场景：**
- 多线程编程
- 异步任务处理
- 事件驱动系统

---

## 五、Stack vs Queue 选择指南

### 何时使用 Stack？

✅ **需要"后进先出"的场景：**
- 括号匹配、表达式求值
- 函数调用、递归转迭代
- 撤销操作（Undo）
- 深度优先搜索（DFS）
- 单调栈问题

**记忆技巧：** 需要"回溯"或"撤销"的场景

### 何时使用 Queue？

✅ **需要"先进先出"的场景：**
- 广度优先搜索（BFS）
- 任务调度、消息队列
- 滑动窗口问题
- 最短路径问题（无权图）
- 生产者-消费者模式

**记忆技巧：** 需要"按顺序处理"或"层级遍历"的场景

---

## 六、常见算法模式

### 1. 双栈模式

```python
# 实现一个支持 getMin() 的栈
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # 辅助栈，存储最小值
    
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self):
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val
    
    def getMin(self):
        return self.min_stack[-1]
```

### 2. 单调栈模式

```python
# 寻找下一个更大元素
def nextGreaterElement(nums):
    stack = []
    result = [-1] * len(nums)
    
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            index = stack.pop()
            result[index] = num
        stack.append(i)
    
    return result
```

### 3. 双端队列模式（Deque）

```python
from collections import deque

# 滑动窗口最大值
def maxSlidingWindow(nums, k):
    dq = deque()  # 存储索引
    result = []
    
    for i, num in enumerate(nums):
        # 移除窗口外的元素
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # 保持单调递减
        while dq and nums[dq[-1]] < num:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

---

## 七、性能对比

| 操作 | list (Stack) | list (Queue) | deque (Queue) | 循环队列 |
|------|--------------|--------------|---------------|----------|
| push/enqueue | O(1) | O(1) | O(1) | O(1) |
| pop (栈) | O(1) | - | - | - |
| pop(0) (队列) | - | O(n) ❌ | O(1) ✅ | O(1) ✅ |
| 空间复杂度 | O(n) | O(n) | O(n) | O(k) 固定 |

**建议：**
- Stack: 使用 `list` ✅
- Queue: 使用 `deque` ✅（不要用 `list.pop(0)`）
- 固定大小队列: 使用循环队列 ✅

---

## 八、实战技巧

### 1. Python 中的最佳实践

```python
# ✅ Stack - 使用 list
stack = []
stack.append(item)  # push
item = stack.pop()  # pop
top = stack[-1] if stack else None  # peek

# ✅ Queue - 使用 deque
from collections import deque
queue = deque()
queue.append(item)  # enqueue
item = queue.popleft()  # dequeue
front = queue[0] if queue else None  # peek

# ❌ 不要用 list 实现 Queue
queue = []
queue.append(item)  # O(1)
item = queue.pop(0)  # ❌ O(n) - 太慢！
```

### 2. 检查空栈/空队列

```python
# Pythonic 方式
if not stack:  # 推荐
    # 栈为空

if stack:  # 推荐
    # 栈不为空

# 也可以（但不够Pythonic）
if len(stack) == 0:
if stack == []:
```

### 3. 常见错误

```python
# ❌ 错误：在空栈上 pop
stack = []
item = stack.pop()  # IndexError!

# ✅ 正确：先检查
if stack:
    item = stack.pop()

# ❌ 错误：用 list 实现队列
queue = []
item = queue.pop(0)  # O(n) - 太慢！

# ✅ 正确：用 deque
from collections import deque
queue = deque()
item = queue.popleft()  # O(1)
```

---

## 九、LeetCode 经典题目

### Stack 相关
- ✅ 20. Valid Parentheses（括号匹配）
- ✅ 71. Simplify Path（路径简化）
- ✅ 150. Evaluate Reverse Polish Notation（表达式求值）
- ✅ 155. Min Stack（最小栈）
- ✅ 739. Daily Temperatures（单调栈）
- ✅ 84. Largest Rectangle in Histogram（柱状图最大矩形）
- ✅ 42. Trapping Rain Water（接雨水）

### Queue 相关
- ✅ 102. Binary Tree Level Order Traversal（层序遍历）
- ✅ 107. Binary Tree Level Order Traversal II
- ✅ 199. Binary Tree Right Side View
- ✅ 239. Sliding Window Maximum（滑动窗口最大值）
- ✅ 127. Word Ladder（单词接龙）
- ✅ 200. Number of Islands（岛屿数量 - BFS）

---

## 十、总结

### Stack（栈）
- **特性：** LIFO（后进先出）
- **实现：** Python `list`（`append()` + `pop()`）
- **应用：** 括号匹配、表达式求值、DFS、撤销操作
- **记忆：** "后进先出"、"回溯"、"撤销"

### Queue（队列）
- **特性：** FIFO（先进先出）
- **实现：** Python `deque`（`append()` + `popleft()`）
- **应用：** BFS、任务调度、滑动窗口、最短路径
- **记忆：** "先进先出"、"按顺序"、"层级遍历"

### 选择原则
- 需要"撤销"或"回溯" → Stack
- 需要"按顺序处理"或"层级遍历" → Queue
- 固定大小队列 → 循环队列
- 动态大小队列 → deque

---

**记住：**
- Stack = 叠盘子（后进先出）
- Queue = 排队（先进先出）
- 在 Python 中，Stack 用 `list`，Queue 用 `deque`！

































# BFS（广度优先搜索）注意事项总结

## 核心模板

```python
from collections import deque

def bfs(root):
    if not root:  # 边界检查
        return []
    
    q = deque([root])
    res = []
    
    while q:
        size = len(q)  # ⚠️ 关键：记录当前层节点数
        level_res = []
        
        for _ in range(size):  # 处理当前层所有节点
            cur = q.popleft()
            level_res.append(cur.val)
            
            # 添加子节点到队列
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        
        res.append(level_res)
    
    return res
```

---

## 注意事项

### 1. **队列选择：使用 `deque` 而非 `list`**
- ✅ `deque.popleft()` 是 O(1)
- ❌ `list.pop(0)` 是 O(n)
- 双端队列支持 `appendleft()`、`append()`、`popleft()`、`pop()`

### 2. **层数记录：必须在循环开始前记录 `size`**
```python
# ✅ 正确
while q:
    size = len(q)  # 在 for 循环前记录
    for _ in range(size):
        cur = q.popleft()
        # ...

# ❌ 错误
while q:
    for _ in range(len(q)):  # len(q) 在循环中会变化！
        cur = q.popleft()
        # ...
```
**原因**：在 `for` 循环中，`len(q)` 会随着 `popleft()` 和 `append()` 不断变化，导致无法正确遍历完一层。

### 3. **空节点检查**
```python
# ✅ 正确：添加前检查
if cur.left:
    q.append(cur.left)
if cur.right:
    q.append(cur.right)

# ❌ 错误：可能添加 None
q.append(cur.left)  # 如果 cur.left 是 None，队列中会有 None
```

### 4. **边界条件：root 为 None**
```python
if not root:
    return []  # 或 return None，根据题目要求
```

### 5. **层与层之间的处理**
- **标准层序遍历**：每层从左到右
- **反向层序遍历**：使用 `deque.appendleft()` 或最后 `[::-1]`
- **锯齿形遍历**：保持 enqueue 顺序一致，只反转结果列表

### 6. **特殊需求处理**

#### **Zigzag 遍历**
```python
# ✅ 正确：保持 enqueue 顺序，反转结果
left_to_right = True
while q:
    size = len(q)
    level_res = []
    for _ in range(size):
        cur = q.popleft()
        level_res.append(cur.val)
        # 总是按 left → right 顺序 enqueue
        if cur.left:
            q.append(cur.left)
        if cur.right:
            q.append(cur.right)
    
    if not left_to_right:
        level_res.reverse()  # 反转当前层结果
    left_to_right = not left_to_right
```

**⚠️ 常见错误**：试图通过改变 enqueue 顺序实现 zigzag
- 改变 enqueue 顺序只能影响**下一层**的顺序
- **当前层**的节点已经在队列中，顺序固定
- 必须通过反转结果列表来实现

#### **连接同层节点（如 `connect` 问题）**
```python
while q:
    size = len(q)
    prev = None  # 追踪前一个节点
    for _ in range(size):
        cur = q.popleft()
        if prev:
            prev.next = cur
        prev = cur
        # ...
```

#### **带编号的 BFS（如 `widthOfBinaryTree`）**
```python
class NodeWithNum:
    def __init__(self, node, num):
        self.node = node
        self.num = num

q = deque([NodeWithNum(root, 1)])
while q:
    size = len(q)
    first = last = 0
    for i in range(size):
        cur = q.popleft()
        if i == 0:
            first = cur.num
        if i == size - 1:
            last = cur.num
        # ...
```

### 7. **图问题中的重复访问**
- 使用 `visited` 集合避免重复访问
- 在添加到队列前标记为已访问
```python
visited = set()
q = deque([start])
visited.add(start)

while q:
    cur = q.popleft()
    for neighbor in get_neighbors(cur):
        if neighbor not in visited:
            visited.add(neighbor)
            q.append(neighbor)
```

### 8. **时间复杂度与空间复杂度**
- **时间复杂度**：O(n)，每个节点访问一次
- **空间复杂度**：O(w)，w 是树的最大宽度（最宽层的节点数）
  - 最坏情况：完全二叉树，w = n/2
  - 最好情况：链状树，w = 1

### 9. **与 DFS 的对比**

| 特性 | BFS | DFS |
|------|-----|-----|
| 数据结构 | 队列（FIFO） | 栈（LIFO） |
| 遍历顺序 | 层序（横向） | 深度优先（纵向） |
| 空间复杂度 | O(宽度) | O(高度) |
| 适用场景 | 最短路径、层序遍历 | 回溯、路径问题 |

### 10. **常见错误总结**

1. ❌ **在循环中使用 `len(q)`**：应该在循环前记录 `size`
2. ❌ **忘记检查空节点**：导致队列中有 `None`
3. ❌ **忘记边界检查**：`root` 为 `None` 时崩溃
4. ❌ **试图通过改变 enqueue 顺序实现 zigzag**：只能影响下一层
5. ❌ **使用 `list` 而非 `deque`**：`list.pop(0)` 效率低
6. ❌ **在 `for` 循环中修改队列长度**：导致层数混乱

---

## 200字归纳

**BFS（广度优先搜索）核心要点**：使用队列（`deque`）实现层序遍历，时间复杂度 O(n)，空间复杂度 O(宽度)。关键步骤：1）边界检查（`root` 为 `None`）；2）在 `while` 循环开始前记录 `size = len(q)`，确保完整遍历一层；3）在 `for` 循环中处理当前层所有节点，同时将子节点入队；4）添加子节点前检查非空；5）特殊需求（如 zigzag）通过反转结果列表实现，而非改变 enqueue 顺序。常见错误：在循环中使用 `len(q)`、忘记空节点检查、使用 `list.pop(0)` 而非 `deque.popleft()`。BFS 适用于最短路径、层序遍历等问题，与 DFS 相比更占空间但能保证找到最短路径。




















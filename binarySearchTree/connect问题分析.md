# Connect 问题分析：遍历 vs BFS

## 一、问题描述

**LC116: Populating Next Right Pointers in Each Node**

给定一个完美二叉树，将每层的节点通过 `next` 指针连接起来。

**示例树：**
```
        1
       /  \
      2    3
     / \   / \
    4   5  6  7
```

**目标结果：**
```
        1 -> NULL
       /  \
      2 -> 3 -> NULL
     / \   / \
    4->5->6->7 -> NULL
```

---

## 二、connect（遍历思路）分析

### 代码逻辑：
```python
def traverse(left_node, right_node):
    if not left_node and not right_node:
        return
    
    # 将每层node两两绑定进行 next 链接
    traverse(left_node.left, left_node.right)      # 连接 4->5
    traverse(left_node.right, right_node.left)     # 连接 5->6 ⭐ 关键！
    traverse(right_node.left, right_node.right)    # 连接 6->7
    left_node.next = right_node                    # 连接 2->3
```

### 执行过程（以第二层为例）：

**初始调用：** `traverse(节点2, 节点3)`

1. **`traverse(节点2.left, 节点2.right)`** → `traverse(4, 5)`
   - 连接 4->5（同一父节点）
   - 递归处理 4 和 5 的子树（都是 None，返回）

2. **`traverse(节点2.right, 节点3.left)`** → `traverse(5, 6)` ⭐
   - **关键：连接不同父节点的相邻节点 5->6**
   - 递归处理 5 和 6 的子树（都是 None，返回）

3. **`traverse(节点3.left, 节点3.right)`** → `traverse(6, 7)`
   - 连接 6->7（同一父节点）
   - 递归处理 6 和 7 的子树（都是 None，返回）

4. **`left_node.next = right_node`** → `节点2.next = 节点3`
   - 连接 2->3

### ✅ 优点：
- **核心思路：将二叉树抽象成三叉树**
- 每个 `traverse(left, right)` 处理一对相邻节点
- 通过 `traverse(left.right, right.left)` 连接不同父节点的相邻节点
- 完美处理了所有情况

---

## 三、connect2（BFS思路）问题分析

### 当前代码：
```python
def connect2(root):
    q = deque()
    q.append(root)
    
    while len(q) > 0:
        size = len(q)
        
        for _ in range(size):
            cur = q.popleft()
            
            if cur.left and cur.right:
                q.append(cur.left)
                q.append(cur.right)
                cur.left.next = cur.right  # ⚠️ 只连接同一父节点的子节点
        
        lv += 1
```

### ❌ 问题：

**执行过程（第二层）：**
```
队列状态：[2, 3]
处理节点2：
  - 连接 2.left.next = 2.right → 4->5 ✅
  - 入队：4, 5
处理节点3：
  - 连接 3.left.next = 3.right → 6->7 ✅
  - 入队：6, 7
```

**缺失的连接：**
- ❌ **5->6 没有连接！**（不同父节点的相邻节点）

### 问题根源：
- 只处理了**同一父节点**的两个子节点
- 没有处理**不同父节点**的相邻节点（如节点5和节点6）

---

## 四、connect2 修复方案

### **方案1：在同一层循环中连接相邻节点（推荐）**

**核心思路：** 在遍历同一层时，将当前节点连接到队列中的下一个节点

```python
def connect2(root):
    if not root:
        return root
    
    q = deque([root])
    
    while q:
        size = len(q)
        
        for i in range(size):
            cur = q.popleft()
            
            # ⭐ 关键：连接当前节点到下一个节点（同一层）
            if i < size - 1:  # 不是该层最后一个节点
                cur.next = q[0]  # 连接到队列中的下一个节点
            
            # 将子节点入队
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
    
    return root
```

**执行过程（第二层）：**
```
初始队列：[2, 3]
i=0, 处理节点2：
  - cur.next = q[0] → 2.next = 3 ✅
  - 入队：4, 5
  队列：[3, 4, 5]
i=1, 处理节点3：
  - cur.next = q[0] → 3.next = 4 ❌ 错误！4是下一层的节点
```

**问题：** 队列中混合了当前层和下一层的节点！

### **方案2：先收集当前层所有节点，再连接（正确）**

```python
def connect2(root):
    if not root:
        return root
    
    q = deque([root])
    
    while q:
        size = len(q)
        level_nodes = []  # 收集当前层的所有节点
        
        # 先收集当前层节点
        for _ in range(size):
            cur = q.popleft()
            level_nodes.append(cur)
            
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        
        # 连接当前层的相邻节点
        for i in range(len(level_nodes) - 1):
            level_nodes[i].next = level_nodes[i + 1]
        # 最后一个节点的 next 保持为 None
    
    return root
```

**执行过程（第二层）：**
```
初始队列：[2, 3]
收集阶段：
  - level_nodes = [2, 3]
  - 入队：4, 5, 6, 7
连接阶段：
  - level_nodes[0].next = level_nodes[1] → 2.next = 3 ✅
```

**执行过程（第三层）：**
```
队列：[4, 5, 6, 7]
收集阶段：
  - level_nodes = [4, 5, 6, 7]
连接阶段：
  - 4.next = 5 ✅
  - 5.next = 6 ✅（不同父节点的相邻节点！）
  - 6.next = 7 ✅
```

### **方案3：在循环中直接连接（优化版，O(1)空间）**

```python
def connect2(root):
    if not root:
        return root
    
    q = deque([root])
    
    while q:
        size = len(q)
        prev = None  # 前一个节点
        
        for _ in range(size):
            cur = q.popleft()
            
            # 连接前一个节点到当前节点
            if prev:
                prev.next = cur
            prev = cur
            
            # 将子节点入队
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        
        # 该层最后一个节点的 next 已经是 None（默认值）
    
    return root
```

**执行过程（第二层）：**
```
队列：[2, 3]
i=0, 处理节点2：
  - prev = None，不连接
  - prev = 2
  - 入队：4, 5
i=1, 处理节点3：
  - prev.next = cur → 2.next = 3 ✅
  - prev = 3
  - 入队：6, 7
```

**执行过程（第三层）：**
```
队列：[4, 5, 6, 7]
i=0, 处理节点4：
  - prev = None，不连接
  - prev = 4
i=1, 处理节点5：
  - prev.next = cur → 4.next = 5 ✅
  - prev = 5
i=2, 处理节点6：
  - prev.next = cur → 5.next = 6 ✅（不同父节点！）
  - prev = 6
i=3, 处理节点7：
  - prev.next = cur → 6.next = 7 ✅
  - prev = 7
```

---

## 五、方案对比

| 方案 | 空间复杂度 | 代码复杂度 | 推荐度 |
|------|-----------|-----------|--------|
| **方案2（收集后连接）** | O(n) - 存储每层节点 | 简单清晰 | ⭐⭐⭐ |
| **方案3（prev指针）** | O(1) - 只用一个指针 | 稍复杂 | ⭐⭐⭐⭐ |

### **推荐：方案3（prev指针）**
- ✅ O(1) 额外空间（除了队列本身）
- ✅ 代码简洁
- ✅ 逻辑清晰：用 `prev` 跟踪前一个节点

---

## 六、完整修复代码

### **方案3（推荐）：**
```python
def connect2(root: 'Optional[Node]') -> 'Optional[Node]':
    if not root:
        return root
    
    q = deque([root])
    
    while q:
        size = len(q)
        prev = None  # 前一个节点
        
        for _ in range(size):
            cur = q.popleft()
            
            # 连接前一个节点到当前节点
            if prev:
                prev.next = cur
            prev = cur
            
            # 将子节点入队
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
    
    return root
```

### **关键修改点：**
1. ✅ 添加 `prev` 变量跟踪前一个节点
2. ✅ 在循环中连接 `prev.next = cur`
3. ✅ 每层循环开始时重置 `prev = None`
4. ✅ 这样就能连接不同父节点的相邻节点（如 5->6）

---

## 七、总结

### **connect（遍历思路）的核心：**
- 将二叉树抽象成三叉树
- 通过 `traverse(left.right, right.left)` 连接不同父节点的相邻节点
- 递归处理，逻辑优雅

### **connect2（BFS思路）的关键：**
- 需要在**同一层**的节点之间建立连接
- 不能只连接同一父节点的子节点
- 必须连接**所有相邻节点**（包括不同父节点的）

### **修复方法：**
- 使用 `prev` 指针跟踪前一个节点
- 在遍历同一层时，将 `prev.next = cur`
- 这样自然处理了所有相邻节点的连接






















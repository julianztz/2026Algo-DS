# zigzagLevelOrder 问题分析

## 你的代码

```python
def zigzagLevelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    res = []
    q = deque([root])
    switch = -1
    
    while q:
        cur_level_res = []
        for _ in range(len(q)):
            cur = q.popleft()

            if switch:  # switch = -1 或 1（都是真值）
                if cur.left:
                    q.append(cur.left)
                if cur.right:
                    q.append(cur.right)
            else:  # 永远不会执行！
                if cur.right:
                    q.append(cur.right)
                if cur.left:
                    q.append(cur.left)

            cur_level_res.append(cur.val)
        switch *= -1
        res.append(cur_level_res)

    return res
```

---

## 问题分析

### **问题1：switch 逻辑错误**

```python
switch = -1  # 初始值
# ...
if switch:  # -1 是真值，1 也是真值
    # 总是执行这个分支
else:  # 永远不会执行！
    # 永远不会执行
switch *= -1  # -1 → 1 → -1 → 1 ...
```

**问题**：
- `switch = -1` 是真值
- `switch = 1` 也是真值
- `switch = 0` 才是假值，但你的代码永远不会让 `switch` 变成 0
- 所以 `else` 分支永远不会执行！

**修复**：应该用布尔值或 0/1
```python
switch = False  # 或 switch = 0
# 或
left_to_right = True
```

---

### **问题2：核心逻辑错误（更严重）**

**关键理解**：改变 enqueue 顺序**不能**改变当前层的遍历顺序！

#### **你的思路分析**

假设树结构：
```
    1
   / \
  2   3
 / \ / \
4  5 6  7
```

**你的代码执行过程**：

1. **第1层**：
   - 队列：`[1]`
   - `switch = -1`（真）
   - `popleft()` → `1`
   - enqueue：先 left 后 right → `[2, 3]`
   - 输出：`[1]` ✅

2. **第2层**：
   - 队列：`[2, 3]`（从左到右）
   - `switch = 1`（真）
   - `popleft()` → `2`，enqueue：先 left 后 right → `[3, 4, 5]`
   - `popleft()` → `3`，enqueue：先 left 后 right → `[4, 5, 6, 7]`
   - 输出：`[2, 3]` ❌（应该是 `[3, 2]`）

3. **第3层**：
   - 队列：`[4, 5, 6, 7]`（从左到右）
   - `switch = -1`（真）
   - 输出：`[4, 5, 6, 7]` ✅

**问题**：
- 改变 enqueue 顺序只能影响**下一层**的顺序
- **当前层**的节点已经在队列中了，`popleft()` 的顺序是固定的
- 无法通过改变 enqueue 顺序来实现 zigzag

---

## 正确的思路

### **方法1：改变当前层的读取顺序（推荐）**

```python
def zigzagLevelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    res = []
    q = deque([root])
    left_to_right = True  # 控制当前层的读取方向

    while q:
        level_size = len(q)
        cur_level_res = []
        
        # 处理当前层的所有节点
        for _ in range(level_size):
            cur = q.popleft()
            cur_level_res.append(cur.val)
            
            # 总是按 left → right 顺序 enqueue（为下一层准备）
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        
        # 根据方向决定是否反转当前层的结果
        if not left_to_right:
            cur_level_res.reverse()  # 或 cur_level_res = cur_level_res[::-1]
        
        res.append(cur_level_res)
        left_to_right = not left_to_right  # 切换方向

    return res
```

**关键点**：
- ✅ 总是按 left → right 顺序 enqueue（保持队列顺序一致）
- ✅ 根据 `left_to_right` 决定是否反转当前层的结果
- ✅ 简单、清晰、高效

---

### **方法2：改变 enqueue 顺序 + 使用双端队列**

```python
def zigzagLevelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    res = []
    q = deque([root])
    left_to_right = True

    while q:
        level_size = len(q)
        cur_level_res = []
        
        for _ in range(level_size):
            if left_to_right:
                # 从左到右：从左边 pop，从右边 append
                cur = q.popleft()
                if cur.left:
                    q.append(cur.left)
                if cur.right:
                    q.append(cur.right)
            else:
                # 从右到左：从右边 pop，从左边 append
                cur = q.pop()
                if cur.right:
                    q.appendleft(cur.right)
                if cur.left:
                    q.appendleft(cur.left)
            
            cur_level_res.append(cur.val)
        
        res.append(cur_level_res)
        left_to_right = not left_to_right

    return res
```

**关键点**：
- ✅ 利用 `deque` 的双端操作
- ✅ 从左到右：`popleft()` + `append()`
- ✅ 从右到左：`pop()` + `appendleft()`
- ⚠️ 但要注意 enqueue 顺序要反过来（先 right 后 left）

---

### **方法3：使用两个栈（DFS 思路）**

```python
def zigzagLevelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    res = []
    stack1 = [root]  # 当前层
    stack2 = []      # 下一层
    left_to_right = True

    while stack1:
        cur_level_res = []
        
        while stack1:
            cur = stack1.pop()
            cur_level_res.append(cur.val)
            
            if left_to_right:
                # 下一层从左到右，所以先 push left 后 push right
                if cur.left:
                    stack2.append(cur.left)
                if cur.right:
                    stack2.append(cur.right)
            else:
                # 下一层从右到左，所以先 push right 后 push left
                if cur.right:
                    stack2.append(cur.right)
                if cur.left:
                    stack2.append(cur.left)
        
        res.append(cur_level_res)
        stack1, stack2 = stack2, stack1  # 交换栈
        left_to_right = not left_to_right

    return res
```

**关键点**：
- ✅ 使用栈（LIFO）自然实现反向
- ✅ 逻辑清晰
- ⚠️ 需要两个栈，空间复杂度略高

---

## 对比总结

| 方法 | 时间复杂度 | 空间复杂度 | 代码复杂度 | 推荐度 |
|------|-----------|-----------|-----------|--------|
| **方法1：反转结果** | O(n) | O(n) | ⭐ 简单 | ⭐⭐⭐⭐⭐ |
| **方法2：双端队列** | O(n) | O(n) | ⭐⭐ 中等 | ⭐⭐⭐⭐ |
| **方法3：双栈** | O(n) | O(n) | ⭐⭐ 中等 | ⭐⭐⭐ |

---

## 你的代码的问题总结

1. **❌ switch 逻辑错误**：`-1` 和 `1` 都是真值，`else` 永远不会执行
2. **❌ 核心逻辑错误**：改变 enqueue 顺序无法改变当前层的遍历顺序
3. **❌ 无法实现 zigzag**：当前层的节点已经在队列中，顺序固定

---

## 修复建议

**推荐使用方法1**（最简单、最清晰）：

```python
def zigzagLevelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    res = []
    q = deque([root])
    left_to_right = True

    while q:
        level_size = len(q)
        cur_level_res = []
        
        for _ in range(level_size):
            cur = q.popleft()
            cur_level_res.append(cur.val)
            
            # 总是按 left → right 顺序 enqueue
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        
        # 根据方向决定是否反转
        if not left_to_right:
            cur_level_res.reverse()
        
        res.append(cur_level_res)
        left_to_right = not left_to_right

    return res
```

**关键改进**：
1. ✅ 使用布尔值 `left_to_right` 而不是 `-1/1`
2. ✅ 总是按 left → right 顺序 enqueue
3. ✅ 根据方向决定是否反转当前层的结果
4. ✅ 逻辑清晰，易于理解





















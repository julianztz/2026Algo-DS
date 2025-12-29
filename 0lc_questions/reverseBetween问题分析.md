# reverseBetween 问题分析

## 一、你的实现分析

### 代码逻辑
```python
def reverseBetween(self, head, left, right):
    # 找到 prev（第 left-1 个节点）
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    
    cur = prev.next  # 要反转部分的第一个节点
    
    # 循环 right - left 次
    for _ in range(right - left):
        next_temp = cur.next
        cur.next = next_temp.next
        next_temp.next = cur
        prev.next = next_temp
```

**核心思路**：头插法 - 每次将 `cur.next` 移到 `prev.next` 的位置

---

## 二、测试用例分析

### 测试用例1：[1,2,3,4], left=2, right=3 ✓

**初始状态：**
```
1 -> 2 -> 3 -> 4 -> None
^    ^    ^
prev cur  next_temp
```

**执行过程：**
- prev 指向节点 1
- cur 指向节点 2
- 循环 1 次（right - left = 1）：

**第1次循环：**
```
next_temp = cur.next = 节点 3
cur.next = next_temp.next = 节点 4  (2 -> 4)
next_temp.next = cur = 节点 2        (3 -> 2)
prev.next = next_temp = 节点 3       (1 -> 3)
```

**结果：**
```
1 -> 3 -> 2 -> 4 -> None
```

**验证：** ✓ 正确！节点 2,3 被反转了

---

### 测试用例2：[1,2,3,4,5], left=2, right=4 ❌

**初始状态：**
```
1 -> 2 -> 3 -> 4 -> 5 -> None
^    ^    ^
prev cur  next_temp
```

**执行过程：**
- prev 指向节点 1
- cur 指向节点 2
- 循环 2 次（right - left = 2）：

**第1次循环：**
```
next_temp = cur.next = 节点 3
cur.next = next_temp.next = 节点 4  (2 -> 4)
next_temp.next = cur = 节点 2        (3 -> 2)
prev.next = next_temp = 节点 3       (1 -> 3)
```

**第1次循环后：**
```
1 -> 3 -> 2 -> 4 -> 5 -> None
^    ^    ^
prev cur  next_temp
     (cur 仍然是节点 2)
```

**第2次循环：**
```
next_temp = cur.next = 节点 4  ⚠️ 问题：cur 还是节点 2，所以 next_temp = 节点 4
cur.next = next_temp.next = 节点 5  (2 -> 5)
next_temp.next = cur = 节点 2        (4 -> 2)
prev.next = next_temp = 节点 4       (1 -> 4)
```

**最终结果：**
```
1 -> 4 -> 2 -> 5 -> None
     ^
     节点 3 丢失了！
```

**问题：** ❌ 节点 3 丢失了！应该是 `1 -> 4 -> 3 -> 2 -> 5`

---

## 三、问题根源分析

### 核心问题

**你的算法使用的是"头插法"反转，但有一个关键问题：**

在每次循环中：
1. `cur` 始终指向**要反转部分的第一个节点**（节点 2）
2. `next_temp = cur.next` 每次都是 `cur` 的下一个节点
3. 但经过第一次循环后，`cur.next` 已经改变了！

**具体问题：**

**第1次循环后：**
- `cur` 仍然指向节点 2
- `cur.next` 现在指向节点 4（不再是节点 3）
- 链表：`1 -> 3 -> 2 -> 4 -> 5`

**第2次循环：**
- `next_temp = cur.next = 节点 4`（跳过了节点 3！）
- 这导致节点 3 被跳过，最终丢失

### 为什么 [1,2,3,4] reverse 2,3 是对的？

因为只循环 1 次，所以不会出现这个问题！

---

## 四、正确的头插法实现

### 方法1：修正你的实现（保持 cur 不变）

**关键修改：** `cur` 始终指向要反转部分的第一个节点，`cur.next` 会不断变化

**你的代码逻辑其实是正确的头插法！** 但让我再仔细检查一下...

等等，让我重新分析。实际上，头插法的正确实现应该是：

```python
def reverseBetween(self, head, left, right):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    # 找到 prev
    for _ in range(left - 1):
        prev = prev.next
    
    cur = prev.next  # 要反转部分的第一个节点
    
    # 头插法：每次将 cur.next 移到 prev.next
    for _ in range(right - left):
        next_temp = cur.next
        cur.next = next_temp.next      # cur 跳过 next_temp
        next_temp.next = prev.next     # next_temp 插入到 prev 后面
        prev.next = next_temp           # 更新 prev.next
```

**关键区别：**
- 你的代码：`next_temp.next = cur`（将 next_temp 指向 cur）
- 正确代码：`next_temp.next = prev.next`（将 next_temp 指向 prev 的下一个）

让我验证一下你的代码逻辑...

实际上，你的代码：
```python
next_temp.next = cur
prev.next = next_temp
```

这意味着：
- `next_temp` 指向 `cur`
- `prev` 指向 `next_temp`

所以结构是：`prev -> next_temp -> cur -> ...`

但问题是，在第二次循环时，`cur.next` 已经改变了，所以 `next_temp = cur.next` 会跳过中间节点。

---

## 五、问题总结

### 你的实现问题

**核心问题：** 在头插法反转中，`cur` 始终指向要反转部分的第一个节点，但 `cur.next` 会不断变化。当循环多次时，`next_temp = cur.next` 会跳过已经被移动的节点。

**具体表现：**
- [1,2,3,4] reverse 2,3：循环 1 次，没问题 ✓
- [1,2,3,4,5] reverse 2,3,4：循环 2 次，第2次循环时 `cur.next` 已经指向节点 4，跳过了节点 3 ❌

### 正确的头插法逻辑

**关键点：**
- `cur` 始终指向要反转部分的第一个节点（不变）
- `cur.next` 会不断变化（指向下一个要处理的节点）
- `next_temp` 每次都是 `cur.next`（当前要插入的节点）
- `next_temp.next` 应该指向 `prev.next`（插入位置的下一个节点），而不是 `cur`

**正确的代码：**
```python
for _ in range(right - left):
    next_temp = cur.next
    cur.next = next_temp.next      # cur 跳过 next_temp
    next_temp.next = prev.next     # ⚠️ 关键：next_temp 指向 prev.next，不是 cur
    prev.next = next_temp           # prev 指向 next_temp
```

**区别：**
- 你的：`next_temp.next = cur` → `prev -> next_temp -> cur -> ...`
- 正确：`next_temp.next = prev.next` → `prev -> next_temp -> (prev.next) -> ...`

---

## 六、手动验证正确逻辑

### [1,2,3,4,5], left=2, right=4

**初始：**
```
1 -> 2 -> 3 -> 4 -> 5
^    ^    ^
prev cur  next_temp
```

**第1次循环（正确逻辑）：**
```
next_temp = 节点 3
cur.next = 节点 4          (2 -> 4)
next_temp.next = prev.next = 节点 2  (3 -> 2)
prev.next = 节点 3          (1 -> 3)
```
**结果：** `1 -> 3 -> 2 -> 4 -> 5`

**第2次循环（正确逻辑）：**
```
next_temp = cur.next = 节点 4
cur.next = 节点 5          (2 -> 5)
next_temp.next = prev.next = 节点 3  (4 -> 3)
prev.next = 节点 4          (1 -> 4)
```
**结果：** `1 -> 4 -> 3 -> 2 -> 5` ✓

**你的代码第2次循环：**
```
next_temp = cur.next = 节点 4
cur.next = 节点 5          (2 -> 5)
next_temp.next = cur = 节点 2  (4 -> 2)  ⚠️ 错误！应该是 4 -> 3
prev.next = 节点 4          (1 -> 4)
```
**结果：** `1 -> 4 -> 2 -> 5` ❌（节点 3 丢失）

---

## 七、问题根源总结

### 核心错误

**你的代码第 69 行：**
```python
next_temp.next = cur  # ❌ 错误
```

**正确应该是：**
```python
next_temp.next = prev.next  # ✅ 正确
```

### 详细分析

**头插法的正确逻辑：**
- `prev.next` 始终指向"当前已反转部分的头部"
- 每次循环，将 `cur.next`（即 `next_temp`）插入到 `prev` 后面
- `next_temp.next` 应该指向**原来的 `prev.next`**（已反转部分的头部），而不是 `cur`

**你的代码问题：**
- `next_temp.next = cur` 让 `next_temp` 指向 `cur`
- 这会导致：`prev -> next_temp -> cur -> ...`
- 但在后续循环中，`cur.next` 已经改变，所以 `next_temp = cur.next` 会跳过中间节点

### 为什么 [1,2,3,4] reverse 2,3 是对的？

**因为只循环 1 次！**
- 第1次循环后，`cur.next` 从节点 3 变成节点 4
- 但只循环 1 次，所以不会用到改变后的 `cur.next`
- 因此不会出现跳过节点的问题

**但 [1,2,3,4,5] reverse 2,3,4 会出错：**
- 第1次循环后，`cur.next` 从节点 3 变成节点 4
- 第2次循环时，`next_temp = cur.next = 节点 4`（跳过了节点 3！）
- 节点 3 被丢失

### 正确的头插法实现

```python
for _ in range(right - left):
    next_temp = cur.next
    cur.next = next_temp.next      # cur 跳过 next_temp
    next_temp.next = prev.next     # ⚠️ 关键：指向 prev.next（已反转部分的头部）
    prev.next = next_temp           # prev 指向 next_temp
```

**关键理解：**
- `prev.next` 是"已反转部分的头部"
- `next_temp` 要插入到 `prev` 后面，所以 `next_temp.next` 应该指向原来的 `prev.next`
- 这样形成：`prev -> next_temp -> (原来的prev.next) -> ...`

### 可视化对比

**你的代码（错误）：**
```
第1次循环后：1 -> 3 -> 2 -> 4 -> 5
              ^    ^    ^
            prev next  cur

第2次循环：
next_temp = cur.next = 4
next_temp.next = cur = 2  ❌ 错误！应该是 3
结果：1 -> 4 -> 2 -> 5  （节点 3 丢失）
```

**正确代码：**
```
第1次循环后：1 -> 3 -> 2 -> 4 -> 5
              ^    ^    ^
            prev next  cur

第2次循环：
next_temp = cur.next = 4
next_temp.next = prev.next = 3  ✅ 正确！
结果：1 -> 4 -> 3 -> 2 -> 5  ✓
```


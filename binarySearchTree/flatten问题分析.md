# Flatten Binary Tree 问题分析

## 一、问题描述

**LC114: Flatten Binary Tree to Linked List**

将二叉树按照前序遍历的顺序展平成链表（右指针指向下一个节点，左指针为 None）。

**示例树：**
```
    1
   / \
  2   3
 / \
4   5
```

**目标结果：**
```
1 -> 2 -> 4 -> 5 -> 3 -> None
```

---

## 二、你的代码分析

### 当前实现：
```python
def flatten(root: Optional[TreeNode]) -> None:
    if not root:
        return 

    flatten(root.left)      # 递归处理左子树
    flatten(root.right)     # 递归处理右子树

    temp_right = root.right
    root.right = root.left    # 左子树 移到右边
    root.right.right = temp_right  # ⚠️ 问题在这里！
    root.left = None
```

---

## 三、问题分析

### **问题1：`root.left` 可能为 None**

**情况：** 如果 `root.left` 是 None，那么：
```python
root.right = root.left  # root.right = None
root.right.right = temp_right  # ❌ AttributeError: 'NoneType' has no attribute 'right'
```

**示例：**
```
    1
     \
      3
```
- `flatten(1.left)` → `flatten(None)` → 返回
- `flatten(1.right)` → `flatten(3)` → 返回
- `root.right = root.left` → `root.right = None`
- `root.right.right` → ❌ 报错！

---

### **问题2：`root.right.right` 不是链表的末尾**

**核心问题：** 即使 `root.left` 存在，`root.right.right = temp_right` 的逻辑也是错误的！

**原因：**
- `root.left` 已经被 `flatten(root.left)` 处理过了
- 所以 `root.left` 现在是一个**链表**（右指针指向下一个节点）
- `root.right = root.left` 后，`root.right` 是这个链表的**头节点**
- `root.right.right` 是链表的**第二个节点**，不是最后一个节点！

**示例：**
```
初始树：
    1
   / \
  2   3
 / \
4   5

执行过程：
1. flatten(2) 处理左子树：
   - flatten(4) → 4 (已经是叶子节点)
   - flatten(5) → 5 (已经是叶子节点)
   - 2.right = 4, 4.right = 5, 2.left = None
   - 结果：2 -> 4 -> 5 -> None

2. flatten(3) 处理右子树：
   - 3 已经是叶子节点，不变
   - 结果：3 -> None

3. 回到节点 1：
   - temp_right = 3
   - root.right = root.left → 1.right = 2
   - root.right.right = temp_right → 2.right = 3 ❌
   - 结果：1 -> 2 -> 3 -> None
   
   但是 4 和 5 丢失了！❌
```

**正确的结构应该是：**
```
1 -> 2 -> 4 -> 5 -> 3 -> None
```

**问题：** `root.right.right = temp_right` 覆盖了原来链表的后续节点！

---

## 四、正确的分治思路

### **核心思想：**
1. 递归处理左右子树（让它们都变成链表）
2. **找到左子树链表的最后一个节点**
3. 将右子树链表连接到左子树链表的末尾
4. 将左子树链表作为新的右子树

### **修复后的代码：**

```python
def flatten(root: Optional[TreeNode]) -> None:
    if not root:
        return 

    # 1. 递归处理左右子树
    flatten(root.left)
    flatten(root.right)

    # 2. 保存右子树（已经是链表）
    temp_right = root.right
    
    # 3. 将左子树（已经是链表）移到右边
    root.right = root.left
    root.left = None
    
    # 4. ⭐ 关键：找到左子树链表的最后一个节点
    # 然后连接右子树链表
    if root.right:  # 如果左子树存在
        # 找到左子树链表的最后一个节点
        last = root.right
        while last.right:  # 沿着右指针走到末尾
            last = last.right
        # 将右子树链表连接到左子树链表的末尾
        last.right = temp_right
    else:
        # 如果左子树不存在，右子树保持不变
        root.right = temp_right
```

---

## 五、执行过程示例

### **示例树：**
```
    1
   / \
  2   3
 / \
4   5
```

### **执行过程：**

**1. flatten(1)：**
```
调用 flatten(2) 和 flatten(3)
```

**2. flatten(2)：**
```
调用 flatten(4) 和 flatten(5)
- flatten(4)：叶子节点，不变
- flatten(5)：叶子节点，不变

处理节点 2：
- temp_right = None (2.right)
- 2.right = 4 (2.left)
- 2.left = None
- 找到 4 的末尾（4.right = None）
- 4.right = None (temp_right)
- 结果：2 -> 4 -> 5 -> None
```

**3. flatten(3)：**
```
叶子节点，不变
结果：3 -> None
```

**4. 回到 flatten(1)：**
```
- temp_right = 3
- 1.right = 2 (1.left)
- 1.left = None
- 找到 2 链表的末尾：
  - last = 2
  - last = 2.right = 4
  - last = 4.right = 5
  - last.right = None，停止
- 5.right = 3 (temp_right)
- 结果：1 -> 2 -> 4 -> 5 -> 3 -> None ✅
```

---

## 六、更简洁的写法

### **方法1：返回链表的最后一个节点**

```python
def flatten(root: Optional[TreeNode]) -> None:
    def flatten_helper(node):
        if not node:
            return None
        
        # 如果是叶子节点，返回自己
        if not node.left and not node.right:
            return node
        
        # 递归处理左右子树
        left_last = flatten_helper(node.left)
        right_last = flatten_helper(node.right)
        
        # 保存右子树
        temp_right = node.right
        
        # 将左子树移到右边
        if node.left:
            node.right = node.left
            node.left = None
            # 将右子树连接到左子树链表的末尾
            if left_last:
                left_last.right = temp_right
        
        # 返回链表的最后一个节点
        if right_last:
            return right_last
        elif left_last:
            return left_last
        else:
            return node
    
    flatten_helper(root)
```

### **方法2：简化版（推荐）**

```python
def flatten(root: Optional[TreeNode]) -> None:
    if not root:
        return 

    flatten(root.left)
    flatten(root.right)

    # 保存右子树
    temp_right = root.right
    
    # 将左子树移到右边
    root.right = root.left
    root.left = None
    
    # 找到新右子树链表的最后一个节点
    # 然后连接原右子树
    if root.right:
        last = root.right
        while last.right:
            last = last.right
        last.right = temp_right
```

---

## 七、问题总结

### **你的代码的问题：**

1. ❌ **没有检查 `root.left` 是否为 None**
   - 当左子树为空时，`root.right.right` 会报错

2. ❌ **`root.right.right = temp_right` 逻辑错误**
   - `root.right` 是左子树链表的头节点
   - `root.right.right` 是链表的第二个节点，不是最后一个
   - 这样会覆盖掉链表的后续节点

### **正确的逻辑：**

1. ✅ 递归处理左右子树（让它们变成链表）
2. ✅ 将左子树链表移到右边
3. ✅ **找到左子树链表的最后一个节点**（关键！）
4. ✅ 将右子树链表连接到左子树链表的末尾

### **关键点：**

- 必须找到左子树链表的**最后一个节点**，而不是第二个节点
- 需要处理 `root.left` 为 None 的情况
- 分治思路是正确的，但连接逻辑需要修正

---

## 八、时间复杂度分析

- **时间复杂度：** O(n²) - 最坏情况下，每次找最后一个节点需要 O(n)
- **空间复杂度：** O(h) - 递归栈深度，h 为树的高度

**优化：** 可以在递归时返回最后一个节点，避免重复遍历，优化到 O(n)






















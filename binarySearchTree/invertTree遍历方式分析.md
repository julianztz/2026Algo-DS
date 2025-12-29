# invertTree 遍历方式分析

## 一、当前代码分析

你的 `invertTree1` 当前实现是**前序遍历**：
```python
def traverse(node):
    if not node:
        return
    res.append(node.val)  # 前序位置
    node.left, node.right = node.right, node.left  # 交换
    traverse(node.left)   # 遍历左（实际是原来的右）
    traverse(node.right)  # 遍历右（实际是原来的左）
```

## 二、三种遍历方式分析

### 1. **前序遍历（当前实现）✅ 正确**

**执行流程：**
```
访问节点 1 -> 交换左右 -> 遍历左(原右) -> 遍历右(原左)
```

**示例树：**
```
    1
   / \
  2   3
 / \
4   5
```

**执行过程：**
1. 访问节点 1：交换 → `1: {left=3, right=2}`
2. 遍历左子树（原右子树 3）：访问节点 3 → 交换 → `3: {left=None, right=None}`
3. 遍历右子树（原左子树 2）：访问节点 2 → 交换 → `2: {left=5, right=4}`
4. 继续遍历节点 2 的子树...

**结果：** ✅ 每个节点都被正确交换一次

---

### 2. **后序遍历 ✅ 正确**

**修改后的代码逻辑：**
```python
def traverse(node):
    if not node:
        return
    traverse(node.left)   # 先遍历左
    traverse(node.right)  # 再遍历右
    node.left, node.right = node.right, node.left  # 后序位置交换
```

**执行流程：**
```
遍历左 -> 遍历右 -> 访问节点 -> 交换左右
```

**执行过程（自底向上）：**
1. 先遍历到底层（节点 4, 5, 3）
2. 从底层开始交换：
   - 节点 4：交换（无子树，不变）
   - 节点 5：交换（无子树，不变）
   - 节点 2：交换 → `2: {left=5, right=4}`
   - 节点 3：交换（无子树，不变）
   - 节点 1：交换 → `1: {left=3, right=2}`

**结果：** ✅ 每个节点都被正确交换一次（自底向上）

---

### 3. **中序遍历 ⚠️ 有问题！**

**如果直接在中序位置交换：**
```python
def traverse(node):
    if not node:
        return
    traverse(node.left)   # 遍历左子树（未交换）
    node.left, node.right = node.right, node.left  # 中序位置交换
    traverse(node.right)  # 遍历右子树（但已经交换了！）
```

**问题分析：**

**示例树：**
```
    1
   / \
  2   3
 / \
4   5
```

**执行过程：**
1. 遍历节点 1 的左子树（节点 2）：
   - 遍历节点 2 的左子树（节点 4）→ 完成
   - **在节点 2 处交换** → `2: {left=5, right=4}`
   - 遍历节点 2 的右子树（但此时"右"是原来的左 4）→ **重复遍历节点 4！**

2. 回到节点 1：
   - **在节点 1 处交换** → `1: {left=3, right=2}`
   - 遍历节点 1 的右子树（但此时"右"是原来的左 2）→ **重复遍历节点 2！**

**问题：**
- ❌ 原来的左子树被遍历了**两次**
- ❌ 原来的右子树可能**没有被遍历**（或遍历不完整）
- ❌ 交换不完整，树结构错误

---

## 三、中序遍历的正确做法

### **方法1：先交换再遍历（类似前序）**

```python
def traverse(node):
    if not node:
        return
    traverse(node.left)   # 遍历左子树（未交换）
    # 关键：在遍历右子树之前交换
    node.left, node.right = node.right, node.left
    traverse(node.right)  # 遍历右子树（已交换，实际是原左）
```

**但这样还是有问题！** 因为：
- 遍历左子树时，左子树内部已经交换过了
- 然后交换当前节点
- 再遍历"右子树"（实际是原左），但原左已经被遍历过了

### **方法2：遍历右子树时用原左的引用（推荐）**

```python
def traverse(node):
    if not node:
        return
    traverse(node.left)   # 遍历左子树
    # 保存原右子树的引用
    original_right = node.right
    node.left, node.right = node.right, node.left  # 交换
    traverse(original_right)  # 遍历原右子树（用保存的引用）
```

**执行过程：**
1. 遍历节点 1 的左子树（节点 2）：
   - 遍历节点 2 的左子树（节点 4）→ 完成
   - 在节点 2 处：保存原右（节点 5），交换 → `2: {left=5, right=4}`
   - 遍历原右（节点 5）→ 完成

2. 回到节点 1：
   - 在节点 1 处：保存原右（节点 3），交换 → `1: {left=3, right=2}`
   - 遍历原右（节点 3）→ 完成

**结果：** ✅ 每个节点都被正确交换一次，且每个子树都被正确遍历

---

## 四、总结对比

| 遍历方式 | 是否可行 | 关键点 |
|---------|---------|--------|
| **前序** | ✅ 是 | 先交换再遍历，交换后的左右对应原右左 |
| **中序** | ⚠️ 需特殊处理 | 必须保存原右子树引用，交换后用原引用遍历 |
| **后序** | ✅ 是 | 先遍历再交换，自底向上，自然正确 |

### **推荐顺序：**
1. **后序遍历**（最自然，自底向上）
2. **前序遍历**（代码简单，逻辑清晰）
3. **中序遍历**（需要额外处理，不推荐）

### **为什么中序最复杂？**
- 前序：交换 → 遍历，顺序清晰
- 后序：遍历 → 交换，自底向上自然
- 中序：遍历左 → **交换** → 遍历右，但交换后"右"已经变了，需要保存原引用

---

## 五、实际代码对比

### 前序遍历（最简单）
```python
def traverse(node):
    if not node: return
    node.left, node.right = node.right, node.left  # 交换
    traverse(node.left)
    traverse(node.right)
```

### 后序遍历（最自然）
```python
def traverse(node):
    if not node: return
    traverse(node.left)
    traverse(node.right)
    node.left, node.right = node.right, node.left  # 交换
```

### 中序遍历（需要特殊处理）
```python
def traverse(node):
    if not node: return
    traverse(node.left)
    original_right = node.right  # 保存原右
    node.left, node.right = node.right, node.left  # 交换
    traverse(original_right)  # 用原引用遍历
```






















# BST 递归公式构造指南

## 一、递归 vs 迭代：哪种更普遍？

### **总体原则**
- **递归（分治）**：✅ **更普遍、更推荐**
  - 代码更简洁清晰
  - 逻辑更容易理解
  - BST问题天然适合递归（树本身就是递归结构）
  
- **迭代**：特定场景使用
  - 需要手动追踪父节点指针（insert, delete）
  - 需要更精确的控制流程
  - 避免栈溢出（深度很大的树）

### **何时用递归，何时用迭代？**

| 操作 | 推荐方法 | 原因 |
|------|---------|------|
| **search** | 递归 | 逻辑简单，代码清晰 |
| **insert** | 递归 | 利用返回值更新树结构，代码简洁 |
| **delete** | 递归 | 复杂逻辑更容易表达 |
| **validate** | 递归 | 需要传递边界信息，递归更自然 |

---

## 二、BST 递归公式构造的通用框架

### **核心思维模式**

BST 递归的核心是：**将问题分解为"当前节点"和"左右子树"两个子问题**

### **三步法构造递归公式**

#### **步骤1：明确函数定义和返回值**
```python
def solve(root: Optional[TreeNode], ...) -> ReturnType:
    # 函数定义要明确：
    # - 输入：当前子树根节点 + 可能的额外参数（边界值、目标值等）
    # - 输出：该子树的结果
```

**关键问题**：这个函数返回什么？
- 返回节点？ → `Optional[TreeNode]`
- 返回布尔值？ → `bool`
- 返回数值？ → `int`
- 返回整个树？ → `Optional[TreeNode]`（树结构）

#### **步骤2：确定 Base Case（边界情况）**
```python
if not root:
    return base_value  # 空树应该返回什么？
```

**常见 base case：**
- 搜索：`return None`（没找到）
- 验证：`return True`（空树是有效的）
- 插入：`return TreeNode(val)`（创建新节点）
- 删除：`return None`（删除后为空）

#### **步骤3：构造递归公式（利用BST性质）**

**核心模式：**
```python
# 1. 处理当前节点
if root.val == target:
    # 找到目标，处理当前节点
    return handle_current_node(root)

# 2. 利用BST性质选择子树
if root.val > target:
    # 目标在左子树（BST性质：左 < 根 < 右）
    return solve(root.left, ...)
elif root.val < target:
    # 目标在右子树
    return solve(root.right, ...)
```

---

## 三、典型问题的递归公式构造

### **1. Search（搜索）**

#### **问题分析**
- **输入**：根节点 + 目标值
- **输出**：找到的节点或 None
- **子问题**：在左子树或右子树中搜索

#### **递归公式构造**
```python
def searchBST(root, val):
    # Step 1: Base case
    if not root:
        return None  # 空树，没找到
    
    # Step 2: 处理当前节点
    if root.val == val:
        return root  # 找到了！
    
    # Step 3: 利用BST性质选择子树
    if root.val > val:
        return searchBST(root.left, val)  # 只在左子树搜索
    else:  # root.val < val
        return searchBST(root.right, val)  # 只在右子树搜索
```

**关键点**：
- ✅ 利用BST性质：只需要搜索一个子树
- ✅ 找到后立即返回，不需要继续搜索
- ✅ 返回值直接就是子问题的结果

---

### **2. Insert（插入）**

#### **问题分析**
- **输入**：根节点 + 要插入的值
- **输出**：插入后的子树根节点
- **子问题**：在左子树或右子树中插入，然后更新树结构

#### **递归公式构造**
```python
def insertIntoBST(root, val):
    # Step 1: Base case
    if not root:
        return TreeNode(val)  # 空位置，创建新节点
    
    # Step 2: 利用BST性质选择插入位置
    if root.val > val:
        # 插入到左子树，然后用结果更新root.left
        root.left = insertIntoBST(root.left, val)
    elif root.val < val:
        # 插入到右子树，然后用结果更新root.right
        root.right = insertIntoBST(root.right, val)
    
    # Step 3: 返回当前根节点（树结构已更新）
    return root
```

**关键点**：
- ✅ **利用返回值更新树结构**：`root.left = insertIntoBST(root.left, val)`
- ✅ 递归返回的是"插入后的子树根节点"
- ✅ 当前节点用子问题的结果更新自己

**思考过程**：
1. "如果要在 root 的左子树插入 val，结果是什么？" → `insertIntoBST(root.left, val)`
2. "这个结果应该放在哪里？" → `root.left = ...`
3. "最后返回什么？" → `return root`（当前树）

---

### **3. Delete（删除）**

#### **问题分析**
- **输入**：根节点 + 要删除的值
- **输出**：删除后的子树根节点
- **子问题**：在左子树或右子树中删除，然后重新组织树结构
- **复杂性**：删除节点有三种情况需要处理

#### **递归公式构造**
```python
def deleteNode(root, key):
    # Step 1: Base case
    if not root:
        return None  # 空树，找不到要删除的节点
    
    # Step 2: 利用BST性质找到要删除的节点
    if root.val > key:
        # 要删除的节点在左子树
        root.left = deleteNode(root.left, key)
        return root
    elif root.val < key:
        # 要删除的节点在右子树
        root.right = deleteNode(root.right, key)
        return root
    else:
        # Step 3: 找到了！处理三种情况
        # 情况1：叶子节点（无子节点）
        if not root.left and not root.right:
            return None  # 删除后为空
        
        # 情况2：只有一个子节点
        if not root.left:
            return root.right  # 返回右子树
        if not root.right:
            return root.left   # 返回左子树
        
        # 情况3：有两个子节点（最复杂）
        # 用右子树的最小值替代当前节点
        successor = findMin(root.right)  # 找到右子树最小值
        root.val = successor.val         # 用successor的值替代
        root.right = deleteNode(root.right, successor.val)  # 删除successor
        return root
```

**关键点**：
- ✅ **利用返回值重组树结构**：`root.left = deleteNode(root.left, key)`
- ✅ 删除后返回"新的子树根节点"（可能是None、左子树、右子树、或重组后的树）
- ✅ 情况3需要先找替代节点，再删除替代节点（递归）

**思考过程**：
1. "如果key在左子树，删除后会变成什么样？" → `deleteNode(root.left, key)` 
2. "这个结果应该替换原来的左子树" → `root.left = ...`
3. "如果要删除的就是root，删除后返回什么？" → 根据子节点情况返回不同的树

---

### **4. Validate（验证BST）**

#### **问题分析**
- **输入**：根节点 + 边界值（min_val, max_val）
- **输出**：是否是有效BST
- **子问题**：验证左子树和右子树都是BST，且满足边界条件

#### **递归公式构造**
```python
def isValidBST(root, min_val=None, max_val=None):
    # Step 1: Base case
    if not root:
        return True  # 空树是有效的BST
    
    # Step 2: 检查当前节点是否满足边界条件
    if min_val is not None and root.val <= min_val:
        return False  # 当前节点 <= 最小值（应该在(min_val, max_val)范围内）
    if max_val is not None and root.val >= max_val:
        return False  # 当前节点 >= 最大值
    
    # Step 3: 递归验证左右子树，并传递新的边界
    # 左子树：最大值限制为root.val（所有左子树节点 < root.val）
    # 右子树：最小值限制为root.val（所有右子树节点 > root.val）
    return (isValidBST(root.left, min_val, root.val) and 
            isValidBST(root.right, root.val, max_val))
```

**关键点**：
- ✅ **传递边界信息**：通过参数传递约束条件
- ✅ 左子树继承上边界，右子树继承下边界
- ✅ 子问题的结果用 `and` 组合（都要满足）

**思考过程**：
1. "当前节点需要满足什么条件？" → 在 (min_val, max_val) 范围内
2. "左子树的约束是什么？" → (min_val, root.val)
3. "右子树的约束是什么？" → (root.val, max_val)
4. "整个树有效需要什么？" → 当前节点有效 AND 左子树有效 AND 右子树有效

---

## 四、构造递归公式的通用模板

### **模板1：搜索类问题（返回节点）**
```python
def searchBST(root, target):
    # Base case
    if not root:
        return None
    
    # 处理当前节点
    if root.val == target:
        return root
    
    # 利用BST性质选择子树
    if root.val > target:
        return searchBST(root.left, target)
    else:
        return searchBST(root.right, target)
```

### **模板2：修改树结构类问题（返回树）**
```python
def modifyBST(root, ...):
    # Base case
    if not root:
        return base_tree  # None 或 TreeNode(...)
    
    # 利用BST性质选择子树并修改
    if root.val > condition:
        root.left = modifyBST(root.left, ...)
    elif root.val < condition:
        root.right = modifyBST(root.right, ...)
    else:
        # 处理当前节点
        handle_current_node(root, ...)
    
    return root  # 返回修改后的树
```

### **模板3：验证类问题（返回布尔值）**
```python
def validateBST(root, constraint1, constraint2):
    # Base case
    if not root:
        return True
    
    # 检查当前节点是否满足约束
    if not check_constraint(root, constraint1, constraint2):
        return False
    
    # 递归验证子树（传递新的约束）
    new_constraint1 = update_constraint1(root, constraint1)
    new_constraint2 = update_constraint2(root, constraint2)
    
    return (validateBST(root.left, constraint1, new_constraint2) and
            validateBST(root.right, new_constraint1, constraint2))
```

---

## 五、构造递归公式的思考流程

### **流程1：从问题到函数定义**
```
问题：在BST中搜索值val
  ↓
函数应该做什么？搜索
  ↓
输入是什么？root（当前子树） + val（目标值）
  ↓
输出是什么？找到的节点（TreeNode）或None
  ↓
函数签名：def searchBST(root, val) -> Optional[TreeNode]
```

### **流程2：从函数定义到Base Case**
```
函数：searchBST(root, val) -> Optional[TreeNode]
  ↓
空树情况：root = None
  ↓
空树应该返回什么？None（没找到）
  ↓
Base case: if not root: return None
```

### **流程3：从Base Case到递归公式**
```
Base case已确定
  ↓
当前节点等于目标吗？
  ├─ 是 → return root（找到了）
  └─ 否 → 继续搜索
      ↓
    利用BST性质：val在左子树还是右子树？
    ├─ root.val > val → 在左子树
    │   ↓
    │  递归：searchBST(root.left, val)
    │   ↓
    │  返回什么？直接返回子问题的结果
    │
    └─ root.val < val → 在右子树
        ↓
        递归：searchBST(root.right, val)
        ↓
        返回什么？直接返回子问题的结果
```

### **流程4：验证递归公式**
```
1. 递归会终止吗？
   ✅ 每次递归都会进入更小的子树，最终到达None

2. 返回值正确吗？
   ✅ 找到时返回节点，找不到返回None

3. 利用了BST性质吗？
   ✅ 只搜索一个子树，而不是两个
```

---

## 六、常见陷阱和解决方案

### **陷阱1：忘记更新树结构**

❌ **错误**：
```python
def insertIntoBST(root, val):
    if not root:
        return TreeNode(val)
    if root.val > val:
        insertIntoBST(root.left, val)  # ❌ 没有接收返回值
    return root  # ❌ 树没有被更新
```

✅ **正确**：
```python
def insertIntoBST(root, val):
    if not root:
        return TreeNode(val)
    if root.val > val:
        root.left = insertIntoBST(root.left, val)  # ✅ 用返回值更新
    return root
```

**解决**：记住！修改树结构的递归，**必须用返回值更新**：`root.left = recursive_call(...)`

---

### **陷阱2：没有利用BST性质**

❌ **错误**：
```python
def searchBST(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    # ❌ 左右都搜索，浪费
    left = searchBST(root.left, val)
    if left:
        return left
    return searchBST(root.right, val)
```

✅ **正确**：
```python
def searchBST(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    # ✅ 只搜索一个子树
    if root.val > val:
        return searchBST(root.left, val)
    else:
        return searchBST(root.right, val)
```

**解决**：利用BST的**有序性**，根据当前节点值决定搜索方向

---

### **陷阱3：Base Case返回错误**

❌ **错误**：
```python
def insertIntoBST(root, val):
    if not root:
        return None  # ❌ 应该创建新节点
    ...
```

✅ **正确**：
```python
def insertIntoBST(root, val):
    if not root:
        return TreeNode(val)  # ✅ 创建新节点
    ...
```

**解决**：思考"空树情况下，这个操作应该返回什么？"

---

### **陷阱4：返回值类型不一致**

❌ **错误**：
```python
def deleteNode(root, key):
    if not root:
        return None
    if root.val > key:
        deleteNode(root.left, key)  # ❌ 没有返回
        return root
    ...
```

✅ **正确**：
```python
def deleteNode(root, key):
    if not root:
        return None
    if root.val > key:
        root.left = deleteNode(root.left, key)  # ✅ 返回并更新
        return root
    ...
```

**解决**：确保所有代码路径都有返回值，且类型一致

---

## 七、实战演练：从问题到代码

### **练习1：BST中的最低公共祖先（LCA）**

**问题**：给定BST和两个节点p、q，找到它们的LCA

**思考过程**：

1. **函数定义**
   - 输入：root（当前子树）、p、q（两个目标值）
   - 输出：LCA节点（TreeNode）或None

2. **Base Case**
   - 空树：`return None`

3. **递归公式**
   ```
   如果p和q都在左子树 → 在左子树找LCA
   如果p和q都在右子树 → 在右子树找LCA
   如果p和q分别在左右子树 → 当前root就是LCA
   ```

4. **代码实现**
```python
def lowestCommonAncestor(root, p, q):
    if not root:
        return None
    
    # 利用BST性质：比较值的大小
    if root.val > p.val and root.val > q.val:
        # 都在左子树
        return lowestCommonAncestor(root.left, p, q)
    elif root.val < p.val and root.val < q.val:
        # 都在右子树
        return lowestCommonAncestor(root.right, p, q)
    else:
        # p和q分别在左右子树，或者root就是p或q
        return root
```

---

### **练习2：BST中第K小的元素**

**问题**：找到BST中第K小的元素（1-indexed）

**思考过程**：

1. **函数定义**
   - 输入：root（当前子树）、k（第K小）
   - 输出：第K小的节点值
   - 难点：需要知道当前节点的排名

2. **方法1：中序遍历（遍历思路）**
```python
def kthSmallest(root, k):
    rank = 0
    result = None
    
    def inorder(node):
        nonlocal rank, result
        if not node:
            return
        inorder(node.left)  # 左
        rank += 1           # 中：当前节点
        if rank == k:
            result = node.val
            return
        inorder(node.right) # 右
    
    inorder(root)
    return result
```

3. **方法2：分治思路（计算左子树节点数）**
```python
def kthSmallest(root, k):
    # 计算左子树节点数
    def countNodes(node):
        if not node:
            return 0
        return 1 + countNodes(node.left) + countNodes(node.right)
    
    left_count = countNodes(root.left)
    
    if left_count == k - 1:
        return root.val  # 当前节点就是第K小
    elif left_count >= k:
        return kthSmallest(root.left, k)  # 在左子树
    else:
        return kthSmallest(root.right, k - left_count - 1)  # 在右子树
```

---

## 八、总结

### **递归公式构造的黄金法则**

1. **明确函数定义**：输入什么？返回什么？
2. **确定Base Case**：空树应该返回什么？
3. **利用BST性质**：根据当前节点值决定递归方向
4. **利用返回值**：修改树结构时，用返回值更新
5. **组合子问题**：用逻辑运算符（and, or）或直接返回

### **递归 vs 迭代的选择**

- **优先用递归**：逻辑清晰，代码简洁
- **特殊场景用迭代**：需要精确控制、避免栈溢出

### **记忆要点**

- ✅ **搜索类**：`return searchBST(left/right, target)`（直接返回）
- ✅ **插入类**：`root.left/right = insertIntoBST(...)`（更新树结构）
- ✅ **删除类**：`root.left/right = deleteNode(...)`（重组树结构）
- ✅ **验证类**：`return validate(left) and validate(right)`（组合结果）

---

## 九、扩展：递归公式的数学表达

### **Search的递归公式**
```
searchBST(root, val) = {
    None,                           if root = None
    root,                           if root.val = val
    searchBST(root.left, val),      if root.val > val
    searchBST(root.right, val),     if root.val < val
}
```

### **Insert的递归公式**
```
insertIntoBST(root, val) = {
    TreeNode(val),                      if root = None
    root with root.left updated,        if root.val > val
    root with root.right updated,       if root.val < val
    root,                               if root.val = val (通常BST不允许重复)
}
```

### **Delete的递归公式**
```
deleteNode(root, key) = {
    None,                           if root = None
    root.left,                      if root.val = key and root.right = None
    root.right,                     if root.val = key and root.left = None
    root with val replaced,         if root.val = key and has both children
    root with left updated,         if root.val > key
    root with right updated,        if root.val < key
}
```

---

**记住**：多练习、多思考、多总结！递归公式的构造是一个熟练过程，掌握这个框架后，大部分BST问题都能迎刃而解。




















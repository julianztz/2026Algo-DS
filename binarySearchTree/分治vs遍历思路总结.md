# 二叉树问题：分治 vs 遍历思路总结

## 一、核心区别

### **遍历思路（Traverse）**
- **关注点**：节点间的移动过程，关注"进入"和"离开"节点的时机
- **特点**：使用外部变量（全局变量、闭包）记录状态
- **方向**：Top-down（从上到下）
- **返回值**：通常返回 `None` 或 `void`

### **分治思路（Divide & Conquer）**
- **关注点**：整颗子树，通过子问题的答案推导原问题
- **特点**：充分利用递归函数的返回值
- **方向**：Bottom-up（从下到上）
- **返回值**：返回子树的结果，用于上层计算

---

## 二、题目分类

### **1. invertTree（反转二叉树）**

#### **遍历思路（前序位置）**
```python
def invertTree1(root):
    def traverse(node):
        if not node:
            return
        # 前序位置：交换左右子树
        node.left, node.right = node.right, node.left
        traverse(node.left)
        traverse(node.right)
    
    traverse(root)
    return root
```
- **特点**：从上到下，遇到节点就交换
- **时机**：前序位置（访问节点时）

#### **分治思路（后序位置）**
```python
def invertTree2(root):
    if not root:
        return None
    
    # 先处理子问题
    left_tree = invertTree2(root.left)
    right_tree = invertTree2(root.right)
    
    # 后序位置：利用子树结果
    root.left, root.right = right_tree, left_tree
    return root
```
- **特点**：从下到上，先处理子树，再处理当前节点
- **时机**：后序位置（利用子树结果）

---

### **2. connect（连接同层节点）**

#### **遍历思路（三叉树抽象）**
```python
def connect(root):
    def traverse(left_node, right_node):
        if not left_node and not right_node:
            return
        
        # 将二叉树抽象成三叉树
        traverse(left_node.left, left_node.right)      # 同一父节点
        traverse(left_node.right, right_node.left)      # 不同父节点 ⭐
        traverse(right_node.left, right_node.right)      # 同一父节点
        left_node.next = right_node
    
    traverse(root.left, root.right)
    return root
```
- **特点**：需要处理不同父节点的相邻节点
- **关键**：将二叉树抽象成三叉树，两两绑定遍历
- **为什么不能用分治**：无法分解成独立的子问题（需要跨子树连接）

---

### **3. flatten（展平二叉树）**

#### **分治思路（后序位置）**
```python
def flatten(root):
    if not root:
        return
    
    # 先处理子问题
    flatten(root.left)
    flatten(root.right)
    
    # 后序位置：利用子树结果
    temp_right = root.right
    root.right = root.left
    root.left = None
    
    if root.right:
        left_end = root.right
        while left_end.right:
            left_end = left_end.right
        left_end.right = temp_right
    else:
        root.right = temp_right
```
- **特点**：需要利用左右子树的结果（都是链表）
- **时机**：后序位置（先处理子树，再连接）
- **为什么不能用遍历**：需要知道子树的结构（链表的末尾），遍历无法直接获得

---

### **4. maxDepth（最大深度）**

#### **分治思路（后序位置）**
```python
def maxDepth(root):
    if not root:
        return 0
    
    # 子问题：左右子树的最大深度
    left = maxDepth(root.left)
    right = maxDepth(root.right)
    
    # 后序位置：利用子树结果
    return 1 + max(left, right)
```
- **特点**：父节点的深度 = 子树最大深度 + 1
- **时机**：后序位置（需要子树的结果）

#### **遍历思路（前序进入，后序离开）**
```python
def maxDepthTraverse(root):
    max_depth = 0
    cur_depth = 0
    
    def traverse(node):
        nonlocal max_depth, cur_depth
        if not node:
            return
        
        # 前序位置：进入节点
        cur_depth += 1
        max_depth = max(max_depth, cur_depth)
        
        traverse(node.left)
        traverse(node.right)
        
        # 后序位置：离开节点
        cur_depth -= 1
    
    traverse(root)
    return max_depth
```
- **特点**：记录遍历过程中的深度变化
- **时机**：前序进入，后序离开

---

### **5. minDepth（最小深度）**

#### **遍历思路（前序进入，后序离开）**
```python
def minDepth(root):
    min_depth = float('inf')
    cur_depth = 0
    
    def traverse(node):
        nonlocal min_depth, cur_depth
        if not node:
            return
        
        # 前序位置：进入节点
        cur_depth += 1
        
        # 叶子节点：更新最小深度
        if not node.left and not node.right:
            min_depth = min(min_depth, cur_depth)
        
        traverse(node.left)
        traverse(node.right)
        
        # 后序位置：离开节点
        cur_depth -= 1
    
    traverse(root)
    return min_depth
```
- **特点**：需要遍历所有节点，找到最小深度
- **时机**：前序进入，后序离开

---

### **6. diameterOfBinaryTree（直径）**

#### **混合思路（后序位置 + 全局变量）**
```python
def diameterOfBinaryTree(root):
    max_diameter = 0
    
    def traverse(node):
        nonlocal max_diameter
        if not node:
            return 0
        
        # 子问题：左右子树的最大深度
        left = traverse(node.left)
        right = traverse(node.right)
        
        # 后序位置：利用子树结果
        max_diameter = max(max_diameter, left + right)  # 更新全局变量
        return 1 + max(left, right)  # 返回子树深度
    
    traverse(root)
    return max_diameter
```
- **特点**：结合分治（返回子树深度）和遍历（更新全局变量）
- **时机**：后序位置（需要子树结果，同时更新全局状态）

---

## 三、选择指南

### **何时用遍历思路？**

1. **需要记录遍历过程的状态**
   - 路径问题（记录路径）
   - 深度问题（记录当前深度）
   - 回溯问题（前序进入，后序离开）

2. **需要处理节点间的移动**
   - 连接不同父节点的相邻节点（connect）
   - 需要知道"进入"和"离开"节点的时机

3. **需要全局状态**
   - 更新全局最大值/最小值
   - 收集所有满足条件的节点

**典型问题：**
- minDepth（遍历所有节点）
- connect（处理节点间关系）
- 路径问题（记录路径）

---

### **何时用分治思路？**

1. **需要利用子树的结果**
   - 父节点的答案 = 左右子树答案的组合
   - 需要知道子树的结构或属性

2. **问题可以分解成子问题**
   - 每个子树独立处理
   - 子树的结果可以推导出父节点的结果

3. **后序位置处理**
   - 需要先处理子树，再处理当前节点

**典型问题：**
- maxDepth（父节点深度 = 子树最大深度 + 1）
- flatten（需要子树的结构）
- invertTree（子树反转后，再交换）
- 计算节点数、路径和等

---

## 四、模板总结

### **遍历思路模板**

```python
def traverse_solution(root):
    # 外部变量（全局状态）
    result = []
    global_state = 0
    
    def traverse(node):
        if not node:
            return
        
        # 前序位置：进入节点
        # 处理当前节点
        process_node(node)
        global_state += 1
        
        # 递归处理子树
        traverse(node.left)
        traverse(node.right)
        
        # 后序位置：离开节点
        # 回溯状态
        global_state -= 1
    
    traverse(root)
    return result
```

**关键点：**
- 使用外部变量记录状态
- 前序位置：进入节点时的处理
- 后序位置：离开节点时的回溯

---

### **分治思路模板**

```python
def divide_conquer_solution(root):
    # Base case
    if not root:
        return base_value  # 返回基础值（如 0, None, []）
    
    # 子问题：递归处理左右子树
    left_result = divide_conquer_solution(root.left)
    right_result = divide_conquer_solution(root.right)
    
    # 后序位置：利用子树结果
    # 组合左右子树的结果
    result = combine(left_result, right_result)
    
    return result
```

**关键点：**
- 充分利用返回值
- 后序位置：利用子树结果
- 返回值用于上层计算

---

### **混合思路模板（分治 + 全局变量）**

```python
def hybrid_solution(root):
    global_state = 0  # 全局状态
    
    def traverse(node):
        nonlocal global_state
        if not node:
            return base_value
        
        # 子问题
        left_result = traverse(node.left)
        right_result = traverse(node.right)
        
        # 后序位置：利用子树结果 + 更新全局状态
        current_result = combine(left_result, right_result)
        global_state = update_global(global_state, current_result)
        
        return current_result  # 返回子树结果
    
    traverse(root)
    return global_state
```

**关键点：**
- 结合分治（返回值）和遍历（全局变量）
- 后序位置：同时处理子树结果和全局状态

---

## 五、判断方法

### **快速判断：能否用返回值解决问题？**

**能 → 用分治**
- 父节点的答案 = f(左子树答案, 右子树答案)
- 例如：maxDepth(root) = 1 + max(maxDepth(left), maxDepth(right))

**不能 → 用遍历**
- 需要记录遍历过程的状态
- 需要处理节点间的关系
- 需要全局状态

### **判断流程**

```
1. 问题能否分解成子问题？
   ├─ 否 → 遍历思路
   └─ 是 → 继续

2. 父节点的答案能否由子树答案推导？
   ├─ 否 → 遍历思路（可能需要全局变量）
   └─ 是 → 分治思路

3. 需要记录遍历过程的状态？
   ├─ 是 → 遍历思路
   └─ 否 → 分治思路
```

---

## 六、常见问题分类

### **分治思路（后序位置）**
- ✅ maxDepth（最大深度）
- ✅ minDepth（最小深度，也可用分治）
- ✅ countNodes（节点数）
- ✅ invertTree（反转二叉树）
- ✅ flatten（展平二叉树）
- ✅ isBalanced（平衡二叉树）
- ✅ pathSum（路径和）

### **遍历思路（前序/后序）**
- ✅ minDepth（最小深度，遍历所有节点）
- ✅ connect（连接同层节点）
- ✅ 路径问题（记录路径）
- ✅ 回溯问题（前序进入，后序离开）

### **混合思路（分治 + 全局变量）**
- ✅ diameterOfBinaryTree（直径）
- ✅ maxPathSum（最大路径和）
- ✅ 需要同时返回子树结果和更新全局状态的问题

---

## 七、总结

### **核心区别**

| 特性 | 遍历思路 | 分治思路 |
|------|---------|---------|
| **关注点** | 节点间的移动过程 | 整颗子树 |
| **状态管理** | 外部变量（全局/闭包） | 返回值 |
| **方向** | Top-down | Bottom-up |
| **时机** | 前序/后序位置 | 后序位置 |
| **返回值** | 通常为 None | 返回子树结果 |

### **选择原则**

1. **能用返回值解决 → 分治**
2. **需要记录过程状态 → 遍历**
3. **需要子树结果 + 全局状态 → 混合**

### **实践建议**

- **优先尝试分治**：逻辑清晰，代码简洁
- **需要过程状态时用遍历**：路径、深度等
- **复杂问题用混合**：同时需要子树结果和全局状态




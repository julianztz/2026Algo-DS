# canJump 问题方法对比分析

## 问题描述
判断是否可以从数组的第一个位置跳到最后一个位置，每个位置的值表示在该位置最多能跳的步数。

## 方法1：倒推法（Greedy - Backward）

### 思路
从后往前遍历，维护一个变量 `pers` 记录**能够到达末尾的位置**。如果当前索引 `i` 可以跳到 `pers`，则更新 `pers = i`。最后检查是否 `pers == 0`。

### 代码
```python
def canJump(nums: List[int]) -> bool:
    sz = len(nums)
    pers = sz-1           # 从后往前，记录能到达末尾的位置
    for i in range(sz-2, -1, -1):
        if nums[i] >= pers - i:     # 当前index可以跳到pers
            pers = i

    if pers == 0:
        return True
    return False
```

### 优点
- ✅ **时间复杂度 O(n)**：只需一次遍历
- ✅ **空间复杂度 O(1)**：只需一个变量
- ✅ **逻辑清晰**：直接维护目标状态

### 关键点
- `pers` 表示：**从前往后看，能够到达末尾的最前面的位置**
- 条件 `nums[i] >= pers - i` 表示：从位置 `i` 能否跳到位置 `pers`

---

## 方法2：DP方法（你原代码的问题分析）

### 原代码问题

#### 问题1：返回值定义不一致
```python
# 第74行
fartherest = max(fartherest, jump(nums, from_ind+i))
```
这里假设 `jump()` 返回的是一个**绝对位置**（比如位置5），用来比较大小。

```python
# 第80行
return fartherest
```
但这里返回的 `fartherest` 是什么？它是子问题返回值的最大值，但：
- 如果 `jump(from_ind+i)` 返回的是绝对位置，那 `fartherest` 也是绝对位置
- 但第78行 `memo[from_ind] = from_ind + fartherest` 又加了 `from_ind`，这显然是错的

#### 问题2：memo存储逻辑错误
```python
memo[from_ind] = from_ind + fartherest
```
这里的问题是：
- 如果 `fartherest` 已经是子问题返回的**绝对位置**（比如从位置3开始能到达位置7），那再加 `from_ind` 就没意义了
- 如果 `fartherest` 是相对步数，那应该直接存，而不是加 `from_ind`

#### 问题3：逻辑混乱
函数的返回值含义不明确：
- 是返回"从当前位置能到达的最远位置"？
- 还是返回"从当前位置开始的最远相对距离"？

导致递归调用时无法正确使用返回值。

---

## 方法3：DP方法（修正版 - 布尔值返回）

### 思路
**状态定义**：`dp(i)` = 从位置 `i` 能否到达末尾

**状态转移**：
- 如果 `i >= n-1`，返回 `True`（已经到达）
- 否则，尝试所有可能的下一步 `i+1, i+2, ..., i+nums[i]`
- 只要有一条路径能到达末尾，返回 `True`

### 代码
```python
def canJumpDP(nums: List[int]) -> bool:
    memo = {}     # index: 能否到达末尾 (True/False)

    def canReachEnd(from_ind: int) -> bool:
        # base case: 已经到达或超过末尾
        if from_ind >= len(nums) - 1:
            return True
        
        # 剪枝：查memo
        if from_ind in memo:
            return memo[from_ind]
        
        # 枚举所有可能的下一步
        max_jump = nums[from_ind]
        for step in range(1, max_jump + 1):
            next_pos = from_ind + step
            if canReachEnd(next_pos):
                memo[from_ind] = True
                return True
        
        # 所有路径都走不通
        memo[from_ind] = False
        return False
    
    return canReachEnd(0)
```

### 优点
- ✅ **逻辑清晰**：返回值就是问题的答案（True/False）
- ✅ **状态定义明确**：`dp(i)` 的含义很清楚
- ✅ **正确性保证**：枚举所有可能性

### 缺点
- ⚠️ **时间复杂度**：最坏情况 O(n²)，每个位置都要尝试所有可能的步数
- ⚠️ **空间复杂度**：O(n) 用于memo和递归栈

---

## 方法4：DP方法（修正版 - 返回最远位置）

### 思路
**状态定义**：`dp(i)` = 从位置 `i` 开始能到达的**最远位置**（绝对位置）

**状态转移**：
- 如果 `i >= n-1`，返回 `n-1`
- 如果 `nums[i] == 0`，只能停留在当前位置
- 否则，枚举所有下一步，取能到达的最远位置

### 代码
```python
def canJumpDP2(nums: List[int]) -> bool:
    memo = {}     # index: 从该index能到达的最远位置

    def farthestReachable(from_ind: int) -> int:
        # base case: 已经到达末尾
        if from_ind >= len(nums) - 1:
            return len(nums) - 1
        
        # 剪枝：查memo
        if from_ind in memo:
            return memo[from_ind]
        
        # 当前能跳的最远距离
        max_jump = nums[from_ind]
        if max_jump == 0:
            # 当前位置无法移动
            memo[from_ind] = from_ind
            return from_ind
        
        # 枚举所有可能的下一步，找最远的
        farthest = from_ind  # 至少能停留在当前位置
        for step in range(1, max_jump + 1):
            next_pos = from_ind + step
            if next_pos >= len(nums) - 1:
                # 可以直接到达末尾
                memo[from_ind] = len(nums) - 1
                return len(nums) - 1
            # 从next_pos能到达的最远位置
            reachable = farthestReachable(next_pos)
            farthest = max(farthest, reachable)
        
        memo[from_ind] = farthest
        return farthest
    
    return farthestReachable(0) >= len(nums) - 1
```

### 关键点
- ✅ **返回值明确**：返回绝对位置（如位置7），不是相对步数
- ✅ **memo存储**：直接存储返回值，不需要额外计算
- ✅ **状态转移清晰**：`farthest = max(farthest, farthestReachable(next_pos))`

---

## 方法对比总结

| 方法 | 时间复杂度 | 空间复杂度 | 优势 | 劣势 |
|------|-----------|-----------|------|------|
| **倒推法** | O(n) | O(1) | 最优性能，代码简洁 | 需要理解反向思维 |
| **DP布尔值** | O(n²) | O(n) | 逻辑直观，枚举所有可能 | 性能较差 |
| **DP最远位置** | O(n²) | O(n) | 返回信息更丰富 | 性能较差 |

## 原DP代码的核心问题

1. **状态定义不清晰**：`jump()` 函数返回什么不明确
2. **memo存储错误**：`memo[from_ind] = from_ind + fartherest` 这行代码逻辑错误
3. **返回值不一致**：比较时用绝对位置，存储时又做了额外计算

## 建议

- **对于canJump问题**：优先使用倒推法或贪心法（方法1），性能最优
- **如果要用DP**：推荐使用方法3（布尔值返回），逻辑最清晰
- **DP的关键**：明确状态定义，返回值含义要一致，memo存储的应该就是返回值本身












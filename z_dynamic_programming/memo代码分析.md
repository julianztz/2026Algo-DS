# CoinChange 当前代码分析（已添加 memo）

## 当前代码

```python
def coinChange(coins: List[int], amount: int) -> int:
    memo = {}
    
    def traverse(coins, amt):
        nonlocal memo

        if amt == 0:
            return 0
        if amt < 0:
            return -1

        num_of_coin = float('inf')

        if amt in memo:
            return memo[amt]

        for coin in coins:
            subProblem = traverse(coins, amt-coin)
            if subProblem == -1:
                continue
            num_of_coin = min(num_of_coin, subProblem+1)
        
        memo[amt] = num_of_coin
        return num_of_coin
        
    res = traverse(coins, amount)
    if res == float('inf'):
        return -1
    return res
```

## 测试结果

✅ 所有测试用例通过：
- `coins=[1,2,5], amount=11` → 3 ✅
- `coins=[2], amount=3` → -1 ✅
- `coins=[1], amount=0` → 0 ✅
- `coins=[1,2,5], amount=100` → 20 ✅

## 代码分析

### ✅ 正确的地方

1. **memo 已添加** ✅
   - 避免了重复计算
   - 防止栈溢出

2. **使用 float('inf')** ✅
   - 初始值足够大

3. **无解情况处理** ✅
   - 最后检查 `res == float('inf')` 返回 -1

4. **memo 检查位置** ✅
   - 在 base case 之后，循环之前

---

### ⚠️ 可以优化的地方（不影响正确性）

#### 问题1：memo 中存储了 float('inf')

**当前代码**：
```python
memo[amt] = num_of_coin  # 如果无解，存储 float('inf')
return num_of_coin
```

**问题**：
- 如果所有子问题都无解，`num_of_coin` 保持 `float('inf')`
- 然后存储 `memo[amt] = float('inf')`
- 虽然功能正确（最后会返回 -1），但 memo 中存储了 `float('inf')`，不够优雅

**优化建议**：
```python
if num_of_coin == float('inf'):
    memo[amt] = -1
    return -1
else:
    memo[amt] = num_of_coin
    return num_of_coin
```

或者：
```python
result = num_of_coin if num_of_coin != float('inf') else -1
memo[amt] = result
return result
```

---

#### 问题2：memo 检查位置可以优化

**当前代码**：
```python
num_of_coin = float('inf')  # 先设置初始值

if amt in memo:  # 然后检查 memo
    return memo[amt]
```

**问题**：
- 如果 `amt` 在 memo 中，`num_of_coin = float('inf')` 这行代码是多余的
- 虽然不影响正确性，但效率稍低

**优化建议**：
```python
if amt in memo:  # 先检查 memo
    return memo[amt]

num_of_coin = float('inf')  # 再设置初始值
```

---

#### 问题3：nonlocal memo 不是必需的

**当前代码**：
```python
def traverse(coins, amt):
    nonlocal memo  # ⚠️ 实际上不需要
```

**说明**：
- 在 Python 中，内部函数可以直接访问外部函数的变量（读取和修改）
- `nonlocal` 主要用于需要修改外部作用域的变量时
- 对于字典 `memo`，直接修改其内容（如 `memo[amt] = value`）不需要 `nonlocal`
- 但如果要重新赋值 `memo = {}`，则需要 `nonlocal`

**结论**：
- 当前代码中 `nonlocal memo` 不是必需的，但加上也没问题
- 可以保留（更明确），也可以移除（更简洁）

---

## 优化后的代码

```python
def coinChange(coins: List[int], amount: int) -> int:
    memo = {}
    
    def traverse(coins, amt):
        # base case
        if amt == 0:
            return 0
        if amt < 0:
            return -1

        # 先检查 memo（优化：在设置初始值之前）
        if amt in memo:
            return memo[amt]

        num_of_coin = float('inf')

        for coin in coins:
            subProblem = traverse(coins, amt-coin)
            if subProblem == -1:
                continue
            num_of_coin = min(num_of_coin, subProblem+1)
        
        # 优化：存储 -1 而不是 float('inf')
        result = num_of_coin if num_of_coin != float('inf') else -1
        memo[amt] = result
        return result
        
    return traverse(coins, amount)
```

---

## 总结

### ✅ 当前代码状态

| 功能 | 状态 | 说明 |
|------|------|------|
| 基本功能 | ✅ 正确 | 所有测试用例通过 |
| 记忆化 | ✅ 已实现 | 避免重复计算 |
| 无解处理 | ✅ 正确 | 返回 -1 |
| 初始值 | ✅ 正确 | 使用 float('inf') |

### ⚠️ 可以优化的地方

1. **memo 存储值**：可以存储 -1 而不是 float('inf')（更优雅）
2. **memo 检查位置**：可以在设置初始值之前检查（效率稍高）
3. **nonlocal**：不是必需的，但保留也没问题

### 结论

**当前代码功能完全正确！** ✅

所有测试用例都通过，逻辑正确，有记忆化避免重复计算。

优化建议只是让代码更优雅、更高效，但不影响正确性。



































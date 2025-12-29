# pickIndex 中 `return left - 1` 的问题分析

## 一、测试结果

### 测试用例1：w = [5]（单个元素）
- **所有 target (1-5) 都返回 -1** ❌
- **应该返回 0** ✓

### 测试用例2：w = [1, 3]
- target = 1 → 返回 -1，应该是 0 ❌
- target = 2, 3, 4 → 返回 0，应该是 1 ❌

### 统计频率测试
- 索引 0: 76%（应该是 25%）❌
- 索引 1: 0%（应该是 75%）❌

## 二、问题根源：`return left - 1` 是错误的

### 为什么 `return left - 1` 是错误的？

**核心理解：**
- `preSum[i]` 表示索引 0 到 i 的权重总和
- 对于 target，我们要找第一个 `preSum[i] >= target` 的位置 i
- **这个位置 i 就是我们要返回的索引！**

**示例：w = [1, 3]，preSum = [1, 4]**

| target | 二分搜索过程 | left 最终值 | 你的返回 | 正确返回 | 说明 |
|--------|------------|------------|---------|---------|------|
| 1 | left=0, right=0 (循环不执行) | 0 | -1 ❌ | 0 ✓ | target=1 在区间 [1,1]，对应索引 0 |
| 2 | left=0→1, right=1 | 1 | 0 ❌ | 1 ✓ | target=2 在区间 [2,4]，对应索引 1 |
| 3 | left=0→1, right=1 | 1 | 0 ❌ | 1 ✓ | target=3 在区间 [2,4]，对应索引 1 |
| 4 | left=0→1, right=1 | 1 | 0 ❌ | 1 ✓ | target=4 在区间 [2,4]，对应索引 1 |

**结论：应该直接 `return left`，不需要 `-1`**

## 三、为什么会有 `-1` 的想法？

可能的原因：
1. **误解了索引映射**：以为 preSum 的索引和原数组索引有偏移
2. **混淆了区间边界**：以为需要减 1 来对应区间

**但实际上：**
- `preSum[i]` 对应的就是原数组的索引 i
- 如果 `target <= preSum[0]`，返回索引 0
- 如果 `preSum[i-1] < target <= preSum[i]`，返回索引 i

## 四、正确的实现

```python
def pickIndex(self) -> int:
    target = random.randint(1, self.preSum[-1])
    
    left, right = 0, len(self.preSum) - 1
    
    while left < right:
        mid = (left + right) // 2
        if self.preSum[mid] < target:
            left = mid + 1
        else:  # preSum[mid] >= target
            right = mid
    
    return left  # ✅ 直接返回 left，不需要 -1
```

## 五、验证

### w = [5]（单个元素）
- preSum = [5]
- target ∈ [1, 5]
- left = 0（循环不执行，因为 left == right）
- return 0 ✓

### w = [1, 3]
- preSum = [1, 4]
- target = 1: left = 0, return 0 ✓
- target = 2, 3, 4: left = 1, return 1 ✓

### w = [1, 2, 3]
- preSum = [1, 3, 6]
- target = 1: left = 0, return 0 ✓
- target = 2, 3: left = 1, return 1 ✓
- target = 4, 5, 6: left = 2, return 2 ✓

## 六、总结

**问题：** `return left - 1` 是错误的

**原因：**
- `left` 已经是正确的索引了
- 不需要减 1

**修正：** `return left`

**验证：**
- 单个元素：应该返回 0，不是 -1
- 多个元素：每个 target 都应该返回正确的索引



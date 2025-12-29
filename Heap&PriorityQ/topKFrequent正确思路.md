# Top K Frequent Elements 正确思路

## 问题分析

### ❌ **错误思路（需要最后sort，失去heap意义）**

```python
# 错误思路
def topKFrequent_wrong(nums, k):
    counter = Counter(nums)  # 1. 统计频率 ✅
    heap = []
    
    # 2. 遍历nums，把元素放入heap ❌
    for e in nums:
        heapq.heappush(heap, e)
    
    # 3. 弹出元素，查counter得到频率 ❌
    result = []
    while heap:
        num = heapq.heappop(heap)
        freq = counter[num]
        result.append((num, freq))
    
    # 4. 按频率排序 ❌ (失去了heap的意义)
    result.sort(key=lambda x: x[1], reverse=True)
    return [num for num, freq in result[:k]]
```

**问题：**
- 把元素本身放入heap，而不是频率
- 最后还需要sort，时间复杂度变成 O(n log n)
- 失去了heap的优势（应该O(n log k)）

---

### ✅ **正确思路（不需要sort，充分利用heap）**

**核心思想：用频率作为堆的优先级**

```python
# 正确思路
def topKFrequent(nums, k):
    counter = Counter(nums)  # 1. 统计频率 ✅
    heap = []
    
    # 2. 把(频率, 元素)放入heap ✅
    # 关键：频率作为优先级，元素作为数据
    for num, freq in counter.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)  # 弹出频率最小的
    
    # 3. 直接得到结果，不需要sort ✅
    return [num for freq, num in reversed(heap)]
```

---

## 三种正确实现方法

### **方法1：维护大小为k的最小堆（推荐）**

```python
from collections import Counter
import heapq

def topKFrequent(nums: List[int], k: int) -> List[int]:
    counter = Counter(nums)
    heap = []
    
    # 维护大小为k的堆
    for num, freq in counter.items():
        heapq.heappush(heap, (freq, num))  # (频率, 元素)
        if len(heap) > k:
            heapq.heappop(heap)  # 弹出频率最小的
    
    # 堆中保留的是频率最大的k个元素
    # 但顺序是频率小的在前，需要reverse
    return [num for freq, num in reversed(heap)]
```

**时间复杂度：** O(n log k)
- 统计频率：O(n)
- 维护大小为k的堆：O(n log k)

**空间复杂度：** O(k)

---

### **方法2：用负频率实现最大堆（更直观）**

```python
def topKFrequent_v2(nums: List[int], k: int) -> List[int]:
    counter = Counter(nums)
    heap = []
    
    # 用负频率，实现最大堆效果
    for num, freq in counter.items():
        heapq.heappush(heap, (-freq, num))  # 负频率！
        if len(heap) > k:
            heapq.heappop(heap)  # 弹出负频率最大的（即频率最小的）
    
    # 堆中的元素：(-3,1) < (-2,2)，所以频率大的在前
    return [num for neg_freq, num in heap]
```

**优点：**
- 不需要reverse
- 逻辑更直观（频率大的在前）

---

### **方法3：全部入堆再弹出k个（效率较低）**

```python
def topKFrequent_v3(nums: List[int], k: int) -> List[int]:
    counter = Counter(nums)
    heap = []
    
    # 全部入堆
    for num, freq in counter.items():
        heapq.heappush(heap, (-freq, num))
    
    # 弹出k个最大的
    result = []
    for _ in range(k):
        neg_freq, num = heapq.heappop(heap)
        result.append(num)
    
    return result
```

**时间复杂度：** O(n log n) - 全部入堆
- 比方法1/2慢，但思路清晰

---

## 详细示例

### 示例：`nums = [1, 1, 1, 2, 2, 3]`, `k = 2`

#### 步骤1：统计频率
```
Counter({1: 3, 2: 2, 3: 1})
```

#### 步骤2：方法1演示（最小堆）

| 操作 | 堆状态 | 说明 |
|------|--------|------|
| Push (3, 1) | `[(3, 1)]` | 频率3的元素1 |
| Push (2, 2) | `[(2, 2), (3, 1)]` | 频率2的元素2，频率3的元素1 |
| Push (1, 3) | `[(2, 2), (3, 1)]` | Push (1,3)后堆大小>k，弹出(1,3) |

**结果：** `[(2, 2), (3, 1)]` → reverse → `[1, 2]` ✅

#### 步骤2：方法2演示（负频率）

| 操作 | 堆状态 | 说明 |
|------|--------|------|
| Push (-3, 1) | `[(-3, 1)]` | 负频率-3 |
| Push (-2, 2) | `[(-3, 1), (-2, 2)]` | -3 < -2，所以(-3,1)在前 |
| Push (-1, 3) | `[(-2, 2), (-3, 1)]` | Push后弹出(-1,3) |

**结果：** `[(-2, 2), (-3, 1)]` → `[2, 1]` ❌ (顺序不对)

**修正：** 需要reverse或按频率排序：
```python
return [num for neg_freq, num in sorted(heap, key=lambda x: x[0])]
# 或者简单地reverse
return [num for neg_freq, num in reversed(heap)]
```

---

## 关键理解点

### 1. **为什么不能用元素本身作为heap的key？**

```python
# ❌ 错误：把元素放入heap
for e in nums:
    heapq.heappush(heap, e)

# 问题：heap按元素值排序，不是按频率排序
# 最后还需要查counter并sort，失去了heap的意义
```

### 2. **为什么用(频率, 元素)作为heap的key？**

```python
# ✅ 正确：用频率作为优先级
heapq.heappush(heap, (freq, num))

# 优势：
# - heap自动按频率排序
# - 不需要最后sort
# - 时间复杂度O(n log k)，不是O(n log n)
```

### 3. **为什么需要维护大小为k的堆？**

```python
if len(heap) > k:
    heapq.heappop(heap)  # 弹出频率最小的

# 原因：
# - 保持堆大小为k，空间复杂度O(k)
# - 时间复杂度O(n log k)，而不是O(n log n)
# - 堆中保留的是频率最大的k个元素
```

---

## 时间复杂度对比

| 方法 | 时间复杂度 | 空间复杂度 | 是否需要sort |
|------|-----------|-----------|-------------|
| **错误思路（最后sort）** | O(n log n) ❌ | O(n) | ❌ 需要 |
| **方法1（维护k大小堆）** | O(n log k) ✅ | O(k) | ❌ 不需要 |
| **方法2（负频率）** | O(n log k) ✅ | O(k) | ❌ 不需要 |
| **方法3（全部入堆）** | O(n log n) | O(n) | ❌ 不需要 |

---

## 总结

### ✅ **正确思路的核心：**
1. **用频率作为堆的优先级**：`(freq, num)` 而不是 `num`
2. **维护大小为k的堆**：始终保持前k个频率最大的元素
3. **不需要最后sort**：heap已经按优先级排序

### ❌ **错误思路的问题：**
1. 把元素本身放入heap
2. 最后还需要sort，时间复杂度变成O(n log n)
3. 失去了heap的优势

### 📝 **记忆要点：**
- **Heap的key = 优先级**
- **Top K问题 = 维护大小为k的堆**
- **不需要最后sort = 充分利用heap的优势**



















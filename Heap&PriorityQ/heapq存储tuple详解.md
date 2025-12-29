# heapq 存储 tuple 详解

## 核心问题

**Q: heap中只能存储primitive type吗？可以存储tuple吗？**

**A: ✅ 可以！heapq可以存储任何可比较的类型，包括tuple、对象等。**

---

## 一、heapq可以存储什么？

### ✅ **可以存储的类型：**

1. **基本类型**：int, float, str
2. **tuple（元组）**：✅ 最常用！
3. **自定义对象**：需要实现 `__lt__` 等方法

### **tuple作为heap元素的优势：**

```python
import heapq

# tuple格式：(优先级, 数据)
heap = []
heapq.heappush(heap, (3, 'task3'))  # 优先级3，数据'task3'
heapq.heappush(heap, (1, 'task1'))  # 优先级1，数据'task1'
heapq.heappush(heap, (2, 'task2'))  # 优先级2，数据'task2'

# 弹出时按优先级排序
popped = heapq.heappop(heap)  # (1, 'task1')
print(popped[0])  # 1 (优先级)
print(popped[1])  # 'task1' (数据)
```

---

## 二、tuple比较规则（关键！）

### **Python tuple的比较规则：**

**按元素顺序比较（lexicographic order）：**
1. 先比较第一个元素
2. 如果第一个元素相同，比较第二个元素
3. 依此类推

### **示例：**

```python
# tuple比较
(1, 'a') < (2, 'b')  # True，因为1 < 2
(1, 'a') < (1, 'b')  # True，因为第一个相同(1==1)，比较第二个('a'<'b')
(2, 'a') < (1, 'b')  # False，因为2 > 1

# 排序示例
tuples = [(3, 'z'), (1, 'b'), (1, 'a'), (2, 'c')]
sorted(tuples)  # [(1, 'a'), (1, 'b'), (2, 'c'), (3, 'z')]
```

### **heap中的tuple比较：**

```python
import heapq

heap = []
heapq.heappush(heap, (3, 'z'))
heapq.heappush(heap, (1, 'b'))
heapq.heappush(heap, (1, 'a'))
heapq.heappush(heap, (2, 'c'))

# heap会按第一个元素排序，第一个相同时按第二个元素排序
print(heap)  # [(1, 'a'), (1, 'b'), (2, 'c'), (3, 'z')]
```

---

## 三、Top K Frequent中的tuple使用

### **为什么用 `(freq, num)` 而不是 `num`？**

#### **错误方式：**
```python
# ❌ 只存储元素
heap = []
for num in nums:
    heapq.heappush(heap, num)

# 问题：heap按元素值排序，不是按频率排序
# 无法知道哪个元素频率最高
```

#### **正确方式：**
```python
# ✅ 存储(频率, 元素)
counter = Counter(nums)
heap = []
for num, freq in counter.items():
    heapq.heappush(heap, (freq, num))  # (优先级, 数据)

# 优势：
# 1. heap按频率（第一个元素）排序
# 2. 可以直接访问频率和元素
# 3. 频率相同时，按元素值排序（可选）
```

### **详细示例：**

```python
from collections import Counter
import heapq

nums = [1, 1, 1, 2, 2, 3]
counter = Counter(nums)  # {1: 3, 2: 2, 3: 1}

heap = []
for num, freq in counter.items():
    heapq.heappush(heap, (freq, num))
    print(f'Push ({freq}, {num}): {heap}')

# 输出：
# Push (3, 1): [(3, 1)]
# Push (2, 2): [(2, 2), (3, 1)]
# Push (1, 3): [(1, 3), (3, 1), (2, 2)]

# 堆顶是最小的，即(1, 3)（频率最小的）
# 但我们要频率最大的，所以维护大小为k的堆
```

---

## 四、tuple在heap中的使用模式

### **模式1：简单优先级队列**
```python
# (优先级, 任务)
heap = []
heapq.heappush(heap, (3, 'task3'))
heapq.heappush(heap, (1, 'task1'))
heapq.heappush(heap, (2, 'task2'))

task = heapq.heappop(heap)  # (1, 'task1')
priority, data = task
```

### **模式2：Top K问题**
```python
# (频率, 元素)
counter = Counter(nums)
heap = []
for num, freq in counter.items():
    heapq.heappush(heap, (freq, num))
    if len(heap) > k:
        heapq.heappop(heap)

# 结果
result = [num for freq, num in heap]
```

### **模式3：带多个优先级的任务**
```python
# (主要优先级, 次要优先级, 任务)
heap = []
heapq.heappush(heap, (3, 1, 'task1'))
heapq.heappush(heap, (3, 2, 'task2'))  # 主要优先级相同，按次要优先级
heapq.heappush(heap, (2, 1, 'task3'))

# 比较顺序：先按第一个元素，相同再按第二个元素
```

### **模式4：负频率（最大堆）**
```python
# (-频率, 元素) 实现最大堆
heap = []
for num, freq in counter.items():
    heapq.heappush(heap, (-freq, num))  # 负频率！

# 因为 -3 < -2，所以(-3,1)会在堆顶（频率最大的）
```

---

## 五、访问tuple元素的方法

### **方法1：直接索引**
```python
item = heapq.heappop(heap)  # (3, 'task1')
priority = item[0]  # 3
data = item[1]      # 'task1'
```

### **方法2：解包（推荐）**
```python
priority, data = heapq.heappop(heap)  # 直接解包
print(f'优先级: {priority}, 数据: {data}')
```

### **方法3：列表推导式**
```python
# 只要数据部分
result = [num for freq, num in heap]

# 只要优先级部分
priorities = [freq for freq, num in heap]
```

---

## 六、常见错误

### **错误1：顺序反了**
```python
# ❌ 错误：元素在前，频率在后
heapq.heappush(heap, (num, freq))
# 问题：heap会按元素值排序，不是按频率排序

# ✅ 正确：频率在前，元素在后
heapq.heappush(heap, (freq, num))
```

### **错误2：只存储元素**
```python
# ❌ 错误：只存储元素
heapq.heappush(heap, num)
# 问题：无法知道频率，需要查counter并sort

# ✅ 正确：存储(频率, 元素)
heapq.heappush(heap, (freq, num))
```

### **错误3：不理解tuple比较**
```python
# ❌ 错误：认为tuple不能作为key
# 实际上tuple是heap的完美用法！

# ✅ 正确：理解tuple按元素顺序比较
# (freq1, num1) < (freq2, num2) 当且仅当
# freq1 < freq2 或 (freq1 == freq2 and num1 < num2)
```

---

## 七、完整示例

```python
from collections import Counter
import heapq
from typing import List

def topKFrequent(nums: List[int], k: int) -> List[int]:
    # 1. 统计频率
    counter = Counter(nums)
    
    # 2. 用tuple存储(频率, 元素)
    heap = []
    for num, freq in counter.items():
        # tuple的第一个元素是优先级（频率）
        # tuple的第二个元素是数据（元素）
        heapq.heappush(heap, (freq, num))
        
        # 维护大小为k的堆
        if len(heap) > k:
            heapq.heappop(heap)
    
    # 3. 提取结果（只要元素部分）
    return [num for freq, num in reversed(heap)]
    # 或者解包：
    # return [item[1] for item in reversed(heap)]
```

---

## 八、总结

### ✅ **关键点：**

1. **heapq可以存储tuple** ✅
2. **tuple比较规则**：按元素顺序比较（第一个、第二个...）
3. **常用模式**：`(优先级, 数据)`
4. **Top K问题**：`(频率, 元素)`

### 📝 **记忆要点：**

- **heap可以存储tuple**，不只能存int
- **tuple比较**：先比第一个，相同再比第二个
- **(freq, num)** 中，freq是优先级，num是数据
- **解包访问**：`priority, data = item`

### 🎯 **应用场景：**

- ✅ 优先级队列：`(优先级, 任务)`
- ✅ Top K问题：`(频率, 元素)`
- ✅ 多级排序：`(主要, 次要, 数据)`
- ✅ 负值技巧：`(-频率, 元素)` 实现最大堆



















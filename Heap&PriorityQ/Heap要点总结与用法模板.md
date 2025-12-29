# Heap 要点总结与 Python 用法模板

## 一、Heap 核心要点

### **1. 基本概念**

- **Heap（堆）**：一种特殊的完全二叉树数据结构
- **Min Heap（最小堆）**：父节点 ≤ 所有子节点（堆顶是最小值）
- **Max Heap（最大堆）**：父节点 ≥ 所有子节点（堆顶是最大值）
- **Python的heapq**：默认实现最小堆

### **2. 核心性质**

1. **堆性质**：`parent ≤ children`（min heap）或 `parent ≥ children`（max heap）
2. **完全二叉树**：用数组实现，满足完全二叉树结构
3. **索引关系**：
   - 对于索引 `i`：
   - 父节点：`(i-1) // 2`
   - 左子节点：`2*i + 1`
   - 右子节点：`2*i + 2`

### **3. 时间复杂度**

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 插入（heappush） | O(log n) | swim（上浮）操作 |
| 删除（heappop） | O(log n) | sink（下沉）操作 |
| 获取堆顶 | O(1) | `heap[0]` |
| 构建堆（heapify） | O(n) | 从无序数组构建 |

### **4. 底层操作原理**

- **Swim（上浮）**：插入新元素时，从底部向上调整
- **Sink（下沉）**：删除堆顶时，用最后一个元素替换，从顶部向下调整
- **自动调整**：heapq自动维护堆性质，不需要手动实现

---

## 二、Python heapq 使用要点

### **1. 导入模块**

```python
import heapq
```

### **2. 基本操作**

```python
# 创建堆（空列表）
heap = []

# 插入元素
heapq.heappush(heap, item)

# 弹出最小元素
min_item = heapq.heappop(heap)

# 查看堆顶（不删除）
top = heap[0]

# 将列表转换为堆（O(n)时间）
heapq.heapify(list)

# 先push再pop（更高效）
item = heapq.heappushpop(heap, item)

# 先pop再push
item = heapq.heapreplace(heap, item)
```

### **3. 重要特性**

1. **✅ heapq是min heap**：堆顶是最小值
2. **✅ 可以存储tuple**：`(优先级, 数据)` 模式
3. **✅ tuple比较规则**：按元素顺序比较（第一个元素优先）
4. **✅ 自动维护堆性质**：插入/删除后自动调整

### **4. 实现最大堆的方法**

```python
# 方法1：插入负值
heap = []
heapq.heappush(heap, -value)  # 插入负值
max_val = -heapq.heappop(heap)  # 弹出时取负

# 方法2：使用tuple，第一个元素取负
heap = []
heapq.heappush(heap, (-priority, value))
max_val = heapq.heappop(heap)[1]
```

---

## 三、常用模板

### **模板1：基本最小堆**

```python
import heapq

heap = []

# 插入元素
for num in nums:
    heapq.heappush(heap, num)

# 弹出最小元素
while heap:
    min_val = heapq.heappop(heap)
    print(min_val)
```

### **模板2：优先级队列（tuple模式）**

```python
import heapq

heap = []

# 插入（优先级, 数据）
heapq.heappush(heap, (3, 'task3'))
heapq.heappush(heap, (1, 'task1'))
heapq.heappush(heap, (2, 'task2'))

# 弹出
priority, task = heapq.heappop(heap)
print(f'优先级: {priority}, 任务: {task}')
```

### **模板3：Top K 问题（维护大小为k的堆）**

```python
import heapq

def find_k_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # 弹出最小的
    return heap  # 返回k个最大的

# 或者用负值实现Top K最小
def find_k_smallest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, -num)  # 负值
        if len(heap) > k:
            heapq.heappop(heap)
    return [-x for x in heap]  # 取负返回
```

### **模板4：Top K Frequent Elements**

```python
from collections import Counter
import heapq
from typing import List

def topKFrequent(nums: List[int], k: int) -> List[int]:
    counter = Counter(nums)
    heap = []
    
    # 用频率作为优先级
    for num, freq in counter.items():
        heapq.heappush(heap, (freq, num))  # (频率, 元素)
        if len(heap) > k:
            heapq.heappop(heap)  # 弹出频率最小的
    
    return [num for freq, num in reversed(heap)]
```

### **模板5：合并K个有序序列**

```python
import heapq

def merge_k_sorted(lists):
    heap = []
    
    # 初始化：每个序列的第一个元素
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))  # (值, 序列索引, 元素索引)
    
    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        # 从同一序列取下一个元素
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result
```

### **模板6：数据流的中位数**

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # 最大堆（用负值实现）
        self.large = []  # 最小堆
    
    def addNum(self, num):
        heapq.heappush(self.small, -num)  # 先加入small
        
        # 保证small的最大值 <= large的最小值
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # 平衡两个堆的大小（差值不超过1）
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return (-self.small[0] + self.large[0]) / 2
```

### **模板7：K路合并（通用版本）**

```python
import heapq

def k_way_merge(*sequences):
    """合并多个有序序列"""
    heap = []
    iterators = [iter(seq) for seq in sequences]
    
    # 初始化
    for i, it in enumerate(iterators):
        try:
            heapq.heappush(heap, (next(it), i, it))
        except StopIteration:
            pass
    
    result = []
    while heap:
        val, idx, it = heapq.heappop(heap)
        result.append(val)
        
        try:
            heapq.heappush(heap, (next(it), idx, it))
        except StopIteration:
            pass
    
    return result
```

---

## 四、典型应用场景

### **1. Top K 问题**
- 前K个最大/最小元素
- 前K个频率最高的元素
- 前K个距离最近的点

### **2. 优先级队列**
- 任务调度
- 事件处理
- 贪心算法

### **3. 排序相关**
- 堆排序
- 部分排序
- 多路归并

### **4. 算法应用**
- Dijkstra最短路径
- Huffman编码
- 中位数维护

---

## 五、常见错误与注意事项

### **❌ 错误1：手动修改列表后不重新heapify**

```python
# ❌ 错误
heap = [3, 1, 4, 1, 5]
heapq.heapify(heap)
heap[0] = 9  # 直接修改
min_val = heapq.heappop(heap)  # 可能得到错误结果

# ✅ 正确：修改后重新heapify
heap[0] = 9
heapq.heapify(heap)
```

### **❌ 错误2：忘记tuple的顺序**

```python
# ❌ 错误：元素在前
heapq.heappush(heap, (num, freq))  # 会按num排序！

# ✅ 正确：优先级在前
heapq.heappush(heap, (freq, num))  # 按freq排序
```

### **❌ 错误3：Top K问题不维护堆大小**

```python
# ❌ 错误：全部入堆再弹出
for num in nums:
    heapq.heappush(heap, num)  # 堆大小 = n
for _ in range(k):
    heapq.heappop(heap)  # O(n log n)

# ✅ 正确：维护大小为k的堆
for num in nums:
    heapq.heappush(heap, num)
    if len(heap) > k:
        heapq.heappop(heap)  # O(n log k)
```

### **❌ 错误4：混淆heapq和PriorityQueue**

```python
# ❌ 算法题用PriorityQueue（性能差）
from queue import PriorityQueue
pq = PriorityQueue()

# ✅ 算法题用heapq（性能好）
import heapq
heap = []
```

### **❌ 错误5：在循环中使用len(heap)**

```python
# ❌ 错误：效率低
while len(heap) > 0:
    heapq.heappop(heap)

# ✅ 正确
while heap:
    heapq.heappop(heap)
```

---

## 六、性能对比

### **heapq vs PriorityQueue**

| 特性 | heapq | PriorityQueue |
|------|-------|---------------|
| 性能 | ⚡ 快（无锁） | 🐌 慢（有锁） |
| 线程安全 | ❌ | ✅ |
| 使用场景 | 算法题、单线程 | 多线程 |

**建议：95%情况用heapq**

### **时间复杂度对比**

| 操作 | Heap | 排序 | 说明 |
|------|------|------|------|
| Top K | O(n log k) ✅ | O(n log n) | Heap更优 |
| 全部排序 | O(n log n) | O(n log n) | 相同 |
| 优先级队列 | O(log n) | - | Heap独有 |

---

## 七、快速参考卡

### **核心操作**

```python
import heapq

heap = []                           # 创建
heapq.heappush(heap, item)          # 插入 O(log n)
item = heapq.heappop(heap)          # 弹出 O(log n)
top = heap[0]                       # 查看堆顶 O(1)
heapq.heapify(lst)                  # 建堆 O(n)
```

### **常用模式**

```python
# 模式1：基本堆
heap = []
for x in items:
    heapq.heappush(heap, x)

# 模式2：优先级队列
heap = []
heapq.heappush(heap, (priority, data))

# 模式3：Top K
heap = []
for x in items:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)

# 模式4：最大堆（用负值）
heap = []
heapq.heappush(heap, -value)
max_val = -heapq.heappop(heap)
```

### **记忆要点**

1. **heapq是最小堆**：堆顶是最小值
2. **可以存储tuple**：`(优先级, 数据)`
3. **tuple比较规则**：按元素顺序比较
4. **Top K问题**：维护大小为k的堆
5. **自动调整**：不需要手动实现swim/sink

---

## 八、实战检查清单

### **使用heap前自问：**

- [ ] 需要的是最小堆还是最大堆？
- [ ] Top K问题是否维护了堆大小？
- [ ] tuple的优先级是否放在第一位？
- [ ] 是否用heapq而不是PriorityQueue？
- [ ] 是否需要最后sort？（如果是，可能用错方法）

### **代码审查要点：**

- ✅ 使用 `import heapq` 而不是 `from queue import PriorityQueue`
- ✅ Top K问题：`if len(heap) > k: heapq.heappop(heap)`
- ✅ tuple模式：`(优先级, 数据)` 顺序正确
- ✅ 最大堆：使用负值技巧
- ✅ 访问堆顶：`heap[0]` 而不是 `heapq.heappop()`

---

## 九、总结

### **核心概念**
- Heap = 完全二叉树 + 堆性质
- heapq = Python的最小堆实现
- 优先级队列 = (优先级, 数据) tuple模式

### **关键操作**
- Push = 插入末尾 + swim上浮
- Pop = 取出堆顶 + 最后元素替换 + sink下沉
- 自动调整，不需要手动实现

### **应用场景**
- Top K问题 → 维护大小为k的堆
- 优先级队列 → tuple模式
- 最大堆 → 负值技巧

### **最佳实践**
- ✅ 算法题用heapq（不用PriorityQueue）
- ✅ Top K维护堆大小（O(n log k)）
- ✅ 用tuple存储优先级+数据
- ✅ 理解原理，不需要手动实现底层操作

---

**记住：heap是解决Top K和优先级队列问题的利器，理解tuple比较规则是关键！**


















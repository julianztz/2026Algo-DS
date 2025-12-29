# Hashtable / Dictionary 常见题型和用法总结

## 一、基本概念

### Python 中的实现

```python
# 创建字典
d = {}
d = dict()

# 基本操作
d[key] = value        # 插入/更新 O(1)
value = d[key]        # 查找 O(1)
del d[key]            # 删除 O(1)
key in d              # 检查存在 O(1)

# 常用方法
d.get(key, default)   # 安全获取，不存在返回 default
d.keys()              # 所有键
d.values()            # 所有值
d.items()             # 所有键值对
```

### 时间复杂度

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 插入 | O(1) 平均 | 哈希表特性 |
| 查找 | O(1) 平均 | 哈希表特性 |
| 删除 | O(1) 平均 | 哈希表特性 |
| 检查存在 | O(1) 平均 | `key in d` |

---

## 二、常见题型分类

### 1. 查找/配对问题

**核心思路：** 使用字典存储已访问的元素，快速查找补数

#### LeetCode 1: Two Sum

```python
def twoSum(nums: List[int], target: int) -> List[int]:
    map = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in map:  # ✅ 先检查，再存储
            return [map[complement], i]
        map[n] = i  # 存储当前元素
    return []
```

**关键点：**
- ✅ 先检查，再存储（避免相同元素返回同一索引）
- ✅ 时间复杂度：O(n)
- ✅ 空间复杂度：O(n)

**注意事项：**
- ❌ 不要先存储再检查（会导致相同元素问题）
- ✅ 使用 `complement in map` 而不是 `complement in map.keys()`

#### 变种：3Sum, 4Sum
- 可以结合排序 + 双指针
- 或者使用多层字典嵌套

---

### 2. 频率统计问题

**核心思路：** 使用字典统计元素出现次数

#### LeetCode 242: Valid Anagram

```python
# 方法1：Counter（最简洁）
from collections import Counter
def isAnagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# 方法2：手动计数
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    map = {}
    for char in s:
        map[char] = map.get(char, 0) + 1
    for char in t:
        map[char] = map.get(char, 0) - 1
        if map[char] < 0:
            return False
    return True
```

**关键点：**
- ✅ 使用 `map.get(key, 0)` 安全获取
- ✅ Counter 是最简洁的方式
- ✅ 字典减法：先加后减，检查是否全为 0

#### LeetCode 387: First Unique Character

```python
def firstUniqChar(s: str) -> int:
    map = {}
    # 统计频率
    for char in s:
        map[char] = map.get(char, 0) + 1
    
    # 按顺序查找第一个频率为 1 的字符
    for i, char in enumerate(s):
        if map[char] == 1:
            return i
    return -1
```

**关键点：**
- ✅ 先统计频率，再按顺序查找
- ✅ 保证返回第一个唯一字符

#### LeetCode 169: Majority Element

```python
# 方法1：字典统计
def majorityElement(nums: List[int]) -> int:
    map = {}
    for n in nums:
        map[n] = map.get(n, 0) + 1
        if map[n] > len(nums) / 2:
            return n

# 方法2：Boyer-Moore（O(1) 空间）
def majorityElement_O1(nums: List[int]) -> int:
    candidate = None
    count = 0
    for n in nums:
        if count == 0:
            candidate = n
        count += 1 if n == candidate else -1
    return candidate
```

---

### 3. 分组问题

**核心思路：** 使用字典的 key 作为分组依据

#### LeetCode 49: Group Anagrams

```python
from collections import defaultdict

def groupAnagrams(strs: List[str]) -> List[List[str]]:
    map = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # tuple 才能作为 key
        map[key].append(s)
    return list(map.values())
```

**关键点：**
- ✅ 使用 `defaultdict(list)` 简化代码
- ✅ 使用 `tuple(sorted(s))` 作为 key（list 不可哈希）
- ✅ 或者使用字符计数数组作为 key（更高效）

**优化：字符计数数组（只小写字母）**
```python
def groupAnagrams(strs: List[str]) -> List[List[str]]:
    map = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for char in s:
            count[ord(char) - ord('a')] += 1
        map[tuple(count)].append(s)  # O(n*k) 不需要排序
    return list(map.values())
```

---

### 4. 映射/模式匹配问题

**核心思路：** 建立双向映射关系

#### LeetCode 290: Word Pattern

```python
def wordPattern(pattern: str, s: str) -> bool:
    map = {}
    used = set()  # 记录已使用的单词
    words = s.split()
    
    if len(pattern) != len(words):
        return False
    
    for i, char in enumerate(pattern):
        if char in map:
            if map[char] != words[i]:
                return False
        else:
            if words[i] in used:  # ✅ 检查双向映射
                return False
            map[char] = words[i]
            used.add(words[i])
    
    return True
```

**关键点：**
- ✅ 需要检查双向映射（pattern → word 和 word → pattern）
- ✅ 使用 set 记录已使用的单词

---

### 5. 集合操作问题

**核心思路：** 使用 set 进行快速查找

#### LeetCode 128: Longest Consecutive Sequence

```python
def longestConsecutive(nums: List[int]) -> int:
    set_nums = set(nums)
    max_length = 0
    
    for n in set_nums:
        # ✅ 关键：只从序列的起点开始遍历
        if n - 1 not in set_nums:
            count = 1
            cur_n = n
            while cur_n + 1 in set_nums:
                cur_n += 1
                count += 1
            max_length = max(count, max_length)
    
    return max_length
```

**关键点：**
- ✅ 使用 set 实现 O(1) 查找
- ✅ 只从序列的起点开始遍历（避免重复计算）
- ✅ 每个元素最多被访问 2 次 → O(n) 时间复杂度

---

### 6. 差值/缺失问题

**核心思路：** 使用字典记录出现情况

#### LeetCode 389: Find the Difference

```python
def findTheDifference(s: str, t: str) -> str:
    map = {}
    for char in s:
        map[char] = map.get(char, 0) + 1
    
    for char in t:
        map[char] = map.get(char, 0) - 1
        if map[char] < 0:  # 负数说明 t 中多了这个字符
            return char
```

**关键点：**
- ✅ 字典减法：先加后减
- ✅ 负数表示 t 中多了该字符

#### LeetCode 448: Find All Numbers Disappeared

```python
def findDisappearedNumbers(nums: List[int]) -> List[int]:
    map = {}
    for i in range(1, len(nums) + 1):
        map[i] = 0
    
    for n in nums:
        map[n] = map.get(n, 0) + 1
    
    return [k for k, v in map.items() if v == 0]
```

---

## 三、常用技巧和模式

### 1. 安全获取值

```python
# ❌ 可能报错
value = d[key]  # KeyError if key not exists

# ✅ 安全方式
value = d.get(key, default)  # 不存在返回 default
value = d.get(key)           # 不存在返回 None
```

### 2. 计数模式

```python
# 模式：统计频率
map = {}
for item in items:
    map[item] = map.get(item, 0) + 1

# 或使用 Counter
from collections import Counter
counter = Counter(items)
```

### 3. 分组模式

```python
# 模式：按 key 分组
from collections import defaultdict
map = defaultdict(list)
for item in items:
    key = get_key(item)
    map[key].append(item)

# 或手动实现
map = {}
for item in items:
    key = get_key(item)
    if key not in map:
        map[key] = []
    map[key].append(item)
```

### 4. 字典减法

```python
# 模式：先加后减，检查是否全为 0
map = {}
for char in s:
    map[char] = map.get(char, 0) + 1

for char in t:
    map[char] = map.get(char, 0) - 1
    if map[char] < 0:  # 负数说明 t 中多了
        return False
```

### 5. 双向映射

```python
# 模式：检查双向映射
map1 = {}  # pattern → word
map2 = {}  # word → pattern

for p, w in zip(pattern, words):
    if p in map1 and map1[p] != w:
        return False
    if w in map2 and map2[w] != p:
        return False
    map1[p] = w
    map2[w] = p
```

---

## 四、注意事项

### 1. 键的可哈希性

```python
# ✅ 可哈希的类型（可以作为 key）
d[1] = 'value'           # int
d['string'] = 'value'    # str
d[(1, 2)] = 'value'     # tuple（如果元素都可哈希）
d[frozenset([1,2])] = 'value'  # frozenset

# ❌ 不可哈希的类型（不能作为 key）
d[[1, 2]] = 'value'     # TypeError: unhashable type: 'list'
d[{1, 2}] = 'value'     # TypeError: unhashable type: 'set'
d[{'a': 1}] = 'value'   # TypeError: unhashable type: 'dict'
```

**解决方案：**
- 使用 `tuple()` 转换
- 使用 `frozenset()` 转换
- 使用字符串表示

### 2. 检查存在的方式

```python
# ✅ 推荐
if key in d:
    value = d[key]

# ✅ 也可以（但不够Pythonic）
if key in d.keys():
    value = d[key]

# ❌ 不推荐（会创建列表）
if key in list(d.keys()):
    value = d[key]
```

### 3. 遍历字典

```python
# 遍历键
for key in d:
    print(key, d[key])

# 遍历键值对（推荐）
for key, value in d.items():
    print(key, value)

# 只遍历值
for value in d.values():
    print(value)
```

### 4. 字典的默认值

```python
# 使用 get() 提供默认值
value = d.get(key, 0)

# 使用 defaultdict
from collections import defaultdict
d = defaultdict(int)    # 默认值为 0
d = defaultdict(list)   # 默认值为 []
d = defaultdict(set)    # 默认值为 set()
```

### 5. 字典的更新

```python
# 更新单个值
d[key] = value

# 批量更新
d.update({'a': 1, 'b': 2})
d.update([('a', 1), ('b', 2)])

# 合并字典（Python 3.9+）
d = {**d1, **d2}
d = d1 | d2
```

---

## 五、常见错误

### 错误1：先存储再检查（2Sum 问题）

```python
# ❌ 错误
map[n] = i
if complement in map:
    return [map[complement], i]

# ✅ 正确
if complement in map:
    return [map[complement], i]
map[n] = i
```

### 错误2：使用 list 作为 key

```python
# ❌ 错误
key = sorted(s)  # list 不可哈希
map[key] = value

# ✅ 正确
key = tuple(sorted(s))  # tuple 可哈希
map[key] = value
```

### 错误3：忘记检查键是否存在

```python
# ❌ 可能报错
value = d[key]  # KeyError

# ✅ 安全
value = d.get(key, default)
```

### 错误4：在循环中修改字典

```python
# ❌ 可能出错
for key in d:
    if some_condition:
        del d[key]  # RuntimeError: dictionary changed size

# ✅ 正确
keys_to_delete = [key for key in d if some_condition]
for key in keys_to_delete:
    del d[key]
```

---

## 六、性能优化技巧

### 1. 使用 set 而不是 list 进行查找

```python
# ❌ 慢（O(n)）
if item in list_of_items:
    ...

# ✅ 快（O(1)）
if item in set_of_items:
    ...
```

### 2. 使用 defaultdict 简化代码

```python
# ❌ 需要检查
map = {}
if key in map:
    map[key].append(value)
else:
    map[key] = [value]

# ✅ 简化
from collections import defaultdict
map = defaultdict(list)
map[key].append(value)
```

### 3. 使用 Counter 进行计数

```python
# ❌ 手动计数
map = {}
for item in items:
    map[item] = map.get(item, 0) + 1

# ✅ 使用 Counter
from collections import Counter
counter = Counter(items)
```

---

## 七、LeetCode 经典题目

### 查找/配对
- ✅ 1. Two Sum
- ✅ 15. 3Sum
- ✅ 18. 4Sum

### 频率统计
- ✅ 242. Valid Anagram
- ✅ 387. First Unique Character
- ✅ 169. Majority Element
- ✅ 389. Find the Difference

### 分组
- ✅ 49. Group Anagrams

### 映射/模式
- ✅ 290. Word Pattern
- ✅ 205. Isomorphic Strings

### 集合操作
- ✅ 128. Longest Consecutive Sequence
- ✅ 217. Contains Duplicate
- ✅ 219. Contains Duplicate II

### 其他
- ✅ 448. Find All Numbers Disappeared
- ✅ 138. Copy List with Random Pointer

---

## 八、总结

### 核心要点

1. **时间复杂度：** O(1) 平均（查找、插入、删除）
2. **空间复杂度：** O(n)（存储 n 个元素）
3. **适用场景：** 需要快速查找、统计频率、分组

### 选择指南

- **需要计数** → `Counter`
- **需要分组** → `defaultdict(list)`
- **需要快速查找** → `set` 或 `dict`
- **需要双向映射** → 两个 `dict` 或 `dict` + `set`

### 记忆口诀

```
查找配对用字典，频率统计用 Counter
分组问题 defaultdict，集合操作用 set
先检查再存储，tuple 才能做 key
get() 方法要常用，避免 KeyError 报错
```

---

**记住：**
- Dictionary = HashTable = Map（在 Python 中）
- 使用 `dict` 时，你就在使用哈希表
- 时间复杂度：O(1) 平均，O(n) 最坏（哈希冲突）
- 空间复杂度：O(n)































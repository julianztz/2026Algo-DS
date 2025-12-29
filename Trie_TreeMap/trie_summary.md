# Prefix Tree / Trie 性质、使用场景和注意事项总结

## 一、基本概念和性质

### 什么是 Trie（前缀树/字典树）？

Trie（发音为 "try"）是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。它特别适合处理**字符串前缀匹配**问题。

### 核心性质

1. **树形结构**：每个节点代表一个字符，从根到某个节点的路径构成一个字符串
2. **共享前缀**：具有相同前缀的字符串会共享路径，节省存储空间
3. **字符为边**：边（或指针）代表字符，节点存储额外的信息（如是否为单词结尾）
4. **多叉树**：每个节点可能有多个子节点（每个字符对应一个分支）

### 数据结构表示

```python
class TrieNode:
    def __init__(self):
        self.children = {}      # 子节点字典 {char: TrieNode}
        self.is_end = False     # 标记是否s为完整单词
        # 可选：存储额外信息
        # self.value = None     # 存储对应的值
        # self.count = 0        # 存储单词出现次数
```

---

## 二、时间复杂度分析

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| **插入（insert）** | O(m) | m 为字符串长度，需要遍历每个字符 |
| **查找（search）** | O(m) | m 为字符串长度，需要遍历每个字符 |
| **前缀查找（startsWith）** | O(m) | m 为前缀长度 |
| **删除（delete）** | O(m) | m 为字符串长度 |
| **空间复杂度** | O(ALPHABET_SIZE × N × M) | N 为单词数量，M 为平均单词长度 |

**注意：**
- 相比哈希表（O(1)），Trie 的查找是 O(m)，其中 m 是字符串长度
- 但对于前缀查找，Trie 的优势明显（O(m) vs 哈希表的 O(N×M)）
- 实际中，m 通常远小于 N（单词总数），所以 Trie 在前缀匹配场景下更高效

---

## 三、使用场景

### 1. **字符串前缀匹配**

**典型场景：**
- 搜索引擎的自动补全功能
- IDE 的代码补全
- 输入法的词汇提示
- 电话号码簿搜索

**为什么用 Trie？**
- 可以快速查找所有以某个前缀开头的字符串
- 不需要遍历所有字符串，只需要沿着树路径走下去

### 2. **字符串集合的快速查找**

**典型场景：**
- 单词拼写检查
- 词典查询
- 敏感词过滤

**为什么用 Trie？**
- 虽然哈希表也是 O(1)，但 Trie 可以：
  - 节省空间（共享前缀）
  - 支持前缀匹配（哈希表不支持）
  - 按字典序遍历

### 3. **最长公共前缀**

**典型场景：**
- LeetCode 14: Longest Common Prefix

**为什么用 Trie？**
- 插入所有字符串后，最长公共前缀就是从根节点到第一个分叉点的路径

### 4. **字符串排序**

**典型场景：**
- 对大量字符串进行字典序排序

**为什么用 Trie？**
- 先序遍历 Trie 得到的就是字典序排列

### 5. **IP 路由查找**

**典型场景：**
- 网络路由表的最长前缀匹配（Longest Prefix Match）

**为什么用 Trie？**
- 路由表的 IP 地址有层级结构，Trie 天然适合

---

## 四、解决的问题类型

### 问题类型 1：前缀查找类

**核心思路：** 使用 `startsWith()` 方法

#### LeetCode 208: Implement Trie (Prefix Tree)

```python
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True  # ✅ 标记单词结尾
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end  # ✅ 必须检查是否为完整单词
    
    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True  # ✅ 不需要检查 is_end
```

**关键点：**
- ✅ `search()` 必须检查 `is_end`（确保是完整单词）
- ✅ `startsWith()` 不需要检查 `is_end`（只需要前缀存在）
- ✅ 插入时记得标记 `is_end = True`

---

### 问题类型 2：单词搜索/替换类

**核心思路：** 遍历 Trie 树，进行 DFS 或 BFS

#### LeetCode 211: Design Add and Search Words Data Structure

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        def dfs(node: TrieNode, idx: int) -> bool:
            if idx == len(word):
                return node.is_end  # ✅ 必须检查完整单词
            
            char = word[idx]
            if char == '.':
                # 通配符：尝试所有子节点
                for child in node.children.values():
                    if dfs(child, idx + 1):
                        return True
                return False
            else:
                # 普通字符：直接匹配
                if char not in node.children:
                    return False
                return dfs(node.children[char], idx + 1)
        
        return dfs(self.root, 0)
```

**关键点：**
- ✅ 通配符 `.` 需要尝试所有子节点（回溯）
- ✅ 使用 DFS 递归遍历
- ✅ 递归终止条件：`idx == len(word)` 且 `node.is_end == True`

---

### 问题类型 3：前缀匹配 + 结果收集

**核心思路：** 找到前缀节点后，DFS 收集所有以该前缀开头的单词

#### LeetCode 1268: Search Suggestions System

```python
def suggestedProducts(products: List[str], searchWord: str) -> List[List[str]]:
    trie = Trie()
    # 插入所有产品
    for product in products:
        trie.insert(product)
    
    result = []
    prefix = ""
    for char in searchWord:
        prefix += char
        # 找到所有以 prefix 开头的单词（按字典序，最多 3 个）
        suggestions = trie.getWordsWithPrefix(prefix, limit=3)
        result.append(suggestions)
    
    return result

# Trie 中需要添加的方法
def getWordsWithPrefix(self, prefix: str, limit: int = None) -> List[str]:
    # 1. 先找到前缀节点
    node = self.root
    for char in prefix:
        if char not in node.children:
            return []
        node = node.children[char]
    
    # 2. 从该节点开始 DFS，收集所有单词
    result = []
    def dfs(node: TrieNode, path: str):
        if len(result) == limit:  # ✅ 限制结果数量
            return
        if node.is_end:
            result.append(path)
        # 按字典序遍历（如果 children 是 dict，需要排序）
        for char in sorted(node.children.keys()):
            dfs(node.children[char], path + char)
    
    dfs(node, prefix)
    return result
```

**关键点：**
- ✅ 两步操作：先找前缀节点，再 DFS 收集单词
- ✅ 需要按字典序排序（如果使用 dict 存储 children）
- ✅ 可以使用 limit 限制结果数量

---

### 问题类型 4：最长公共前缀

**核心思路：** 插入所有字符串，最长公共前缀 = 从根到第一个分叉点的路径

#### LeetCode 14: Longest Common Prefix

```python
def longestCommonPrefix(strs: List[str]) -> str:
    if not strs:
        return ""
    
    trie = Trie()
    for s in strs:
        if not s:  # ✅ 处理空字符串
            return ""
        trie.insert(s)
    
    # 找到第一个分叉点
    node = trie.root
    prefix = ""
    while len(node.children) == 1 and not node.is_end:
        # ✅ 只有一个子节点 且 不是单词结尾
        char = next(iter(node.children.keys()))
        prefix += char
        node = node.children[char]
    
    return prefix
```

**关键点：**
- ✅ 从根节点开始，沿着唯一路径走
- ✅ 遇到分叉（`len(node.children) > 1`）或单词结尾（`node.is_end == True`）时停止

---

### 问题类型 5：单词替换

**核心思路：** 查找每个单词的最短前缀（在 Trie 中能找到的最短单词）

#### LeetCode 648: Replace Words

```python
def replaceWords(dictionary: List[str], sentence: str) -> str:
    trie = Trie()
    for word in dictionary:
        trie.insert(word)
    
    words = sentence.split()
    result = []
    
    for word in words:
        # 查找最短前缀
        prefix = trie.findShortestPrefix(word)
        result.append(prefix if prefix else word)  # ✅ 找不到则用原词
    
    return " ".join(result)

# Trie 中需要添加的方法
def findShortestPrefix(self, word: str) -> str:
    node = self.root
    prefix = ""
    for char in word:
        if char not in node.children:
            return None  # 找不到前缀
        node = node.children[char]
        prefix += char
        if node.is_end:  # ✅ 找到最短前缀
            return prefix
    return None
```

**关键点：**
- ✅ 遍历字符串，一旦遇到 `is_end == True` 的节点就返回
- ✅ 找不到前缀时返回原词

---

## 五、注意事项和常见错误

### 1. ❌ 忘记标记单词结尾

```python
# ❌ 错误：插入后忘记标记 is_end
def insert(self, word: str) -> None:
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    # 忘记：node.is_end = True

# ✅ 正确
def insert(self, word: str) -> None:
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end = True  # ✅ 必须标记
```

**影响：** `search()` 会返回错误结果，因为无法区分完整单词和前缀

---

### 2. ❌ search() 和 startsWith() 混淆

```python
# ❌ 错误：search() 没有检查 is_end
def search(self, word: str) -> bool:
    node = self.root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    return True  # ❌ 错误！"app" 不是单词，但 "apple" 是，这样会误判

# ✅ 正确
def search(self, word: str) -> bool:
    node = self.root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    return node.is_end  # ✅ 必须检查是否为完整单词
```

**区别：**
- `search()`: 检查**完整单词**是否存在 → 需要 `node.is_end == True`
- `startsWith()`: 检查**前缀**是否存在 → 不需要检查 `is_end`

---

### 3. ❌ 节点为空指针访问

```python
# ❌ 错误：没有检查节点是否存在就访问
def search(self, word: str) -> bool:
    node = self.root
    for char in word:
        node = node.children[char]  # ❌ KeyError if char not in children
    return node.is_end

# ✅ 正确
def search(self, word: str) -> bool:
    node = self.root
    for char in word:
        if char not in node.children:  # ✅ 先检查
            return False
        node = node.children[char]
    return node.is_end
```

---

### 4. ❌ 字符串为空的情况

```python
# ❌ 可能的问题：空字符串
def insert(self, word: str) -> None:
    if not word:  # ✅ 处理空字符串
        self.root.is_end = True  # 空字符串作为单词
        return
    # ... 正常插入逻辑

def search(self, word: str) -> bool:
    if not word:
        return self.root.is_end  # ✅ 检查根节点
    # ... 正常查找逻辑
```

---

### 5. ❌ 字典序问题

```python
# ❌ 问题：使用 dict 存储 children，遍历顺序不确定
def getAllWords(self, node: TrieNode) -> List[str]:
    result = []
    if node.is_end:
        result.append("")
    for char, child in node.children.items():  # ❌ 顺序不确定
        for word in self.getAllWords(child):
            result.append(char + word)
    return result

# ✅ 正确：需要排序
def getAllWords(self, node: TrieNode) -> List[str]:
    result = []
    if node.is_end:
        result.append("")
    for char in sorted(node.children.keys()):  # ✅ 按字典序
        child = node.children[char]
        for word in self.getAllWords(child):
            result.append(char + word)
    return result
```

**解决方案：**
- 使用 `sorted(node.children.keys())` 按字典序遍历
- 或者使用 `collections.OrderedDict`（但需要按 key 排序）
- 或者使用数组 `children = [None] * 26`（适合小写字母）

---

### 6. ❌ 内存泄漏（删除操作）

```python
# ❌ 问题：删除单词后，无用节点没有被清理
def delete(self, word: str) -> bool:
    node = self.root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    if not node.is_end:
        return False
    node.is_end = False  # ❌ 只标记，不删除节点
    return True

# ✅ 正确：递归删除无用节点
def delete(self, word: str) -> bool:
    def _delete(node: TrieNode, word: str, idx: int) -> bool:
        if idx == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0  # ✅ 如果无子节点，可以删除
        
        char = word[idx]
        if char not in node.children:
            return False
        
        child = node.children[char]
        should_delete = _delete(child, word, idx + 1)
        
        if should_delete:
            del node.children[char]  # ✅ 删除子节点
            return len(node.children) == 0 and not node.is_end
        
        return False
    
    return _delete(self.root, word, 0)
```

**关键点：**
- ✅ 删除时从叶子节点向上递归
- ✅ 只有当节点没有子节点且不是单词结尾时，才能删除
- ✅ 注意：通常在实际应用中，删除操作可以只标记 `is_end = False`，不真正删除节点（节省时间，但占用空间）

---

### 7. ❌ 重复插入的处理

```python
# 问题：重复插入同一个单词
# 选项1：允许重复（可以记录 count）
class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0  # ✅ 记录出现次数

def insert(self, word: str) -> None:
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.count += 1  # ✅ 增加计数

# 选项2：不允许重复（使用 is_end 标记）
def insert(self, word: str) -> None:
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end = True  # ✅ 简单标记，重复插入不影响
```

---

## 六、优化技巧

### 1. 使用数组代替字典（固定字符集）

**适用场景：** 只有小写字母（26个）或 ASCII 字符（128个）

```python
# ✅ 优化：使用数组，访问更快
class TrieNode:
    def __init__(self):
        self.children = [None] * 26  # 26 个小写字母
        self.is_end = False

class Trie:
    def _char_to_index(self, char: str) -> int:
        return ord(char) - ord('a')
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            idx = self._char_to_index(char)
            if node.children[idx] is None:
                node.children[idx] = TrieNode()
            node = node.children[idx]
        node.is_end = True
```

**优点：**
- ✅ 访问更快（数组索引 vs 字典查找）
- ✅ 内存连续，缓存友好
- ✅ 按字典序遍历时不需要排序

**缺点：**
- ❌ 只适合固定字符集
- ❌ 字符集大时浪费空间（如 Unicode）

---

### 2. 压缩 Trie（Radix Tree / Patricia Tree）

**适用场景：** 字符串集合很大，且有大量共享前缀

**原理：** 将只有一个子节点的节点合并

```python
# 压缩 Trie 节点：存储字符串片段而不是单个字符
class CompressedTrieNode:
    def __init__(self):
        self.children = {}  # {prefix: TrieNode}
        self.is_end = False
```

**优点：**
- ✅ 减少节点数量，节省空间
- ✅ 减少查找深度

**缺点：**
- ❌ 实现复杂
- ❌ 插入和删除操作更复杂

---

### 3. 双向 Trie（Double Trie）

**适用场景：** 需要同时支持前缀和后缀匹配

**原理：** 同时维护正向和反向的 Trie

```python
class DoubleTrie:
    def __init__(self):
        self.forward = Trie()   # 正向 Trie
        self.backward = Trie()  # 反向 Trie（存储反转后的字符串）
    
    def insert(self, word: str) -> None:
        self.forward.insert(word)
        self.backward.insert(word[::-1])  # 反转后插入
    
    def searchSuffix(self, suffix: str) -> bool:
        return self.backward.startsWith(suffix[::-1])
```

---

## 七、Trie vs 其他数据结构

### Trie vs HashTable

| 特性 | Trie | HashTable |
|------|------|-----------|
| **完整单词查找** | O(m) | O(1) 平均 |
| **前缀查找** | O(m) | O(N×M) 需要遍历所有 |
| **空间复杂度** | O(ALPHABET×N×M) | O(N×M) |
| **共享前缀** | ✅ 共享 | ❌ 不共享 |
| **字典序遍历** | ✅ 容易 | ❌ 需要排序 |
| **适用场景** | 前缀匹配、自动补全 | 精确查找、频繁更新 |

**选择建议：**
- **需要前缀匹配** → Trie
- **只需要精确查找** → HashTable
- **需要字典序遍历** → Trie

---

### Trie vs 排序数组 + 二分查找

| 特性 | Trie | 排序数组 + 二分 |
|------|------|----------------|
| **查找** | O(m) | O(log N) |
| **前缀查找** | O(m) | O(N) 需要遍历 |
| **插入** | O(m) | O(N) 需要移动元素 |
| **空间** | O(ALPHABET×N×M) | O(N×M) |
| **适用场景** | 动态插入、前缀匹配 | 静态集合、精确查找 |

---

## 八、经典 LeetCode 题目

### 基础题
- ✅ **208. Implement Trie (Prefix Tree)** - 实现基础 Trie
- ✅ **211. Design Add and Search Words Data Structure** - 支持通配符的 Trie

### 前缀匹配
- ✅ **1268. Search Suggestions System** - 前缀匹配 + 结果收集
- ✅ **720. Longest Word in Dictionary** - 前缀匹配判断

### 最长公共前缀
- ✅ **14. Longest Common Prefix** - 使用 Trie 找最长公共前缀

### 单词替换
- ✅ **648. Replace Words** - 最短前缀替换

### 单词搜索
- ✅ **212. Word Search II** - 二维网格中搜索单词（Trie + DFS）
- ✅ **421. Maximum XOR of Two Numbers in an Array** - 位运算 Trie

### 高级应用
- ✅ **1032. Stream of Characters** - 流式字符串匹配（反向 Trie）
- ✅ **642. Design Search Autocomplete System** - 自动补全系统

---

## 九、实现模板

### 标准实现（使用字典）

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

### 优化实现（使用数组，仅小写字母）

```python
class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def _char_to_index(self, char: str) -> int:
        return ord(char) - ord('a')
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            idx = self._char_to_index(char)
            if node.children[idx] is None:
                node.children[idx] = TrieNode()
            node = node.children[idx]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            idx = self._char_to_index(char)
            if node.children[idx] is None:
                return False
            node = node.children[idx]
        return node.is_end
    
    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            idx = self._char_to_index(char)
            if node.children[idx] is None:
                return False
            node = node.children[idx]
        return True
```

---

## 十、总结

### 核心要点

1. **时间复杂度：**
   - 插入/查找/删除：O(m)，m 为字符串长度
   - 前缀匹配：O(m)，这是 Trie 的核心优势

2. **空间复杂度：**
   - O(ALPHABET_SIZE × N × M)
   - 通过共享前缀节省空间

3. **适用场景：**
   - ✅ 前缀匹配、自动补全
   - ✅ 字符串集合查找
   - ✅ 字典序相关操作
   - ❌ 只需要精确查找时，哈希表更简单高效

### 记忆口诀

```
前缀匹配用 Trie，共享路径省空间
插入查找都是 O(m)，前缀匹配最擅长
is_end 标记不能忘，search 和 startsWith 要区分
字典存储灵活用，数组存储更高效
```

### 何时选择 Trie？

**✅ 选择 Trie：**
- 需要前缀匹配（如自动补全）
- 需要按字典序遍历
- 字符串集合有大量共享前缀
- 需要支持通配符匹配

**❌ 不选择 Trie：**
- 只需要精确查找（用 HashTable）
- 字符串集合很小（用简单的 set 或 list）
- 频繁的插入和删除（HashTable 更高效）

---

**记住：**
- Trie = Prefix Tree = 前缀树 = 字典树
- 核心优势是**前缀匹配**，而不是精确查找
- 在需要前缀匹配的场景下，Trie 是不可替代的数据结构

















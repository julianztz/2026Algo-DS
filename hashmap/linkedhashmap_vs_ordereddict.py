# -*- coding: utf-8 -*-
"""
LinkedHashMap vs OrderedDict 的实现对比
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from collections import OrderedDict

print("=" * 70)
print("LinkedHashMap vs OrderedDict 的实现对比")
print("=" * 70)

print("""
【你的理解完全正确！】

其他语言（如 Java）：
  - 需要手动实现 LinkedHashMap
  - 将 key-value 包装成 Node
  - 用双向链表维护顺序
  - 需要手动管理链表的添加/删除

Python 的 OrderedDict：
  - 已经内置了顺序维护
  - 不需要手动实现链表
  - 直接使用即可
""")

print("\n" + "=" * 70)
print("1. Java 的 LinkedHashMap 实现思路")
print("=" * 70)

print("""
【Java 需要手动实现】

class LinkedHashMap {
    // 1. 定义 Node（包含 key, value, prev, next）
    class Node {
        K key;
        V value;
        Node prev;  // 双向链表的前驱
        Node next;  // 双向链表的后继
    }
    
    // 2. 使用 HashMap 存储 key -> Node 的映射
    HashMap<K, Node> map;
    
    // 3. 维护双向链表的头尾指针
    Node head;  // 链表头（最久未使用）
    Node tail;  // 链表尾（最近使用）
    
    // 4. 每次操作需要：
    //    - 更新 HashMap
    //    - 更新双向链表（添加/删除/移动节点）
    
    void put(K key, V value) {
        if (key in map) {
            // 更新值
            Node node = map.get(key);
            node.value = value;
            // 移动到末尾（需要手动操作链表）
            removeFromList(node);
            addToTail(node);
        } else {
            // 创建新节点
            Node node = new Node(key, value);
            // 添加到 HashMap
            map.put(key, node);
            // 添加到链表末尾（需要手动操作）
            addToTail(node);
            
            if (size >= capacity) {
                // 移除最久未使用的（链表头）
                Node lru = head;
                removeFromList(lru);
                map.remove(lru.key);
            }
        }
    }
}

【关键点】
  - 需要手动定义 Node 类
  - 需要手动维护双向链表
  - 需要手动实现链表的添加/删除/移动操作
  - 代码复杂，容易出错
""")

print("\n" + "=" * 70)
print("2. Python 的 OrderedDict 实现")
print("=" * 70)

print("""
【Python 已经内置实现】

from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()  # ✅ 直接使用，不需要手动实现链表
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # ✅ 内置方法，自动维护顺序
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)  # ✅ 内置方法
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)  # ✅ 内置方法
            self.cache[key] = value
            self.cache.move_to_end(key)  # ✅ 内置方法

【关键点】
  - 不需要定义 Node 类
  - 不需要手动维护链表
  - OrderedDict 内部已经实现了双向链表
  - 代码简洁，不容易出错
""")

print("\n" + "=" * 70)
print("3. OrderedDict 的内部实现（简化理解）")
print("=" * 70)

print("""
OrderedDict 内部实现（简化版）：

class OrderedDict:
    def __init__(self):
        self._map = {}  # 哈希表：key -> Node
        self._head = None  # 双向链表头
        self._tail = None  # 双向链表尾
    
    class _Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None
    
    def move_to_end(self, key):
        # 内部实现：自动操作双向链表
        node = self._map[key]
        # 1. 从当前位置移除
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        # 2. 添加到末尾
        node.prev = self._tail
        self._tail.next = node
        self._tail = node
    
    def popitem(self, last=True):
        # 内部实现：自动操作双向链表
        if last:
            node = self._tail  # 最后一个
        else:
            node = self._head  # 第一个
        # 从链表中移除
        # 从 map 中移除
        return (node.key, node.value)

【关键理解】
  - OrderedDict 内部已经实现了双向链表
  - 我们只需要调用高级 API（move_to_end, popitem）
  - 不需要关心底层实现细节
""")

print("\n" + "=" * 70)
print("4. 代码复杂度对比")
print("=" * 70)

print("""
【Java LinkedHashMap 实现】
  代码行数：~150-200 行
  需要实现：
    - Node 类定义
    - 双向链表的添加/删除/移动
    - HashMap 和链表的同步维护
    - 边界情况处理
  
  优点：
    ✅ 完全控制，可以自定义
    ✅ 理解底层实现
  
  缺点：
    ❌ 代码复杂
    ❌ 容易出错
    ❌ 需要大量测试

【Python OrderedDict 实现】
  代码行数：~20 行
  只需要：
    - 调用 OrderedDict 的 API
    - move_to_end()
    - popitem(last=False)
  
  优点：
    ✅ 代码简洁
    ✅ 不容易出错
    ✅ 经过充分测试
  
  缺点：
    ⚠️ 对底层实现理解较少（但通常不需要）
""")

print("\n" + "=" * 70)
print("5. 实际代码对比")
print("=" * 70)

print("""
【Java 风格的实现（伪代码）】

class LRUCache {
    class Node {
        int key, value;
        Node prev, next;
    }
    
    HashMap<Integer, Node> map;
    Node head, tail;
    int capacity;
    
    void addToTail(Node node) {
        // 手动操作链表
        node.prev = tail;
        tail.next = node;
        tail = node;
    }
    
    void removeFromList(Node node) {
        // 手动操作链表
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    void moveToEnd(Node node) {
        removeFromList(node);
        addToTail(node);
    }
    
    // ... 大量链表操作代码
}

【Python 实现】

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()  # ✅ 一行搞定
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # ✅ 一行搞定
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)  # ✅ 一行搞定
            self.cache[key] = value
            self.cache.move_to_end(key)
""")

print("\n" + "=" * 70)
print("6. 为什么 Python 更简单？")
print("=" * 70)

print("""
【Python 的优势】

1. OrderedDict 已经内置了双向链表
   - 不需要手动定义 Node
   - 不需要手动维护链表
   - 内部已经实现了所有链表操作

2. 提供了高级 API
   - move_to_end(): 自动处理链表的移动
   - popitem(last=False): 自动处理链表的删除
   - 我们只需要调用，不需要关心实现

3. 经过充分测试
   - 是 Python 标准库的一部分
   - 经过大量测试，稳定可靠

【其他语言的情况】

Java:
  - LinkedHashMap 也是标准库的一部分
  - 但如果不使用标准库，需要手动实现
  - 面试中可能需要手写实现

C++:
  - 没有内置的 LinkedHashMap
  - 需要手动实现或使用第三方库

Python:
  - OrderedDict 是标准库
  - 直接使用即可
  - 面试中通常允许使用标准库
""")

print("\n" + "=" * 70)
print("7. 学习建议")
print("=" * 70)

print("""
【理解底层实现（可选）】
  - 了解 OrderedDict 内部使用双向链表
  - 理解哈希表 + 双向链表的组合
  - 有助于理解 LRU Cache 的原理

【实际使用（推荐）】
  - 直接使用 OrderedDict
  - 调用 move_to_end() 和 popitem(last=False)
  - 不需要手动实现链表

【面试准备】
  - Python: 可以使用 OrderedDict（通常允许）
  - Java: 可能需要手写 LinkedHashMap
  - 理解原理即可，不需要手写实现
""")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)

print("""
✅ 你的理解完全正确！

【其他语言（如 Java）】
  - 需要手动实现 LinkedHashMap
  - 将 key-value 包装成 Node
  - 用双向链表维护顺序
  - 需要手动管理链表的添加/删除
  - 代码复杂（~150-200 行）

【Python 的 OrderedDict】
  - 已经内置了顺序维护
  - 内部使用双向链表（但我们不需要关心）
  - 提供了高级 API（move_to_end, popitem）
  - 代码简洁（~20 行）
  - 不需要手动实现链表

【关键理解】
  - OrderedDict 内部已经实现了双向链表
  - 我们只需要调用 API，不需要手动实现
  - 这是 Python 的优势之一！
""")






























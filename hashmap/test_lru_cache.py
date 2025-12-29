# -*- coding: utf-8 -*-
"""
测试 LRU Cache 实现的问题
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from collections import OrderedDict

# 你的实现（有问题）
class LRUCache_WRONG:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) == self.capacity:
                self.cache.pop(0)  # ❌ 问题：OrderedDict 不支持 pop(0)
            self.cache[key] = value
            self.cache.move_to_end(key)

# 正确的实现
class LRUCache_CORRECT:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # 移动到末尾（最近使用）
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:  # ✅ 使用 >= 更安全
                self.cache.popitem(last=False)  # ✅ 弹出第一个元素（最久未使用）
            self.cache[key] = value
            self.cache.move_to_end(key)

print("=" * 70)
print("LRU Cache 实现问题分析")
print("=" * 70)

print("\n【你的实现问题】")
print("""
问题1：self.cache.pop(0) ❌
  - OrderedDict 不支持索引访问（pop(0)）
  - OrderedDict 不是列表，不能使用索引
  - 应该使用 popitem(last=False) 弹出第一个元素

问题2：len(self.cache) == self.capacity
  - 应该使用 >= 更安全
  - 虽然理论上不会超过，但 >= 更健壮
""")

print("\n" + "=" * 70)
print("OrderedDict 的 pop 方法")
print("=" * 70)

od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print(f"初始: {od}")

print("\n【OrderedDict 支持的方法】")

# pop(key): 弹出指定 key
try:
    value = od.pop('b')
    print(f"  od.pop('b'): {value}, 剩余: {od}")
except Exception as e:
    print(f"  od.pop('b'): ❌ {e}")

# popitem(): 弹出最后一个
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
last = od.popitem()
print(f"  od.popitem(): 弹出 {last}, 剩余: {od}")

# popitem(last=False): 弹出第一个
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
first = od.popitem(last=False)
print(f"  od.popitem(last=False): 弹出 {first}, 剩余: {od}")

# pop(0): 不支持
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
try:
    od.pop(0)  # ❌ 这会报错
except Exception as e:
    print(f"  od.pop(0): ❌ {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("为什么不能 pop(0)？")
print("=" * 70)

print("""
OrderedDict 不是列表，不支持索引访问：

❌ 错误理解：
  OrderedDict 像列表一样，可以用索引访问
  od[0] 或 od.pop(0)

✅ 正确理解：
  OrderedDict 是字典，用 key 访问
  od['key'] 或 od.pop('key')
  
  要弹出第一个元素，使用：
  od.popitem(last=False)  # 弹出第一个（最久未使用的）
""")

print("\n" + "=" * 70)
print("测试你的实现")
print("=" * 70)

print("\n【错误实现测试】")
try:
    lru_wrong = LRUCache_WRONG(2)
    lru_wrong.put(1, 1)
    lru_wrong.put(2, 2)
    print(f"  初始: {list(lru_wrong.cache.keys())}")
    lru_wrong.put(3, 3)  # 应该移除 1
    print(f"  put(3) 后: {list(lru_wrong.cache.keys())}")
except Exception as e:
    print(f"  ❌ 错误: {type(e).__name__}: {e}")

print("\n【正确实现测试】")
lru_correct = LRUCache_CORRECT(2)
lru_correct.put(1, 1)
lru_correct.put(2, 2)
print(f"  初始: {list(lru_correct.cache.keys())}")

result = lru_correct.get(1)
print(f"  get(1): {result}, cache: {list(lru_correct.cache.keys())}")

lru_correct.put(3, 3)  # 应该移除 2（最久未使用）
print(f"  put(3) 后: {list(lru_correct.cache.keys())}")

result = lru_correct.get(2)
print(f"  get(2): {result} (应该返回 -1，因为已被移除)")

lru_correct.put(4, 4)  # 应该移除 1
print(f"  put(4) 后: {list(lru_correct.cache.keys())}")

print("\n" + "=" * 70)
print("正确的实现")
print("=" * 70)

print("""
def put(self, key: int, value: int) -> None:
    if key in self.cache:
        self.cache[key] = value
        self.cache.move_to_end(key)
    else:
        if len(self.cache) >= self.capacity:  # ✅ >= 更安全
            self.cache.popitem(last=False)  # ✅ 弹出第一个元素
        self.cache[key] = value
        self.cache.move_to_end(key)
""")

print("\n" + "=" * 70)
print("关键理解")
print("=" * 70)

print("""
【OrderedDict 的操作】

1. 访问元素：
   ✅ od['key'] 或 od.get('key')
   ❌ od[0]  # 不支持索引

2. 弹出元素：
   ✅ od.pop('key')  # 弹出指定 key
   ✅ od.popitem()  # 弹出最后一个
   ✅ od.popitem(last=False)  # 弹出第一个
   ❌ od.pop(0)  # 不支持索引

3. LRU Cache 中：
   - 第一个元素 = 最久未使用的
   - 最后一个元素 = 最近使用的
   - 使用 popitem(last=False) 移除最久未使用的
""")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)

print("""
❌ 你的问题：
  1. self.cache.pop(0)  → OrderedDict 不支持索引访问
  2. len(self.cache) == self.capacity  → 应该用 >=

✅ 正确方式：
  1. self.cache.popitem(last=False)  → 弹出第一个元素
  2. len(self.cache) >= self.capacity  → 更安全

💡 关键理解：
  - OrderedDict 是字典，不是列表
  - 不能用索引访问（pop(0)）
  - 要用 popitem(last=False) 弹出第一个元素
""")






























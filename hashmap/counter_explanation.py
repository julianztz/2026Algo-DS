# -*- coding: utf-8 -*-
"""
Counter 详解和 isAnagram 函数分析
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from collections import Counter

# 你的实现
def isAnagram_Counter(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# 手动实现（对比）
def isAnagram_Manual(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    
    map = dict()
    for l in s:
        map[l] = map.get(l, 0) + 1
    
    for l in t:
        map[l] = map.get(l, 0) - 1
        if map[l] < 0:
            return False
    
    return True

# 排序方法（对比）
def isAnagram_Sorted(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)

print("=" * 70)
print("你的 isAnagram 函数分析")
print("=" * 70)

print("""
你的实现：
  def isAnagram(s: str, t: str) -> bool:
      return Counter(s) == Counter(t)

✅ 优点：
  - 代码简洁（一行解决）
  - 使用 Counter 自动计数
  - Counter 支持直接比较

✅ 正确性：
  - Counter(s) 统计 s 中每个字符的出现次数
  - Counter(t) 统计 t 中每个字符的出现次数
  - 如果两个 Counter 相等，说明字符频率相同 → 是 anagram

✅ 时间复杂度：O(n)
✅ 空间复杂度：O(n)
""")

print("\n" + "=" * 70)
print("Counter 详解")
print("=" * 70)

print("""
【什么是 Counter？】

Counter 是 Python collections 模块中的一个类
- 专门用于计数
- 是 dict 的子类
- 自动统计可迭代对象中元素的出现次数
""")

# 演示 Counter 的基本用法
print("\n【Counter 基本用法】")

# 1. 从字符串创建
s = "hello"
counter_s = Counter(s)
print(f"Counter('{s}') = {counter_s}")
print(f"  说明：自动统计每个字符的出现次数")

# 2. 从列表创建
nums = [1, 2, 2, 3, 3, 3]
counter_nums = Counter(nums)
print(f"\nCounter({nums}) = {counter_nums}")
print(f"  说明：自动统计每个数字的出现次数")

# 3. 访问计数
print(f"\n访问计数：")
print(f"  counter_s['l'] = {counter_s['l']}")
print(f"  counter_s['x'] = {counter_s['x']}  # 不存在的键返回 0（不会报错）")

# 4. 常用方法
print(f"\n常用方法：")
print(f"  counter_s.most_common(2) = {counter_s.most_common(2)}")
print(f"  counter_s.keys() = {list(counter_s.keys())}")
print(f"  counter_s.values() = {list(counter_s.values())}")
print(f"  counter_s.items() = {list(counter_s.items())}")

# 5. Counter 运算
print(f"\nCounter 运算：")
c1 = Counter('aab')
c2 = Counter('abc')
print(f"  c1 = Counter('aab') = {c1}")
print(f"  c2 = Counter('abc') = {c2}")
print(f"  c1 + c2 = {c1 + c2}  # 相加")
print(f"  c1 - c2 = {c1 - c2}  # 相减（只保留正数）")
print(f"  c1 & c2 = {c1 & c2}  # 交集（取最小值）")
print(f"  c1 | c2 = {c1 | c2}  # 并集（取最大值）")

# 6. Counter 比较
print(f"\nCounter 比较：")
c3 = Counter('aab')
c4 = Counter('aba')
print(f"  c3 = Counter('aab') = {c3}")
print(f"  c4 = Counter('aba') = {c4}")
print(f"  c3 == c4 = {c3 == c4}  # ✅ Counter 支持直接比较")

print("\n" + "=" * 70)
print("isAnagram 函数对比")
print("=" * 70)

test_cases = [
    ("anagram", "nagaram", True),
    ("rat", "car", False),
    ("listen", "silent", True),
    ("a", "a", True),
    ("a", "ab", False),
    ("", "", True),
]

print("\n【Counter 方法测试】")
for s, t, expected in test_cases:
    result = isAnagram_Counter(s, t)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}' vs '{t}' → {result} (expected: {expected})")

print("\n【手动方法测试】")
for s, t, expected in test_cases:
    result = isAnagram_Manual(s, t)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}' vs '{t}' → {result} (expected: {expected})")

print("\n【排序方法测试】")
for s, t, expected in test_cases:
    result = isAnagram_Sorted(s, t)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}' vs '{t}' → {result} (expected: {expected})")

print("\n" + "=" * 70)
print("Counter vs 手动实现")
print("=" * 70)

print("""
【Counter 方法】
  def isAnagram(s: str, t: str) -> bool:
      return Counter(s) == Counter(t)

  优点：
    ✅ 代码简洁（一行）
    ✅ 自动处理计数
    ✅ Counter 支持直接比较
    
  缺点：
    ⚠️ 需要导入 Counter
    ⚠️ 可能稍微慢一点（但差异很小）

【手动实现】
  def isAnagram(s: str, t: str) -> bool:
      if len(s) != len(t):
          return False
      map = dict()
      for l in s:
          map[l] = map.get(l, 0) + 1
      for l in t:
          map[l] = map.get(l, 0) - 1
          if map[l] < 0:
              return False
      return True

  优点：
    ✅ 不需要额外导入
    ✅ 可以提前返回（如果长度不同）
    ✅ 更明确的逻辑
    
  缺点：
    ⚠️ 代码更长
    ⚠️ 需要手动处理计数
""")

print("\n" + "=" * 70)
print("Counter 的底层实现")
print("=" * 70)

print("""
Counter 底层也是使用字典（哈希表）实现：

Counter('hello') 内部过程：
  1. 创建一个空字典
  2. 遍历字符串 'hello'
  3. 对每个字符：
     - 如果字符在字典中，计数 +1
     - 如果字符不在字典中，初始化为 1
  4. 返回 Counter 对象（本质是字典）

所以：
  Counter(s) == Counter(t)
  等价于：
    统计 s 的字符频率 == 统计 t 的字符频率
""")

print("\n" + "=" * 70)
print("Counter 的更多用法")
print("=" * 70)

print("""
【1. 统计字符频率】
  Counter('hello') → Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

【2. 统计单词频率】
  Counter(['apple', 'banana', 'apple']) → Counter({'apple': 2, 'banana': 1})

【3. 找出最常见的元素】
  Counter('hello').most_common(2) → [('l', 2), ('h', 1)]

【4. 更新计数】
  c = Counter('aab')
  c.update('abc')  # 添加新计数
  # Counter({'a': 3, 'b': 2, 'c': 1})

【5. 减法运算】
  c1 = Counter('aab')
  c2 = Counter('abc')
  c1 - c2  # Counter({'a': 1})  # 只保留正数
""")

print("\n" + "=" * 70)
print("性能对比")
print("=" * 70)

import time

s = "anagram" * 1000
t = "nagaram" * 1000

# Counter 方法
start = time.time()
for _ in range(1000):
    isAnagram_Counter(s, t)
time_counter = time.time() - start

# 手动方法
start = time.time()
for _ in range(1000):
    isAnagram_Manual(s, t)
time_manual = time.time() - start

# 排序方法
start = time.time()
for _ in range(1000):
    isAnagram_Sorted(s, t)
time_sorted = time.time() - start

print(f"\n性能测试（1000次，字符串长度 {len(s)}）：")
print(f"  Counter 方法: {time_counter:.4f} 秒")
print(f"  手动方法:     {time_manual:.4f} 秒")
print(f"  排序方法:     {time_sorted:.4f} 秒")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)

print("""
✅ 你的 isAnagram 函数完全正确！

使用 Counter 的优点：
  1. 代码简洁（一行解决）
  2. 自动计数，不需要手动处理
  3. Counter 支持直接比较（==）
  4. 可读性好

Counter 的核心用法：
  - Counter(iterable) → 统计元素出现次数
  - Counter 是 dict 的子类
  - 支持 +, -, &, | 运算
  - 支持 == 比较
  - 不存在的键返回 0（不会报错）

时间复杂度：O(n)
空间复杂度：O(n)

你的实现是最简洁、最Pythonic的方式！✅
""")































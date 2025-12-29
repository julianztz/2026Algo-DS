# -*- coding: utf-8 -*-
"""
在 Dictionary 中随机返回 key-value pair，O(1) 时间复杂度
"""

import sys
import io
import random

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("随机返回 Dictionary 的 key-value pair，O(1) 时间复杂度")
print("=" * 70)

print("\n【你的思路】")
print("""
1. 用 self.key_array 维护一个连续的 key 数组
2. 随机取一个 index，访问对应的 key
3. 用这个 key 去访问 dictionary

✅ 思路基本正确！
⚠️ 但需要考虑删除操作时的维护问题
""")

print("\n" + "=" * 70)
print("1. 你的思路的问题分析")
print("=" * 70)

print("""
【问题1：删除元素时如何维护 key_array？】

如果直接删除数组中的元素：
  - 方法1：list.remove(key) → O(n) 时间复杂度 ❌
  - 方法2：标记为 None → 随机访问时可能访问到已删除的元素 ❌
  - 方法3：移动元素填补空洞 → O(n) 时间复杂度 ❌

【问题2：如何保证 O(1) 删除？】

需要：
  - 知道 key 在数组中的位置（index）
  - 快速删除并维护数组的连续性
""")

print("\n" + "=" * 70)
print("2. 优化方案：使用 key -> index 映射")
print("=" * 70)

print("""
【核心思路】

数据结构：
  1. self.dict: 存储 key -> value
  2. self.key_array: 存储 key 的数组
  3. self.key_to_index: 存储 key -> index 的映射

操作：
  - 插入：添加到数组末尾，O(1)
  - 删除：将最后一个元素移到被删除的位置，O(1)
  - 随机访问：随机取 index，O(1)
""")

# 实现
class RandomDict:
    def __init__(self):
        self.dict = {}  # key -> value
        self.key_array = []  # 存储 key 的数组
        self.key_to_index = {}  # key -> index 的映射
    
    def put(self, key, value):
        """插入/更新，O(1)"""
        if key in self.dict:
            # 已存在，只更新值
            self.dict[key] = value
        else:
            # 新元素
            self.dict[key] = value
            self.key_to_index[key] = len(self.key_array)
            self.key_array.append(key)
    
    def remove(self, key):
        """删除，O(1)"""
        if key not in self.dict:
            return False
        
        # 获取要删除的 key 的 index
        index = self.key_to_index[key]
        last_key = self.key_array[-1]
        
        # 将最后一个元素移到被删除的位置
        self.key_array[index] = last_key
        self.key_to_index[last_key] = index
        
        # 删除最后一个元素
        self.key_array.pop()
        del self.key_to_index[key]
        del self.dict[key]
        
        return True
    
    def get(self, key):
        """获取值，O(1)"""
        return self.dict.get(key)
    
    def getRandom(self):
        """随机返回 key-value pair，O(1)"""
        if not self.key_array:
            return None
        
        # 随机取一个 index
        random_index = random.randint(0, len(self.key_array) - 1)
        random_key = self.key_array[random_index]
        random_value = self.dict[random_key]
        
        return (random_key, random_value)
    
    def size(self):
        return len(self.key_array)

print("\n" + "=" * 70)
print("3. 完整实现")
print("=" * 70)

print("""
class RandomDict:
    def __init__(self):
        self.dict = {}  # key -> value
        self.key_array = []  # 存储 key 的数组
        self.key_to_index = {}  # key -> index 的映射
    
    def put(self, key, value):
        if key in self.dict:
            self.dict[key] = value
        else:
            self.dict[key] = value
            self.key_to_index[key] = len(self.key_array)
            self.key_array.append(key)
    
    def remove(self, key):
        if key not in self.dict:
            return False
        
        index = self.key_to_index[key]
        last_key = self.key_array[-1]
        
        # 将最后一个元素移到被删除的位置
        self.key_array[index] = last_key
        self.key_to_index[last_key] = index
        
        # 删除最后一个元素
        self.key_array.pop()
        del self.key_to_index[key]
        del self.dict[key]
        
        return True
    
    def getRandom(self):
        if not self.key_array:
            return None
        
        random_index = random.randint(0, len(self.key_array) - 1)
        random_key = self.key_array[random_index]
        return (random_key, self.dict[random_key])
""")

print("\n" + "=" * 70)
print("4. 测试演示")
print("=" * 70)

rd = RandomDict()

# 插入元素
print("【插入元素】")
rd.put('a', 1)
rd.put('b', 2)
rd.put('c', 3)
rd.put('d', 4)
print(f"  插入后: dict={rd.dict}, array={rd.key_array}, index_map={rd.key_to_index}")

# 随机访问
print("\n【随机访问】")
for i in range(5):
    result = rd.getRandom()
    print(f"  第 {i+1} 次随机: {result}")

# 删除元素
print("\n【删除元素 'b'】")
rd.remove('b')
print(f"  删除后: dict={rd.dict}, array={rd.key_array}, index_map={rd.key_to_index}")
print("  ✅ 注意：'d' 移到了 'b' 的位置，数组保持连续")

# 再次随机访问
print("\n【删除后随机访问】")
for i in range(5):
    result = rd.getRandom()
    print(f"  第 {i+1} 次随机: {result}")

# 删除中间元素
print("\n【删除元素 'a'】")
rd.remove('a')
print(f"  删除后: dict={rd.dict}, array={rd.key_array}, index_map={rd.key_to_index}")

# 再次随机访问
print("\n【最终随机访问】")
for i in range(5):
    result = rd.getRandom()
    print(f"  第 {i+1} 次随机: {result}")

print("\n" + "=" * 70)
print("5. 时间复杂度分析")
print("=" * 70)

print("""
【时间复杂度】

put(key, value):
  - 检查是否存在: O(1)
  - 添加到数组末尾: O(1)
  - 更新映射: O(1)
  - 总时间复杂度: O(1) ✅

remove(key):
  - 查找 index: O(1)
  - 将最后一个元素移到被删除位置: O(1)
  - 删除最后一个元素: O(1)
  - 更新映射: O(1)
  - 总时间复杂度: O(1) ✅

getRandom():
  - 随机取 index: O(1)
  - 访问数组: O(1)
  - 访问字典: O(1)
  - 总时间复杂度: O(1) ✅

【空间复杂度】
  - O(n): 存储 key_array 和 key_to_index
""")

print("\n" + "=" * 70)
print("6. 关键技巧：删除时的元素交换")
print("=" * 70)

print("""
【删除操作的关键】

当删除 key 时：
  1. 获取 key 的 index
  2. 获取数组的最后一个元素 last_key
  3. 将 last_key 移到被删除的位置
  4. 更新 last_key 的 index 映射
  5. 删除数组的最后一个元素
  6. 删除 key 的映射和值

这样做的优势：
  ✅ 数组保持连续（没有空洞）
  ✅ 删除操作 O(1)
  ✅ 随机访问时不会访问到已删除的元素
""")

print("\n" + "=" * 70)
print("7. 你的思路 vs 优化方案")
print("=" * 70)

print("""
【你的思路】
  ✅ 使用 key_array 维护 key 数组
  ✅ 随机取 index 访问
  ⚠️ 删除时需要额外处理

【优化方案】
  ✅ 使用 key_array 维护 key 数组
  ✅ 使用 key_to_index 维护 key -> index 映射
  ✅ 删除时：将最后一个元素移到被删除位置
  ✅ 所有操作都是 O(1)

【关键改进】
  - 添加 key_to_index 映射，实现 O(1) 删除
  - 删除时交换最后一个元素，保持数组连续
""")

print("\n" + "=" * 70)
print("8. 边界情况处理")
print("=" * 70)

print("""
【边界情况】

1. 空字典：
   - getRandom() 返回 None
   - 需要检查数组是否为空

2. 只有一个元素：
   - 删除后数组为空
   - 需要正常处理

3. 删除最后一个元素：
   - 数组变为空
   - 需要正常处理
""")

# 测试边界情况
print("\n【边界情况测试】")
rd2 = RandomDict()
rd2.put('x', 10)
print(f"  插入一个元素: {rd2.getRandom()}")

rd2.remove('x')
print(f"  删除后: size={rd2.size()}, getRandom()={rd2.getRandom()}")

print("\n" + "=" * 70)
print("9. 完整代码模板")
print("=" * 70)

print("""
import random

class RandomDict:
    def __init__(self):
        self.dict = {}  # key -> value
        self.key_array = []  # 存储 key 的数组
        self.key_to_index = {}  # key -> index 的映射
    
    def put(self, key, value):
        '''插入/更新，O(1)'''
        if key in self.dict:
            self.dict[key] = value
        else:
            self.dict[key] = value
            self.key_to_index[key] = len(self.key_array)
            self.key_array.append(key)
    
    def remove(self, key):
        '''删除，O(1)'''
        if key not in self.dict:
            return False
        
        index = self.key_to_index[key]
        last_key = self.key_array[-1]
        
        # 将最后一个元素移到被删除的位置
        self.key_array[index] = last_key
        self.key_to_index[last_key] = index
        
        # 删除最后一个元素
        self.key_array.pop()
        del self.key_to_index[key]
        del self.dict[key]
        
        return True
    
    def get(self, key):
        '''获取值，O(1)'''
        return self.dict.get(key)
    
    def getRandom(self):
        '''随机返回 key-value pair，O(1)'''
        if not self.key_array:
            return None
        
        random_index = random.randint(0, len(self.key_array) - 1)
        random_key = self.key_array[random_index]
        return (random_key, self.dict[random_key])
    
    def size(self):
        return len(self.key_array)
""")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)

print("""
✅ 你的思路基本正确！

【你的思路】
  - 使用 key_array 维护 key 数组
  - 随机取 index 访问
  - ✅ 思路正确

【需要改进的地方】
  - 添加 key_to_index 映射，实现 O(1) 删除
  - 删除时：将最后一个元素移到被删除位置
  - 保持数组连续，避免空洞

【最终方案】
  - 数据结构：dict + key_array + key_to_index
  - 所有操作：O(1) 时间复杂度
  - 随机访问：O(1) 时间复杂度 ✅
""")


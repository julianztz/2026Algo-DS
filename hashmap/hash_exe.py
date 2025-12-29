from collections import Counter, OrderedDict
from typing import List

'''
Python 3.7 开始，标准库提供的哈希表 dict 的键的遍历顺序就是键的插入顺序

它能让所有键按照插入顺序排列，是因为它把标准的哈希表和链表结合起来，组成了一种新的数据结构：哈希链表。
插入的val 作为链表node 链接

拉链法
开放寻址法
'''



# lc1 2Sum hashtable 实现
def twoSum(num: List[int], target: int) -> List[int]:
    map = dict()
    for i, n in enumerate(num):
        complement = target - n
        
        # map[n] = i  # 存储当前元素✅ 关键修复：先检查，再存储
        # 如果先存储再检查，当 n == complement 时会返回同一个索引两次
        if complement in map:  # 简化：不需要 .keys()
            return [map[complement], i]        
        map[n] = i 
    
    return []  # 如果没有找到，返回空列表

'''
Counter 是 collections 模块中的类，用于计数：   100%适配
是 dict 的子类
自动统计可迭代对象中元素的出现次数
不存在的键返回 0（不会报错）
'''
def isAnagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# 49 group  anagrams
'''
Given an array of strings strs, group the anagrams together.
'''
def groupAnagrams(strs: List[str]) -> List[List[str]]:
    map = {}
    for s in strs:
        key = ''.join(sorted(s))      # sorted 会把str变更成list
        if key in map:                # list mutable 不能作为key
            map[key].append(s)
        else:
            map[key] = [s]
    
    res = list(map.values())
    print(res)
    return res


# linkedHashmap -- python 已经实现 OrderedDict() 
'''
LRU （least recent used）算法
计算机用来清除LRU的算法

思路：
linkedHashmap -- OrderedDict()
每次get/put更新LRU -- move_to_end()
如果size不够，remove LRU

'''
class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        # 已有元素更新
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
        # 新元素替代LRU
        else:
            if len(self.cache) >= self.capacity:  # ✅ 使用 >= 更安全
                self.cache.popitem(last=False)  # ✅ 弹出第一个元素（最久未使用的），不能用 pop(0)
            self.cache[key] = value
            self.cache.move_to_end(key)
     
# review。。。 arrayHashmap -- 
# arr[] 记录 key-val
# map{} 记录 key 和 key的index



if __name__ == '__main__':
    nums = [2,7,11,15]
    tar = 9
    # twoSum(nums, tar)
    # groupAnagrams(["eat","tea","tan","ate","nat","bat"])
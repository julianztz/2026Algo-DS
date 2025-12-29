from typing import List


'''
前缀问题 -- 核心模板

1. ✅ **区间查询**：多次查询区间 [i, j] 的和
2. ✅ **子数组和**：寻找满足条件的子数组
3. ✅ **左右分割**：比较数组左边和右边的和
4. ✅ **数组不变**：数组元素不频繁变化
'''
class PrefixSum:
    # 前缀和数组
    def __init__(self, nums: List[int]):
        # 提前计算 preSum[] -- sum [0] ; prod [1]
        self.prefix = [0] * (len(nums) + 1)           
        # 计算 nums 的累加和
        for i in range(1, len(self.prefix)):
            self.prefix[i] = self.prefix[i - 1] + nums[i - 1]
    
    # 查询闭区间 [i, j] 的累加和;直接读取，减去重复位置
    def query(self, i: int, j: int) -> int:
        return self.prefix[j + 1] - self.prefix[i]
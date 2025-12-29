from typing import List

def twoSumHash(nums: List[int], target: int) -> List[int]:
    # dict[] -- complement: index
    map = dict()
    for i, num in enumerate(nums):
        complement = target - num
        if num in map.keys():
            first_num = map[num]
            return [first_num, i]
        else:
            map[complement] = i

def twoSumPointer(nums: List[int], target: int) -> List[int]:
    # sort -- nlogn
    # 首位pointer

    nums.insert(0)
    pass




if __name__ == '__main__':
    nums = [2,7,11,12]
    twoSumHash(nums, 9)

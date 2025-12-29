from typing import List


'''
思维模式

1、（回溯）是否可以通过遍历一遍二叉树得到答案？
    如果可以，用一个 traverse 函数配合外部变量来实现，这叫「遍历」的思维模式。
2、（DP）是否可以定义一个递归函数，通过子问题（子树）的答案推导出原问题的答案？ 
    如果可以，写出这个递归函数的定义，并充分利用这个函数的返回值，这叫「分解问题」的思维模式。

如果单独抽出一个二叉树节点，它需要做什么事情？
需要在什么时候（前/中/后序位置）做？
其他的节点不用你操心，递归函数会帮你在所有节点上执行相同的操作。


递归思路 -- 涉及递归的问题都可以用binary tree解决
'''



'''
mergeSort: 本质--b tree后序遍历

base case: split成单个元素list
子问题：左右半边分别sort
    递归公式：左不包[:mid]  右包[mid:] 

'''
# 区分左右两边
def mergeSort(nums):
    # base： 分到底
    if len(nums) <= 1:
        return nums

    mid = len(nums) // 2              # 更新中点给下一层

    # 递归公式：左右split + merge(排序)
    left = mergeSort(nums[:mid])            
    right = mergeSort(nums[mid:])     # 中间点归右边
    return merge(left, right)



# 后序位置：merging two (sorted) lists
def merge(left, right) -> List:
    l = 0
    r = 0
    res = []

    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            res.append(left[l])
            l += 1
        else:
            res.append(right[r])
            r += 1

    res.extend(right[r:])   # 原地修改列表; 
    # res += res[r:]        # 会创建新列表 more space needed
    res.extend(left[l:])

    print(res)
    return res
    

'''
quickSort： 本质--b tree 前序遍历

'''
def quickSort(nums):
    pass
def quick():
    pass


if __name__ == '__main__':
    ls = [4,5,1,3,2]
    # ls1 = [4,5]
    # ls2 = [1,2,3]
    # merge(ls1, ls2)

    mergeSort(ls)



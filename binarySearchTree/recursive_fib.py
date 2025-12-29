# -*- coding: utf-8 -*-
'''
递归两种思路

1. 遍历一遍树（回溯）-- backtrack, 关注节点间移动
2. 分解问题（DP分治）-- DP思路，关注整颗子树 left+1 / right+1
        递归函数一定有return；结果需要返还给上层计算
'''


# eg1 fib()   f(n) = f(n-1) + f(n-2)
# 分解问题思路 top-down （二叉树后序遍历相同）
# ⚠️ 时间复杂度：O(2^n) - 指数级！
# ⚠️ 空间复杂度：O(n) - 递归调用栈深度
# 
# 为什么慢？因为存在大量重复计算！
# 例如：计算 fib(5) 时：
#   - fib(5) 需要 fib(4) + fib(3)
#   - fib(4) 需要 fib(3) + fib(2)
#   - fib(3) 需要 fib(2) + fib(1)
#   可以看到 fib(3) 被计算了多次，fib(2) 被计算了更多次
# 
# 递归树展开：
#                    fib(5)
#                   /      \
#              fib(4)      fib(3)
#             /     \      /     \
#        fib(3)  fib(2) fib(2) fib(1)
#        /   \
#   fib(2) fib(1)
# 
# 每个节点都会分裂成两个子节点，总节点数约为 2^n
def fib_dp(n):
    if n == 1 or n == 2:
        return 1

    left1 = fib_dp(n-1)      
    left2 = fib_dp(n-2)
    return left1 + left2

# 优化版本：带记忆化的递归（Memoization）
# ✅ 时间复杂度：O(n) - 每个子问题只计算一次
# ✅ 空间复杂度：O(n) - 存储结果 + 递归栈
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 1 or n == 2:
        return 1
    
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]


# fib（）普通遍历算法 btm-up
# ✅ 时间复杂度：O(n) - 线性时间
# ✅ 空间复杂度：O(n) - 存储结果数组（可优化到O(1)）
# 
# 为什么快？每个值只计算一次，没有重复计算
# 从 fib(1), fib(2) 开始，逐步计算到 fib(n)
def fib_iter(n):
    res = [1,1]
    for i in range(2, n):
        res.append(res[i-1]+res[i-2])
    print(res)







if __name__ == '__main__':

    
    print("fib简单测试:")
    # print(f"fib_dp(10) = {fib_dp(10)}")
    # print(f"fib_memo(10) = {fib_memo(10)}")
    fib_iter(40)
    
    print("\n")

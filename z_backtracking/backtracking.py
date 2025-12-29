from typing import List, Optional

'''
================================================================================
回溯算法核心总结
================================================================================

【核心思想】
回溯 = DFS + 状态恢复。通过递归遍历决策树，在叶子节点收集解，通过"选择-递归-撤销"保证状态正确。

【关键注意事项】（200字）
1. 状态管理：使用标记数组（如used[]）跟踪已选元素，避免在循环中直接修改原列表（pop/insert会导致索引错乱）
2. 路径复制：保存结果时用path.copy()或path[:]，避免引用问题导致所有结果相同
3. 撤销对称：选择与撤销必须完全对称，顺序相反，确保状态完全恢复
4. 剪枝优化：在循环开始前检查条件，提前跳过无效分支（如used[i]检查）
5. 结束条件：明确何时到达叶子节点（如len(path)==len(nums)），及时保存并返回
6. 变量作用域：使用nonlocal访问外层变量，或通过参数传递状态
7. 去重处理：对于含重复元素的问题，需要排序+跳过相同元素（if i>0 and nums[i]==nums[i-1] and not used[i-1]）

【标准代码框架】
def solve(nums):
    res = []
    used = [False] * len(nums)  # 或使用set()跟踪已选
    
    def backtrack(path, ...):
        nonlocal res, used
        
        # 1. 结束条件
        if 满足条件:
            res.append(path.copy())  # 必须复制！
            return
        
        # 2. 遍历选择列表
        for i in range(len(nums)):  # 或 for choice in choices
            # 2.1 剪枝：跳过无效选择
            if used[i] or 其他剪枝条件:
                continue
            
            # 2.2 选择（前序）
            used[i] = True
            path.append(nums[i])
            
            # 2.3 递归
            backtrack(path, ...)
            
            # 2.4 撤销（后序，与选择顺序相反）
            path.pop()
            used[i] = False
    
    backtrack([], ...)
    return res

================================================================================
'''

'''
回溯 -- DFS  same

解决回溯问题 -- 遍历(思路)一颗决策树的过程
    --leaf node 存储答案
    --遍历完成；收集所有leaf node解；得到答案

--✅回溯模板✅--       
- ✅loop中做选择
- ✅关注edge（选择在树枝上）
- ✅节点反映选择后的状态
def backtrack(路径，选择列表):
    # 0. base case
    if  结束条件满足 : 
        // result.add(路径)
        return 

    # 1. 遍历树
    for 选择 in 选择列表:      // 核心 -- 选择-递归-撤销选择  -- 特别简单
        // 选择
        backtrack(路径，选择列表)
        // 撤销选择


--✅DFS模板✅--      
- ✅loop外做选择
- ✅关注节点
def dfs(路径，选择列表):
    # 0. base case
    if leaf node: 
        return 

    # 1. 遍历树
    // 选择
    for 选择 in 选择列表:      // 核心 -- 选择-递归-撤销选择  -- 特别简单
        dfs(路径，选择列表)
    // 撤销选择
'''



# lc46 Permutation 全排列问题
'''
Given an array nums of distinct integers, return all the possible permutations. 
You can return the answer in any order.
'''
def permute(nums: List[int]) -> List[List[int]]:
    res = []
    used = [False] * len(nums)

    # 回溯函数（路径，选择列表）
    def backtrack(path: List[int], nums:List[int]):
        nonlocal res, used

        # 0.base case
        if len(path) == len(nums):    # 选择列表为空
            res.append(path.copy())   # 注意list mutable，需要复制
            return

        # 1.递归公式 -- 多叉树遍历
        #    针对edge： loop内部剪枝，选择，撤销
        for i,n in enumerate(nums):
            # 0. 剪枝--当前层跳过选择过的
            if used[i]:
                continue

            # 1.前序 -- 选择
            used[i] = True
            path.append(n)
            
            # 2.递归函数
            backtrack(path, nums)

            # 3.后序 -- 撤销选择
            path.pop()
            used[i] = False

    backtrack([],nums)
    print(res)
    return res


# lc200 Number of Islands
'''
Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), 
return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. 
You may assume all four edges of the grid are all surrounded by water.

思考：相邻的1算一个岛 -- 一旦找到1把相邻的(递归式)翻成0
思路：
遍历整个grid，遇到岛用dfs反转相邻1
'''
def numIslands(grid: List[List[str]]) -> int:
    m = len(grid)           # height
    n = len(grid[0])        # length
    res = 0

    # grid_check = [[False] * n] * m   # 不需要， 因为0位置直接return了


    # 递归式翻牌子 相邻所有 1->0 
    def dfs(i, j):
        nonlocal grid, m, n
        if i<0 or j<0 or i>=m or j>=n:    # 出界
            return
        if grid[i][j] == 0:               # 到0位置直接返回
            return
   
        # 反转 0->1
        grid[i][j] = 0          

        # 上下左右neighbour翻牌子
        dfs(i-1, j)    
        dfs(i+1, j)
        dfs(i, j-1)
        dfs(i, j+1)

    # 遍历grid
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:        # 找到岛
                res += 1
                dfs(i, j)     

    print(res)
    return res


# lc1254 Number of Closed islands
'''
Given a 2D grid consists of 
0s (land) and 1s (water).  
An island is a maximal 4-directionally connected group of 0s and a closed island is an island totally 
(all left, top, right, bottom) surrounded by 1s.

思路：类似lc200
遍历整个grid
遇到岛0，如果不在边界则 -- dfs反转相邻1

'''
def closedIsland(grid: List[List[int]]) -> int:
    res = 0
    m = len(grid)
    n = len(grid[0])

    # 检查坐标是否在边界
    def border_check(i, j):
        nonlocal m, n
        if i==0 or j==0 or i==m-1 or j==n-1:
            return True        # 边界岛
        return False
    # 递归检查 

    # 1. 都是0 且不在边界
    # 2. 是1 return
    def isClosed(i,j):
        nonlocal m, n
        # 1. 边界检查
        if i<0 or j<0 or i>=m or j>=n:          
            return True
        
        # 2. 如果是水(1)或正在检查中(2)，返回True（作为边界）
        if grid[i][j] == 1 or grid[i][j] == 2:
            return True
        
        # 3. 如果当前是0且在边界，不是封闭岛
        if grid[i][j] == 0 and border_check(i,j):
            return False
        
        # 4. 当前是0且不在边界，标记为2（正在检查中，避免重复访问）
        grid[i][j] = 2
        
        # 5. 递归检查四个方向
        closed = isClosed(i-1,j) and isClosed(i+1,j) and isClosed(i,j-1) and isClosed(i,j+1)
        
        # 6. 根据结果决定最终标记
        if closed:
            grid[i][j] = 1  # 封闭岛，标记为水
        else:
            grid[i][j] = 0  # 非封闭岛，恢复为陆地
        
        return closed

    # 遍历整个grid
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:           # island 且不在边界
                if isClosed(i,j):                                  # 检查并反转相邻非边界岛
                    res += 1

    print(res)
    return res
    


if __name__ == '__main__':
    # permute([1,2,3])

    grid = [[1,0],[0,1]]
    grid2 = [
        [1,1,1,1,0],
        [1,1,0,1,0],
        [1,1,0,0,0],
        [1,1,1,0,0],
    ]
    grid3 = [[0,0,1,0,0],
             [0,1,0,1,0],
             [0,1,1,1,0]]
    grid4 = [[0,0,1,1,0,1,0,0,1,0],
             [1,1,0,1,1,0,1,1,1,0],
             [1,0,1,1,1,0,0,1,1,0],
             [0,1,1,0,0,0,0,1,0,1],
             [0,0,0,0,0,0,1,1,1,0],
             [0,1,0,1,0,1,0,1,1,1],
             [1,0,1,0,1,1,0,0,0,1],
             [1,1,1,1,1,1,0,0,0,0],
             [1,1,1,0,0,1,0,1,0,1],
             [1,1,1,0,1,1,0,1,1,0]]
    # numIslands(grid2)
    closedIsland(grid4)


'''
BFS 算法的本质就是遍历一幅图
BFS 算法经常用来求解最短路径问题

'''
from collections import deque
from itertools import _Step, combinations
from typing import List

'''
 tempate
# 从 s 开始 BFS 遍历图的所有节点，且记录遍历的步数
def bfs(graph, s, target):
    visited = [False] * len(graph)
    q = deque([s])
    visited[s] = True
    # 记录从 s 开始走到当前节点的步数
    step = 0
    
    while q:
        sz = len(q)
        for i in range(sz):
            cur = q.popleft()
            print(f"visit {cur} at step {step}")
            # 判断是否到达终点
            if cur == target:
                return step

            # 将邻居节点加入队列，向四周扩散搜索
            for to in neighborsOf(cur):
                if not visited[to]:
                    q.append(to)
                    visited[to] = True
        step += 1
    # 如果走到这里，说明在图中没有找到目标节点
    return -1
'''


# lc773 Sliding Puzzle 华容道问题
'''
On an 2 x 3 board, there are five tiles labeled from 1 to 5, 
and an empty square represented by 0. A move consists of choosing 0 and a 4-directionally adjacent number and swapping it.

The state of the board is solved if and only if the board is [[1,2,3],[4,5,0]].

Given the puzzle board board, return the least number of moves required so that the state of the board is solved. 
If it is impossible for the state of the board to be solved, return -1.

思路： 如何画tree/graph？看作整体
      123
      405
    /  |  \
 103  123  123
 425  045  450

'''
def slidingPuzzle(board: List[List[int]]) -> int:
    target_state = '123450'
    start_state = ''
    for i in range(len(board)):
        for j in range(len(board[0])):
            start_state += str(board[i][j])

    # -- BFS 标准框架 --
    q = deque()
    visited = set()

    q.append(start_state)
    visited.add(start_state)          # 记录访问过的组合

    total_step = 0
    while q:
        sz = len(q)
        for _ in range(sz):
            cur = q.popleft()
            if cur == target_state:
                return total_step
            
            '''
            找所有3种子节点组合
            1. 交换0和相邻位置
            2. 返还linear str form
            '''
            combinations = zero_neighbour_swap(cur)
            for 

    def zero_neighbour_swap(board):
        ind = board.index('0')
        

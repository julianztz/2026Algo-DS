'''
bfs: 找最短路径
dps
'''

from logging import root
from turtle import right
from typing import List, Optional
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right




class Solution:
    '''
    111.Minimum Depth of Binary Tree
    Given a binary tree, find its minimum depth.
    The minimum depth is the number of nodes along the shortest path 
    from the root node down to the nearest leaf node.
    '''

    '''
    DFS 思路： 
    遍历时记录当前tree的最小深度以及当前节点深度
    前序位置进入节点时增加深度；后序位置离开节点减小深度
    如果leaf node 更新最小深度
    '''
    def minDepthDFS(self, root: Optional[TreeNode]) -> int:
        # 1. visit all nodes
        # 2. leaf return 1 save in node
        # 3. parent get min(left, right)
        if not root:
            return 0

        self.minDepth = float('inf')
        self.curNodeDepth = 0
        self.traverse(root)
        print(self.minDepth)
        return self.minDepth


    def traverse(self, root):
        # 到达tree btm -- Null
        if not root:
            return
        
        # enter node 增加depth
        self.curNodeDepth += 1

        # leaf node：更新最小深度
        if not root.left and not root.right:   # leaf node
            self.minDepth = min(self.minDepth, self.curNodeDepth)

        # 递归到底
        self.traverse(root.left)
        self.traverse(root.right)

        self.curNodeDepth -= 1

    '''
    BFS 思路：  在不遍历整个树的情况下 找到最小深度 return
    层序遍历 -- 当reach第一个leaf node就得到minDepth ！！
    '''
    def minDepthBFS(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        q = deque()
        q.append(root)

        lv = 1

        while len(q) > 0:
            size = len(q)            # 每层开始时 q中的节点数量一定

            for _ in range(size):    # 对每一层 q中所有节点进行遍历，pop光所有node再 push下一层直到底层
                cur = q.popleft()
                if not cur.left and not cur.right:   # 如果leaf node，直接返还深度
                    print(cur.val, " at level", lv)
                    return lv

                if cur.left:
                    q.append(cur.left)
                if cur.right:
                    q.append(cur.right)
            lv += 1


    '''
    104. max Depth of Binary Tree
    Given a binary tree, find its max depth.
    The max depth is the number of nodes along the longest path 
    from the root node down to the farthest leaf node.
    '''
    # ！！！ BFS: 记录层数 return largest
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        q = deque()
        q.append(root)      # 从root开始为第一层
        depth = 0           # root node 深度：1

        while len(q) > 0:   # need to finish the while 因为找最长
            depth += 1      # 进入node之前更新 深度，避免最后结果 +1 extra
            for _ in range(len(q)):
                cur = q.popleft()

                if not cur.left and not cur.right:    # 可以省略
                    # do nothing
                    continue
                
                if cur.left:
                    q.append(cur.left)
                if cur.right:
                    q.append(cur.right)
            
        print(depth)
        return depth

    # better ！！！ DFS 思路 recursive ： root的最大深度 == 左右子树的最大深度+1
    def maxDepthDFS(self, root: Optional[TreeNode]) -> int:
        # 子问题：求子树最大深度
        # base case： root is Null -- return 1
        # 公式： maxDepthDFS(left) + 1
        if not root:
            return 0
        left = self.maxDepthDFS(root.left)
        right = self.maxDepthDFS(root.right)

        return 1+max(left, right)


    '''
    102. binary tree level order traversal
    Given the root of a binary tree, return the level order traversal of its nodes' values. 
    '''
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        res = [[root.val]]
        q = deque()
        q.append(root)

        while len(q) > 0:

            cur_lv_nodes = []
            for _ in range(len(q)):    # 遍历每一层
                cur = q.popleft()

                if cur.left:
                    q.append(cur.left)
                    cur_lv_nodes.append(cur.left.val)
                if cur.right:
                    q.append(cur.right)
                    cur_lv_nodes.append(cur.right.val)

            if cur_lv_nodes:                   # when the q is empty, stop
                res.append(cur_lv_nodes)

        print(res)
        return res

    '''
    SOLVED!! good Q
    543. diameter of binary tree
    Given the root of a binary tree, return the length of the diameter of the tree.
    The diameter of a binary tree is the length of the longest path between any two nodes in a tree. 
    This path may or may not pass through the root.
    The length of a path between two nodes is represented by the number of edges between them.

    思路： DFS后序
    每个子节点的直径 == 左/右子树最大深度和！！
    '''
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        
        max_diameter = 0

        # 每个节点的最大depth
        def traverse(node):
            # base case: leaf node
            if not node:
                return 0

            # 子问题：左右子树最大深度和
            # 递归公式：计算左右子树
            left = traverse(node.left)      
            right = traverse(node.right)

            nonlocal max_diameter                                   # immutable (int) 需要nonlocal共享外部变量
            max_diameter = max(max_diameter, left+right)            # 左/右子树最大深度和 更新至max
            return 1+max(left, right)                               # leaf node 深度为0 故+1 得到每个node高度

        traverse(root)
        return max_diameter

   


        


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(6)
    #     1
    #    / \
    #   2   3
    #  /   / \
    # 4   5   6

    root2 = TreeNode(3)
    root2.left = TreeNode(9)
    root2.right = TreeNode(20)
    root2.right.left = TreeNode(15)
    root2.right.right = TreeNode(7)
    #     3
    #    / \
    #   9   20
    #      / \
    #    15  7

    s = Solution()
    # s.minDepthDFS(root)
    # s.minDepthDFS(root2)

    # s.minDepthBFS(root)
    # s.minDepthBFS(root2)

    s.maxDepth(root)
    s.maxDepth(root2)
    s.levelOrder(root)


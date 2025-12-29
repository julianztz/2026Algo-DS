from ast import List
from optparse import Option
from platform import node
from typing import Optional
from collections import deque


'''
binary search tree 遍历

递归遍历(DFS) -- preorder / inorder / postorder   # 先中后读root node
层序遍历(BFS)
'''


class TreeNode:
    def __init__(self, value) -> None:
        self.left = None
        self.val = value
        self.right = None


# Todo 层序遍历 每个node自己记录depth
class State:
    def __init__(self, node:TreeNode, depth:int) -> None:
        self.node = node
        self.depth = depth
    


'''
DFS
递归思路

子问题： 访问子分支
终止条件：到达底层null
递归公式：preorder(left) preorder(right)


前中后顺序区别 -- 掌握的信息量不同
pre: 当前节点信息
in: 左子节点 + 当前节点
post: 左右子节点 + 当前节点
'''
#中左右 preorder
def preorder(root: Optional[TreeNode]) -> None:
    # 1. base case (return) -- 到达null 则return回到上一层parent node
    if not root:
        return
    # 2. formula -- 递归公式 preorder(左&右child)
    print(root.val)
    preorder(root.left)
    preorder(root.right)


# 左中右 inorder
def inorder(root: Optional[TreeNode]) -> None:
    # 1. base case (return) -- 到达null 则return回到上一层parent node
    if not root:
        return
    # 2. formula -- 递归公式 inorder(左&右child)
    inorder(root.left)
    print(root.val)
    inorder(root.right)

# 左右中 postorder
# 需要储存结果到list （不可在递归函数内建list??）
# 1. closure   # inner 函数用outter函数的var
# 2. DP 思路： parent node的结果 == left 结果 + right 结果

'''
常用遍历法 （用到closure概念，但是未return traverse function）
'''
def postorder(root: Optional[TreeNode]) -> List:
    '''
    pythonic -- （闭包+作用域）
    '''
    result = []
    def traverse(node):
        # 1. base case (return) -- 到达null 则return回到上一层parent node
        if not node:
            return
        # 2. formula -- 递归公式 postorder(左&右child)
        traverse(node.left)
        traverse(node.right)
        result.append(node.val)

    traverse(root)
    return result

'''
不推荐 但是值得思考！！
DP 思路 -- real recursive   # 每层都需要create [], 与上一层extend
'''
def postOrder_recursive(root: Optional[TreeNode]) -> List:
    res = []
    if not root:
        return []

    res.extend(postOrder_recursive(root.left))
    res.extend(postOrder_recursive(root.right))
    res.append(root.val)
    return res

'''
python 高科技
generator + yield keyword
惰性遍历
'''
def postorder_recursive_yield(root):
    def gen(node):
        if not node:
            return
        yield from gen(node.left)
        yield from gen(node.right)
        yield node.val
    return list(gen(root))
#### 满足条件 遍历停止
# for val in postorder_recursive_yield(root):
#     if val > 100:
#         breaK



'''
BFS
层序遍历

思路：利用queue (FIFO) 一个个节点从上到下，从左到右enqueue再dequeue处理
'''
# 不记录层数
def levelOrder(root: Optional[TreeNode]) -> None:
    q = deque()
    q.append(root)

    while len(q) > 0:
        cur = q.popleft()
        print(cur.val)

        if cur.left:
            q.append(cur.left)
        if cur.right:
            q.append(cur.right)

# ！！！bst常用算法！！！ 记录层数 （非深度）    # depth是从btm up 计算
def levelOrder2(root: Optional[TreeNode]) -> None:
    q = deque()
    q.append(root)

    lv = 1

    while len(q) > 0:

        size = len(q)            # 每层开始时 q中的节点数量一定

        for _ in range(size):    # 对每一层 q中所有节点进行遍历，pop光所有node再 push下一层直到底层
            cur = q.popleft()
            print(cur.val, " at level", lv)

            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        lv += 1



'''
1118思考： 通过递归方法得到层序遍历结果
'''



'''
记录二叉树节点数
！！动态规划 -- 关注整颗子树！
'''
def countNode(root) -> int:
    if not root:
        return 0

    left = countNode(root.left)
    right = countNode(root.right)

    return left + right + 1                 # 后序： 记录左右 + 自己(+1)


'''
用遍历思路写traverse function 打印遍历过程
!! 回溯 -- 关注节点间的移动过程
'''
def traverse(root) -> None:
    if not root:
        return

    print("root进入left")
    traverse(root.left)
    print("左子node完成,left返回root")

    print("root进入right")
    traverse(root.right)
    print("右子node完成:right返回root")





if __name__ == "__main__":
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

    #### DFS
    # preorder(root)
    # inorder(root)
    print(postorder(root))
    ls = postOrder_recursive(root)
    print(ls)

    #### BFS
    # levelOrder(root)
    # levelOrder2(root)
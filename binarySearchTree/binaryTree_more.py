from typing import List, Optional
from collections import deque


'''
--BT 遍历--

递归遍历(DFS) -- preorder / inorder / postorder   # 先中后读root node
层序遍历(BFS) -- deque 按顺序

--BT 思路--
1. 遍历：是否可以通过遍历一遍二叉树得到答案？如果可以，
用一个 traverse 函数配合外部变量来实现，这叫「遍历」的思维模式。

2. 分治：是否可以定义一个递归函数，通过子问题（子树）的答案推导出原问题的答案？
如果可以，写出这个递归函数的定义，并充分利用这个函数的返回值，这叫「分解问题」的思维模式。
'''




class TreeNode:
    def __init__(self, value) -> None:
        self.left = None
        self.val = value
        self.right = None



# lc226 invert binary tree
'''
for all nodes, swap left right
return list of inverted nodes

思路：
1. 遍历：在前中后序（都ok）位置进行左右swap，从上到下
    中序需要注意只能交换一次位置？？
2. 分治：递归，关注整颗子树
'''

# 遍历思路： top-down
def invertTree1(root: Optional[TreeNode]) -> Optional[TreeNode]:
    res = []

    def traverse(node):
        # leaf node -- return
        if not node:
            return
        # 交换左右子树       
        res.append(node.val)
        node.left, node.right = node.right, node.left
        traverse(node.left)
        traverse(node.right)

    traverse(root)
    print(res)
    return root


# !!! review 分治思路： btm-up
def invertTree2(root: Optional[TreeNode]) -> Optional[TreeNode]:
    # base case
    if not root:
        return
    
    # 子问题：invert(left) & invert(right)
    # 递归公式：
    left_tree = invertTree2(root.left)
    right_tree = invertTree2(root.right)

    root.left, root.right = right_tree, left_tree
    return root
    
# $$$ lc116 
'''
You are given a perfect binary tree where all leaves are on the same level, 
and every parent has two children. The binary tree has the following definition:
struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
Populate each next pointer to point to its next right node.
If there is no next right node, the next pointer should be set to NULL.
Initially, all next pointers are set to NULL.

思路： 
1. DFS
遍历：将每层节点两两绑定遍历！！
        1
       /  \
      2    3
     / \   / \
    4   5  6  7
23下层 遍历3次：45 & 56 & 67 使得所有node链接
一棵二叉树被抽象成了一棵三叉树，三叉树上的每个节点就是原先二叉树的两个相邻节点

分治：无解，无法分成子问题


'''
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

def connect(root: 'Optional[Node]') -> 'Optional[Node]':
    if not root:
        return

    def traverse(left_node, right_node) -> Node:
        if not left_node and not right_node:
            return

        # 将每层node两两绑定进行 next 链接
        traverse(left_node.left, left_node.right)
        traverse(left_node.right, right_node.left)
        traverse(right_node.left, right_node.right)
        left_node.next = right_node

    traverse(root.left, root.right)
    return root

# 2.BFS -- deque
def connect2(root: 'Optional[Node]') -> 'Optional[Node]':
    q = deque()
    q.append(root)

    while len(q) > 0:
        size = len(q)

        # 1. 追踪前一个node
        prev = None    
        for _ in range(size):
            cur = q.popleft()

            # 链接到当前node
            if prev:
                prev.next = cur
            prev = cur

            if cur.left and cur.right:
                q.append(cur.left)
                q.append(cur.right)

    return root


# lc114 flatten binary tree to linked list
'''
Given the root of a binary tree, flatten the tree into a "linked list":

The "linked list" should use the same TreeNode class where the right child pointer 
points to the next node in the list and the left child pointer is always null.
The "linked list" should be in the same order as a pre-order traversal of the binary tree.

        !!Do not return anything, modify root in-place instead.

思路：
遍历：只遍历一次且原地改动 no extra space； 无解？？？
分治：
子问题-flatten(左子树) & flatten(右子树)
'''
# 分治思路
def flatten(root: Optional[TreeNode]) -> None:
    if not root:
        return 

    flatten(root.left)
    flatten(root.right)

    temp_right = root.right
    root.right = root.left         # 左子树 移到右边
    root.left = None

    # 将整个左子树接到右边
    left_end = root.right
    if left_end:
        while left_end and left_end.right:   # 得到左子树末端
            left_end = left_end.right

        if temp_right:
            left_end.right = temp_right

    else:
        root.right = temp_right


# lc107 Binary Tree level order traveral II
'''
Given the root of a binary tree, return the bottom-up level order traversal of its nodes' values. 
(i.e., from left to right, level by level from leaf to root).

BFS 思路：
对于每个node enque left & right
每层deque 直到q empty
用FIFO 储存结果，return 反向levelOrder nodes （bottom-up）

'''
def levelOrderBottom(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    res_q = deque()
    q = deque([root])

    while q:
        sz = len(q)
        cur_lev_res = []
        for _ in range(sz):
            cur = q.popleft()
            
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)

            cur_lev_res.append(cur.val)
        
        res_q.appendleft(cur_lev_res)

    return list(res_q)


# lc103 Binary Tree Zigzag Level Order Traversal
'''
Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. 
(i.e., from left to right, then right to left for the next level and alternate between).

Input: root = [3,9,20,null,null,15,7]
Output: [[3],[20,9],[15,7]]
思路：常规BFS + switch控制每层颠倒顺序
'''
def zigzagLevelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    res = []
    q = deque([root])

    switch = False
    while q:

        cur_level_res = []
        for _ in range(len(q)):
            cur = q.popleft()

            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)

            cur_level_res.append(cur.val)
        if switch:
            cur_level_res.reverse()

        switch = not switch
        res.append(cur_level_res)

    return res
        
# $$$ lc 662. Maximum Width of Binary Tree
'''
Given the root of a binary tree, return the maximum width of the given tree.

The maximum width of a tree is the maximum width among all levels.

The width of one level is defined as the length between the end-nodes (the leftmost and rightmost non-null nodes),
where the null nodes between the end-nodes that would be present in a complete binary tree 
extending down to that level are also counted into the length calculation.

思路：
BFS
每个node编号： 左子=parent*2  右子=parent*2+1  当前level 的node数量=右子-左子+1
'''
class Node_num():
    def __init__(self, node, num) -> None:
        self.node = node
        self.num = num

def widthOfBinaryTree(root: Optional[TreeNode]) -> int:

    if not root:
        return 0
    q = deque[Node_num]([Node_num(root, 1)])

    max_width = 1   # root一个node
    while q:
        first = 0
        last = 0
        q_size = len(q)
        for _ in range(q_size):
            cur = q.popleft()
            cur_node = cur.node
            cur_num = cur.num

            # 左子node： num * 2
            if cur_node.left:
                q.append(Node_num(cur_node.left,cur_num*2))
            # 右子node： num * 2 + 1
            if cur_node.right:
                q.append(Node_num(cur_node.right,cur_num*2+1))

            # 记录第一个和最后一个的num用来计算max
            if _ == 0:
                first = cur_num
            # if _ == len(q) - 1:      # ❌ 错误！len(q) 变化
            if _ == q_size - 1:
                last = cur_num

        max_width = max(max_width, last-first+1)

    return max_width


if __name__ == '__main__':
    # root = TreeNode(1)
    # root.left = TreeNode(2)
    # root.left.left = TreeNode(4)
    # root.left.right = TreeNode(5)
    # root.right = TreeNode(3)
    # invertTree1(root)


    zig_root = TreeNode(1)
    zig_root.left = TreeNode(2)
    zig_root.right = TreeNode(3)
    zig_root.left.left = TreeNode(4)
    zig_root.right.right = TreeNode(5)
    zigzagLevelOrder(zig_root)
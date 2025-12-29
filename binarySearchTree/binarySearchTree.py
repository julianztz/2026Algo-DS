'''
BST 的inorder 返还结果为升序排列

'''
from typing import Optional, List
from collections import deque

class TreeNode:
    def __init__(self, value) -> None:
        self.left = None
        self.val = value
        self.right = None



# 230  Kth Smallest Element in a BST
'''
Given the root of a binary search tree, and an integer k, return the 
kth smallest value (1-indexed) of all the values of the nodes in the tree.
思路：inorder返还bst升序排列
'''
def kthSmallest(root: Optional[TreeNode], k: int) -> int:
    if not root:
        return -1
    
    res = -1
    # inorder -- bst升序排列
    rank = 0
    def traverse(node, k):
        nonlocal rank, res
        if not node:
            return 
        traverse(node.left, k)
        rank += 1
        if rank == k:
            res = node.val
            return
        traverse(node.right, k)
    
    traverse(root, k)
    return res


# $$$$$$ lc 98. Validate Binary Search Tree
'''
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

The left subtree of a node contains only nodes with keys strictly less than the node's key.
The right subtree of a node contains only nodes with keys strictly greater than the node's key.
Both the left and right subtrees must also be binary search trees.

思路：
分治：validate子树是bst && 且
        # 1. node 左小右大 且 左子树小于root & 右子树大于root
        # 左子树：不停变小，但是不能小于min_val
        # 右子树：不停变大，但是不能超过max_val
遍历：
'''

# way1 ❌ 错误 没有考虑最高父节点
def isValidBST0(root: Optional[TreeNode]) -> bool:
    # 0.base case
    if not root:
        return True

    '''
    繁琐
    valid = True
    valid &= isValidBST(root.left)
    if root.left and root.val <= root.left.val:
        return False
    valid &= isValidBST(root.right)

    if root.right and root.val >= root.right.val:
        return False
    return True
    '''

    # 1. 只处理左右子节点
    if root.left and root.val <= root.left.val:
        return False
    if root.right and root.val >= root.right.val:
        return False

    # 2. return递归
    return isValidBST0(root.left) and isValidBST0(root.right)

# way2 
def isValidBST(root: Optional[TreeNode]) -> bool:


    def validBST(node, max_val, min_val) -> bool:
        # 0. base case
        if not node:
            return True

        # 1. node 左小右大 且 左子树小于root & 右子树大于root
        # 左子树：不停变小，但是不能小于min_val
        # 右子树：不停变大，但是不能超过max_val
        # 注意：必须用 is not None，不能用 if max_val，因为 max_val=0 时会被当作 False
        if max_val is not None and node.val >= max_val:
            return False
        if min_val is not None and node.val <= min_val:
            return False

        # 左子树：最大值限制为 node.val（所有左子树节点必须 < node.val）
        # 右子树：最小值限制为 node.val（所有右子树节点必须 > node.val）
        return validBST(node.left,  node.val, min_val) \
           and validBST(node.right, max_val, node.val)

    return validBST(root, None, None)


# lc700 Search in a Binary Search Tree
# way1 迭代
def searchBSTIteration(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    if not root:
        return 

    tar = root
    while tar:
        if tar.val < val:
            tar = tar.right
        elif tar.val > val:
            tar = tar.left
        elif tar.val == val:
            return tar

    return None

# way2 递归 分治思路（利用BST性质早期返回）- 推荐
def searchBST(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    if not root:
        return None

    # 利用BST性质：只搜索一个子树，找到后立即返回（不会继续遍历）
    if root.val > val:
        return searchBST(root.left, val)  # 只搜索左子树
    elif root.val < val:
        return searchBST(root.right, val)  # 只搜索右子树
    else:  # root.val == val
        return root  # 找到后立即返回，递归栈逐层返回，不会继续遍历

# ❌ 错误方式：不用BST性质，左右都递归
# def searchBST_wrong(root, val):
#     if not root:
#         return None
#     if root.val == val:
#         return root
#     # 问题：即使target在右子树，也会先遍历左子树（浪费）
#     left = searchBST_wrong(root.left, val)
#     if left:
#         return left
#     return searchBST_wrong(root.right, val)
# 时间复杂度：O(n) vs O(log n)，且访问节点数更多


# $$$ lc701 Insert into a Binary Search Tree
'''
思路： 找到位置，插入节点
'''
def insertIntoBST(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    if not root:
        return TreeNode(val)

    if root.val > val:
        left_node = insertIntoBST(root.left, val)
        root.left = left_node

    elif root.val < val:
        right_node = insertIntoBST(root.right, val)
        root.right = right_node

    return root

# way2 迭代（指针追踪）
def insertIntoBSTIterationImproved(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    if not root:
        return TreeNode(val)
    
    parent = None
    current = root
    is_left = False  # 标记应该插入到左还是右
    
    # 找到插入位置（parent是插入点的父节点）
    while current:
        parent = current
        if current.val > val:
            current = current.left
            is_left = True
        else:  # current.val < val        不考虑相同node
            current = current.right
            is_left = False
    
    # 在parent的相应位置插入新节点
    if is_left:
        parent.left = TreeNode(val)
    else:
        parent.right = TreeNode(val)
    return root
    

# lc450 Delete Node in a BST
# way1 指针迭代实现 -- 复杂
def deleteNode(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None
    
    cur = root
    parent = None
    is_left = False  # 初始值不重要，会在循环中更新
    
    # 1. 找到要删除的节点
    while cur and cur.val != key:
        parent = cur
        if key < cur.val:
            cur = cur.left
            is_left = True
        else:
            cur = cur.right
            is_left = False
    
    # 2. 如果没找到，直接返回
    if not cur:
        return root
    
    # 3. 删除节点（三种情况）
    if cur.left and cur.right:
        # 情况1：有两个子节点 - 用右子树的最小节点（inorder successor）替代
        successor = cur.right
        successor_parent = cur
        
        # 找到右子树的最小节点（最左边的节点）
        while successor.left:
            successor_parent = successor
            successor = successor.left
        
        # 用successor的值替代cur的值
        cur.val = successor.val
        
        # 删除successor（它最多只有一个右子节点）
        if successor_parent == cur:
            successor_parent.right = successor.right
        else:
            successor_parent.left = successor.right
            
    elif cur.left:
        # 情况2：只有左子节点
        if not parent:  # 删除的是根节点
            root = cur.left
        elif is_left:
            parent.left = cur.left
        else:
            parent.right = cur.left
    elif cur.right:
        # 情况3：只有右子节点
        if not parent:  # 删除的是根节点
            root = cur.right
        elif is_left:
            parent.left = cur.right
        else:
            parent.right = cur.right
    else:
        # 情况4：叶子节点
        if not parent:  # 删除的是根节点（且树只有一个节点）
            root = None
        elif is_left:
            parent.left = None
        else:
            parent.right = None
    
    return root


# way2 递归分治思路（推荐，更简洁）
def deleteNodeRecursive(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    递归版本：利用返回值重组树结构
    
    递归公式：
    deleteNode(root, key) = {
        None,                           if root = None
        deleteNode(root.left, key),     if root.val > key (在左子树)
        deleteNode(root.right, key),    if root.val < key (在右子树)
        handle_delete(root),            if root.val = key (找到了)
    }
    """
    if not root:
        return None
    
    # 利用BST性质找到要删除的节点
    if root.val > key:
        # 要删除的节点在左子树，删除后更新左子树
        root.left = deleteNodeRecursive(root.left, key)
        return root
    elif root.val < key:
        # 要删除的节点在右子树，删除后更新右子树
        root.right = deleteNodeRecursive(root.right, key)
        return root
    else:
        # 找到了要删除的节点，处理三种情况
        # 情况1：叶子节点或无子节点
        if not root.left:
            return root.right  # 返回右子树（可能是None）
        if not root.right:
            return root.left   # 返回左子树
        
        # 情况2：有两个子节点 - 用右子树的最小值（inorder successor）替代
        # 找到右子树的最小节点
        successor = root.right
        while successor.left:
            successor = successor.left
        
        # 用successor的值替代当前节点
        root.val = successor.val
        # 删除successor（它最多只有一个右子节点）
        root.right = deleteNodeRecursive(root.right, successor.val)
        return root

# 对比总结：
# - 递归版本：代码更简洁，逻辑更清晰，推荐使用
# - 迭代版本：需要手动追踪parent指针，代码更复杂，但在深度很大的树中可以避免栈溢出
        

        
if __name__ == '__main__':
    root = TreeNode(0)
    root.right = TreeNode(-1)

    print(isValidBST(root))
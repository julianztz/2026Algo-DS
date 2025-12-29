from collections import deque
from binaryTree_more import TreeNode, Node_num, widthOfBinaryTree

# 测试用例1：简单树
#     1
#    / \
#   2   3
root1 = TreeNode(1)
root1.left = TreeNode(2)
root1.right = TreeNode(3)

# 测试用例2：更复杂的树
#         1
#        / \
#       2   3
#      /     \
#     4       5
root2 = TreeNode(1)
root2.left = TreeNode(2)
root2.right = TreeNode(3)
root2.left.left = TreeNode(4)
root2.right.right = TreeNode(5)

# 测试用例3：只有左子树
#     1
#    /
#   2
root3 = TreeNode(1)
root3.left = TreeNode(2)

print("=" * 60)
print("测试 widthOfBinaryTree")
print("=" * 60)

print("\n测试用例1: [1,2,3]")
print("预期: 2 (第2层有2个节点)")
try:
    result1 = widthOfBinaryTree(root1)
    print(f"结果: {result1}")
except Exception as e:
    print(f"错误: {e}")

print("\n测试用例2: [1,2,3,null,4,null,5]")
print("预期: 2 (第3层有2个节点，但中间有null)")
try:
    result2 = widthOfBinaryTree(root2)
    print(f"结果: {result2}")
except Exception as e:
    print(f"错误: {e}")

print("\n测试用例3: [1,2]")
print("预期: 1 (只有1个节点)")
try:
    result3 = widthOfBinaryTree(root3)
    print(f"结果: {result3}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("手动追踪代码执行过程（测试用例1）")
print("=" * 60)

def trace_widthOfBinaryTree(root):
    if not root:
        return 0
    
    q = deque([Node_num(root, 1)])
    max_width = 1
    level = 0
    
    while q:
        level += 1
        first = 0
        last = 0
        size = len(q)
        print(f"\n【第 {level} 层】")
        print(f"  队列初始长度: {size}")
        print(f"  队列内容: {[(n.node.val, n.num) for n in q]}")
        
        for i in range(size):
            cur = q.popleft()
            cur_node = cur.node
            cur_num = cur.num
            
            print(f"\n  迭代 {i}:")
            print(f"    处理节点: val={cur_node.val}, num={cur_num}")
            print(f"    popleft 后队列长度: {len(q)}")
            
            if cur_node.left:
                q.append(Node_num(cur_node.left, cur_num*2))
                print(f"    添加左子节点: val={cur_node.left.val}, num={cur_num*2}")
            if cur_node.right:
                q.append(Node_num(cur_node.right, cur_num*2+1))
                print(f"    添加右子节点: val={cur_node.right.val}, num={cur_num*2+1}")
            
            print(f"    当前队列长度: {len(q)}")
            
            # 记录第一个和最后一个的num用来计算max
            if i == 0:
                first = cur_num
                print(f"    ✅ first = {first}")
            
            # ⚠️ 问题在这里！
            print(f"    检查: i={i}, len(q)={len(q)}, len(q)-1={len(q)-1}")
            if i == len(q) - 1:  # ❌ 问题：len(q) 在循环中会变化！
                last = cur_num
                print(f"    ✅ last = {last}")
            else:
                print(f"    ❌ 不满足条件，last 未更新")
        
        print(f"\n  层结果: first={first}, last={last}")
        if last > 0:
            width = last - first + 1
            print(f"  宽度 = {last} - {first} + 1 = {width}")
            max_width = max(max_width, width)
        else:
            print(f"  ⚠️ last 未正确设置！")
        print(f"  当前 max_width = {max_width}")

    return max_width

print("\n追踪执行:")
trace_widthOfBinaryTree(root1)




















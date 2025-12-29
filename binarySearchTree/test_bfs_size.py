from collections import deque
from binaryTree_more import TreeNode

# 创建测试树
#     1
#    / \
#   2   3
#  / \ / \
# 4  5 6  7

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.left = TreeNode(6)
root.right.right = TreeNode(7)

print("=" * 60)
print("❌ 方式1：在 for 循环中使用 len(q)")
print("=" * 60)

def bfs_with_len_in_loop(root):
    if not root:
        return []
    
    q = deque([root])
    res = []
    level = 0
    
    while q:
        level += 1
        level_res = []
        print(f"\n【第 {level} 层】")
        print(f"  进入循环前：队列长度 = {len(q)}, 队列内容 = {[n.val for n in q]}")
        
        # ❌ 在 for 循环中使用 len(q)
        for i in range(len(q)):  # range() 会立即计算，但 len(q) 在循环中会变化
            cur = q.popleft()
            level_res.append(cur.val)
            print(f"    迭代 {i}: 处理节点 {cur.val}")
            print(f"      popleft 后：队列长度 = {len(q)}, 队列内容 = {[n.val for n in q]}")
            
            if cur.left:
                q.append(cur.left)
                print(f"      添加左子节点 {cur.left.val} 后：队列长度 = {len(q)}")
            if cur.right:
                q.append(cur.right)
                print(f"      添加右子节点 {cur.right.val} 后：队列长度 = {len(q)}")
        
        res.append(level_res)
        print(f"  完成第 {level} 层，结果 = {level_res}")
        print(f"  循环后：队列长度 = {len(q)}, 队列内容 = {[n.val for n in q]}")
    
    return res

result1 = bfs_with_len_in_loop(root)

print("\n" + "=" * 60)
print("✅ 方式2：在循环前记录 size = len(q)")
print("=" * 60)

def bfs_with_fixed_size(root):
    if not root:
        return []
    
    q = deque([root])
    res = []
    level = 0
    
    while q:
        level += 1
        size = len(q)  # ✅ 固定记录当前层的节点数
        level_res = []
        print(f"\n【第 {level} 层】")
        print(f"  进入循环前：size = {size} (已固定), 队列内容 = {[n.val for n in q]}")
        
        # ✅ 使用固定的 size
        for i in range(size):  # 使用固定值，不会变化
            cur = q.popleft()
            level_res.append(cur.val)
            print(f"    迭代 {i}: 处理节点 {cur.val}")
            print(f"      popleft 后：队列长度 = {len(q)} (但循环次数已由 size={size} 确定)")
            
            if cur.left:
                q.append(cur.left)
                print(f"      添加左子节点 {cur.left.val} 后：队列长度 = {len(q)}")
            if cur.right:
                q.append(cur.right)
                print(f"      添加右子节点 {cur.right.val} 后：队列长度 = {len(q)}")
        
        res.append(level_res)
        print(f"  完成第 {level} 层，结果 = {level_res}")
        print(f"  循环后：队列长度 = {len(q)}, 队列内容 = {[n.val for n in q]}")
    
    return res

result2 = bfs_with_fixed_size(root)

print("\n" + "=" * 60)
print("结果对比")
print("=" * 60)
print(f"方式1结果: {result1}")
print(f"方式2结果: {result2}")
print(f"结果相同: {result1 == result2}")

print("\n" + "=" * 60)
print("关键理解")
print("=" * 60)
print("""
虽然两种方式在这个简单例子中都能正常工作，但关键区别在于：

1. 方式1（❌）：
   - range(len(q)) 在循环开始时会立即计算迭代次数
   - 但在循环过程中，len(q) 会不断变化（虽然不影响已确定的迭代次数）
   - 代码意图不够清晰

2. 方式2（✅）：
   - size = len(q) 明确固定了"当前层的节点数"
   - 代码意图清晰：我要处理这一层的所有节点
   - 更安全，避免潜在 bug
   - 符合所有标准 BFS 模板

结论：虽然都能工作，但方式2是最佳实践！
""")




















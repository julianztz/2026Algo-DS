class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def detectCycle(head):
    """
    使用快慢指针找到链表中环的入口节点
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    if not head or not head.next:
        return None
    
    # 第一阶段：检测是否有环
    slow = head
    fast = head
    
    print("=== 第一阶段：检测环 ===")
    print("从第一个实际节点开始，不是dummy head！")
    print(f"起始位置: slow={slow.val}, fast={fast.val}")
    
    step = 0
    while fast and fast.next:
        step += 1
        print(f"\n步骤{step}:")
        print(f"  移动前: slow={slow.val}, fast={fast.val}")
        
        # slow走1步
        slow = slow.next
        print(f"  slow走1步: {slow.val}")
        
        # fast走2步
        print(f"  fast走2步: {fast.val} -> ", end="")
        fast = fast.next
        print(f"{fast.val} -> ", end="")
        fast = fast.next
        print(f"{fast.val}")
        
        print(f"  移动后: slow={slow.val}, fast={fast.val}")
        
        if slow == fast:
            print("✅ 发现环！快慢指针相遇")
            print(f"相遇点: 节点{slow.val}")
            break
    else:
        print("❌ 无环")
        return None
    
    # 第二阶段：找到环的入口
    print("\n=== 第二阶段：找环入口 ===")
    print("数学原理: a = c (头到环入口 = 相遇点到环入口)")
    slow = head  # 重置slow到头部
    print(f"重置后: slow={slow.val}, fast={fast.val}")
    
    step = 0
    while slow != fast:
        step += 1
        slow = slow.next
        fast = fast.next
        print(f"步骤{step}: slow={slow.val}, fast={fast.val}")
    
    print(f"🎯 环的入口节点值: {slow.val}")
    return slow

def createCycleList():
    """创建带环的链表: 1->2->3->4->5->2"""
    # 创建节点
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)
    
    # 连接节点
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node2  # 成环：5指向2
    
    return node1

def explainFastPointerMovement():
    """详细解释快慢指针的移动过程"""
    print("=== 快慢指针移动详解 ===")
    print("链表结构: 1->2->3->4->5->2(成环)")
    print("环结构: 2->3->4->5->2->3->4->5->...")
    print()
    
    print("第一阶段：检测环")
    print("步骤1: slow=1, fast=1")
    print("  slow走1步: 1->2")
    print("  fast走2步: 1->2->3")
    print("  结果: slow=2, fast=3")
    print()
    
    print("步骤2: slow=2, fast=3")
    print("  slow走1步: 2->3")
    print("  fast走2步: 3->4->5")
    print("  结果: slow=3, fast=5")
    print()
    
    print("步骤3: slow=3, fast=5")
    print("  slow走1步: 3->4")
    print("  fast走2步: 5->2->3")
    print("  结果: slow=4, fast=3")
    print()
    
    print("步骤4: slow=4, fast=3")
    print("  slow走1步: 4->5")
    print("  fast走2步: 3->4->5")
    print("  结果: slow=5, fast=5")
    print("  ✅ 相遇！在节点5相遇")
    print()
    
    print("第二阶段：找环入口")
    print("数学原理: 头到环入口距离 = 相遇点到环入口距离")
    print("重置slow到头部，两个指针同速移动")
    print("步骤1: slow=1, fast=5")
    print("  同时走1步: slow=2, fast=2")
    print("  ✅ 相遇！环入口是节点2")

def printList(head, max_steps=10):
    """打印链表（限制步数避免无限循环）"""
    result = []
    current = head
    step = 0
    
    while current and step < max_steps:
        result.append(str(current.val))
        current = current.next
        step += 1
    
    if step >= max_steps:
        result.append("...")
    
    return " -> ".join(result)

# 测试
if __name__ == "__main__":
    print("创建带环链表: 1->2->3->4->5->2...")
    head = createCycleList()
    print(f"链表: {printList(head)}")
    print()
    
    # 解释快指针移动
    explainFastPointerMovement()
    print()
    
    # 找环的入口
    cycle_start = detectCycle(head)
    
    if cycle_start:
        print(f"\n🎉 环的入口节点值: {cycle_start.val}")
    else:
        print("\n❌ 未找到环")

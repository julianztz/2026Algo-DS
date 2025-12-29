from linkedList_twoPointers import *


# lc206 reverse linkedlist
class Solution:
    # way1 iterative -- 三指针！！
    # 核心： 一个个node link依次换顺序，因为每次loop需要断开link，所以nxt指针记录下个node
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:

        if not head or not head.next:
            return head

        pre, cur, nxt = None, head, head.next
        while cur:                   # 1->2->3
            # 三个pointers向后移动一位；改变一个next方向
            cur.next = pre          # 1<-2 3
            pre = cur
            cur = nxt
            if nxt:
                nxt = nxt.next
        return pre


    # way2 递归！！
    # [1 2 3 4 5]
    def reverseListRecursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 1. 基础情况return 当前node 
        if not head or not head.next:    # 只有一个node
            return head

        # 2. recursive -- 走到list结尾（倒数第二个），反转
        last = self.reverseListRecursive(head.next)     # head 4 -> last 5 始终为5，最后return node5作为新的head！！
        head.next.next = head                           # 反转4 5
        head.next = None

        return last


    # lc92 reverse linked list 2 - 反转链表中第left到第right个节点
    # 例如: [1,2,3,4] left=2, right=3 -> [1,3,2,4]
    '''
    思路： 头插法 
    0.check 单个节点swap（不变） ; dummy head 因为有可能有头节点改变操作
    1.找到起始位置之前 prev 和起始位置 cur
    2.for (right - left) -- 三指针
        ！！！ prev 和 cur 永远指向那两个node不变！！！
        cur 的下一个node移动到 反转链头部
        整个反转链向后shift一位

    '''
    
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if left == right:
            return head
        
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        
        # 找到第left-1个节点（需要反转部分的前一个节点）
        for _ in range(left - 1):
            prev = prev.next
        
        # 开始反转
        # prev -> 1, cur -> 2, next -> 3, ...
        cur = prev.next  # 要反转部分的第一个节点
        
        # 反转left到right之间的节点
        for _ in range(right - left):
            next_temp = cur.next
            cur.next = next_temp.next
            next_temp.next = prev.next
            prev.next = next_temp
        
        return dummy.next


    # lc25 Reverse Nodes in k-Group
    '''
    Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.
    k is a positive integer and is less than or equal to the length of the linked list.
    If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

    You may not alter the values in the list's nodes, only nodes themselves may be changed.

    思路：类似reverseBetween
    every k nodes, 先读到end
        如果未超过list长度，reverse这一段
        如果超过说明读完linkedlist，直接return
    '''
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        cur = head

        while cur:
            p = cur           # poseidon 移动用指针 用来确保能读到k个nodes

            # 1. 读至第 k 个nodes（end）
            for _ in range(k):
                if not p:
                    return dummy.next
                p = p.next

            # 2. reverse目前 k 个nodes：prev / cur / p  (头插)
            for _ in range(k - 1):  # 需要 k-1 次操作
                next_temp = cur.next
                cur.next = next_temp.next
                next_temp.next = prev.next
                prev.next = next_temp

            prev = cur
            cur = cur.next


        return dummy.next



    # 234 回文链表 
    # O(n) time + O(1) space -- 遍历一遍 + 指针
    '''
    思路：
    快慢指针找中点 （区分奇数偶数node）
    反转后半list
    最后比较：此时pre指向end，head同时开始move，直到指向同一个node？？
    '''
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        # 边界情况
        if not head or not head.next:
            return True
        
        # 步骤1：找到中点（使用快慢指针）
        # 问题1：fast和slow应该从哪个节点开始？
        # 问题2：slow最终会停在哪个位置？是中间节点还是中间的前一个？
        slow = head
        fast = head
        half_size = 0          
        while fast and fast.next:
            slow = slow.next                      # slow at 中间 或者 中间+1
            fast = fast.next.next                 # fast at 最后 或者 Null
            half_size += 1

        # 奇数list -- skip 中间node
        if fast:            # 快指针在最后一个node -- odd
            slow = slow.next

        # 步骤2：反转后半部分！！
        # 问题3：后半部分应该从哪个节点开始？
        # 问题4：slow停在中间，那么后半部分的头是slow还是slow.next？
        pre, cur, nxt = None, slow, slow.next
        while cur:
            cur.next = pre
            pre = cur
            cur = nxt
            if nxt:
                nxt = nxt.next
        # 反转后
        # 前半部分：1 -> 2 -> 3 
        #          h       None
        # 后半部分：None <- 2 <- 1     None
        #                       pre  cur/nxt  

        # 步骤3：比较前半部分和后半部分
        # 问题5：如何确保两个指针同时到达末尾？
        while pre:
            if pre.val != head.val:
                return False
            pre = pre.next
            head = head.next

        return True
        
        # 步骤4：（可选）恢复链表结构

    # 不推荐但是简单 O(n) O(n)
    def isPalindromePython(self, head: Optional[ListNode]) -> bool:
        arr = []
        while head:
            arr.append(head.val)
            head = head.next


        return arr == arr[::-1]
        

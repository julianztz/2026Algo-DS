from typing import Optional, List


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:

    # 141 linkedlistCycle
    def hasCycle(self, head: ListNode) -> bool:
        fast = head
        slow = head

        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

            if fast == slow:
                return True

        return False

    # 142 linkedlistCycle2 -- Floyd algo
    '''
    Given the head of a linked list, return the node where the cycle begins.
    If there is no cycle, return null.
    '''
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = head
        slow = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast == slow:     # meet point
                break

        if not (fast and fast.next):  
            return None

        slow = head
        while fast != slow:      # k - m
            fast = fast.next 
            slow = slow.next
        return slow


    # 19 remove Nth node from the end of list
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0)
        dummy.next = head
        p1 = dummy
        p2 = dummy

        for _ in range(n):
            p1 = p1.next

        if not p1:  # n大于链表长度
            return dummy.next

        while p1.next:
            p1 = p1.next
            p2 = p2.next

        # p2 right before target
        p2.next = p2.next.next
        return dummy.next



    # 21 merge two sorted lists
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        p1 = list1
        p2 = list2
        dummy = ListNode(0)  # 修复：传递参数给ListNode
        p3 = dummy

        while p1 and p2:
            if p1.val <= p2.val:  # 优化：使用<=保持稳定性
                p3.next = p1
                p1 = p1.next
            else:
                p3.next = p2
                p2 = p2.next
            p3 = p3.next

        # 处理剩余节点
        p3.next = p1 if p1 else p2

        return dummy.next  # 修复：返回实际头节点


    # 23 merge k sorted lists
    def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return []

        dummy = ListNode(0)
        p = dummy

        while True:    # 遍历所有node

            min_val = float('inf')
            min_idx = -1           # min所在的linkedlist
            p_min = None

            for i in range(len(lists)):
                if lists[i] and lists[i].val < min_val:
                    min_val = lists[i].val
                    min_idx = i
                    p_min = lists[i]

            if min_idx == -1:
                break
            # 更新结果链表
            p.next = p_min
            p = p.next

            lists[min_idx] = lists[min_idx].next

        return dummy.next



            



        return dummy.next




    # 876 middle of the linked list
    def middleNode(self, head: ListNode) -> ListNode:
        fast = head
        slow = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

        return slow

    # 160 intersection of two linked lists
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        p1 = headA
        p2 = headB

        while p1 != p2:
            if p1:
                p1 = p1.next
            else:
                p1 = headB
            
            if p2:
                p2 = p2.next
            else:
                p2 = headA
        return p1

    # 86 partition list
    '''
    Given the head of a linked list and a value x, 
    partition it such that all nodes less than x come before nodes greater than or equal to x.
    You should preserve the original relative order of the nodes in each of the two partitions.
    '''
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        p = head
        dummy_small = ListNode(0)
        dummy_big = ListNode(0)
        p1, p2 = dummy_small, dummy_big

        while p:
            if p.val < x:
                p1.next = p
                p1 = p1.next
            else:
                p2.next = p
                p2 = p2.next

            # 必须打断原链表，否则可能出现cycle
            temp = p.next
            p.next = None
            p = temp

        p1.next = dummy_big.next
        return dummy_small.next

    # 83 remove duplicate from sorted list
    '''
    delete all duplicates such that each element appears only once. 
    Return the linked list sorted as well.

    思路： 快慢指针。 loop 快指针，当快指针val不等于慢指针，慢指针next指向快指针
    tricky: 最后当fast到None，slow也需要指过去
    '''
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = head
        fast = head
        while fast:
            fast = fast.next
            if not fast or fast.val != slow.val:
                slow.next = fast
                slow = fast
        return head

    # $$$ redo 82 remove duplicates from sorted list -- 进阶版
    '''
    Given the head of a sorted linked list, 
    delete all nodes that have duplicate numbers, 
    leaving only distinct numbers from the original list. 
    Return the linked list sorted as well.
    思路：需要完全删除有重复的node，所以选择三指针prev cur cur.next, prev来track需要删除node之前，以便于link到下一个
    '''
    def deleteDuplicates2(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
            
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy  # 指向当前确定不重复的节点
        curr = head   # 当前检查的节点
        
        while curr:
            # 如果当前节点和下一个节点值相同，跳过所有重复节点
            if curr.next and curr.val == curr.next.val:
                duplicate_val = curr.val
                # 跳过所有值为duplicate_val的节点
                while curr and curr.val == duplicate_val:
                    curr = curr.next
                # 连接prev到下一个不重复的节点
                prev.next = curr
            else:
                # 当前节点不重复，移动到下一个
                prev = curr
                curr = curr.next
                
        return dummy.next



    # $$$ redo 2 add two numbers
    '''
    You are given two non-empty linked lists representing two non-negative integers. 
    The digits are stored in reverse order, and each of their nodes contains a single digit.
    Add the two numbers and return the sum as a linked list.
    '''
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        curr = dummy
        carry = 0

        while l1 or l2 or carry:
            # 获取当前位的值，如果链表为空则为0
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            
            # 计算当前位的和
            total = val1 + val2 + carry
            carry = total // 10  # 计算进位
            digit = total % 10   # 计算当前位的值
            
            # 创建新节点
            curr.next = ListNode(digit)
            curr = curr.next
            
            # 移动到下一个节点
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next

        





    # $$$ redo 23 merge k sorted list -- priorty queue OR divide and conquer(recursive)
    '''
    You are given an array of k linked-lists lists, 
    each linked-list is sorted in ascending order.
    Merge all the linked-lists into one sorted linked-list and return it.
    '''
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        if len(lists) == 1:
            return lists[0]
        
        # 分治法：将k个链表分成两半，递归合并
        mid = len(lists) // 2
        left = self.mergeKLists(lists[:mid])
        right = self.mergeKLists(lists[mid:])
        return self.mergeTwoLists(left, right)
    
    # 方法2：优先队列（堆）- 时间复杂度O(N log k)
    def mergeKLists_Heap(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        import heapq
        
        heap = []
        dummy = ListNode(0)
        p = dummy
        
        # 将每个链表的头节点加入堆
        for i, lst in enumerate(lists):
            if lst:
                heapq.heappush(heap, (lst.val, i, lst))
        
        while heap:
            val, i, node = heapq.heappop(heap)
            p.next = node
            p = p.next
            
            # 如果该链表还有下一个节点，加入堆
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        
        return dummy.next
    
    # 方法3：顺序合并 - 时间复杂度O(kN)
    def mergeKLists_Sequential(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        
        result = lists[0]
        for i in range(1, len(lists)):
            result = self.mergeTwoLists(result, lists[i])
        return result



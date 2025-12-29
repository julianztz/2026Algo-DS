'''
WHY list?
链表的节点不需要挨在一起，给点内存 new 出来一个节点就能用，操作系统会觉得这娃好养活。
不需要考虑扩缩容和数据搬移的问题，理论上讲，链表是没有容量限制的

con: 不如array通过index访问迅速
'''


# 单链表
class ListNode:
    def __init__(self, element, next=None):
        self.val = element
        self.next = next

# 单链表生成工具，输入array自动convert为链表
def createLinkedList(arr: 'list[int]') -> 'ListNode':
    if not arr:
        return None

    head = ListNode(arr[0])
    cur = head
    for i in range(1, len(arr)):
        cur.next = ListNode(arr[i])
        cur = cur.next

    return head

# 单链表遍历
head = createLinkedList([2,5,6,3,1])
cur = head
while cur:                   # cur node is NOT None!!
    # print(cur.val)
    cur = cur.next





# 双链表
class DoubleListNode:
    def __init__(self, element, prev=None, next=None) -> None:
        self.val = element
        self.prev = prev
        self.next = next

# 双链表生成工具
def createDoubleLinkedList(arr: 'list[int]') -> 'DoubleListNode':
    if not arr:
        return None

    head = DoubleListNode(arr[0])
    cur = head
    for i in range(1, len(arr)):
        new_node = DoubleListNode(arr[i])
        cur.next = new_node
        new_node.prev = cur
        cur = new_node

    return head

# 双链表遍历: 向前 & 向后
head = createDoubleLinkedList([1, 2, 3, 4, 5])
tail = head
while tail.next:
    tail = tail.next

# 根据target node与head和tail距离决定向前或者向后遍历--提高效率
cur = head
while cur:
    print(cur.val)
    cur = cur.next

cur = tail
while cur:
    print(cur.val)
    cur = cur.prev


# 删除第 4 个节点
# 先找到第 3 个节点
p = head
for i in range(2):
    p = p.next
# 现在 p 指向第 3 个节点，我们将它后面的那个节点摘除出去
toDelete = p.next
# 把 toDelete 从链表中摘除
p.next = toDelete.next
toDelete.next.prev = p

# 把 toDelete 的前后指针都置为 null 是个好习惯（可选）
toDelete.next = None
toDelete.prev = None

# 现在链表变成了 1 -> 2 -> 3 -> 5




'''
lc707 design linkedList API
double / single
'''
# single linked list
class MyLinkedList:

    class Node:
        def __init__(self, val=None) -> None:
            self.val = val
            self.next = None

    def __init__(self):
        self.dummy_head = self.Node()
        self.size = 0

    # 获取链表中下标为 index 的节点的值。如果下标无效，则返回 -1 
    def get(self, index: int) -> int:
        if index >= self.size or index < 0:
            return -1
        else:
            cur = self.dummy_head.next  # 从第一个真实节点开始
            for _ in range(index):
                cur = cur.next
            return cur.val

    #  将一个值为 val 的节点插入到链表中第一个元素之前。在插入完成后，新节点会成为链表的第一个节点。
    def addAtHead(self, val: int) -> None:
        new_node = self.Node(val)                     # 创建新节点
        new_node.next = self.dummy_head.next          # 新节点指向原来的第一个节点
        self.dummy_head.next = new_node               # dummy head指向新节点
        self.size += 1

    # 将一个值为 val 的节点追加到链表中作为链表的最后一个元素。
    def addAtTail(self, val: int) -> None:
        tail = self.dummy_head
        while tail.next:
            tail = tail.next                    # 找到tail node
        
        node_to_add = self.Node(val)
        tail.next = node_to_add
        self.size += 1

    # 将一个值为 val 的节点插入到链表中下标为 index 的节点之前。
    # 如果 index 等于链表的长度，那么该节点会被追加到链表的末尾。
    # 如果 index 比长度更大，该节点将 不会插入 到链表中。
    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.size or index < 0:
            return
        elif index == self.size:
            self.addAtTail(val)
        else:
            node_to_add = self.Node(val)
            cur = self.dummy_head
            for _ in range(index):  # 找到index-1位置
                cur = cur.next
            node_to_add.next = cur.next
            cur.next = node_to_add
            self.size += 1
            
    #  如果下标有效，则删除链表中下标为 index 的节点。
    def deleteAtIndex(self, index: int) -> None:
        if index >= self.size or index < 0:
            return
        
        cur = self.dummy_head
        for _ in range(index):  # 找到index-1位置
            cur = cur.next
        cur.next = cur.next.next  # 跳过要删除的节点
        self.size -= 1


# double linked list
# 优势：尾部指针使得尾部操作更快
class MyDoubleLinkedList:

    class Node:
        def __init__(self, val=None) -> None:
            self.val = val
            self.next = None
            self.prev = None

    def __init__(self):
        self.dummy_head = self.Node()
        self.dummy_tail = self.Node()
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head
        self.size = 0

    # 获取链表中下标为 index 的节点的值。如果下标无效，则返回 -1 
    def get(self, index: int) -> int:
        if index >= self.size or index < 0:
            return -1
        else:
            # if index <= self.size / 2:        
            cur = self.dummy_head.next  # 从第一个真实节点开始 forward
            for _ in range(index):
                cur = cur.next
            return cur.val
            # else:
            #     cur = self.dummy_tail.prev  # backward
            #     for _ in range(self.size - 1 - index):
            #         cur = cur.prev
            #     return cur.val

    #  将一个值为 val 的节点插入到链表中第一个元素之前。在插入完成后，新节点会成为链表的第一个节点。
    def addAtHead(self, val: int) -> None:
        new_node = self.Node(val)                     # 创建新节点
        new_node.next = self.dummy_head.next          # 新节点指向原来的第一个节点
        new_node.prev = self.dummy_head               # 新节点的prev指向dummy_head
        self.dummy_head.next.prev = new_node          # 原第一个节点的prev指向新节点
        self.dummy_head.next = new_node               # dummy head指向新节点
        self.size += 1

    # 将一个值为 val 的节点追加到链表中作为链表的最后一个元素。
    def addAtTail(self, val: int) -> None:
        node_to_add = self.Node(val)
        node_to_add.prev = self.dummy_tail.prev       # 新节点的prev指向原最后一个节点
        node_to_add.next = self.dummy_tail            # 新节点的next指向dummy_tail
        self.dummy_tail.prev.next = node_to_add       # 原最后一个节点的next指向新节点
        self.dummy_tail.prev = node_to_add            # dummy_tail的prev指向新节点
        self.size += 1

    # 将一个值为 val 的节点插入到链表中下标为 index 的节点之前。
    # 如果 index 等于链表的长度，那么该节点会被追加到链表的末尾。
    # 如果 index 比长度更大，该节点将 不会插入 到链表中。
    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.size or index < 0:
            return
        elif index == self.size:
            self.addAtTail(val)
        else:
            node_to_add = self.Node(val)
            # if index <= self.size / 2:       # forward
            cur = self.dummy_head
            for _ in range(index):       # 找到index-1位置
                cur = cur.next
            node_to_add.next = cur.next
            node_to_add.prev = cur
            cur.next.prev = node_to_add
            cur.next = node_to_add
            # else:
            #     cur = self.dummy_tail.prev
            #     for _ in range(self.size - index - 1):
            #         cur = cur.prev
            #     node_to_add.next = cur.next
            #     node_to_add.prev = cur
            #     cur.next.prev = node_to_add
            #     cur.next = node_to_add
            self.size += 1
            

    #  如果下标有效，则删除链表中下标为 index 的节点。
    def deleteAtIndex(self, index: int) -> None:
        if index >= self.size or index < 0:
            return
        
        # if index <= self.size / 2:       # forward
        cur = self.dummy_head
        for _ in range(index):       # 找到index-1位置
            cur = cur.next
        to_delete = cur.next
        cur.next = to_delete.next
        to_delete.next.prev = cur
        # else:                           # backward
        #     cur = self.dummy_tail
        #     for _ in range(self.size - index - 1):
        #         cur = cur.prev
        #     to_delete = cur.prev
        #     cur.prev = to_delete.prev
        #     to_delete.prev.next = cur
        
        self.size -= 1
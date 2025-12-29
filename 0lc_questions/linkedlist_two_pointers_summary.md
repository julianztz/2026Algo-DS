# 链表双指针问题总结

## 1. 双指针类型

### 1.1 快慢指针（Fast-Slow Pointers）
- **模式**: 一个指针移动快，一个指针移动慢
- **常见速度比**: 2:1（fast 走 2 步，slow 走 1 步）
- **应用**: 检测环、找中点、找倒数第 N 个节点

### 1.2 前后指针（Leading-Trailing Pointers）
- **模式**: 一个指针先走 N 步，然后两个指针同时移动
- **应用**: 删除倒数第 N 个节点

### 1.3 左右指针（Two Pointers on Different Lists）
- **模式**: 两个指针分别在不同链表上移动
- **应用**: 合并两个排序链表、链表相交

### 1.4 三指针（Three Pointers）
- **模式**: 使用三个指针追踪不同位置
- **应用**: 删除所有重复元素、复杂链表操作

---

## 2. 常见问题类型

### 2.1 检测环（Cycle Detection）

**问题**: LC141 - 判断链表是否有环

**模式**: 快慢指针（Floyd 算法）

**关键点**:
- ✅ 初始位置：`fast = slow = head`
- ✅ 循环条件：`while fast and fast.next`
- ✅ 移动：`fast = fast.next.next`, `slow = slow.next`
- ✅ 判断：`if fast == slow: return True`

**注意事项**:
- ⚠️ 必须检查 `fast.next`，避免 `None.next` 报错
- ⚠️ 从第一个实际节点开始，不是 dummy head

```python
def hasCycle(self, head: ListNode) -> bool:
    fast = head
    slow = head
    
    while fast and fast.next:  # ✅ 必须检查 fast.next
        fast = fast.next.next
        slow = slow.next
        
        if fast == slow:
            return True
    
    return False
```

---

### 2.2 找环入口（Cycle Entry Point）

**问题**: LC142 - 找到环的入口节点

**模式**: 快慢指针（Floyd 算法 - 两阶段）

**关键点**:
- ✅ 第一阶段：检测环，找到相遇点
- ✅ 第二阶段：重置 slow 到 head，两个指针同速移动
- ✅ 数学原理：头到环入口距离 = 相遇点到环入口距离

**注意事项**:
- ⚠️ 第一阶段后要检查是否有环（`if not (fast and fast.next)`）
- ⚠️ 第二阶段两个指针都走 1 步（不是 fast 走 2 步）

```python
def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
    fast = head
    slow = head
    
    # 第一阶段：检测环
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
        if fast == slow:
            break
    
    # 检查是否有环
    if not (fast and fast.next):
        return None
    
    # 第二阶段：找环入口
    slow = head  # ✅ 重置 slow 到头部
    while fast != slow:
        fast = fast.next  # ✅ 同速移动
        slow = slow.next
    
    return slow
```

---

### 2.3 找中点（Middle Node）

**问题**: LC876 - 找到链表的中点

**模式**: 快慢指针

**关键点**:
- ✅ 初始位置：`fast = slow = head`
- ✅ 循环条件：`while fast and fast.next`
- ✅ 移动：`fast = fast.next.next`, `slow = slow.next`
- ✅ 结果：`slow` 指向中点（奇数长度）或前半部分的最后一个（偶数长度）

**注意事项**:
- ⚠️ 偶数长度时，slow 指向前半部分的最后一个节点
- ⚠️ 如果需要后半部分的第一个，可以用 `slow.next`

```python
def middleNode(self, head: ListNode) -> ListNode:
    fast = head
    slow = head
    
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    return slow  # 奇数：中点，偶数：前半部分最后一个
```

---

### 2.4 删除倒数第 N 个节点（Remove Nth from End）

**问题**: LC19 - 删除链表中倒数第 n 个节点

**模式**: 前后指针（Leading-Trailing）

**关键点**:
- ✅ 使用 dummy head 简化边界情况
- ✅ 先让 p1 走 n 步
- ✅ 然后 p1 和 p2 同时移动，直到 p1 到达末尾
- ✅ 此时 p2 指向要删除节点的前一个节点

**注意事项**:
- ⚠️ 必须使用 dummy head，否则无法删除头节点
- ⚠️ 检查 n 是否大于链表长度（`if not p1`）
- ⚠️ 循环条件是 `while p1.next`，不是 `while p1`

```python
def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0)  # ✅ 必须使用 dummy head
    dummy.next = head
    p1 = dummy
    p2 = dummy
    
    # p1 先走 n 步
    for _ in range(n):
        p1 = p1.next
    
    # 检查 n 是否大于链表长度
    if not p1:
        return dummy.next
    
    # 两个指针同时移动
    while p1.next:  # ✅ 注意是 p1.next
        p1 = p1.next
        p2 = p2.next
    
    # p2 指向要删除节点的前一个节点
    p2.next = p2.next.next
    return dummy.next
```

---

### 2.5 合并两个排序链表（Merge Two Sorted Lists）

**问题**: LC21 - 合并两个升序链表

**模式**: 左右指针（Two Pointers on Different Lists）

**关键点**:
- ✅ 使用 dummy head 简化代码
- ✅ 比较两个指针的值，选择较小的
- ✅ 处理剩余节点

**注意事项**:
- ⚠️ 使用 `<=` 保持稳定性（相同值保持原顺序）
- ⚠️ 最后要处理剩余节点（`p3.next = p1 if p1 else p2`）

```python
def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
    p1 = list1
    p2 = list2
    dummy = ListNode(0)
    p3 = dummy
    
    while p1 and p2:
        if p1.val <= p2.val:  # ✅ 使用 <= 保持稳定性
            p3.next = p1
            p1 = p1.next
        else:
            p3.next = p2
            p2 = p2.next
        p3 = p3.next
    
    # 处理剩余节点
    p3.next = p1 if p1 else p2
    
    return dummy.next
```

---

### 2.6 链表相交（Intersection of Two Linked Lists）

**问题**: LC160 - 找到两个链表的相交节点

**模式**: 左右指针 + 交换路径

**关键点**:
- ✅ 两个指针分别从两个链表头部开始
- ✅ 到达末尾后，交换到另一个链表的头部
- ✅ 数学原理：a + c + b = b + c + a（c 是公共部分）

**注意事项**:
- ⚠️ 如果没有相交，两个指针会同时到达 None（`p1 == p2 == None`）
- ⚠️ 循环条件是 `while p1 != p2`，不是 `while p1 and p2`

```python
def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
    p1 = headA
    p2 = headB
    
    while p1 != p2:
        # 到达末尾后，交换到另一个链表
        p1 = p1.next if p1 else headB
        p2 = p2.next if p2 else headA
    
    return p1  # 如果相交返回交点，否则返回 None
```

---

### 2.7 删除重复元素（Remove Duplicates）

**问题**: LC83 - 删除排序链表中的重复元素（保留一个）

**模式**: 快慢指针

**关键点**:
- ✅ slow 指向当前不重复的节点
- ✅ fast 向前移动，找到下一个不同的值
- ✅ 当 fast.val != slow.val 时，连接 slow.next = fast

**注意事项**:
- ⚠️ 最后当 fast 到 None 时，slow 也需要指向 None
- ⚠️ 循环条件：`while fast`，然后在循环内移动 fast

```python
def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head
    
    while fast:
        fast = fast.next
        if not fast or fast.val != slow.val:
            slow.next = fast
            slow = fast
    
    return head
```

---

### 2.8 删除所有重复元素（Remove All Duplicates）

**问题**: LC82 - 删除所有重复的节点（不保留）

**模式**: 三指针（prev, curr, curr.next）

**关键点**:
- ✅ 使用 dummy head 简化边界情况
- ✅ prev 指向当前确定不重复的节点
- ✅ curr 检查当前节点
- ✅ 如果发现重复，跳过所有重复节点

**注意事项**:
- ⚠️ 必须使用 dummy head，因为头节点可能被删除
- ⚠️ 跳过重复节点时，要跳过所有相同值的节点

```python
def deleteDuplicates2(self, head: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0)  # ✅ 必须使用 dummy head
    dummy.next = head
    prev = dummy  # 指向当前确定不重复的节点
    curr = head   # 当前检查的节点
    
    while curr:
        # 如果当前节点和下一个节点值相同，跳过所有重复节点
        if curr.next and curr.val == curr.next.val:
            duplicate_val = curr.val
            # 跳过所有值为 duplicate_val 的节点
            while curr and curr.val == duplicate_val:
                curr = curr.next
            # 连接 prev 到下一个不重复的节点
            prev.next = curr
        else:
            # 当前节点不重复，移动到下一个
            prev = curr
            curr = curr.next
    
    return dummy.next
```

---

### 2.9 分割链表（Partition List）

**问题**: LC86 - 将链表分割为小于 x 和大于等于 x 两部分

**模式**: 双指针（两个 dummy head）

**关键点**:
- ✅ 使用两个 dummy head（small 和 big）
- ✅ 遍历原链表，根据值分配到 small 或 big
- ✅ **必须打断原链表**，否则可能出现 cycle

**注意事项**:
- ⚠️ **关键**：必须打断原链表（`p.next = None`），否则可能出现 cycle
- ⚠️ 最后连接 small 和 big：`p1.next = dummy_big.next`

```python
def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
    dummy_small = ListNode(0)
    dummy_big = ListNode(0)
    p1, p2 = dummy_small, dummy_big
    p = head
    
    while p:
        if p.val < x:
            p1.next = p
            p1 = p1.next
        else:
            p2.next = p
            p2 = p2.next
        
        # ✅ 必须打断原链表，否则可能出现 cycle
        temp = p.next
        p.next = None
        p = temp
    
    p1.next = dummy_big.next
    return dummy_small.next
```

---

## 3. 通用注意事项

### 3.1 边界情况处理

**必须检查的情况**:
- ✅ 空链表：`if not head: return None`
- ✅ 单节点链表：`if not head.next: return head`
- ✅ 链表长度为 1 或 2 的特殊情况

### 3.2 Dummy Head 的使用

**何时使用 dummy head**:
- ✅ 需要删除或修改头节点时
- ✅ 简化边界情况处理
- ✅ 统一处理逻辑

**示例**:
```python
dummy = ListNode(0)
dummy.next = head
# ... 操作 ...
return dummy.next
```

### 3.3 循环条件

**常见循环条件**:
- ✅ `while fast and fast.next` - 快慢指针（fast 走 2 步）
- ✅ `while p1 and p2` - 两个指针都不为空
- ✅ `while p1 != p2` - 两个指针不相等（用于相交问题）
- ✅ `while p1.next` - 需要访问下一个节点时

### 3.4 指针移动顺序

**关键原则**:
- ✅ 先检查再移动（避免访问 None）
- ✅ 先移动再判断（根据问题需求）
- ✅ 注意移动的顺序（可能影响结果）

**示例**:
```python
# 错误：先移动再检查
while fast:
    fast = fast.next.next  # ❌ 可能访问 None.next

# 正确：先检查再移动
while fast and fast.next:
    fast = fast.next.next  # ✅ 安全
```

### 3.5 避免 Cycle

**常见导致 cycle 的情况**:
- ⚠️ 分割链表时，没有打断原链表
- ⚠️ 合并链表时，没有正确处理指针
- ⚠️ 删除节点时，没有正确断开连接

**解决方法**:
- ✅ 分割链表时，必须设置 `p.next = None`
- ✅ 合并链表时，确保指针正确移动
- ✅ 删除节点时，确保前后节点正确连接

---

## 4. 代码模板

### 4.1 快慢指针模板

```python
def fastSlowPointer(head: ListNode):
    fast = head
    slow = head
    
    while fast and fast.next:  # ✅ 必须检查 fast.next
        fast = fast.next.next
        slow = slow.next
        
        # 根据问题需求添加判断逻辑
        if condition:
            # 处理逻辑
            pass
    
    return result
```

### 4.2 前后指针模板

```python
def leadingTrailingPointer(head: ListNode, n: int):
    dummy = ListNode(0)  # ✅ 使用 dummy head
    dummy.next = head
    p1 = dummy
    p2 = dummy
    
    # p1 先走 n 步
    for _ in range(n):
        p1 = p1.next
    
    # 检查边界情况
    if not p1:
        return dummy.next
    
    # 两个指针同时移动
    while p1.next:  # ✅ 注意是 p1.next
        p1 = p1.next
        p2 = p2.next
    
    # 处理逻辑
    return dummy.next
```

### 4.3 双链表指针模板

```python
def twoListsPointers(head1: ListNode, head2: ListNode):
    p1 = head1
    p2 = head2
    dummy = ListNode(0)
    p3 = dummy
    
    while p1 and p2:
        # 根据问题需求选择逻辑
        if condition:
            p3.next = p1
            p1 = p1.next
        else:
            p3.next = p2
            p2 = p2.next
        p3 = p3.next
    
    # 处理剩余节点
    p3.next = p1 if p1 else p2
    
    return dummy.next
```

---

## 5. 易错点总结

### 5.1 空指针检查

**常见错误**:
- ❌ `while fast:` 然后 `fast = fast.next.next` - 可能访问 `None.next`
- ❌ 没有检查 `fast.next` 就访问 `fast.next.next`

**正确做法**:
- ✅ `while fast and fast.next:` 确保安全访问

### 5.2 循环条件

**常见错误**:
- ❌ `while p1 and p2:` 用于相交问题 - 会提前退出
- ❌ `while p1:` 用于删除倒数第 N 个 - 无法正确定位

**正确做法**:
- ✅ 根据问题需求选择合适的循环条件

### 5.3 指针移动

**常见错误**:
- ❌ 忘记移动指针，导致死循环
- ❌ 移动顺序错误，导致逻辑错误

**正确做法**:
- ✅ 确保每次循环都移动指针
- ✅ 注意移动的顺序和时机

### 5.4 Dummy Head

**常见错误**:
- ❌ 需要删除头节点时，没有使用 dummy head
- ❌ 返回时忘记返回 `dummy.next`

**正确做法**:
- ✅ 需要修改或删除头节点时，使用 dummy head
- ✅ 返回 `dummy.next`，不是 `dummy`

---

## 6. 时间复杂度分析

| 问题类型 | 时间复杂度 | 空间复杂度 |
|---------|-----------|-----------|
| 检测环 | O(n) | O(1) |
| 找环入口 | O(n) | O(1) |
| 找中点 | O(n) | O(1) |
| 删除倒数第 N 个 | O(n) | O(1) |
| 合并两个排序链表 | O(n + m) | O(1) |
| 链表相交 | O(n + m) | O(1) |
| 删除重复元素 | O(n) | O(1) |
| 删除所有重复元素 | O(n) | O(1) |
| 分割链表 | O(n) | O(1) |

**关键点**:
- ✅ 双指针方法通常时间复杂度为 O(n)
- ✅ 空间复杂度通常为 O(1)（不包括结果链表）

---

## 7. 总结

### 7.1 核心原则

1. **边界检查**: 始终检查空链表和单节点情况
2. **Dummy Head**: 需要修改头节点时使用
3. **循环条件**: 根据问题选择合适的循环条件
4. **指针移动**: 确保安全移动，避免访问 None
5. **避免 Cycle**: 注意断开原链表的连接

### 7.2 问题识别

- **检测环/找中点**: 快慢指针（2:1 速度比）
- **删除倒数第 N 个**: 前后指针（先走 N 步）
- **合并链表**: 双指针（两个链表）
- **删除重复**: 快慢指针（slow 追踪，fast 扫描）
- **分割链表**: 双指针（两个 dummy head）

### 7.3 调试技巧

1. **画图**: 画出链表结构和指针位置
2. **打印**: 打印指针的值和位置
3. **边界测试**: 测试空链表、单节点、两个节点
4. **特殊值**: 测试边界值（如 n=1, n=长度）

---

## 8. 练习建议

### 8.1 基础练习
1. LC141 - 检测环
2. LC876 - 找中点
3. LC19 - 删除倒数第 N 个节点

### 8.2 进阶练习
1. LC142 - 找环入口
2. LC21 - 合并两个排序链表
3. LC160 - 链表相交

### 8.3 高级练习
1. LC82 - 删除所有重复元素
2. LC86 - 分割链表
3. LC23 - 合并 k 个排序链表

---

**记住**: 双指针是链表问题的核心技巧，掌握好这些模式和注意事项，可以解决大部分链表问题！




























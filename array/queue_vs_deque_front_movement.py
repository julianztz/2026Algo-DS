# -*- coding: utf-8 -*-
"""
单端队列 vs 双端队列：为什么 front 移动方向不同？
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("核心问题：为什么单端队列 front 后移，双端队列 front 前移？")
print("=" * 70)

print("""
关键理解：操作方向决定了指针移动方向

【单端队列（Queue）】
  - front 端：只能删除（dequeue），不能插入
  - rear 端：只能插入（enqueue），不能删除
  
【双端队列（Deque）】
  - front 端：可以插入（insertFront）和删除（deleteFront）
  - rear 端：可以插入（insertLast）和删除（deleteLast）
""")

print("\n" + "=" * 70)
print("1. 单端队列（Queue）- front 只能删除，所以总是后移")
print("=" * 70)

print("""
单端队列的操作限制：
  ✅ rear 端：只能 enqueue（插入）
  ✅ front 端：只能 dequeue（删除）
  ❌ front 端：不能插入
  ❌ rear 端：不能删除

初始状态：front=0, rear=0
数组：[None, None, None]
      ↑
   front=rear=0

操作1: enqueue(1) - 在 rear 端插入
  在 rear=0 位置插入 1
  rear 后移到 1
  结果：front=0, rear=1
  数组：[1, None, None]
        ↑    ↑
      front rear

操作2: enqueue(2) - 在 rear 端插入
  在 rear=1 位置插入 2
  rear 后移到 2
  结果：front=0, rear=2
  数组：[1, 2, None]
        ↑       ↑
      front    rear

操作3: dequeue() - 在 front 端删除
  清空 front=0 位置
  front 后移到 1（因为只能删除，删除后移向下一个元素）
  结果：front=1, rear=2
  数组：[None, 2, None]
             ↑    ↑
           front rear

关键点：
  - front 只能删除，删除后需要指向下一个有效元素
  - 所以 front 总是后移（向右移动）
  - front 永远不会前移，因为不能在 front 端插入
""")

print("\n" + "=" * 70)
print("2. 双端队列（Deque）- front 可以插入，所以需要前移")
print("=" * 70)

print("""
双端队列的操作能力：
  ✅ front 端：可以 insertFront（插入）和 deleteFront（删除）
  ✅ rear 端：可以 insertLast（插入）和 deleteLast（删除）

初始状态：front=0, rear=0
数组：[None, None, None]
      ↑
   front=rear=0

操作1: insertLast(1) - 在 rear 端插入
  在 rear=0 位置插入 1
  rear 后移到 1
  结果：front=0, rear=1
  数组：[1, None, None]
        ↑    ↑
      front rear

操作2: insertFront(2) - 在 front 端插入
  要在 front=0 之前插入，需要：
  1. front 前移到 2（循环数组的最后一个位置）
  2. 在 front=2 位置插入 2
  结果：front=2, rear=1
  数组：[1, None, 2]
             ↑    ↑
           rear  front

关键点：
  - front 可以插入，插入时要在 front 之前插入
  - 所以 insertFront 时 front 需要前移（向左移动）
  - deleteFront 时 front 后移（向右移动），和单端队列一样
""")

print("\n" + "=" * 70)
print("3. 对比：为什么移动方向不同？")
print("=" * 70)

print("""
【单端队列】
  front 端操作：只有 dequeue（删除）
    - 删除后，front 指向下一个有效元素
    - 所以 front 总是后移（向右）
    - front 永远不会前移

【双端队列】
  front 端操作：insertFront（插入）和 deleteFront（删除）
    - insertFront：要在 front 之前插入，所以 front 前移（向左）
    - deleteFront：删除后，front 指向下一个有效元素，所以 front 后移（向右）
    - front 可以前移也可以后移

可视化对比：

单端队列 front 移动：
  删除 → 删除 → 删除
  ←─────── 只能后移（向右）

双端队列 front 移动：
  插入 ← 插入 ← 插入
  ───────→ 可以前移（向左）也可以后移（向右）
  删除 → 删除 → 删除
""")

print("\n" + "=" * 70)
print("4. 详细示例：双端队列的 front 移动")
print("=" * 70)

print("""
初始：front=0, rear=0, size=0
数组：[None, None, None]
      ↑
   front=rear=0

步骤1: insertLast(1)
  在 rear=0 插入 1，rear 后移到 1
  结果：front=0, rear=1
  数组：[1, None, None]
        ↑    ↑
      front rear

步骤2: insertFront(2)
  要在 front=0 之前插入 2
  front 前移到 2（循环）
  在 front=2 插入 2
  结果：front=2, rear=1
  数组：[1, None, 2]
             ↑    ↑
           rear  front
  注意：front 前移了！

步骤3: insertFront(3)
  要在 front=2 之前插入 3
  front 前移到 1
  在 front=1 插入 3
  结果：front=1, rear=1
  数组：[1, 3, 2]
             ↑
        front=rear
  注意：front 又前移了！

步骤4: deleteFront()
  删除 front=1 位置的元素（3）
  front 后移到 2
  结果：front=2, rear=1
  数组：[1, None, 2]
             ↑    ↑
           rear  front
  注意：front 后移了！

总结：
  - insertFront：front 前移（向左）
  - deleteFront：front 后移（向右）
  - 单端队列只有 deleteFront，所以 front 只后移
""")

print("\n" + "=" * 70)
print("5. 为什么单端队列不能在 front 端插入？")
print("=" * 70)

print("""
单端队列的设计目的：
  - 实现 FIFO（先进先出）
  - 就像排队：新来的人从队尾加入，离开的人从队首离开
  
如果允许在 front 端插入：
  - 会破坏 FIFO 特性
  - 新插入的元素会"插队"，不符合队列的定义
  
双端队列的设计目的：
  - 允许在两端操作
  - 可以模拟栈（LIFO）或队列（FIFO）
  - 更灵活，但失去了严格的 FIFO 特性
""")

print("\n" + "=" * 70)
print("6. 总结")
print("=" * 70)

print("""
【单端队列】
  - front 端：只能删除（dequeue）
  - front 移动：只后移（向右）
  - 原因：删除后需要指向下一个有效元素

【双端队列】
  - front 端：可以插入（insertFront）和删除（deleteFront）
  - front 移动：前移（insertFront）或后移（deleteFront）
  - 原因：
    * insertFront：要在 front 之前插入，所以前移
    * deleteFront：删除后需要指向下一个有效元素，所以后移

【核心区别】
  单端队列的 front 只能删除 → 只后移
  双端队列的 front 可以插入 → 需要前移（插入时）
""")


































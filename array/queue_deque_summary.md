# 单端队列 vs 双端队列 - 指针移动规律总结

## 核心原则

**front 和 rear 永远维护的是有元素的位置：**
- `front`: 指向第一个有效元素的索引
- `rear`: 指向最后一个有效元素的下一个位置索引（左闭右开区间）

无论怎么移动，只需要让 front 和 rear 指针指向正确位置就好！

---

## 单端队列（Queue）

### 操作限制
- **front 端**：只能删除（dequeue），不能插入
- **rear 端**：只能插入（enqueue），不能删除

### 指针移动规律

| 指针 | 操作 | 移动方向 | 原因 |
|------|------|---------|------|
| **front** | dequeue（删除） | **只后移** | 删除后需要指向下一个有效元素 |
| **rear** | enqueue（插入） | **只后移** | 插入后需要指向下一个插入位置 |

### 可视化

```
初始：front=0, rear=0
数组：[None, None, None]
      ↑
   front=rear=0

enqueue(1): rear 后移
数组：[1, None, None]
      ↑    ↑
   front rear

enqueue(2): rear 后移
数组：[1, 2, None]
      ↑       ↑
   front    rear

dequeue(): front 后移
数组：[None, 2, None]
             ↑    ↑
           front rear
```

---

## 双端队列（Deque）

### 操作能力
- **front 端**：可以插入（insertFront）和删除（deleteFront）
- **rear 端**：可以插入（insertLast）和删除（deleteLast）

### 指针移动规律

| 指针 | 操作 | 移动方向 | 原因 |
|------|------|---------|------|
| **front** | insertFront（插入） | **前移** | 要在 front 之前插入，所以前移 |
| **front** | deleteFront（删除） | **后移** | 删除后需要指向下一个有效元素 |
| **rear** | insertLast（插入） | **后移** | 插入后需要指向下一个插入位置 |
| **rear** | deleteLast（删除） | **前移** | 删除后需要指向最后一个有效元素的下一个位置 |

### 可视化

```
初始：front=0, rear=0
数组：[None, None, None]
      ↑
   front=rear=0

insertLast(1): rear 后移
数组：[1, None, None]
      ↑    ↑
   front rear

insertFront(2): front 前移
数组：[1, None, 2]
             ↑    ↑
           rear  front

insertFront(3): front 前移
数组：[1, 3, 2]
             ↑
        front=rear

deleteFront(): front 后移
数组：[1, None, 2]
             ↑    ↑
           rear  front

deleteLast(): rear 前移
数组：[1, None, None]
      ↑
   front=rear=0
```

---

## 关键理解

### 1. 指针含义（永远不变）

无论单端还是双端队列，指针的含义都是一样的：
- **front**: 指向第一个有效元素的索引
- **rear**: 指向最后一个有效元素的下一个位置索引（左闭右开）

### 2. 移动方向取决于操作

- **插入操作**：
  - front 端插入 → front 前移（要在前面插入）
  - rear 端插入 → rear 后移（在后面插入）

- **删除操作**：
  - front 端删除 → front 后移（删除后指向下一个）
  - rear 端删除 → rear 前移（删除后指向最后一个的下一个）

### 3. 单端 vs 双端的区别

| 特性 | 单端队列 | 双端队列 |
|------|---------|---------|
| front 端插入 | ❌ 不允许 | ✅ 允许（前移） |
| front 端删除 | ✅ 允许（后移） | ✅ 允许（后移） |
| rear 端插入 | ✅ 允许（后移） | ✅ 允许（后移） |
| rear 端删除 | ❌ 不允许 | ✅ 允许（前移） |

---

## 记忆口诀

### 单端队列
```
front: 只能删 → 只后移
rear:  只能插 → 只后移
```

### 双端队列
```
front: 插前移，删后移
rear:  插后移，删前移
```

---

## 实现要点

1. **保持指针含义一致**：无论怎么操作，front 和 rear 的含义不变
2. **根据操作调整指针**：插入/删除时，移动指针到正确位置
3. **使用 mod 运算**：处理循环数组的边界情况
4. **维护 size**：确保 isEmpty 和 isFull 判断正确

---

## 总结

✅ **核心原则**：front 和 rear 永远维护的是有元素的位置

✅ **单端队列**：
- front 只能删除 → 只后移
- rear 只能插入 → 只后移

✅ **双端队列**：
- front → 插入时前移，删除时后移
- rear → 插入时后移，删除时前移

✅ **关键**：无论怎么移动，只需要让 front 和 rear 指针指向正确位置就好！


































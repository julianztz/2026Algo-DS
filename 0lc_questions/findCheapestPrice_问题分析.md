# Find Cheapest Price 问题分析

## 问题描述
在 Dijkstra 基础上添加 stops 限制（最多 k 个中间节点），但添加 stop 判断后无法计算可到达的节点。

## 🔴 当前代码的问题

### 问题1：stop 变量的含义完全错误

**当前代码（第106-109行）：**
```python
stop = 0
for neighbor, weight in graph.get(node, []):
    stop += 1
    if total_dist + weight < distTo[neighbor] and stop <= k:
```

**问题分析：**
- `stop = 0` 在每次从队列取出节点时都会重置为 0
- `stop += 1` 只是在遍历当前节点的**邻居索引**，不是路径上的 stops 数
- 例如：如果节点 A 有 5 个邻居，遍历到第 3 个邻居时 `stop = 3`，但这**不是**从 src 到 A 经过的 stops 数

**举例说明：**
```
图：0 -> 1 -> 2 -> 3
从节点 0 开始，k = 1

当处理节点 0 时：
- stop = 0（重置）
- 遍历到邻居 1：stop = 1，满足 stop <= 1，可以访问
- 遍历到邻居 2：stop = 2，不满足 stop <= 1，被跳过 ❌

但实际上：
- 0 -> 1 是 0 个 stops（直接到达）
- 0 -> 1 -> 2 是 1 个 stop（经过节点 1）
```

### 问题2：visited 集合的使用错误

**当前代码（第102-104行）：**
```python
if node in visited: continue
visited.add(node)
```

**问题分析：**
- 在带 stops 限制的 Dijkstra 中，**同一个节点可能需要在不同的 stops 数下被访问多次**
- 例如：到达节点 3 可能有两条路径：
  - 路径1：0 -> 1 -> 3（1 stop，cost=700）
  - 路径2：0 -> 1 -> 2 -> 3（2 stops，cost=400）
  
  如果 k=2，两条路径都应该考虑，但 visited 集合会阻止路径2的探索

**正确理解：**
- 在标准 Dijkstra 中，一旦找到到某个节点的最短路径，就不需要再访问它
- 但在带 stops 限制的 Dijkstra 中，**同一个节点在不同 stops 数下可能有不同的最优解**

### 问题3：distTo 只记录一个值，无法处理多维度状态

**当前代码（第83-84行）：**
```python
distTo = {dist+1: float('inf') for dist in range(n)}
distTo[src] = 0
```

**问题分析：**
- `distTo[node]` 只记录到达 node 的最小 cost
- 但没有记录是在**多少个 stops** 下达到的这个 cost
- 这导致无法正确判断：即使 cost 更大，但如果 stops 更少，也可能是有效路径

## ✅ 正确的解决方案

### 核心思想
在带 stops 限制的 Dijkstra 中，**状态是二维的**：(node, stops)

### 方法1：修改优先队列存储三元组

**关键改变：**
1. 优先队列存储 `(cost, node, stops)` 三元组
2. 不能用简单的 `visited` 集合，改用 `(node, stops)` 作为访问标记
3. 或者用 `distTo[node][stops]` 记录不同 stops 下的最小 cost

**伪代码：**
```python
def findCheapestPrice(n, flights, src, dst, k):
    # 构建图
    graph = build_graph(flights)
    
    # 优先队列：(cost, node, stops)
    pq = [(0, src, 0)]  # 从 src 开始，0 cost，0 stops
    
    # 记录到达每个节点的最小 cost（在不同 stops 下）
    # 方式1：用字典记录 (node, stops) -> min_cost
    min_cost = {}  # {(node, stops): min_cost}
    
    # 方式2：用二维数组 distTo[node][stops] = min_cost
    # 但 stops 最多 k+1 个（0 到 k）
    
    while pq:
        cost, node, stops = heapq.heappop(pq)
        
        # 如果到达目标节点，返回（因为优先队列保证这是最短路径）
        if node == dst:
            return cost
        
        # 如果 stops 已经达到上限，不能再继续
        if stops > k:
            continue
        
        # 检查是否已经访问过这个状态
        # 方式1：用 (node, stops) 作为 key
        if (node, stops) in min_cost and cost >= min_cost[(node, stops)]:
            continue
        
        min_cost[(node, stops)] = cost
        
        # 遍历邻居
        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            new_stops = stops + 1  # 经过当前 node 到达 neighbor，stops + 1
            
            # 如果新路径更优（cost 更小）且 stops <= k
            if new_stops <= k + 1:  # k+1 因为 stops 是从 0 开始计数的
                # 检查是否已经有更优的路径到达 neighbor
                if (neighbor, new_stops) not in min_cost or new_cost < min_cost[(neighbor, new_stops)]:
                    heapq.heappush(pq, (new_cost, neighbor, new_stops))
    
    return -1
```

### 方法2：使用 Bellman-Ford 思想（更简单）

**关键思想：**
- 进行 k+1 轮松弛（因为最多 k 个 stops = k+1 条边）
- 每轮更新所有可达节点的最小 cost

**伪代码：**
```python
def findCheapestPrice(n, flights, src, dst, k):
    # dist[i] 表示经过 i 轮松弛后到达各节点的最小 cost
    dist = [float('inf')] * n
    dist[src] = 0
    
    # 进行 k+1 轮松弛（k 个 stops = k+1 条边）
    for _ in range(k + 1):
        # 保存上一轮的结果，避免同轮内相互影响
        new_dist = dist.copy()
        
        for u, v, w in flights:
            if dist[u] != float('inf'):
                new_dist[v] = min(new_dist[v], dist[u] + w)
        
        dist = new_dist
    
    return dist[dst] if dist[dst] != float('inf') else -1
```

## 📊 两种方法对比

| 维度 | 方法1：改进的 Dijkstra | 方法2：Bellman-Ford |
|------|----------------------|-------------------|
| **时间复杂度** | O(E * k * log V) | O(E * k) |
| **空间复杂度** | O(V * k) | O(V) |
| **实现复杂度** | 较复杂 | 简单 |
| **适用场景** | 需要精确控制 stops | 简单直接 |

## 🎯 推荐实现

对于这个问题，**方法2（Bellman-Ford）更简单直接**，因为：
1. 代码更简洁
2. 不需要处理复杂的 visited 逻辑
3. 时间复杂度虽然稍高，但对于 k 较小的情况完全可以接受

## 🔍 为什么当前代码无法计算可到达的节点？

**根本原因：**
1. `stop` 变量只是邻居索引，不是路径上的 stops 数
2. `stop <= k` 的判断会错误地阻止很多有效路径
3. `visited` 集合会阻止同一节点在不同 stops 下的访问

**具体例子：**
```
图：0 -> 1 -> 2 -> 3
k = 1

当前代码执行过程：
1. 队列：[(0, 0)]
2. 取出 (0, 0)，visited.add(0)
3. 遍历节点 0 的邻居：
   - 邻居 1：stop = 1，满足 stop <= 1，加入队列 [(100, 1)]
4. 取出 (100, 1)，visited.add(1)
5. 遍历节点 1 的邻居：
   - 邻居 2：stop = 1，满足 stop <= 1，加入队列 [(200, 2)]
   - 邻居 3：stop = 2，不满足 stop <= 1，被跳过 ❌
6. 取出 (200, 2)，visited.add(2)
7. 遍历节点 2 的邻居：
   - 但此时 stop 又从 0 开始计数，逻辑混乱

问题：节点 3 永远无法通过 0->1->3 这条路径到达（如果存在的话）
```









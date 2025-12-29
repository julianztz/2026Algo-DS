# Network Delay Time 问题思路分析

## 问题回顾
- 给定有向加权图（通过 `times` 列表表示边）
- 从节点 `k` 发送信号
- 返回**所有节点收到信号的最短时间**（即从 k 到所有节点的最短路径中的最大值）
- 如果有节点不可达，返回 -1

---

## 思路1：DFS 递归找所有解，记录最长路径

### ❌ 主要问题

1. **概念错误：DFS 不能保证找到最短路径**
   - DFS 会遍历所有可能的路径，包括非最短路径
   - 题目要求的是"最短路径"中的最大值，不是"所有路径"中的最大值
   - 例如：从 k 到节点 v 可能有路径 A(长度10) 和路径 B(长度5)，DFS 可能先找到 A，但实际最短路径是 B

2. **时间复杂度极高**
   - 需要探索所有可能的路径组合
   - 最坏情况 O(2^E) 或更高（E 是边数）
   - 对于有环的图，需要额外的环检测机制

3. **需要额外的剪枝和回溯**
   - 必须记录当前路径长度，如果发现更短路径才更新
   - 实际上这就是在实现一个低效的 Dijkstra/Bellman-Ford

4. **边界情况复杂**
   - 需要处理环（避免无限递归）
   - 需要处理多个路径到同一节点的情况

### ✅ 如果坚持用 DFS，需要这样改进：

**改进思路：DFS + 记忆化（类似动态规划）**
- 用 `dist[node]` 记录从 k 到 node 的**最短距离**
- 遍历时，如果当前路径长度 >= `dist[node]`，则剪枝（因为不是更优解）
- 这样实际上是在用 DFS 实现 Bellman-Ford 的思想

### 伪代码流程（改进版 DFS）

```
function networkDelayTime(times, n, k):
    # 1. 构建邻接表
    graph = buildGraph(times)  # {node: [(neighbor, weight), ...]}
    
    # 2. 初始化距离数组
    dist = [inf] * (n + 1)  # 节点编号从1到n
    dist[k] = 0
    
    # 3. DFS 递归函数（带记忆化）
    function dfs(node, currentDist):
        # 剪枝：如果当前路径不是更优的，直接返回
        if currentDist >= dist[node]:
            return
        
        # 更新最短距离
        dist[node] = currentDist
        
        # 遍历所有邻居
        for (neighbor, weight) in graph[node]:
            newDist = currentDist + weight
            # 递归探索（即使 neighbor 已访问过，如果路径更短也要更新）
            dfs(neighbor, newDist)
    
    # 4. 从 k 开始 DFS
    dfs(k, 0)
    
    # 5. 检查结果
    maxDist = max(dist[1:])  # 跳过索引0，节点从1开始
    
    if maxDist == inf:
        return -1  # 有节点不可达
    else:
        return maxDist
```

**时间复杂度：** O(V * E) - 最坏情况下每条边都会被重新访问多次
**空间复杂度：** O(V + E) - 递归栈 + 图存储

---

## 思路2：BFS + Dijkstra（推荐 ✅）

### ✅ 优点

1. **正确性保证**
   - Dijkstra 算法专门用于解决单源最短路径问题
   - 保证找到从 k 到所有节点的最短路径

2. **时间复杂度优秀**
   - O(E log V) - 使用优先队列
   - 比 DFS 方法高效得多

3. **实现简单**
   - 直接复用已有的 Dijkstra 实现
   - 只需要从 `times` 列表构建图，然后调用 Dijkstra

4. **边界情况处理清晰**
   - 不可达节点自然返回 inf，容易判断

### ⚠️ 需要注意的点

1. **节点编号从 1 开始**
   - LeetCode 题目中节点编号是 1 到 n
   - 构建图时要注意索引

2. **检查所有节点是否可达**
   - 遍历 distTo 字典，检查是否有 inf 值
   - 或者检查 distTo 中是否包含所有 1 到 n 的节点

### 伪代码流程（Dijkstra 方法）

```
function networkDelayTime(times, n, k):
    # 1. 从 times 列表构建邻接表
    graph = {}
    for (u, v, w) in times:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    
    # 注意：可能有些节点没有出边，需要初始化所有节点
    # 或者让 Dijkstra 函数处理缺失节点的情况
    
    # 2. 调用 Dijkstra 算法
    distTo = dijkstra(graph, k)
    
    # 3. 检查所有节点是否可达，并找最大距离
    maxDist = 0
    for node in range(1, n + 1):  # 节点编号 1 到 n
        if node not in distTo or distTo[node] == inf:
            return -1  # 有节点不可达
        maxDist = max(maxDist, distTo[node])
    
    return maxDist

# Dijkstra 函数（复用已有实现）
function dijkstra(graph, src):
    distTo = {}
    # 初始化：所有在 graph 中的节点距离为 inf
    for node in graph:
        distTo[node] = inf
    distTo[src] = 0
    
    pq = [(0, src)]  # 优先队列：(距离, 节点)
    visited = set()
    
    while pq:
        dist, node = heapq.heappop(pq)
        
        if node in visited:
            continue
        
        visited.add(node)
        
        # 遍历邻居
        for neighbor, weight in graph.get(node, []):
            if dist + weight < distTo.get(neighbor, inf):
                distTo[neighbor] = dist + weight
                heapq.heappush(pq, (distTo[neighbor], neighbor))
    
    return distTo
```

**时间复杂度：** O(E log V)
**空间复杂度：** O(V + E)

---

## 两种方法对比总结

| 维度 | DFS 方法 | Dijkstra 方法 |
|------|----------|---------------|
| **正确性** | ⚠️ 需要改进（加记忆化） | ✅ 保证正确 |
| **时间复杂度** | O(V * E) | O(E log V) |
| **实现复杂度** | 较复杂（需要剪枝） | 简单（直接复用） |
| **适用场景** | 不推荐 | ✅ 推荐 |

---

## 推荐实现顺序

1. **先实现思路2（Dijkstra）** - 简单、正确、高效
2. **再实现思路1（改进版DFS）** - 作为学习理解，但不推荐用于实际解题

---

## 关键实现细节

### 从 times 构建图的函数

```python
def build_graph(times: List[List[int]]) -> Dict[int, List[Tuple[int, int]]]:
    """
    将 times 列表转换为邻接表
    
    times[i] = [ui, vi, wi] 表示从 ui 到 vi 的边，权重为 wi
    返回: {节点: [(邻居, 权重), ...]}
    """
    graph = {}
    for u, v, w in times:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    return graph
```

### 检查所有节点可达性

```python
# 方法1：检查 distTo 中是否包含所有节点
all_nodes_reachable = all(
    node in distTo and distTo[node] != float('inf') 
    for node in range(1, n + 1)
)

# 方法2：直接找最大值，如果有 inf 说明不可达
max_dist = max(distTo.get(node, float('inf')) for node in range(1, n + 1))
if max_dist == float('inf'):
    return -1
```


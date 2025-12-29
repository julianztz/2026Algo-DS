"""
图最短路径问题 - 快速参考模板

包含：
1. BFS 模板（无权图）
2. Dijkstra 模板（有权图）
3. 带 Stops 限制的 Dijkstra
4. 辅助函数
"""

from collections import deque
import heapq
from typing import List, Dict, Tuple


# ==================== 辅助函数 ====================

def build_graph(edges: List[List[int]]) -> Dict[int, List[Tuple[int, int]]]:
    """
    将边列表转换为邻接表
    
    输入: [[u, v, w], ...] 或 [[u, v], ...]（无权图时 w=1）
    输出: {u: [(v, w), ...]}
    """
    graph = {}
    for edge in edges:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) > 2 else 1  # 默认权重为 1
        
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    
    return graph


# ==================== BFS 模板 ====================

def bfs_shortest_path(graph: Dict[int, List[int]], start: int, target: int) -> int:
    """
    BFS 找无权图中的最短路径（步数）
    
    适用场景：
    - 无权图（所有边权重相等）
    - 求最短步数/层数
    """
    queue = deque([start])
    visited = set([start])
    distance = {start: 0}
    
    while queue:
        node = queue.popleft()
        
        if node == target:
            return distance[node]
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    
    return -1


def bfs_with_levels(graph: Dict[int, List[int]], start: int, target: int) -> int:
    """
    BFS 按层遍历找最短路径
    
    适用场景：需要知道当前在第几层
    """
    queue = deque([start])
    visited = set([start])
    level = 0
    
    while queue:
        size = len(queue)
        
        for _ in range(size):
            node = queue.popleft()
            
            if node == target:
                return level
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        level += 1
    
    return -1


# ==================== Dijkstra 模板 ====================

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], src: int) -> Dict[int, int]:
    """
    Dijkstra 算法：单源最短路径
    
    适用场景：
    - 有权图
    - 无负权重边
    - 求最短路径权重和
    
    返回: {node: min_distance}
    """
    # 初始化
    distTo = {node: float('inf') for node in graph}
    distTo[src] = 0
    
    # 优先队列：(距离, 节点)
    pq = [(0, src)]
    visited = set()
    
    while pq:
        dist, node = heapq.heappop(pq)
        
        # 跳过已访问的节点
        if node in visited:
            continue
        
        visited.add(node)
        
        # 松弛操作
        for neighbor, weight in graph.get(node, []):
            if dist + weight < distTo[neighbor]:
                distTo[neighbor] = dist + weight
                heapq.heappush(pq, (distTo[neighbor], neighbor))
    
    return distTo


def dijkstra_to_target(graph: Dict[int, List[Tuple[int, int]]], src: int, dst: int) -> int:
    """
    Dijkstra 算法：从 src 到 dst 的最短距离（提前返回优化）
    """
    distTo = {node: float('inf') for node in graph}
    distTo[src] = 0
    
    pq = [(0, src)]
    visited = set()
    
    while pq:
        dist, node = heapq.heappop(pq)
        
        # 到达目标节点，提前返回
        if node == dst:
            return dist
        
        if node in visited:
            continue
        
        visited.add(node)
        
        for neighbor, weight in graph.get(node, []):
            if dist + weight < distTo[neighbor]:
                distTo[neighbor] = dist + weight
                heapq.heappush(pq, (distTo[neighbor], neighbor))
    
    return -1


# ==================== 带限制的 Dijkstra ====================

def dijkstra_with_stops(n: int, edges: List[List[int]], src: int, dst: int, k: int) -> int:
    """
    带 stops 限制的 Dijkstra
    
    适用场景：
    - 有权图
    - 最多 k 个中间节点（stops）
    
    关键点：
    1. 状态是二维的：(node, stops)
    2. 不能用简单的 visited 集合
    3. 同一个节点可能需要在不同 stops 下被访问多次
    """
    # 构建图
    graph = build_graph(edges)
    
    # 优先队列：(cost, node, stops)
    pq = [(0, src, 0)]
    
    # 记录每个 (node, stops) 状态的最小 cost
    min_cost = {}  # {(node, stops): min_cost}
    
    while pq:
        cost, node, stops = heapq.heappop(pq)
        
        # 到达目标节点，直接返回
        if node == dst:
            return cost
        
        # 超过 stops 限制，跳过
        if stops > k:
            continue
        
        # 检查是否已访问过这个状态
        if (node, stops) in min_cost and cost >= min_cost[(node, stops)]:
            continue
        
        min_cost[(node, stops)] = cost
        
        # 遍历邻居
        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            new_stops = stops + 1  # 经过当前 node 到达 neighbor
            
            # 如果新路径的 stops 在限制内
            if new_stops <= k + 1:
                if (neighbor, new_stops) not in min_cost or new_cost < min_cost[(neighbor, new_stops)]:
                    heapq.heappush(pq, (new_cost, neighbor, new_stops))
    
    return -1


# ==================== 使用示例 ====================

if __name__ == '__main__':
    # 示例1：BFS（无权图）
    print("=== BFS 示例 ===")
    graph_bfs = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2]
    }
    result = bfs_shortest_path(graph_bfs, 0, 3)
    print(f"从节点 0 到节点 3 的最短步数: {result}")  # 输出: 2
    
    # 示例2：Dijkstra（有权图）
    print("\n=== Dijkstra 示例 ===")
    edges = [[0, 1, 4], [0, 3, 2], [1, 2, 1], [2, 5, 5], [3, 4, 3], [5, 4, 1]]
    graph_dijkstra = build_graph(edges)
    distances = dijkstra(graph_dijkstra, 0)
    print(f"从节点 0 到各节点的最短距离: {distances}")
    
    # 示例3：带 stops 限制的 Dijkstra
    print("\n=== 带 Stops 限制的 Dijkstra 示例 ===")
    flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
    result = dijkstra_with_stops(4, flights, 0, 3, 1)
    print(f"从节点 0 到节点 3，最多 1 个 stop 的最便宜价格: {result}")  # 输出: 700









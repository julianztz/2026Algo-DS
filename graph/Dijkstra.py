'''
Dijkstra （BFS改良版）只能处理不包含负权重边的图
本质是标准 BFS 算法 + 贪心思想

Dijkstra 算法和标准的 BFS 算法的区别：
1、标准 BFS 算法使用普通队列，Dijkstra 算法使用优先级队列，
    让距离起点更近的节点优先出队（贪心思想的体现）。
2、标准 BFS 算法使用一个 visited 数组记录访问过的节点，确保算法不会陷入死循环；
    Dijkstra 算法使用一个 distTo 数组，同时记录起点到其他节点的最短路径。
'''

import heapq
from typing import List, Dict, Tuple
from collections import defaultdict

class State:

    def __init__(self, node, distFromStart) -> None:
        self.node = node
        self.distFromStart = distFromStart

    # less than -- 小顶堆比较函数
    def __lt__(self, other:'State') -> bool:
        return self.distFromStart < other.distFromStart


def dijkstra(graph: Dict[int, List[Tuple[int, int]]], src: int) -> Dict[int, int]:
    """
    Dijkstra算法：计算从源节点src到所有其他节点的最短距离
    
    参数:
        graph: 邻接表表示的图
            - key: 节点编号
            - value: [(邻居节点, 权重), ...] 的列表
        src: 源节点编号
    
    返回:
        distTo: 字典，key为节点，value为从src到该节点的最短距离
    """
    # 初始化距离数组，所有节点距离为无穷大
    distTo = {node: float('inf') for node in graph}
    distTo[src] = 0  # 源节点到自己的距离为0
    
    # 优先级队列：(距离, 节点)
    pq = [(0, src)]
    visited = set()
    
    while pq:
        # 取出距离最小的节点
        dist, node = heapq.heappop(pq)
        
        # 如果已经访问过，跳过（因为可能有重复节点在队列中）
        if node in visited:
            continue
        
        visited.add(node)
        
        # 遍历当前节点的所有邻居
        for neighbor, weight in graph.get(node, []):
            # 如果找到更短的路径
            if dist + weight < distTo[neighbor]:
                distTo[neighbor] = dist + weight
                heapq.heappush(pq, (distTo[neighbor], neighbor))
    
    return distTo


# ========== 方式1：使用字典（邻接表）表示图 - 推荐 ==========
# 不需要实现Graph类，直接用字典即可
def create_graph_example() -> Dict[int, List[Tuple[int, int]]]:
    """
    创建示例图：
        0 --(4)--> 1 --(1)--> 2
        |                    |
        (2)                  (5)
        |                    |
        v                    v
        3 --(3)--> 4 <--(1)-- 5
    """
    graph = {
        0: [(1, 4), (3, 2)],
        1: [(2, 1)],
        2: [(5, 5)],
        3: [(4, 3)],
        4: [],                     #[(5,1)],
        5: [(4, 1)]
    }
    return graph


# ========== 方式2：使用networkx库（可选） ==========
# 需要先安装: pip install networkx
def dijkstra_with_networkx():
    """
    如果使用networkx库，可以这样实现：
    
    import networkx as nx
    
    # 创建图
    G = nx.DiGraph()  # 有向图
    G.add_weighted_edges_from([
        (0, 1, 4), (0, 3, 2),
        (1, 2, 1),
        (2, 5, 5),
        (3, 4, 3),
        (5, 4, 1)
    ])
    
    # 直接使用networkx的Dijkstra算法
    distances = nx.single_source_dijkstra_path_length(G, source=0)
    print(distances)  # {0: 0, 1: 4, 3: 2, 2: 5, 4: 5, 5: 10}
    """
    pass






# ========== 测试示例 ==========
if __name__ == "__main__":
    # 创建图
    graph = create_graph_example()
    
    # 计算从节点0到所有其他节点的最短距离
    src = 0
    distances = dijkstra(graph, src)
    
    print(f"从节点 {src} 到其他节点的最短距离：")
    for node, dist in sorted(distances.items()):
        if dist == float('inf'):
            print(f"  节点 {node}: 不可达")
        else:
            print(f"  节点 {node}: {dist}")
    
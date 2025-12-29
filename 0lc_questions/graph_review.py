from typing import List
import heapq

# $$$$$$ review $$$$$$ lc 743 Network Delay time
'''
You are given a network of n nodes, labeled from 1 to n. 
You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), 
where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal.
If it is impossible for all the n nodes to receive the signal, return -1.

1 <= k <= n <= 100
1 <= times.length <= 6000
times[i].length == 3
1 <= ui, vi <= n
ui != vi
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2

思路1：Dijkstra -- BFS + Greedy

'''

def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:

    # distTo: 字典，key为 to_node，value为从 k节点 到该节点的最短距离
    # to_node : dist
    distTo = {dist+1: float('inf') for dist in range(n)}
    distTo[k] = 0

    # priority Q
    pq  = [(0, k)]
    visited = set()

    # 构建邻接表 Graph
    graph = {}
    for u, v, w in times:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))


    while pq:
        # 小顶堆top -- 最小dist 节点
        (total_dist, node) = heapq.heappop(pq)
        
        if node in visited: continue

        visited.add(node)

        # 直接读取邻接表graph中node所有的相邻node
        for neighbor, weight in graph.get(node, []):
            # 如果找到更短的路径
            if total_dist + weight < distTo[neighbor]:
                distTo[neighbor] = total_dist + weight
                heapq.heappush(pq, (distTo[neighbor], neighbor))


    for node in range(1, n + 1):
        if distTo.get(node, float('inf')) == float('inf'):
            return -1
    return max(distTo.values())


# $$$$$$ review $$$$$$ lc787 Cheapest Flights Within K Stops
'''
There are n cities connected by some number of flights. 
You are given an array flights where flights[i] = [fromi, toi, pricei] 
indicates that there is a flight from city fromi to city toi with cost pricei.

You are also given three integers src, dst, and k, 
return the cheapest price from src to dst with at most k stops. 
If there is no such route, return -1.

思路： Dijkstra
restriction k -- maximum # of stop allowed
'''
def findCheapestPrice(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    
    # 构建邻接表 Graph
    graph = {}
    for u, v, w in flights:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))

    # 优先队列：(cost, node, stops)
    # stops 表示从 src 到当前节点经过的中间节点数
    pq = [(0, src, 0)]  # 从 src 开始，0 cost，0 stops
    
    # 记录到达每个 (node, stops) 状态的最小 cost
    min_cost = {}  # {(node, stops): min_cost}

    while pq:
        # 小顶堆top -- 最小距离node
        cost, node, stops = heapq.heappop(pq)
        
        # 如果到达目标节点，直接返回（优先队列保证这是最短路径）
        if node == dst:
            return cost
        
        # 如果 stops 已经超过限制，跳过
        if stops > k:
            continue
        
        # 检查是否已访问过这个 (node, stops) 状态
        # 如果已有更优的路径到达这个状态，跳过
        if (node, stops) in min_cost and cost >= min_cost[(node, stops)]:
            continue
        
        # 记录当前状态的最小 cost
        min_cost[(node, stops)] = cost

        # 遍历当前节点的所有邻居
        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            new_stops = stops + 1  # 经过当前 node 到达 neighbor，stops + 1

            # 如果新路径的 stops 在限制内
            if new_stops <= k + 1:
                # 检查是否已经有更优的路径到达 (neighbor, new_stops)
                if (neighbor, new_stops) not in min_cost or new_cost < min_cost[(neighbor, new_stops)]:
                    heapq.heappush(pq, (new_cost, neighbor, new_stops))
    
    # 如果无法到达目标节点，返回 -1
    return -1


if __name__ == '__main__':
    flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
    findCheapestPrice(4, flights, 0, 3, 1)
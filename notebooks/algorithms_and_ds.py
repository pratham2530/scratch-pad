"""
Implementations of binary trees, shortest path algorithms (dijkstra, bellman-ford),
network flow algorithm (ford-fulkerson), and fenwick trees. 
"""

from collections import deque
import heapq


class Node:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


# --- Binary Tree ---


class BinaryTree:
    def __init__(self):
        self.root = None

    def add_node(self, val):
        new_node = Node(val)
        
        if not self.root:
            self.root = new_node
            return

        curr = self.root

        while True:
            if val < curr.val:
                if not curr.left:
                    curr.left = new_node
                    break

                curr = curr.left

            else:
                if not curr.right:
                    curr.right = new_node
                    break

                curr = curr.right


# --- Dijkstra's and Bellman-Ford algorithms ---


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, node_from, node_to, weight):
        if node_from not in self.adjacency_list:
            self.adjacency_list[node_from] = []

        self.adjacency_list[node_from].append((node_to, weight))

    def distances(self, source):
        all_nodes = set(self.adjacency_list.keys())

        # add leaf nodes 
        for neighbours in self.adjacency_list.values():
            for neighbour, _ in neighbours:
                all_nodes.add(neighbour)

        distances = {node: float("inf") for node in all_nodes}  # not reached other nodes
        distances[source] = 0  # start from source node

        return distances

    def dijkstra_queue(self, source):
        distances = self.distances(source)
        queue = deque([source])  # store visited nodes

        while queue:
            curr_node = queue.popleft()

            # if curr_node is a leaf node return []
            for neighbour, weight in self.adjacency_list.get(curr_node, []):
                new_distance = distances[curr_node] + weight

                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    queue.append(neighbour)

        return distances

    def dijkstra_min_heap(self, source):
        distances = self.distances(source)
        min_heap = [(0, source)]

        while min_heap:
            curr_distance, curr_node = heapq.heappop(min_heap)

            # if a longer path is found to the node already visited skip it
            if curr_distance > distances[curr_node]:
                continue

            for neighbour, weight in self.adjacency_list.get(curr_node, []):
                new_distance = distances[curr_node] + weight

                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    heapq.heappush(min_heap, (new_distance, neighbour))

        return distances

    def bellman_ford(self, source):
        distances = self.distances(source)
        num_vertices = len(distances)

        # worst-case scenario is a singular path
        for _ in range(num_vertices - 1):
            for node, neighbours in self.adjacency_list.items():
                for neighbour, weight in neighbours:
                    if distances[node] + weight < distances[neighbour]:
                        distances[neighbour] = distances[node] + weight

        # run the loop twice to find negative cycles
        for _ in range(num_vertices - 1):
            for node, neighbours in self.adjacency_list.items():
                for neighbour, weight in neighbours:
                    if distances[node] + weight < distances[neighbour]:
                        print(f"The graph contains a negative weight cycle containing {node}.")
                        return None
        return distances


# --- Ford-Fulkerson algorithm ---


class MaxFlowGraph:
    def __init__(self):
        self.residual_graph = {}

    def add_edge(self, from_node, to_node, capacity):
        if from_node not in self.residual_graph:
            self.residual_graph[from_node] = {}

        if to_node not in self.residual_graph:
            self.residual_graph[to_node] = {}

        self.residual_graph[from_node][to_node] = capacity

        # initialise reverse edges with zero capacity
        if from_node not in self.residual_graph[to_node]:
            self.residual_graph[to_node][from_node] = 0

    def bfs_augementing_path(self, source, sink, parent):
        queue = deque([source])
        visited = set()
        visited.add(source)

        while queue:
            curr_node = queue.popleft()

            for neighbour, resid_capacity in self.residual_graph.get(curr_node, {}).items():
                if neighbour not in visited and resid_capacity > 0:
                    parent[neighbour] = curr_node

                    if neighbour == sink:
                        return True

                    visited.add(neighbour)
                    queue.append(neighbour)

        return False

    def ford_fulkerson(self, source, sink):
        max_flow = 0

        # track path from bfs
        parent = {}

        while self.bfs_augementing_path(source, sink, parent):
            bottleneck = float("inf")
            curr_node = sink

            while curr_node != source:
                prev_node = parent[curr_node]

                # find minimum available capacity from sink to source
                bottleneck = min(bottleneck, self.residual_graph[prev_node][curr_node])
                curr_node = prev_node

            curr_node = sink

            while curr_node != source:
                prev_node = parent[curr_node]
                self.residual_graph[prev_node][curr_node] -= bottleneck 
                self.residual_graph[curr_node][prev_node] += bottleneck 
                curr_node = prev_node

            max_flow += bottleneck

            # reset for next iteration
            parent = {}

        return max_flow


# --- Fenwick Tree ---


class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, i: int, delta: int) -> None:
        while i < self.size:
            self.tree[i] += delta
            i += i & (-i) # jump to next index whose range contains i (see algorithms_and_ds_notes.md)

    def prefix_query(self, i: int) -> int:
        total_sum = 0
        while i > 0:
            total_sum += self.tree[i]
            i -= i & (-i) 

        return total_sum

    def range_query(self, left: int, right: int) -> int:
        return self.prefix_query(right) - self.prefix_query(left - 1)

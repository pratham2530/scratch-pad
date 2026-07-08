"""Module implementing mathematical programming algorithms and data structures.

This module provides implementations for various data structures and algorithms,
including Binary Trees, Graph Shortest Path algorithms (Dijkstra, Bellman-Ford),
Network Flow algorithms (Ford-Fulkerson), and Range Query structures (Fenwick Tree).
"""

from collections import deque
import heapq


class Node:
    """Represents a node in a binary tree structure."""

    def __init__(self, val=0):
        # Each parent node has a left child node, a right child node and a value.
        self.val = val
        self.left = None
        self.right = None


# --- Binary Tree ---


class BinaryTree:
    """A binary search tree data structure implementation."""

    def __init__(self):
        """A binary tree has one root (starting) node and each parent
        node has two child nodes where the value of the left (right)
        child node is smaller (greater) than or equal to the parent node (*).
        """

        self.root = None

    def add_node(self, val):
        """Traverse through the tree from the root node to the leaf
        node so that when the new node is added (*) still holds.
        """

        new_node = Node(val)

        # When the first node is added, self.root needs to be updated.
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


# --- Dijkstra's and Bellman-Ford Algorithms ---


class Graph:
    """Represents a directed graph structure supporting shortest path algorithms.

    Dijkstra's algorithm finds the shortest path between two vertices in a
    weighted graph where the weights are positive.

    The Bellman-Ford algorithm finds the shortest path between two vertices
    in a weighted graph where the weights can be negative.
    """

    def __init__(self):
        """We can represent the graph by an adjacency list:

        adjacency_list = {
            node1: [(node, weight2), (node3, weight3)],
            node4: [(node5, weight5)]
        }.
        """

        self.adjacency_list = {}

    def add_edge(self, node_from, node_to, weight):
        """Adds a directed weighted edge to the graph adjacency list."""
        if node_from not in self.adjacency_list:
            self.adjacency_list[node_from] = []

        self.adjacency_list[node_from].append((node_to, weight))

    def distances(self, source):
        """Calculates default infinite distances for all unique nodes in the graph."""
        # We first add the nodes which only have edges leading to them and not going to any node.
        all_nodes = set(self.adjacency_list.keys())
        for neighbours in self.adjacency_list.values():
            for neighbour, _ in neighbours:
                all_nodes.add(neighbour)

        distances = {
            node: float("inf") for node in all_nodes
        }  # We have not reached other nodes yet.
        distances[source] = 0  # We're starting from the source node.

        return distances

    def dijkstra_queue(self, source):
        """Computes shortest path distances using a standard double-ended queue.

        When we pop a node from the queue, we check the distance from the source node
        to each of the nodes neighbours via the current node is smaller than the recorded
        distance for each neighbour.

        The first time, the distances from the source node to its neighbours
        are infinite hence the distances of the neighbours are all updated.
        """
        distances = self.distances(source)

        queue = deque([source])  # This is the queue where we store the visited nodes.

        while queue:
            curr_node = queue.popleft()

            # If curr_node has no edges leading to other nodes return an empty list to skip over.
            for neighbour, weight in self.adjacency_list.get(curr_node, []):
                new_distance = distances[curr_node] + weight

                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    queue.append(neighbour)

        return distances

    def dijkstra_min_heap(self, source):
        """Computes shortest path distances using a priority queue (min-heap).

        In a min-heap, the element with the smallest distance is always popped first.
        Each element is a tuple (distance from source node, node).

        This is faster than implementing a queue since when a node is popped from the
        min-heap, the distance to the node known is the smallest. This is a greedy approach
        while in a queue the weights aren't checked.
        """
        distances = self.distances(source)

        min_heap = [(0, source)]

        while min_heap:
            curr_distance, curr_node = heapq.heappop(min_heap)

            # If a longer path is found to the node we already visited, skip it.
            if curr_distance > distances[curr_node]:
                continue

            for neighbour, weight in self.adjacency_list.get(curr_node, []):
                new_distance = distances[curr_node] + weight

                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    heapq.heappush(min_heap, (new_distance, neighbour))

        return distances

    def bellman_ford(self, source):
        """Computes shortest path distances and detects negative weight cycles.

        In the worst-case scenario, this graph: A -> B -> C -> ... -> Z is
        possible where each node has an edge to and from it. To reach Z from
        A we need to move 26 - 1 = 25 times.

        At each iteration, the distance of the node travelled is updated to
        by adding the new weight.
        """
        distances = self.distances(source)
        num_vertices = len(distances)

        for _ in range(num_vertices - 1):
            for node, neighbours in self.adjacency_list.items():
                for neighbour, weight in neighbours:
                    if distances[node] + weight < distances[neighbour]:
                        distances[neighbour] = distances[node] + weight

        # Run the loop twice to find negative cycles. If A, B and C are nodes
        # then A -> B -> C -> A is a negative cycle if the sum of the weights
        # is negative.

        for _ in range(num_vertices - 1):
            for node, neighbours in self.adjacency_list.items():
                for neighbour, weight in neighbours:
                    if distances[node] + weight < distances[neighbour]:
                        print(
                            f"The graph contains a negative weight cycle containing {node}."
                        )
                        return None
        return distances


# --- Ford-Fulkerson Algorithm ---


class MaxFlowGraph:
    """Represents a flow network graph supporting maximum flow computations.

    The Ford-Fulkerson algorithm finds shortest path wth the maximum flow from a source node to the
    sink node of a network. Each edge has a maximum capacity and we also track the amount of flow
    currently passing through it.
    """

    def __init__(self):
        """Use a nested dictionary to store the capacities. For each key-value pair, the key
        is the node moved from and the value is a dictionary of nodes moved to.

        For example, if node A can send up to 5 and 10 units to nodes B and C
        respectively then the residual graph looks like this:

        self.residual_graph = {
            A: {B: 5, C: 10},
            B: {A: 0, C: 0},
            C: {A: 0, B: 0}
        }

        where the reverse edges are initialised with a capacity of zero.
        """

        self.residual_graph = {}

    def add_edge(self, from_node, to_node, capacity):
        """Adds forward and reverse edges with capacity constraints to the network."""
        if from_node not in self.residual_graph:
            self.residual_graph[from_node] = {}

        if to_node not in self.residual_graph:
            self.residual_graph[to_node] = {}

        self.residual_graph[from_node][to_node] = capacity

        if from_node not in self.residual_graph[to_node]:
            self.residual_graph[to_node][from_node] = 0

    def bfs_augementing_path(self, source, sink, parent):
        """Finds a path with available capacity exists from the source node to the sink node
        if one exists.

        The path is stored in the parent dictionary where a key-value pair represents
        an edge between from the node stored in the value to the node stored in the key.
        """

        queue = deque([source])
        visited = set()
        visited.add(source)

        while queue:
            curr_node = queue.popleft()

            for neighbour, resid_capacity in self.residual_graph.get(
                curr_node, {}
            ).items():
                if neighbour not in visited and resid_capacity > 0:
                    parent[neighbour] = curr_node

                    if neighbour == sink:
                        return True

                    visited.add(neighbour)
                    queue.append(neighbour)

        return False

    def ford_fulkerson(self, source, sink):
        """Returns the maximum flow through the grapth from the souce node to the sink node.

        Find the bottleneck: the minimum available capacity along the path from the
        sink node to the source node.

        Pushing the bottleneck forward decreases the available capacity forward and
        increases the available capacity backwards. This allows the algorithm to
        'backtrack' if the optimal path is through a different node.
        """
        max_flow = 0

        # This tracks the path from the BFS.
        parent = {}

        # While the BFS can find a path with available capacity keep running the loop.
        while self.bfs_augementing_path(source, sink, parent):
            bottleneck = float("inf")
            curr_node = sink

            while curr_node != source:
                prev_node = parent[curr_node]
                bottleneck = min(bottleneck, self.residual_graph[prev_node][curr_node])
                curr_node = prev_node

            curr_node = sink

            while curr_node != source:
                prev_node = parent[curr_node]
                self.residual_graph[prev_node][
                    curr_node
                ] -= bottleneck  # Subtract the bottleneck from forward edges.
                self.residual_graph[curr_node][
                    prev_node
                ] += bottleneck  # Add the bottleneck to reverse edges.
                curr_node = prev_node

            max_flow += bottleneck

            # Reset the parent dictionary for the next iteration.
            parent = {}

        return max_flow


# --- Fenwick Tree ---


class FenwickTree:
    """A Fenwick Tree (Binary Indexed Tree) structure for prefix and range sum queries.

    A Fenwick tree is useful to update an element or find the sum of a range of
    elements of an array. Both operations are done in O(log(N)) time where N is
    the length of the array.

    For a normal array, the range sum is computed in O(N) time while for a
    prefix array, updating an element takes O(N) time.

    The LSB of i is the position of the first one bit from the right of i in
    binary. For example, 5 in binary is 101 hence LSB(5) = 1. Using bit-wise
    operations, LSB(i) = i & (-i).

    -i = ~i + 1 where ~ flips each bit of i. Adding one to ~i flips the i - 1
    bits right of the ith bit back to zero and the ith bit back to one. Hence,
    i and (-i) have a one bit in the ith position from the right but the
    remaining bits are opposite parity.

    Thus the & operation gives the position of the 'least signficant bit'.
    """

    def __init__(self, size):
        """A Fenwick tree is stored as a 1-indexed array where the ith index is the sum of LSB(i) elements.

        For example, tree[5] stores the sum of one element ending in 5 which is the 5th element.

        LSB(6) = 2 so tree[6] stores the sum of the 5th and 6th elements. Since arrays in Python are
        zero-indexed and LSB(0) = 0, self.tree is initialised to a zero array of length size + 1.
        """
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, i: int, delta: int) -> None:
        """Add delta to the element at index i.

        TASK: Find all indexes containing sums of numbers including i.

        1. Index i is the sum of LSB(i) numbers ending in i so the sum clearly contains i.

        2. Secondly, if an index j > i is the sum of numbers including i then need

           j - LSB(j) < i <= j.

        j = i + LSB(i) clearly satisfies the right inequality. The left inequality is equivalent to:

        LSB(i) < LSB(i + LSB(i)) = LSB(j). A bit-wise carry, i.e. doing i += i & (-i), ensures that
        j := i + i & (-i) is the least j satisfying LSB(j) > LSB(i).
        """

        while i < self.size:
            self.tree[i] += delta
            i += i & (-i)

    def prefix_query(self, i: int) -> int:
        """Returns the prefix sum from index 1 to i."""

        total_sum = 0
        while i > 0:
            total_sum += self.tree[i]
            i -= i & (-i)

        return total_sum

    def range_query(self, left: int, right: int) -> int:
        """Returns the sum of the range [left, right]."""

        return self.prefix_query(right) - self.prefix_query(left - 1)


# --- Segment Tree ---
# Similar to a Fenwick Tree, range queries and point updates take O(log(n)) time
# in a Segment Tree. If the tree has N elements where N is a power of two, then
# the tree has 2N - 1 nodes so the array is of size 2N.
#
# A quick calculation shows if N = 2^k then the number of nodes in the tree is
# 1 + ... + 2^k = 2^{k + 1} - 1 = 2N - 1.
#
# If N is not a power of two, then the tree is padded to the smallest power of
# two larger than N. From a similar calculation to the one above, the number of
# nodes in the padded tree is 4N - 1 so the array is of size 2N.

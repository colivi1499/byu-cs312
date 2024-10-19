from linear_priority_queue import LinearPriorityQueue
from heap_priority_queue import HeapPriorityQueue
INFINITY = float('inf')

def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    path_to_target: list[int] = []
    pq: HeapPriorityQueue = HeapPriorityQueue()
    pq.make(graph)
    pq.update(0, source)
    dist: dict[int, float] = {node:INFINITY for node in graph}
    dist[source] = 0
    predecessor: dict[int, int] = {node:None for node in graph}
    while (not pq.is_empty()):
        distance, node = pq.pop_min()
        if (node == target):
            break

        if (distance > dist[node]):
            continue

        for neighbor,weight in graph[node].items():
            new_distance = dist[node] + weight
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                predecessor[neighbor] = node
                pq.update(new_distance, neighbor)

    if (dist[target] == INFINITY):
        return [], INFINITY

    next_node: int = target
    while next_node is not None:
        path_to_target.append(next_node)
        next_node = predecessor[next_node]

    path_to_target.reverse()

    return path_to_target, dist[target]

def find_shortest_path_with_array(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    path_to_target: list[int] = []
    pq: LinearPriorityQueue = LinearPriorityQueue()
    pq.make(graph)
    pq.update(0, source)
    dist = {node:INFINITY for node in graph}
    dist[source] = 0
    predecessor: dict[int, int] = {node:None for node in graph}
    while (not pq.is_empty()):
        distance, node = pq.pop_min()
        if (node == target):
            break

        if (distance > dist[node]):
            continue

        for neighbor,weight in graph[node].items():
            new_distance = dist[node] + weight
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                predecessor[neighbor] = node
                pq.update(new_distance, neighbor)

    if (dist[target] == INFINITY):
        return [], INFINITY

    next_node: int = target
    while next_node is not None:
        path_to_target.append(next_node)
        next_node = predecessor[next_node]
        
    path_to_target.reverse()

    return path_to_target, dist[target]


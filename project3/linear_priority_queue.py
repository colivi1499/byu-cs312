INFINITY = float('inf')

class LinearPriorityQueue:
    def __init__(self):
        self.distances: dict[int, float] = {}

    def make(self, graph:dict[int, dict[int, float]]):
        for node in graph:
            self.distances[node] = INFINITY

    def pop_min(self) -> tuple[float,int]:
        if self.is_empty():
            raise ValueError("No nodes in priority queue")
        
        min_node, min_distance = min(self.distances.items(), key=lambda item: item[1])
        
        del self.distances[min_node]
        return min_distance, min_node
    
    def update(self, new_distance: float, node: int):
        self.distances[node] = new_distance

    def push(self, new_distance: float, node: int):
        self.distances[node] = new_distance

    def is_empty(self) -> bool:
        return len(self.distances) == 0
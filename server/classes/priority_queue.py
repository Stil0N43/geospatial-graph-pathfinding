import heapq


class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, int]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: int, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> int:
        return heapq.heappop(self.elements)[1]

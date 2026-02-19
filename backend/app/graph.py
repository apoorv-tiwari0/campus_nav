import json
from collections import deque


class CampusGraph:

    def __init__(self, path="data/graph.json"):

        with open(path, "r") as f:
            self.graph = json.load(f)

    def shortest_path(self, start, goal):

        if start == goal:
            return [start]

        visited = set()
        queue = deque([[start]])

        while queue:

            path = queue.popleft()
            node = path[-1]

            if node == goal:
                return path

            if node not in visited:

                visited.add(node)

                for neighbor in self.graph.get(node, []):
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        return []

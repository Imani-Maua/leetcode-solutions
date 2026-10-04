graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A"],
    "D": ["B"]
}

start = "A"
queue = [start]
i = 0

visited = set()


while i < len(queue):

    node = queue[i]

    i += 1

    if node in visited:
        continue

    visited.add(node)

    for neighbour in graph[node]:
        queue.append(neighbour)
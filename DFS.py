graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A"],
    "D": ["B"]
}

start = "A"
stack = [start]
i = 0

visited = set()


while stack:
    node = stack.pop()


    if node in visited:
        continue

    visited.add(node)

    for neighbour in graph[node]:
        stack.append(neighbour)


print(stack)
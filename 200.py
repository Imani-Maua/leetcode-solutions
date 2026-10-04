from typing import List
from collections import deque



class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

       if not grid:
           return 0

       rows = len(grid)
       cols= len(grid[0])
       visited = set()
       islands = 0



       def breadth_first_search(row: int, col: int):

           search_queue = deque()
           search_queue.append((row, col))
           visited.add((row, col))

           while search_queue:
               row, col = search_queue.popleft()

               directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

               for dr, dc in directions:

                   r, c = row + dr, col + dc

                   if (r in range(rows) and c in range(cols) and grid[r][c] == "1" and (r,c) not in visited):
                       visited.add((r,c))
                       search_queue.append((r,c))
       for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "1" and (row, col) not in visited:
                    breadth_first_search(row, col)
                    islands += 1

       return islands







grid = grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

sol = Solution()
print(sol.numIslands(grid=grid))



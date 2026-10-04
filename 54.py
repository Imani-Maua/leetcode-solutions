class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        result = []

        first_row = 0
        first_col = 0
        last_row = len(matrix) - 1
        last_col = len(matrix[0]) - 1

        while first_row <= last_row and first_col <= last_col:

            # Top row: left → right
            for col in range(first_col, last_col + 1):
                result.append(matrix[first_row][col])

            first_row += 1

            # Right column: top → bottom
            for row in range(first_row, last_row + 1):
                result.append(matrix[row][last_col])

            last_col -= 1

            # Bottom row: right → left
            if first_row <= last_row:
                for col in range(last_col, first_col - 1, -1):
                    result.append(matrix[last_row][col])

                last_row -= 1

            # Left column: bottom → top
            if first_col <= last_col:
                for row in range(last_row, first_row - 1, -1):
                    result.append(matrix[row][first_col])

                first_col += 1

        return result
     


matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

solution = Solution()
print(solution.spiralOrder(matrix=matrix))
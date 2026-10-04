class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        result = []

        while matrix:
            #add the first row/ list to the resulting array
            result += (matrix.pop(0))

            if matrix and matrix[0]:
                for row in matrix:
                    result.append(row.pop())

            if matrix:
                result += (matrix.pop()[::-1])

            if matrix and matrix[0]:
                for row in matrix[::-1]:
                    result.append(row.pop(0))


        return result

matrix = [[1,2,3],[4,5,6],[7,8,9]]
obj = Solution()
print(obj.spiralOrder(matrix=matrix))
class Solution:
    def minimumAbsDifference(self, arr: list[int]) -> list[list[int]]:

        #resulting array
        result = []

        #sort
        arr.sort()


        #initialize min_value
        min_abs = float('inf')

        #initialize i
        i = 0


        #loop  through the array, find min abs difference

        while i in range(len(arr)-1):
            min_abs = min(min_abs, abs(arr[i] - arr[i+1]))
            i+=1

        i = 0
        #loop through the array, find the pairs whose diff == min_abs value
        while i in range(len(arr)-1):
            if abs(arr[i] - arr[i+1]) == min_abs:
                result.append([arr[i], arr[i+1]])

            i += 1

        return result
    

arr = [1,3,6,10,15]
sol = Solution()

print(sol.minimumAbsDifference(arr))

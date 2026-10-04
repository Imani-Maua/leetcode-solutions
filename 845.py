class Solution:
    def longestMountain(self, arr: list[int]) -> int:

        longest = 0
        array = len(arr)
        i = 0

        while i < array - 1:

            #a mountain must start by going up

            while i < array - 1 and arr[i] >= arr[i + 1]:
                 i += 1
                 continue

            start = i

            #ascend
            while i < array - 1 and arr[i] < arr[i + 1]:
                i += 1

            if i == array - 1:
                break

            peak = i

            #descend

            while i < array - 1 and arr[i] > arr[i + 1]:
                i += 1

            if i > peak:
                longest = max(longest, i - start + 1)

        return longest






        
arr = [2,2,2]
obj = Solution()
print(obj.longestMountain(arr=arr))
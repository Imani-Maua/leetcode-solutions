class Solution:
    def longestMountain(self, arr: list[int]) -> int:

        longest = 0

        for i in range(1, len(arr) -1):

            if arr[i - 1] < arr[i] > arr[i+1]:

                left = right = i

                while left > 0 and arr[left] > arr[left - 1]:
                    left -= 1
                    print(f"left: {left}")


                while right < len(arr) -1 and arr[right] > arr[right + 1]:
                    right += 1

                longest = max(longest, right - left + 1)

        return longest


arr = [48,62,39]
obj = Solution()
print(obj.longestMountain(arr=arr))
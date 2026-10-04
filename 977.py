class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:

        result = []
        if not nums:
            return nums

        if nums[0] >= 0:
            return [num ** 2 for num in nums]


        idx = 0
        for i, num in enumerate(nums):
            if num >= 0:
                idx = i
                break

        positives = nums[idx:]

        negatives = nums[:idx]
        negatives = [abs(num) for num in reversed(negatives)]

        i = 0
        j = 0 

        while i < len(positives) and j < len(negatives):
            if positives[i] < negatives[j]:
                result.append(positives[i])
                i += 1

            else:
                result.append(negatives[j])
                j += 1


        result.extend(positives[i:])
        result.extend(negatives[j:])

        return [num ** 2 for num in result]



nums = [-4,-1,0,3,10]
sol = Solution()
print(sol.sortedSquares(nums))
class Solution:
    def smallerNumbersThanCurrent(self, nums: list[int]) -> list[int]:
        temp = sorted(nums)
        mapped = {}
        result = []

        for i, num in enumerate(temp):
            if num not in mapped:
                mapped[num] = i
        
        for num in nums:
            result.append(mapped[num])

        return result

nums = [8, 1, 2, 2, 3]
obj = Solution()

print(obj.smallerNumbersThanCurrent(nums))
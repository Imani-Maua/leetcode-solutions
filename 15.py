from typing import List
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []

        if nums[0] > 0 or nums[-1] < 0:
            return []

        for i, num in enumerate(nums):

            left, right = i + 1, len(nums) -1
            if  i > 0 and num == nums[i-1]: continue

            while left < right:

                total = num + nums[left] + nums[right]

                if total > 0:
                    right -= 1

                elif total < 0:
                    left += 1

                else:
                    result.append([num, nums[left], nums[right]])
                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

        return result


nums = [0,0,0]
sol = Solution()
print(sol.threeSum(nums=nums))


class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        """
        ALGORITHM:
            create a variable to store the current max
            create a variable to store the value of the biggest subarray


            make the first number in the array both the current max and the biggest subarray

            loop through the array starting from the second array to the end,
            at each point check the value of the current max and the value of the array upto 
            the next value
        """

        best_seen = nums[0]

        best_overall = nums[0]

        for i in range(1, len(nums)):
            best_seen = max(nums[i], best_seen + nums[i])

            best_overall = max(best_overall, best_seen)

        return best_overall


nums = [-2,1,-3,4,-1,2,1,-5,4]

sol = Solution()

print(sol.maxSubArray(nums))
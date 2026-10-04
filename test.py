from typing import List
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        triplets = []
        if nums[0] > 0: return []

        for i, num in enumerate(nums):
            left, right = i+1, len(nums)-1
            if i > 0 and num == nums[i-1]: continue
            while left < right:
                total = num + nums[left] + nums[right]

                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    triplets.append([num, nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while nums[left] == nums[left-1] and left < right:
                        left +=1 
                    while nums[right] == nums[right+1] and left < right:
                        right -= 1

        return triplets


        
 


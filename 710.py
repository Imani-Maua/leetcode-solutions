class Solution:
    def findDisappearedNumbers(self, nums: list[int]) -> list[int]:
       result = []
       set_nums = set(nums)

    
       for num in range(1, len(nums) + 1):
        if num not in set_nums:
            result.append(num)
        

       return result


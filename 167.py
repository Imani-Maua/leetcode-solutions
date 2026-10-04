class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:

        right = len(numbers) -1
        left = 0

        while left < right:
            total = numbers[left] + numbers[right]

            if total > target:
                right -= 1
                while left < right and right != len(numbers) - 1 and numbers[right] == numbers[right + 1]:
                    right -= 1

            elif total < target:
                left += 1
                while left < right and left != 0 and numbers[left] == numbers[left - 1]:
                    left += 1

            else:
                return [left+1, right+1]

        return []



nums = [2,3, 4, 5, 6, 7,11,15]

obj = Solution()
print(obj.twoSum(nums, 9))

                

            


class NumArray:

    def __init__(self, nums: list[int]):

        self.nums = nums
        

    def sumRange(self, left: int, right: int) -> int:
        """
        ALGORITHM:
            initialize sum as nums[left]

            WHILE left < right:
                sum += array[left + 1]

                left += 1
        """
        sum = self.nums[left]


        while left < right:
            sum += self.nums[left + 1]

            left += 1


        return sum
        

nums = [-2, 0, 3, -5, 2, -1]
obj = NumArray(nums)

sol = obj.sumRange(2, 5)

print(sol)
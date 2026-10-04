class NumArray:

    def __init__(self, nums: list[int]):

        self.nums = nums
        

    def sumRange(self, left: int, right: int) -> int:
        pref = [0] * len(self.nums)
        sum = self.nums[0]
        pref[0] = nums[0]

        for i in range(1, len(self.nums)):
            pref[i] = pref[i - 1] + self.nums[i]

        print(f"pref: {pref}")
        if left == 0:
            return pref[right]

        return pref[right] - pref[left - 1]
            

nums = [-2, 0, 3, -5, 2, -1]
obj = NumArray(nums)

sol = obj.sumRange(0, 2)

print(sol)
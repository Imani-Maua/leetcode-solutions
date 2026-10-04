class Solution:
    def containsNearbyDuplicate(self, nums: list[int], k: int) -> bool:

        #initialize a dictionary: O(N)
        duplicates = {}

        #initialize a flag to keep track of the duplicates
        flag = False

        i = 0

        #loop through the array: O(N)
        while i in range(len(nums)):
        #at every iteration, check if the number is in dictionary: O(1), if not, add to dictionary
        # {number: index}

            if nums[i] not in duplicates:
                duplicates[nums[i]] = i


            #if in dictionary, check that abs value of diff is <= k. 
            else: 
                diff = abs(i - duplicates[nums[i]])
                # if so, flip flag to True
                if diff <= k:
                    flag = True
                    break

                # if not, delete num from the dictionary, update to the new value
                else:
                    duplicates[nums[i]] = i
            i += 1
               

        #otherwise return false
        return flag

nums = [1,2,3,1]
k = 3
obj = Solution()
print(obj.containsNearbyDuplicate(nums, k))
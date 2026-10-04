class Solution:
    def climbStairs(self, n: int) -> int:
        # initialize dp as dp[0] * (n+1)
        dp = [0] * (n+1)

        # initialize dp[0] and dp[1] as 1
        dp[0] = dp[1] = 1
        # one way of getting to dp[0] is by doing nothing

        # iterate through the array dp starting from index 2:
        # at every dp[i], add dp[i-1] + dp[i-2]
        #for every dp[i], you only got here either from one step or 2 steps back

        for i in range(2, len(dp)):
            dp[i] = dp[i-1] + dp[i-2]

        #return value at dp[-1]
        return dp[-1]


n = 45
obj = Solution()

print(obj.climbStairs(n))
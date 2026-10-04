class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:

        #initialize an array dp which coins indexes from 0 upto amount + 1
        # amount + 1 because we need the index at amount
        #initialize the array with amount + 1 because we need to replace the values with min possible values and they cannot
        #sum up to amount + 1
        dp = [amount + 1] * (amount + 1)


        #set dp[0] as 0 since you need 0 coins to make 0 shillings
        # [0 12 12 12 12 12 12 12 12 12 12 12]
        dp[0] = 0

        # iterate through dp which is all values from 0 to amount (indexes)
        # for every amount, consider all the coins
        for amount in range(len(dp)):
            for coin in coins:
       # only consider amounts whose value is more than the coin
       # dp[i] = min(dp[i], 1 + dp[i - c])
                if (amount - coin) >= 0:
                    dp[amount] = min(dp[amount], 1 + dp[amount - coin])

  

        #return dp[amount]
        return dp[amount] if dp[amount] != amount + 1 else -1 


coins = [1,2,5]
amount = 11
obj = Solution()
print(obj.coinChange(coins, amount))
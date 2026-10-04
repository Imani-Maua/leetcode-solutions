class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        
        max_profit = 0

        if len(prices) < 2:
            return 0
        
        min_price = min(prices[0], prices[1])
       

        for i in range(1, len(prices)):
            max_profit = max(max_profit, prices[i] - min_price)
            min_price = min(min_price, prices[i])

        return max_profit

prices = [7,6,4,3,1]

sol = Solution()
print(sol.maxProfit(prices=prices))
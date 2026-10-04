class Solution:
    def maxProfit(self, prices: list[int]) -> int:

        left, right = 0, 1
        max_profit = 0

        while right != len(prices):

            if prices[left] < prices[right]:
                max_profit = (max_profit, (prices[right] - prices[left]))

            else:

                left = right

            right += 1

        return max_profit


prices = [7,1,5,3,6,4]

sol = Solution()
print(sol.maxProfit(prices=prices))
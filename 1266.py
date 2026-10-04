class Solution:
    def minTimeToVisitAllPoints(self, points: list[list[int]]) -> int:

        #create a variable time to keep track of the time between points
        time = 0

        #check for the time taken between the points at index 0 and 1
        #time taken between indexes is max(dx, dy)
      

        #loop from index 1 to the last index, computing max(dx, dy) at every point, and adding the difference to time
        for idx in range(1, len(points)):
            time += max(abs((points[idx][0] - points[idx-1][0])), abs((points[idx][1] - points[idx-1][1])))

        #return time
        return time


points = [[3,2],[-2,2]]
obj = Solution()

print(obj.minTimeToVisitAllPoints(points=points))




        
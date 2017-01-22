class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # 15min
        # sortedNums = sorted([(nums[i], i) for i in range(len(nums))])
        # start = 0
        # end = len(nums) - 1
        # while start < end:
        #     # Wrong: if start + end == target
        #     if sortedNums[start][0] + sortedNums[end][0] == target:
        #         # return [start, end] Wrong: should original index
        #         return [sortedNums[start][1], sortedNums[end][1]]
        #     elif sortedNums[start][0] + sortedNums[end][0] < target:
        #         start += 1
        #     else:
        #         end -= 1
        # return []

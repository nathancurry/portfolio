"""
My solutions keep using more memory than most people.
"""

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        # catch base case
        if len(nums) == 0:
            return 0
        # find entry
        for c,v in enumerate(nums):
            if v < target:
                continue
            elif v >= target:
                return c
        # if nothing found, return length
        return len(nums)

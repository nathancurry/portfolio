"""
I feel good about this. Took a bit of failure to realize I should be splitting
at len - index instead of using conditional offsets.
"""

class Solution:
    def search(self, nums: List[int], target: int) -> int:    
        l:int = len(nums)
        # base case and final pass
        if not l:
            return -1
        elif l < 3:
            for c,v in enumerate(nums):
                if target == v:
                    return c
            return -1

        # fix for lists of length 3
        index:int = l // 2
        if target == nums[index]:
            return index
        elif target < nums[index]:
            return self.search(nums[:l - index], target)
        else:
            o = self.search(nums[index + 1:], target)
            if o == -1:
                return o
            else:
                return o + index + 1
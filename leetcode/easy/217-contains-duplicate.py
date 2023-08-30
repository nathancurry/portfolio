"""
I had a long day and it was nice to do something I'm good at.
"""

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        dup = set()
        for i in nums:
            if i in dup:
                return True
            dup.add(i)
        return False 
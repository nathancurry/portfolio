"""
This took me longer than it should have, since I was trying to be too clever.
This solution is a bit memory heavy, but reasonably fast.
"""

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        dedup = set()
        for n in nums:
            dedup.add(n)
        out = len(dedup)
        for c,v in enumerate(sorted(dedup)):
            nums[c] = v
        return out
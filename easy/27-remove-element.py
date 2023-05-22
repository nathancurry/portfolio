"""
Store the value in a "stack" and pull it back off into the original array. 
"""

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        stack = list()
        for num in nums:
            if num != val:
                stack.append(num)
        for c,v in enumerate(stack):
            nums[c] = v
        return len(stack)
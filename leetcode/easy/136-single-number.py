"""
I like this solution because it uses the constraint set forth in the problem to 
solve it. I think there are performance issues when using exceptions like this,
but I'm not sure exactly what they are.
"""

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        pops = set()

        # remove will throw an exception if the element is not in the set, so 
        # pairs of numbers will be removed and the last one standing will be
        # returned
        for num in nums:
            try:
                pops.remove(num)
            except:
                pops.add(num)
        
        return pops.pop()
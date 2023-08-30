"""
I think this is a strong solution. Better on memory than CPU, but it's simple. 
Save time by storing the product in a hash and simply call on the way out.
"""

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # s
        products = dict()
        for c,v in enumerate(nums):
            if v in out:
                continue
            else:
                products[v] = 1
                for cc,vv in enumerate(nums): 
                    if c != cc:
                        products[v] *= vv
        
        return [products[x] for x in nums]
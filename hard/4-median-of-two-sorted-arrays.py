"""
Straightforward.
"""

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        m = sorted(nums1 + nums2)        
        mid = len(m)//2
        odd = len(m)%2

        if odd:
            return m[mid]
        else:
            return (m[mid] + m[mid - 1]) / 2
            

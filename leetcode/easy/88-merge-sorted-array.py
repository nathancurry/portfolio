"""
This is my second solution. I had a nested loop with a skip variable, but my other
solution had some edge case bugs I couldn't sort. This solution, I handle base
cases, then build a dict with number counts, and write a handler function for 
number retrieval.
"""

class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """
        # base case
        if n == 0:
            return
        if m == 0:
            for c,v in enumerate(nums2):
                nums1[c] = v
            return

        # build "stack" 
        count = dict()
        for num in nums2:
            count[num] = count.get(num, 0) + 1

        # function to handle stack
        def pop_num(count):
            num = min(count.keys())
            count[num] -= 1
            if count[num] == 0:
                count.pop(num)
            return num

        num = pop_num(count)
        
        for c,v in enumerate(nums1):
            if c < m:
                if v > num:
                    nums1[c] = num
                    count[v] = count.get(v, 0) + 1
                    num = pop_num(count)
                else:
                    continue
            # once you reach m, zeros are padding and the last pop will raise an exception
            else:
                if v == 0:
                    nums1[c] = num
                    try:
                        num = pop_num(count)
                    except:
                        return
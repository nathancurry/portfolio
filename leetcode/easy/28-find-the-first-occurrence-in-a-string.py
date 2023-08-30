"""
I think this is a good simple solution.
"""

class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        # find first character match, then match slice
        for c,v in enumerate(haystack):
            if v != needle[0]:
                continue
            else:
                if needle == haystack[c:c+len(needle)]:
                    return c
                
        # if no matches, return -1
        return -1
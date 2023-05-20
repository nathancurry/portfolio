"""
I feel like there are probably better solutions than relying on the length and specific character check.
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        l = str(x)
        if len(l) == 1:
            return True
        if l[0] == "-":
            return False
        v = True
        for c,v in enumerate(l):
            if l[-c-1] != v:
                v = False
                break
        return v
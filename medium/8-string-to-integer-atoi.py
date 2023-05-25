"""
This solution is a bit simplistic, but I think it's good
"""

class Solution:
    def myAtoi(self, s: str) -> int:
        # prep and base case
        s = s.lstrip(' ')
        if len(s) == 0:
            return 0

        # handle valid signing
        signed = False
        if s[0] == '-':
            signed = True
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]
        
        # build the string
        o = ''
        for c in s:
            try:
                int(c)
                o += c
            except:
                break

        # catch zero length string
        if len(o) == 0:
            return 0

        # convert to signed int and check bounds
        o = int(o)
        if signed:
            if o > 2147483648:
                return -2147483648
            else:
                return -o
        else:
            if o > 2147483647:
                return 2147483647
            else:
                return o
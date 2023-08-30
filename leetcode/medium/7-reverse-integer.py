"""
This solution is a little aggressive on memory, but not sure if there's a much
more efficient way to approach. I basically just pipeline simple transforms. I
improved memory use noticeably by not introducing a string variable and just
altering x in place.
"""

class Solution:
    def reverse(self, x: int) -> int:
        l = list(str(x))
        l.reverse()
        signed = False

        # build string and track signing
        for c in l:
            if c == '-':
                signed = True
            else:
                x += c
        
        # turn it back into a number
        x = int(x)
        if signed:
            x = -x

        # catch out of bounds
        if x > 2147483647 or x < -2147483648:
            return 0

        return x
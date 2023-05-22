"""
Admittedly pretty computationally intensive, but I'm currently optimizing for simplicity
"""

class Solution:
    def mySqrt(self, x: int) -> int:
        # catch the edge cases
        if x < 2:
            return x
        # and then brute force it
        for i in range(x):
            c = i + 1
            if x / (c) < c:
                return c - 1

"""
I've had lots of practice figuring out who has the most candy.
"""


class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        most = max(candies)
        out = []
        for num in candies:
            if num + extraCandies >= most:
                out.append(True)
            else:
                out.append(False)
        return out
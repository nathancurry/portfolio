"""
I use sets here. I opted not to use a dict because I would have to invert it
instead of just using max(). I add 0 to the set to ward off goblins.
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        compare = set({0})
        l = list(s)
        for c, v in enumerate(s):
            length = 1
            charset = set({v})
            for i in s[c+1:]:
                if i in charset:
                    break
                else:
                    charset.add(i)
                    length += 1
            compare.add(length)
        return max(compare)
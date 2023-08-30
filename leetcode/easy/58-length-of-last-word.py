"""
This solution is incredibly hacky. I'm not sure the best pattern to iterate from the end of a string, but there has got to be a better way.
"""

class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        c = 0
        brk = False
        for v in range(len(s)):
            if not s[-v-1].isalpha():
                if brk:
                    break
                continue
            else:
                brk = True
                c += 1
        return c
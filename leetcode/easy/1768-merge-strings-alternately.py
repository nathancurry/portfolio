"""
This doesn't look pretty but it works.
"""

class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        out = ''
        if word1 or word2
            out += word1[0]
            inw1 = word1[1:]
        else:
            inw1 = ''
        if word2:
            out += word2[0]
            inw2 = word2[1:]
        else:
            inw2 = ''

        if inw1 or inw2:
            out += self.mergeAlternately(inw1, inw2)
        return out
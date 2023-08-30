"""
I enjoyed this solution because it's a very dumb process.
"""

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        strno = len(strs)
        buffer = ''
        for c,v in enumerate(strs[0]):
            for string in strs[1:]:
                try:
                    if v != string[c]:
                        return buffer
                except IndexError:
                    return buffer
            buffer += v
        return buffer


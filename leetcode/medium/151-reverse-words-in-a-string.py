"""
I had an embarrassingly ornate solution I was working on, but luckily it didn't
work.
"""

class Solution:
    def reverseWords(self, s: str) -> str:
        bw = s.split()
        return ' '.join(reversed(bw))
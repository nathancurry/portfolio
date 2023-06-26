"""
First, replace vowels with a placeholder and move to their own list. Then, zip
the two lists together, popping the vowels so they end up reversed.
"""


class Solution:
    def reverseVowels(self, s: str) -> str:
        word = []
        vowels = []
        out = ''

        for char in s:
            if char.lower() in ['a', 'e', 'i', 'o', 'u']:
                vowels.append(char)
                word.append('_')
            else:
                word.append(c)

        for char in word:
            if char == '_':
                out += vowels.pop()
            else:
                out += char
        return out
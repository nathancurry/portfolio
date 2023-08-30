"""
I dislike the aesthetics here, but it is what it is.

I wrote another solution with an adjustment variable that scanned for pairs first, but I believe that was 10-20% slower.
"""

class Solution:
    def romanToInt(self, s: str) -> int:
        tally = 0
        check = False
        for c,v in enumerate(s):
            match v:
                case 'M':
                    if check and s[c-1] == 'C':
                        tally += 800
                    else:
                        tally += 1000
                case 'D':
                    if check and s[c-1] == 'C':
                        tally += 300
                    else:
                        tally += 500
                case 'C':
                    if check and s[c-1] == 'X':
                        tally += 80
                    else:
                        tally += 100
                case 'L':
                    if check and s[c-1] == 'X':
                        tally += 30
                    else:
                        tally += 50
                case 'X':
                    if check and s[c-1] == 'I':
                        tally += 8
                    else:
                        tally += 10
                case 'V':
                    if check and s[c-1] == 'I':
                        tally += 3
                    else:
                        tally += 5
                case 'I':
                    tally += 1
            check = True
        return tally
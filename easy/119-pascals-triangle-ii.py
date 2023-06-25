"""
I just adapted 118 to not save the full triangle. I looked at other solutions. 
The best I saw was using binomial coefficients, but need to dig into it more to
fully grasp.
"""

class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        # case of base
        if rowIndex == 0:
            return [1]
        
        # init vars
        hold = []
        previous = [1]
        for row in range(rowIndex + 1):
            if row == 0:
                continue
            else:
                for col in range(row + 1):
                    if col == 0 or col == row:
                        hold.append(1)
                    else:
                        hold.append(previous[col] + previous[col-1])
                previous = hold
                hold = []
        return previous

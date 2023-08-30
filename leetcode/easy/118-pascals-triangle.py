"""
I took some time off from exercises and I'm mentally fatigued from work, so
dropped back down to easies. This performs well, beating 95+% of submissions in
both runtime and memory usage. I'm happy with this.
"""

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        # base case
        if numRows < 1:
            return []
        
        # init vars
        hold = []
        out = []
        previous = [1]
        for row in range(numRows):
            if row == 0:
                out.append([1])
            else:
                for col in range(row + 1):
                    if col == 0 or col == row:
                        hold.append(1)
                    else:
                        hold.append(previous[col] + previous[col-1])
                out.append(hold)
                previous = hold
                hold = []
        return out
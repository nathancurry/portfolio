"""
This is my third attempt.  Initially I ran into some brainblocks and didn't
recurse, so it was ugly.
"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        carry = 0
        def adder(l1, l2, carry):    
            if l1:
                carry += l1.val
                l1 = l1.next
            if l2:
                carry += l2.val
                l2 = l2.next
            l3 = ListNode(val = carry % 10)
            if any([l1, l2, carry // 10]):
                l3.next = adder(l1, l2, carry // 10)
            return l3
        
        return adder(l1, l2, carry)
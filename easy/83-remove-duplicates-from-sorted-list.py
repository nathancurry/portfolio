"""
I came up with this solution quickly. This will help with the other linked-list munging challenges I skipped
"""

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def deleteDuplicates(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head == None:
            return None
        run = head
        while run.next != None:
            if run.next.val == run.val:
                print(run.val, run.next.val)
                hold = run
                run.next = run.next.next
            else:
                run = run.next
        return head
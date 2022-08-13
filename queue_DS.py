"""This module contains a class of a queue data structure, this queue is used to store a history list of block
website by the user"""

# queue data structure class
class history_queue:
    def __init__(self):
        self.queue = list()

    # class method to modify the queue, if the amount of elements in the queue is less than 20, the new block website will just
    # be added into the queue if it is not in the queue already, else, it will pop the last element and insert it as the first element
    def modify(self, add):
        if add not in self.queue:
            if len(self.queue) < 20:
                self.queue.insert(0, add)
            else:
                self.queue.insert(0, add)
                self.queue.pop()
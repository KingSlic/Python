class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, item):
        node = Node(item)
        if self.head == None:
            self.head = node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next

            temp.next = node

    def prepend(self, item):
        node = Node(item)
        node.next = self.head

        self.head = node

    def delete(self, item):
        # Delete an item from linked list
        pass
    def display(self):
        pass # Your implementation goes in here

            

our_linked_list = LinkedList()
our_linked_list.append("A")
our_linked_list.append("B")
our_linked_list.append("C")
our_linked_list.append("D")
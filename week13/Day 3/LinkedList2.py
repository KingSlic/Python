
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
        
# A linkedlist isn't a chain of nodes by itself --
# it's a CONTAINER THAT KNOWS WHERE THE CHAIN STARTS (head)

class LinkedList:
    def __init__(self):
        # create empty list (need a container before adding values)
        self.head = None
        
    def append(self, data):
        
        # Step 1: make a new Node w/ incoming data
        new_node = Node(data)
        
        # Step 2: if list is empty (head is None)
        if self.head is None:
            self.head = new_node
            return
        
        # Step 3: otherwise, walk to the end of the list
        current = self.head
        while current.next is not None:
            current = current.next
        
        # Step 4: link the new node at the end
        current.next = new_node
        
    def insert(self, data, position):
        new_node = Node(data)
        
        # Step 1: handle inserting at the head (position 0)
        if position == 0:
            
            # remember to connect the new node's .next to the old head
            new_node.next = self.head
            self.head = new_node
            return

        # Step 2: Walk to the node right *before* the position
        current = self.head
        index = 0
        while index < position - 1:
            current = current.next
            index += 1
            
        # Step 3: connect new_node into the chain
        new_node.next = current.next
        current.next = new_node
        
    
    def delete_at_position(self, position):
        if self.head is None:
            print("List is empty")
            return
        
        # Deleting head node
        if position == 0:
            removed = self.head
            self.head = self.head.next
            return removed.data
        
        current = self.head
        counter = 0
        while current.next is not None and counter < position - 1:
            current = current.next
            counter += 1
            
        if current.next is None:
            print("Position out of range")
            return
        
        # Skip over the node to delete it
        removed = current.next
        current.next = current.next.next
        return removed.data
        
    def get_at_position(self, position):
        current = self.head
        index = 0
        
        while current:
            if index == position:
                return current.data
            current = current.next
            index += 1
            
        return None
        
    def print_list(self):
        current = self.head
        values = []
        index = 0
        while current is not None:
            values.append(f"[{index}: {current.data}]")
            current = current.next
            index += 1
        print(" -> ".join(values) + " -> None")
        
        
    def length(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count
    
    
    def find_value(self, data):
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
            
        return -1
    
    
    def get_last(self):
        if self.head is None:
            return None
        
        current = self.head
        while current.next is not None:
            current = current.next
        return current.data
        
            
# lst = LinkedList()
# lst.append(10)
# lst.append(20)
# lst.append(30)
# lst.print_list()
# lst.insert("X", 2)
# lst.print_list()

# lst.delete_at_position(1)
# lst.print_list()

# lst.delete_at_position(2)
# lst.print_list()
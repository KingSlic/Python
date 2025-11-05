
class Stack:
    def __init__(self):
        self.__items = []

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        
        return self.__items.pop()
    
    def peek(self):
        if self.is_empty():
            return None
        
        return self.__items[-1]

    def is_empty(self):
        return len(self.__items) == 0
    
    def size(self):
        return len(self.__items)
    

stack = Stack()
stack.push(-1)
stack.push(5)
stack.push(8)
stack.push(-5)

while stack.size() > 0:
    print(stack.pop())
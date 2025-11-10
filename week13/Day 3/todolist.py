# You'll need to include your LinkedList and Node classes from the lesson

from LinkedList2 import LinkedList 


class Task:
    def __init__(self, name):
        self.name = name              #Task description (string)
        self.complete = "incomplete"  #Status: "complete" or "incomplete"
        
    def __str__(self):
        status = self.complete.capitalize()
        return f"{self.name} - {status}"
        


class ToDoList:
    def __init__(self, list_name="My Tasks"):
        self.list_name = list_name
        self.tasks = LinkedList()      # Use your LinkedList to store Task objects
    
    # IMPLEMENT THESE METHODS:
    
    def add_task(self, task_name):

        new_task = Task(task_name)
        self.tasks.append(new_task)
        print(f"Added task: {new_task}")
    
    
    def complete_task(self, position):
        if position <= 0:
            return False
        
        index = position - 1
        
        task = self.tasks.get_at_position(index)
        
        if task is None:
            return False
        
        task.complete = "complete"
        print(f"Task {position} marked complete: {task}")
        return True
            
    
    def remove_task(self, position):
        if position <= 0:
            return False
        
        index = position - 1
        
        removed_task = self.tasks.delete_at_position(index)
        
        if removed_task is None:
            return False
        
        print(f"Removed task {position}: {removed_task}")
        return True
    
    
    
    def view_all_tasks(self):
        print(self.list_name)
        print("=" * len(self.list_name))
        
        current = self.tasks.head
        index = 1
        
        if current is None:
            print("No tasks yet! Now's the time to add your first")
            return
        
        while current:
            task = current.data
            print(f"{index}. {task}")
            current = current.next
            index += 1
            
            
def test_todo_list():
    """Test function to verify ToDoList functionality"""
    print("=== Testing To-Do List Implementation ===\n")
    
    # Create a new to-do list
    todo = ToDoList("School Tasks")
    
    # Test adding tasks
    print("1. Adding tasks...")
    todo.add_task("Study for math exam")
    todo.add_task("Write history essay")
    todo.add_task("Submit science project")
    todo.add_task("Read chapter 5")
    
    # Test viewing all tasks
    print("\n2. Viewing all tasks:")
    todo.view_all_tasks()
    
    # Test completing tasks
    print("\n3. Completing some tasks...")
    todo.complete_task(2)  # Complete second task
    todo.complete_task(4)  # Complete fourth task
    
    # Test viewing after completion
    print("\n4. Viewing tasks after completion:")
    todo.view_all_tasks()
    
    
    # Test removing tasks
    print("\n5. Removing a task...")
    todo.remove_task(3)  # Remove third task
    todo.view_all_tasks()
    
    # Test edge cases
    print("\n6. Testing edge cases...")
    print("Trying to complete task at invalid position:")
    result = todo.complete_task(10)  # Position that doesn't exist
    print(f"Result: {result}")
    
    print("Trying to remove task at invalid position:")
    result = todo.remove_task(0)  # Invalid position (should be 1-indexed)
    print(f"Result: {result}")
    
    print("\n=== Test completed! ===")
    
if __name__ == "__main__":
    test_todo_list()
    


def add(a, b):
    return a+b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a*b

def divide(a, b):
    return a/b

def main():
    num1 = float(input("Enter the first number for calculations: "))
    num2 = float(input("Enter the second number for calculations: "))
    operation = input("Choose an operation to perform (+ - * /): ")

    if operation == "/":
        if num2 == 0:
            return print("\nError: Cannot divide by zero!")
        else:
            return print(f"\n{num1} {operation} {num2} = ", divide(num1, num2))
    elif operation == "+":
        return print(f"\n{num1} {operation} {num2} = ", add(num1, num2))
    elif operation == "-":
        return print(f"\n{num1} {operation} {num2} = ", subtract(num1, num2))
    elif operation == "*":
        return print(f"\n{num1} {operation} {num2} = ", multiply(num1, num2))  
    else:
        return "That is an invalid input, try again."
    
main()
# class Dog:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.energy = 100
#         self.another_att = "Test"

#     def bark(self):
#         print(f"{self.name} says: woof woof!")

#     def play(self, minutes):
#         self.energy -= minutes * 2
#         print(f"{self.name} played for {minutes} minutes")

# dog_max = Dog("Max", 5)
# dog_max.bark()
# dog_max.play(5)

# print(dog_max.energy)


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self.transactions = []
        self.list_of_numbers = [5, 10, 15]

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: {amount}")


    def withdraw(self, amount):
        if amount > self.balance:
            print("insufficient funds!")
        else:
            print(f"You've withdrawn ${amount}")
            self.transactions.append(f"Withdraw ${amount}")
            self.balance -= amount
    
    def show_transactions(self):
        print(f"\n---------- Transaction History for {self.owner}")
        
        if len(self.transactions) == 0:
            print("No transactions found")
        else:
            for transactionMsg in self.transactions:
                print(transactionMsg)

        print(f"Current balance: ${self.balance}\n")


johnAccount = BankAccount("John", 2000)
bobAccount = BankAccount("Bob", 3000)

johnAccount.show_transactions()

johnAccount.deposit(1000)

johnAccount.withdraw(500)
johnAccount.show_transactions()
# # Let's define our simple class
# class Dog:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.energy = 100
#         self.another_attribute = "Test"

#     def bark(self):
#         print(f"{self.name} says: Woof Woof!")

#     def play(self, minutes):
#         self.energy -= minutes * 2
#         print(f"{self.name} dog played for {minutes} minutes")


# dog_max = Dog("Max", 5)
# dog_max.bark()
# dog_max.play(5)
# dog_max.play(10)

# print(dog_max.energy)

# dog_buddy = Dog("Buddy", 5)
# dog_buddy.play(5)
# dog_buddy.play(5)


# user_data = input("Enter a number")
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self.transactions = [] # ["Deposit 2000", "Withdraw 500", "Deposit 200"]

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"{self.owner} Deposit: ${amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds!")
        else:
            self.transactions.append(f"{self.owner} Withdraw ${amount}")
            self.balance -= amount

    def show_transactions(self):
        print(f"\n------------ Transaction History for {self.owner} ---")
        
        if len(self.transactions) == 0:
            print("No transactions were found.")
        else:
            for transactionMsg in self.transactions:
                print(transactionMsg)

        print(f"Current balance: ${self.balance}\n")


johnAccount = BankAccount("John", 2000)
bobAccount = BankAccount("Bob", 2000)

johnAccount.show_transactions()
print(johnAccount.owner)

johnAccount.show_transactions()

johnAccount.deposit(1000)

johnAccount.withdraw(2500)


johnAccount.show_transactions()

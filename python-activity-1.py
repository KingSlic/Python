
userName = input("Enter your name: ")
userAge = int(input("Enter your age: "))


if userAge < 13:
    price = 8
elif userAge >= 13 and userAge < 65:
    price = 12
else:
    price = 9

ticketCount = int(input("How many tickets would you like? "))

totalCost = price*ticketCount

print("\n" + "=" * 30)
print(f"🎟️  Receipt for {userName}")
print("-" * 30)
print(f"Age: {userAge}")
print(f"Ticket price: ${price}")
print(f"Number of tickets: {ticketCount}")
print(f"Total cost: ${totalCost}")
print("=" * 30)
print("Thank you for your purchase!\n")



print("\n=== RESTAURANT MENU ===")
print("1. Pizza - $15.99")
print("2. Burger - $12.50")
print("3. Salad - $9.99")
print("4. Pasta - $13.75")

entree = int(input("Enter your choice (1-4): "))

if entree == 1:
    meal = "Pizza"
    price = 15.99
elif entree == 2:
    meal = "Burger"
    price = 12.50
elif entree == 3:
    meal = "Salad"
    price = 9.99
elif entree == 4:
    meal = "Pasta"
    price = 13.75
else:
    print("Invalid selection, try again!")


drink = input("Would you like a drink? (+$2.50) (y/n): ")

if drink == 'y':
    bev = "Yes"
    drink = 2.50
else:
    bev = "No"
    drink = 0

subtotal = price + drink
tax = subtotal * 0.08

total = subtotal + tax

print("\n=== YOUR ORDER ===")
print(f"Food: {meal} - ${price:.2f}")
print(f"Drink: {bev} - ${drink:.2f}")
print(f"Subtotal: ${subtotal:.2f}")
print(f"Tax (8%): ${tax:.2f}")
print(f"Total: ${total:.2f}\n")



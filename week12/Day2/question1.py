def calculate_budget():
    income = float(input("Enter your monthly income: "))
    rent = float(input("Enter your monthly rent: "))
    food = float(input("Enter your monthly food cost: "))
    leisure = float(input("Enter your monthly entertainment expense: "))

    expenses = rent + food + leisure
    balance = income - expenses

    if balance < 0:
        advice = "You're overspending! Cut back on expenses."
    elif balance < 100:
        advice = "Your budget is tight! Be careful with spending."
    else:
        advice = "Great job! You have money left over."

    print("\n\n=== BUDGET SUMMARY ===")
    print(f"Monthly Income: ${income}")
    print(f"Total Expenses: ${expenses}")
    print(f"Remaining Money: ${balance}")

    print(f"Budget Advice: {advice}\n")

calculate_budget()
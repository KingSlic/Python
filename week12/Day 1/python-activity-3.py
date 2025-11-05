
petType = input("Enter pet type (dog/cat/bird/hamster): ")
petAgeInHuman = int(input("Enter your pet's age in human years: "))

if petType == 'dog':
    if petAgeInHuman <= 2:
        petAge = petAgeInHuman * 12
    else:
        petAge = 24 + ((petAgeInHuman - 2)*4)
elif petType == 'cat':
    if petAgeInHuman <= 2:
        petAge = petAgeInHuman * 12
    else:
        petAge = 24 + ((petAgeInHuman - 2)*4)
elif petType == "bird":
    petAge = petAgeInHuman * 9
elif petType == "hamster":
    petAge = petAgeInHuman * 25
else:
    print("Invalid pet type, try again.")


print("\n=== PET AGE CONVERSION ===")
print(f"Pet Type: {petType}")
print(f"Human Age: {petAgeInHuman} years")
print(f"Pet Age: {petAge} years")
print(f"\nFun Fact: Your {petType} is like a {petAge}-year-old human!\n")

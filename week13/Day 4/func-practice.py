# Sort by length

# words = ['python', 'java', 'javascript', 'c++']
# sorted_words = sorted(words, key=lambda x: len(x))
# print(sorted_words)

# # Sort by last character
# sorted_by_last = sorted(words, key=lambda x: x[-1])
# print(sorted_by_last)

# # Sort dictionaries
# users = [
#     {'name': 'Alice', 'age': 25},
#     {'name': 'Bob', 'age': 30},
#     {'name': 'Charlie', 'age': 19}
# ]
# sorted_users = sorted(users, key=lambda x: x['age'])
# print(sorted_users)

def create_multiplier(factor):
    """Creates function that multiplies by specific factor"""
    return lambda x: x * factor

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))
print(triple(8))

def create_validator(min_val, max_val):
    """Creates a validation function for a range"""
    return lambda x: min_val <= x <= max_val

is_valid_age = create_validator(0,120)
is_valid_percentage = create_validator(0, 100)

print(is_valid_age(25))
print(is_valid_percentage(134))




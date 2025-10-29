
def calcAverage(scores):
    return sum(scores) / len(scores)

def getLetterGrade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"
    

def main():
    scores = []

    numOfScores = int(input("How many test scores would you like to enter? "))
    
    count = 0
    while count < numOfScores:
        score = float(input(f"Enter score {count+1}: "))
        scores.append(score)
        count += 1

    average = calcAverage(scores)
    letter = getLetterGrade(average)

    print("\n=== RESULTS ===")
    print(f"Scores: {scores}")
    print(f"Average Score: {average:.2f}")
    print(f"Letter Grade: {letter}")


main()

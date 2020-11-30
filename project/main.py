while True:
    grade = input("Enter total grade for the group: ")
    try:
        grade = float(grade)
        if grade < 9:
            print("Wrong grade")
        else:
            break
    except ValueError:
        print("Enter a number")

print("Group got a grade of", grade)
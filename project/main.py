while True:
    grade = input("Enter total grade for the group: ")
    try:
        grade = int(grade)
        if grade > 9:
            print("Wrong grade")
        else:
            break

print("Group got a grade of", grade)
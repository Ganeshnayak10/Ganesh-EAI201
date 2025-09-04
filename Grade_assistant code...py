def grade_marks(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 35:
        return "D"
    else:
        return "F"

print("Student Grading Assistant")
subjects = int(input("Enter number of subjects: "))

results = {}
total = 0

for i in range(1, subjects + 1):
    subject = input(f"\nEnter subject {i} name: ")
    marks = int(input(f"Enter marks obtained in {subject}: "))
    grade = grade_marks(marks)
    results[subject] = (marks, grade)
    total += marks

average = total / subjects
print("\nTotal Marks:", total)
print("Average Marks:", round(average, 2))
print("Overall Grade:", grade_marks(average))

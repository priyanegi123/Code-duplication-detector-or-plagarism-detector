import random

class Student:
    def __init__(self, name, roll_no, marks):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks

    def __str__(self):
        return f"{self.name} (Roll No: {self.roll_no}) - Marks: {self.marks}"

class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, name, roll_no, marks):
        student = Student(name, roll_no, marks)
        self.students.append(student)

    def average_marks(self):
        if not self.students:
            return 0
        total = sum(student.marks for student in self.students)
        return total / len(self.students)

    def topper(self):
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.marks)

    def print_students(self):
        for student in self.students:
            print(student)

def generate_random_students(classroom, count):
    first_names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Helen", "Ian", "Jane"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Martinez", "Lee"]
    for i in range(count):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        roll_no = 1000 + i
        marks = random.randint(40, 100)
        classroom.add_student(name, roll_no, marks)

if __name__ == "__main__":
    classroom = Classroom()
    generate_random_students(classroom, 20)
    print("Student List:")
    classroom.print_students()
    print("\nAverage Marks:", classroom.average_marks())
    print("Topper:", classroom.topper())
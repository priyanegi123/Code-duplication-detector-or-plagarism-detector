import random

class Pupil:
    def __init__(self, full_name, student_id, score):
        self.full_name = full_name
        self.student_id = student_id
        self.score = score

    def __str__(self):
        return f"{self.full_name} (ID: {self.student_id}) - Score: {self.score}"

class SchoolClass:
    def __init__(self):
        self.pupils = []

    def enroll_pupil(self, full_name, student_id, score):
        pupil = Pupil(full_name, student_id, score)
        self.pupils.append(pupil)

    def get_average_score(self):
        if not self.pupils:
            return 0
        total = sum(pupil.score for pupil in self.pupils)
        return total / len(self.pupils)

    def get_topper(self):
        if not self.pupils:
            return None
        return max(self.pupils, key=lambda p: p.score)

    def display_pupils(self):
        for pupil in self.pupils:
            print(pupil)

def create_random_pupils(school_class, count):
    first_names = ["Anna", "Brian", "Cathy", "Derek", "Ella", "Fred", "Gina", "Harry", "Isla", "Jack"]
    last_names = ["Clark", "Evans", "Green", "Hill", "King", "Lewis", "Moore", "Nelson", "Owen", "Parker"]
    for i in range(count):
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        student_id = 2000 + i
        score = random.randint(45, 98)
        school_class.enroll_pupil(full_name, student_id, score)

if __name__ == "__main__":
    school_class = SchoolClass()
    create_random_pupils(school_class, 20)
    print("Pupil List:")
    school_class.display_pupils()
    print("\nAverage Score:", school_class.get_average_score())
    print("Topper:", school_class.get_topper())
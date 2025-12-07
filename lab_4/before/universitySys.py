import json
import os
from datetime import datetime

class UniversitySystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.load_data()

    def add_student(self):
        print("\nДобавление студента")
        name = input("Имя: ")
        age = int(input("Возраст: "))
        student_id = input("ID студента: ")
        self.students.append({
            'name': name,
            'age': age,
            'id': student_id,
            'courses': [],
            'grades': {}
        })
        print("Студент добавлен!")
        self.save_data()

    def add_course(self):
        print("\nДобавление курса")
        title = input("Название: ")
        course_id = input("ID курса: ")
        self.courses.append({
            'title': title,
            'id': course_id,
            'students': []
        })
        print("Курс добавлен!")
        self.save_data()

    def enroll_student(self):
        print("\nЗапись студента на курс")
        student_id = input("ID студента: ")
        course_id = input("ID курса: ")

        student = None
        for s in self.students:
            if s['id'] == student_id:
                student = s
                break

        course = None
        for c in self.courses:
            if c['id'] == course_id:
                course = c
                break

        if not student:
            print("Студент не найден!")
            return

        if not course:
            print("Курс не найден!")
            return

        if course_id in student['courses']:
            print("Студент уже записан на этот курс!")
            return

        student['courses'].append(course_id)
        course['students'].append(student_id)
        student['grades'][course_id] = []
        print("Студент записан на курс!")
        self.save_data()

    def add_grade(self):
        print("\nДобавление оценки")
        student_id = input("ID студента: ")
        course_id = input("ID курса: ")
        grade = int(input("Оценка (1-5): "))

        student = None
        for s in self.students:
            if s['id'] == student_id:
                student = s
                break

        if not student:
            print("Студент не найден!")
            return

        if course_id not in student['courses']:
            print("Студент не записан на этот курс!")
            return

        student['grades'][course_id].append({
            'grade': grade,
            'date': datetime.now().strftime("%Y-%m-%d")
        })
        print("Оценка добавлена!")
        self.save_data()

    def generate_report(self, report_type):
        if report_type == "students":
            self.print_students()
        elif report_type == "courses":
            self.print_courses()
        elif report_type == "student_grades":
            self.print_student_grades()
        elif report_type == "course_students":
            self.print_course_students()
        elif report_type == "statistics":
            self.print_statistics()
        else:
            print("Неизвестный тип отчета!")

    def print_students(self):
        print("\n=== Список студентов ===")
        for student in self.students:
            print(f"ID: {student['id']}, Имя: {student['name']}, Возраст: {student['age']}")

    def print_courses(self):
        print("\n=== Список курсов ===")
        for course in self.courses:
            print(f"ID: {course['id']}, Название: {course['title']}")

    def print_student_grades(self):
        print("\n=== Оценки студента ===")
        student_id = input("ID студента: ")

        student = None
        for s in self.students:
            if s['id'] == student_id:
                student = s
                break

        if not student:
            print("Студент не найден!")
            return

        print(f"Студент: {student['name']}")
        for course_id, grades in student['grades'].items():
            course_title = ""
            for c in self.courses:
                if c['id'] == course_id:
                    course_title = c['title']
                    break

            print(f"\nКурс: {course_title}")
            for grade in grades:
                print(f"  Оценка: {grade['grade']}, Дата: {grade['date']}")

    def print_course_students(self):
        print("\n=== Студенты курса ===")
        course_id = input("ID курса: ")

        course = None
        for c in self.courses:
            if c['id'] == course_id:
                course = c
                break

        if not course:
            print("Курс не найден!")
            return

        print(f"Курс: {course['title']}")
        for student_id in course['students']:
            student = None
            for s in self.students:
                if s['id'] == student_id:
                    student = s
                    break

            if student:
                print(f"  Студент: {student['name']}, ID: {student['id']}")

    def print_statistics(self):
        print("\n=== Статистика ===")

        print(f"Всего студентов: {len(self.students)}")

        print(f"Всего курсов: {len(self.courses)}")

        total_age = 0
        for student in self.students:
            total_age += student['age']
        if self.students:
            avg_age = total_age / len(self.students)
            print(f"Средний возраст студентов: {avg_age:.1f}")

        total_grades = 0
        count_grades = 0
        for student in self.students:
            for course_grades in student['grades'].values():
                for grade_record in course_grades:
                    total_grades += grade_record['grade']
                    count_grades += 1

        if count_grades > 0:
            avg_grade = total_grades / count_grades
            print(f"Средняя оценка: {avg_grade:.2f}")

    def save_data(self):
        data = {
            'students': self.students,
            'courses': self.courses
        }
        with open('university_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists('university_data.json'):
            with open('university_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.students = data.get('students', [])
                self.courses = data.get('courses', [])

    def show_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("УНИВЕРСИТЕТСКАЯ СИСТЕМА")
            print("=" * 50)
            print("1. Добавить студента")
            print("2. Добавить курс")
            print("3. Записать студента на курс")
            print("4. Добавить оценку")
            print("5. Сформировать отчет")
            print("6. Выйти")

            choice = input("\nВыберите действие: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_course()
            elif choice == "3":
                self.enroll_student()
            elif choice == "4":
                self.add_grade()
            elif choice == "5":
                print("\nТипы отчетов:")
                print("1. Список студентов")
                print("2. Список курсов")
                print("3. Оценки студента")
                print("4. Студенты курса")
                print("5. Статистика")
                report_choice = input("Выберите тип отчета: ")

                report_types = {
                    "1": "students",
                    "2": "courses",
                    "3": "student_grades",
                    "4": "course_students",
                    "5": "statistics"
                }

                if report_choice in report_types:
                    self.generate_report(report_types[report_choice])
                else:
                    print("Неверный выбор!")
            elif choice == "6":
                print("Выход из системы...")
                break
            else:
                print("Неверный выбор!")

class ReportGenerator:
    @staticmethod
    def generate_student_list(students):
        report = "Отчет: Список студентов\n"
        report += "=" * 30 + "\n"
        for student in students:
            report += f"ID: {student['id']}, Имя: {student['name']}\n"
        return report

    @staticmethod
    def generate_course_list(courses):
        report = "Отчет: Список курсов\n"
        report += "=" * 30 + "\n"
        for course in courses:
            report += f"ID: {course['id']}, Название: {course['title']}\n"
        return report

    @staticmethod
    def calculate_average_age(students):
        if not students:
            return 0
        total_age = 0
        for student in students:
            total_age += student['age']
        return total_age / len(students)

if __name__ == "__main__":
    system = UniversitySystem()
    system.show_menu()
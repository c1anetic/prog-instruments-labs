from typing import List, Dict, Any
from models import Student, Course

class ReportGenerator:
    def __init__(self, service):
        self.service = service

    def generate_student_list(self, students: List[Student]) -> None:
        print("\n=== Список студентов ===")
        for student in students:
            print(f"ID: {student.id}, Имя: {student.name}, Возраст: {student.age}")

    def generate_course_list(self, courses: List[Course]) -> None:
        print("\n=== Список курсов ===")
        for course in courses:
            print(f"ID: {course.id}, Название: {course.title}")

    def generate_student_grades_report(self, student_id: str) -> bool:
        student = self.service.find_student_by_id(student_id)
        if not student:
            return False

        print(f"\nСтудент: {student.name}")
        for course_id, grades in student.grades.items():
            course = self.service.find_course_by_id(course_id)
            if course:
                print(f"\nКурс: {course.title}")
                for grade in grades:
                    print(f"  Оценка: {grade.value}, Дата: {grade.date}")
        return True

    def generate_course_students_report(self, course_id: str) -> bool:
        course = self.service.find_course_by_id(course_id)
        if not course:
            return False

        print(f"\nКурс: {course.title}")
        for student_id in course.students:
            student = self.service.find_student_by_id(student_id)
            if student:
                print(f"  Студент: {student.name}, ID: {student.id}")
        return True

    def generate_statistics_report(self) -> None:
        print("\n=== Статистика ===")
        students = self.service.get_all_students()
        courses = self.service.get_all_courses()

        print(f"Всего студентов: {len(students)}")
        print(f"Всего курсов: {len(courses)}")

        if students:
            total_age = sum(student.age for student in students)
            avg_age = total_age / len(students)
            print(f"Средний возраст студентов: {avg_age:.1f}")

        total_grades = 0
        count_grades = 0
        for student in students:
            for course_grades in student.grades.values():
                for grade_record in course_grades:
                    total_grades += grade_record.value
                    count_grades += 1

        if count_grades > 0:
            avg_grade = total_grades / count_grades
            print(f"Средняя оценка: {avg_grade:.2f}")

    def calculate_average_age(self, students: List[Student]) -> float:
        if not students:
            return 0
        total_age = sum(student.age for student in students)
        return total_age / len(students)
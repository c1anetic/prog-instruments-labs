from typing import Optional, Tuple, List, Dict, Any
from models import Student, Course, Grade
from storage import DataStorage

class UniversityService:
    def __init__(self, storage: DataStorage):
        self.storage = storage
        data = storage.load()
        self.students = data['students']
        self.courses = data['courses']

    def save_data(self) -> None:
        self.storage.save(self.students, self.courses)

    def find_student_by_id(self, student_id: str) -> Optional[Student]:
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id: str) -> Optional[Course]:
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def add_student(self, name: str, age: int, student_id: str) -> None:
        student = Student(name=name, age=age, id=student_id)
        self.students.append(student)
        self.save_data()

    def add_course(self, title: str, course_id: str) -> None:
        course = Course(title=title, id=course_id)
        self.courses.append(course)
        self.save_data()

    def enroll_student(self, student_id: str, course_id: str) -> bool:
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            return False

        if course_id in student.courses:
            return False

        student.courses.append(course_id)
        course.students.append(student_id)
        student.grades[course_id] = []
        self.save_data()
        return True

    def add_grade(self, student_id: str, course_id: str, grade_value: int) -> bool:
        student = self.find_student_by_id(student_id)

        if not student:
            return False

        if course_id not in student.courses:
            return False

        grade = Grade(value=grade_value)
        student.grades[course_id].append(grade)
        self.save_data()
        return True

    def get_all_students(self) -> List[Student]:
        return self.students

    def get_all_courses(self) -> List[Course]:
        return self.courses
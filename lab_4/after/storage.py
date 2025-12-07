import json
import os
from typing import Dict, List, Any
from models import Student, Course, Grade


class DataStorage:
    def __init__(self, filename: str = 'university_data.json'):
        self.filename = filename

    def save(self, students: List[Student], courses: List[Course]) -> None:
        data = {
            'students': [
                {
                    'name': s.name,
                    'age': s.age,
                    'id': s.id,
                    'courses': s.courses,
                    'grades': {course_id: [{'grade': g.value, 'date': g.date}
                                           for g in grades]
                               for course_id, grades in s.grades.items()}
                }
                for s in students
            ],
            'courses': [
                {
                    'title': c.title,
                    'id': c.id,
                    'students': c.students
                }
                for c in courses
            ]
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.filename):
            return {'students': [], 'courses': []}

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        students = []
        for s_data in data.get('students', []):
            student = Student(
                name=s_data['name'],
                age=s_data['age'],
                id=s_data['id'],
                courses=s_data.get('courses', [])
            )
            student.grades = {
                course_id: [Grade(value=g['grade'], date=g['date'])
                            for g in grades_list]
                for course_id, grades_list in s_data.get('grades', {}).items()
            }
            students.append(student)

        courses = [
            Course(
                title=c_data['title'],
                id=c_data['id'],
                students=c_data.get('students', [])
            )
            for c_data in data.get('courses', [])
        ]

        return {'students': students, 'courses': courses}
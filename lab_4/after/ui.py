from service import UniversityService
from report_generator import ReportGenerator


class ConsoleUI:
    def __init__(self, service: UniversityService, report_generator: ReportGenerator):
        self.service = service
        self.report_generator = report_generator

    def show_menu(self) -> None:
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
                self.add_student_ui()
            elif choice == "2":
                self.add_course_ui()
            elif choice == "3":
                self.enroll_student_ui()
            elif choice == "4":
                self.add_grade_ui()
            elif choice == "5":
                self.show_report_menu()
            elif choice == "6":
                print("Выход из системы...")
                break
            else:
                print("Неверный выбор!")

    def add_student_ui(self) -> None:
        print("\nДобавление студента")
        name = input("Имя: ")
        age = int(input("Возраст: "))
        student_id = input("ID студента: ")
        self.service.add_student(name, age, student_id)
        print("Студент добавлен!")

    def add_course_ui(self) -> None:
        print("\nДобавление курса")
        title = input("Название: ")
        course_id = input("ID курса: ")
        self.service.add_course(title, course_id)
        print("Курс добавлен!")

    def enroll_student_ui(self) -> None:
        print("\nЗапись студента на курс")
        student_id = input("ID студента: ")
        course_id = input("ID курса: ")

        if self.service.enroll_student(student_id, course_id):
            print("Студент записан на курс!")
        else:
            print("Ошибка: студент или курс не найден, либо студент уже записан на этот курс!")

    def add_grade_ui(self) -> None:
        print("\nДобавление оценки")
        student_id = input("ID студента: ")
        course_id = input("ID курса: ")
        grade = int(input("Оценка (1-5): "))

        if self.service.add_grade(student_id, course_id, grade):
            print("Оценка добавлена!")
        else:
            print("Ошибка: студент не найден или не записан на курс!")

    def show_report_menu(self) -> None:
        print("\nТипы отчетов:")
        print("1. Список студентов")
        print("2. Список курсов")
        print("3. Оценки студента")
        print("4. Студенты курса")
        print("5. Статистика")
        report_choice = input("Выберите тип отчета: ")

        if report_choice == "1":
            self.report_generator.generate_student_list(self.service.get_all_students())
        elif report_choice == "2":
            self.report_generator.generate_course_list(self.service.get_all_courses())
        elif report_choice == "3":
            student_id = input("ID студента: ")
            if not self.report_generator.generate_student_grades_report(student_id):
                print("Студент не найден!")
        elif report_choice == "4":
            course_id = input("ID курса: ")
            if not self.report_generator.generate_course_students_report(course_id):
                print("Курс не найден!")
        elif report_choice == "5":
            self.report_generator.generate_statistics_report()
        else:
            print("Неверный выбор!")
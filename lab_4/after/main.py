from storage import DataStorage
from service import UniversityService
from report_generator import ReportGenerator
from ui import ConsoleUI

def main():
    storage = DataStorage()
    service = UniversityService(storage)
    report_generator = ReportGenerator(service)
    ui = ConsoleUI(service, report_generator)
    ui.show_menu()

if __name__ == "__main__":
    main()
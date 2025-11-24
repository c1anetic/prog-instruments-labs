import json


def load_json(filename: str) -> dict:
    """
    Загружает из JSON-файла.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке {filename}: {e}")
        return {}

def read(filename: str) -> str:
    """
    Читает содержимое текстового файла.

    :param filename: Путь к файлу, который нужно прочитать.
    :return: Строка с содержимым файла или сообщение об ошибке.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")

def save(filename: str, text: str) -> None:
    """
    Сохраняет текст в файл.

    :param filename: Путь к файлу, в который будет записан текст.
    :param text: Строка, которая будет записана в файл.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
    except Exception as e:
        print(f"Ошибка при записи в файл {filename}: {e}")
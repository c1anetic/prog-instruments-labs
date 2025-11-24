import json
import tempfile
import os
from file_utils import load_json, read, save


class TestFileUtils:
    """Тесты для утилит работы с файлами"""

    def test_load_json_valid_file(self):
        """Тест загрузки валидного JSON файла"""
        test_data = {"key": "value", "numbers": [1, 2, 3]}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == test_data
        finally:
            os.unlink(temp_path)

    def test_load_json_invalid_file(self):
        """Тест загрузки невалидного JSON файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_load_json_nonexistent_file(self):
        """Тест загрузки несуществующего файла"""
        result = load_json("nonexistent_file.json")
        assert result == {}

    def test_read_file_success(self):
        """Тест успешного чтения файла"""
        test_content = "test content\nwith multiple lines"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            temp_path = f.name

        try:
            result = read(temp_path)
            assert result == test_content
        finally:
            os.unlink(temp_path)

    def test_read_file_nonexistent(self):
        """Тест чтения несуществующего файла"""
        result = read("nonexistent_file.txt")
        assert result is None

    def test_save_file_success(self):
        """Тест успешного сохранения файла"""
        test_content = "content to save"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name

        try:
            save(temp_path, test_content)

            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()

            assert saved_content == test_content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
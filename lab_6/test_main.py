import pytest
from unittest.mock import patch
from main import frequency_test, runs_test, longest_run_test, run_tests


class TestStatisticalTests:
    """Тесты статистических функций"""

    @pytest.mark.parametrize("sequence,expected_range", [
        ("0101010101", (0.9, 1.1)),
        ("1111100000", (0.8, 1.0)),
        ("0000011111", (0.8, 1.0)),
        ("", (0, 0)),
        ("1", (0.3, 0.4)),
        ("0", (0.3, 0.4)),
    ])
    def test_frequency_test_parametrized(self, sequence, expected_range):
        """Параметризованный тест частотного теста"""
        result = frequency_test(sequence)

        if sequence == "":
            assert result == 0
        else:
            min_val, max_val = expected_range
            assert min_val <= result <= max_val

    def test_frequency_test_edge_cases(self):
        """Тест крайних случаев для частотного теста"""
        long_ones = "1" * 1000
        result = frequency_test(long_ones)
        assert result < 0.01

        random_seq = "01" * 500
        result = frequency_test(random_seq)
        assert result > 0.1

    @pytest.mark.parametrize("sequence,should_be_zero", [
        ("01010101", False),
        ("11111111", True),
        ("00000000", True),
        ("", True),
        ("111000", False),
    ])
    def test_runs_test_parametrized(self, sequence, should_be_zero):
        """Параметризованный тест теста на последовательности"""
        result = runs_test(sequence)

        if should_be_zero:
            assert result == 0
        else:
            assert 0 <= result <= 1

    def test_runs_test_complex_cases(self):
        """Тест сложных случаев для теста на последовательности"""
        import random
        random.seed(42)
        random_seq = ''.join(str(random.randint(0, 1)) for _ in range(1000))
        result = runs_test(random_seq)
        assert result > 0.001

        many_runs = "01010101010101010101"
        result = runs_test(many_runs)
        assert 0 <= result <= 1

    @pytest.mark.parametrize("sequence,block_size,should_be_zero", [
        ("", 8, True),
        ("01010", 8, True),
        ("0101010101010101", 8, False),
    ])
    def test_longest_run_test_parametrized(self, sequence, block_size, should_be_zero):
        with patch('main.load_json') as mock_load:
            mock_load.return_value = {
                "PROBABILITIES": ["0.2148", "0.3672", "0.2305", "0.1875"]
            }
            result = longest_run_test(sequence, block_size)

        if should_be_zero:
            assert result == 0
        else:
            assert 0 <= result <= 1

    @patch('main.load_json')
    @patch('main.read')
    @patch('main.save')
    def test_run_tests_integration(self, mock_save, mock_read, mock_load_json):
        """Интеграционный тест функции run_tests с моками"""
        mock_load_json.return_value = {
            "CGEN_SEQ_PATH": "c_sequence.txt",
            "JAVAGEN_SEQ_PATH": "java_sequence.txt",
            "RESULTS_PATH": "results.txt",
            "PROBABILITIES": ["0.2148", "0.3672", "0.2305", "0.1875"]
        }

        mock_read.side_effect = [
            "01010101010101010101",  # C sequence
            "10101010101010101010"  # Java sequence
        ]
        run_tests()

        assert mock_load_json.call_count >= 1
        assert mock_read.call_count == 2
        mock_save.assert_called_once()

        call_args = mock_save.call_args
        assert call_args[0][0] == "results.txt"
        saved_content = call_args[0][1]
        assert "Результаты тестирования" in saved_content
        assert "C Sequence:" in saved_content
        assert "Java Sequence:" in saved_content
        assert "Критерий прохождения: P-value ≥ 0.01" in saved_content

    @patch('main.load_json')
    def test_run_tests_error_handling(self, mock_load_json):
        """Тест обработки ошибок в run_tests"""
        mock_load_json.side_effect = Exception("File not found")

        with pytest.raises(Exception, match="File not found"):
            run_tests()

    @patch('main.load_json')
    def test_longest_run_test_with_mock(self, mock_load_json):
        """Тест longest_run_test с моком для load_json"""
        mock_load_json.return_value = {
            "PROBABILITIES": ["0.2148", "0.3672", "0.2305", "0.1875"]
        }

        test_sequence = "0101010101010101" * 2  # 32 бита = 4 блока по 8

        result = longest_run_test(test_sequence, 8)
        mock_load_json.assert_called_once_with("settings.json")
        assert 0 <= result <= 1


class TestEdgeCases:
    """Тесты крайних случаев и обработки ошибок"""

    def test_frequency_test_division_by_zero(self):
        """Тест обработки деления на ноль в frequency_test"""
        result = frequency_test("")
        assert result == 0

    def test_runs_test_division_by_zero(self):
        """Тест обработки деления на ноль в runs_test"""
        result = runs_test("")
        assert result == 0

    def test_longest_run_test_division_by_zero(self):
        """Тест обработки деления на ноль в longest_run_test"""
        result = longest_run_test("", 8)
        assert result == 0

    @patch('main.load_json')
    def test_longest_run_test_settings_error(self, mock_load_json):
        """Тест обработки ошибок в настройках для longest_run_test"""
        mock_load_json.return_value = {}

        with pytest.raises(KeyError):
            longest_run_test("01010101", 8)


class TestMathematicalCorrectness:
    """Тесты математической корректности"""

    def test_frequency_test_known_values(self):
        """Тест частотного теста на известных значениях"""
        sequence = "1" * 55 + "0" * 45
        result = frequency_test(sequence)
        assert result > 0.05

    def test_runs_test_known_patterns(self):
        """Тест runs test на известных паттернах"""
        sequence = "1" * 5 + "0" * 5 + "1" * 5 + "0" * 5
        result = runs_test(sequence)
        assert result < 0.01

    @patch('main.load_json')
    def test_longest_run_test_calculation(self, mock_load_json):
        """Тест корректности вычислений в longest_run_test"""
        mock_load_json.return_value = {
            "PROBABILITIES": ["0.2148", "0.3672", "0.2305", "0.1875"]
        }

        sequence = "0101010101010101"
        result = longest_run_test(sequence, 8)
        assert 0 <= result <= 1

    def test_frequency_test_extreme_bias(self):
        """Тест частотного теста с сильным смещением"""
        sequence = "1" * 90 + "0" * 10
        result = frequency_test(sequence)
        assert result < 0.01

    @patch('main.load_json')
    def test_longest_run_test_different_patterns(self, mock_load_json):
        """Тест longest_run_test с разными паттернами"""
        mock_load_json.return_value = {
            "PROBABILITIES": ["0.2148", "0.3672", "0.2305", "0.1875"]
        }

        long_runs = "1" * 4 + "0" * 4 + "1" * 4 + "0" * 4
        result1 = longest_run_test(long_runs, 8)

        short_runs = "0101010101010101"
        result2 = longest_run_test(short_runs, 8)

        assert 0 <= result1 <= 1
        assert 0 <= result2 <= 1


class TestMockingAdvanced:
    """тесты с использованием моков"""

    @patch('main.load_json')
    @patch('main.frequency_test')
    @patch('main.runs_test')
    @patch('main.longest_run_test')
    @patch('main.save')
    def test_run_tests_with_all_mocks(self, mock_save, mock_longest, mock_runs, mock_freq, mock_load):
        """Тест run_tests с моками всех статистических функций"""
        mock_load.return_value = {
            "CGEN_SEQ_PATH": "c_sequence.txt",
            "JAVAGEN_SEQ_PATH": "java_sequence.txt",
            "RESULTS_PATH": "results.txt",
            "PROBABILITIES": ["0.2148", "0.3672", "0.2305", "0.1875"]
        }

        mock_freq.return_value = 0.5
        mock_runs.return_value = 0.3
        mock_longest.return_value = 0.7

        run_tests()

        assert mock_freq.call_count == 2
        assert mock_runs.call_count == 2
        assert mock_longest.call_count == 2
        mock_save.assert_called_once()

    @patch('main.load_json')
    def test_multiple_longest_run_calls(self, mock_load):
        """Тест multiple вызовов longest_run_test с разными параметрами"""
        mock_load.return_value = {
            "PROBABILITIES": ["0.2148", "0.3672", "0.2305", "0.1875"]
        }

        sequence = "01010101010101010101010101010101"  # 32 бита

        result1 = longest_run_test(sequence, 8)
        result2 = longest_run_test(sequence, 16)
        result3 = longest_run_test(sequence, 4)

        assert 0 <= result1 <= 1
        assert 0 <= result2 <= 1
        assert 0 <= result3 <= 1

        assert mock_load.call_count == 3
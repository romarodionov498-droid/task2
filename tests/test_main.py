import unittest

from src.main import validate_config


class TestConfig(unittest.TestCase):
    """Проверяет параметры конфигурации."""

    def setUp(self):
        """Создает корректную конфигурацию перед каждым тестом."""
        self.config = {
            "package": "org.apache.commons:commons-lang3",
            "repository": "https://repo.maven.apache.org/maven2",
            "test_mode": "false",
            "version": "3.14.0",
            "output_file": "graph.svg",
            "max_depth": "3",
        }

    def test_valid_config(self):
        """Проверяет корректную конфигурацию."""
        validate_config(self.config)

    def test_invalid_package(self):
        """Проверяет некорректное имя пакета."""
        self.config["package"] = "abc"
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_repository(self):
        """Проверяет некорректный адрес репозитория."""
        self.config["repository"] = "abc"
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_test_mode(self):
        """Проверяет некорректный тестовый режим."""
        self.config["test_mode"] = "abc"
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_version(self):
        """Проверяет некорректную версию пакета."""
        self.config["version"] = "???"
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_output_file(self):
        """Проверяет некорректное имя файла изображения."""
        self.config["output_file"] = "graph.txt"
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_max_depth(self):
        """Проверяет некорректную глубину анализа."""
        self.config["max_depth"] = "-3"
        with self.assertRaises(ValueError):
            validate_config(self.config)
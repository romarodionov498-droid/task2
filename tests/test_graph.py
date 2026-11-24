import unittest
from pathlib import Path

from src.graph import (
    build_graph,
    get_test_dependencies,
    read_test_repository,
)


TEST_PATH = (
    Path(__file__).resolve().parents[1] / "test_repository.json"
)


class TestGraph(unittest.TestCase):
    """Проверяет построение графа зависимостей."""

    def setUp(self):
        """Загружает тестовый репозиторий."""
        self.repository = read_test_repository(TEST_PATH)

    def get_children(self, package):
        """Получает зависимости тестового пакета."""
        return get_test_dependencies(self.repository, package)

    def test_cycle(self):
        """Проверяет циклические и общие зависимости."""
        graph = build_graph("A", self.get_children, 3)

        expected = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": ["A", "E"],
            "E": [],
        }

        self.assertEqual(graph, expected)

    def test_max_depth(self):
        """Проверяет ограничение глубины."""
        graph = build_graph("A", self.get_children, 1)

        expected = {
            "A": ["B", "C"],
            "B": [],
            "C": [],
        }

        self.assertEqual(graph, expected)

    def test_zero_depth(self):
        """Проверяет нулевую глубину."""
        graph = build_graph("A", self.get_children, 0)

        self.assertEqual(graph, {"A": []})

    def test_no_dependencies(self):
        """Проверяет пакет без зависимостей."""
        graph = build_graph("E", self.get_children, 3)

        self.assertEqual(graph, {"E": []})
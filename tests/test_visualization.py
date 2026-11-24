import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.visualization import generate_dot, save_svg


class TestVisualization(unittest.TestCase):
    """Проверяет визуализацию графа зависимостей."""

    def test_generate_dot(self):
        """Проверяет формирование описания графа."""
        graph = {
            "A": ["B"],
            "B": [],
        }

        expected = (
            "digraph dependencies {\n"
            '    "A";\n'
            '    "A" -> "B";\n'
            '    "B";\n'
            "}"
        )

        self.assertEqual(generate_dot(graph), expected)

    def test_no_dependencies(self):
        """Проверяет граф без зависимостей."""
        graph = {"A": []}

        expected = (
            "digraph dependencies {\n"
            '    "A";\n'
            "}"
        )

        self.assertEqual(generate_dot(graph), expected)

    def test_cycle(self):
        """Проверяет описание циклических зависимостей."""
        graph = {
            "A": ["B"],
            "B": ["A"],
        }

        dot_text = generate_dot(graph)

        self.assertIn('"A" -> "B";', dot_text)
        self.assertIn('"B" -> "A";', dot_text)

    def test_save_svg(self):
        """Проверяет создание изображения SVG."""
        graph = {"A": ["B"], "B": []}
        dot_text = generate_dot(graph)

        with TemporaryDirectory() as directory:
            output = Path(directory) / "graph.svg"

            save_svg(dot_text, str(output))

            self.assertTrue(output.is_file())

            content = output.read_text(encoding="utf-8")
            self.assertIn("<svg", content)
import subprocess


def generate_dot(graph):
    """Формирует текстовое описание графа на языке Graphviz."""
    lines = ["digraph dependencies {"]

    for package, dependencies in graph.items():
        lines.append(f'    "{package}";')

        for dependency in dependencies:
            lines.append(f'    "{package}" -> "{dependency}";')

    lines.append("}")

    return "\n".join(lines)


def save_svg(dot_text, output_file):
    """Сохраняет изображение графа в формате SVG."""
    subprocess.run(
        ["dot", "-Tsvg", "-o", output_file],
        input=dot_text,
        encoding="utf-8",
        check=True,
    )
import os
import glob
import ast


def parse_module_classes(module_path: str) -> list[ast.ClassDef]:
    classes = []
    files = get_python_files(module_path)

    for file in files:
        with open(file) as f:
            file_classes = get_classes(f.read())
            classes += file_classes

    return classes


def parse_file_classes(file_path: str) -> list[ast.ClassDef]:
    with open(file_path) as f:
        classes = get_classes(f.read())
    return classes


def get_python_files(module_path: str) -> list[ast.ClassDef]:
    python_files = []

    for file_path in glob.glob(os.path.join(module_path, "**/*.py"), recursive=True):
        python_files.append(file_path)
    return python_files


def get_classes(file) -> list[ast.ClassDef]:
    classes = []

    tree = ast.parse(file)
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(node)

    return classes

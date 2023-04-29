import ast


def calculate_dit(cls: ast.ClassDef, hierarchy_classes) -> int:
    bases = cls.bases[:]
    while bases:
        base = bases.pop()
        if isinstance(base, ast.Name) and base.id in hierarchy_classes.keys():
            return 1 + \
                calculate_dit(hierarchy_classes[str(
                    base.id)], hierarchy_classes)
    return 0


def calculate_noc(cls: ast.ClassDef, classes: list[ast.ClassDef]) -> int:
    children = []
    for c in classes:
        for b in c.bases:
            if isinstance(b, ast.Name) and cls.name == b.id or \
                    isinstance(b, ast.Attribute) and cls.name == b.attr:
                children.append(c)

    return len(children)


def calculate_mood(cls: ast.ClassDef, hierarchy_classes):
    inherited_methods = []
    overridden_methods = []
    overridden_attributes = []
    inherited_attributes = []

    for base in cls.bases:
        if isinstance(base, ast.FunctionDef):
            pass
    print()
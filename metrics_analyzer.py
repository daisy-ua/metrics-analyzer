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
    inherited_methods = set()
    inherited_attributes = set()

    methods = set()
    hidden_methods = set()

    attributes = set()
    hidden_attributes = set()

    for body in cls.body:
        if isinstance(body, ast.FunctionDef):
            if body.name.endswith('_'):
                for attr in body.body:
                    if isinstance(attr, ast.Assign) and isinstance(attr.targets[0], ast.Attribute):
                        value = attr.targets[0].attr
                        attributes.add(value)

                        if value.startswith('__'):
                            hidden_attributes.add(value)

                continue

            methods.add(body.name)

            if body.name.startswith('_'):
                hidden_methods.add(body.name)

        elif isinstance(body, ast.Assign) and isinstance(body.targets[0], ast.Name):
            value = body.targets[0].id
            attributes.add(value)

            if value.startswith('__'):
                hidden_attributes.add(value)

    bases = __iterate_bases(cls, hierarchy_classes)
    for base in bases:
        for body in base.body:
            if isinstance(body, ast.FunctionDef):
                if body.name.startswith('_'):
                    for attr in body.body:
                        if isinstance(attr, ast.Assign) and isinstance(attr.targets[0], ast.Attribute):
                            value = attr.targets[0].attr
                            if not value.startswith('__'):
                                inherited_attributes.add(value)

                    continue

                inherited_methods.add(body.name)

            elif isinstance(body, ast.Assign) and isinstance(body.targets[0], ast.Name):
                value = body.targets[0].id
                if not value.startswith('__'):
                    inherited_attributes.add(value)

    overridden_methods = inherited_methods.intersection(methods)
    methods.update(inherited_methods)

    class_only_attributes = attributes.copy()
    overridden_attributes = inherited_attributes.intersection(attributes)
    attributes.update(inherited_attributes)

    original_methods = [m for m in methods if m not in inherited_methods]

    return {
        'm-total': len(methods),
        'm-hidden': len(hidden_methods),
        'm-not-overriden': len(inherited_methods) - len(overridden_methods),
        'm-overriden': len(overridden_methods),
        'm-original': len(original_methods),
        'a-total': len(attributes),
        'a-hidden': len(hidden_attributes),
        'a-class-only': len(class_only_attributes),
        'a-not-overriden': len(inherited_attributes) - len(overridden_attributes)
    }


def __iterate_bases(cls: ast.ClassDef, hierarchy_classes):
    bases = []
    for base in cls.bases:
        if isinstance(base, ast.Name) and base.id in hierarchy_classes.keys():
            bases.append(hierarchy_classes[str(base.id)])
            bases += __iterate_bases(
                hierarchy_classes[str(base.id)], hierarchy_classes)

    return bases

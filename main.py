from file_parser import parse_module_classes
from metrics_analyzer import *
from file_parser import *

if __name__ == '__main__':
    module_path = "/home/supervisor/Downloads/scrapy-master/scrapy/core"
    classes = parse_module_classes(module_path)

    # with open("/home/supervisor/Downloads/test.py") as f:
    #     classes = get_classes(f.read())

    hierarchy_classes = {}
    for cls in classes:
        hierarchy_classes[cls.name] = cls

    max_dit = 0
    for cls in classes:
        dit = calculate_dit(cls, hierarchy_classes)
        if dit > max_dit:
            max_dit = dit


        noc = calculate_noc(cls, classes)
        # print(f'{cls.name} : {noc}')


        mood = calculate_mood(cls, hierarchy_classes)
        

    # print(max_dit)


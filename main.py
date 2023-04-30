from file_parser import parse_module_classes
from metrics_analyzer import *
from file_parser import parse_module_classes, parse_file_classes
import argparse


sample_filename = './sample/sample_input_1.py'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', default=sample_filename, help='File to analyze')
    parser.add_argument('-d', help='Directory to analyze')

    args = parser.parse_args()

    if args.d == None:
        classes = parse_file_classes(args.f)
    else:
        classes = parse_module_classes(args.d)

    output = analyze_metrics(classes)
    with open('output.txt', 'w') as f:
        for o in output:
            for k, v in o.items():
                f.write('%s: %s\n' % (k, v))
            f.write('\n')

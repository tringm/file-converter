import argparse
import importlib
import sys
import unittest

from test.test_result import TestResultCompareFileMeld, TestResultLogMetrics
from config import root_path


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)


def get_test_suites():
    checking_dirs = {root_path() / 'test'}
    suites_dir = set()
    while checking_dirs:
        checking_d = checking_dirs.pop()
        sub_dirs = {d for d in checking_d.iterdir() if d.is_dir() and d.stem != '__pycache__'}
        if not sub_dirs:
            suites_dir.add(checking_d)
        else:
            checking_dirs = checking_dirs.union(sub_dirs)
    test_suites = {}
    for d in suites_dir:
        tests = unittest.TestLoader().discover(d)
        if tests.countTestCases() > 0:
            parent = d.parent.stem
            test_suites[f"{parent}.{d.stem}"] = tests
    return test_suites


if __name__ == '__main__':
    parser = ArgParser(description='test file-converter')
    t_suites = get_test_suites()
    parser.add_argument('test',
                        choices=list(t_suites.keys()) + ['all'],
                        help=f"Test a/all test suite(s) or a specific test cases",
                        type=str)
    parser.add_argument('--verbosity', choices=[1, 2], help=f"Test verbosity (default 2)", type=int, default=2)
    parser.add_argument('--meld',
                        help='Use meld to compare out and exp file (default False)',
                        action='store_true')

    args = parser.parse_args()

    if args.meld:
        result_class = TestResultCompareFileMeld
    else:
        result_class = TestResultLogMetrics

    (root_path() / 'test' / 'io' / 'out').mkdir(parents=True, exist_ok=True)
    # TODO: ugly fix to remove metrics.log file
    if (root_path() / 'test' / 'io' / 'out' / 'metrics.log').is_file():
        (root_path() / 'test' / 'io' / 'out' / 'metrics.log').unlink()

    runner = unittest.TextTestRunner(verbosity=args.verbosity, resultclass=result_class)

    result = False
    if args.test:
        if args.test == 'all':
            results = set()
            for s in t_suites:
                results.add(runner.run(t_suites[s]).wasSuccessful())
            result = all(results)
        else:
            if args.test in list(t_suites.keys()):
                result = runner.run(t_suites[args.test]).wasSuccessful()
            else:
                try:
                    test_path = args.test.split('.')
                    module = importlib.import_module('.'.join(test_path[:-1]))
                    test_case_class = getattr(module, test_path[-1])
                    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_case_class)
                    result = runner.run(suite).wasSuccessful()
                except ValueError:
                    sys.stderr.write(f"error: Suite or test case {args.test} not found\n")
                    parser.print_help()
        if not result:
            sys.exit("Some tests failed")

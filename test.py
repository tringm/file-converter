import argparse
import importlib
import sys
import unittest

from test.tests import get_suites, TestResultCompareFileMeld


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    parser = ArgParser(description='test file-converter')
    suites = get_suites()
    parser.add_argument('test',
                        choices=list(suites.keys()) + ['all'],
                        help=f"Test a/all test suite(s) or a specific test cases",
                        type=str)
    parser.add_argument('--verbosity', choices=[1, 2], help=f"Test verbosity (default 2)", type=int, default=2)
    parser.add_argument('--meld',
                        choices=['True', 'False'],
                        help='Use meld to compare out and exp file (default False)',
                        default='False')

    args = parser.parse_args()

    if args.meld:
        result_class = TestResultCompareFileMeld
    else:
        result_class = unittest.TextTestResult

    runner = unittest.TextTestRunner(verbosity=args.verbosity, resultclass=result_class)

    result = False
    if args.test:
        if args.test == 'all':
            results = set()
            for s in suites:
                results.add(runner.run(suites[s]).wasSuccessful())
            result = all(results)
        else:
            if args.test in list(suites.keys()):
                result = runner.run(suites[args.test]).wasSuccessful()
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

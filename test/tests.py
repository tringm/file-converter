import filecmp
import os
import unittest
from pathlib import Path

from config import root_path


class TestResultCompareFileMeld(unittest.TextTestResult):
    def addFailure(self, test, err):
        if hasattr(test, 'out_file') and hasattr(test, 'exp_file'):
            method_id = test.id().split('.')[-1]
            if method_id in test.out_file and method_id in test.exp_file:
                cont = True
                while cont:
                    res = input("[d]iff, [c]ontinue or [f]reeze? ")
                    if res == "f":
                        os.rename(test.out_file[method_id], test.exp_file[method_id])
                        cont = False
                    elif res == "c":
                        cont = False
                    elif res == "d":
                        os.system("meld " + str(test.exp_file[method_id]) + " " + str(test.out_file[method_id]))
        super(TestResultCompareFileMeld, self).addFailure(test, err)

    def addError(self, test, err):
        super(TestResultCompareFileMeld, self).addError(test, err)


class TestCaseCompare(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input_folder = root_path() / 'test' / 'io' / 'in'
        cls.output_folder = root_path() / 'test' / 'io' / 'out'
        cls.out_file = {}
        cls.exp_file = {}
        cls.in_file = {}

    def file_compare(self, out_f: Path, exp_f: Path, msg=None):
        if not out_f.exists() or not exp_f.exists():
            raise ValueError("Either %s or %s does not exist" % (str(out_f), str(exp_f)))
        if not out_f.is_file() or not exp_f.is_file():
            raise ValueError("Either %s or %s is not a file" % (str(out_f), str(exp_f)))
        if not msg:
            self.assertTrue(filecmp.cmp(str(out_f), str(exp_f), shallow=False),
                            f"out file {str(out_f)} does not match exp file {str(exp_f)}")
        else:
            self.assertTrue(filecmp.cmp(str(out_f), str(exp_f), shallow=False), msg)

    def set_up_compare_files(self, method_id):
        self.out_file[method_id] = self.output_folder / (method_id + '_out.txt')
        self.exp_file[method_id] = self.output_folder / (method_id + '_exp.txt')

    def file_compare_by_method_id(self, method_id):
        self.file_compare(out_f=self.out_file[method_id], exp_f=self.exp_file[method_id])


def get_suites():
    checking_dirs = {root_path() / 'test'}
    suites_dir = set()
    while checking_dirs:
        checking_d = checking_dirs.pop()
        sub_dirs = {d for d in checking_d.iterdir() if d.is_dir() and d.stem != '__pycache__'}
        if not sub_dirs:
            suites_dir.add(checking_d)
        else:
            checking_dirs = checking_dirs.union(sub_dirs)
    suites = {}
    for d in suites_dir:
        tests = unittest.TestLoader().discover(d)
        if tests.countTestCases() > 0:
            parent = d.parent.stem
            suites[f"{parent}.{d.stem}"] = tests
    return suites

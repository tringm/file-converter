import filecmp
import time
import unittest
from pathlib import Path

from config import root_path


class TestCaseTimer(unittest.TestCase):
    def setUp(self) -> None:
        self._started_at = time.time()

    def tearDown(self) -> None:
        self._elapsed = time.time() - self._started_at


class TestCaseCompare(TestCaseTimer):
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
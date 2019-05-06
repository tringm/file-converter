import json

import ndjson

from core.converter import PandasFormatConverter
from test.tests import TestCaseCompare


class TestPandasFormatConverter(TestCaseCompare):
    @classmethod
    def setUpClass(cls):
        super(TestPandasFormatConverter, cls).setUpClass()
        cls.converter = PandasFormatConverter()

    def test_json_to_csv(self):
        out_f = self.output_folder / "test_json_to_csv_out.csv"
        self.converter.convert_file(self.input_folder / 'sample.json', 'csv', out_f)
        self.file_compare(out_f, self.input_folder / 'sample_with_index.csv')

    def test_json_to_csv_with_convert_options(self):
        out_f = self.output_folder / "test_json_to_csv_with_convert_options_out.csv"
        self.converter.convert_file(input_file_path=self.input_folder / 'sample.json',
                                    output_format='csv',
                                    output_file_path=out_f,
                                    convert_options={'sep': ';', 'index': False})
        self.file_compare(out_f, self.input_folder / 'sample_semicolon.csv')

    def test_json_to_ndjson(self):
        out_f = self.output_folder / "test_json_to_ndjson_out.ndjson"
        self.converter.convert_file(self.input_folder / 'sample.json', 'ndjson', out_f)
        self.assertEqual(ndjson.load(out_f.open()), ndjson.load((self.input_folder / 'sample.ndjson').open()))

    def test_json_to_excel(self):
        method_id = self.id().split('.')[-1]
        self.out_file[method_id] = self.output_folder / (method_id + "_out.xlsx")
        self.exp_file[method_id] = self.output_folder / (method_id + "_exp.xlsx")
        # TODO: compare excel file?
        self.converter.convert_file(self.input_folder / 'sample.json', 'xlsx', self.out_file[method_id])

    def test_ndjson_to_csv(self):
        out_f = self.output_folder / "test_ndjson_to_csv_out.csv"
        self.converter.convert_file(self.input_folder / 'sample.ndjson', 'csv', out_f)
        self.file_compare(out_f, self.input_folder / 'sample_with_index.csv')

    def test_ndjson_to_json(self):
        out_f = self.output_folder / "test_ndjson_to_json_out.json"
        self.converter.convert_file(self.input_folder / 'sample.ndjson', 'json', out_f)
        self.assertCountEqual(json.load(out_f.open()), json.load((self.input_folder / 'sample.json').open()))

    def test_csv_to_json(self):
        out_f = self.output_folder / "test_csv_to_json_out.json"
        self.converter.convert_file(self.input_folder / 'sample.csv', 'json', out_f)
        self.assertCountEqual(json.load(out_f.open()), json.load((self.input_folder / 'sample_null.json').open()))

    def test_csv_to_json_with_load_options(self):
        out_f = self.output_folder / "test_csv_to_json_with_load_options_out.json"
        self.converter.convert_file(self.input_folder / 'sample_semicolon.csv', 'json', out_f,
                                    load_options={'sep': ';'})
        self.assertCountEqual(json.load(out_f.open()), json.load((self.input_folder / 'sample_null.json').open()))

    def test_csv_to_ndjson(self):
        out_f = self.output_folder / "test_csv_to_ndjson_out.ndjson"
        self.converter.convert_file(self.input_folder / 'sample.csv', 'ndjson', out_f)
        self.assertEqual(ndjson.load(out_f.open()), ndjson.load((self.input_folder / 'sample_null.ndjson').open()))

    def test_excel_to_json(self):
        out_f = self.output_folder / "test_excel_to_json_out.json"
        self.converter.convert_file(self.input_folder / 'sample.csv', 'json', out_f)
        self.assertCountEqual(json.load(out_f.open()), json.load((self.input_folder / 'sample_null.json').open()))

    def test_excel_to_ndjson(self):
        out_f = self.output_folder / "test_excel_to_ndjson_out.ndjson"
        self.converter.convert_file(self.input_folder / 'sample.csv', 'ndjson', out_f)
        self.assertEqual(ndjson.load(out_f.open()), ndjson.load((self.input_folder / 'sample_null.ndjson').open()))


from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path
import pandas as pd
import timeit


allowed_formats = ['csv', 'json', 'xlsx', 'ndjson']


class FormatConverter(ABC):
    def __init__(self):
        super().__init__()

    def validate_convert_file(self, input_file_path, output_format, output_file_path, input_format):
        if output_format not in allowed_formats:
            raise ValueError(f"Expected input format to be {str(allowed_formats)} instead of {output_format}")

        try:
            input_file_path = Path(input_file_path)
        except Exception as e:
            raise e

        file_name = input_file_path.stem

        if not output_file_path:
            output_file_path = input_file_path.parent / (file_name + output_format)
        else:
            try:
                output_file_path = Path(output_file_path)
            except Exception as e:
                raise e

        if not input_format:
            input_format = input_file_path.suffix.replace('.', '')

        if input_format not in allowed_formats:
            raise ValueError(f"Expected input format to be {str(allowed_formats)} instead of {input_format}")

        return input_file_path, output_format, output_file_path, input_format

    @abstractmethod
    def convert_file(self, input_file_path: Union[str, Path], output_format: str, output_file_path=None,
                     input_format=None):
        """

        :param input_file_path: input file path
        :param output_format: output format
        :param output_file_path: if output folder is not define, the output file will be in the same dir with input file
        :param input_format:  if input format is not define, the input format will be auto detected by file name suffix
        :return:
        """
        pass


class PandasFormatConverter(FormatConverter):
    def __init__(self):
        super().__init__()

    def convert_file(self, input_file_path: Union[str, Path], output_format: str, output_file_path=None,
                     input_format=None, load_options=None, convert_options=None):
        """

        :param input_file_path: input file path
        :param output_format: output format
        :param output_file_path: if output folder is not define, the output file will be in the same dir with input file
        :param input_format: if input format is not define, the input format will be auto detected by file name suffix
        :param load_options: dictionary contains arguments for pandas read function
        :param convert_options: dictionary contains arguments for pandas convert function
        :return:
        """
        start = timeit.default_timer()
        try:
            input_file_path, output_format, output_file_path, input_format,  = \
                self.validate_convert_file(input_file_path, output_format, output_file_path, input_format)
        except Exception as e:
            raise e

        read_functions = {'csv': pd.read_csv, 'xlsx': pd.read_excel, 'json': pd.read_json, 'ndjson': pd.read_json}
        default_options = {'csv': {}, 'xlsx': {}, 'json': {'orient': 'records'},
                           'ndjson': {'orient': 'records', 'lines': True}}

        if not load_options:
            load_options = default_options[input_format]
        else:
            load_options.update(default_options[input_format])

        data = read_functions[input_format](input_file_path, **load_options)
        print(f"Load file {str(input_file_path)} took {timeit.default_timer() - start}")

        start = timeit.default_timer()
        convert_functions = {'csv': data.to_csv, 'xlsx': data.to_excel, 'json': data.to_json, 'ndjson': data.to_json}

        if not convert_options:
            convert_options = default_options[output_format]
        else:
            convert_options.update(default_options[output_format])

        convert_functions[output_format](output_file_path, **convert_options)

        print(f"Convert file to {output_format} took {timeit.default_timer() - start}")

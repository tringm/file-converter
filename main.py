import argparse
import sys

import core.converter as converter


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    parser = ArgParser(description='run file-converter')
    converters = {converter_cls.__name__: converter_cls for converter_cls in converter.FormatConverter.__subclasses__()}
    parser.add_argument('converter',
                        choices=list(converters.keys()),
                        help=f"Use a converter",
                        type=str)
    parser.add_argument('input_file_path', metavar='inPath',
                        help="Path to the input file")
    parser.add_argument('output_format',
                        choices=converter.allowed_formats,
                        help=f"Output format")
    parser.add_argument('--outPath',
                        help=f"Path to output file. "
                        f"If not defined, output file will be in the same folder with input file",
                        default=None)
    parser.add_argument('--inFormat',
                        help=f"Input format. If not defined, use file extension",
                        default=None)

    args = parser.parse_args()

    converters[args.converter].convert_file(args.input_file_path, args.output_format, args.output_file_path,
                                            args.input_format)
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from typing import List

import flow_files.dto.program_arguments


def main(args: List[str]):
    """
    The main entry point. Defines the ArgumentParser, parses them, configure logging, and activates the run_flow
    method of the main flow, passing the information from the CLI.
    Args:
        args: argument from the CLI
    """
    from flow_files import word_count_flow, common
    parser = common.get_parser()
    parser.add_argument(
        '--input-path',
        default='gs://dataflow-samples/shakespeare/kinglear.txt',
        dest="input_path",
        help='The file path for the input text to process.')
    parser.add_argument('--output-path',
                        required=True,
                        dest="output_path",
                        help='The path prefix for output files.')
    args, beam_args = parser.parse_known_args(args)
    arguments = flow_files.dto.program_arguments.ProgramArguments(
        **args.__dict__)
    common.configure_logging(logging_info=arguments.log_info,
                             logging_debug=arguments.log_debug)
    word_count_flow.run_flow(arguments, beam_args)


if __name__ == '__main__':
    main(sys.argv[1:])

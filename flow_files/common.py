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

import logging
# You can import these functions from the flow dispatcher (main program, locally) or from the dataflow workers,
# Implication: make sure to not import anything that is installed only on the dev environment
from argparse import ArgumentParser
from typing import Literal

RUNTIME_ENVIRONMENTS = ['local', 'cloud']
RUNTIME_ENVIRONMENT = Literal['local', 'cloud']


def get_parser() -> ArgumentParser:
    """
    Create and return the ArgumentParser. This is contained in the common module, as it might be used for multiple
    entry-points. The common options will be contained inside this function, while the specific arguments for each
    entry point, would be contained in the entry points themselves.

    Returns:
        ArgumentParser
    """
    parser = ArgumentParser()
    parser.add_argument('--log-info',
                        action="store_true",
                        default=True,
                        dest="log_info",
                        help="Logging INFO level in main process")
    parser.add_argument('--log-debug',
                        action="store_true",
                        default=False,
                        dest="log_debug",
                        help="Logging DEBUG level in main process")
    parser.add_argument(
        "ENVIRONMENT",
        help="Which Environment to run in. Choices: %(choices)s",
        choices=RUNTIME_ENVIRONMENTS)
    return parser


def configure_logging(logging_info=True, logging_debug=False):
    """
    Setup logging.
    """
    logging.basicConfig(
        format=
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    if logging_debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif logging_info:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARN)

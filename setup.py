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

import setuptools

setuptools.setup(
    name='Example Word Count',
    version='1.0',
    install_requires=[
        # Although modern python exposes @dataclass,
        # this is to demonstrate pypi dependencies that will be installed on the workers as well on local environment
        "pydantic==1.9.0",
    ],

    # To setup a local dev environment, that allows running the flow, and also other scripts.
    # These dependencies will NOT be installed on the dataflow workers.
    # pip install -e .[dev]
    extras_require={
        "dev": [
            "apache-beam[gcp]",  # for local development and executing the flow
            "yapf",  # for python formatting
        ]
    },
    packages=setuptools.find_packages(),
)
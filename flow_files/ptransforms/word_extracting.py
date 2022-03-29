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

import apache_beam as beam


class WordExtracting(beam.DoFn):
    """
    Parse each line of input text into words.
    """

    def process(self, element):
        import re
        return [
            x.lower().strip()
            for x in re.findall(r'[\w\']+', element, re.UNICODE)
            if len(x.strip()) > 2
        ]

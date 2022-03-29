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

import csv
import io

import pydantic


class WordCount(pydantic.BaseModel):
    """
    DTO to model the pair of a word to the count of occurrences in a text
    """
    word: str
    count: int

    def to_csv_string(self):
        """
        Helper method to format the WordCount to a string in a CSV format.
        The method in its current form is far from memory efficient, but it is generic, and will work consistently,
        with any pydantic Model

        Returns:
            string, a representation of this instance, in a CSV format.
        """
        output = io.StringIO()
        fieldnames = list(self.schema()["properties"].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writerow(self.dict())
        return output.getvalue().strip()

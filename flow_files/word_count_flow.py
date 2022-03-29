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
import os
from typing import List

import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import PipelineOptions

from . import dto
from . import ptransforms
from .common import RUNTIME_ENVIRONMENT
from .dto.program_arguments import ProgramArguments


def get_beam_options(environment: RUNTIME_ENVIRONMENT,
                     beam_args: List[str]) -> PipelineOptions:
    """
    Function to create the required PipelineOptions object, depending on the given runtime environment and other
    arguments passed from the CLI

    Args:
        environment:
            String. Either "cloud" or "local".
        beam_args:
            List[str]. arguments provided by the CLI to be passed to the apache beam pipeline.

    Returns:
        PipelineOptions. To be passed to the constructor of the apache_beam.Pipeline.
    """

    # You can have more runtime environments (e.g production / test / dev etc. each with its own configurations)
    if environment == "cloud":
        return PipelineOptions(
            flags=beam_args,
            runner='DataflowRunner',
            job_name='wordcount-from-python-multiple-files',
            setup_file='./setup.py',

            # Feel free to hard-code other properties that will not change, but remember that in this structure,
            # any properties given here are not overridable by the CLI
            # project='my-project-id',
            # temp_location='gs://my-bucket/temp',
            # region='us-central1',
        )
    else:
        assert environment == "local"

        # The output directory is already in .gitignore
        if not os.path.exists("./output"):
            os.mkdir("output")
        return PipelineOptions(
            runner="DirectRunner",
            temp_location='./output/temp',
        )


def tuple_to_wordcount(word: str, count: int) -> dto.WordCount:
    """
    Helper method to convert a tuple to a WordCount object
    """
    return dto.WordCount(word=word, count=count)


def wordcount_to_csv_string(wordcount: dto.WordCount) -> str:
    """
    Helper method to convert a WordCount object to a csv string (implemented inside the DTO object).
    """
    return wordcount.to_csv_string()


def run_flow(args: ProgramArguments, beam_args: List[str]):
    """
    The main flow.

    Args:
        args: ProgramArguments. the parsed arguments object.
        beam_args: list of strings, the rest of the unparsed cli arguments.
    """
    beam_options = get_beam_options(args.ENVIRONMENT, beam_args)
    logging.info(f"{args}, Beam options: {beam_options.get_all_options()}")
    with beam.Pipeline(options=beam_options) as p:
        lines = p | 'Read' >> ReadFromText(args.input_path)
        counts = (
            lines
            | 'Split' >>
            (beam.ParDo(ptransforms.WordExtracting()).with_output_types(str))
            | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
            | 'GroupAndSum' >> beam.CombinePerKey(sum)
            | 'ToWordCount' >>
            (beam.MapTuple(tuple_to_wordcount)).with_output_types(
                dto.WordCount))
        output = counts | 'Format' >> beam.Map(wordcount_to_csv_string)
        output | 'Write' >> WriteToText(args.output_path)

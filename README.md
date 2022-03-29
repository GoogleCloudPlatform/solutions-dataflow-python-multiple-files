# solutions-dataflow-python-multiple-files-example
## Introduction
A WordCount example for Apache Beam / Google Cloud Dataflow, demonstrating basic file/folder structure that allows splitting business logic to multiple files and with pypi dependencies for local development and cloud runtime.

## Versions
Built and tested on: 
- python 3.9.9
- apache-beam[gcp] 2.37.0

## Motivation
The need to split your code into multiple files might serve different purposes, starting on just better ordering of code and also to re-use logic in case you are maintaining multiple flows/scripts in one code base and want to share the logic between several of these entry points.

Building apache-beam based data pipelines is a great tool to any data engineer. Python is one of the most popular languages to write these data pipelines, due to its rich ecosystem of data-related packages, among other things. However, due its interpreted nature, it is not straight forward to distribute the code into a distributed processing engine like Google Cloud Dataflow. The distributed workers need to have the right python files and to install the dependencies of your code.

This is unlike other complied languages (mainly Java) where your code and files are compiled into one Jar that is easily distributable, as it is all containing.

For dependencies, there is the possibility of using the standard `requirements.txt` file, and specifying the path in `PipelineOptions`  (e.g. via the CLI argument `--requirements_file=/your/requirements/file/path`). However, this does not solve the need to split the business logic of your flow into multiple files. 

This Repository demonstrates a variation of the official [WordCount example](https://beam.apache.org/get-started/wordcount-example/) provided by Apache Beam, but splitting the code into several python files, including several modules (namely: `dto` for simple dataclasses and `ptransforms` for all your apache beam needs). It also demonstrates how to specify PyPi dependencies for both production and for local development (we use `pydantic` instead of standard dataclasses strictly for that purpose).

## Tree
```bash
$ tree .
 ├── flow_files                 # all business logic goes here, including the flow itself
 │  ├── dto                     # for simple DTOs
 │  │  ├── __init__.py
 │  │  └── wordcount.py         # the WordCount DTO
 │  ├── ptransforms             # for all PTransforms (inherit apache_beam.DoFn)
 │  │  ├── __init__.py
 │  │  └── word_extracting.py   # extract words from lines of text
 │  ├── __init__.py
 │  ├── common.py               # common functionality
 │  └── word_count_flow.py       # the main flow - this is the where the pipeline is described. You can multiple flow files.
 ├── output                     # Just an empty folder to hold results
 ├── .gitignore
 ├── LICENSE
 ├── README.md                  # this file
 ├── main.py                    # the main entry point. Mostly defines CLI arguments and calls the word_count_flow entry point. You can have multiple entry points here. 
 └── setup.py                   # the setup.py, that describes the package, and its dependencies
```


## Key points
- `setup.py` contains all the dependencies, as well as describing the package itself. Note that part of the setup is to define the core-dependencies (under the `install_requires` section) as well as defining a dev setup, that includes the dependencies required for local development and testing (under the section `extra_requires`). The dev dependencies will NOT be installed on the remote workers.
- `main.py` is the entry point to run the flow. You can change its name, and have multiple entry points, each can point to a different flow, or do other things (e.g other scripts that do not require running on dataflow.) It is recommended to keep the business logic in these entry-point files to a minimum.
- `flow_files` is the main package that holds all the flows and business logic needed. It can have sub-packages for better separation.
- `word_count_flow.py` is the main flow. it will define the CLI arguments and parse them. Create a runner for the apache beam flow, and import logic from other files to construct the flow.

## How to run?
Before running on the Google Cloud Dataflow platform, make sure you are authenticated:
```bash
gcloud auth application-default login
```
Read more about the command in the [official docs](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login).

### Installing the dependencies
This repo has a dependency list for production, as well as added development dependencies that will be __added__ to the production dependencies.

To install the production dependencies only:
```bash
pip install -e .
```

To install the production and development dependencies:
```bash
pip install -e ".[dev]"  # Note the name `dev` corresponds to the environment defined in the `setup.py` file.
```

### Running the flow

In order to run locally:
```bash
python -m main local [--input-path INPUT_PATH] --output-path OUTPUT_PATH
```
Note that input path is optional (defaults to a file in a public read-only bucket, `gs://dataflow-samples/shakespeare/kinglear.txt`), as it has a default, but output path is required. Both paths can be local filesystem or `gs://` GCS bucket paths.

To run on Google Cloud Dataflow:
```bash
python -m main cloud [--input-path INPUT_PATH] --output-path OUTPUT_PATH
```
When running in cloud mode, the paths cannot be local file systems, and must be accessible to dataflow (usually `gs://` GCS bucket paths).
Note that running the __module__ main with the `-m` flag is crucial for the flow to run. Another important thing is to note that the `word_count_flow.py` has hard-coded the `setup_file` argument, which is also a must (although hard-coding it is not a must, you just need to make sure to provide that argument to point to the correct setup file).

Both of the above are required so Dataflow knows to run this as one module (not as individual files), and to install the required dependencies. 

## Modifying and extending arguments
The `word_count_flow.py` contains some hard-coded configurations for a local runtime (for testing) and for running on the cloud (dataflow). This is of-course, extendable to be more robust, contain more runtime environments (e.g test/qa), get more CLI arguments to fine-tune the behaviour of the flow.

One important note, is that the way `DataflowRunner` is constructed, is that any value that is passed directly as a named argument (e.g. project) cannot be overridden from the CLI arguments (in the `DataflowRunner` constructor this is called the `flags` arguments, a list of strings, representing arbitrary cli arguments that were not parsed by `ArgumentParser`).

This means that if you run the flow with a `region` cli argument:
```bash
python -m main cloud [--input-path INPUT_PATH] --output-path OUTPUT_PATH --region europe-west4
```

And the `DataflowRunner` is instantiated with a named argument `region`, e.g:
```python
options = PipelineOptions(
    flags=beam_args,  # unparsed arguments that will be passed to beam, and might include `['--region', 'europe-west4']`
    runner='DataflowRunner',
    job_name='wordcount-from-python-multiple-files',
    setup_file='./setup.py',
    
    region='us-central1', # A named argument cannot be overridden from the CLI
)
```

That argument will be ignored and the flow will run in the `us-central1` region.
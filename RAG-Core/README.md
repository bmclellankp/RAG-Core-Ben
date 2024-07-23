<div align="center">

<div align="center">


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://www.codium.ai/images/cover-agent/cover-agent-dark.png" width="330">
  <source media="(prefers-color-scheme: light)" srcset="https://www.codium.ai/images/cover-agent/cover-agent-light.png" width="330">
  <img src="https://www.codium.ai/images/cover-agent/cover-agent-light.png" alt="logo" width="330">

</picture>
<br/>
RAG Core Agent aims to help efficiently transform code, by automatically generating and writing new code based on existing files.
</div>

[![GitHub license](https://img.shields.io/badge/License-AGPL_3.0-blue.svg)](https://github.com/Codium-ai/cover-agent/blob/main/LICENSE)
[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label&color=purple)](https://discord.gg/cYsvFJJbdM)
[![Twitter](https://img.shields.io/twitter/follow/codiumai)](https://twitter.com/codiumai)
    <a href="https://github.com/Codium-ai/cover-agent/commits/main">
    <img alt="GitHub" src="https://img.shields.io/github/last-commit/Codium-ai/cover-agent/main?style=for-the-badge" height="20">
    </a>
</div>

## Table of Contents
- [Overview](#overview)
- [Installation and Usage](#installation-and-usage)
- [Roadmap](#roadmap)

# RAG Core-Agent
Welcome to RAG Core. This focused project utilizes Generative AI to automate and enhance the generation of transformed code, aiming to streamline development workflows. RAG Core-Agent can run via a terminal.
[![Test generation xxx](https://www.codium.ai/wp-content/uploads/2024/05/CodiumAI-CoverAgent-v240519-small-loop.gif)](https://youtu.be/fIYkSEJ4eqE?feature=shared)

## Overview
This tool is designed to automate the transformation and generation of code for software projects. Utilizing advanced Generative AI models, it aims to simplify and expedite the transformation and testing process, ensuring high-quality software development. The system comprises several components:
1. **Prompt Builder:** Gathers necessary data from the codebase and constructs the prompt to be passed to the Large Language Model (LLM).
2. **AI Caller:** Interacts with the LLM to generate tests based on the prompt provided.

## Installation and Usage
### Requirements
Before you begin, make sure you have the following:
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` & `AWS_REGION_NAME` set in your environment variables, which is required for calling Bedrock.

If running directly from the repository you will also need:
- Python installed on your system.
- Poetry installed for managing Python package dependencies. Installation instructions for Poetry can be found at [https://python-poetry.org/docs/](https://python-poetry.org/docs/).

### Standalone Runtime
The RAG Core can be installed as a Python Pip package or run as a standalone executable.

#### Python Pip
To install the Python Pip package directly via GitHub run the following command:
```
pip install git+gitlink 
```

### Repository Setup
Run the following command to install all the dependencies and run the project from source:
```shell
poetry install
```

### Adding a Use Case
To add a new use case, create a new prompt in the settings folder as a .toml file. Ensure the title at the top of the .toml file matches the filename (excluding .toml). This filename becomes the new use case command. Replace or add variables within the prompt using the desired variables from the Python environment, such as {{ source_file_name }}.

### Running the Code
After downloading the executable or installing the Pip package you can run the Cover Agent to generate and validate unit tests. Execute it from the command line by using the following command:
```shell
cover-agent \
  --source-file-path "<path_to_source_file>" \
  --output-file-path "<path_to_test_file>" \
  --usecase-command "<path_to_coverage_report>" \
  --language "<test_command_to_run>" \
  --model "<directory_to_run_test_command>" \
  --api-base "<type_of_coverage_report>" \
  --included-files "<optional_list_of_files_to_include>"
  --additional-instructions <desired_coverage_between_0_and_100> \
  --max-iterations <max_number_of_llm_iterations> \
  --report-filepath <max_number_of_llm_iterations> \
  
```

You can use the example code below to try out the RAG Core Agent.

#### Python

Run the following command to transform Python 2 code to Python 3 code as an example:
```shell
cover-agent \
  --source-file-path "templated_tests/app.py" \
  --output-file-path "templated_tests/converted_app.py" \
  --usecase-command "py2_3"
```

### Outputs
A new transformed file will be outputted locally within the repository at the specified directory location.


### Using other LLMs
This project uses LiteLLM to communicate with OpenAI and other hosted LLMs (supporting 100+ LLMs to date). To use a different model other than the OpenAI default you'll need to:
1. Export any environment variables needed by the supported LLM [following the LiteLLM instructions](https://litellm.vercel.app/docs/proxy/quick_start#supported-llms).
2. Call the name of the model using the `--model` option when calling RAG Core Agent.

For example (as found in the [LiteLLM Quick Start guide](https://litellm.vercel.app/docs/proxy/quick_start#supported-llms)):
```shell
export VERTEX_PROJECT="hardy-project"
export VERTEX_LOCATION="us-west"

cover-agent \
  ...
  --model "anthropic.claude-3-sonnet-20240229-v1:0"
```

#### OpenAI Compatible Endpoint
```shell
export OPENAI_API_KEY="<your api key>" # If <your-api-base> requires an API KEY, set this value.

cover-agent \
  ...
  --model "openai/<your model name>" \
  --api-base "<your-api-base>"
```


## Development
This section discusses the development of this project.

## Roadmap
Below is the roadmap of planned features, with the current implementation status:

- [x] Use models from Bedrock
- [ ] Improve usability

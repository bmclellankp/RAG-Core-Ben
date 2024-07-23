import logging
import os

from jinja2 import Environment, StrictUndefined

from rag_core.settings.config_loader import get_settings

MAX_TESTS_PER_RUN = 4

# Markdown text used as conditional appends
ADDITIONAL_INCLUDES_TEXT = """
## Additional Includes
The following is a set of included files used as context for the source code above. This is usually included libraries needed as context to write better tests:
======
{included_files}
======
"""

ADDITIONAL_INSTRUCTIONS_TEXT = """
## Additional Instructions
======
{additional_instructions}
======
"""

FAILED_TESTS_TEXT = """
## Previous Iterations Failed Tests
Below is a list of failed tests that you generated in previous iterations. Do not generate the same tests again, and take the failed tests into account when generating new tests.
======
{failed_test_runs}
======
"""


class PromptBuilder:
    def __init__(
        self,
        source_file_path: str,
        included_files: str = "",
        additional_instructions: str = "",
        language: str = "python",
    ):
        """
        The `PromptBuilder` class is responsible for building a formatted prompt string by replacing placeholders with the actual content of files read during initialization. It takes in various paths and settings as parameters and provides a method to generate the prompt.

        Attributes:
            prompt_template (str): The content of the prompt template file.
            source_file (str): The content of the source file.
            test_file (str): The content of the test file.
            code_coverage_report (str): The code coverage report.
            included_files (str): The formatted additional includes section.
            additional_instructions (str): The formatted additional instructions section.
            failed_test_runs (str): The formatted failed test runs section.
            language (str): The programming language of the source and test files.

        Methods:
            __init__(self, prompt_template_path: str, source_file_path: str, test_file_path: str, code_coverage_report: str, included_files: str = "", additional_instructions: str = "", failed_test_runs: str = "")
                Initializes the `PromptBuilder` object with the provided paths and settings.

            _read_file(self, file_path)
                Helper method to read the content of a file.

            build_prompt(self)
                Replaces placeholders with the actual content of files read during initialization and returns the formatted prompt string.
        """
        self.source_file_name = os.path.basename(source_file_path)
        self.source_file = self._read_file(source_file_path)
        self.language = language

        # Conditionally fill in optional sections
        self.included_files = (
            ADDITIONAL_INCLUDES_TEXT.format(included_files=included_files)
            if included_files
            else ""
        )
        self.additional_instructions = (
            ADDITIONAL_INSTRUCTIONS_TEXT.format(
                additional_instructions=additional_instructions
            )
            if additional_instructions
            else ""
        )

    def _read_file(self, file_path):
        """
        Helper method to read file contents.

        Parameters:
            file_path (str): Path to the file to be read.

        Returns:
            str: The content of the file.
        """
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading {file_path}: {e}"

    def build_prompt_custom(self, file) -> dict:
        variables = {
            "source_file_name": self.source_file_name,
            "source_file": self.source_file,
            "additional_includes_section": self.included_files,
            "additional_instructions_text": self.additional_instructions,
            "language": self.language,
            "max_tests": MAX_TESTS_PER_RUN,
        }
        print(file)
        environment = Environment(undefined=StrictUndefined)
        try:
            system_prompt = environment.from_string(
                get_settings().get(file).system
            ).render(variables)
            user_prompt = environment.from_string(get_settings().get(file).user).render(
                variables
            )
            print(user_prompt)
            print(system_prompt)
        except Exception as e:
            logging.error(f"Error rendering prompt: {e}")
            return {"system": "", "user": ""}

        return {"system": system_prompt, "user": user_prompt}

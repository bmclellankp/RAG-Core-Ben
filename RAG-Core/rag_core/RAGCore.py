import re
import os 

from rag_core.PromptBuilder import PromptBuilder
from rag_core.AICaller import AICaller
from rag_core.FilePreprocessor import FilePreprocessor
from rag_core.utils import load_yaml
from rag_core.settings.config_loader import get_settings


class RAGCore:
    def __init__(self, args):
        """
        Initialize the UnitTestGenerator class with the provided parameters.

        Parameters:
            source_file_path (str): The path to the source file being tested.
            output_file_path (str): The path to the output file where generated code will be written.
            usecase_command (str): The command to run the app based on the desired usecase.
            llm_model (str): The language model to be used for test generation.
            api_base (str, optional): The base API url to use in case model is set to Ollama or Hugging Face. Defaults to an empty string.
            included_files (list, optional): A list of paths to included files. Defaults to None.
            additional_instructions (str, optional): Additional instructions for test generation. Defaults to an empty string.

        Returns:
            None
        """
        self.source_file_path=args.source_file_path
        self.output_file_path=args.output_file_path
        self.usecase_command=args.usecase_command
        if args.language:
            self.language=args.language
        else:
            self.language = self.get_code_language(self.source_file_path)
        self.llm_model=args.model
        self.api_base=args.api_base
        self.included_files=self.get_included_files(args.included_files)
        self.additional_instructions=args.additional_instructions 

        # Objects to instantiate
        self.ai_caller = AICaller(model=self.llm_model, api_base=self.api_base)

        # States to maintain within this class
        self.preprocessor = FilePreprocessor(self.output_file_path)
        self.total_input_token_count = 0
        self.total_output_token_count = 0

    def _validate_paths(self):
        if not os.path.isfile(self.source_file_path):
            raise FileNotFoundError(
                f"Source file not found at {self.source_file_path}"
            )

    def get_code_language(self, source_file_path):
        """
        Get the programming language based on the file extension of the provided source file path.

        Parameters:
            source_file_path (str): The path to the source file for which the programming language needs to be determined.

        Returns:
            str: The programming language inferred from the file extension of the provided source file path. Defaults to 'unknown' if the language cannot be determined.
        """
        # Retrieve the mapping of languages to their file extensions from settings
        language_extension_map_org = get_settings().language_extension_map_org

        # Initialize a dictionary to map file extensions to their corresponding languages
        extension_to_language = {}

        # Populate the extension_to_language dictionary
        for language, extensions in language_extension_map_org.items():
            for ext in extensions:
                extension_to_language[ext] = language

        # Extract the file extension from the source file path
        extension_s = "." + str(source_file_path).rsplit(".")[-1]

        # Initialize the default language name as 'unknown'
        language_name = "unknown"

        # Check if the extracted file extension is in the dictionary
        if extension_s and (extension_s in extension_to_language):
            # Set the language name based on the file extension
            language_name = extension_to_language[extension_s]

        # Return the language name in lowercase
        return language_name.lower()

    @staticmethod
    def get_included_files(included_files):
        """
        A method to read and concatenate the contents of included files into a single string.

        Parameters:
            included_files (list): A list of paths to included files.

        Returns:
            str: A string containing the concatenated contents of the included files, or an empty string if the input list is empty.
        """
        if included_files:
            included_files_content = []
            file_names = []
            for file_path in included_files:
                try:
                    with open(file_path, "r") as file:
                        included_files_content.append(file.read())
                        file_names.append(file_path)
                except IOError as e:
                    print(f"Error reading file {file_path}: {str(e)}")
            out_str = ""
            if included_files_content:
                for i, content in enumerate(included_files_content):
                    out_str += (
                        f"file_path: `{file_names[i]}`\ncontent:\n```\n{content}\n```\n"
                    )

            return out_str.strip()
        return ""

    def build_prompt(self):
        """
        Builds a prompt using the provided information to be used for a given usecase.

        Returns:
            str: The generated prompt to be used for code generation.
        """
        # Call PromptBuilder to build the prompt
        self.prompt_builder = PromptBuilder(
            source_file_path=self.source_file_path,
            included_files=self.included_files,
            additional_instructions=self.additional_instructions,
            language=self.language
        )
        return self.prompt_builder.build_prompt_custom(file = self.usecase_command)

    def perform_action(self, max_tokens=4096, dry_run=False):
        """
        Generate code using the AI model based on the constructed prompt.

        Parameters:
            max_tokens (int, optional): The maximum number of tokens to use for generating tests. Defaults to 4096.
            dry_run (bool, optional): A flag indicating whether to perform a dry run without calling the AI model. Defaults to False.

        Raises:
            Exception: If there is an error during code generation, such as a parsing error while processing the AI model response.
        """
        self.prompt = self.build_prompt()

        if dry_run:
            response = "```def test_something():\n    pass```\n```def test_something_else():\n    pass```\n```def test_something_different():\n    pass```"
        else:
            response, prompt_token_count, response_token_count = (
                self.ai_caller.call_model(prompt=self.prompt, max_tokens=max_tokens)
            )
            self.total_input_token_count += prompt_token_count
            self.total_output_token_count += response_token_count
        try:
            # Write the response to a new .py file at self.output_file_path
            with open(self.output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(response)
        except Exception as e:
            print(f"Error writing response to file: {e}")

def extract_error_message_python(fail_message):
    """
    Extracts and returns the error message from the provided failure message.

    Parameters:
        fail_message (str): The failure message containing the error message to be extracted.

    Returns:
        str: The extracted error message from the failure message, or an empty string if no error message is found.

    """
    try:
        # Define a regular expression pattern to match the error message
        MAX_LINES = 20
        pattern = r"={3,} FAILURES ={3,}(.*?)(={3,}|$)"
        match = re.search(pattern, fail_message, re.DOTALL)
        if match:
            err_str = match.group(1).strip("\n")
            err_str_lines = err_str.split("\n")
            if len(err_str_lines) > MAX_LINES:
                # show last MAX_lines lines
                err_str = "...\n" + "\n".join(err_str_lines[-MAX_LINES:])
            return err_str
        return ""
    except Exception as e:
        print(f"Error extracting error message: {e}")
        return ""

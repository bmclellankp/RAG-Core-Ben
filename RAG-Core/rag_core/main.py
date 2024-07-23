import argparse
import os
from rag_core.RAGCore import RAGCore
from rag_core.version import __version__
from rag_core.Context import Context

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description=f"Cover Agent v{__version__}")
    parser.add_argument(
        "--source-file-path", required=True, help="Path to the source file."
    )
    parser.add_argument(
        "--output-file-path", required=True, help="Path to the output file."
    )
    parser.add_argument(
        "--usecase-command",
        required=True,
        help="The command to decide usecase e.g. py2_3, UnitTest etc..",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="The language of the source file e.g. python, java"
    )
    parser.add_argument(
        "--model",
        default="anthropic.claude-3-sonnet-20240229-v1:0",
        help="Which LLM model to use. Default: %(default)s.",
    )
    parser.add_argument(
        "--api-base",
        default="http://localhost:11434",
        help="The API url to use for Ollama or Hugging Face. Default: %(default)s.",
    )
    parser.add_argument(
        "--included-files",
        default=None,
        nargs="*",
        help='List of files to include. For example, "--included-files library1.c library2.c." Default: %(default)s.',
    )
    parser.add_argument(
        "--additional-instructions",
        default="",
        help="Any additional instructions you wish to append at the end of the prompt. Default: %(default)s.",
    )
    parser.add_argument(
        "--report-filepath",
        default="test_results.html",
        help="Path to the output report file. Default: %(default)s.",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    agent = RAGCore(args)
    agent.perform_action()

if __name__ == "__main__":
    main()

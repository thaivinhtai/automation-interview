#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Framework executor.
"""

from sys import path
from pathlib import Path


def main() -> None:
    """Main Function"""

    # Import custom library
    from framework_modules import (
        ARGUMENTS, set_python_path_env_var, generate_docs, execute_test_cases
    )

    # Add workspace directory to PYTHON_PATH, thus the RobotFramework can
    # recognize our custom libs
    set_python_path_env_var()

    # Generate documents and sign the sequence of test cases to be executed
    if ARGUMENTS.gen_doc:
        return generate_docs()

    # Run test cases in normal environment
    execute_test_cases()


if __name__ == "__main__":
    # Add workspace to python path, mark it as an Python lib
    path.append(str(Path(__file__).parent.absolute()))
    # run main engine
    main()

# [V4] UNIT TESTING | ADD UNIT TESTS WITH PYTEST

## TODO

- [x] 1. Add the libraries to write unit tests with Python:
  - [x] pytest
  - [x] Mock: https://docs.python.org/3/library/unittest.mock.html
- [x] 2. Choose a test naming convention
- [x] 3. Create a directory for test files
- [x] 4. Write test cases
- [x] 5. Mock dependencies (if needed)
- [x] 6. Run the tests
- [x] 7. Analyze test results
- [ ] 8. Continuous Integration and Test Automation (optional)
- [x] 9. Refactor and improve


## Introduction

Unit testing is an essential practice in software development that helps ensure the correctness and reliability of individual units or components of a codebase. In this task, we will be adding unit tests to our Python project using the pytest testing framework.

## Prerequisites

Before proceeding, ensure that you have the following prerequisites installed:

- Python (version 3.6 or later)
- pip (Python package installer)

## Tasks

1. **Install pytest and mock libraries:**
   - Open your terminal or command prompt.
   - Navigate to your project directory.
   - Run the following command to install pytest and mock:
     ```
     pip install pytest mock
     ```

2. **Choose a test naming convention:**
   - Define a convention for naming test files and test functions.
   - A common convention is to prefix test files with `test_` (e.g., `test_module.py`) and test functions with `test_` (e.g., `test_function_name`).
   - This convention helps distinguish test code from production code and makes it easier to identify and run tests.

3. **Create a directory for test files:**
   - Create a new directory in your project root, typically named `tests`.
   - This directory will contain all your test files.

4. **Write test cases:**
   - Create a new Python file in the `tests` directory for each module or class you want to test.
   - Import the necessary modules or classes from your production code.
   - Define test functions using the `test_` prefix and the appropriate naming convention.
   - Within each test function, use pytest's assertion methods (e.g., `assert`, `assertEqual`, `assertTrue`) to verify the expected behavior of the code under test.
   - Consider testing different scenarios, including edge cases and error handling.

5. **Mock dependencies (if needed):**
   - If your code has external dependencies (e.g., APIs, databases, file systems), consider mocking them using the `mock` library.
   - Mocking allows you to isolate the code under test from its dependencies, making the tests more reliable and faster.
   - Import the `mock` library and use its functionality to create mock objects and patch dependencies.

6. **Run the tests:**
   - Open your terminal or command prompt.
   - Navigate to your project directory.
   - Run the following command to execute all tests in the `tests` directory:
     ```
     pytest tests/
     ```
   - Pytest will automatically discover and run all test files and functions within the specified directory.

7. **Analyze test results:**
   - Pytest will display the test results in the terminal, indicating which tests passed and which failed.
   - If any tests fail, pytest will provide detailed information about the failure, including the test function name, the line of code that caused the failure, and the expected and actual values.

8. **Continuous Integration and Test Automation:**
   - Consider integrating your unit tests with a Continuous Integration (CI) system, such as Travis CI, CircleCI, or GitHub Actions.
   - CI systems can automatically run your tests whenever changes are pushed to your code repository, ensuring that your codebase remains stable and reliable.

9. **Refactor and improve:**
   - Regularly review and refactor your test code to improve readability, maintainability, and performance.
   - Add more tests to cover new features or edge cases as your codebase evolves.
   - Consider implementing test-driven development (TDD) practices to write tests before implementing the actual code.

By following these steps, you will have a solid foundation for unit testing in your Python project using pytest. Unit tests will help catch bugs early, ensure code correctness, and facilitate refactoring and maintenance of your codebase.
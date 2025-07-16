# 0x03. Unittests and Integration Tests

## 📚 Project Overview

This project covers the core concepts and practical skills of **unit testing** and **integration testing** in Python. You will learn to:
- Write clear, maintainable unit tests for functions using `unittest`
- Use advanced testing features such as **parameterized tests**, **mocking**, and **fixtures**
- Understand and implement integration tests that cover the end-to-end logic of your code
- Distinguish clearly between unit and integration testing approaches

All tests are written to check the logic of utility functions for GitHub org clients, focusing on input/output correctness, edge cases, and reliability.

---

## 🛠️ Project Structure

0x03-Unittests_and_integration_tests/
│
├── test_utils.py # Unit tests for utils.py functions
├── fixtures.py # Test fixtures and payloads for integration tests
├── utils.py # Utility functions to be tested
├── client.py # GithubOrgClient class to be tested
├── ...


---

## 🔬 Learning Objectives

By the end of this project, you will be able to:
- Explain the difference between **unit** and **integration** tests
- Use Python's `unittest` framework for robust test coverage
- Apply parameterization to avoid code repetition
- Use `mock` to isolate tests from external dependencies
- Structure your code to maximize testability and maintainability

---

## ⚡️ Getting Started

### Prerequisites

- Python 3.7+ (Recommended: Ubuntu 18.04 with Python 3.7)
- `requests` and `parameterized` libraries (install via pip)
- All code and tests should be in the appropriate project folders

### Running Tests

From the root of your repo, run:

```bash
python3 -m unittest 0x03-Unittests_and_integration_tests/test_utils.py

📄 File Descriptions
File	Description
utils.py	Utility functions for nested map access, etc.
client.py	GithubOrgClient with repo/org methods
test_utils.py	Unittest class for testing utility functions
fixtures.py	Sample data used in integration tests

👨🏽‍💻 Author
Your Jacob N
ALX Software Engineering Student

🏷️ License
This project is part of the ALX Africa curriculum.
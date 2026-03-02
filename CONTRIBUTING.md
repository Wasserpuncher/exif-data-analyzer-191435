# Contributing to EXIF Data Analyzer

We welcome contributions to the EXIF Data Analyzer project! Your help is valuable in making this tool even better. Please take a moment to review this document to understand how to contribute effectively.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Code Contributions](#code-contributions)
- [Development Setup](#development-setup)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Coding Style](#coding-style)

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project, you agree to abide by its terms. Please be respectful and considerate towards other contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on the [GitHub Issues page](https://github.com/your-username/exif-data-analyzer/issues).
When reporting a bug, please include:
- A clear and concise description of the bug.
- Steps to reproduce the behavior.
- Expected behavior.
- Screenshots or error messages if applicable.
- Your operating system and Python version.

### Suggesting Enhancements

We're always looking for ways to improve the tool. If you have an idea for a new feature or an improvement to an existing one, please open an issue on the [GitHub Issues page](https://github.com/your-username/exif-data-analyzer/issues).
When suggesting an enhancement, please include:
- A clear and concise description of the suggested enhancement.
- Why you think it would be valuable.
- Any potential alternatives or considerations.

### Code Contributions

We welcome code contributions! If you'd like to contribute code, please follow the [Pull Request Guidelines](#pull-request-guidelines).

## Development Setup

1.  **Fork the repository**: Click the "Fork" button on the top right of the [GitHub repository page](https://github.com/your-username/exif-data-analyzer).
2.  **Clone your forked repository**:
    ```bash
    git clone https://github.com/your-username/exif-data-analyzer.git
    cd exif-data-analyzer
    ```
3.  **Add the upstream remote**:
    ```bash
    git remote add upstream https://github.com/original-owner/exif-data-analyzer.git
    ```
4.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
5.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Pull Request Guidelines

1.  **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name-or-bugfix/issue-number
    ```
    (Choose a descriptive name for your branch.)

2.  **Make your changes**: Implement your feature or fix the bug.
    - Ensure your code adheres to the [Coding Style](#coding-style).
    - Add or update unit tests for your changes in `test_main.py`.
    - Update documentation (`README.md`, `README_de.md`, docstrings) if necessary.

3.  **Run tests**: Before committing, ensure all tests pass.
    ```bash
    pytest
    ```

4.  **Commit your changes**: Write clear, concise commit messages.
    ```bash
    git commit -m "feat: Add new feature to extract X"
    git commit -m "fix: Resolve bug in Y when Z happens"
    ```
    (Refer to Conventional Commits for good practice, though not strictly enforced.)

5.  **Push your branch**:
    ```bash
    git push origin feature/your-feature-name
    ```

6.  **Open a Pull Request (PR)**:
    - Go to your forked repository on GitHub and click "Compare & pull request".
    - Provide a detailed description of your changes in the PR.
    - Reference any related issues (e.g., "Closes #123").

## Coding Style

-   Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
-   Use descriptive variable and function names.
-   Include type hints for function signatures.
-   Write clear docstrings for all classes, methods, and functions.
-   Ensure comments are bilingual (English/German) where appropriate, especially in core logic (`main.py`, `test_main.py`).
-   Keep functions and methods small and focused.
-   Prioritize readability and maintainability.

# Frisor-Saxe

![Tests](https://github.com/NTIG-Uppsala/Frisor-Saxe/actions/workflows/tests.yml/badge.svg)

# The Project

In this project we are creating a website for a hairdresser company.

## [Link to website](https://ntig-uppsala.github.io/Frisor-Saxe/)

# Programming Languages
* HTML
* CSS
* Python
* JavaScript

# Code Validation
Code is automatically validated using a fork of Cyb3r-Jak3's HTML/CSS validator.

# Coding Standards
HTML/CSS: [W3Schools](https://www.w3schools.com/html/html5_syntax.asp)

Python: [PEP8](https://peps.python.org/pep-0008/)

JavaScript: [W3Schools](https://www.w3schools.com/js/js_conventions.asp)

# Development Environment
Windows 10

Visual Studio Code:
- Pylance
- Live Preview

Python installed via winget `winget install Python.Python.3.10`
- Python requirements: `pip install -r /tests/test_requirements.txt`

# Running Tests Locally
In order to run the tests locally without having to rely on GitHub actions you have to be in the root directory and run the following command: `python .\test\test.py http://127.0.0.1:3000/root/` whilst hosting a local preview with Live Preview.

# Definition of Done
- Unless everyone present has worked together, the remaining people must check the task before it can be considered done.
- Code must pass all relevant tests and code validation.
- Code must follow the coding standard.
- All documents and spreadsheets must be uploaded to Google Drive and all code must be uploaded to GitHub.  
- Task must be submitted to the presentation document if it is present in the backlog.
- Comment tricky code
- Branches shall be merged
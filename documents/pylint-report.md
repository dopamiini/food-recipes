# Pylint Report

**Code quality score:** 10.00/10

**Previous run:** 10.00/10

**Change:** +0.00

**Status:** All checks passed with a perfect score.

Pylint was run for all python project files. See [pylint-report.txt](pylint-report.txt) for details.

## Installing and Running Pylint
Pylint is a Python code analysis tool.

### 1. Install Pylint

In Windows, open PowerShell in the project directory. If the project uses a virtual environment, then activate it first:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install Pylint using pip:

```powershell
python -m pip install pylint
```

### 2. Run Pylint

To check a single Python file, such as `app.py`, run:

```powershell
python -m pylint app.py
```

To check all the main Python files in the project, run:

```powershell
python -m pylint app.py db.py recipes.py users.py config.py
```
or
```powershell
python -m pylint *.py
```

Pylint displays detected issues in the terminal, along with a code quality score.

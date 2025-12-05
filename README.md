# Advent of Code - Python

A modular Python framework for efficiently tackling Advent of Code challenges, designed for clarity, quality, and easy setup. The repository supports day-by-day workflows for solving, testing, and submitting solutions, with strong emphasis on reproducible results and consistent code standards.

## Tooling

- [**uv**](https://docs.astral.sh/uv/) for Python dependency management and virtual environments.

- [**direnv**](https://direnv.net/) to handle loading and unloading environment variables depending on the current directory.

- [**pre-commit**](https://pre-commit.com/#install) to enforce code quality on every commit with the following hooks:

   - [**ruff**](https://docs.astral.sh/ruff/) for fast formatting and linting.

   - [**mypy**](https://mypy.readthedocs.io/en/stable/) for static type checking.

All dependencies and tools are defined in `pyproject.toml` for deterministic environments.

## Project structure

```plaintext
.
├── _2022/                    # 2022 Advent of Code solutions
├── _2023/                    # 2023 Advent of Code solutions
├── _2024/                    # 2024 Advent of Code solutions
├── _2025/                    # 2025 Advent of Code solutions
│   ├── solutions/
│   │   ├── day01.py          # Solution for Day 1, 2025
│   │   ├── day02.py          # Solution for Day 2, 2025
│   │   └── ...
│   └── tests/
│       ├── data/
│       ├── __init__.py
│       ├── test_01.py        # Tests for Day 1, 2025
│       ├── test_02.py        # Tests for Day 2, 2025
│       └── ...
├── .github/
│   └── workflows/
│       └── ci.yml
├── aoc/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── authenticator.py   # Manages Advent of Code authentication credentials
│   │   ├── base.py            # Base class definitions for shared functionality
│   │   ├── file.py            # Handles file operations (e.g., input files, test files)
│   │   ├── reader.py          # Reads and parses input data for the solution
│   │   ├── submission.py      # Logic for submitting answers to AoC
│   │   └── tester.py          # Utilities for testing solutions
│   └── utils/
│       ├── __init__.py
│       └── initialise.py      # Utilities for initializing daily solution files
├── templates/
├── .gitignore
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── main.py                    # Main script to manage tasks and run solutions
├── pyproject.toml             # Project dependencies and configuration
├── README.md
└── uv.lock
```

- `aoc/`: Auth, input reading, submission, test/utility modules.

- `solutions/`: One file per Advent of Code day/year.

- `data/` and `tests/`: Daily inputs and unit test scaffolds.

- `main.py`: Command-line interface for all core actions.

## Setup Instructions

1. Install `uv` (if not already available):

   - Unix/macOS:

      ```bash
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```

   - Windows (PowerShell):

      ```bash
      irm https://astral.sh/uv/install.ps1 | iex
      ```

3. Install `direnv`:

   - macOS (using Homebrew):

      ```bash
      brew install direnv
      ```

   - Linux/Unix:

      ```bash
      # Ubuntu/Debian
      sudo apt install direnv

      # Fedora
      sudo dnf install direnv

      # Arch
      sudo pacman -S direnv
      ```

   - Windows:

      ```bash
      # Using Scoop
      scoop install direnv

      # Using Chocolatey
      choco install direnv
      ```

   After installation, add the hook to your shell configuration:

      - For bash (`~/.bashrc` or `~/.bash_profile`):

         ```bash
         eval "$(direnv hook bash)"
         ```

      - For zsh (`~/.zshrc`):

         ```bash
         eval "$(direnv hook zsh)"
         ```

      - For PowerShell (add to your profile):

         ```bash
         Invoke-Expression "$(direnv hook pwsh)"
         ```

   Restart your shell or source your config file after adding the hook.

2. Install project dependencies:

   ```bash
   uv sync --all-extras --dev
   ```

3. Set up pre-commit hooks:

   ```bash
   uv run pre-commit install
   ```

   Hooks will auto-run `ruff` and `mypy` checks before every commit.

## AoC session cookie

To download puzzle inputs and submit answers, you need to configure your Advent of Code session cookie:

1. Find your session cookie:

   - Go to [adventofcode.com](https://adventofcode.com/) and log in

   - Open your browser's Developer Tools:

      - Chrome/Edge/Brave: Right-click → "Inspect" or press `Ctrl+Shift+I` (`Cmd+Option+I` on Mac)

      - Firefox: Press `F12`

   - Navigate to the "Application" tab (Chrome/Edge) or "Storage" tab (Firefox)

   - Expand "Cookies" and select "https://adventofcode.com"

   - Find the cookie named session and copy its value

2. Create a `.envrc` file in the project root:

   ```plaintext
   export AOC_SESSION=your_session_cookie_value_here
   export GITHUB_USERNAME=github_user
   export GITHUB_USER_EMAIL=user@github.com
   ```

3. Allow `direnv` to load the environment variables:

   ```bash
   direnv allow .
   ```

The session cookie will now automatically load when you `cd` into the project directory. Make sure `.envrc` is in your `.gitignore` to keep your credentials private.

## Usage

- Help and available commands:

   ```bash
   uv run python main.py --help
   ```

- Scaffold a new day's solution and input:

   ```bash
   uv run python main.py --year <YEAR> --day <DAY> --add
   ```

- Validate a part using test input:

   ```bash
   # Add test data input
   uv run python main.py --year <YEAR> --day <DAY> --part <PART> --add-test-input

   # Add test suite boiler plate functions
   uv run python main.py --year <YEAR> --day <DAY> --part <PART> --add-test-file

   # Test solution for a specific day part
   uv run python main.py --year <YEAR> --day <DAY> --part <PART>
   ```

- Solve full puzzle input:

   ```bash
   uv run python main.py --year <YEAR> --day <DAY> --part <PART> --skip-test
   ```

- Submit your answer:

   ```bash
   uv run python main.py --year <YEAR> --day <DAY> --part <PART> --skip-test --submit
   ```

- Run all tests:

   ```bash
   # Run all tests in the entire repository
   uv run pytest

   # Run all tests for a specific year
   uv run pytest _202Y/

   # Run tests for a specific day
   uv run pytest _202Y/tests/test_DD.py
   ```

All core workflows utilize the CLI, and the testing framework is fully integrated.

## CI and code quality checks

GitHub Actions continuously check code quality on push/PR:

- **Formatting**: `uv run ruff format --check .`

- **Linting**: `uv run ruff check .`

- **Type checking**: `uv run mypy ...`

- **Tests**: `uv run pytest _202Y`

These match the checks enforced by local pre-commit.

## Acknowledgments

This project structure was inspired by nitekat1124's [Advent of Code repository](https://github.com/nitekat1124/advent-of-code-2023).

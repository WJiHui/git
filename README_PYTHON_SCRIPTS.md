# Git Repository Python Scripts

This directory contains Python scripts for analyzing and working with git repositories.

## Scripts

### 1. git_stats.py

A comprehensive tool for analyzing git repository statistics.

**Features:**
- Repository information (branch, remote URL, total commits)
- File analysis by extension and size
- Commit history analysis (contributors, activity)
- Repository status check

**Usage:**
```bash
python git_stats.py
```

**Example output:**
```
============================================================
Git Repository Statistics
============================================================
Current branch: dev
Remote URL: https://github.com/username/repo.git
Total commits: 42
Last commit: abc123 | John Doe | 2024-02-10 | Update README

============================================================
File Analysis
============================================================
Total tracked files: 15
Files by extension:
  .py: 8 files
  .txt: 3 files
  .md: 2 files
  .json: 1 file
  no_extension: 1 file
...
```

### 2. example_usage.py

Demonstration script showing how to use the git statistics tool and perform git operations.

**Features:**
- Demonstrates running git_stats.py
- Creates sample files for testing
- Shows git add/commit operations
- Provides cleanup instructions

**Usage:**
```bash
python example_usage.py
```

## Requirements

- Python 3.6+
- Git installed and available in PATH
- Access to a git repository

## Installation

No installation required. Just run the scripts from within a git repository.

## Examples

### Basic usage
```bash
cd /path/to/your/git/repo
python git_stats.py
```

### Run with example
```bash
cd /path/to/your/git/repo
python example_usage.py
```

## License

These scripts are provided as-is for educational and utility purposes.

## Author

Created by OpenHands Agent
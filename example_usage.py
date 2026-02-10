#!/usr/bin/env python3
"""
Example usage of git_stats.py
This script demonstrates how to use the git statistics tool.
"""

import subprocess
import sys


def run_script():
    """Run the git_stats.py script."""
    print("Running git repository statistics...")
    print("-" * 40)
    
    try:
        # Run the git_stats.py script
        result = subprocess.run(
            [sys.executable, "git_stats.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error running git_stats.py:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error: {e}")


def create_sample_files():
    """Create some sample files to demonstrate git operations."""
    print("\nCreating sample files for demonstration...")
    
    # Create a sample Python file
    with open("sample_script.py", "w") as f:
        f.write('''#!/usr/bin/env python3
"""
Sample Python script for demonstration.
"""

def hello_world():
    """Print a hello message."""
    print("Hello from the sample script!")

def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

if __name__ == "__main__":
    hello_world()
    result = calculate_sum(5, 3)
    print(f"5 + 3 = {result}")
''')
    
    # Create a sample configuration file
    with open("config.json", "w") as f:
        f.write('''{
    "project": "Git Statistics Demo",
    "version": "1.0.0",
    "author": "OpenHands Agent",
    "description": "Sample configuration file"
}
''')
    
    # Create a sample text file
    with open("notes.txt", "w") as f:
        f.write('''Git Repository Statistics Tool
===============================

This tool provides:
1. Repository information
2. File analysis by extension
3. Commit history analysis
4. Repository status check

Usage:
    python git_stats.py
''')
    
    print("Created sample files: sample_script.py, config.json, notes.txt")


def main():
    """Main function."""
    print("Git Statistics Tool - Example Usage")
    print("=" * 40)
    
    # Option 1: Run the statistics tool
    print("\nOption 1: Run git statistics tool")
    run_script()
    
    # Option 2: Create sample files and show git operations
    print("\n" + "=" * 40)
    print("Option 2: Demonstrate git operations")
    
    create_sample_files()
    
    # Show git status
    print("\nGit status after creating sample files:")
    subprocess.run(["git", "status", "--short"])
    
    # Add and commit the sample files
    print("\nAdding sample files to git...")
    subprocess.run(["git", "add", "sample_script.py", "config.json", "notes.txt"])
    
    print("\nCommitting sample files...")
    subprocess.run(["git", "commit", "-m", "Add sample files for demonstration"])
    
    # Run statistics again to show changes
    print("\n" + "=" * 40)
    print("Running git statistics after adding sample files:")
    run_script()
    
    print("\n" + "=" * 40)
    print("Example usage completed!")
    print("\nTo clean up, you can run:")
    print("  git reset HEAD~1  # Undo the last commit")
    print("  git checkout -- sample_script.py config.json notes.txt  # Discard changes")
    print("  rm sample_script.py config.json notes.txt  # Remove files")


if __name__ == "__main__":
    main()
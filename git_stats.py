#!/usr/bin/env python3
"""
Git Repository Statistics Script
This script analyzes a git repository and provides statistics about files and commits.
"""

import os
import sys
import subprocess
from datetime import datetime
from collections import Counter


def run_git_command(cmd):
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {cmd}")
        print(f"Error: {e.stderr}")
        return None


def get_repo_info():
    """Get basic repository information."""
    print("=" * 60)
    print("Git Repository Statistics")
    print("=" * 60)
    
    # Get current branch
    branch = run_git_command("git branch --show-current")
    print(f"Current branch: {branch}")
    
    # Get remote URL
    remote = run_git_command("git remote get-url origin")
    print(f"Remote URL: {remote}")
    
    # Get total commits
    commits = run_git_command("git rev-list --count HEAD")
    print(f"Total commits: {commits}")
    
    # Get last commit info
    last_commit = run_git_command("git log -1 --format='%H | %an | %ad | %s' --date=short")
    print(f"Last commit: {last_commit}")
    
    return branch, remote, commits


def analyze_files():
    """Analyze files in the repository."""
    print("\n" + "=" * 60)
    print("File Analysis")
    print("=" * 60)
    
    # Get all tracked files
    files = run_git_command("git ls-files")
    if not files:
        print("No tracked files found.")
        return
    
    file_list = files.split('\n')
    print(f"Total tracked files: {len(file_list)}")
    
    # Count files by extension
    extensions = Counter()
    for file in file_list:
        _, ext = os.path.splitext(file)
        if ext:
            extensions[ext] += 1
        else:
            extensions['no_extension'] += 1
    
    print("\nFiles by extension:")
    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext}: {count} files")
    
    # Get file sizes
    print("\nFile sizes (largest 10 files):")
    size_info = []
    for file in file_list:
        if os.path.exists(file):
            size = os.path.getsize(file)
            size_info.append((file, size))
    
    for file, size in sorted(size_info, key=lambda x: x[1], reverse=True)[:10]:
        size_kb = size / 1024
        print(f"  {file}: {size_kb:.2f} KB")
    
    return len(file_list)


def analyze_commits():
    """Analyze commit history."""
    print("\n" + "=" * 60)
    print("Commit Analysis")
    print("=" * 60)
    
    # Get commit authors
    authors = run_git_command("git shortlog -s -n HEAD")
    print("Top contributors:")
    if authors:
        print(authors)
    
    # Get commits per day (last 30 days)
    print("\nRecent commit activity (last 30 days):")
    dates = run_git_command("git log --since='30 days ago' --format='%ad' --date=short")
    if dates:
        date_list = dates.split('\n')
        date_counts = Counter(date_list)
        for date, count in sorted(date_counts.items(), reverse=True)[:10]:
            print(f"  {date}: {count} commits")
    
    # Get commit message lengths
    messages = run_git_command("git log --since='30 days ago' --format='%s'")
    if messages:
        msg_list = messages.split('\n')
        avg_len = sum(len(msg) for msg in msg_list) / len(msg_list)
        print(f"\nAverage commit message length (last 30 days): {avg_len:.1f} characters")


def check_git_status():
    """Check git status for any uncommitted changes."""
    print("\n" + "=" * 60)
    print("Repository Status")
    print("=" * 60)
    
    status = run_git_command("git status --porcelain")
    if status:
        print("Uncommitted changes found:")
        print(status)
        
        # Count changes
        lines = status.split('\n')
        staged = sum(1 for line in lines if line.startswith('M ') or line.startswith('A '))
        unstaged = sum(1 for line in lines if line.startswith(' M') or line.startswith('??'))
        print(f"\nStaged changes: {staged}")
        print(f"Unstaged changes: {unstaged}")
    else:
        print("Working directory is clean.")


def main():
    """Main function."""
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("Error: Not in a git repository.")
        print("Please run this script from within a git repository.")
        sys.exit(1)
    
    try:
        # Get repository info
        branch, remote, commits = get_repo_info()
        
        # Analyze files
        file_count = analyze_files()
        
        # Analyze commits
        analyze_commits()
        
        # Check status
        check_git_status()
        
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"Repository: {remote.split('/')[-1].replace('.git', '')}")
        print(f"Branch: {branch}")
        print(f"Total commits: {commits}")
        print(f"Total files: {file_count}")
        print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
import subprocess
import os
import re

diff_result = ""

def check_commit_exists(repo_path, commit):
    try:
        subprocess.run(['git', '-C', repo_path, 'cat-file', '-e', commit],
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_git_diff(repo_path, commit1, commit2):
    if not os.path.exists(repo_path):
        return f"Error: The specified repository path does not exist: {repo_path}"

    if not os.path.exists(os.path.join(repo_path, '.git')):
        return f"Error: The specified path is not a git repository: {repo_path}"

    if not check_commit_exists(repo_path, commit1):
        return f"Error: Commit not found: {commit1}"

    if not check_commit_exists(repo_path, commit2):
        return f"Error: Commit not found: {commit2}"

    try:
        result = subprocess.run(['git', '-C', repo_path, 'diff', commit1, commit2], 
                                capture_output=True, 
                                text=True, 
                                check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred while running git diff: {e.stderr}"

def format_diff(diff_output):
    files = result.split(r'diff --git', diff_output)[1:]  # Split by file, ignore the first empty part
    formatted_output = ""

    for file_diff in files:
        lines = file_diff.split('\n')
        file_name = lines[0].split()[-1].lstrip('b/')
        
        # Find the start of the actual diff content
        diff_start = next(i for i, line in enumerate(lines) if line.startswith('@@'))
        
        # Extract added lines and count total changes
        added_lines = [line[1:] for line in lines[diff_start:] if line.startswith('+') and not line.startswith('+++')]
        total_changes = sum(1 for line in lines[diff_start:] if line.startswith(('+', '-')) and not line.startswith(('+++ b', '--- a')))
        print(f"total_changes{total_changes}")
        if added_lines:
            formatted_output += f"# {file_name}: {total_changes} change{'s' if total_changes > 1 else ''}\n"
            formatted_output += '\n'.join(added_lines) + '\n\n'
    print("**************")
    print(formatted_output.strip())
    print("**************")
    return formatted_output.strip()

if __name__ == "__main__":
    repo_path = "/path/to/your/repo"
    commit1 = "abc123"  # Replace with actual commit SHA
    commit2 = "def456"  # Replace with actual commit SHA
    
    diff = get_git_diff(repo_path, commit1, commit2)
    formatted_diff = format_diff(diff)
    diff_result = formatted_diff
    print(diff_result)

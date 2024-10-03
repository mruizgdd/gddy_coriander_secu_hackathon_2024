import subprocess
import os
import sys

def check_commit_exists(repo_path, commit):
    try:
        result = subprocess.run(['git', '-C', repo_path, 'rev-parse', '--verify', commit],
                                check=True, capture_output=True, text=True)
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
    files = diff_output.split('diff --git')[1:]  # Split by file, ignore the first empty part
    formatted_output = ""
    for file_diff in files:
        lines = file_diff.split('\n')
        file_name = lines[0].split()[-1].lstrip('b/')
        
        # Find the start of the actual diff content
        diff_start = next(i for i, line in enumerate(lines) if line.startswith('@@'))
        
        # Extract added lines and count total changes
        added_lines = [line[1:] for line in lines[diff_start:] if line.startswith('+') and not line.startswith('+++')]
        total_changes = sum(1 for line in lines[diff_start:] if line.startswith(('+', '-')) and not line.startswith(('+++ b', '--- a')))
        
        if added_lines:
            formatted_output += f"# {file_name}: {total_changes} change{'s' if total_changes > 1 else ''}\n"
            formatted_output += '\n'.join(added_lines) + '\n\n'
    
    return formatted_output.strip()

# Get the PR base and head SHAs
pr_base_sha = sys.argv[1]
pr_head_sha = sys.argv[2]
repo_path = os.getcwd()
diff = get_git_diff(repo_path, pr_base_sha, pr_head_sha)
diff_result = format_diff(diff)
with open('diff_result.txt', 'w') as f:
    f.write(str(diff_result))

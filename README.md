# Security Check GitHub Action Requirements

This document outlines the necessary requirements and setup for the Security Check GitHub Action. This action performs a security analysis on pull requests by checking the git diff and identifying potential security issues.

## Overview

The Security Check Action analyzes the changes in each new pull request, looking for potential security vulnerabilities. If issues are found, the action will display them and cause the PR checks to fail, preventing merging until the issues are addressed.

## Requirements

### 1. Branch Protection Rule

A branch protection rule must be set up for your main branch (usually `main` or `master`) with the following setting enabled:

- **Require status checks to pass before merging**

This ensures that pull requests cannot be merged until the security check passes.

#### How to Set Up:

1. Go to your repository on GitHub
2. Click on "Settings" at the top of the repository page
3. In the left sidebar, click on "Branches"
4. Under "Branch protection rules", click on "Add rule"
5. In the "Branch name pattern" field, enter your main branch name (e.g., `main` or `master`)
6. Check the box next to "Require status checks to pass before merging"
7. In the search box that appears, find and select the name of the security check status
8. Scroll down and click "Create" or "Save changes"

### 2. GitHub Secret: CORIANDER_TOKEN

A GitHub secret named `CORIANDER_TOKEN` must be set up in your repository. This token should be a GitHub Personal Access Token (Classic) with the following permission:

- `project - read:project`

#### How to Set Up:

1. Generate a Personal Access Token (Classic):
   - Go to your GitHub account settings
   - Click on "Developer settings" > "Personal access tokens" > "Tokens (classic)"
   - Click "Generate new token (classic)"
   - Give it a descriptive name
   - Select the `project - read:project` permission
   - Click "Generate token" and copy the token

2. Add the token as a repository secret:
   - Go to your repository on GitHub
   - Click on "Settings" > "Secrets and variables" > "Actions"
   - Click "New repository secret"
   - Name: `CORIANDER_TOKEN`
   - Value: Paste the Personal Access Token you generated
   - Click "Add secret"

### 3. GitHub Action Workflow File

A GitHub Action workflow file must be created in your repository with the content from:

`gddy_coriander_secu_hackathon_2024/Prompts/Prompt.txt`

This file should be committed and merged into your main branch.

#### How to Set Up:

1. Obtain the content from `gddy_coriander_secu_hackathon_2024/Prompts/Prompt.txt`
2. In your repository, create a new file: `.github/workflows/security-check.yml`
3. Paste the content into this new file
4. Commit the file directly to your main branch or create a pull request to merge it

## Verification

After setting up these requirements:

1. Create a new pull request to test the action
2. Verify that the security check runs automatically
3. Check that the "Merge" button is disabled if the security check fails
4. Ensure that the action is using the `CORIANDER_TOKEN` secret correctly

## Troubleshooting

If the action is not working as expected:

1. Check that all requirements above are correctly set up
2. Verify that the `CORIANDER_TOKEN` has the correct permissions
3. Ensure the workflow file is in the correct location and has valid YAML syntax
4. Review the Action logs for any error messages or issues

For further assistance, please contact the repository maintainer or refer to the GitHub Actions documentation.

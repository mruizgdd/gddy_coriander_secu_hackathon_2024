import json
import subprocess
import requests
import re

prompt = """
As a mobile security expert, please perform a comprehensive security analysis of the provided Android/iOS app code. Your analysis should focus on identifying potential security vulnerabilities, related to the following categories:

Categories:

* Insecure Data Storage: Look for sensitive data (e.g., personal information, authentication tokens) stored without proper encryption or protection mechanisms.
* Improper Input Validation: Check for inputs that are not properly sanitized, which could lead to injection attacks or crashes.
* Insecure Network Communication: Identify any use of non-secure protocols (e.g., HTTP instead of HTTPS) or weak SSL/TLS configurations.
* Hardcoded Secrets: Search for embedded API keys, passwords, or other sensitive information hardcoded into the app.
* Authentication and Authorization Flaws: Examine the authentication mechanisms for weaknesses and ensure proper authorization checks are in place.
* Use of Deprecated or Vulnerable APIs: Spot any reliance on outdated libraries or APIs known to have security issues.
* Insufficient Error Handling: Look for exceptions or errors that are not properly handled, potentially revealing stack traces or sensitive information.
* Weak Cryptography: Identify the use of weak encryption algorithms or improper cryptographic implementations.
* Permission Misconfigurations: Review the app's permissions to ensure they are necessary and not overly broad.

Instructions:

1. Identify and Describe Issues: For each security vulnerability found, provide a clear and concise description, including the affected code snippets or sections.
2. Assess Impact: Explain the potential risks and impact associated with each vulnerability.
3. Recommend Solutions: Offer practical recommendations or code fixes to address the identified issues.
4. Prioritize Findings: Rank the vulnerabilities based on their severity (e.g., critical, high, medium, low).

Output Format:

* Title: Brief title of the vulnerability.
* Description: Detailed explanation of the issue.
* Location: File names and line numbers where the issue is found.
* Impact: Potential consequences if the vulnerability is exploited.
* Recommendation: Steps or code changes required to fix the issue.
* Severity Level: Critical, High, Medium, or Low.


Output Format:

Please provide your findings in a markdown table with the following structure:

| 🏷️ Title | 📝 Description | 📍 Location | 💥 Impact | 🛠️ Recommendation | ⚠️ Severity Level |
|----------|---------------|------------|-----------|-------------------|-------------------|
| Brief title of the vulnerability | Detailed explanation of the issue. | File names and line numbers where the issue is found. | Potential consequences if the vulnerability is exploited. | Steps or code changes required to fix the issue. | 🚨 Critical/🔴 High/🟠 Medium/🟡 Low |
| Next vulnerability title | Detailed explanation of the next issue. | File names and line numbers where the next issue is found. | Potential consequences if the next vulnerability is exploited. | Steps or code changes required to fix the next issue. | 🚨 Critical/🔴 High/🟠 Medium/🟡 Low |

Issues Found Example:

| 🏷️ Title | 📝 Description | 📍 Location | 💥 Impact | 🛠️ Recommendation | ⚠️ Severity Level |
|----------|---------------|------------|-----------|-------------------|-------------------|
| SQL Injection in Login Form | The login form is vulnerable to SQL injection attacks due to unsanitized user input being directly concatenated into SQL queries. | auth.php, lines 45-52 | An attacker could bypass authentication, extract sensitive data from the database, or potentially gain full control of the database. | Use prepared statements or parameterized queries instead of string concatenation. Implement input validation and sanitization. | 🚨 Critical


No Issues Found Example:

✅ No Security Issues Were Found!

Use this framework to conduct a thorough security review of the app code, ensuring all potential vulnerabilities are identified and addressed, please DO NOT add any additional explainations or comments, ONLY answer using RAW markdown code depending on the case (Issues Found or No Issues Found).
Please only take in consideration code that is related to any of the categories above.


The next lines are the code to review:

"""

def extract_message(response):
    try:
        data = json.loads(response)
        return data['data']['value']['content']
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response: {e}")
        return None

def extract_chat_id(response):
    try:
        data = json.loads(response)
        return data['data']['id']
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response: {e}")
        return None


def remove_markdown_code_indicators(text):
    text = re.sub(r'^```(markdown)?[\s\n]*', '', text)
    text = re.sub(r'[\s\n]*```$', '', text)
    return text.strip()


# The token should be the last non-empty line
token =f"eyJhbGciOiAiUlMyNTYiLCAia2lkIjogIm5jZ1FmdFpJWncifQ.eyJhdXRoIjogImJhc2ljIiwgImZ0YyI6IDIsICJpYXQiOiAxNzI3OTY3Njc0LCAianRpIjogIktyX3J1MllxSDJsd0tiSVZQTkgyWVEiLCAidHlwIjogImpvbWF4IiwgInZhdCI6IDE3Mjc5Njc2NzQsICJmYWN0b3JzIjogeyJrX2ZlZCI6IDE3Mjc5Njc2NzQsICJwX29rdGEiOiAxNzI3OTY3Njc0fSwgImN0eCI6ICIiLCAiYWNjb3VudE5hbWUiOiAiZ2RpYXp2aWxsZWdhcyIsICJzdWIiOiAiNDM4MzQwIiwgInV0eXAiOiAxMDF9.Up28oAzgU73clTvxOlCssi-ri0iEDAU0jjyGMESfWc9CkZQSZ0WVzhFcwnOFopXivV8BbE6CL86MkH6wDmkKrbOy2cDWOCTS5aTRjhhoPJNilcIR3J2XVTmETSrb37hxnh011Grm-UuqBEfJQp_kH2NdFw-93LI_-XGOd3GUbA8MaudrtwSA6U2LRDMhKqgP0Z8aElCU-DOxgTSPBlm4IEBJPF45FZh-fK6zr9eD3djJqnXFqo8-oKJOwXv5tUo34dwA8Lahi5RJUqaA2kbvHZozpXmbE7ytVIIhXi_O0z-svAwZ08NxR8SyeU5KaMJV1OKhOu_PX_NZxBIoz5iVSQ"
with open('diff_result.txt', 'r') as file:
    diff_result = file.read()
url = 'https://caas.api.godaddy.com/v1/threads'
headers = {
    'Authorization': f"sso-jwt {token}",
    'accept': 'application/json',
    'Content-Type': 'application/json'
}


data = {
    "description": "",
    "isPrivate": "false",
    "messages":
    [
        {
            "content": f"{prompt}\n{diff_result}",
            "from": "user"
        }
    ],
    "name": "mobile security expert",
    "protected": "author",
    "provider": "openai_chat",
    "providerOptions":
    {
        "frequency_penalty": 0,
        "max_tokens": 4096,
        "model": "gpt-4o",
        "presence_penalty": 0,
        "temperature": 0.7,
        "top_p": 1
    }
}


response = requests.post(url, headers=headers, json=data)
json_message = f"{response.text}"
chat_id = extract_chat_id(json_message)


data = {
    "isTemplate": "false",
    "moderation":
    {
        "moderate": "true",
        "moderatePrompt": "true",
        "moderateTemplate": "true",
        "provider": "openai"
    },
    "privacy":
    {
        "enabled": "detect",
        "threshold": 0.5
    },
    "providerOptions":
    {
        "frequency_penalty": 0,
        "max_tokens": 4096,
        "model": "gpt-4o",
        "presence_penalty": 0,
        "temperature": 0.7,
        "top_p": 1
    }
}

get_url = f"{url}/{chat_id}"
chat_response = requests.post(get_url, headers=headers, json=data)
chat_response_json = f"{chat_response.text}"



message = extract_message(chat_response_json)
trimmed_message = remove_markdown_code_indicators(message)
print(trimmed_message)
with open('result.txt', 'w') as file:
    file.write(str(trimmed_message))

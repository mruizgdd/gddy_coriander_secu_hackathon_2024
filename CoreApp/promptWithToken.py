import json
import re
import requests
import argparse

PROMPT = """
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

class ProviderOptions:
    def __init__(self, frequency_penalty=0, max_tokens=4096, model="gpt-4o", 
                 presence_penalty=0, temperature=0.7, top_p=1):
        self.frequency_penalty = frequency_penalty
        self.max_tokens = max_tokens
        self.model = model
        self.presence_penalty = presence_penalty
        self.temperature = temperature
        self.top_p = top_p

    def to_dict(self):
        return {
            "frequency_penalty": self.frequency_penalty,
            "max_tokens": self.max_tokens,
            "model": self.model,
            "presence_penalty": self.presence_penalty,
            "temperature": self.temperature,
            "top_p": self.top_p
        }

def get_headers(secret_token):
    return {
        'Authorization': f"sso-jwt {secret_token}",
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

# Helper functions
def extract_json_data(response, key):
    try:
        data = json.loads(response)
        return data['data'][key]
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response: {e}")
        return None

def remove_markdown_code_indicators(text):
    text = re.sub(r'^```(markdown)?[\s\n]*', '', text)
    text = re.sub(r'[\s\n]*```$', '', text)
    return text.strip()

# Main functionality
def create_chat_thread(url, headers, prompt, diff_result):
    provider_options = ProviderOptions()  # Using default values
    data = {
        "description": "",
        "isPrivate": "false",
        "messages": [{"content": f"{prompt}\n{diff_result}", "from": "user"}],
        "name": "mobile security expert",
        "protected": "author",
        "provider": "openai_chat",
        "providerOptions": provider_options.to_dict()
    }
    response = requests.post(url, headers=headers, json=data)
    return extract_json_data(response.text, 'id')

def get_chat_response(url, headers, chat_id):
    provider_options = ProviderOptions()  # Using default values
    data = {
        "isTemplate": "false",
        "moderation": {
            "moderate": "true",
            "moderatePrompt": "true",
            "moderateTemplate": "true",
            "provider": "openai"
        },
        "privacy": {
            "enabled": "detect",
            "threshold": 0.5
        },
        "providerOptions": provider_options.to_dict()
    }
    get_url = f"{url}/{chat_id}"
    response = requests.post(get_url, headers=headers, json=data)
    return extract_json_data(response.text, 'value')['content']

def main(secret_token):
    url = 'https://caas.api.godaddy.com/v1/threads'
    headers = get_headers(secret_token)

    with open('diff_result.txt', 'r') as file:
        diff_result = file.read()

    chat_id = create_chat_thread(url, headers, PROMPT, diff_result)
    if chat_id:
        message = get_chat_response(url, headers, chat_id)
        if message:
            trimmed_message = remove_markdown_code_indicators(message)
            print(trimmed_message)
            with open('result.txt', 'w') as file:
                file.write(str(trimmed_message))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process chat with a secret token.")
    parser.add_argument("secret_token", help="The secret authentication token")
    args = parser.parse_args()

    main(args.secret_token)
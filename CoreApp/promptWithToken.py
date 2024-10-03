import json
import subprocess
import requests

prompt = """
As a mobile security expert, please perform a comprehensive security analysis of the provided Android/iOS app code. Your analysis should focus on identifying potential security vulnerabilities, including but not limited to:

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

Please provide your findings in a JSON file with the following structure (wrapped in triple apostrohpes):

'''
[
  {
    "title": "Brief title of the vulnerability",
    "description": "Detailed explanation of the issue.",
    "location": "File names and line numbers where the issue is found.",
    "impact": "Potential consequences if the vulnerability is exploited.",
    "recommendation": "Steps or code changes required to fix the issue.",
    "severity_level": "Critical/High/Medium/Low"
  },
  {
    "title": "Next vulnerability title",
    "description": "Detailed explanation of the next issue.",
    "location": "File names and line numbers where the next issue is found.",
    "impact": "Potential consequences if the next vulnerability is exploited.",
    "recommendation": "Steps or code changes required to fix the next issue.",
    "severity_level": "Critical/High/Medium/Low"
  }
  // ... Continue for each vulnerability found
]
'''

Example (wrapped in triple apostrohpes):

'''
[
  {
    "title": "Hardcoded API Key Found in Source Code",
    "description": "An API key for the payment gateway is hardcoded in 'PaymentProcessor.java' at line 45.",
    "location": "/app/src/main/java/com/example/payment/PaymentProcessor.java:45",
    "impact": "Attackers with access to the APK can decompile it to retrieve the API key, leading to unauthorized transactions.",
    "recommendation": "Remove the hardcoded API key and store it securely using Android's Keystore system or fetch it securely from a remote server after authentication.",
    "severity_level": "High"
  }
]
'''

Use this framework to conduct a thorough security review of the app code, ensuring all potential vulnerabilities are identified and addressed in the specified JSON format.
The next lines are the code to review.
"""

def extract_message(response):
    """Extracts the 'message' value from a JSON response.

    Args:
        response (str): The JSON response string.

    Returns:
        str: The 'message' value, or None if it's not found.
    """

    try:
        data = json.loads(response)
        return data['data']['value']
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response: {e}")
        return None

# The token should be the last non-empty line
token =f"eyJhbGciOiAiUlMyNTYiLCAia2lkIjogIm5jZ1FmdFpJWncifQ.eyJhdXRoIjogImJhc2ljIiwgImZ0YyI6IDIsICJpYXQiOiAxNzI3OTY3Njc0LCAianRpIjogIktyX3J1MllxSDJsd0tiSVZQTkgyWVEiLCAidHlwIjogImpvbWF4IiwgInZhdCI6IDE3Mjc5Njc2NzQsICJmYWN0b3JzIjogeyJrX2ZlZCI6IDE3Mjc5Njc2NzQsICJwX29rdGEiOiAxNzI3OTY3Njc0fSwgImN0eCI6ICIiLCAiYWNjb3VudE5hbWUiOiAiZ2RpYXp2aWxsZWdhcyIsICJzdWIiOiAiNDM4MzQwIiwgInV0eXAiOiAxMDF9.Up28oAzgU73clTvxOlCssi-ri0iEDAU0jjyGMESfWc9CkZQSZ0WVzhFcwnOFopXivV8BbE6CL86MkH6wDmkKrbOy2cDWOCTS5aTRjhhoPJNilcIR3J2XVTmETSrb37hxnh011Grm-UuqBEfJQp_kH2NdFw-93LI_-XGOd3GUbA8MaudrtwSA6U2LRDMhKqgP0Z8aElCU-DOxgTSPBlm4IEBJPF45FZh-fK6zr9eD3djJqnXFqo8-oKJOwXv5tUo34dwA8Lahi5RJUqaA2kbvHZozpXmbE7ytVIIhXi_O0z-svAwZ08NxR8SyeU5KaMJV1OKhOu_PX_NZxBIoz5iVSQ"
with open('diff_result.txt', 'r') as f:
    diff_result = f.read()
url = 'https://caas.api.godaddy.com/v1/prompts'
headers = {
    'Authorization': f"sso-jwt {token}",
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'prompt': f"'{prompt}{diff_result}'",
    'provider': 'openai_chat',
    'providerOptions': {
        'model': 'gpt-4o'
    }
}

response = requests.post(url, headers=headers, json=data)
json_message = f"{response.text}"
message = extract_message(json_message)
print(message)

import json
import subprocess
import requests

from codeDiff import diff_result

prompt = '''As a mobile security expert, please perform a comprehensive security analysis of the provided Android/iOS app code. Your analysis should focus on identifying potential security vulnerabilities, including but not limited to:

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

Example:

--BEGIN OF EXAMPLE--

Title: Hardcoded API Key Found in Source Code

Description: An API key for the payment gateway is hardcoded in PaymentProcessor.java at line 45.

Location: /app/src/main/java/com/example/payment/PaymentProcessor.java:45

Impact: Attackers with access to the APK can decompile it to retrieve the API key, leading to unauthorized transactions.

Recommendation: Remove the hardcoded API key and store it securely using Android's Keystore system or fetch it securely from a remote server after authentication.

Severity Level: High

--END OF EXAMPLE--

Use this framework to conduct a thorough security review of the app code, ensuring all potential vulnerabilities are identified and addressed. 

Next is the iOS/Android code. '''

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
token =f"eyJhbGciOiAiUlMyNTYiLCAia2lkIjogIm5jZ1FmdFpJWncifQ.eyJhdXRoIjogImJhc2ljIiwgImZ0YyI6IDIsICJpYXQiOiAxNzI3ODI0NTEwLCAianRpIjogIm9IRVhRTmJ6SXNSRnpDdjMyRV91SHciLCAidHlwIjogImpvbWF4IiwgInZhdCI6IDE3Mjc4MjQ1MTAsICJmYWN0b3JzIjogeyJrX2ZlZCI6IDE3Mjc4MjQ1MTAsICJwX29rdGEiOiAxNzI3ODI0NTEwfSwgImN0eCI6ICIiLCAiYWNjb3VudE5hbWUiOiAiZ2RpYXp2aWxsZWdhcyIsICJzdWIiOiAiNDM4MzQwIiwgInV0eXAiOiAxMDF9.MXEjyo17HeeEdCwPoz-q9S6hlxxkK7971Gsjz5lYzKshFpkfIvt9JarCiDkmZfb8jowvgeGTkcBfJnKpqktP1dP6OKRP_0wcj0wONzwLFFB76Md6ulaTLbsObLwvOlPmGc6dPK1deCWGuJZqlUd3jGHoG_VlCMkwE9rKeA3EOG3e8L0JKiIUk8e10Loj4sb6r7cbHQEZ5PuEQSG9uzFNzJZcXbNQIElXki5A7aAMnU3VHws-VzkBi26q53mVpU0BGL1UDmk7HUKY22RrUpoABJydVWcTW1wHCMBurCL0vRi9CGMmMsvjAgKyrBFP00CLZ5yxS2mVqnozeIIwqi_OzQ"
print(token)
url = 'https://caas.api.godaddy.com/v1/prompts'
headers = {
    'Authorization': f"sso-jwt {token}",
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'prompt': '{prompt}{diff_result}',
    'provider': 'openai_chat',
    'providerOptions': {
        'model': 'gpt-3.5-turbo'
    }
}

response = requests.post(url, headers=headers, json=data)
json_message = f"{response.text}"
message = extract_message(json_message)
print(message)
print(requests.__version__)

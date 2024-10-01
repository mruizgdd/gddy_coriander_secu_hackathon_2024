import json
import subprocess
import requests

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
    'prompt': ' Write a code that says hola in Python',
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

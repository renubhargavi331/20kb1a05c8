import requests

url = "http://20.244.56.144/test/register"
data = {
    "companyName": "renubotique",
    "ownerName": "Renu Bhargavi Pudi",
    "rollNo": "20kb1a05c8",
    "ownerEmail": "renubhargavipudi@gmai.com",
    "accessCode": "nbYNBp"
}

response = requests.post(url, json=data)

print(response.json())

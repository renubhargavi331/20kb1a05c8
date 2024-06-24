import requests

url = "http://20.244.56.144/test/auth"
data = {'companyName': 'renubotique', 
        'clientID': 'b42be82a-dff0-4085-a662-027c539829da',
        'clientSecret': 'NxzzbChehTbYJkuc', 
        'ownerName': 'Renu Bhargavi Pudi', 
        'ownerEmail': 'renubhargavipudi@gmai.com', 
        'rollNo': '20kb1a05c8'}

response = requests.post(url, json=data)

print(response.json())

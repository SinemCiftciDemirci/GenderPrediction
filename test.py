import requests

url = 'http://127.0.0.1:5000/predict_gender'
data = {
    "last_menstrual_date": "2024-06-15",
    "husband_birth_date": "1990-05-20"
}

response = requests.post(url, json=data)
print(response.json())

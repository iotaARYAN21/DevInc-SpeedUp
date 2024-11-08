import requests

num1 = input();
num2 = input();
operator = input();
data = {"expr":num1+operator+num2}
response = requests.post('https://api.mathjs.org/v4/',json=data)

if(response.status_code == 200):
    print(response.json())
else:
    print(response.status_code)
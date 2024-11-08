import requests

num1 = input();  # taking the first number and second number argument as input
num2 = input(); 
operator = input(); # the operation to perform
data = {"expr":num1+operator+num2}  # creating the type of data as accepted by the api
response = requests.post('https://api.mathjs.org/v4/',json=data)   # creating the request

if(response.status_code == 200): # means the fetching was succesfull
    print(response.json())
else:
    print(response.status_code)
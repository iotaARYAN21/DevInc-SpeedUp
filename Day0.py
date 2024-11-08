import requests

num1 = input();  # taking the first number and second number argument as input
num2 = input(); 
operator = input(); # the operation to perform
data = {"num1":num1,"num2":num2,"operation":operator}  # creating the type of data as accepted by the api
response = requests.post('http://127.0.0.1:5000/calculate',json=data)   # creating the request

if(response.status_code == 200): # means the fetching was succesfull
    print(response.json())
else:
    print(response.status_code)
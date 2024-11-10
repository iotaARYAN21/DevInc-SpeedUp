import requests

# Define the base URL
base_url = "http://127.0.0.1:5000"

def register():
    username = input("Enter username ")
    email = input("Enter email ")
    password = input("Enter password ")
    data = {"username":username,"email":email,"password":password}
    response = requests.post(f"{base_url}/register",json=data)

    if response.status_code == 201:
        print("Registered successfully ")
    else:
        try:
            print("Registration falid",response.json())
        except requests.exceptions.JSONDecodeError:
            print("Error:")
            print("Response" , response.text)
        
        # print("Registration Failed ")
        # print(response.json())

def login():
    username = input("Enter username ")
    password = input("Enter password ")
    data = {"username":username,"password":password}
    response = requests.post(f"{base_url}/login",json=data)

    if response.status_code == 200:
        try:
            token = response.json().get("access_token")
            print(response.json())
            print("Login Done")
            return token
        except requests.exceptions.JSONDecodeError:
            print("Error",response.text)
        # token = response.json().get("access_token")
        # print("Login success")
        # print(f"jwt token : {token}")
        # return token
    else:
        try:
            print("Login failed",response.json())
        except requests.exceptions.JSONDecodeError:
            print("Eroro",response.text)
        # print("login failed")
        # print(response.json())


# Add a task
def add_task(token):
    task = input("Enter the task description: ")
    status = input("Enter the status (Pending or Completed): ")
    data = {"task": task, "status": status}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{base_url}/tasks", json=data,headers=headers)

    # if the status input is incorrect
    while status not in ['Pending','Completed']:
        print("Invalid status")
        status = input("Enter the status again")
    if response.status_code == 401:  # Unauthorized
        print("Your session has expired. Please log in again.")
    elif response.status_code == 201:
        try:
            print(response.json())  # Expected JSON response on success
        except requests.exceptions.JSONDecodeError:
            print("Error: Expected JSON response, got something else.")
            print("Response content:", response.text)
    else:
        print(f"Failed to add task. Status code: {response.status_code}")
        print("Response content:", response.text)


# Delete a task by ID
def delete_task(token):
    task_id = input("Enter the task ID to delete: ")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{base_url}/tasks/{task_id}",headers=headers)
    print(response.json())


# Update a task by ID
def update_task(token):
    task_id = input("Enter the task ID to update: ")
    task = input("Enter the task description (leave blank to keep current): ")
    status = input("Enter the new status (Pending or Completed, leave blank to keep current): ")
    data = {"task": task if task else None, "status": status if status else None}
    headers = {"Authorization":f"Bearer {token}"}
    response = requests.put(f"{base_url}/tasks/{task_id}", json=data,headers=headers)
    print(response.json())

# Main function to select action
def main():
    token = None
    while True:
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. Exit")
        print("5. Register")
        print("6. Login")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            if token:
                add_task(token)
            else:
                print("You need to log in first.")   # Edge case for me
        elif choice == '2':
            if token:
                delete_task(token)
            else:
                print("You need to log in first.")
        elif choice == '3':
            if token:
                update_task(token)
            else:
                print("You need to log in first.")
        elif choice == '4':
            break
        elif choice == '5':
            register()
        elif choice == '6':
            token = login()
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

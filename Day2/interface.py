import requests

# Define the base URL
base_url = "http://127.0.0.1:5000"

# Add a task
def add_task():
    task = input("Enter the task description: ")
    status = input("Enter the status (Pending or Completed): ")
    data = {"task": task, "status": status}
    response = requests.post(f"{base_url}/tasks", json=data)
    
    # Check for successful response
    if response.status_code == 201:
        try:
            print(response.json())  # Expected JSON response on success
        except requests.exceptions.JSONDecodeError:
            print("Error: Expected JSON response, got something else.")
            print("Response content:", response.text)
    else:
        print(f"Failed to add task. Status code: {response.status_code}")
        print("Response content:", response.text)
# Delete a task by ID
def delete_task():
    task_id = input("Enter the task ID to delete: ")
    response = requests.delete(f"{base_url}/tasks/{task_id}")
    print(response.json())

# Update a task by ID
def update_task():
    task_id = input("Enter the task ID to update: ")
    task = input("Enter the task description (leave blank to keep current): ")
    status = input("Enter the new status (Pending or Completed, leave blank to keep current): ")
    data = {"task": task if task else None, "status": status if status else None}
    response = requests.patch(f"{base_url}/tasks/{task_id}", json=data)
    print(response.json())

# Main function to select action
def main():
    while True:
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_task()
        elif choice == '2':
            delete_task()
        elif choice == '3':
            update_task()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

from config import ARTIFACTORY_URL, headers, spacing, requests, json, html

"""
Retrieves the list of users. Format and displays the user information
"""
def get_users():
    url = f"{ARTIFACTORY_URL}/api/security/users"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Error: Failed to retrieve users {response.status_code}")

    if response.status_code == 200:
        users = response.json()
        print(f"List of Users ({len(users)}):")
        count = 1
        for user in users:
            print(f"{count}. {user['name']}".ljust(spacing) + f" Realm: {user['realm']}")
            count+=1     


"""
Create a new repository.
    
Parameters:
userName (string): The name of the user.
"""
def create_user(userName):
    email = input('Enter Email: ')
    password = input('Enter Password: ')

    username = html.escape(userName)
    email = html.escape(email)
    password = html.escape(password)

    userdata = {
        "username": username,
        "email": email,
        "password": password,
        "internal_password_disabled": False,
        "admin": False,
    }

    userJson = json.dumps(userdata)

    url = f"{ARTIFACTORY_URL}/api/security/users/{username}"
    
    try:
        response = requests.put(url, headers=headers, data=userJson)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Error: Failed to create user {response.status_code}")
        res = response.json()
        if len(res['errors']) > 0:
            errors = res['errors']
            print(f"{errors[0]['message']}".capitalize())

    if response.status_code == 200 or response.status_code == 201:
        print(f"User was created {response}")


"""
Delete a repository.
    
Parameters:
userName (string): The name of the user.
"""
def del_user(userName):
    url = f"{ARTIFACTORY_URL}/api/security/users/{userName}"


    confirm = False
    confirm = input('Confirm (y/n) that you want this user deleted?: ').lower() == 'y'

    if confirm:
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()  # Raise an exception for unsuccessful requests
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {e}")
        except Exception as e:
            print(f"Error: Failed to delete user {response.status_code}")
            res = response.json()
            if len(res['errors']) > 0:
                errors = res['errors']
                print(f"{errors[0]['message']}".capitalize())
    else:
        print('Operation aborted')
        return

    if response.status_code == 200 or response.status_code == 201:
        print(f"User was deleted {response}") 



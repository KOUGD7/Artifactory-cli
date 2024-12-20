from config import ARTIFACTORY_URL, headers, spacing, requests, json, html

def get_users():

    url = f"{ARTIFACTORY_URL}/api/security/users"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        users = response.json()
        print(f"List of Users ({len(users)}):")
        count = 1
        for user in users:
            print(f"{count}. {user['name']}".ljust(spacing) + f" Realm: {user['realm']}")
            count+=1
    else:
        print(f"Error: Failed to retrieve users {response.status_code}")


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
    response = requests.put(url, headers=headers, data=userJson)

    print(response.json)

    if response.status_code == 200 or response.status_code == 201:
        print(f"User was created {response}")
        
    else:
        print(f"Error: Failed to create user {response.status_code}")
        res = response.json()
        if len(res['errors']) > 0:
            errors = res['errors']
            print(f"{errors[0]['message']}".capitalize())

def del_user(userName):

    url = f"{ARTIFACTORY_URL}/api/security/users/{userName}"


    confirm = False
    confirm = input('Confirm (y/n) that you want this user deleted?: ').lower() == 'y'

    if confirm:
        response = requests.delete(url, headers=headers)
    else:
        print('Operation aborted')
        return

    if response.status_code == 200 or response.status_code == 201:
        print(f"User was deleted {response}")
    else:
        print(f"Error: Failed to delete user {response.status_code}")
        res = response.json()
        if len(res['errors']) > 0:
            errors = res['errors']
            print(f"{errors[0]['message']}".capitalize())



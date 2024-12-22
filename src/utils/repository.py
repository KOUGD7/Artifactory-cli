from config import ARTIFACTORY_URL, headers, spacing, requests, json, html

"""
Retrieves the list of repository. Format and displays the repository information
"""
def get_repos():
    url = f"{ARTIFACTORY_URL}/api/repositories"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Error: {response.status_code}")

    if response.status_code == 200:
        repos = response.json()
        print(f"List of Repositories ({len(repos)}):")
        count = 1
        for repo in repos:
            if 'key' in repo and 'packageType' in repo:
                print(f"{count}. {repo['key']}".ljust(spacing) + f"{repo['type']}".ljust(12) + f" Package type: {repo['packageType']}")
            count+=1
    else:
        print(f"Failed to retrieve repositories")


"""
    Create a new repository.
    
    Parameters:
    repoName (string): The name of the repository.
    rclass (string): The class of the repository.
    method (string): The operation (create, update or delete) to the perform on repo.
    """
def create_repo(repoName, rclass="local", method = 'create'):
    repoName = html.escape(repoName)
    
    url = f"{ARTIFACTORY_URL}/api/repositories/{repoName}"
    config = {
        'key': repoName,
        "rclass": rclass
    }
    repo_config = json.dumps(config)

    if method == 'update':
        del config['rclass']

        repo_descrip = input('Enter Description: ')
        repo_descrip = html.escape(repo_descrip)
        config['description'] = repo_descrip
        repo_config = json.dumps(config)

        try:
            response = requests.post(url, headers=headers, data=repo_config)
            response.raise_for_status()  # Raise an exception for unsuccessful requests
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {e}")
        except Exception as e:
            print(f"Error: Failed to {method} repository {response.status_code}")

    elif method == 'delete':
        confirm = False
        confirm = input('Confirm (y/n) that you want this repo removed?: ').lower() == 'y'
        if confirm:
            response = requests.delete(url, headers=headers)
        else:
            print('Operation aborted')
            return

    else:
        response = requests.put(url, headers=headers, data=repo_config)

    if response.status_code == 200 or response.status_code == 201:
        print(response.text)
        
    else:
        res = response.json()
        if len(res['errors']) > 0:
            errors = res['errors']
            print(f"{errors[0]['message']}".capitalize())


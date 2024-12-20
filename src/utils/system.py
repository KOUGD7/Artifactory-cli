from config import ARTIFACTORY_URL, headers, spacing, requests

def get_help():
    help_dict = {
        'EXIT': 'Quit the CLI',
        'HELP': 'Provides Help information for CLI',
        'PING': 'Get a simple status response about the state of Artifactory',
        'REPOADD <repository name>': 'Create Repository',
        'REPODEL <repository name>': 'Delete Repository',
        'REPOUPATE': 'Update Repository',
        'REPOLIST': 'Display list of repositories',
        'USERADD <user name>': 'Create Repository User',
        'USERDEL <user name>': 'Delete Repository',
        'USERLIST': 'Display list of users',
        'STORAGE': 'Display Storage Summary Information',
        'VERSION': 'Return information about the current Artifactory version',    
    }

    print("For more information on a specific command, type HELP command-name")
    for key in help_dict.keys():
        print(f"{key}".ljust(spacing)+f"{help_dict[key]}")


def get_version():
    url = f"{ARTIFACTORY_URL}/api/system/version"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        systemVersion = response.json()
        print("version:".ljust(spacing)+f"{systemVersion['version']}")
        print("revision:" .ljust(spacing)+f"{systemVersion['revision']}")
    else:
        print(f"Error: Failed to get version {response.status_code}")


def get_ping():
    url = f"{ARTIFACTORY_URL}/api/v1/system/readiness"

    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        raise(e)

    if response.status_code == 200:
        status = response.json()
        print("Status:".ljust(spacing)+f" {status['code']}")
    else:
        print(f"Error: Failed to ping {response.status_code}")


def get_storage():

    url = f"{ARTIFACTORY_URL}/api/storageinfo"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        info = response.json()
        repos = info['repositoriesSummaryList']
        count = 1
        for repo in repos:
            if 'packageType' in repo:
                print(f"{count}. {repo['repoKey']}".ljust(spacing)+f"Used: {repo['usedSpace']}".ljust(18) + f" Type: {repo['packageType']}")
            else:
                print(f"{repo['repoKey']}".ljust(spacing)+f"Used: {repo['usedSpace']}")

            count+=1
    else:
        print(f"Error: Failed to get storage info {response.status_code}")

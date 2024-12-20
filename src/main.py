from utils.system import get_ping, get_storage, get_help, get_version
from utils.repository import create_repo, get_repos

if __name__ == "__main__":
    print('Welcome to JFrog CLI. For more information on a specific command, type HELP command-name')

    run = True
    while run:
        inputText = input("Enter: ")
        cmd = ''
        lst = inputText.split()
        if len(lst) > 0: cmd = lst[0].upper()
        
        match cmd:
            case 'PING':
                get_ping()

            case 'STORAGE':
                get_storage()

            case 'REPOADD' | 'REPODEL' | 'REPOUPDATE':
                
                repo_type =''
                if cmd == 'REPOADD':
                    operation = 'create'
                    repo_type = input('Enter Repo Type: ')
                elif cmd == 'REPODEL':
                    operation = 'delete'
                else:
                    operation = 'update'

                if len(lst) == 2:
                    
                    if repo_type:
                        create_repo(lst[1], repo_type.lower(), method=operation)
                    else:
                        create_repo(lst[1], method=operation)
                else:
                    print(f'Invalid command. Use {cmd} <repository name>')
                    get_help()

            
            case 'REPOLIST':
                get_repos()

            case 'VERSION':
                get_version()

            case 'HELP':
                get_help()
                
            case 'EXIT':
                run = False

            case _:
                print(f"'{cmd}' is not recognized as an command. For more information on a specific command, type HELP command-name")
        print('\n')
from github import Github


def has_java_file(nameWithOwner: str, token: str):
    # iterate through every file until you find a .java file

    g = Github(token)

    repo = g.get_repo(nameWithOwner)
    contents = repo.get_contents('')
    while contents:
        file_content = contents.pop()
        try:
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.name.endswith('.java') or file_content.name.endswith('.jar'):
                    return True
        except:
            pass
    return False

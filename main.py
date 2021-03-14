from pprint import pprint
from src.utils.csv import get_ck_data
from src.models.Repo import Repo
from src.utils.repos import has_java_file
from src.utils.graphql import get_query, get_repos_data
import pandas as pd
import os
import progressbar
import git

from dotenv import load_dotenv

# Load env file
load_dotenv()

# Get env variables
url = os.getenv('API_URL')
tokens = ['Bearer {}'.format(token)
          for token in os.getenv('AUTH_TOKENS').split(',')]


# ? Set your request configs here
total_repos = 1
repos_per_request = 1
# TODO: replace with Y3Vyc29yOjI=
initial_cursor = 'Y3Vyc29yOjEx'  # First repo with .java files

if repos_per_request % total_repos != 0:
    raise Exception('repos_per_request should be divisible by total_repos')


repo_list: "list[Repo]" = []


# extremely necessary progress bar for better user experience
widgets = [
    progressbar.Percentage(),
    progressbar.Bar(marker='\x1b[32m#\x1b[39m'),
]
bar = progressbar.ProgressBar(
    widgets=widgets,
    max_value=int(total_repos / repos_per_request),
    min_value=0,
    redirect_stdout=True
).start()


current_token = 0

print('Fetching repos...')

i = 0
while i < int(total_repos / repos_per_request):
    # Make 1000 requests

    try:
        current_cursor = repo_list[-1].cursor if len(repo_list) > 0 else None

        print('Fetching cursor: {}'.format(current_cursor))

        # Build query
        query = get_query(repos_per_request, current_cursor or initial_cursor)

        # Get repo data
        repo_data: list = get_repos_data(url, query, tokens[current_token])

        # For each repo clone and run ck through it
        has_java_count = 0
        for repo in repo_data:
            new_repo = Repo(repo)

            print('Searching for .java files for {}...'.format(
                new_repo.nameWithOwner))
            if has_java_file(new_repo.nameWithOwner, tokens[current_token].replace('Bearer ', '')):

                print('Cloning repo {}...'.format(new_repo.nameWithOwner))
                git.Git("repos").clone(new_repo.url)

                print('Running CK...'.format(new_repo.nameWithOwner))
                os.system(
                    "java -jar ck/target/ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar repos/{} true 0 false".format(new_repo.nameWithOwner.split('/')[1]))

                new_repo.add_ck_data(get_ck_data())

                # add repo to list
                repo_list.append(new_repo)

                # remove repo after finishing
                print('Deleting repo {}')
                os.system(
                    'rm -rf repos/* class.csv method.csv')

                has_java_count += 1

            i += has_java_count
            bar.update(i)

    except Exception as err:
        print(err)
        if current_token < len(tokens) - 1:
            current_token += 1.
        else:
            current_token = 0


print('All repos were fetched')

bar.finish()

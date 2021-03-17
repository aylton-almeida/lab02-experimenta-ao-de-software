import os
import progressbar
import time

from pprint import pprint
from src.utils.csv import get_ck_data, save_repos_to_csv
from src.models.Repo import Repo
from src.utils.repos import has_java_file
from src.utils.graphql import get_query, get_repos_data
from dotenv import load_dotenv

# Load env file
load_dotenv()


def mine_repos():
    # Get env variables
    url = os.getenv('API_URL')
    tokens = ['Bearer {}'.format(token)
              for token in os.getenv('AUTH_TOKENS').split(',')]

    # ? Set your request configs here
    total_repos = 1000
    repos_per_request = 100
    stars = '<2694'
    # First repo with .java files Y3Vyc29yOjI=
    initial_cursor = None

    if total_repos % repos_per_request != 0:
        raise Exception('repos_per_request should be divisible by total_repos')

    repo_list: "list[Repo]" = []

    # extremely necessary progress bar for better user experience
    widgets = [
        progressbar.Percentage(),
        progressbar.Bar(marker='\x1b[32m#\x1b[39m'),
    ]
    bar = progressbar.ProgressBar(
        widgets=widgets,
        max_value=total_repos,
        min_value=0,
        redirect_stdout=True
    ).start()

    current_token = 0

    print('Fetching repos...')

    current_cursor = initial_cursor

    while len(repo_list) < total_repos:
        # Make 1000 requests

        try:

            print('Fetching cursor: {}'.format(current_cursor))
            print('Current token: {}'.format(current_token))

            # Build query
            query = get_query(repos_per_request,
                              current_cursor, stars)

            # Get repos data
            repo_data: list = get_repos_data(
                url, query, tokens[int(current_token)])

            if len(repo_data) > 0:

                # For each repo clone and run ck through it
                for repo in repo_data:
                    new_repo = Repo(repo)

                    if (len(repo_list) % 50) == 0:
                        save_repos_to_csv(repo_list, 'data.csv')

                    print('Searching for .java files for {}...'.format(
                        new_repo.nameWithOwner))
                    if has_java_file(new_repo.nameWithOwner, tokens[int(current_token)].replace('Bearer ', '')):

                        # add repo to list
                        repo_list.append(new_repo)

                        bar.update(len(repo_list))

                    if len(repo_list) == total_repos:
                        break

                    current_cursor = repo_list[-1].cursor if len(
                        repo_list) > 0 else None
            else:
                current_cursor = None
                stars = '<{}'.format(repo_list[-1].stargazerCount)
                print(stars)

        except:
            time.sleep(len(repo_list) * 2)
            if current_token < len(tokens) - 1:
                current_token += 1.
            else:
                current_token = 0

    print('All repos were fetched')

    save_repos_to_csv(repo_list, 'data.csv')

    bar.finish()


if __name__ == '__main__':
    mine_repos()

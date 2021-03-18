import pandas as pd
import os
import progressbar
import git

from src.utils.csv import get_ck_data, save_repos_to_csv
from src.models.Repo import Repo
from dotenv import load_dotenv

# Load env file
load_dotenv()


def clone_repo():
    data_frame = pd.read_csv('repos_data.csv', ';')

    # Cleaning folders
    os.system('rm -rf repos/* ck_data.csv')
    os.system('touch ck_data.csv')

    # extremely necessary progress bar for better user experience
    widgets = [
        progressbar.Percentage(),
        progressbar.Bar(marker='\x1b[32m#\x1b[39m'),
    ]
    bar = progressbar.ProgressBar(
        widgets=widgets,
        max_value=len(data_frame.index),
        min_value=0,
        redirect_stdout=True
    ).start()

    print('Analyzing repos...')

    for index, row in data_frame.iterrows():
        repo = Repo.from_dataframe(row)
        repo_folder = repo.nameWithOwner.replace('/', '-')

        print('Cloning repo {}...'.format(repo.nameWithOwner))
        os.system("mkdir -p repos/{}".format(repo_folder))
        git.Git("repos/{}".format(repo_folder)).clone(repo.url)

        print('Running CK...')
        os.system(
            "java -jar ck/target/ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar repos/{} true 0 false".format(
                repo_folder))

        print('Renaming files...')
        os.system(
            'mv class.csv repos/{}/class.csv'.format(repo_folder))

        repo.add_ck_data(get_ck_data('repos/{}/class.csv'.format(repo_folder)))
        save_repos_to_csv([repo], 'ck_data.csv', 'a')

        # remove method.csv after finishing
        print('Deleting method.csv...'.format(repo.nameWithOwner))
        os.system('rm -rf method.csv')

        bar.update(index + 1)

    print('All repos were fetched')

    bar.finish()


if __name__ == '__main__':
    clone_repo()

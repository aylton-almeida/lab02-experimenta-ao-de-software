import pandas as pd
import os
import progressbar
import git

from src.utils.csv import get_ck_data
from src.models.Repo import Repo
from dotenv import load_dotenv

# Load env file
load_dotenv()


def clone_repo():
    data_frame = pd.read_csv('1_data.csv')

    # extremely necessary progress bar for better user experience
    widgets = [
        progressbar.Percentage(),
        progressbar.Bar(marker='\x1b[32m#\x1b[39m'),
    ]
    bar = progressbar.ProgressBar(
        widgets=widgets,
        max_value=data_frame.size,
        min_value=0,
        redirect_stdout=True
    ).start()

    print('Analyzing repos...')

    for index, row in data_frame.iterrows():
        repo = Repo.from_dataframe(row)

        print('Cloning repo {}...'.format(repo.nameWithOwner))
        git.Git("repos").clone(repo.url)

        print('Running CK...'.format(repo.nameWithOwner))
        os.system(
            "java -jar ck/target/ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar repos/{} true 0 false".format(
                repo.nameWithOwner.split('/')[1]))

        repo.add_ck_data(get_ck_data('class.csv', 'method.csv'))
        print(repo)

        # remove repo after finishing
        print('Deleting repo {}')
        os.system(
            'rm -rf repos/* class.csv method.csv')

        bar.update()

    print('All repos were fetched')

    bar.finish()


if __name__ == '__main__':
    clone_repo()

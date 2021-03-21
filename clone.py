import pandas as pd
import os
import progressbar
import sys

from src.utils.csv import get_ck_data, save_repos_to_csv
from src.models.Repo import Repo
from dotenv import load_dotenv

# Load env file
load_dotenv()


def clone_repo():
    if len(sys.argv) < 2:
        print('Type your destination file')
        return
    if len(sys.argv) < 3:
        print('Type your initial index')
        return

    data_frame = pd.read_csv('repos_data.csv', ';')

    os.system('rm -rf repos/*')

    print('Analyzing repos...')

    data_arr = [*data_frame.iterrows()]

    destination_file = sys.argv[1]
    initial_index = int(sys.argv[2])
    final_index = int(sys.argv[3]) if len(
        sys.argv) > 3 else (len(data_arr) - 1)

    print(destination_file, initial_index, final_index)

    # Get non fetched data
    final_arr = data_arr[initial_index:final_index]

    # extremely necessary progress bar for better user experience
    with progressbar.ProgressBar(max_value=final_index, min_value=initial_index, redirect_stdout=True) as bar:
        for index, row in final_arr:
            repo = Repo.from_dataframe(row)
            repo_folder = repo.nameWithOwner.replace('/', '-')

            print('Cloning repo {}...'.format(repo.nameWithOwner))
            os.system("mkdir -p repos/{}".format(repo_folder))
            os.system('git clone {} repos/{}/{}'.format(repo.url, repo_folder,
                                                        repo.nameWithOwner.split('/')[1]))

            print('Running CK...')
            os.system(
                "java -jar ck/target/ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar repos/{} true 0 false".format(
                    repo_folder))

            repo.add_ck_data(get_ck_data(
                'class.csv'.format(repo_folder)))
            save_repos_to_csv([repo], destination_file, 'a')

            # remove method.csv after finishing
            print('Deleting method.csv...'.format(repo.nameWithOwner))
            os.system('rm -rf method.csv class.csv repos/*')

            bar.update(index + 1)

    print('All repos were fetched')


if __name__ == '__main__':
    clone_repo()

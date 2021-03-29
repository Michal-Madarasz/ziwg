import os
import pandas as pd

if __name__ == '__main__':
    path = './data/csv/bibs-test.csv'
    if os.path.isfile(path):
        with open(path, 'rb') as fh:
            data_file = pd.read_csv(path, sep=',', header=0)

            titles = [x for x in data_file['title']]
            print(titles)
    else:
        print(f"Error: Path does not exist")

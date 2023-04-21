import pandas as pd  # maybe default csv package can do this too but idc right now


def remove_duplicates(input):
    df = pd.read_csv(input, encoding='utf-8', delimiter=',')
    num_rows = df.shape[0]
    print(f"Currently there are {num_rows} rows in the created CSV file ")

    print('removing duplicate rows...')

    df.drop_duplicates(subset=['url'], inplace=True)
    print(f"Found {num_rows - df.shape[0]} duplicate rows and deleted.")

    df.to_csv(input, index=False, encoding='utf-8')

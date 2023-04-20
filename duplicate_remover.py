import pandas as pd
file_name = "history.csv"
file_name_output = "clean_history.csv"

df = pd.read_csv(file_name, encoding='utf-8', delimiter=',')


df.drop_duplicates(subset=['url'], inplace=True)


df.to_csv(file_name_output, index=False, encoding='utf-8')

import pandas as pd
from sqlalchemy import create_engine

# Load CSV file into a pandas dataframe
df = pd.read_csv('history.csv')

# Connect to the database using SQLAlchemy
engine = create_engine('sqlite:///newpipe.db', echo=True)

# Insert dataframe into a SQL database table
df.to_sql('streams', engine, if_exists='replace', index=False)

# uid, service_id, url, title, stream_type, duration, uploader, uploader_url, thumbnail_url, view_count, textual_upload_date, upload_date, is_upload_date_approximation


# INSERT OR REPLACE INTO streams(uid, service_id, url, title, stream_type, duration, uploader, uploader_url, thumbnail_url, view_count, textual_upload_date, upload_date, is_upload_date_approximation)
# SELECT uid, service_id, url, title, stream_type, duration, uploader, uploader_url, thumbnail_url, view_count, textual_upload_date, upload_date, is_upload_date_approximation
# FROM streamz

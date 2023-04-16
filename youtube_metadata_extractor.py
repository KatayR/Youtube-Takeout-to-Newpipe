from __future__ import unicode_literals
import csv
from bs4 import BeautifulSoup
import time
import googleapiclient.discovery
import os
import googleapiclient.discovery
import googleapiclient.errors
import os
import re


# get youtube api ready
api_key = os.environ['YOUTUBE_API_KEY']
youtube = googleapiclient.discovery.build(
    'youtube', 'v3', developerKey=api_key)

# deal with youtubes time format like PT23M21S


def yt_time_to_seconds(time):
    regex_string = 'PT((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?'
    regex = re.compile(regex_string)
    match = regex.match(time)
    if match:
        minutes = int(match.group('minutes')) if match.group('minutes') else 0
        seconds = int(match.group('seconds')) if match.group('seconds') else 0
        return minutes * 60 + seconds
    return 0


# Define the URL of the HTML file containing the data
with open("C:/Users/rasit/Desktop/m_watch_history.html", 'r', encoding='utf-8') as url:
    soup = BeautifulSoup(url, "html.parser")

# Find all the video links in the HTML
blocks = soup.find_all(
    'div', class_='content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')

# Initialize a variable to keep track of the uid value
uid = 1901  # this is the highest uid number + 1 in my streams table of newpipe.db

# Create a CSV file and write the header row
csv_file = open("historyy.csv", "w", newline="", encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["uid", "service_id", "url", "title", "stream_type", "duration", "uploader", "uploader_url",
                     "thumbnail_url", "view_count", "textual_upload_date", "upload_date", "is_upload_date_approximation"])


# Loop over the video links and write a row to the CSV file for each one
for videos in blocks:
    aTags = videos.find_all('a')
    # Get the relevant data from the link
    for tag in aTags:
        link = tag["href"]
        if link and "youtube.com" in link and not 'channel' in link:
            url = link
            title = tag.text.strip()
            continue
        if link and "youtube.com" in link and 'channel' in link:
            uploader_url = link
            uploader = tag.text.strip()

    # Get the video ID from the URL
    video_id = url.split("=")[1]

    # Call Youtube api for more info. Idk if this makes it faster or slower
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    duration_response = response['items'][0]['contentDetails']['duration']
    uploadDate_response = response['items'][0]['snippet']['publishedAt'][:10]
    viewcount_response = response['items'][0]['statistics']['viewCount']

    # Assign values returned rom API
    textual_upload_date = uploadDate_response

    struct_time = time.strptime(
        textual_upload_date, "%Y-%m-%d")
    seconds_since_epoch = time.mktime(struct_time)
    upload_date = int(seconds_since_epoch * 1000)

    vid_duration = yt_time_to_seconds(duration_response)

    view_count = viewcount_response

    # Construct the thumbnail URL
    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"

    # Write the row to the CSV file
    csv_writer.writerow([uid, 0, url, title, "VIDEO_STREAM", vid_duration,
                        uploader, uploader_url, thumbnail_url, view_count, textual_upload_date, upload_date, 1])

    # Increment the uid value
    print(f"{uid-1900} done")
    uid += 1
# Close the CSV file
csv_file.close()

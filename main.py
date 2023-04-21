from __future__ import unicode_literals
import csv
from bs4 import BeautifulSoup
import time
import googleapiclient.discovery
import os
import googleapiclient.discovery
import googleapiclient.errors
import re
from max_uid import find_max_uid
from duplicate_remover import remove_duplicates


# ready Youtube API
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
max_uid = find_max_uid()
uid = max_uid  # finds maximum uid number in your "streams" table
# Create a CSV file and write the header row
csv_file = open("historyy.csv", "w", newline="", encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["uid", "service_id", "url", "title", "stream_type", "duration", "uploader", "uploader_url",
                     "thumbnail_url", "view_count", "textual_upload_date", "upload_date", "is_upload_date_approximation"])

# used a stopwatch to see how long it takes
start = time.time()

# Loop over the video links and write a row to the CSV file for each one
for videos in blocks:
    aTags = videos.find_all('a')
    # Get the relevant data from the Takeout html
    for tag in aTags:
        if '://' in tag.text.strip():
            continue
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

    # Call Youtube api for more info. Idk if this makes it faster or
    # slower relative to using youtube-dl, BeautifulSoup and stuff
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    print(title + "\n" + url)

    try:  # this part checks if video is hidden. Yes, I know. But youtube API is broken. So I had to...
        duration_response = response['items'][0]['contentDetails']['duration']
        uploadDate_response = response['items'][0]['snippet']['publishedAt'][:10]
    except:
        duration_response = 'PT4M04S'
        uploadDate_response = '2000-04-04'

    # This checks if video is unlisted AND "you"(your api) can't access it. Api is weird.
    try:
        viewcount_response = response['items'][0]['statistics']['viewCount']
    except:
        viewcount_response = 404

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
    print(f"{uid-max_uid} done\n")
    uid += 1
# Close the CSV file
end = time.time()
print('it took ' + '{:.2f}'.format(end - start) + ' seconds')
csv_file.close()


remove_duplicates('historyy.csv')

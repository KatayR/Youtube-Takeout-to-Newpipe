from __future__ import unicode_literals
import csv
from bs4 import BeautifulSoup
import time
import googleapiclient.discovery
import os
import googleapiclient.discovery
import googleapiclient.errors
import re

import youtube_dl


ydl_opts = {}


# Define the URL of the HTML file containing the data
with open("C:/Users/rasit/Desktop/m_watch_history.html", 'r', encoding='utf-8') as url:
    soup = BeautifulSoup(url, "html.parser")

# Find all the video links in the HTML
blocks = soup.find_all(
    'div', class_='content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')

# Initialize a variable to keep track of the uid value
uid = 1901  # this is the highest uid number + 1 in my streams table in newpipe.db

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

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        scraped = ydl.extract_info(url, download=False)

    try:  # this part checks if video is hidden. Yes, I know. But youtube API is broken. So I had to...
        vid_duration = scraped['duration']
        uploadDate_response = scraped['upload_date']
    except:
        vid_duration = 'PT4M04S'
        uploadDate_response = '20000404'

    # This checks if video is unlisted AND "you"(your api) can't access it. Api is weird.
    try:
        view_count = scraped['view_count']
    except:
        view_count = 404

    textual_upload_date = uploadDate_response[:4] + '-' + \
        uploadDate_response[4:6] + '-' + uploadDate_response[6:]
    struct_time = time.strptime(
        textual_upload_date, "%Y-%m-%d")
    seconds_since_epoch = time.mktime(struct_time)
    upload_date = int(seconds_since_epoch * 1000)

    # Construct the thumbnail URL
    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"

    # Write the row to the CSV file
    csv_writer.writerow([uid, 0, url, title, "VIDEO_STREAM", vid_duration,
                        uploader, uploader_url, thumbnail_url, view_count, textual_upload_date, upload_date, 1])

    # Increment the uid value
    print(f"{uid-1900} done\n")
    uid += 1
# Close the CSV file
end = time.time()
print('it took ' + '{:.2f}'.format(end - start) + ' seconds')
csv_file.close()

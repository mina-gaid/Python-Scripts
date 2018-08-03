#!/usr/bin/python
import os

# YouTube video searching API
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Downloading YouTube videos
import pafy

DEVELOPER_KEY = "ENTER_API_KEY_HERE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_VIDEO_URL_PREFIX = "https://www.youtube.com/watch?v="

pafy.set_api_key(DEVELOPER_KEY)


def youtube_search(options):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(q=options.q, part="id,snippet",
                                            maxResults=options.max_results).execute()

    videos = []
    for search_result in search_response.get("items", []):

        if search_result["id"]["kind"] == "youtube#video":
            video = {
                'video_id': search_result["id"]["videoId"],
                'title': search_result["snippet"]["title"],
                'desc': search_result["snippet"]["description"],
                'published': search_result["snippet"]["publishedAt"]
            }
            videos.append(video)

    return videos


def youtube_download_video(video_id, output_path):
    url = YOUTUBE_VIDEO_URL_PREFIX + video_id
    try:

        pafy.set_api_key(DEVELOPER_KEY)
        video = pafy.new(url, basic=False)

        print("VIDEO INFORMATION")
        print("  video.title     = %s" % video.title)
        print("  video.viewcount = %i" % video.viewcount)
        print("  video.author    = %s" % video.author)
        print("  video.length    = %i" % video.length)
        print("  video.duration  = %s" % video.duration)
        print("  video.likes     = %i" % video.likes)
        print("  video.dislikes  = %i" % video.dislikes)

        video_best = video.getbest(preftype='mp4')

        output_file = os.path.join(
            output_path, video_id + "." + video_best.extension)
        video_best.download(filepath=output_file, quiet=True)
    except:
        print("Warning, unable to download video with id '%s'" % video_id)
        return False

    return True


def youtube_search_and_download(query, num_videos, output_path):

    argparser.add_argument("--q", help="Search term", default=query)
    argparser.add_argument(
        "--max-results", help="Max results", default=num_videos)
    args = argparser.parse_args()

    try:
        videos = youtube_search(args)
        for video in videos:
            youtube_download_video(video['video_id'], output_path)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

    print("DONE")


if __name__ == "__main__":

    output_path = LOCAL_PATH_TO_DOWNLOAD"
    youtube_search_and_download("two cats", 5, output_path)

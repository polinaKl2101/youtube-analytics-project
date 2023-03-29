import datetime
import os
import isodate
from googleapiclient.discovery import build


class PlayList:

    __api_key: str = os.getenv('YT_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, playlist_id: str) -> None:

        self.__playlist_id = playlist_id
        self.__playlists_info = self.__youtube.playlists().list(id=playlist_id, part='contentDetails,snippet',
                                                                maxResults=50, ).execute()
        self.__playlist_videos = self.__youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,).execute()
        self.__video_ids = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]
        self.__video_response = self.__youtube.videos().list(part='contentDetails,statistics',
                                       id=','.join(self.__video_ids)).execute()

        self.__title = self.__playlists_info['items'][0]['snippet']['title']
        self.__url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def total_duration(self):
        total = datetime.timedelta()

        for video in self.__video_response['items']:

            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):

        max_likes = 0
        max_likes_video = None

        for i in range(len(self.__video_ids)):
            likes = int(self.__video_response['items'][i]['statistics']['likeCount'])
            if likes > max_likes:
                max_likes = likes
                max_likes_video = self.__video_response['items'][i]['id']
        return f"https://youtu.be/{max_likes_video}"



from googleapiclient.discovery import build
import isodate
import json
import os
from googleapiclient.errors import HttpError


class Video:
    __api_key: str = os.getenv('YT_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, video_id: str):

        try:
            self.__video_id = video_id
            self.__video_response = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=self.__video_id).execute()
            self.__video_title = self.__video_response['items'][0]['snippet']['title']
            self.__video_link = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.__view_count: int = self.__video_response['items'][0]['statistics']['viewCount']
            self.__like_count: int = self.__video_response['items'][0]['statistics']['likeCount']

        except:
            self.__video_title = None
            self.__video_link = None
            self.__view_count = None
            self.__like_count = None

    def __str__(self):
        return self.__video_title

    def __check_id(self, video_id):
        video_response = self.__youtube.videos().list(part='status', id=video_id).execute()
        result = video_response['pageInfo']['totalResults']

    @property
    def video_id(self):
        return self.__video_id

    @property
    def title(self):
        return self.__video_title

    @property
    def video_link(self):
        return self.__video_link

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count


class PLVideo:
    __api_key: str = os.getenv('YT_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, video_id, playlist_id):
        self.__video_id = video_id
        self.__video_response = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=self.__video_id).execute()
        self.__video_title = self.__video_response['items'][0]['snippet']['title']
        self.__video_link = f"https://www.youtube.com/watch?v={self.__video_id}"
        self.__view_count: int = self.__video_response['items'][0]['statistics']['viewCount']
        self.__like_count: int = self.__video_response['items'][0]['statistics']['likeCount']
        self.__playlist_id = playlist_id

    def __str__(self):
        return self.__video_title

    @property
    def video_id(self):
        return self.__video_id

    @property
    def video_title(self):
        return self.__video_title

    @property
    def video_link(self):
        return self.__video_link

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count

    @property
    def playlist_id(self):
        return self.__playlist_id

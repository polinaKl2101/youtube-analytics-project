import os
import json
from googleapiclient.discovery import build
import isodate


class Channel:
    """Класс для ютуб-канала"""
    __api_key: str = os.getenv('YT_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.__title = self.__channel['items'][0]['snippet']['title']
        self.__video_count = self.__channel['items'][0]['statistics']['videoCount']
        self.__url = f"https://www.youtube.com/channel/{channel_id}"
        self.__description = self.__channel['items'][0]['snippet']['description']
        self.__subscribers_count = self.__channel['items'][0]['statistics']['subscriberCount']
        self.__view_count = self.__channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"'{self.__title} ({self.__url})'"

    def __add__(self, other):
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        return int(self.subscribers) - int(other.subscribers)

    def __ge__(self, other):
        if int(self.subscribers) >= int(other.subscribers):
            return True
        else:
            return False

    def __lt__(self, other):
        if int(self.subscribers) < int(other.subscribers):
            return True
        else:
            return False

    def __gt__(self, other):
        if int(self.subscribers) > int(other.subscribers):
            return True
        else:
            return False

    def __le__(self, other):
        if int(self.subscribers) <= int(other.subscribers):
            return True
        else:
            return False

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    def to_json(self, name):
        data = {"channel_id": self.__channel_id,
                "title": self.__title,
                "url": self.__url,
                "description": self.__description,
                "subscribers_count": self.__subscribers_count,
                "view_count": self.__view_count}
        with open(name, "a+") as file:
            json.dump(data, file)

    @classmethod
    def get_service(cls):
        return cls.__youtube

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def video_count(self):
        return self.__video_count

    @property
    def url(self):
        return self.__url

    @property
    def subscribers(self):
        return self.__subscribers_count



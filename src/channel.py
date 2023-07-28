import os
import json
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.id = self.channel['items'][0]['id']
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriber_count = self.channel['items'][0]["statistics"]['subscriberCount']
        self.video_count = self.channel['items'][0]["statistics"]['videoCount']
        self.view_count = self.channel['items'][0]["statistics"]['viewCount']

    @classmethod
    def get_service(cls):
        """Получает объект для работы с YouTube API"""
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_name):
        """Записывает аттрибуты экземпляра класса в json файл"""
        with open(file_name, 'w') as f:
            json.dump(self.__dict__, f)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id: str):
        try:
            self.video_id = video_id
            self.video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id).execute()
            self.url: str = self.video['items'][0]['snippet']['thumbnails']["default"]['url']
            self.video_title: str = self.video['items'][0]['snippet']['title']
            self.view_count: int = self.video['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_id = video_id
            self.url: str = None
            self.title: str = None
            self.view_count: int = None
            self.like_count: int = None

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id

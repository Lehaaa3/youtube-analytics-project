import os
import isodate
from googleapiclient.discovery import build
import datetime

api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = youtube.playlists().list(id=self.playlist_id,
                                                 part='snippet',
                                                 maxResults=50,
                                                 ).execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        total_playlist_time = datetime.timedelta(days=0,
                                                 seconds=0,
                                                 microseconds=0,
                                                 milliseconds=0,
                                                 minutes=0,
                                                 hours=0,
                                                 weeks=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_playlist_time += duration
        return total_playlist_time

    def show_best_video(self):
        best_video = ""
        max_like = 0
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > max_like:
                best_video = video['id']
        return f"https://youtu.be/{best_video}"

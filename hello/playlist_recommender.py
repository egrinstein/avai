import boto3
import pandas as pd
from io import StringIO

from django.conf import settings
from django.conf.urls.static import static

PLAYLIST_PATH = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

class PlaylistRecommender:
    def __init__(self):
        s3 = boto3.client("s3", settings.AWS_S3_REGION_NAME)
        
        # get a handle on the object you want (i.e. your file)
        obj = s3.get_object(Key='label_to_song.csv',
                            Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        csv_text = obj['Body'].read().decode('utf-8')
        self.playlist = pd.read_csv(StringIO(csv_text))

    def recommend(self, labels):
        known_labels = [
            d for d in labels
            if d["label"] in list(self.playlist["[en]"])
        ]

        if known_labels:
            top_label = max(known_labels, key=lambda x: x["confidence"])["label"]
        else:
            top_label = 'else'
        playlist_id = self.playlist[self.playlist["[en]"] == top_label].iloc[0]["URI Filtr"]

        return playlist_id.split(":")[-1]


def recommend_playlist(labels):
    recommender = PlaylistRecommender()
    return recommender.recommend(labels)
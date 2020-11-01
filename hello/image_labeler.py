import boto3

BUCKET = "image-playlist"
KEY = "dog.jpg"
MAX_LABELS = 10
MIN_CONFIDENCE = 90
REGION = "eu-west-1"

class ImageLabeler:
    def __init__(
        self,
        bucket=BUCKET,
        max_labels=MAX_LABELS,
        min_confidence=MIN_CONFIDENCE,
        region=REGION
    ):

        self.bucket = bucket
        self.max_labels = max_labels
        self.min_confidence = min_confidence

        self.rekognition = boto3.client("rekognition", region)

    def detect(self, file_name_in_bucket):
        response = self.rekognition.detect_labels(
            Image={
                "S3Object": {
                    "Bucket": self.bucket,
                    "Name": file_name_in_bucket,
                }
            },
            MaxLabels=self.max_labels,
            MinConfidence=self.min_confidence,
        )
        return parse_response(response)


def parse_response(response):
    return [
        {
            "label": d["Name"],
            "confidence": int(d["Confidence"])
        }
        for d in response["Labels"]
    ]


def detect_image_labels(file_name_in_bucket):
    labeler = ImageLabeler()
    return labeler.detect(file_name_in_bucket)

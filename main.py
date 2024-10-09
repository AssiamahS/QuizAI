from moviepy.editor import TextClip, concatenate_videoclips
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def create_quiz_video(quiz_text, output_path):
    clips = []
    for question in quiz_text:
        clip = TextClip(question, fontsize=70, color='white').set_duration(5)
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_path, fps=24)

def upload_to_youtube(video_path, title, description, category="22", privacy="public"):
    youtube = build('youtube', 'v3', developerKey='YOUR_API_KEY')

    body = dict(
        snippet=dict(
            title=title,
            description=description,
            tags=["quiz", "AWS"],
            categoryId=category
        ),
        status=dict(
            privacyStatus=privacy
        )
    )

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media
    ).execute()

# Example usage
quiz = ["What is AWS?", "Name an AWS service", "What does S3 stand for?"]
output_video_path = "quiz_video.mp4"
create_quiz_video(quiz, output_video_path)
upload_to_youtube(output_video_path, "AWS Quiz", "Test your AWS knowledge!")

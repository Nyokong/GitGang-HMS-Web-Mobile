# tasks.py
from celery import shared_task
from moviepy.editor import VideoFileClip
import os
import ffmpeg

@shared_task
def segment_video(video_path, output_dir):
    with VideoFileClip(video_path) as video:
        duration = video.duration
        for i in range(0, int(duration), 5):
            segment_path = os.path.join(output_dir, f'segment_{i}.mp4')
            video.subclip(i, min(i + 5, duration)).write_videofile(segment_path, codec='libx264')

    # Create HLS playlist
    ffmpeg.input(os.path.join(output_dir, 'segment_%d.mp4'), pattern_type='sequence') \
          .output(os.path.join(output_dir, 'playlist.m3u8'), format='hls', hls_time=5, hls_list_size=0) \
          .run()

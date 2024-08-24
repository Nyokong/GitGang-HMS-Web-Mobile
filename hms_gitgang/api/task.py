from rest_framework.response import Response
from rest_framework import status

import logging
logger = logging.getLogger(__name__)

def my_task(initial_path, sub_folder, temp_dir):
    try:
        logger.info("Task is running")
        # Your task code here
        return {"message": "HLS playlist created successfully!"}
    except Exception as e:
        logger.error(f"Error during HLS creation: {e}")
        return {"error": "HLS creation failed"}

# opencv-python

import os

# movie py 
import moviepy.editor as mp

# settings
from django.conf import settings

# video compression module and adaptive streaming
import m3u8

def my_task(initial_path, sub_folder, temp_dir):
    try:
        print("Task is running: ")
        logger.info("Task is running")
        """
        # Load the video file
        video = mp.VideoFileClip(initial_path).resize(0.5)

        # Split the video into segments (e.g., 10 seconds each)
        segment_duration = 5
        segments = []
        
        print("now cutting into segments")
        for i in range(0, int(video.duration), segment_duration):
            # create the segments
            segment = video.subclip(i, min(i + segment_duration, video.duration))

            # Ensure audio is included and specify temp audio file location
            temp_audiofile = os.path.join(temp_dir, f'temp_audio_{i}.m4a')

            # create segment path
            segment_file = os.path.join(sub_folder, str(f'segment_{i}.ts'))
            
            segment.write_videofile(segment_file, codec='libx264',audio_codec='aac', temp_audiofile=temp_audiofile)

            segments.append(segment_file)

        # Create the M3U8 playlist
        playlist = m3u8.M3U8()
        for segment_file in segments:
            playlist.add_segment(m3u8.Segment(uri=segment_file, duration=segment_duration))

        # Save the playlist to a file in the subfolder
        playlist_file = os.path.join(sub_folder, 'playlist.m3u8')
        with open(playlist_file, 'w') as f:
            f.write(playlist.dumps())

        # Clean up temporary files
        for temp_file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, temp_file))
            """
        # {"error": "HLS creation failed"}
        return print(f'{"error": "HLS creation failed"}')
    except Exception as e:
        print(f"Error during HLS creation: {e}")
        logger.error(f"Error during HLS creation: {e}")
        return print(f'{"error": "HLS creation failed"}')


from rest_framework import serializers

def validate_file_size(file):
    max_size = 20 * 1024 * 1024 # 100 MB
    
    if file.size > max_size:
        print("video is too big")
        raise serializers.ValidationError(f'File size too big - should not exceed {max_size/(1024 * 1024)} MB.')

import pygame
import sys
import subprocess
from moviepy.editor import VideoFileClip

# Function to play a video
def play_video(path):
    clip = VideoFileClip(path)
    clip.preview()
    pygame.display.set_caption('Dialogue Scene')

# Play the video
play_video('img/caribou.mp4')
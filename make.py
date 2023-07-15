from moviepy.editor import *
from scripts.skins import get_skins, rt360render
import os

# Create a list to hold the ImageClips
clips = []

# Loop in reverse through the image filenames and create ImageClips
for i in range(10, 0, -1):
    filename = os.path.join("assets", str(i) + ".png")
    clip = ImageClip(filename, duration=2)
    clip = clip.resize((1080, 1920))
    clips.append(clip)

# Create clip from the backgrounds, clip will be used as the clip that will be rendered
final_clip = concatenate_videoclips(clips)

top_skins = get_skins()
top_skins.reverse()

# Make the pinned comment crediting the skin creators
with open(os.path.join("youtube", "comment.txt"), "w") as file:

    file.write(f"SKINS:\n")
    for i in range(9, -1, -1):
        # If - is in the string it means the user is unkown (by their choice)
        if '—' in top_skins[i][3]:
            file.write(f"{i+1}: by an unkown user: {top_skins[i][4]}\n")
        else:
            file.write(f"{i+1} by {top_skins[i][3]}: {top_skins[i][4]}\n")


# Renders the top 10 skins
for i in range(10):
    rt360render(top_skins[i][0], top_skins[i][2], 0, i)

# Image clip, will store skin renders
image_clip = []

# Make image clips from rendered skins
cur_start = 0
for i in range(10):
    for j in range(0, 360, 180):
        image = ImageClip(f"{i} {j}.png", duration=1).set_start(cur_start).set_position((0, 810))
        image_clip.append(image)
        cur_start += 1

# Composite final clip and the skins
final_clip = CompositeVideoClip([final_clip, *image_clip])

# Takes the music file which is 29 secs and gets from 3 secs to 23 secs because the final vid is 20 secods and 3 to 23 is prefered 
audioclip = AudioFileClip(os.path.join("assets", "music.mp3")).subclip(t_start=3, t_end=23)
new_audioclip = CompositeAudioClip([audioclip])

# Change the audio to the music
final_clip.audio = new_audioclip

# Render the video (In 1 fps for a super fast render)
final_clip.write_videofile(os.path.join("youtube", "Top Skins.mp4"), fps=1)

# Remove skin renders from PC after video render is done
for i in range(10):
    for j in range(0, 360, 180):
        try:
            os.remove(f"{i} {j}.png")
        except:
            pass
# %%
from moviepy.editor import VideoFileClip
import pytube
from pytube import YouTube
from moviepy.editor import concatenate_videoclips
import pygame
import os
import time
import cv2 
import matplotlib.pyplot as plt 
# from upload_video import upload_video
#from youtube_uploader_selenium import YouTubeUploader
#import json 

# %%
def make_and_upload_full_match(season, match_date, court_number, match_number, players_a, players_b, youtube_link_list, clip_info_list):
    start = time.time()
    
    title = f"{season} {match_date} court{court_number} match{match_number}"
    description = f"{players_a[0]} {players_a[1]} vs {players_b[0]} {players_b[1]}"
    file_name = f"{season}-{match_date}-court{court_number}-match{match_number}-{players_a[0]}-{players_a[1]}vs{players_b[0]}-{players_b[1]}"
    file_path = "videos/" + file_name + ".mp4"
    
    print("== title:", title)
    print("- Description:", description)
    
    # video_metadata = {
    #     "title": title,
    #     "description": description
    # }
    
    # print("- youtube metadata: ", video_metadata)
    
    # video_metadata_json = json.dumps(video_metadata, indent = 2)
    
    # with open(f"videos/{file_name}.json", "w") as outfile:
    #     outfile.write(video_metadata_json)
    
    # metadata_path = f"videos/{file_name}.json"
    
    # print("- metadata for youtube video is saved to: " + metadata_path)
    
    clip_list = []
        
    for i in range(0, len(youtube_link_list)): 
        video_id = youtube_link_list[i].split("=")[-1]
        
        print("")
        print(f"- Processing video: {video_id}...")
        
        if os.path.isfile(f"videos/video_{video_id}.mp4") == False:
            yt = YouTube(youtube_link_list[i])
            yt.streams.get_highest_resolution().download("videos", f"video_{video_id}.mp4")
            
            print(f"video_{video_id}.mp4 is downloaded")
        else: print(f"video_{video_id}.mp4 alread exist! Skip downloading this file.")
        
        clip_info = clip_info_list[i]
        
        start_string = clip_info[0]
        start_sec = int(start_string.split(":")[0]) * 60 + int(start_string.split(":")[1]) * 1
        
        end_string = clip_info[1]
        end_sec = int(end_string.split(":")[0]) * 60 + int(end_string.split(":")[1]) * 1 - 1
        
        try:
            clip_list.append(VideoFileClip(f"videos/video_{video_id}.mp4").subclip(start_sec, end_sec))
        except:
            print(f"Downloaded {video_id} is corrupted. Start redownloading the video.")
            
            yt = YouTube(youtube_link_list[i])
            yt.streams.get_highest_resolution().download("videos", f"video_{video_id}.mp4")
            
            print(f"video_{video_id}.mp4 is downloaded")
            
            clip_list.append(VideoFileClip(f"videos/video_{video_id}.mp4").subclip(start_sec, end_sec))
        print(f"subclip: ({start_sec // 60}:{start_sec % 60} ~ {end_sec // 60}:{end_sec % 60})")
        
    final_clip = concatenate_videoclips(clip_list)
    
    print("")
    print(f"- match duration: {int(final_clip.duration // 60)} min {int(final_clip.duration % 60)} sec")

    start_frame = final_clip.get_frame(0)
    end_frame = final_clip.get_frame(int(final_clip.duration) - 1)
    
    print("- start frame: ")
    plt.imshow(start_frame)
    plt.axis("off")
    plt.show() 
    
    print("- end frame: ")
    plt.imshow(end_frame)
    plt.axis("off")
    plt.show() 

    final_clip.write_videofile(f"videos/{file_name}.mp4")
    print("- save match video to: ", file_path)
    
    vid = cv2.VideoCapture(f"videos/{file_name}.mp4")
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(f"- match video resolution: {height} x {width}")


    #uploader = YouTubeUploader(file_path, metadata_path)
    #was_video_uploaded, video_id = uploader.upload()
    
    #video_id = upload_video(file_path, title, description)
    
    #print("- match video uploaded to youtube with video id: ", video_id) 
    
    end = time.time()
    print(f"- took {(end - start) / 60} minutes")
    print(" ")
    
    #return video_id 
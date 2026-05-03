from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from tkinter import Tk, filedialog

def choose_path():
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory()

def download_video(url, path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"Downloading: {yt.title}")
        
        stream = yt.streams.filter(progressive=True, file_extension="mp4")\
                           .order_by("resolution")\
                           .desc()\
                           .first()
        
        stream.download(output_path=path)
        print("Done!\n")
    except Exception as e:
        print(f"Error: {e}")

def download_audio(url, path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"Downloading: {yt.title}")
        
        stream = yt.streams.get_audio_only()
        stream.download(output_path=path)
        
        print("Done!\n")
    except Exception as e:
        print(f"Error: {e}")

def download_playlist(url, path):
    try:
        pl = Playlist(url)
        print(f"Playlist: {pl.title}")
        
        for vid in pl.videos:
            try:
                print(f"Downloading: {vid.title}")
                vid.streams.get_audio_only().download(output_path=path)
            except Exception as e:
                print(f"Skipped: {e}")
        
        print("Playlist finished!\n")
    except Exception as e:
        print(f"Error: {e}")

while True:
    try:
        category_num = int(input("Video (0) / Audio (1) / Playlist (2): "))
    except ValueError:
        print("Please enter 0, 1, or 2")
        continue

    url = input("URL: ")
    path = choose_path()

    if not path:
        print("No folder selected!")
        continue

    if category_num == 0:
        download_video(url, path)
    elif category_num == 1:
        download_audio(url, path)
    elif category_num == 2:
        download_playlist(url, path)
    else:
        print("Invalid choice")
        continue

    end = input("Download another? (y/n): ").lower()
    if end != "y":
        break
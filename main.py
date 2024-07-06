from yt_dlp import YoutubeDL
import re
import os
import subprocess
import msvcrt  # Only available on Windows
import logging
import ctypes
import sys
import datetime
import time

NAME = 'YouTube QuickSave'
VER = '1.1.240623'
TCRED = '\033[91m'
TCGREEN = '\033[92m'
TCGRAY = '\033[0m'
TCBLUE = '\033[94m'

mkvmerge_path = r'C:\Program Files\MKVToolNix\mkvmerge.exe'  # Path to mkvmerge

# Configure logging
logs_folder = 'Logs' # Logs folder name
os.makedirs(logs_folder, exist_ok=True) # Create a 'Logs' folder if it doesn't exist
today_date = datetime.date.today().strftime('%Y-%m-%d') # Get today's date in YYYY-MM-DD format
log_file = os.path.join(logs_folder, f"{today_date}.log") # Construct the log file path with today's date
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_youtube_url(url):
    # Check if URL is a valid YouTube video URL
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return re.match(youtube_regex, url) is not None

def download_video(url):
    # Download YouTube video with subtitles
    output_dir = os.getcwd()  # Get current working directory
    ydl_opts = {
        'format': '(bestvideo[height<=1080]+bestaudio)/best[height<=1080]',  # Minimum 720p quality
        'merge_output_format': 'webm',  # Output format for merged video
        'writesubtitles': True,  # Write subtitles to separate files
        'writeautomaticsub': True,  # Write automatically generated subtitles
        'subtitleslangs': ['en', 'ar', 'ru', 'ar-en', 'ru-en'],  # Languages for subtitles
        'skip_download': False,  # Download the video
        'outtmpl': output_dir + '/%(title)s/%(title)s.%(ext)s',  # Output template for downloaded files
        'postprocessors': [{
            'key': 'FFmpegMetadata',
            'add_metadata': True,
            'add_chapters': True,
        }],
        'quiet': True,  # Run quietly
        'no_warnings': True,  # Suppress warnings
    }

    # Download video with specified options
    with YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"{TCBLUE}STEP 1 {TCGRAY}Downloading necessary file(s)")
            ydl.download([url])
            # Remove the initial message
            sys.stdout.write("\033[F")  # Move cursor up one line
            sys.stdout.write("\033[K")  # Clear the line
            print(f"{TCBLUE}STEP 1 {TCGREEN}File(s) successfully downloaded{TCGRAY}")
            logging.info(f"Downloaded video from {url}")
            rename_subtitles(output_dir)  # Rename dual-language subtitles
        except Exception as e:
            logging.error(f"Error downloading {url}: {e}")
    
def rename_subtitles(output_dir):
    print(f"{TCBLUE}STEP 2 {TCGRAY}Preparing file(s) to be merged")
    sys.stdout.write("\033[F")  # Move cursor up one line
    sys.stdout.write("\033[K")  # Clear the line
    print(f"{TCBLUE}STEP 2 {TCGREEN}File(s) successfully prepared for merging{TCGRAY}")
    # Rename dual-language subtitle files
    for dirpath, _, filenames in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith('.ar-en.vtt'):
                base_name = os.path.splitext(filename)[0]
                new_filename = base_name.replace('.ar-en', '.ar') + '.vtt'
                os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
                logging.info(f"Renamed {filename} to {new_filename}")
            elif filename.endswith('.ru-en.vtt'):
                base_name = os.path.splitext(filename)[0]
                new_filename = base_name.replace('.ru-en', '.ru') + '.vtt'
                os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
                logging.info(f"Renamed {filename} to {new_filename}")

def merge_files(video_file, subtitle_files, output_file):
    # Merge video and subtitle files into a single MKV file
    if not output_file.endswith('.mkv'):
        output_file += '.mkv'  # Ensure output file ends with .mkv

    language_tracks = []  # Store language-specific subtitle tracks

    # Add English subtitle track first to ensure it's default
    for subtitle_file in subtitle_files:
        if subtitle_file.endswith('.en.vtt'):
            language_tracks.extend(['--track-name', '0:English', '--language', '0:eng', '--default-track', '0:yes', subtitle_file])

    # Add other language subtitle tracks
    for subtitle_file in subtitle_files:
        if subtitle_file.endswith('.ar.vtt'):
            language_tracks.extend(['--track-name', '0:العربية', '--language', '0:ara', '--default-track', '0:no', subtitle_file])
        elif subtitle_file.endswith('.ru.vtt'):
            language_tracks.extend(['--track-name', '0:Русский', '--language', '0:rus', '--default-track', '0:no', subtitle_file])

    command = [mkvmerge_path, '-o', output_file, video_file] + language_tracks  # Command to merge files

    # Execute command and handle errors
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info(f'Merged files into {output_file} successfully!')
        print(f"{TCBLUE}STEP 3 {TCGRAY}Merging file(s)")
        os.remove(video_file)  # Delete input video file
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear the line
        print(f"{TCBLUE}STEP 3 {TCGREEN}File(s) successfully merged{TCGRAY}")
        for subtitle_file in subtitle_files:
            os.remove(subtitle_file)  # Delete input subtitle files
        logging.info('Input files deleted.')
        print(f"{TCBLUE}STEP 4 {TCGRAY}Deleting temp file(s)")
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear the line
        print(f"{TCBLUE}STEP 4 {TCGREEN}Temp file(s) successfully deleted{TCGRAY}")
        print(f"\nOutput : {output_file}\n")
    except subprocess.CalledProcessError as e:
        logging.error(f'Error occurred: {e}')
    except Exception as e:
        logging.error(f'Error occurred during file deletion: {e}')

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console screen for Windows and Unix-like systems
    
def main():
    while True:
        print(f"{TCGREEN}Welcome to {NAME} v{VER}{TCGRAY}")
        youtube_url = input(f"Please Enter a valid YouTube URL ({TCBLUE}Video or Playlist{TCGRAY}): \n")
        print("")
        
        if is_youtube_url(youtube_url):
            download_video(youtube_url)  # Download video with subtitles

            directories = [d for d in os.listdir('.') if os.path.isdir(d) and d != logs_folder]  # List all directories
            
            for directory in directories:
                video_files = [file for file in os.listdir(directory) if file.endswith('.webm')]  # Check for .webm files
                
                if not video_files:
                    logging.info(f'No .webm video files found in directory {directory}.')
                else:
                    video_file = os.path.join(directory, video_files[0])
                    subtitle_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.vtt')]
                    output_file = os.path.splitext(video_file)[0] + '.mkv'  # Output file name

                    merge_files(video_file, subtitle_files, output_file)  # Merge files

            print(f"Press {TCGREEN}Enter{TCGRAY} to start again or {TCRED}Esc{TCGRAY} to close...")
            while True:
                key = msvcrt.getch()
                if key == b'\r':  # Enter key
                    clear_console()  # Clear the console screen
                    break
                elif key == b'\x1b':  # Esc key
                    print("Exiting...")
                    return
        else:
            print(f"{TCRED}Invalid YouTube URL. Please enter a valid URL from youtube.com.{TCGRAY}")
            input(f"Press {TCGREEN}Enter{TCGRAY} to continue...")  # Prompt to continue
            clear_console()  # Clear the console screen

if __name__ == "__main__":
    main()
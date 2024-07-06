import os
import re
import subprocess
import logging
import datetime
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext, font, filedialog
from yt_dlp import YoutubeDL

NAME = 'YouTube QuickSave'
VER = '1.4.240705'

# Configure logging
logs_folder = 'Logs'
os.makedirs(logs_folder, exist_ok=True)
today_date = datetime.date.today().strftime('%Y-%m-%d')
log_file = os.path.join(logs_folder, f"{today_date}.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class YouTubeDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(NAME + " v" + VER)
        self.geometry("600x350")  # Increased height to accommodate new elements
        
        # Set favicon
        self.iconbitmap('favicon.ico')  # Ensure this file is in the same directory or provide full path

        custom_font = font.Font(size=9)

        # MKVMerge path input
        mkvmerge_frame = tk.Frame(self)
        mkvmerge_frame.pack(pady=5)

        self.mkvmerge_label = tk.Label(mkvmerge_frame, text="MKVMerge Path:", font=custom_font, width=15, anchor='w')
        self.mkvmerge_label.pack(side=tk.LEFT)

        self.mkvmerge_entry = tk.Entry(mkvmerge_frame, width=50, font=custom_font)
        self.mkvmerge_entry.pack(side=tk.LEFT, padx=(5, 5))
        self.mkvmerge_entry.insert(0, r'C:\Program Files\MKVToolNix\mkvmerge.exe')

        self.browse_mkvmerge_button = tk.Button(mkvmerge_frame, text="Browse", command=self.browse_mkvmerge, font=custom_font, width=10)
        self.browse_mkvmerge_button.pack(side=tk.LEFT)

        # Download directory input
        download_dir_frame = tk.Frame(self)
        download_dir_frame.pack(pady=5)

        self.download_dir_label = tk.Label(download_dir_frame, text="Download Directory:", font=custom_font, width=15, anchor='w')
        self.download_dir_label.pack(side=tk.LEFT)

        self.download_dir_entry = tk.Entry(download_dir_frame, width=50, font=custom_font)
        self.download_dir_entry.pack(side=tk.LEFT, padx=(5, 5))
        self.download_dir_entry.insert(0, os.getcwd())  # Default to current working directory

        self.browse_download_dir_button = tk.Button(download_dir_frame, text="Browse", command=self.browse_download_dir, font=custom_font, width=10)
        self.browse_download_dir_button.pack(side=tk.LEFT)

        # Frame for URL input and download button
        input_frame = tk.Frame(self)
        input_frame.pack(pady=5)

        # YouTube URL Label
        self.url_label = tk.Label(input_frame, text="YouTube URL:", font=custom_font, width=15, anchor='w')
        self.url_label.pack(side=tk.LEFT, padx=(0, 5))

        self.url_entry = tk.Entry(input_frame, width=50, font=custom_font)
        self.url_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.url_entry.bind('<KeyRelease>', self.update_button_text)

        self.action_button = tk.Button(input_frame, text="Paste", command=self.button_action, width=10, font=custom_font)
        self.action_button.pack(side=tk.LEFT)

        # Console screen
        self.console = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=60, bg="black", fg="white", font=custom_font)
        self.console.pack(pady=10)

    def browse_mkvmerge(self):
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select mkvmerge executable",
            filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
        )
        if filename:
            self.mkvmerge_entry.delete(0, tk.END)
            self.mkvmerge_entry.insert(0, filename)

    def browse_download_dir(self):
        directory = filedialog.askdirectory(
            initialdir="/",
            title="Select download directory"
        )
        if directory:
            self.download_dir_entry.delete(0, tk.END)
            self.download_dir_entry.insert(0, directory)

    def update_button_text(self, event=None):
        if self.url_entry.get().strip():
            self.action_button.config(text="Download")
        else:
            self.action_button.config(text="Paste")

    def button_action(self):
        if not self.url_entry.get().strip():
            self.paste_from_clipboard()
        else:
            self.download_video()

    def paste_from_clipboard(self):
        clipboard_content = self.clipboard_get()
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, clipboard_content)
        self.update_button_text()

    def console_print(self, message):
        self.console.insert(tk.END, message + '\n')
        self.console.see(tk.END)
        self.update_idletasks()

    def is_youtube_url(self, url):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        return re.match(youtube_regex, url) is not None

    def download_video(self):
        self.console.delete('1.0', tk.END)
        
        url = self.url_entry.get()
        if not self.is_youtube_url(url):
            messagebox.showerror("Invalid URL", "Please enter a valid YouTube URL.")
            return

        output_dir = self.download_dir_entry.get()  # Get the selected download directory
        ydl_opts = {
            'format': '(bestvideo[height<=1080]+bestaudio)/best[height<=1080]',
            'merge_output_format': 'webm',
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'ar', 'ru', 'ar-en', 'ru-en'],
            'skip_download': False,
            'outtmpl': os.path.join(output_dir, '%(title)s', '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
                'add_chapters': True,
            }],
            'quiet': True,
            'no_warnings': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                self.console_print("Downloading necessary file(s)")
                ydl.download([url])
                self.console_print("File(s) successfully downloaded")
                logging.info(f"Downloaded video from {url}")
                self.rename_subtitles(output_dir)
                self.process_downloaded_files(output_dir)
            except Exception as e:
                logging.error(f"Error downloading {url}: {e}")
                messagebox.showerror("Download Error", f"An error occurred while downloading the video: {e}")

    def rename_subtitles(self, output_dir):
        self.console_print("Preparing file(s) to be merged")
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
        self.console_print("File(s) successfully prepared for merging")

    def merge_files(self, video_file, subtitle_files, output_file):
        if not output_file.endswith('.mkv'):
            output_file += '.mkv'

        language_tracks = []

        for subtitle_file in subtitle_files:
            if subtitle_file.endswith('.en.vtt'):
                language_tracks.extend(['--track-name', '0:English', '--language', '0:eng', '--default-track', '0:yes', subtitle_file])

        for subtitle_file in subtitle_files:
            if subtitle_file.endswith('.ar.vtt'):
                language_tracks.extend(['--track-name', '0:العربية', '--language', '0:ara', '--default-track', '0:no', subtitle_file])
            elif subtitle_file.endswith('.ru.vtt'):
                language_tracks.extend(['--track-name', '0:Русский', '--language', '0:rus', '--default-track', '0:no', subtitle_file])

        mkvmerge_path = self.mkvmerge_entry.get()
        command = [mkvmerge_path, '-o', output_file, video_file] + language_tracks

        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logging.info(f'Merged files into {output_file} successfully!')
            self.console_print("Merging file(s)")
            os.remove(video_file)
            self.console_print("File(s) successfully merged")
            for subtitle_file in subtitle_files:
                os.remove(subtitle_file)
            logging.info('Input files deleted.')
            self.console_print("Deleting temp file(s)")
            self.console_print("Temp file(s) successfully deleted")
            self.console_print(f"\nOutput : {output_file}\n")
        except subprocess.CalledProcessError as e:
            logging.error(f'Error occurred: {e}')
            messagebox.showerror("Merge Error", f"An error occurred while merging the files: {e}")
        except Exception as e:
            logging.error(f'Error occurred during file deletion: {e}')
            messagebox.showerror("File Deletion Error", f"An error occurred while deleting temporary files: {e}")

    def process_downloaded_files(self, output_dir):
        directories = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d)) and d != logs_folder]

        for directory in directories:
            video_files = [file for file in os.listdir(os.path.join(output_dir, directory)) if file.endswith('.webm')]

            if not video_files:
                logging.info(f'No .webm video files found in directory {directory}.')
            else:
                video_file = os.path.join(output_dir, directory, video_files[0])
                subtitle_files = [os.path.join(output_dir, directory, file) for file in os.listdir(os.path.join(output_dir, directory)) if file.endswith('.vtt')]
                output_file = os.path.splitext(video_file)[0] + '.mkv'

                self.merge_files(video_file, subtitle_files, output_file)


if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.resizable(False, False)
    app.mainloop()
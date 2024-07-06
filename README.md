![YouTube-QuickSave GUI](https://i.imgur.com/ATyeZb6.png)

# YouTube QuickSave v1.4.240705

YouTube QuickSave is a user-friendly application for downloading YouTube videos along with their subtitles. It offers a straightforward interface for downloading videos, renaming subtitle files, and merging them into a single MKV file using MKVMerge.

## Features

- Download YouTube videos in the best available format (up to 1080p).
- Download and merge chapters into the video.
- Automatically download subtitles in multiple languages.
- Rename subtitle files to ensure correct language codes.
- Merge video and subtitle files into a single MKV file.
- Log activities for later reference.

## Requirements

- Python 3.x
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [MKVToolNix](https://mkvtoolnix.download/) (mkvmerge)
- [ffmpeg](https://ffmpeg.org/)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/IsaacSabir/YouTube-QuickSave.git
    cd YouTubeQuickSave
    ```

2. **Install required Python packages:**
    ```bash
    pip install yt-dlp
    ```

3. **Download and install MKVToolNix:**
    - Download and install MKVToolNix from [here](https://mkvtoolnix.download/downloads.html).
    - Ensure `mkvmerge.exe` is located in `C:\Program Files\MKVToolNix\mkvmerge.exe` or update the path in the script accordingly.

4. **Install ffmpeg:**

    - Download and install ffmpeg from [here](https://ffmpeg.org/download.html).
    - Ensure `ffmpeg` is added to your system's PATH.

## Usage

1. **Run the application:**
    ```bash
    python main.py
    ```

2. **Set MKVMerge Path:**
    - Click on "Browse" next to the MKVMerge Path field.
    - Select the `mkvmerge.exe` executable from the MKVToolNix installation directory.

3. **Set Download Directory:**
    - Click on "Browse" next to the Download Directory field.
    - Select or create a directory where you want to save downloaded videos.

4. **Download a YouTube video:**
    - Paste the YouTube URL into the YouTube URL field.
    - Click the "Download" button.

5. **View Console Output:**
    - The console at the bottom of the application will display the download progress and status.

## How It Works

1. **Download Video and Subtitles:**

    The script uses yt-dlp to download the YouTube video along with subtitles in specified languages.

2. **Rename Subtitles:**

    The script renames dual-language subtitles for easier processing.

3. **Merge Files:**

    The script uses `mkvmerge` to merge the video and subtitle files into a single MKV file, ensuring English subtitles are set as default.

4. **Clean Up:**

    Temporary files are deleted after merging.

## Logging

- Logs are stored in the `Logs` directory.
- Each log file is named with the current date (`YYYY-MM-DD.log`) (e.g., `2024-07-05.log`).

## Known Issues

- Ensure you have the necessary permissions to write to the directories.
- Make sure the paths for `mkvmerge` and `ffmpeg` are correctly set.

## Troubleshooting

- Ensure you have a stable internet connection and not using VPN.
- Verify that the MKVMerge path is correctly set to the `mkvmerge.exe` file.
- Check the logs for detailed error messages if something goes wrong.

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [MKVToolNix](https://mkvtoolnix.download/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

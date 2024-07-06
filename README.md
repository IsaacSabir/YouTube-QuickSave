# YouTube QuickSave

**Version**: 1.1.240623

**Description**: YouTube QuickSave is a Python script designed to download YouTube videos along with subtitles in various languages, and merge them into a single MKV file.

## Features

- Downloads YouTube videos in 1080p quality (or lower if not available).
- Downloads chapters and merge them into the video.
- Downloads subtitles in multiple languages: English, Arabic, Russian (request more languages if you want).
- Merges video and subtitle files into a single MKV file using MKVToolNix.

## Requirements

- Python 3.x
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [MKVToolNix](https://mkvtoolnix.download/) (mkvmerge)
- [ffmpeg](https://ffmpeg.org/)

## Installation

1. **Clone the repository or download the script:**

    ```sh
    git clone https://github.com/IsaacSabir/YouTube-QuickSave.git
    cd YouTube-QuickSave
    ```

2. **Install the required Python packages:**

    ```sh
    pip install yt-dlp
    ```

3. **Install MKVToolNix:**

    - Download and install MKVToolNix from [here](https://mkvtoolnix.download/downloads.html).
    - Ensure `mkvmerge.exe` is located in `C:\Program Files\MKVToolNix\mkvmerge.exe` or update the path in the script accordingly.

4. **Install ffmpeg:**

    - Download and install ffmpeg from [here](https://ffmpeg.org/download.html).
    - Ensure `ffmpeg` is added to your system's PATH.

## Usage

1. **Run the script:**

    ```sh
    python main.py
    ```

2. **Follow the prompts:**

    - Enter a valid YouTube URL (video or playlist).
    - The script will download the video and subtitles, then merge them into an MKV file.

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
- Each log file is named with the current date (`YYYY-MM-DD.log`).

## Known Issues

- Ensure you have the necessary permissions to write to the directories.
- Make sure the paths for `mkvmerge` and `ffmpeg` are correctly set.

## Contributing

Feel free to fork the project, make improvements, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

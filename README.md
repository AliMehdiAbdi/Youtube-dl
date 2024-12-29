# YouTube-dl

This project allows you to download YouTube videos along with their thumbnails using the `yt_dlp` library. The script enables you to specify video and audio formats and merges them into a single container format. Additionally, it saves the thumbnail of the video in the specified output directory.

## Features

- Download YouTube videos in specified video and audio formats.
- Merge video and audio streams into a single container.
- Embed the thumbnail in the downloaded video.
- Save the thumbnail separately after the video download is complete.

## Requirements

- Python 3.x
- `yt_dlp` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/AliMehdiAbdi/YouTube-dl.git
    cd YouTube-dl
    ```

2. Install the required Python packages:

    ```sh
    pip install yt_dlp
    ```

## Netscape Formatted Cookies

1. Install a Browser extension like EditThisCookie or Get cookies.txt

2. Export the cookies for YouTube in the Netscape format and save them as a `.txt` file (e.g., `cookies.txt`).

3. When running the script, provide the path to the cookies file when prompted:

```sh
Enter the Cookies File Path (leave blank if not applicable): /path/to/cookies.txt
```

The script will use the provided cookies file to authenticate your session and download the video.

## Usage

1. Open the terminal and navigate to the project directory.

2. Run the script:

    ```sh
    python ytdl.py
    ```

3. Follow the prompts:

    - Enter the YouTube video URL.
    - Enter the desired output path for the downloaded files.
    - (Optional) Enter the path to the cookies file if needed.

4. The script will download the video, merge the video and audio streams, embed the thumbnail, and save the thumbnail separately in the specified output directory.

## Example

```sh
Enter the YouTube video URL: https://www.youtube.com/watch?v=example
Enter the desired output path: ~/youtube/
Enter the Cookies File Path (leave blank if not applicable): /path/to/cookies.txt

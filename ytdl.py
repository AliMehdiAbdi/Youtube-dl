import subprocess
import yt_dlp
import re

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']} ETA {d['_eta_str']}")
    elif d['status'] == 'finished':
        print("Download completed")

def download_thumbnail(url, output_path, cookies_path=None):
    ydl_opts = {
        'skip_download': True,
        'writethumbnail': True,
        'outtmpl': f'{output_path}/thumbnail.%(ext)s'
    }
    
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading thumbnail...")
            ydl.download([url])
    except Exception as e:
        print(f"An error occurred while downloading thumbnail: {e}")

def download_video(url, output_path, video_format, audio_format, container, cookies_path=None):
    ydl_opts = {
        'format': f"{video_format}+{audio_format}",
        'merge_output_format': container,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'embedthumbnail': True
    }
    
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading video...")
            ydl.download([url])
    except Exception as e:
        print(f"An error occurred while downloading video: {e}")

def validate_url(url):
    youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$')
    return re.match(youtube_regex, url) is not None

def get_formats(url, cookies_path=None):
    ydl_opts = {'quiet': True}
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        video_formats = [f for f in formats if 'vcodec' in f and f['vcodec'] != 'none']
        audio_formats = [f for f in formats if 'acodec' in f and f['acodec'] != 'none']
    return video_formats, audio_formats

def main():
    url = input("Enter the YouTube video URL: ")
    output_path = "youtube/"
    cookies_path = input("Enter the Cookies File Path (leave blank if not applicable): ")
    cookies_path = cookies_path if cookies_path else None
    
    if not validate_url(url):
        print("Invalid YouTube URL.")
        return

    download_thumbnail(url, output_path, cookies_path)

    video_formats, audio_formats = get_formats(url, cookies_path)
    
    print("\nAvailable Video Formats:")
    for vf in video_formats:
        size = f"{vf['filesize'] // (1024 * 1024)} MB" if 'filesize' in vf else 'Unknown size'
        print(f"{vf['format_id']}: {vf['ext']} - {vf['resolution']} - {vf.get('tbr', 'N/A')}k - {size}")

    print("\nAvailable Audio Formats:")
    for af in audio_formats:
        size = f"{af['filesize'] // (1024 * 1024)} MB" if 'filesize' in af else 'Unknown size'
        print(f"{af['format_id']}: {af['ext']} - {af['abr']}k - {size}")
        
    video_format = input("\nEnter Video Format ID: ")
    audio_format = input("Enter Audio Format ID: ")
    container = input("Enter Container Format: ")
    
    download_video(url, output_path, video_format, audio_format, container, cookies_path)

if __name__ == "__main__":
    main()

import subprocess
import yt_dlp
import re

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']} ETA {d['_eta_str']}")
    elif d['status'] == 'finished':
        print("Download completed")

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
    return video_formats, audio_formats, info_dict['duration']

def format_filesize(filesize):
    if filesize is None:
        return 'Unknown size'
    for unit in ['B', 'KiB', 'MiB', 'GiB']:
        if filesize < 1024:
            return f"{filesize:.2f} {unit}"
        filesize /= 1024
    return f"{filesize:.2f} TiB"

def approximate_size(bitrate_kbps, duration_sec):
    if bitrate_kbps is None or duration_sec is None:
        return 'Unknown size'
    filesize_bytes = (bitrate_kbps * 1000 / 8) * duration_sec
    return format_filesize(filesize_bytes)

def main():
    url = input("Enter the YouTube video URL: ")
    output_path = "youtube/"
    cookies_path = input("Enter the Cookies File Path (leave blank if not applicable): ")
    cookies_path = cookies_path if cookies_path else None
    
    if not validate_url(url):
        print("Invalid YouTube URL.")
        return

    video_formats, audio_formats, duration = get_formats(url, cookies_path)
    
    print("\nAvailable Video Formats:")
    for vf in video_formats:
        filesize = vf.get('filesize_approx') or vf.get('filesize')
        if filesize is None:
            filesize = approximate_size(vf.get('tbr'), duration)
        else:
            filesize = format_filesize(filesize)
        print(f"{vf['format_id']}: {vf['ext']} - {vf['resolution']} - {vf.get('tbr', 'N/A')}k - {filesize}")

    print("\nAvailable Audio Formats:")
    for af in audio_formats:
        filesize = af.get('filesize_approx') or af.get('filesize')
        if filesize is None:
            filesize = approximate_size(af.get('abr'), duration)
        else:
            filesize = format_filesize(filesize)
        print(f"{af['format_id']}: {af['ext']} - {af['abr']}k - {filesize}")
        
    video_format = input("\nEnter Video Format ID: ")
    audio_format = input("Enter Audio Format ID: ")
    container = input("Enter Container Format: ")
    
    download_video(url, output_path, video_format, audio_format, container, cookies_path)
    download_thumbnail(url, output_path, cookies_path)

if __name__ == "__main__":
    main()

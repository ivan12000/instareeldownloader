import instaloader
import sys
import os

def download_instagram_reel(url, output_path):
    # Ensure URL ends with a "/"
    if not url.endswith('/'):
        url += '/'

    L = instaloader.Instaloader(dirname_pattern=output_path, filename_pattern='{shortcode}')

    try:
        print(f"Extracting shortcode from URL: {url}")
        shortcode = url.split("/")[-2]
        print(f"Shortcode extracted: {shortcode}")

        print("Attempting to download post...")
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        print(f"Post information: {post}")

        print(f"Downloading post to {output_path}...")
        L.download_post(post, target=output_path)
        
        reel_file = os.path.join(output_path, f"{post.shortcode}.mp4")
        if os.path.exists(reel_file):
            print(f"Reel downloaded successfully: {reel_file}")
            return reel_file
        else:
            print("Download completed, but reel file not found.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <Instagram Reel URL>")
        sys.exit(1)
    
    instagram_url = sys.argv[1]
    output_directory = '.'

    print(f"Starting download for URL: {instagram_url}")
    reel_file = download_instagram_reel(instagram_url, output_directory)
    if reel_file:
        print(f"Downloaded Instagram reel: {reel_file}")
    else:
        print("Failed to download the Instagram reel.")

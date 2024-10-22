import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re

BASE_URL = "https://downloads.khinsider.com"

def validate_url(url):
    return "//downloads.khinsider.com/game-soundtracks/album/" in url

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def download_file(url, file_path, file_size):
    if os.path.exists(file_path):
        if os.path.getsize(file_path) == file_size:
            print(f'[skipping] "{os.path.basename(file_path)}" already downloaded.')
            return

    print(f"[downloading] {os.path.basename(file_path)} [{file_size/1000000:.2f}MB]")
    response = requests.get(url, stream=True)
    with open(file_path, "wb") as output:
        for chunk in response.iter_content(chunk_size=8192):
            output.write(chunk)
    print(f'[done] "{os.path.basename(file_path)}"')

def fetch_from_url(url):
    if not validate_url(url):
        print(f"[error] Invalid url: {url}")
        return

    print(f"[info] Url found: {url}")

    base_dir = "downloads"
    dir_name = os.path.join(base_dir, url.split("/")[-1].strip())

    os.makedirs(dir_name, exist_ok=True)

    print("[info] crawling for links...")

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    song_list = soup.find(id="songlist")
    rows = song_list.find_all("tr")
    song_map = {}

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue  # Skip rows that don't have enough columns

        if len(cols) >= 9:
            track_number = cols[1].get_text(strip=True)
            subtrack_number = cols[2].get_text(strip=True)  # Remove trailing dot
            song_anchor = cols[3].find("a")
        elif len(cols) >= 3:
            track_number = ""
            subtrack_number = cols[1].get_text(strip=True)  # Remove trailing dot
            song_anchor = cols[2].find("a")
        else:
            continue

        if song_anchor and "mp3" in song_anchor.get("href", ""):
            href = BASE_URL + song_anchor.get("href")
            song_name = song_anchor.get_text(strip=True)
            if track_number != "":
                formatted_filename = f"{track_number}-{subtrack_number} {sanitize_filename(song_name)}"
            else:
                formatted_filename = f"{subtrack_number} {sanitize_filename(song_name)}"
            song_map[href] = formatted_filename

    if not song_map:
        print(f"[error] No links found for the url: {url}")
        return

    print(f"[info] {len(song_map)} links acquired")

    def process_song(href, song_name):
        link_soup = BeautifulSoup(requests.get(href).content, 'html.parser')
        audio = link_soup.find("audio")
        if not audio:
            print(f"[error] No audio found for {song_name}")
            return

        mp3_url = audio.get("src")
        if not mp3_url:
            print(f"[error] No mp3 URL found for {song_name}")
            return

        file_name = sanitize_filename(song_name) + ".mp3"
        file_path = os.path.join(dir_name, file_name)

        response = requests.head(mp3_url)
        file_size = int(response.headers.get('Content-Length', 0))

        download_file(mp3_url, file_path, file_size)

    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust as needed
        executor.map(process_song, song_map.keys(), song_map.values())

def main():
    input_file_name = "inputs.txt"
    if os.path.exists(input_file_name):
        print("[info] Input file found. Parsing for links...")
        with open(input_file_name, "r") as file:
            for line in file:
                fetch_from_url(line.strip())
    else:
        print("Please input link to album on khinsider.")
        print("Example: http://downloads.khinsider.com/game-soundtracks/album/disgaea-4-a-promise-unforgotten-soundtrack")
        url = input("Url: ").strip()
        fetch_from_url(url)

if __name__ == "__main__":
    main()

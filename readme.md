# KHInsider Soundtrack Downloader

This Python script allows you to download entire soundtracks from KHInsider (https://downloads.khinsider.com). It can process multiple album URLs and download all MP3 files from each album.

## Features

- Download entire soundtracks from KHInsider
- Process multiple album URLs from an input file
- Concurrent downloads for faster processing
- Skips already downloaded files
- Sanitizes filenames for compatibility

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - beautifulsoup4

## Installation

1. Clone this repository or download the `app.py` file.
```bash
git clone https://github.com/orenjerry/khinsider-downloader.git
```
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:

```bash
python app.py
```

Optionally, you can try use older version of the script (it might work for some albums, but not all):

```bash
python old_version.py
```

2. The script will look for an `inputs.txt` file in the same directory. If found, it will process all URLs in that file.
3. If `inputs.txt` is not found, you'll be prompted to enter a single album URL.

### Input File Format

Create a file named `inputs.txt` in the same directory as the script. Add one album URL per line, like this:

```
https://downloads.khinsider.com/game-soundtracks/album/album-name-1
https://downloads.khinsider.com/game-soundtracks/album/album-name-2
```


## Output

Downloaded MP3 files will be saved in a `downloads` directory, organized by album name.

## Customization

You can adjust the number of concurrent downloads by modifying the `max_workers` parameter in the `ThreadPoolExecutor` line of the `fetch_from_url` function.

## Disclaimer

This script is for personal use only. Please respect copyright laws and the terms of service of the websites you're downloading from.

## License

[MIT License](https://opensource.org/licenses/MIT)

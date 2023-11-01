# SpotiSync

SpotiSync is a Python automation project that enables users to download their favorite Spotify playlists as MP3 files effortlessly. With SpotiSync, you can convert your Spotify playlists into downloadable audio files, making it easier to enjoy your music offline or on other devices.

## Features

- Download Spotify playlists as MP3 files.
- Convert playlists for offline listening or on other devices.
- Simple and user-friendly Python automation.

## Usage

To use SpotiSync, follow these steps:

1. Clone this repository.
2. Install the required dependencies.
3. Use Spotify for Developers & Google Cloud Console to create respective API's.
5. Run the `spotisync.py` script with your API Keys & Client ID
6. Playlist ID can be found in the link to playlist when copied from 'Share' options.
7. Downloaded songs will be stored in 'Downloads' folder
8. Initial run will open the Spotify website for confirmation & store a .cache file for future executions.

## Versions
1. Version 1 uses only Spotify API and uses pyautogui & webbrowser to fetch links. Longer run time but no restriction on playlist size.
2. Version 2 uses Google's Youtube Data API which is much faster and fetches links quickly but only playlists with 115 songs can be donwloaded per day due to quota restrictions on API.

##Issues
1. TimeoutException for downloaded button causes an error because the website may sometimes take a significant time to process the video link which causes the program to terminate at last downloaded link.
2. A rare backend error on website could also cause the program to terminate. I have no exceptions set up to deal with this the program needs to run again.

## Author: Uzair

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



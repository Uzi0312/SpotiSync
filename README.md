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
4. Run the `spotisync.py` script with your API Keys & Client ID
5. Downloaded songs will be stored in 'Downloads' folder

## Versions
1. Version 1 uses only Spotify API and uses pyautogui & webbrowser to fetch links. Longer run time but no restriction on playlist size.
2. Version 2 uses Google's Youtube Data API which is much faster and fetches links quickly but only playlists with 115 songs can be donwloaded per day due to quota restrictions on API.

## Author: Uzair

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



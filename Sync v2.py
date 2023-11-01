from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build

#Song limit: 115-120 or Quota exceeded error
#Adjust time.sleep() wait times according to systems's response times. Wait timeout for download button is 120s because site may have a significant delay sometimes processing links.

#Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="Your Client ID", client_secret="Your Client Secret", redirect_uri="http://localhost:8888/callback", scope="playlist-read-private"))

#Chromedriver path
driver = webdriver.Chrome(executable_path=r"Path to Chromedriver")

#YouTube API Key and build obj
api_key = 'Your Youtube Data API Key'
youtube = build('youtube', 'v3', developerKey=api_key)

#Gets list of tracks from specified playlist
def GetPlaylist(playlist_id):
    tracklist = []  #List of tracks
    # Fetch the playlist
    try:
        playlist = sp.playlist_tracks(playlist_id)
        global playlist_name
        PL_meta_data = sp.playlist(playlist_id) #Fetching playlists's metadata to get playlist's name
        # Extract the playlist name
        playlist_name = PL_meta_data['name']
        # Extract and print the song titles
        for track in playlist['items']:
            track_info = track['track']
            song_name = track_info['name']
            artists = [artist['name'] for artist in track_info['artists']]
            artist_names = ', '.join(artists)
            title = f"{song_name} by {artist_names}"
            tracklist.append(title)
    except Exception as e:
        print(f"An error occurred while retrieving playlist data: {e}") 

    return tracklist

#Gets youtube links of all the tracks in a dictionary format
def GetYtLinks(tracklist):
    track_data = {} #Dictionary of type {link:track} #Because its easier to use in convert function
    print("Fetching links...")
    try:
        for track in tracklist:
            # Search for a video by name
            search_response = youtube.search().list(
                q = track,
                type = 'video',
                part = 'id',
                maxResults=1  # You can adjust the number of results
            ).execute()

            # Extract the video ID of the first result
            video_id = search_response['items'][0]['id']['videoId']

            # Generate the URL to the video
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            track_data[video_url] = track
        print("Links fetched:", len(track_data.keys()))
    except Exception as e:
        print(f"An error occured while fetching {track} link:", e)

    return track_data

#Converting & downloading the track links using ytmp3 website
def ConvertToMp3(track_data):
    print(f"Downloading tracks from {playlist_name}")
    track_links = list(track_data.keys()) #List of all the track links
    driver.get("https://ytmp3.nu/UGhs/")
    bad_links = [] #List of all tracks that were not downloaded
    for link in reversed(track_links): #Reversed traversal because list.remove() was skiping links
        try:
            track = track_data[link] #Track title
            search_box = driver.find_element(By.ID, "url")
            search_box.click()
            search_box.send_keys(link)
            search_box.send_keys(Keys.RETURN) #Presses enter
            track_links.pop()
            wait = WebDriverWait(driver, 120) #Waiting for download button a whole fucking 2 mins because the site is shit sometimes
            download_btn = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Download')))
            download_btn.click()
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'w') #Closes ad pop-up
            time.sleep(1)
            convertnxt_btn = driver.find_element(By.LINK_TEXT, 'Convert next')
            convertnxt_btn.click()
            time.sleep(0.5)
            print(f"Downloaded {track}")
            time.sleep(1) #Waiting for search box to exist
        except Exception as e:
            print(f"An error occurred while downloading {track}: {e}")
            bad_links.append(track)
            back_btn = driver.find_element(By.LINK_TEXT, 'Back')
            back_btn.click() #To go back to searchbox 
            continue  # Continue with the next link

    print(f"{playlist_name} downloaded!")
    print("Tracks left out:", bad_links)
    driver.implicitly_wait(30) #Waiting for any downloads in progress
    driver.quit() # Close the browser when all links are processed
 

playlist_id = input("Playlist id: ")
tracklist = GetPlaylist(playlist_id)
track_links = GetYtLinks(tracklist)
ConvertToMp3(track_links)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyautogui
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import webbrowser
import pyperclip

#Wait time for download button is 120s because website acts up sometimes, Don't reduce for faster results.
#Ajust time.sleep() according to your system's response times

#Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="Your Client ID", client_secret="Your Client Secret", redirect_uri="http://localhost:8888/callback", scope="playlist-read-private"))

#Chromedriver path
driver = webdriver.Chrome(executable_path=r"Path to Chromedriver")

#Youtube API Key and build obj
api_key = 'Your Youtube Data API key'
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

#Fetches Track links from Youtube
def GetYtLinks(tracklist):
    print("Fetching links...")
    track_data = {} #Dictionary of type {link:track} #Because its easier to use in convert function
    for track in tracklist:
        link_query = track.replace(' ', '+')
        query = link_query + " audio"
        webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
        time.sleep(4)
        pyautogui.click(x=458, y=271) #Adjust if required. Points to first result of search
        time.sleep(4)
        pyautogui.hotkey('ctrl', 'l') #Jumping to URL bar
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        link = pyperclip.paste()
        track_data[link] = track
        pyautogui.hotkey('ctrl', 'w') #Closing tab
        time.sleep(1)
    print("Links fetched:", len(track_data.keys()))
    
    return track_data

#Chrome automation for conversion
def ConvertToMp3(Track_Data):
    print(f"Downloading tracks from {playlist_name}")
    track_links = list(Track_Data.keys()) #List of all the track links
    driver.get("https://ytmp3.nu/UGhs/")
    bad_links = [] #List of all tracks that were not downloaded
    for link in reversed(track_links): #Reversed traversal because list.remove() was skiping links
        try:
            track = Track_Data[link]
            search_box = driver.find_element(By.ID, "url")
            search_box.click()
            search_box.send_keys(link)
            search_box.send_keys(Keys.RETURN) #Presses enter
            track_links.pop()
            wait = WebDriverWait(driver, 120) #Waiting for download button
            download_btn = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Download')))
            download_btn.click()
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'w')
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

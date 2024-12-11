import requests
from bs4 import BeautifulSoup
import csv
import datetime
import json
import pprint

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def main(base_url, start_datetime, max_results):
    current_datetime = start_datetime
    tracks_list = []

    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    url = f"{base_url}/{formatted_datetime}/{max_results}"
    data = fetch_data(url)

    for track in data:
        track_info = {
            "artist": track["nowPlayingArtist"],
            "track": track["nowPlayingTrack"],
            "image": track["nowPlayingImage"]
        }

        tracks_list.append(track_info)
    
    if data:
        last_play_time_str = data[-1]["nowPlayingTime"]
        current_datetime = datetime.datetime.strptime(last_play_time_str, '%Y-%m-%d %H:%M:%S')
    else:
        return

# Store the data in a CSV file
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for track in tracks_list:
            writer.writerow([f"Track: {track['track']}, Artist: {track['artist']}, Image: {track['image']}"])
    
    print("Data has been written to output.csv")

if __name__ == "__main__":
    base_url = "https://listenapi.planetradio.co.uk/api9.2/events/tar"
    #start_datetime = datetime.datetime.strptime('2024-11-13 22:49:00', '%Y-%m-%d %H:%M:%S')
    start_datetime = datetime.datetime.now()
    max_results = 100  # Antal resultater pr. anmodning
    main(base_url, start_datetime, max_results)
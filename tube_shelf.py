import sqlite3
from contextlib import closing

import json
import re
import webbrowser
from urllib.parse import urlparse

# new
def create_database(conn: sqlite3.Connection) -> None:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS videos(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            time TEXT NOT NULL,
            link TEXT NOT NULL
        )
    ''')

def is_valid_duration(duration: str) -> bool:
    pattern = r"^(\d{1,2}:\d{2}|\d+:\d{2}:\d{2})$"
    return re.fullmatch(pattern, duration) is not None

def display_welcome() -> None:
    print('\n'+'='*70)
    print(" " * 22 + chr(0x1F30C),"TubeShelf")
    print("=" * 70)

    print("\nWelcome to TubeShelf.")

    print("\nYour next watch is waiting in the archive")
    print("Pick a route, cue the playlist, and enjoy the show.")

    print("\nNeed to leave in a hurry?")
    print("Press Ctrl+C at any time.")

def display_menu() -> None:
    
    print("\nWhat's your next move?\n")
    print("1. List all videos")
    print("2. Add a new video")
    print("3. Update a saved video")
    print("4. Remove a video")
    print("5. Launch a video")
    print("6. Leave TubeShelf")


def load_data() -> list[dict[str, str]]:
    try:
        with open('youtube.json', 'r') as file:
            videos = json.load(file)

        # data migration: upgrade old records with new format added
        for video in videos:
            video.setdefault('link', "")

        return videos
        
    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("The data file is corrupted. Starting with an empty library.")
        return []
        
def save_data(videos: list[dict[str, str]]) -> None:
    with open('youtube.json', 'w') as file:
        json.dump(videos, file, indent=4)

def get_valid_video_number(videos: list[dict[str, str]], prompt: str) -> int | None:
    try:
        index = int(input(prompt))
    except ValueError:
        print("Enter a valid number.")
        return None
    
    if not 1 <= index <= len(videos):
        print("invalid video number.")
        return None

    return index -1

def is_valid_youtube_url(url: str) -> bool:
    parsed = urlparse(url)
    valid_domains = (
        "youtube.com",
        "www.youtube.com",
        "youtu.be"
    )
    return parsed.scheme in ("http", "https") and parsed.netloc in valid_domains

def open_video(videos: list[dict[str, str]]) -> None:
    if not videos:
        print("No videos available.")
        return

    list_all_videos(videos)

    index = get_valid_video_number(videos, "Enter the video number to open: ")

    if index is None:
        return

    print("\nRolling the tape....")

    webbrowser.open(videos[index]["link"])

def list_all_videos(videos: list[dict[str, str]]) -> None:
    print("\n" + "-" * 70)

    if not videos:
        print('No videos found. Add your first video!')
    else:
        for index,video in enumerate(videos, start=1):
            
            print(
                f"{index}. {video['name']}\n"
                f"   Duration: {video['time']}\n"
                f"   Link: {video['link']}")

    print("\n" + '-' * 70)


def add_video(videos: list[dict[str, str]]) -> None:
    name = input("Enter video name: ").strip()

    while True:
        time = input("Enter video time: ").strip()
        if is_valid_duration(time):
            break
        print("Please enter time in MM:SS or HH:MM:SS format.")
    

    while True:
        link = input("Enter video link: ").strip() 
        if is_valid_youtube_url(link):
            break
        print("Please enter a valid YouTube URL.")


    if not name or not time or not link:
        print("Video name or duration cannot be empty.")
        return

    
    
    videos.append(
        {
            'name': name,
            'time': time,
            'link': link
        }
    )
    save_data(videos)
    print("\nVideo added successfully.")
    print("\n" + "-" * 70)

def update_video(videos: list[dict[str, str]]) -> None:
    if not videos:
        print("No videos found to update.")
        return
    
    list_all_videos(videos)
    index = get_valid_video_number(videos, "Enter the video number to update: ")

    if index is None:
        return
    
    
    name = input("Enter the new video name: ").strip()

    while True:
        time = input("Enter the new video time: ").strip()
        if is_valid_duration(time):
            break
        print("Enter time in a valid format(HH:MM:SS)")

    while True:
        link = input("Enter video link: ").strip() 
        if is_valid_youtube_url(link):
            break
        print("Please enter a valid YouTube URL.")

    if not name or not time or not link:
        print("Video name or duration cannot be empty.")
        return

    videos[index] = {
        'name': name,
        'time': time,
        'link': link
    }

    save_data(videos)

    print("\nVideo updated successfully.")

def remove_video(videos: list[dict[str, str]]) -> None:

    if not videos:
        print("No videos found to remove.")
        return

    list_all_videos(videos)

    index = get_valid_video_number(videos, "Enter the video number to remove: ")

    if index is None:
        return

    del videos[index]

    save_data(videos)

    print("\nVideo removed successfully.")

def exit_app():
    print("\nThanks for using TubeShelf!")
    print("See you, space cowboy...")


def main()-> None:
    with closing(sqlite3.connect("tubeshelf.db")) as conn:
        videos = load_data()

        create_database(conn)

        display_welcome()

        try:
            while True:
                display_menu()        

                try:
                    choice = int(input("\nEnter your choice: "))

                except ValueError:
                    print("Enter a valid choice(1-6)")
                    continue


                match choice:
                    case 1:
                        list_all_videos(videos)

                    case 2:
                        add_video(videos)

                    case 3:
                        update_video(videos)

                    case 4:
                        remove_video(videos)

                    case 5:
                        open_video(videos)

                    case 6:
                        exit_app()
                        break
                    
                    case _:
                        print("\nEnter a valid choice(1-6)")

        except KeyboardInterrupt:
            print("\n\nEmergency exit initiated.")
            print("Thanks for using TubeShelf!")
            print("See you, space cowboy...")
            
if __name__ == "__main__":
    main()
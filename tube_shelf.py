import sqlite3
from contextlib import closing
import re
import webbrowser
from urllib.parse import urlparse


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


def list_all_videos(conn: sqlite3.Connection) -> None:
    print("\n" + "-" * 70)
    cursor = conn.execute("SELECT id, name, time, link FROM videos ORDER BY id")
    videos = cursor.fetchall()

    if not videos:
        print('No videos found. Add your first video!')
    else:
        for video_id, name, time, link in videos:
            print(
                    f"{video_id}. {name}\n"
                    f"   Duration: {time}\n"
                    f"   Link: {link}"
                )

    print("\n" + '-' * 70)


def add_video(conn: sqlite3.Connection) -> None:
    while True:
        name = input("Enter video name: ").strip()
        if name:
            break
        print("Video name cannot be empty.")

    while True:
        duration = input("Enter video time: ").strip()
        if is_valid_duration(duration):
            break
        print("Please enter time in MM:SS or HH:MM:SS format.")
    
    

    while True:
        link = input("Enter video link: ").strip() 
        if is_valid_youtube_url(link):
            break
        print("Please enter a valid YouTube URL.")

    data = (name, duration, link)

    try:
        with conn:
            conn.execute('''
                INSERT INTO videos(name, time, link)
                VALUES(?, ?, ?)
            ''', data)

    except sqlite3.Error as e:
        print(f"Database Error: {e}")

    # will run only when try block is successful
    else:
        print("\nVideo added successfully.")    

    print("\n" + "-" * 70)

def update_video(conn: sqlite3.Connection) -> None:

    cursor_video = conn.execute("SELECT 1 FROM videos LIMIT 1")
    if cursor_video.fetchone() is None:
        print("No videos found to update.")
        return

    

    list_all_videos(conn)

    while True:
        try:
            video_id = int(input("Enter video number to update: ").strip())

            if video_id <= 0:
                print("Video id must be a positive number.")
                continue

            
            cursor_id = conn.execute("SELECT 1 FROM videos WHERE id = ?", (video_id,))
            if cursor_id.fetchone() is None:
                print("Video ID not found.")
                continue

            break
            
        except ValueError:
            print("Enter a valid video ID")

    while True:
        name = input("Enter the new video name: ").strip()
        if name:
            break
        print("Video name cannot be empty")

    while True:
        duration = input("Enter the new video time: ").strip()
        if is_valid_duration(duration):
            break
        print("Enter time in a valid format(HH:MM:SS)")

    while True:
        link = input("Enter video link: ").strip() 
        if is_valid_youtube_url(link):
            break
        print("Please enter a valid YouTube URL.")

    data = (name, duration, link, video_id)

    try:
        with conn:
            cursor = conn.execute('''
                UPDATE videos
                SET name = ?, time = ?, link = ?
                WHERE id = ?
            ''', data)

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    else:
        if cursor.rowcount == 0:
            print("Video ID not found")
        else:
            print("Video updated successfully.")

    print("\n" + "-" * 70)


        

def remove_video(videos: list[dict[str, str]]) -> None:
    pass

    # if not videos:
    #     print("No videos found to remove.")
    #     return

    # list_all_videos(videos)

    # index = get_valid_video_number(videos, "Enter the video number to remove: ")

    # if index is None:
    #     return

    # del videos[index]

    # (videos)

    # print("\nVideo removed successfully.")

def exit_app():
    print("\nThanks for using TubeShelf!")
    print("See you, space cowboy...")


def main()-> None:
    with closing(sqlite3.connect("tubeshelf.db")) as conn:

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
                        list_all_videos(conn)

                    case 2:
                        add_video(conn)

                    case 3:
                        update_video(conn)

                    case 4:
                        remove_video(conn)

                    case 5:
                        open_video(conn)

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
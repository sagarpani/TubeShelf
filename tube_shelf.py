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


def is_valid_youtube_url(url: str) -> bool:
    parsed = urlparse(url)
    valid_domains = (
        "youtube.com",
        "www.youtube.com",
        "youtu.be"
    )
    return parsed.scheme in ("http", "https") and parsed.netloc in valid_domains

def open_video(conn: sqlite3.Connection) -> None:
    
    cursor_video = conn.execute("SELECT 1 FROM videos LIMIT 1")
    if cursor_video.fetchone() is None:
        print("\nNo videos found to open.")
        return      
    
    list_all_videos(conn)
    
    while True:
        try:
            video_id = int(input("\nEnter video number to open: "))

            if is_valid_video_id(conn, video_id):
                break
            
        except ValueError:
            print("\nEnter a valid video ID")
        

    cursor = conn.execute("SELECT link FROM videos WHERE id = ?", (video_id,))
    result = cursor.fetchone()

    if result is None:
        print("Video not found.")
        return

    (link,) = result
    

    print("\nRolling the tape....")

    webbrowser.open(link)


def list_all_videos(conn: sqlite3.Connection) -> None:
    print("\n" + "-" * 70)
    cursor = conn.execute("SELECT id, name, time, link FROM videos ORDER BY id")
    videos = cursor.fetchall()

    if not videos:
        print('\nNo videos found. Add your first video!')
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
        print("\nVideo name cannot be empty.")

    while True:
        duration = input("Enter video time: ").strip()
        if is_valid_duration(duration):
            break
        print("\nPlease enter time in MM:SS or HH:MM:SS format.")
    
    

    while True:
        link = input("Enter video link: ").strip() 
        if is_valid_youtube_url(link):
            break
        print("\nPlease enter a valid YouTube URL.")

    data = (name, duration, link)

    try:
        with conn:
            conn.execute('''
                INSERT INTO videos(name, time, link)
                VALUES(?, ?, ?)
            ''', data)

    except sqlite3.Error as e:
        print(f"\nDatabase Error: {e}")

    # will run only when try block is successful
    else:
        print("\nVideo added successfully.")    

    print("\n" + "-" * 70)

def is_valid_video_id(conn: sqlite3.Connection, video_id: int) -> bool:

    if video_id <= 0:
        print("\nVideo id must be a positive number.")
        return False

        
    cursor_id = conn.execute("SELECT 1 FROM videos WHERE id = ?", (video_id,))
    if cursor_id.fetchone() is None:
        print("\nVideo ID not found.")
        return False

    return True
            
    

def update_video(conn: sqlite3.Connection) -> None:

    cursor_video = conn.execute("SELECT 1 FROM videos LIMIT 1")
    if cursor_video.fetchone() is None:
        print("\nNo videos found to update.")
        return

    

    list_all_videos(conn)

    while True:
        try:
            video_id = int(input("Enter video number to update: "))

            if is_valid_video_id(conn, video_id):
                break
            
        except ValueError:
            print("\nEnter a valid video ID")

    while True:
        name = input("Enter the new video name: ").strip()
        if name:
            break
        print("\nVideo name cannot be empty")

    while True:
        duration = input("Enter the new video time: ").strip()
        if is_valid_duration(duration):
            break
        print("\nEnter time in a valid format(HH:MM:SS)")

    while True:
        link = input("Enter video link: ").strip() 
        if is_valid_youtube_url(link):
            break
        print("\nPlease enter a valid YouTube URL.")

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
            print("\nVideo ID not found")
        else:
            print("\nVideo updated successfully.")

    print("\n" + "-" * 70)


        

def remove_video(conn: sqlite3.Connection) -> None:
    cursor_video = conn.execute("SELECT 1 FROM videos LIMIT 1")
    if cursor_video.fetchone() is None:
        print("\nNo videos found to remove.")
        return

    list_all_videos(conn)

    while True:
        try:
            video_id = int(input("Enter video number to remove: "))

        except ValueError as e:
            print(f"Error: {e}")
        else:
            if is_valid_video_id(conn, video_id):
                break

    while True:

        letter = input(f"Confirm delete request of video number {video_id} (y/n): ").strip().lower()

            
        if letter == 'y':
            print(f"Deleting video number {video_id}...")
            break

        elif letter == 'n':
            print("Deletion aborted.")
            return
        
        print("Enter a valid response between y and n.")

    try:
        with conn:
            cursor = conn.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    except sqlite3.Error as e:
        print(f"\nDatabase Error: {e}")
    else:
        if cursor.rowcount == 0:
            print("\nVideo id not found.")
        else:   
            print("\nVideo removed successfully.")


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
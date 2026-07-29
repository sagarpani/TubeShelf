# 🌌 TubeShelf

A lightweight command-line application built with Python for saving, managing, and launching your favourite YouTube videos.

TubeShelf lets you create your own personal video library directly from the terminal. Inspired by a laid-back **space-jazz aesthetic**, it combines practical video management with a little cinematic personality.

> *Your next watch is waiting in the archive. Pick a route, cue the playlist, and enjoy the show.*

---

## 🎷 Inspiration

TubeShelf features a subtle space-jazz atmosphere inspired by the style and mood of *Cowboy Bebop*. From the welcoming terminal dialogue to the final sign-off, the application adds a relaxed, cinematic personality to a simple command-line video manager.

The project uses original dialogue and a space-themed interface while paying tribute to the show's iconic atmosphere.

> *See you, space cowboy...*

---

## ✨ Features

* 📚 View all saved videos
* ➕ Add new YouTube videos
* ✏️ Update existing video details
* 🗑️ Remove saved videos
* 🚀 Launch videos directly in your default web browser
* 🔗 Validate YouTube video URLs
* ⏱️ Validate video durations
* 💾 Store video data locally using JSON
* 🔄 Support older records through simple data migration
* 🛡️ Handle missing and corrupted data files
* ⌨️ Exit safely using `Ctrl+C`
* 🌌 Enjoy a space-jazz-inspired terminal experience

---

## 🛠️ Technologies Used

* Python 3
* `json`
* `re`
* `webbrowser`
* `urllib.parse`

No external packages are required.

---

## 📋 Requirements

Before running TubeShelf, make sure Python 3 is installed on your computer.

Open a terminal and check your Python version:

```bash
python --version
```

If that does not work, try:

```bash
python3 --version
```

---

## 🚀 Installation and Setup

### 1. Clone or download the project

You can download the project as a ZIP file from GitHub or clone the repository using Git:

```bash
git clone https://github.com/sagarpani/TubeShelf.git

### 2. Open the project folder

Move into the project directory:

```bash
cd TubeShelf
```

### 3. Run the application

Run the Python file:

```bash
python tubeshelf.py
```

If your system uses `python3`, run:

```bash
python3 tubeshelf.py
```

> Replace `tubeshelf.py` with the actual name of your Python file if it is different.

---

## 🎮 How to Use

When the application starts, you will see the TubeShelf welcome screen followed by the main menu:

```text
What's your next move?

1. List all videos
2. Add a new video
3. Update a saved video
4. Remove a video
5. Launch a video
6. Leave TubeShelf
```

Enter the number of the action you want to perform and press `Enter`.

---

### 📚 List All Videos

Choose:

```text
1
```

TubeShelf displays every saved video along with its:

* Name
* Duration
* YouTube link

---

### ➕ Add a New Video

Choose:

```text
2
```

Then enter:

* Video name
* Video duration
* YouTube video link

The video duration must use one of the following formats:

```text
MM:SS
```

Example:

```text
4:51
```

Or:

```text
HH:MM:SS
```

Example:

```text
1:04:51
```

TubeShelf validates the duration format and YouTube URL before saving the video.

---

### ✏️ Update a Saved Video

Choose:

```text
3
```

Select the number of the video you want to update, then enter its new:

* Name
* Duration
* YouTube link

The updated information is automatically saved to the local JSON file.

---

### 🗑️ Remove a Video

Choose:

```text
4
```

Select the number of the video you want to remove.

The video is deleted from the library, and the updated data is automatically saved.

---

### 🚀 Launch a Video

Choose:

```text
5
```

Select the number of the video you want to watch.

TubeShelf will open the saved YouTube link in your system's default web browser.

```text
Rolling the tape....
```

---

### 👋 Leave TubeShelf

Choose:

```text
6
```

TubeShelf will close with its final transmission:

```text
Thanks for using TubeShelf!

See you, space cowboy...
```

---

### ⌨️ Emergency Exit

Need to leave in a hurry?

Press:

```text
Ctrl+C
```

at any time to exit the application safely.

---

## 📁 Project Structure

```text
TubeShelf/
│
├── tubeshelf.py
├── youtube.json
└── README.md
```

* `tubeshelf.py` — Main application source code
* `youtube.json` — Stores the saved video library
* `README.md` — Project documentation

> If your Python file has a different name, update the filename in this section and in the run commands above.

---

## 💾 Data Storage

TubeShelf stores video information locally inside the `youtube.json` file.

Each video is saved in the following format:

```json
{
    "name": "Apocalypse",
    "time": "4:51",
    "link": "https://youtu.be/sElE_BfQ67s"
}
```

Your video library remains available after closing and reopening the application.

---

## 🔄 Backward Compatibility

TubeShelf supports older video records through a simple data-migration process.

When existing data is loaded, older records that do not contain a YouTube link are automatically updated with an empty `link` field. This allows older JSON data to continue working after the application's data structure evolves.

---

## ⚠️ Notes

* TubeShelf is a local application. Your video data is stored on your computer.
* No external Python packages are required.
* Videos open in the default web browser configured on your operating system.
* If `youtube.json` does not exist, TubeShelf automatically starts with an empty library.
* If the JSON data file is corrupted, TubeShelf displays a warning and starts with an empty library.
* Avoid manually editing `youtube.json` unless you are familiar with JSON syntax.

---

## 🎯 Learning Objectives

This project was built to practise and demonstrate:

* Python functions
* Type hints
* File handling
* JSON data storage
* CRUD operations
* Exception handling
* Regular expressions
* Input validation
* URL parsing
* Data migration
* Python standard-library modules
* Command-line application design
* Basic terminal user experience

---

## 🔮 Possible Future Improvements

Some ideas for future versions include:

* Search videos by name
* Add video categories
* Add favourite videos
* Sort and filter videos
* Replace JSON storage with SQLite

---

## 👨‍💻 Author

**Sagar Pani**<br>
[Portfolio](https://sagar-evolves-dev.vercel.app/)<br>
[LinkedIn](https://www.linkedin.com/in/sagarpani/)

Built as part of my Python learning journey.

---

## 🛸 Closing Transmission

```text
Thanks for using TubeShelf!

See you, space cowboy...
```

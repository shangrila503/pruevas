# Apple Maze Monsters

Apple Maze Monsters is a small beginner-friendly Python and pygame maze game.
You control a cute green ball-shaped monster, eat all the red apples, and avoid
the small brown ants.

The game uses simple shapes instead of image files, so it is easy to run and easy
to change while you are learning to code.

## What you need

- A Windows computer
- Python 3 installed
- pygame installed

## 1. How to install Python on Windows

1. Go to the official Python website: <https://www.python.org/downloads/>
2. Click the button to download the newest Python 3 version for Windows.
3. Open the installer after it downloads.
4. Very important: check the box that says **Add python.exe to PATH**.
5. Click **Install Now** and wait for the install to finish.
6. Open Command Prompt and type this command to check Python:

```bat
python --version
```

If Python is installed correctly, you should see a version number.

## 2. How to install pygame

1. Open Command Prompt.
2. Move into the folder where this project is saved. For example:

```bat
cd C:\Users\YourName\Downloads\apple-maze-monsters
```

3. Install pygame with this command:

```bat
pip install -r requirements.txt
```

If that does not work, try:

```bat
python -m pip install -r requirements.txt
```

## 3. How to run the game

In Command Prompt, make sure you are still inside the project folder. Then run:

```bat
python main.py
```

## How to play

- Use the arrow keys to move the green monster.
- Eat every red apple to win.
- Do not touch the brown ants.
- If an ant touches you, the game shows **Game Over**.
- If you eat all the apples, the game shows **You Win!**.

## Files in this project

- `main.py` - the game code
- `requirements.txt` - the Python package needed to run the game
- `README.md` - these instructions

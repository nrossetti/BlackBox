# BlackBox

BlackBox is a simple Python application that allows you to black out a part of your screen. It was originally created for personal use, particularly for blacking out a portion of a fullscreen visualizer projected on a wall. However, it can also be used for various other purposes such as chroma keying a part of a screen.

## How It Works

BlackBox utilizes Tkinter for the GUI and Pystray for the system tray functionality. It creates a borderless, resizable window that allows you to select a color to fill a portion of your screen. You can adjust the size and position of the blacked-out area by dragging the window. The system tray icon provides options to show/hide the window, change the color, or close the application.

## Features

- Borderless, resizable, and movable window
- System tray icon for easy access to options
- Ability to change fill color

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/nrossetti/BlackBox.git
   cd BlackBox
   ```

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

To run BlackBox, simply execute the following command:

```
python main.py
```

## Building Executable

If you want to create a standalone executable for your platform, you can use PyInstaller. Here's how:

```
pyinstaller --onefile --noconsole --add-data="static;static" --icon=static/bb.ico --name=BlackBox main.py
```

## TODO

- Implement persistence feature to save color and position settings and load on application startup
  
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

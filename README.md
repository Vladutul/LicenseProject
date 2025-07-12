# LicenseProject - CNC Drilling Machine – DIY Project with Arduino and Python Interface

A PyQt5-based application for 3D shape manipulation, GCode generation, and serial communication with Arduino.

## Features

- **3D Visualization:** Visualize and manipulate 3D shapes (parallelepipeds, holes, drill plates) using pyqtgraph.
- **GCode Generation:** Generate GCode files for CNC/3D printing based on the defined shapes.
- **Project Save/Load:** Save and load your project state as JSON files.
- **Serial Communication:** Send GCode files and commands to Arduino via serial port.
- **Modular UI:** Dockable widgets for serial connection, shape manipulation, and connection management.

## Requirements

- Python 3.11+
- PyQt5
- pyqtgraph
- numpy
- pyserial
- qtpy

Install dependencies with:

```sh
pip install pyqt5 pyqtgraph numpy pyserial qtpy
```

## Project Structure

```
src/
  classMain.py                # Main UI window and logic
  connectionWindow.py         # Connection window dock widget
  gCodeGeneration.py          # GCode generation logic
  main.py                     # Application entry point
  miniFigure.py               # Mini figure creation logic
  plot.py                     # 3D plotting and visualization
  saveAndLoad.py              # Project save/load logic
  serialConnection.py         # Serial connection manager
  serialConnectionBackend.py  # Serial backend logic
  serialConnectionFrontend.py # Serial frontend UI
  serialThread.py             # Serial reading thread
  shapeManipulation.py        # Shape manipulation dock widget
```

## How to Run

1. Clone the repository.
2. Install the dependencies.
3. Run the application:

```sh
python src/main.py
```

## Usage

- Use the menu bar to open/save projects, generate/send GCode, and manage dock widgets.
- Manipulate shapes in the "Shape Manipulation" dock.
- Connect to your Arduino in the "Serial Connection" dock and send GCode or manual commands.

## Demo

Watch a demo of the project on YouTube:  
[![YouTube Video](https://img.shields.io/badge/Watch%20on-YouTube-red?logo=youtube)](https://www.youtube.com/your-video-link)

## License

This project is for educational purposes.

CNC Drilling Machine – DIY Project with Arduino and Python Interface

*Made with PyQt5 and pyqtgraph.*

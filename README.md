# Airport-Database-Management-GUI

This project involves creating a Python-based graphical user interface (GUI) using tkinter to interact with the "airports.db" SQLite database. The goal is to facilitate effective interaction with the data stored in the database, enabling users to view, update, add, and modify information. The database serves as both an input and an output, reflecting the real-world scenario where persistent data needs to be managed and updated over time.

## Project Functionality

The project mandates the creation of a tkinter-based GUI, enabling users to interact with the "airports.db" database. The following functionalities are central to the program's objectives:

- **Continent Management:**
  - Search for continents based on continent code, name, or both.
  - Add a new continent to the database by specifying relevant data points.
  - Update an existing continent in the database.

- **Country Management:**
  - Search for countries based on country code, name, or both.
  - Add a new country to the database by specifying relevant data points.
  - Update an existing country in the database.

- **Region Management:**
  - Search for regions based on region code, local code, name, or a combination.
  - Add a new region to the database by specifying relevant data points.
  - Update an existing region in the database.

The project introduces the concept of Python packages to organize the code effectively, allowing for better management of modules and their functionalities. It presents an opportunity to understand the importance of structuring code for efficient collaboration and maintenance.

## Usage

1. Clone or download this repository.
2. Ensure Python is installed on your system.
3. Open the project in an appropriate IDE (e.g., PyCharm).
4. Run the `main.py` script to launch the GUI.

## Dependencies

The project relies on the following:

- Python 3.x
- Tkinter (Python's standard GUI toolkit)
- SQLite database (airports.db)

## Project Structure

The project is organized into four major areas:
1. **p2app.views:** Defines the GUI using tkinter.
2. **p2app.engine:** Contains functionality to communicate with the SQLite database.
3. **p2app.events:** Provides tools for communication between views and the engine.
4. **project2.py:** Initializes the program and launches the user interface.

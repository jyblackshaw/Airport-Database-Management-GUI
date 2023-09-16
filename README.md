# Airport-Database-Management-GUI

This project involves creating a Python-based graphical user interface (GUI) using tkinter to interact with the "airports.db" SQLite database. The goal is to facilitate effective interaction with the data stored in the database, enabling users to view, update, add, and modify information. The database serves as both an input and an output, reflecting the real-world scenario where persistent data needs to be managed and updated over time.

Data Persistence and Management
In the realm of Python programming, data management isn't always confined to objects stored in memory. There's a need for persistent data that remains accessible even after the program ends and is restarted. Additionally, when dealing with large amounts of data that can't fit into available memory, storing data in files becomes imperative. This project emphasizes the effective storage and retrieval of data from a database, enhancing understanding of how databases function in conjunction with programs.

The Role of Databases and DBMS
Databases and Database Management Systems (DBMSs) play a crucial role in handling persistent data efficiently. SQLite, being a relational DBMS, allows for seamless management of data through SQL statements, abstracting away the complexities of file handling. This project delves into utilizing SQLite, leveraging its ability to handle large files even when memory is limited. Despite the challenge of bridging the gap between Python and SQLite, the project aims to navigate this tradeoff effectively.

Project Functionality
The project mandates the creation of a tkinter-based GUI, enabling users to interact with the "airports.db" database. The following functionalities are central to the program's objectives:

Continent Management:

Search for continents based on continent code, name, or both.
Add a new continent to the database by specifying relevant data points.
Update an existing continent in the database.
Country Management:

Search for countries based on country code, name, or both.
Add a new country to the database by specifying relevant data points.
Update an existing country in the database.
Region Management:

Search for regions based on region code, local code, name, or a combination.
Add a new region to the database by specifying relevant data points.
Update an existing region in the database.
The project introduces the concept of Python packages to organize the code effectively, allowing for better management of modules and their functionalities. It presents an opportunity to understand the importance of structuring code for efficient collaboration and maintenance.

Getting Started
Clone or download this repository.
Ensure Python is installed on your system.
Open the project in an appropriate IDE (e.g., PyCharm).
Run the main.py script to launch the GUI.
Dependencies
The project relies on the following:

Python 3.x
Tkinter (Python's standard GUI toolkit)
SQLite database (airports.db)
Project Structure
The project is organized into four major areas:

p2app.views: Defines the GUI using tkinter.
p2app.engine: Contains functionality to communicate with the SQLite database.
p2app.events: Provides tools for communication between views and the engine.
project2.py: Initializes the program and launches the user interface.

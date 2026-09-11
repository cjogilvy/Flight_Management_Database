# Flight Management Database

A small Python and SQLite command-line application for managing flights, pilots, airports, and aircraft. It demonstrates database design, SQL queries, validation, and updates through an interactive terminal menu.

## Features

- Search flights by time range, destination, or aircraft
- Update a flight's status or arrival destination
- View a pilot's schedule and assign pilots to flights
- Create and delete flights
- View aircraft maintenance dates and usage statistics
- Update an aircraft's last inspection date

## Requirements

- Python 3.8 or newer
- No external Python packages are required

## Quick Start

1. Open a terminal in the project folder.
2. Start the application:

   ```bash
   python Flight_Management.py
   ```

3. Use the numbered menus to explore the sample data and features.

The repository includes `Flight_Management.db` with sample pilots, flights, destinations, aircraft, and pilot assignments, so the application can be run immediately.

## Creating a Fresh Database

`Database_Creation.py` creates and seeds a new `Flight_Management.db` file. Use it only when setting up a fresh copy of the project:

```bash
python Database_Creation.py
```

The script expects the database file and tables not to exist yet. To reset the sample data, close the application, remove or rename the existing `Flight_Management.db`, and run the creation script again.

## Project Files

- `Flight_Management.py` - interactive command-line application and SQL operations
- `Database_Creation.py` - creates the SQLite tables and inserts sample data
- `Flight_Management.db` - included SQLite database used by the application
- `FlightManagement_Document.pdf` - supporting project documentation

## Example Walkthrough

After starting the application, try:

1. Select **Find a Flight** and search by destination or aircraft.
2. Select **Find a Pilot** to view a pilot's schedule.
3. Select **View Aircraft Stats** to inspect maintenance dates and aircraft usage.
4. Select **Create or Delete a Flight** to test the validated update workflows.

Changes made through the application are saved to `Flight_Management.db`. Make a backup of that file before experimenting if you want to preserve the original sample data.
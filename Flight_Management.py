import sqlite3
from datetime import datetime

# Links to the database created in the database creation script
db_file = "Flight_Management.db"
connection = sqlite3.connect(db_file)
cursor = connection.cursor()


### ~~~ General Functions ~~~ ###
def validate_existence(cursor, table, column, value):
    # Checks if a value is in that column in that table
    # Select * returns all values that matches the criteria
    # Limit 1 restricts the number of values returned to 1
    # If values are returned the function returns True, else False
    query = f"SELECT * FROM {table} WHERE {column} = ? LIMIT 1;"
    cursor.execute(query, (value,))
    return cursor.fetchone() is not None

def list_options(cursor, table, id_column, name_column):
    # Lists options from a table with their IDs and names.
    query = f"SELECT {id_column}, {name_column} FROM {table};"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"{id_column}: {row[0]}, {name_column}: {row[1]}")

def validate_date_input(date_str, format="%Y-%m-%d %H:%M"):
    # Checks if the date string is in the format "%Y-%m-%d %H:%M".
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        print(f"Error: Invalid date format. Please use {format}.")
        return None


### ~~~ Find a flight ~~~ ###
def find_flight_menu():
    # Takes the input 1,2 or 3 and calls the relevant functions
    while True:
        print("\n=== Find a Flight ===")
        print("1. Search Flights")
        print("2. Update Flight Information")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            search_flights()
        elif choice == "2":
            update_flight_information()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def search_flights():
    # Allows users to search for flights using various criteria.
    print("\nSearch Flights by:")
    print("1. Time Range")
    print("2. Destination")
    print("3. Aircraft")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        # Search by time range
        start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
        start_dt = validate_date_input(start_time)
        if not start_dt:
            return
        end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
        end_dt = validate_date_input(end_time)
        if not end_dt:
            return
        if start_dt >= end_dt:
            print("Error: Start time must be before end time.")
            return
        # Query for flights between certain dates
        query = """
        SELECT Flight_ID, Departure_Date, Arrival_Date, Status FROM Flights
        WHERE Departure_Date BETWEEN ? AND ?;
        """
        cursor.execute(query, (start_time, end_time))
        results = cursor.fetchall()
        if results:
            print("\nFlights in Time Range:")
            for row in results:
                print(f"Flight ID: {row[0]}, Departure: {row[1]}, Arrival: {row[2]}, Status: {row[3]}")
        else:
            print("No flights found in this time range.")

    elif choice == "2":
        # Search by destination
        print("\nSearch Destination by:")
        print("1. Airport ID")
        print("2. City Name")
        print("3. Country Name")
        dest_choice = input("Enter your choice: ")
        
        if dest_choice == "1":
            list_options(cursor, "Destinations", "Airport_ID", "Airport_Name")
            dest_input = input("Enter airport ID: ")
            column = "Airport_ID"
        elif dest_choice == "2":
            list_options(cursor, "Destinations", "Airport_ID", "City")
            dest_input = input("Enter city name: ")
            column = "City"
        elif dest_choice == "3":
            list_options(cursor, "Destinations", "Airport_ID", "Country")
            dest_input = input("Enter country name: ")
            column = "Country"
        else:
            print("Invalid choice. Enter a number.")
            return

        # Finds the airport ID from the user's input and valid the result
        query_validation = f"SELECT Airport_ID FROM Destinations WHERE {column} = ? LIMIT 1;"
        cursor.execute(query_validation, (dest_input,))
        destination_id = cursor.fetchone()
        if not destination_id:
            print("Error: Destination not found.")
            return
        destination_id = destination_id[0]

        # Asks user to search for arrivals or departures
        print("\nSearch Flights for:")
        print("1. Arrivals")
        print("2. Departures")
        arrival_or_departure = input("Enter your choice: ")
        
        if arrival_or_departure == "1":
            direction = "Arrival_Airport_ID"
        elif arrival_or_departure == "2":
            direction = "Departure_Airport_ID"
        else:
            print("Invalid choice.")
            return

        # Query flights by destination
        query = f"""
        SELECT Flights.Flight_ID, Flights.Departure_Date, Flights.Arrival_Date, Flights.Status, 
        Departure.Airport_Name AS From_Airport, Arrival.Airport_Name AS To_Airport FROM Flights
        JOIN Destinations AS Departure ON Flights.Departure_Airport_ID = Departure.Airport_ID
        JOIN Destinations AS Arrival ON Flights.Arrival_Airport_ID = Arrival.Airport_ID
        WHERE Flights.{direction} = ?;
        """
        cursor.execute(query, (destination_id,))
        results = cursor.fetchall()
        if results:
            print("\nFlights:")
            for row in results:
                print(f"Flight ID: {row[0]}, From: {row[4]}, To: {row[5]}, Departure: {row[1]}, Arrival: {row[2]}, Status: {row[3]}")
        else:
            print("No flights found for this destination.")

    elif choice == "3":
        # Search by aircraft
        list_options(cursor, "Aircraft", "Aircraft_ID", "Model_No")
        aircraft_id = input("Enter aircraft ID: ")
        if not validate_existence(cursor, "Aircraft", "Aircraft_ID", aircraft_id):
            print("Error: Aircraft not found.")
            return

        # Query flights by aircraft
        query = """
        SELECT Flights.Flight_ID, Flights.Departure_Date, Flights.Arrival_Date, Flights.Status, 
        Departure.Airport_Name AS From_Airport, Arrival.Airport_Name AS To_Airport FROM Flights
        JOIN Destinations AS Departure ON Flights.Departure_Airport_ID = Departure.Airport_ID
        JOIN Destinations AS Arrival ON Flights.Arrival_Airport_ID = Arrival.Airport_ID
        WHERE Flights.Aircraft_ID = ?;
        """
        cursor.execute(query, (aircraft_id,))
        results = cursor.fetchall()
        if results:
            print("\nFlights:")
            for row in results:
                print(f"Flight ID: {row[0]}, From: {row[4]}, To: {row[5]}, Departure: {row[1]}, Arrival: {row[2]}, Status: {row[3]}")
        else:
            print("No flights found for this aircraft.")
    else:
        print("Invalid choice. Please try again.")

def update_flight_information():
    # Allows the user to update the flight information
    # List flights with detailed information
    query_flights = """
    SELECT Flights.Flight_ID, Departure.City AS From_City, Arrival.City AS To_City,
    Flights.Departure_Date, Flights.Status FROM Flights
    JOIN Destinations AS Departure ON Flights.Departure_Airport_ID = Departure.Airport_ID
    JOIN Destinations AS Arrival ON Flights.Arrival_Airport_ID = Arrival.Airport_ID;
    """
    cursor.execute(query_flights)
    flights = cursor.fetchall()

    print("\nAvailable Flights:")
    for flight in flights:
        print(f"Flight ID: {flight[0]}, From: {flight[1]}, To: {flight[2]}, "
              f"Departure: {flight[3]}, Status: {flight[4]}")

    # Get user input for flight ID
    flight_id = input("\nEnter flight ID: ")
    if not validate_existence(cursor, "Flights", "Flight_ID", flight_id):
        print("Error: Flight not found.")
        return

    print("\nWhat would you like to update?")
    print("1. Status")
    print("2. Destination")
    choice = input("Enter your choice: ")

    if choice == "1":
        # Update flight status
        status = input("Enter new status (Scheduled/Delayed/Canceled): ")
        if status not in ["Scheduled", "Delayed", "Canceled"]:
            print("Error: Invalid status.")
            return
        query_update_status = "UPDATE Flights SET Status = ? WHERE Flight_ID = ?;"
        cursor.execute(query_update_status, (status, flight_id))
        connection.commit()
        print("Flight status updated successfully!")

    elif choice == "2":
        # Update flight destination
        list_options(cursor, "Destinations", "Airport_ID", "Airport_Name")
        destination_id = input("Enter new destination ID: ")
        if not validate_existence(cursor, "Destinations", "Airport_ID", destination_id):
            print("Error: Destination not found.")
            return
        query_update_destination = "UPDATE Flights SET Arrival_Airport_ID = ? WHERE Flight_ID = ?;"
        cursor.execute(query_update_destination, (destination_id, flight_id))
        connection.commit()
        print("Flight destination updated successfully!")

    else:
        print("Invalid choice.")


### ~~~ Find a pilot ~~~ ###
def find_pilot_menu():
    # Menu that calls different functions relating to the pilot
    while True:
        print("\n=== Find a Pilot ===")
        print("1. View Pilot Schedule")
        print("2. Assign Pilot to Flight")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            view_pilot_schedule()
        elif choice == "2":
            assign_pilot_to_flight()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def view_pilot_schedule():
    # Shows the schedule for a specific pilot
    # Lists pilots by experience for the user to select
    print("\nPilots by Experience:")
    query_pilots = """
    SELECT Pilot_ID, Name, Years_Experience
    FROM Pilot ORDER BY Years_Experience DESC;
    """
    cursor.execute(query_pilots)
    pilots = cursor.fetchall()
    if not pilots:
        print("No pilots found.")
        return

    for pilot in pilots:
        print(f"Pilot ID: {pilot[0]}, Name: {pilot[1]}, Years Experience: {pilot[2]}")

    # Search by Pilot ID or Name
    print("\nSearch Pilot by:")
    print("1. Pilot ID")
    print("2. Pilot Name")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        pilot_id = input("Enter Pilot ID: ")
        if not validate_existence(cursor, "Pilot", "Pilot_ID", pilot_id):
            print("Error: Pilot not found.")
            return
    # If searching by name, queries the database to find relevant ID number
    elif choice == "2":
        pilot_name = input("Enter Pilot Name: ")
        query_pilot = "SELECT Pilot_ID FROM Pilot WHERE Name = ?;"
        cursor.execute(query_pilot, (pilot_name,))
        pilot = cursor.fetchone()
        if not pilot:
            print("Error: Pilot not found.")
            return
        pilot_id = pilot[0]
    else:
        print("Invalid choice.")
        return

    # Display pilot's schedule
    query_schedule = """
    SELECT Flights.Flight_ID, Departure.City AS From_Airport, Arrival.City AS To_Airport,
    Flights.Departure_Date, Flights.Arrival_Date, Flights.Status FROM Flights
    JOIN Pilots_Assigned ON Flights.Flight_ID = Pilots_Assigned.Flight_ID
    JOIN Destinations AS Departure ON Flights.Departure_Airport_ID = Departure.Airport_ID
    JOIN Destinations AS Arrival ON Flights.Arrival_Airport_ID = Arrival.Airport_ID 
    WHERE Pilots_Assigned.Pilot_ID = ?;
    """
    cursor.execute(query_schedule, (pilot_id,))
    schedule = cursor.fetchall()
    if not schedule:
        print(f"No flights found for Pilot ID {pilot_id}.")
        return

    print(f"\nSchedule for Pilot ID {pilot_id}:")
    for flight in schedule:
        print(f"Flight ID: {flight[0]}, From: {flight[1]}, To: {flight[2]}, Departure: {flight[3]}, Arrival: {flight[4]}, Status: {flight[5]}")

def assign_pilot_to_flight():
    # This function assigns a pilot to a specific flight
    # it also links to the function to create a new flight
    print("\nAssign a Pilot to a Flight:")
    print("1. Assign to an Existing Flight")
    print("2. Create a New Flight")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        # List flights with current pilot count
        query_flights = """
        SELECT Flights.Flight_ID, Departure.City AS From_Airport, Arrival.City AS To_Airport, Flights.Departure_Date, Flights.Status,
        (SELECT COUNT(*) FROM Pilots_Assigned WHERE Pilots_Assigned.Flight_ID = Flights.Flight_ID) AS Pilot_Count FROM Flights
        JOIN Destinations AS Departure ON Flights.Departure_Airport_ID = Departure.Airport_ID
        JOIN Destinations AS Arrival ON Flights.Arrival_Airport_ID = Arrival.Airport_ID;
        """
        cursor.execute(query_flights)
        flights = cursor.fetchall()
        if not flights:
            print("No flights found.")
            return

        print("\nAvailable Flights:")
        for flight in flights:
            print(f"Flight ID: {flight[0]}, From: {flight[1]}, To: {flight[2]}, "
                  f"Departure: {flight[3]}, Status: {flight[4]}, Pilots Assigned: {flight[5]}")
        flight_id = input("\nEnter Flight ID: ")
        if not validate_existence(cursor, "Flights", "Flight_ID", flight_id):
            print("Error: Flight not found.")
            return
    elif choice == "2":
        # Call the create_new_flight function
        create_new_flight()
        return
    else:
        print("Invalid choice.")
        return

    # List all pilots
    print("\nAvailable Pilots:")
    list_options(cursor, "Pilot", "Pilot_ID", "Name")
    pilot_id = input("Enter Pilot ID: ")
    if not validate_existence(cursor, "Pilot", "Pilot_ID", pilot_id):
        print("Error: Pilot not found.")
        return

    # Check if the pilot is already assigned to the flight
    query_check = """
    SELECT 1 FROM Pilots_Assigned WHERE Flight_ID = ? AND Pilot_ID = ?;
    """
    cursor.execute(query_check, (flight_id, pilot_id))
    if cursor.fetchone():
        print("Error: This pilot is already assigned to the selected flight.")
        return

    # Assign the pilot to the flight
    role = input("Enter pilot's role (Captain/Co-Pilot): ")
    if role not in ["Captain", "Co-Pilot"]:
        print("Error: Role must be 'Captain' or 'Co-Pilot'.")
        return

    query_assign = """
    INSERT INTO Pilots_Assigned (Flight_ID, Pilot_ID, Role)
    VALUES (?, ?, ?);
    """
    cursor.execute(query_assign, (flight_id, pilot_id, role))
    connection.commit()
    print("Pilot assigned successfully!")


### ~~~ Create/Delete a flight ~~~ ###
def add_or_remove_flight_menu():
    # Menu for selecting whether to add or remove a flight.
    while True:
        print("\n=== Create/Delete a Flight ===")
        print("1. Create a New Flight")
        print("2. Delete a Flight")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            create_new_flight()
        elif choice == "2":
            delete_flight()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def create_new_flight():
    # This function takes the user through creating a new flight
    try:
        print("\n=== Create a New Flight ===")
        
        # Choose departure and arrival airports
        print("\nStep 1: Choose Departure Airport")
        list_options(cursor, "Destinations", "Airport_ID", "Airport_Name")
        departure_airport = input("Enter departure airport ID: ")
        if not validate_existence(cursor, "Destinations", "Airport_ID", departure_airport):
            print("Error: Invalid departure airport ID.")
            return

        print("\nStep 2: Choose Arrival Airport")
        arrival_airport = input("Enter arrival airport ID: ")
        if not validate_existence(cursor, "Destinations", "Airport_ID", arrival_airport):
            print("Error: Invalid arrival airport ID.")
            return
        if arrival_airport == departure_airport:
            print("Error: Departure and arrival airports cannot be the same.")
            return

        # Specify flight times
        print("\nStep 3: Enter Flight Times")
        departure_date = input("Enter departure date (YYYY-MM-DD HH:MM): ")
        departure_dt = validate_date_input(departure_date)
        arrival_date = input("Enter arrival date (YYYY-MM-DD HH:MM): ")
        arrival_dt = validate_date_input(arrival_date)
        if not departure_dt or not arrival_dt:
            return
        if departure_dt >= arrival_dt:
            print("Error: Arrival date must be after departure date.")
            return

        # List all aircraft
        print("\nStep 4: Select an Aircraft")
        list_options(cursor, "Aircraft", "Aircraft_ID", "Model_No")
        aircraft_id = input("Enter aircraft ID: ")
        if not validate_existence(cursor, "Aircraft", "Aircraft_ID", aircraft_id):
            print("Error: Invalid aircraft ID.")
            return

        # Assign a Captain and a Co-Pilot
        print("\nStep 5: Assign Captain and Co-Pilot")
        print("Pilots by Experience:")
        query_pilots = """
        SELECT Pilot_ID, Name, Years_Experience FROM Pilot
        ORDER BY Years_Experience DESC;
        """
        cursor.execute(query_pilots)
        pilots = cursor.fetchall()
        if not pilots:
            print("No pilots available.")
            return

        for pilot in pilots:
            print(f"Pilot ID: {pilot[0]}, Name: {pilot[1]}, Years Experience: {pilot[2]}")

        # Assign Captain
        captain_id = input("Enter Pilot ID for Captain: ")
        if not validate_existence(cursor, "Pilot", "Pilot_ID", captain_id):
            print("Error: Invalid Captain ID.")
            return

        # Assign Co-Pilot
        co_pilot_id = input("Enter Pilot ID for Co-Pilot: ")
        if not validate_existence(cursor, "Pilot", "Pilot_ID", co_pilot_id):
            print("Error: Invalid Co-Pilot ID.")
            return

        # Ensure Captain and Co-Pilot are not the same person
        if captain_id == co_pilot_id:
            print("Error: Captain and Co-Pilot cannot be the same person.")
            return

        # Create the flight
        query_flight = """
        INSERT INTO Flights (Departure_Airport_ID, Arrival_Airport_ID, Departure_Date, Arrival_Date, Status, Aircraft_ID)
        VALUES (?, ?, ?, ?, 'Scheduled', ?);
        """
        cursor.execute(query_flight, (departure_airport, arrival_airport, departure_date, arrival_date, aircraft_id))
        flight_id = cursor.lastrowid  # Get the ID of the newly created flight

        # Assign Captain and Co-Pilot to the flight
        query_assign_pilot = """
        INSERT INTO Pilots_Assigned (Flight_ID, Pilot_ID, Role)
        VALUES (?, ?, ?);
        """
        cursor.execute(query_assign_pilot, (flight_id, captain_id, 'Captain'))
        cursor.execute(query_assign_pilot, (flight_id, co_pilot_id, 'Co-Pilot'))
        connection.commit()

        print("Flight created successfully with assigned Captain and Co-Pilot!")

    except Exception as e:
        print(f"Error: {e}")

def delete_flight():
    # Allows the user to delete a flight from the database, removing it from the flights and pilots assigned table 
    try:
        print("\n=== Delete a Flight ===")
        
        # Display all flights to help the user select one
        query_flights = """
        SELECT Flights.Flight_ID, Departure.City AS From_City, Arrival.City AS To_City,
        Flights.Departure_Date, Flights.Arrival_Date, Flights.Status FROM Flights
        JOIN Destinations AS Departure ON Flights.Departure_Airport_ID = Departure.Airport_ID
        JOIN Destinations AS Arrival ON Flights.Arrival_Airport_ID = Arrival.Airport_ID;
        """
        cursor.execute(query_flights)
        flights = cursor.fetchall()

        if not flights:
            print("No flights available to delete.")
            return

        print("\nAvailable Flights:")
        for flight in flights:
            print(f"Flight ID: {flight[0]}, From: {flight[1]}, To: {flight[2]}, "
                  f"Departure: {flight[3]}, Arrival: {flight[4]}, Status: {flight[5]}")

        # Get user input for the flight ID
        flight_id = input("\nEnter the Flight ID to delete: ")
        if not validate_existence(cursor, "Flights", "Flight_ID", flight_id):
            print("Error: Flight not found.")
            return

        # Confirm the deletion
        confirmation = input(f"Are you sure you want to delete Flight ID {flight_id}? (yes/no): ").lower()
        if confirmation != "yes":
            print("Deletion canceled.")
            return

        # Delete from Pilots_Assigned table
        query_delete_pilots = "DELETE FROM Pilots_Assigned WHERE Flight_ID = ?;"
        cursor.execute(query_delete_pilots, (flight_id,))
        
        # Delete from Flights table
        query_delete_flight = "DELETE FROM Flights WHERE Flight_ID = ?;"
        cursor.execute(query_delete_flight, (flight_id,))
        
        # Commit the changes
        connection.commit()
        print(f"Flight ID {flight_id} and associated pilot assignments have been deleted successfully.")

    except Exception as e:
        print(f"Error: {e}")


### ~~~ View Aircraft Stats ~~~ ###
def view_aircraft_menu():
    """
    Menu for viewing aircraft-related statistics.
    """
    while True:
        print("\n=== View Aircraft Stats ===")
        print("1. View Maintenance Schedule")
        print("2. Update Last Inspection")
        print("3. View Aircraft Usage")
        print("4. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            view_maintenance_schedule()
        elif choice == "2":
            update_last_inspection()
        elif choice == "3":
            view_aircraft_usage()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def view_maintenance_schedule():
    # Displays the maintenance schedule for all aircraft, highlighting overdue maintenance.
    try:
        query = """
        SELECT Aircraft.Aircraft_ID, Aircraft.Model_No, Aircraft.Last_Inspection,
        DATE(Last_Inspection, '+365 days') AS Next_Maintenance FROM Aircraft;
        """
        cursor.execute(query)
        aircraft = cursor.fetchall()
        if not aircraft:
            print("No aircraft found.")
            return

        print("\nMaintenance Schedule:")
        for row in aircraft:
            overdue = " (OVERDUE)" if datetime.strptime(row[3], "%Y-%m-%d") <= datetime.now() else ""
            print(f"Aircraft ID: {row[0]}, Model: {row[1]}, Last Inspection: {row[2]}, Next Maintenance: {row[3]}{overdue}")
    except Exception as e:
        print(f"Error: {e}")

def update_last_inspection():
    # Allows the user to update the last maintenance date of an aircraft to either today or a specified date.
    try:
        print("\n=== Update Aircraft Last Inspection ===")
        # List all aircraft to help the user select one
        list_options(cursor, "Aircraft", "Aircraft_ID", "Model_No")
        aircraft_id = input("Enter Aircraft ID: ")
        if not validate_existence(cursor, "Aircraft", "Aircraft_ID", aircraft_id):
            print("Error: Aircraft not found.")
            return

        # Ask the user for the new maintenance date
        print("\nUpdate Last Inspection Date:")
        print("1. Set to Today's Date")
        print("2. Enter a Custom Date")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Set the last inspection date to today
            new_date = datetime.now().strftime("%Y-%m-%d")
        elif choice == "2":
            new_date = input("Enter the new maintenance date (YYYY-MM-DD): ")
            # Validate the entered date
            if not validate_date_input(new_date):
                print("Error: Invalid date format.")
                return
        else:
            print("Invalid choice.")
            return

        # Update the maintenance date in the database
        query = "UPDATE Aircraft SET Last_Inspection = ? WHERE Aircraft_ID = ?;"
        cursor.execute(query, (new_date, aircraft_id))
        connection.commit()
        print(f"Aircraft ID {aircraft_id} maintenance date updated to {new_date}.")
    except Exception as e:
        print(f"Error: {e}")

def view_aircraft_usage():
    # Displays the number of flights each aircraft has been used for.
    try:
        query = """
        SELECT Aircraft.Aircraft_ID, Aircraft.Model_No, COUNT(Flights.Flight_ID) AS FlightCount FROM Aircraft
        LEFT JOIN Flights ON Aircraft.Aircraft_ID = Flights.Aircraft_ID
        GROUP BY Aircraft.Aircraft_ID;
        """
        cursor.execute(query)
        aircraft_usage = cursor.fetchall()
        if not aircraft_usage:
            print("No aircraft found.")
            return

        print("\nAircraft Usage:")
        for row in aircraft_usage:
            print(f"Aircraft ID: {row[0]}, Model: {row[1]}, Flights: {row[2]}")
    except Exception as e:
        print(f"Error: {e}")


### ~~~ Main Menu ~~~ ###
def main_menu():
    # Display the main menu that calls the 4 different sub menus
    while True:
        print("\n=== Flight Management System ===")
        print("1. Find a Flight")
        print("2. Find a Pilot")
        print("3. Create or Delete a Flight")
        print("4. View Aircraft Stats")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            find_flight_menu()
        elif choice == "2":
            find_pilot_menu()
        elif choice == "3":
            add_or_remove_flight_menu()
        elif choice == "4":
            view_aircraft_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
    connection.close()

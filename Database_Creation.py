import sqlite3

db_file = "Flight_Management.db"
connection = sqlite3.connect(db_file)
cursor = connection.cursor()

# Creates the tables in the database
Tables = [
    """
    CREATE TABLE Pilot (
        Pilot_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Years_Experience INTEGER,
        Contact_No INTEGER,
        Email TEXT
    );
    """,
    """
    CREATE TABLE Pilots_Assigned (
        Pilots_Assigned_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Flight_ID INTEGER,
        Pilot_ID INTEGER,
        Role TEXT,
        FOREIGN KEY (Flight_ID) REFERENCES Flights(Flight_ID),
        FOREIGN KEY (Pilot_ID) REFERENCES Pilots(Pilot_ID)
    );
    """,
    """
    CREATE TABLE Flights (
        Flight_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Departure_Airport_ID INTEGER,
        Arrival_Airport_ID INTEGER,
        Departure_Date DATETIME,
        Arrival_Date DATETIME,
        Status TEXT,
        Aircraft_ID INTEGER,
        FOREIGN KEY (Departure_Airport_ID) REFERENCES Destinations(Airport_ID)
        FOREIGN KEY (Arrival_Airport_ID) REFERENCES Destinations(Airport_ID)
        FOREIGN KEY (Aircraft_ID) REFERENCES Aircraft(Aircraft_ID)
    );
    """,
    """
    CREATE TABLE Destinations (
        Airport_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Airport_Name TEXT,
        City TEXT,
        Country TEXT
    );
    """,
    """
    CREATE TABLE Aircraft(
        Aircraft_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Model_No INTEGER,
        Build_Date DATE,
        Capacity INTEGER,
        Milage INTEGER,
        Last_Inspection DATE
    );
    """
]

# Iterates through the tables and executes the queries
for table in Tables:
    cursor.execute(table)

# Inserts the data into the tables
Data = [
    """
    INSERT INTO Pilot (Name, Years_Experience, Contact_No, Email)
    VALUES
    ('Alice Johnson', 15, 1234567890, 'alice.johnson@example.com'),
    ('Bob Smith', 10, 1234567891, 'bob.smith@example.com'),
    ('Charlie Brown', 7, 1234567892, 'charlie.brown@example.com'),
    ('Diana Green', 20, 1234567893, 'diana.green@example.com'),
    ('Evan White', 8, 1234567894, 'evan.white@example.com'),
    ('Fiona Black', 12, 1234567895, 'fiona.black@example.com'),
    ('George Blue', 5, 1234567896, 'george.blue@example.com'),
    ('Hannah Red', 3, 1234567897, 'hannah.red@example.com'),
    ('Ivy Silver', 9, 1234567898, 'ivy.silver@example.com'),
    ('Jack Gold', 14, 1234567899, 'jack.gold@example.com');
    """,
    """
    INSERT INTO Pilots_Assigned (Flight_ID, Pilot_ID, Role)
    VALUES
    (1, 1, 'Captain'),
    (1, 2, 'Co-Pilot'),
    (2, 3, 'Captain'),
    (2, 4, 'Co-Pilot'),
    (3, 5, 'Captain'),
    (4, 6, 'Captain'),
    (5, 7, 'Captain'),
    (6, 8, 'Co-Pilot'),
    (7, 9, 'Captain'),
    (8, 10, 'Co-Pilot'),
    (9, 2, 'Captain'),
    (10, 3, 'Co-Pilot');
    """,
    """
    INSERT INTO Flights (Departure_Airport_ID, Arrival_Airport_ID, Departure_Date, Arrival_Date, Status, Aircraft_ID)
    VALUES
    (1, 2, '2024-12-01 08:00', '2024-12-01 16:00', 'Scheduled', 1),
    (2, 3, '2024-12-02 09:00', '2024-12-02 17:00', 'Scheduled', 2),
    (3, 4, '2024-12-03 10:00', '2024-12-03 18:00', 'Delayed', 3),
    (4, 5, '2024-12-04 11:00', '2024-12-04 19:00', 'Scheduled', 4),
    (5, 6, '2024-12-05 12:00', '2024-12-05 20:00', 'Canceled', 5),
    (6, 7, '2024-12-06 13:00', '2024-12-06 21:00', 'Scheduled', 6),
    (7, 8, '2024-12-07 14:00', '2024-12-07 22:00', 'Delayed', 7),
    (8, 9, '2024-12-08 15:00', '2024-12-08 23:00', 'Scheduled', 8),
    (9, 10, '2024-12-09 16:00', '2024-12-10 00:00', 'Scheduled', 9),
    (10, 1, '2024-12-10 17:00', '2024-12-10 01:00', 'Scheduled', 10);
    """,
    """
    INSERT INTO Destinations (Airport_Name, City, Country)
    VALUES
    ('Heathrow Airport', 'London', 'United Kingdom'),
    ('John F. Kennedy Airport', 'New York', 'United States'),
    ('Charles de Gaulle Airport', 'Paris', 'France'),
    ('Tokyo International Airport', 'Tokyo', 'Japan'),
    ('Dubai International Airport', 'Dubai', 'United Arab Emirates'),
    ('Frankfurt Airport', 'Frankfurt', 'Germany'),
    ('Changi Airport', 'Singapore', 'Singapore'),
    ('Sydney Airport', 'Sydney', 'Australia'),
    ('Cape Town International Airport', 'Cape Town', 'South Africa'),
    ('Los Angeles International Airport', 'Los Angeles', 'United States');
    """,
    """
    INSERT INTO Aircraft (Model_No, Build_Date, Capacity, Milage, Last_Inspection)
    VALUES
    (737, '2015-05-20', 80, 15000, '2023-11-01'),
    (747, '2010-03-15', 90, 20000, '2024-09-15'),
    (320, '2018-07-10', 100, 12000, '2024-10-05'),
    (787, '2020-01-25', 120, 5000, '2023-08-20'),
    (330, '2012-06-30', 50, 18000, '2023-07-15'),
    (350, '2019-12-12', 65, 8000, '2024-09-25'),
    (767, '2011-09-14', 20, 22000, '2023-10-30'),
    (777, '2016-04-02', 500, 14000, '2024-06-10'),
    (319, '2017-11-11', 17, 11000, '2024-05-22'),
    (321, '2021-03-05', 85, 4000, '2023-07-05');
    """
]

# Iterates through the data for each tables and executes the queries
for data in Data:
    cursor.execute(data)

connection.commit()
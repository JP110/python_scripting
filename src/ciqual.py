import csv
import sqlite3
import argparse

def create_db(csv_file):
    #Connect to the database ciqual
    conn = sqlite3.connect("ciqual.db")
    cursor = conn.cursor()

    # Delete table if they already exists
    cursor.execute("""
        DROP TABLE IF EXISTS Nutrient
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS Grp
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS Food
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS NutData
    """)

    #Create tables
    cursor.execute("""
        CREATE TABLE Nutrient (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE Grp (
            id TEXT PRIMARY KEY,
            name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE Food (
            id TEXT PRIMARY KEY,
            name TEXT,
            grp_id TEXT,
            FOREIGN KEY (grp_id) REFERENCES Grp(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE NutData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id TEXT,
            nutrient_id INTEGER,
            value TEXT,
            FOREIGN KEY (food_id) REFERENCES Food(id),
            FOREIGN KEY (nutrient_id) REFERENCES Nutrient(id)
        )
    """)

    # Open the CSV file
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # Read the first row to get column names
        name_columns = next(reader)
        for h in range(13,len(name_columns)):
                nutrient_name = name_columns[h]
                cursor.execute("INSERT INTO Nutrient (name) VALUES (?)", (nutrient_name,))

        for row in reader:
                 # Insert into the Grp table
                grp_id = row[0]
                grp_name = row[3]
                cursor.execute("INSERT OR REPLACE INTO Grp (id, name) VALUES (?, ?)", (grp_id, grp_name))

                # Insert into the Food table
                food_id = row[6]
                food_name = row[7]
                cursor.execute("INSERT OR REPLACE INTO Food (id, name, grp_id) VALUES (?, ?, ?)", (food_id, food_name, grp_id))

                # Insert into the NutData table
                for h in range(13,len(name_columns)):
                    valeur = row[h]
                    aa = valeur.replace("<","").replace(">","")
                    cursor.execute("SELECT id FROM Nutrient WHERE name = ?", (name_columns[h],))
                    result = cursor.fetchone()
                    cursor.execute("INSERT INTO NutData (food_id, nutrient_id, value) VALUES (?, ?, ?)", (food_id, result[0], aa))


    # Execute the SELECT query to retrieve the top 10 values of calcium
    query = """
        SELECT Food.name , CAST(NutData.value AS DECIMAL) AS casted_value
        FROM NutData, Food, Nutrient
        WHERE Nutrient.name = 'Calcium (mg/100 g)' AND  NutData.food_id = Food.id AND  NutData.nutrient_id = Nutrient.id
        ORDER BY casted_value DESC
        LIMIT 10;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Display the results
    for result in results:
        print(result)


    # Commit and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
     #instruct parser to parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to the csv file")
    args = parser.parse_args()

    create_db(args.file) 
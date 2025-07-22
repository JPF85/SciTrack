import json
import mysql.connector

json_file = r"C:\Jack\code\SciTrack\data\2025-07-22_12-44-28_spectra.json"

with open(json_file, 'r') as file:
    data = json.load(file)

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='myPassword',  # replace with your actual password
    database='scitrack',
)
cursor = conn.cursor()

for entry in data:
    try:
        # Insert into Spectra table
        cursor.execute(
            """
            INSERT INTO Spectra (sName, formula, numPeaks, contributor, casNo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                entry['Name'],
                entry['Formula'],
                int(entry['Num peaks']),
                "NIST",
                entry['CASNO']
            )
        )
        # Retreive spID of this entry
        spID = cursor.lastrowid

        # Insert into Intensities table
        for mz, intensity in zip(entry['mzs'], entry['intensities']):
            cursor.execute(
                """
                INSERT INTO Intensities (spID, mz, intensity)
                VALUES (%s, %s, %s)
                """,
                (spID, mz, intensity)
            )

    except mysql.connector.Error as err:
        print(f"Error inserting entry {entry.get('Name', 'unknown')}: {err}")

# commit changes
conn.commit()
print(f"Data loaded successfully")

# close connection
cursor.close()
conn.close()

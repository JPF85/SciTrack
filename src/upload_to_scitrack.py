import json
import mysql.connector
from pathlib import Path

# Get the path to the script's directory (src)
base_dir = Path(__file__).resolve().parent

# connect to database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='myPassword',  # replace with your actual password
    database='scitrack',
)
cursor = conn.cursor()

# region remove data from DB before repopulating

# Get list of all tables in the current database
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

# remove data from tables before inserting our new data
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
for (table_name,) in tables:  # fetchall returns list of tuples
    cursor.execute(f"TRUNCATE TABLE `{table_name}`;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
conn.commit()

# endregion

# region populate spectra/intensity tables with nist-based (falsified) data -----------------------------------------------------------------------------------------------------

nist_path = base_dir.parent / "data" / "2025-07-22_12-44-28_spectra.json"

with open(nist_path, 'r') as file:
    data = json.load(file)

# counts for spectra and intnsities
sp_count = 0
in_count = 0

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
        # increment spectra counter
        sp_count += 1

        # Insert into Intensities table
        for mz, intensity in zip(entry['mzs'], entry['intensities']):
            cursor.execute(
                """
                INSERT INTO Intensities (spID, mz, intensity)
                VALUES (%s, %s, %s)
                """,
                (spID, mz, intensity)
            )
            # increment intensity counter
            in_count += 1

    except mysql.connector.Error as err:
        print(f"Error inserting entry {entry.get('Name', 'unknown')}: {err}")

# commit changes
conn.commit()
print(f"Synthetic NIST DB loaded successfully")
print(f"Spectra: {sp_count}")
print(f"Intensities: {in_count}")

# endregion

# region populate members table -------------------------------------------------------------------------------------------------------------------------------------------------

mem_path = base_dir.parent / "data" / "members.json"

with open(mem_path, 'r') as f:
    data = json.load(f)

for entry in data:
    try:
        # Insert into Spectra table
        cursor.execute(
            """
            INSERT INTO Member (memName, email, memType, memStart, memEnd, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                entry['memName'],
                entry['email'],
                entry['memType'],
                entry['memStart'],
                entry['memEnd'],
                entry['phone']
            )
        )

    except mysql.connector.Error as err:
        print(f"Error inserting entry {entry.get('memName', 'unknown')}: {err}")

# commit changes
conn.commit()
print(f"Members loaded successfully")
print(f"Number of Members: {len(data)}")

# endregion

# region populate pi table ------------------------------------------------------------------------------------------------------------------------------------------------------

pi_path = base_dir.parent / "data" / "20250723_141344_pi_table.json"

with open(pi_path, 'r') as f:
    data = json.load(f)

for entry in data:
    try:
        # Insert into Spectra table
        cursor.execute(
            """
            INSERT INTO PrmaryInvestigator (empID, piID)
            VALUES (%s, %s)
            """,
            (
                entry['empID'],
                entry['piID']
            )
        )

    except mysql.connector.Error as err:
        print(f"Error inserting entry {entry.get('empID', 'unknown')}: {err}")

# commit changes
conn.commit()
print(f"PI table loaded successfully")
print(f"Relationships logged: {len(data)}")

# endregion

# region populate supervisor table ----------------------------------------------------------------------------------------------------------------------------------------------

sup_path = base_dir.parent / "data" / "20250723_141344_supervisor_table.json"

with open(sup_path, 'r') as f:
    data = json.load(f)

for entry in data:
    try:
        # Insert into Spectra table
        cursor.execute(
            """
            INSERT INTO Supervisor (subID, superID, supStart, supEnd)
            VALUES (%s, %s, %s, %s)
            """,
            (
                entry['subID'],
                entry['superID'],
                entry['supStart'],
                entry['supEnd']
            )
        )

    except mysql.connector.Error as err:
        print(f"Error inserting entry {entry.get('subID', 'unknown')}: {err}")

# commit changes
conn.commit()
print(f"Supervisor table loaded successfully")
print(f"Relationships logged: {len(data)}")

#endregion

# close connection
cursor.close()
conn.close()

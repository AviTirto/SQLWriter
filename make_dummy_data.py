import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('company.db')

# Create a cursor object
cursor = connection.cursor()

# Create the 'employee' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary INTEGER NOT NULL
);
'''
cursor.execute(create_table_query)

# Data to insert into the 'employee' table
employees = [
    ("John Doe", "Engineering", 70000),
    ("Jane Smith", "Human Resources", 65000),
    ("Alice Johnson", "Marketing", 72000),
    ("Bob Brown", "Sales", 68000),
    ("Charlie Black", "Engineering", 71000),
    ("Daisy White", "Human Resources", 66000),
    ("Edward Green", "Marketing", 69000),
    ("Fiona Grey", "Sales", 64000),
    ("George Yellow", "Engineering", 73000),
    ("Hannah Blue", "Human Resources", 61000),
    ("Ivan Purple", "Marketing", 75000),
    ("Jessica Cyan", "Sales", 70000),
    ("Kyle Red", "Engineering", 68000),
    ("Lily Orange", "Human Resources", 67000),
    ("Martin Indigo", "Marketing", 72000),
    ("Nina Teal", "Sales", 65000),
    ("Oscar Lime", "Engineering", 73000),
    ("Penny Olive", "Human Resources", 62000),
    ("Quentin Silver", "Marketing", 74000),
    ("Rachel Maroon", "Sales", 69000),
    ("Steve Pink", "Engineering", 71000),
    ("Tina Violet", "Human Resources", 68000),
    ("Ursula Gold", "Marketing", 76000),
    ("Victor Bronze", "Sales", 64000),
    ("Wendy Mauve", "Engineering", 69000),
    ("Xavier Cream", "Human Resources", 65000),
    ("Yolanda Peach", "Marketing", 70000),
    ("Zack Sage", "Sales", 68000),
    ("Abby Coral", "Engineering", 72000),
    ("Bill Moss", "Human Resources", 63000)
]

# Insert data into the 'employee' table
insert_query = 'INSERT INTO employee (employee_name, department, salary) VALUES (?, ?, ?);'
cursor.executemany(insert_query, employees)

# Commit the changes
connection.commit()

# Close the connection
connection.close()

print("Table created and data inserted successfully.")
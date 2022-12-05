import sqlite3

# Open database
conn = sqlite3.connect('database.db')

# Create table
conn.execute('''CREATE TABLE users
		(userId INTEGER PRIMARY KEY,
		password TEXT,
		email TEXT,
		firstName TEXT,
		lastName TEXT,
		state TEXT,
		phone TEXT
		)''')

conn.execute('''CREATE TABLE meal_items
		(mealId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		description TEXT,
		image TEXT,
		categoryId INTEGER,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')


conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')

conn.execute('''CREATE TABLE cart (userId INTEGER, mealId INTEGER, FOREIGN KEY(userId) REFERENCES users(userId), FOREIGN KEY(mealId) REFERENCES meal_items(mealId))''')


conn.close()

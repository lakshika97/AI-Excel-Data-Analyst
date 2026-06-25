import sqlite3

conn = sqlite3.connect("company_sales.db")
cursor = conn.cursor()

#Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMERY KEY,
    name TEXT,
    category TEXT,
    price REAL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMERY KEY,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)""")

# Seed Mock Data
cursor.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?,?)", [
    (1, 'M3 MacBook Pro', 'Electronics', 3499.00),
    (2, '4K Ergonomic Monitor', 'Electronics', 899.00),
    (3, 'Mechanical Keyboard', 'Accessories', 189.00),
    (4, 'Noise Cancelling Headphones', 'Electronics', 450.00)
])

cursor.executemany("INSERT OR IGNORE INTO orders VALUES (?,?,?,?)", [
    (101, 1, 2, '2026-06-20'),
    (102, 3, 5, '2026-06-21'),
    (103, 2, 1, '2026-06-22'),
    (104, 4, 3, '2026-06-23')
])

conn.commit()
conn.close()
print("Database 'company_sales.db' created and seeded successfully!")
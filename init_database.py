"""
Database Initialization Script
Creates SQLite database and populates it with sample sales data
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    """Create database and tables"""
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    
    # Read and execute schema
    with open('schema.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    print("✓ Database and tables created successfully")
    return conn

def generate_sample_data():
    """Generate realistic sample sales data"""
    products = [
        ('Laptop', 800, 1200),
        ('Mouse', 15, 50),
        ('Keyboard', 30, 100),
        ('Monitor', 150, 400),
        ('Headphones', 25, 150),
        ('Webcam', 40, 120),
        ('USB Cable', 5, 20),
        ('External HDD', 60, 150),
        ('SSD Drive', 80, 250),
        ('Graphics Card', 300, 800),
        ('RAM Module', 50, 200),
        ('Power Supply', 60, 150),
        ('Cooling Fan', 15, 50),
        ('Motherboard', 120, 350),
        ('Processor', 200, 600)
    ]
    
    sales_data = []
    start_date = datetime.now() - timedelta(days=365)
    
    # Generate sales for the past year
    for _ in range(500):  # 500 sales records
        product_name, min_price, max_price = random.choice(products)
        quantity = random.randint(1, 10)
        price = round(random.uniform(min_price, max_price), 2)
        
        # Random date within the past year
        days_ago = random.randint(0, 365)
        sale_date = (start_date + timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        sales_data.append((product_name, quantity, price, sale_date))
    
    return sales_data

def populate_database(conn, sales_data):
    """Insert sample data into database"""
    cursor = conn.cursor()
    
    cursor.executemany(
        'INSERT INTO sales (product, quantity, price, sale_date) VALUES (?, ?, ?, ?)',
        sales_data
    )
    
    conn.commit()
    print(f"✓ Inserted {len(sales_data)} sales records")

def display_sample_records(conn):
    """Display first few records"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales LIMIT 5')
    records = cursor.fetchall()
    
    print("\n📊 Sample Records:")
    print("-" * 80)
    print(f"{'ID':<5} {'Product':<20} {'Quantity':<10} {'Price':<10} {'Date':<12}")
    print("-" * 80)
    for record in records:
        print(f"{record[0]:<5} {record[1]:<20} {record[2]:<10} ${record[3]:<9.2f} {record[4]:<12}")
    print("-" * 80)

def main():
    """Main initialization function"""
    print("🚀 Initializing Sales Database...\n")
    
    # Create database
    conn = create_database()
    
    # Generate and populate data
    sales_data = generate_sample_data()
    populate_database(conn, sales_data)
    
    # Display sample
    display_sample_records(conn)
    
    # Get total count
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM sales')
    total = cursor.fetchone()[0]
    print(f"\n✅ Database initialized successfully with {total} records!")
    
    conn.close()

if __name__ == '__main__':
    main()

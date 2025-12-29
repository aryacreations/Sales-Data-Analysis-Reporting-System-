-- Sales Data Analysis Database Schema

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    sale_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_product ON sales(product);
CREATE INDEX IF NOT EXISTS idx_sale_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_created_at ON sales(created_at);

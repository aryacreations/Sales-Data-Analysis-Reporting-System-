# Sales Data Analysis & Reporting System

A comprehensive sales data analysis system that uses **SQL** for data storage, **Pandas** for data manipulation, and **NumPy** for statistical calculations and revenue analysis.

## Features

- **SQL Database**: SQLite database for storing sales records
- **Data Analysis**: Comprehensive analysis using Pandas and NumPy
- **Revenue Calculations**: Total revenue, average sale value, and statistical measures
- **Trend Analysis**: Monthly sales trends and patterns
- **Product Analysis**: Best-selling products by revenue and quantity
- **Visualizations**: Beautiful charts and graphs for data insights
- **Interactive Dashboard**: Streamlit web dashboard with real-time filtering and exploration

## 📊 What the Project Does

1. **Load sales data from SQL database**
2. **Compute key metrics**:
   - Total revenue (using NumPy)
   - Average sale value
   - Monthly sales trends
   - Best-selling products
   - Statistical measures (mean, median, std dev)
3. **Generate comprehensive reports**
4. **Create visualizations**:
   - Monthly revenue trends
   - Top products by revenue
   - Sales distribution analysis
   - Quantity vs revenue comparison
5. **Interactive Web Dashboard**:
   - Real-time data filtering by date and product
   - Interactive charts with Plotly
   - KPI metrics display
   - Data export capabilities

## 🗄️ Database Structure

```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    sale_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd d:\oldprojects\sales-data-analysis
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Option 1: Interactive Dashboard (Recommended) 🌟

Launch the Streamlit web dashboard for interactive data exploration:

```bash
streamlit run dashboard.py
```

This will open a web browser with an interactive dashboard featuring:
- 📊 Real-time KPI metrics
- 📈 Interactive charts and visualizations
- 🔍 Date range and product filtering
- 💾 Data export capabilities
- 📱 Responsive design

### Option 2: Run Complete Analysis

Run the main script to execute the full analysis pipeline:

```bash
python main.py
```

This will:
- Initialize the database (if not exists)
- Populate with sample data
- Run comprehensive analysis
- Generate all visualizations

### Option 3: Run Individual Components

**Initialize Database Only**:
```bash
python init_database.py
```

**Run Analysis Only**:
```bash
python sales_analysis.py
```

**Generate Visualizations Only**:
```bash
python visualizations.py
```

## 📁 Project Structure

```
sales-data-analysis/
├── schema.sql              # Database schema definition
├── init_database.py        # Database initialization script
├── sales_analysis.py       # Main analysis module (Pandas + NumPy)
├── visualizations.py       # Visualization module (Matplotlib)
├── dashboard.py            # Streamlit interactive dashboard
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── sales.db               # SQLite database (generated)
```

## 📈 Sample Output

The system generates:

1. **Console Report**:
   - Overall statistics (revenue, avg sale, total items sold)
   - Top 10 best-selling products
   - Monthly sales trends
   - Monthly revenue statistics

2. **Visualizations**:
   - `monthly_revenue_trend.png` - Line chart of monthly revenue
   - `top_products.png` - Bar chart of top products
   - `sales_distribution.png` - Histogram and box plot of sales
   - `quantity_vs_revenue.png` - Dual-axis chart comparing quantity and revenue

## 🛠️ Technologies Used

- **Python 3.x**
- **SQLite** - Database storage
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical calculations and statistics
- **Matplotlib** - Static data visualization
- **Streamlit** - Interactive web dashboard
- **Plotly** - Interactive charts and graphs

## 📊 Key Metrics Calculated

- **Total Revenue**: Sum of all sales (quantity × price)
- **Average Sale Value**: Mean revenue per transaction
- **Median Sale Value**: Middle value of all sales
- **Standard Deviation**: Measure of sales variability
- **Monthly Trends**: Revenue, quantity, and transaction count by month
- **Product Performance**: Revenue, quantity sold, and average price per product

## 🎨 Visualization Features

- Color-coded charts with gradients
- Trend lines and averages
- Statistical annotations
- Professional styling with grid lines
- High-resolution output (300 DPI)

## 📝 Sample Data

The system includes a data generator that creates realistic sales data for:
- 15 different products (electronics)
- 500 sales transactions
- 12 months of historical data
- Varied quantities and prices

## 🔧 Customization

You can customize the analysis by modifying:

- **Number of records**: Change the range in `generate_sample_data()` in `init_database.py`
- **Products**: Modify the `products` list in `init_database.py`
- **Top N products**: Change the `top_n` parameter in analysis functions
- **Date range**: Adjust `timedelta(days=365)` for different time periods

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a demonstration of SQL, Pandas, and NumPy integration for sales data analysis.

---

**Happy Analyzing! 📊**

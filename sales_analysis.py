"""
Sales Data Analysis Module
Uses Pandas for data manipulation and NumPy for calculations
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

class SalesAnalyzer:
    """Main class for sales data analysis"""
    
    def __init__(self, db_path='sales.db'):
        """Initialize analyzer with database connection"""
        self.db_path = db_path
        self.df = None
        
    def load_data(self):
        """Load sales data from SQL database into Pandas DataFrame"""
        conn = sqlite3.connect(self.db_path)
        
        query = """
        SELECT id, product, quantity, price, sale_date
        FROM sales
        ORDER BY sale_date
        """
        
        self.df = pd.read_sql_query(query, conn)
        self.df['sale_date'] = pd.to_datetime(self.df['sale_date'])
        
        conn.close()
        print(f"✓ Loaded {len(self.df)} sales records\n")
        
        return self.df
    
    def calculate_total_revenue(self):
        """Calculate total revenue using NumPy"""
        if self.df is None:
            self.load_data()
        
        # Calculate revenue for each sale
        revenue_array = np.array(self.df['quantity']) * np.array(self.df['price'])
        total_revenue = np.sum(revenue_array)
        
        return total_revenue
    
    def calculate_monthly_trends(self):
        """Analyze monthly sales trends"""
        if self.df is None:
            self.load_data()
        
        # Add revenue column
        self.df['revenue'] = self.df['quantity'] * self.df['price']
        
        # Extract year-month
        self.df['year_month'] = self.df['sale_date'].dt.to_period('M')
        
        # Group by month
        monthly_sales = self.df.groupby('year_month').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'id': 'count'
        }).rename(columns={'id': 'num_sales'})
        
        # Calculate statistics using NumPy
        monthly_revenue = np.array(monthly_sales['revenue'])
        monthly_sales['avg_revenue'] = np.mean(monthly_revenue)
        monthly_sales['std_revenue'] = np.std(monthly_revenue)
        
        return monthly_sales
    
    def find_best_selling_products(self, top_n=10):
        """Find best-selling products by revenue and quantity"""
        if self.df is None:
            self.load_data()
        
        # Calculate revenue
        self.df['revenue'] = self.df['quantity'] * self.df['price']
        
        # Group by product
        product_stats = self.df.groupby('product').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'id': 'count',
            'price': 'mean'
        }).rename(columns={'id': 'num_sales', 'price': 'avg_price'})
        
        # Sort by revenue
        product_stats = product_stats.sort_values('revenue', ascending=False)
        
        return product_stats.head(top_n)
    
    def calculate_statistics(self):
        """Calculate various statistical measures using NumPy"""
        if self.df is None:
            self.load_data()
        
        # Calculate revenue
        revenue = np.array(self.df['quantity']) * np.array(self.df['price'])
        
        stats = {
            'total_revenue': np.sum(revenue),
            'average_sale_value': np.mean(revenue),
            'median_sale_value': np.median(revenue),
            'std_sale_value': np.std(revenue),
            'min_sale_value': np.min(revenue),
            'max_sale_value': np.max(revenue),
            'total_items_sold': np.sum(self.df['quantity']),
            'total_transactions': len(self.df),
            'average_quantity_per_sale': np.mean(self.df['quantity']),
            'average_price': np.mean(self.df['price'])
        }
        
        return stats
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("=" * 80)
        print("📊 SALES DATA ANALYSIS REPORT")
        print("=" * 80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Overall Statistics
        stats = self.calculate_statistics()
        print("📈 OVERALL STATISTICS")
        print("-" * 80)
        print(f"Total Revenue:              ${stats['total_revenue']:,.2f}")
        print(f"Average Sale Value:         ${stats['average_sale_value']:,.2f}")
        print(f"Median Sale Value:          ${stats['median_sale_value']:,.2f}")
        print(f"Std Dev Sale Value:         ${stats['std_sale_value']:,.2f}")
        print(f"Min Sale Value:             ${stats['min_sale_value']:,.2f}")
        print(f"Max Sale Value:             ${stats['max_sale_value']:,.2f}")
        print(f"Total Items Sold:           {stats['total_items_sold']:,}")
        print(f"Total Transactions:         {stats['total_transactions']:,}")
        print(f"Avg Quantity per Sale:      {stats['average_quantity_per_sale']:.2f}")
        print(f"Average Price:              ${stats['average_price']:,.2f}\n")
        
        # Best Selling Products
        print("🏆 TOP 10 BEST-SELLING PRODUCTS (By Revenue)")
        print("-" * 80)
        best_products = self.find_best_selling_products(10)
        print(f"{'Product':<20} {'Revenue':<15} {'Qty Sold':<12} {'Sales':<10} {'Avg Price':<12}")
        print("-" * 80)
        for product, row in best_products.iterrows():
            print(f"{product:<20} ${row['revenue']:>12,.2f}  {row['quantity']:>8,}    {row['num_sales']:>6}    ${row['avg_price']:>8,.2f}")
        print()
        
        # Monthly Trends
        print("📅 MONTHLY SALES TRENDS")
        print("-" * 80)
        monthly = self.calculate_monthly_trends()
        print(f"{'Month':<12} {'Revenue':<15} {'Quantity':<12} {'# Sales':<10}")
        print("-" * 80)
        for month, row in monthly.iterrows():
            print(f"{str(month):<12} ${row['revenue']:>12,.2f}  {row['quantity']:>8,}    {row['num_sales']:>6}")
        print()
        
        # Monthly Statistics
        monthly_revenue = np.array(monthly['revenue'])
        print("📊 MONTHLY REVENUE STATISTICS")
        print("-" * 80)
        print(f"Average Monthly Revenue:    ${np.mean(monthly_revenue):,.2f}")
        print(f"Median Monthly Revenue:     ${np.median(monthly_revenue):,.2f}")
        print(f"Std Dev Monthly Revenue:    ${np.std(monthly_revenue):,.2f}")
        print(f"Best Month Revenue:         ${np.max(monthly_revenue):,.2f}")
        print(f"Worst Month Revenue:        ${np.min(monthly_revenue):,.2f}")
        
        print("\n" + "=" * 80)
        print("✅ Report Generated Successfully!")
        print("=" * 80)
        
        return stats, best_products, monthly

def main():
    """Main function to run analysis"""
    analyzer = SalesAnalyzer()
    analyzer.load_data()
    analyzer.generate_summary_report()

if __name__ == '__main__':
    main()

"""
Main Entry Point for Sales Data Analysis System
Orchestrates database initialization, analysis, and reporting
"""

from init_database import main as init_db
from sales_analysis import SalesAnalyzer
from visualizations import SalesVisualizer
import os

def main():
    """Main application entry point"""
    print("\n" + "=" * 80)
    print("🚀 SALES DATA ANALYSIS & REPORTING SYSTEM")
    print("=" * 80 + "\n")
    
    # Check if database exists
    db_exists = os.path.exists('sales.db')
    
    if not db_exists:
        print("📦 Database not found. Initializing...\n")
        init_db()
        print("\n")
    else:
        print("✓ Database found. Loading data...\n")
    
    # Run analysis
    print("🔍 Running Sales Analysis...\n")
    analyzer = SalesAnalyzer()
    analyzer.load_data()
    stats, products, monthly = analyzer.generate_summary_report()
    
    # Generate visualizations
    print("\n📊 Generating Visualizations...\n")
    visualizer = SalesVisualizer(analyzer)
    visualizer.generate_all_visualizations()
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\n📁 Generated Files:")
    print("   - sales.db (SQLite Database)")
    print("   - monthly_revenue_trend.png")
    print("   - top_products.png")
    print("   - sales_distribution.png")
    print("   - quantity_vs_revenue.png")
    print("\n" + "=" * 80 + "\n")

if __name__ == '__main__':
    main()
